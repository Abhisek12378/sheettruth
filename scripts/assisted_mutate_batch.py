"""Assisted mutation through the Message Batches API: submit once, collect later.

The one-by-one script (assisted_mutate.py) sends each proposal request and applies the reply as it
arrives. This script does the same work in two steps so that all requests travel as one batch:

  submit   pick the seed cells, send every proposal request as one Message Batch, and save a
           manifest (batch id, model, preferred types) plus the seeds next to it
  status   print how far the batch has come
  collect  once the batch has ended, read every reply, validate it, apply it to a copy of the
           workbook, recalculate, rebuild the window and append the kept examples to examples.jsonl

Seeds, prompts, validation and the apply step are shared with assisted_mutate.py, so the records
written here have the same shape and the same `assisted-<seed id>` ids. `collect` can be run again
after an interruption: seeds already written to examples.jsonl are skipped.

Usage (run from the project root):
  ANTHROPIC_API_KEY=... python scripts/assisted_mutate_batch.py submit data/dataset/enron_v2/examples.jsonl \\
      --xlsx data/xlsx/enron --out data/dataset/enron_opus --name range --count 750 --model <model id> \\
      --preferred "extra_rows, skipped_rows"
  python scripts/assisted_mutate_batch.py status --out data/dataset/enron_opus --name range
  python scripts/assisted_mutate_batch.py collect --out data/dataset/enron_opus --name range --xlsx data/xlsx/enron
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import random
import sys
import time
import warnings
from pathlib import Path

import yaml

warnings.filterwarnings("ignore")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import assisted_mutate as am  # noqa: E402
from sheettruth.data.recalc import Recalculator  # noqa: E402

PROGRESS_EVERY = 25
SLOW_APPLY_SECONDS = 20


def manifest_path(out_dir: Path, name: str) -> Path:
    return out_dir / f"batch_{name}.json"


def seeds_path(out_dir: Path, name: str) -> Path:
    return out_dir / f"batch_{name}_seeds.jsonl"


def load_manifest(out_dir: Path, name: str) -> dict:
    path = manifest_path(out_dir, name)
    if not path.exists():
        sys.exit(f"no manifest at {path}; run submit first")
    return json.loads(path.read_text())


def seed_ids_in(paths: list[str]) -> set[str]:
    """Seed ids already used by other batches (their seeds files), so batches stay disjoint."""
    used: set[str] = set()
    for p in paths:
        if p and Path(p).exists():
            used.update(e["id"] for e in am.load_jsonl(p))
    return used


def build_request(example: dict, model: str, preferred: str) -> dict:
    prompt = am.PROPOSAL_PROMPT.format(guide=am.TYPE_GUIDE, preferred=preferred,
                                       window=example["window"], formula=example["original_formula"])
    return {
        "custom_id": example["id"],
        "params": {
            "model": model,
            "max_tokens": am.MAX_REPLY_TOKENS,
            "output_config": {"effort": "low"},
            "messages": [{"role": "user", "content": prompt}],
        },
    }


def parse_reply_text(text: str) -> dict | None:
    start, end = text.find("{"), text.rfind("}")
    if start < 0 or end < start:
        return None
    try:
        return json.loads(text[start:end + 1])
    except ValueError:
        return None


def message_text(message) -> str:
    return "".join(b.text for b in message.content if getattr(b, "type", "") == "text")


def pick_seeds(args, rng: random.Random, out_dir: Path) -> list[dict]:
    """Fresh seed cells: not already written to examples.jsonl and not in another batch's seeds."""
    already = am.done_sources(out_dir / "examples.jsonl") | seed_ids_in(args.exclude.split(","))
    pool = am.pick_sources(am.load_jsonl(args.examples), args.count + len(already), rng, args.xlsx,
                           args.max_file_kb)
    return [e for e in pool if e["id"] not in already][: args.count]


def make_client():
    try:
        import anthropic
    except ImportError:
        sys.exit("pip install anthropic")
    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("set ANTHROPIC_API_KEY")
    return anthropic.Anthropic(timeout=am.API_TIMEOUT_SECONDS, max_retries=2)


def cmd_submit(args) -> None:
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    if manifest_path(out_dir, args.name).exists():
        sys.exit(f"batch '{args.name}' already submitted; pick another --name")
    seeds = pick_seeds(args, random.Random(args.seed), out_dir)
    if not seeds:
        sys.exit("no fresh seed cells left")
    client = make_client()
    batch = client.messages.batches.create(requests=[build_request(e, args.model, args.preferred) for e in seeds])
    with open(seeds_path(out_dir, args.name), "w") as f:
        for e in seeds:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")
    manifest = {"batch_id": batch.id, "name": args.name, "model": args.model, "preferred": args.preferred,
                "seeds": len(seeds), "created_at": str(batch.created_at), "config": args.config}
    manifest_path(out_dir, args.name).write_text(json.dumps(manifest, indent=1))
    print(f"submitted batch {batch.id} with {len(seeds)} requests; manifest {manifest_path(out_dir, args.name)}")


def cmd_status(args) -> None:
    manifest = load_manifest(Path(args.out), args.name)
    batch = make_client().messages.batches.retrieve(manifest["batch_id"])
    counts = batch.request_counts
    print(f"batch {batch.id}: {batch.processing_status}; processing={counts.processing} "
          f"succeeded={counts.succeeded} errored={counts.errored} expired={counts.expired} canceled={counts.canceled}")


def apply_one(example: dict, proposal: dict | None, args, cfg: dict, recalc: Recalculator,
              rng: random.Random) -> dict | None:
    if not am.proposal_is_valid(proposal, example):
        return None
    started = time.time()
    try:
        record = am.apply_proposal(example, proposal, args.xlsx, cfg, recalc, rng)
    except Exception as ex:
        print(f"apply failed for {example['workbook']}: {type(ex).__name__}", file=sys.stderr, flush=True)
        return None
    if time.time() - started > SLOW_APPLY_SECONDS:
        print(f"slow apply {time.time() - started:.0f}s for {example['workbook']}", file=sys.stderr, flush=True)
    return record


def cmd_collect(args) -> None:
    out_dir = Path(args.out)
    manifest = load_manifest(out_dir, args.name)
    client = make_client()
    batch = client.messages.batches.retrieve(manifest["batch_id"])
    if batch.processing_status != "ended":
        sys.exit(f"batch {batch.id} is still {batch.processing_status}; try again later")
    seeds = {e["id"]: e for e in am.load_jsonl(str(seeds_path(out_dir, args.name)))}
    out_path = out_dir / "examples.jsonl"
    already = am.done_sources(out_path)
    cfg = yaml.safe_load(open(manifest.get("config", args.config)))
    rng = random.Random(args.seed)
    recalc = Recalculator(timeout=cfg["recalc"]["timeout_s"])
    tally: collections.Counter = collections.Counter()
    with open(out_path, "a") as f:
        for i, entry in enumerate(client.messages.batches.results(batch.id), 1):
            example = seeds.get(entry.custom_id)
            if example is None or entry.custom_id in already:
                tally["skipped"] += 1
                continue
            if entry.result.type != "succeeded":
                tally[f"request_{entry.result.type}"] += 1
                continue
            proposal = parse_reply_text(message_text(entry.result.message))
            record = apply_one(example, proposal, args, cfg, recalc, rng)
            if record is None:
                tally["rejected"] += 1
                continue
            record["id"] = f"assisted-{example['id']}"
            record["source_id"] = example["id"]
            tally[record["type"]] += 1
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
            f.flush()
            if i % PROGRESS_EVERY == 0:
                print(f"{i}/{len(seeds)} replies, {dict(tally)}", flush=True)
    print(json.dumps(dict(tally), indent=1))


def parse_args():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="command", required=True)

    submit = sub.add_parser("submit", help="send one Message Batch of proposal requests")
    submit.add_argument("examples", help="examples.jsonl from build_dataset.py; its ok examples are the seeds")
    submit.add_argument("--xlsx", required=True, help="root of the converted .xlsx files")
    submit.add_argument("--out", required=True)
    submit.add_argument("--name", required=True, help="short batch name, used in the manifest file names")
    submit.add_argument("--config", default="configs/default.yaml")
    submit.add_argument("--count", type=int, default=750)
    submit.add_argument("--model", required=True, help="model id for the Anthropic API")
    submit.add_argument("--preferred", default="extra_rows, missing_factor, wrong_operator, missing_term, double_count")
    submit.add_argument("--exclude", default="", help="comma-separated seeds files of other batches to stay disjoint from")
    submit.add_argument("--max-file-kb", type=int, default=600, help="skip seed workbooks larger than this")
    submit.add_argument("--seed", type=int, default=11)

    status = sub.add_parser("status", help="print the batch progress")
    status.add_argument("--out", required=True)
    status.add_argument("--name", required=True)

    collect = sub.add_parser("collect", help="apply the replies of an ended batch")
    collect.add_argument("--out", required=True)
    collect.add_argument("--name", required=True)
    collect.add_argument("--xlsx", required=True, help="root of the converted .xlsx files")
    collect.add_argument("--config", default="configs/default.yaml")
    collect.add_argument("--seed", type=int, default=11)
    return ap.parse_args()


def main() -> None:
    args = parse_args()
    commands = {"submit": cmd_submit, "status": cmd_status, "collect": cmd_collect}
    commands[args.command](args)


if __name__ == "__main__":
    main()
