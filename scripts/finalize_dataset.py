"""Turn raw example files into balanced train/val sets in chat JSONL format.

Balancing rules:
  * every error example is kept, up to --per-type-cap per error type
  * ok examples are sampled down to match the number of error examples, stratified by the
    function family of the target cell so no family is mostly ok or mostly error
  * unsupported examples are capped at --unsupported-share of the final set
Splits are taken from the examples themselves (assigned per workbook when they were built), so a
workbook never appears in both train and val.

Each output line is {"messages": [system, user, assistant]} where the assistant reply is the JSON
verdict the model must learn to produce.

Usage:
  python scripts/finalize_dataset.py data/dataset/enron/examples.jsonl --out data/dataset/final
"""
from __future__ import annotations

import argparse
import collections
import json
import random
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sheettruth.prompt import SYSTEM_PROMPT  # noqa: E402


def assistant_reply(example: dict) -> str:
    reply = {
        "verdict": example["verdict"],
        "type": example.get("type"),
        "expected": example.get("expected"),
        "reason": example.get("reason", ""),
    }
    return json.dumps(reply, ensure_ascii=False)


def to_chat(example: dict) -> dict:
    return {"messages": [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": example["window"]},
        {"role": "assistant", "content": assistant_reply(example)},
    ]}


def load_examples(paths: list[str]) -> list[dict]:
    """All examples from the given files; a repeated id (from a resumed run) is kept once."""
    out, seen = [], set()
    for p in paths:
        with open(p) as f:
            for line in f:
                if not line.strip():
                    continue
                e = json.loads(line)
                if e["id"] not in seen:
                    seen.add(e["id"])
                    out.append(e)
    return out


def is_valid_error(e: dict) -> bool:
    """Reject error examples that a rule bug could have produced: a broken formula that references
    the target cell itself, or a sign flip on a formula with fewer than two references."""
    broken = e.get("broken_formula") or ""
    if re.search(r"(?<![A-Z$])\$?" + re.escape(e["addr"]) + r"(?!\d)", broken):
        return False
    if e["type"] == "wrong_sign" and len(re.findall(r"\$?[A-Z]{1,3}\$?\d+", broken)) < 2:
        return False
    return True


def cap_errors(errors: list[dict], per_type_cap: int, rng: random.Random) -> list[dict]:
    by_type: dict[str, list[dict]] = collections.defaultdict(list)
    for e in errors:
        by_type[e["type"]].append(e)
    kept = []
    for items in by_type.values():
        rng.shuffle(items)
        kept.extend(items[:per_type_cap])
    return kept


def sample_ok_stratified(ok: list[dict], errors: list[dict], rng: random.Random, hard_share: float = 0.0) -> list[dict]:
    """Pick as many ok examples as there are errors. Hard negatives (cells a mutator could have
    broken) fill up to hard_share of that quota first; the rest matches the error set's
    function-family mix."""
    hard = [e for e in ok if e.get("hard_negative")]
    rng.shuffle(hard)
    hard = hard[:int(hard_share * len(errors))]
    regular = [e for e in ok if not e.get("hard_negative")]
    scale = (len(errors) - len(hard)) / len(errors) if errors else 0.0
    target_by_family = {f: round(n * scale) for f, n in collections.Counter(e["func_family"] for e in errors).items()}
    ok_by_family: dict[str, list[dict]] = collections.defaultdict(list)
    for e in regular:
        ok_by_family[e["func_family"]].append(e)
    chosen: list[dict] = []
    shortfall = 0
    for family, n in target_by_family.items():
        pool = ok_by_family.get(family, [])
        rng.shuffle(pool)
        chosen.extend(pool[:n])
        shortfall += max(0, n - len(pool))
    if shortfall:
        used = {id(e) for e in chosen}
        leftovers = [e for e in regular if id(e) not in used]
        rng.shuffle(leftovers)
        chosen.extend(leftovers[:shortfall])
    return hard + chosen


def balance(examples: list[dict], per_type_cap: int, unsupported_share: float, rng: random.Random,
            hard_share: float = 0.0) -> list[dict]:
    errors = cap_errors([e for e in examples if e["verdict"] == "error" and is_valid_error(e)], per_type_cap, rng)
    ok = sample_ok_stratified([e for e in examples if e["verdict"] == "ok"], errors, rng, hard_share)
    unsupported = [e for e in examples if e["verdict"] == "unsupported"]
    rng.shuffle(unsupported)
    max_unsupported = int((len(errors) + len(ok)) * unsupported_share / (1 - unsupported_share))
    final = errors + ok + unsupported[:max_unsupported]
    rng.shuffle(final)
    return final


def summarise(examples: list[dict]) -> dict:
    by_verdict = collections.Counter(e["verdict"] for e in examples)
    by_verdict["hard_negative"] = sum(1 for e in examples if e.get("hard_negative"))
    by_type = collections.Counter(e["type"] for e in examples if e["verdict"] == "error")
    by_family: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    for e in examples:
        by_family[e["func_family"]][e["verdict"]] += 1
    workbooks = len({e["workbook"] for e in examples})
    return {"total": len(examples), "workbooks": workbooks, "by_verdict": dict(by_verdict),
            "by_type": dict(by_type), "by_family": {k: dict(v) for k, v in sorted(by_family.items())}}


def write_jsonl(path: Path, rows: list[dict]) -> None:
    with open(path, "w") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("inputs", nargs="+", help="one or more examples.jsonl files")
    ap.add_argument("--out", required=True)
    ap.add_argument("--per-type-cap", type=int, default=1200)
    ap.add_argument("--unsupported-share", type=float, default=0.10)
    ap.add_argument("--hard-negative-share", type=float, default=0.35,
                    help="share of the ok quota reserved for hard negatives, when the inputs hold any")
    ap.add_argument("--seed", type=int, default=20261031)
    args = ap.parse_args()

    rng = random.Random(args.seed)
    examples = load_examples(args.inputs)
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    report = {}
    for split in ("train", "val"):
        subset = [e for e in examples if e["split"] == split]
        final = balance(subset, args.per_type_cap, args.unsupported_share, rng, args.hard_negative_share)
        write_jsonl(out_dir / f"{split}.jsonl", [to_chat(e) for e in final])
        write_jsonl(out_dir / f"{split}_meta.jsonl", [{k: v for k, v in e.items() if k != "window"} for e in final])
        report[split] = summarise(final)
    (out_dir / "report.json").write_text(json.dumps(report, indent=1))
    print(json.dumps(report, indent=1))


if __name__ == "__main__":
    main()
