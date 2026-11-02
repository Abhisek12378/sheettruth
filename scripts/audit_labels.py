"""Ask an independent model whether a sample of labels is right, and list the disagreements.

The sample is stratified: the same number of examples from each error type plus the ok class.
For every example the judge sees the window and the label and answers agree / disagree / unsure
with one sentence. Disagreements are written out for a human to read; they are the cells where
either the mutator rule or the judge is wrong, and only reading them tells which.

Usage:
  ANTHROPIC_API_KEY=... python scripts/audit_labels.py data/dataset/final/train_meta.jsonl \\
      data/dataset/enron/examples.jsonl --per-class 40 --out data/dataset/audit --model <reviewer model id>
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import random
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from pathlib import Path

JUDGE_PROMPT = """You are reviewing a training label for a spreadsheet auditing model.

Below is the context window for one formula cell, then the label a rule-based pipeline assigned.
The label says whether the TARGET formula is correct for what its labels and surroundings imply,
and if not, which error type and what the formula should be.

Answer with one JSON object only:
{{"agree": "yes" | "no" | "unsure", "reason": "<one sentence>"}}

Say "no" only if the window itself shows the label is wrong (for example the label says the range
skips rows but the cells past the range end are blank or belong to another block, or the label
says ok but the formula clearly contradicts its row label). Say "unsure" if the window does not
hold enough evidence either way.

=== WINDOW ===
{window}

=== LABEL ===
{label}
"""


def load_jsonl(path: str) -> list[dict]:
    with open(path) as f:
        return [json.loads(line) for line in f if line.strip()]


def stratified_sample(examples: list[dict], per_class: int, rng: random.Random) -> list[dict]:
    by_class: dict[str, list[dict]] = collections.defaultdict(list)
    for e in examples:
        key = e["type"] if e["verdict"] == "error" else e["verdict"]
        if key != "unsupported":
            by_class[key].append(e)
    out = []
    for items in by_class.values():
        rng.shuffle(items)
        out.extend(items[:per_class])
    return out


def label_text(e: dict) -> str:
    if e["verdict"] == "ok":
        return "verdict=ok (the formula is correct as written)"
    return (f"verdict=error, type={e['type']}, formula as written={e.get('broken_formula')}, "
            f"expected={e.get('expected')}, reason={e.get('reason')}")


def judge_one(client, model: str, e: dict) -> dict:
    prompt = JUDGE_PROMPT.format(window=e["window"], label=label_text(e))
    for attempt in range(3):
        try:
            msg = client.messages.create(model=model, max_tokens=400, messages=[{"role": "user", "content": prompt}])
            text = next(b.text for b in msg.content if getattr(b, "type", "") == "text").strip()
            start, end = text.find("{"), text.rfind("}")
            verdict = json.loads(text[start:end + 1])
            return {"id": e["id"], "class": e["type"] or e["verdict"], "agree": verdict.get("agree", "unsure"),
                    "judge_reason": verdict.get("reason", ""), "label": label_text(e), "workbook": e["workbook"],
                    "sheet": e["sheet"], "addr": e["addr"]}
        except Exception as ex:
            time.sleep(2 * (attempt + 1))
            last = str(ex)[:120]
    return {"id": e["id"], "class": e["type"] or e["verdict"], "agree": "failed", "judge_reason": last}


def load_earlier(out_dir: Path) -> dict[str, dict]:
    path = out_dir / "judgements.jsonl"
    if not path.exists():
        return {}
    return {r["id"]: r for r in load_jsonl(str(path))}


def parse_args():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("meta", help="train_meta.jsonl from finalize_dataset.py (ids and labels)")
    ap.add_argument("examples", help="examples.jsonl from build_dataset.py (windows)")
    ap.add_argument("--per-class", type=int, default=40)
    ap.add_argument("--out", required=True)
    ap.add_argument("--model", required=True, help="reviewer model id for the Anthropic API")
    ap.add_argument("--concurrency", type=int, default=4)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--resume", action="store_true", help="keep earlier judgements in --out and redo only failed ones")
    return ap.parse_args()


def make_client():
    try:
        import anthropic
    except ImportError:
        sys.exit("pip install anthropic")
    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("set ANTHROPIC_API_KEY")
    return anthropic.Anthropic()


def build_sample(args) -> list[dict]:
    windows = {e["id"]: e["window"] for e in load_jsonl(args.examples)}
    meta = [e for e in load_jsonl(args.meta) if e["id"] in windows]
    for e in meta:
        e["window"] = windows[e["id"]]
    return stratified_sample(meta, args.per_class, random.Random(args.seed))


def write_outputs(out_dir: Path, results: list[dict]) -> None:
    with open(out_dir / "judgements.jsonl", "w") as f:
        for r in results:
            f.write(json.dumps(r) + "\n")
    summary: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    for r in results:
        summary[r["class"]][r["agree"]] += 1
    disagreements = [r for r in results if r["agree"] == "no"]
    with open(out_dir / "disagreements.md", "w") as f:
        for r in disagreements:
            f.write(f"## {r['id']}  {r['class']}  {r['workbook']} / {r['sheet']}!{r['addr']}\n\n")
            f.write(f"- label: {r['label']}\n- judge: {r['judge_reason']}\n\n")
    print(json.dumps({k: dict(v) for k, v in summary.items()}, indent=1))
    print(f"{len(disagreements)} disagreements written to {out_dir / 'disagreements.md'}")


def main() -> None:
    args = parse_args()
    client = make_client()
    sample = build_sample(args)
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    earlier = load_earlier(out_dir) if args.resume else {}
    kept = [earlier[e["id"]] for e in sample if earlier.get(e["id"], {}).get("agree", "failed") != "failed"]
    todo = [e for e in sample if earlier.get(e["id"], {}).get("agree", "failed") == "failed"]
    print(f"judging {len(todo)} examples with {args.model} ({len(kept)} kept from earlier run)", flush=True)
    with ThreadPoolExecutor(args.concurrency) as pool:
        fresh = list(pool.map(partial(judge_one, client, args.model), todo))
    write_outputs(out_dir, kept + fresh)


if __name__ == "__main__":
    main()
