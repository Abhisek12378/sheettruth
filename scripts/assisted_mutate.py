"""Let a reviewer model propose realistic formula errors; code applies and checks each one.

The rule-based mutators cover a fixed set of shapes. This script takes correct cells from an
earlier build, shows a reviewer model the context window and the formula, and asks for one
realistic mistake of a named type that a careful reader could catch from the window alone. The
proposal is then applied the same way as a rule-based mutation: written into a copy of the
workbook (sometimes across the whole run of identical formulas), recalculated, and turned into a
window. A proposal is kept only if the broken formula parses, differs from the original, does not
reference the target cell, and the cells it names as evidence still show up in the new window.

Usage:
  ANTHROPIC_API_KEY=... python scripts/assisted_mutate.py data/dataset/enron_v2/examples.jsonl \\
      --xlsx data/xlsx/enron --out data/dataset/enron_assisted --count 1000 --model <reviewer model id>
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import random
import re
import sys
import tempfile
import time
import warnings
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import yaml
from openpyxl.formula import Tokenizer

warnings.filterwarnings("ignore")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import build_dataset as bd  # noqa: E402
from sheettruth.data.recalc import Recalculator  # noqa: E402
from sheettruth.prompt import ERROR_TYPES  # noqa: E402
from sheettruth.windows.builder import build_window  # noqa: E402
from sheettruth.windows.cellinfo import Workbook, build_context  # noqa: E402

TYPE_GUIDE = """wrong_function: the aggregate function does not match the label (SUM where AVERAGE is meant, MAX for a total)
skipped_rows: the range stops short at either end, or collapsed to one cell written as A5:A5
extra_rows: the range reaches one or two cells too far into a header, price, rate or other foreign row
double_count: a cell already inside the summed range is added again, or the range includes a subtotal of itself
wrong_sign: a labelled amount is added where it should be subtracted, or the reverse
wrong_reference: one reference points one to three rows (or columns) away from the cell that belongs there
missing_term: one labelled term of a sum is left out
wrong_operator: a product written as a division, or parentheses dropped so the order of operations changes
missing_factor: one multiplier (a rate, a unit factor) is left out of a product"""

PROPOSAL_PROMPT = """You help build a training set for a spreadsheet auditor. Below is the context window of one
formula cell whose formula is correct, followed by the formula. Propose ONE realistic mistake a
busy analyst could have made in this exact cell, of one of these types:

{guide}

Prefer these types when the cell allows it: {preferred}.

Rules:
- The broken formula must be a plausible edit of the original (same style, one slip), valid
  spreadsheet syntax, and must not reference the target cell itself.
- A careful reader must be able to detect the mistake from the window alone. Name the window
  cells that give it away (addresses such as Sheet1!B7).
- If no realistic, detectable mistake fits this cell, answer {{"skip": true}}.

Answer with one JSON object only:
{{"type": "<one of the types>", "broken_formula": "=...", "reason": "<one sentence, naming the labels involved>", "evidence": ["<cell address>", ...]}}

=== WINDOW ===
{window}

=== FORMULA ===
{formula}
"""

ADDRESS = re.compile(r"\$?[A-Z]{1,3}\$?\d+")
API_TIMEOUT_SECONDS = 600.0
MAX_REPLY_TOKENS = 8000
SLOW_APPLY_SECONDS = 20
USAGE_SAMPLES = [1, 2, 3, 4, 5, 6, 7, 8]     # the first few calls report their token usage


def load_jsonl(path: str) -> list[dict]:
    with open(path) as f:
        return [json.loads(line) for line in f if line.strip()]


def pick_sources(examples: list[dict], count: int, rng: random.Random, xlsx_root: str = "",
                 max_file_kb: int = 0) -> list[dict]:
    """Correct, non-hard-negative cells from workbooks small enough to recalculate quickly, spread
    across function families."""
    ok = [e for e in examples if e["verdict"] == "ok" and not e.get("hard_negative")]
    if max_file_kb:
        ok = [e for e in ok if (Path(xlsx_root) / e["workbook"]).stat().st_size <= max_file_kb * 1024]
    by_family: dict[str, list[dict]] = collections.defaultdict(list)
    for e in ok:
        by_family[e["func_family"]].append(e)
    for items in by_family.values():
        rng.shuffle(items)
    chosen: list[dict] = []
    while len(chosen) < count and any(by_family.values()):
        for items in by_family.values():
            if items and len(chosen) < count:
                chosen.append(items.pop())
    return chosen


def ask_model(client, model: str, example: dict, preferred: str) -> dict | None:
    prompt = PROPOSAL_PROMPT.format(guide=TYPE_GUIDE, preferred=preferred, window=example["window"],
                                    formula=example["original_formula"])
    for attempt in range(3):
        try:
            msg = client.messages.create(model=model, max_tokens=MAX_REPLY_TOKENS,
                                         output_config={"effort": "low"},
                                         messages=[{"role": "user", "content": prompt}])
            if USAGE_SAMPLES:
                USAGE_SAMPLES.pop()
                print(f"usage sample: input={msg.usage.input_tokens} output={msg.usage.output_tokens} stop={msg.stop_reason}",
                      file=sys.stderr, flush=True)
            text = "".join(b.text for b in msg.content if getattr(b, "type", "") == "text")
            start, end = text.find("{"), text.rfind("}")
            if start < 0 or end < start:
                raise ValueError(f"no JSON in reply (stop={msg.stop_reason}): {text[:80]!r}")
            return json.loads(text[start:end + 1])
        except Exception as ex:
            print(f"api attempt {attempt + 1} failed for {example['id']}: {type(ex).__name__}: {str(ex)[:400]}",
                  file=sys.stderr, flush=True)
            time.sleep(5 * (attempt + 1))
    return None


def formula_is_valid(broken: str, original: str, target_addr: str) -> bool:
    if not isinstance(broken, str) or not broken.startswith("=") or broken.strip() == original.strip():
        return False
    if re.search(r"(?<![A-Z$])\$?" + re.escape(target_addr) + r"(?!\d)", broken):
        return False
    try:
        Tokenizer(broken)
    except Exception:
        return False
    return True


def proposal_is_valid(p: dict | None, example: dict) -> bool:
    if not p or p.get("skip") or p.get("type") not in ERROR_TYPES:
        return False
    return formula_is_valid(p.get("broken_formula", ""), example["original_formula"], example["addr"])


def apply_proposal(example: dict, proposal: dict, xlsx_root: str, cfg: dict, recalc: Recalculator,
                   rng: random.Random) -> dict | None:
    """Write the proposed formula into a copy, recalculate, rebuild the window, check the evidence."""
    path = str(Path(xlsx_root) / example["workbook"])
    wb = Workbook(path)
    ctx = build_context(wb, example["sheet"], example["addr"], cfg["window"]["max_header_levels"])
    if ctx is None:
        return None
    run = bd._run_cells(ctx)
    block_wide = bool(run) and rng.random() < cfg["mutators"].get("block_wide_probability", 0.0)
    with tempfile.TemporaryDirectory(prefix="st-assist-") as tmp:
        copy = os.path.join(tmp, "copy.xlsx")
        try:
            bd._write_corrupted_copy(path, ctx.sheet.name, example["addr"], proposal["broken_formula"], copy,
                                     run if block_wide else ())
        except Exception:
            return None
        ok, status = recalc.recalc(copy)
        corrupted = Workbook(copy, strip_formula_values=not ok)
        cctx = build_context(corrupted, ctx.sheet.name, example["addr"], cfg["window"]["max_header_levels"])
        if cctx is None:
            return None
        window = build_window(cctx, bd.window_config(cfg))
    if window.unsupported_reason:
        return None
    evidence = [a.replace("$", "") for item in proposal.get("evidence", []) for a in ADDRESS.findall(str(item).upper())]
    if evidence and not any(a in window.text for a in evidence):
        return None
    keep = {k: example[k] for k in ("source", "split", "workbook", "sheet", "addr", "func_family", "original_formula")}
    return {**keep, "verdict": "error", "type": proposal["type"], "expected": example["original_formula"],
            "broken_formula": proposal["broken_formula"], "reason": str(proposal.get("reason", "")),
            "touched_cells": evidence, "mutator_version": "assisted", "block_wide": block_wide,
            "run_size": len(run) + 1, "recalc": status, "window": window.text, "tokens": window.tokens,
            "truncated": window.truncated}


def done_sources(out_path: Path) -> set[str]:
    if not out_path.exists():
        return set()
    return {r["source_id"] for r in load_jsonl(str(out_path))}


def parse_args():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("examples", help="examples.jsonl from build_dataset.py; its ok examples are the seeds")
    ap.add_argument("--xlsx", required=True, help="root of the converted .xlsx files")
    ap.add_argument("--out", required=True)
    ap.add_argument("--config", default="configs/default.yaml")
    ap.add_argument("--count", type=int, default=1000)
    ap.add_argument("--model", required=True, help="reviewer model id for the Anthropic API")
    ap.add_argument("--preferred", default="extra_rows, missing_factor, wrong_operator, missing_term, double_count")
    ap.add_argument("--concurrency", type=int, default=4)
    ap.add_argument("--max-file-kb", type=int, default=600, help="skip seed workbooks larger than this")
    ap.add_argument("--seed", type=int, default=11)
    return ap.parse_args()


def main() -> None:
    args = parse_args()
    try:
        import anthropic
    except ImportError:
        sys.exit("pip install anthropic")
    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("set ANTHROPIC_API_KEY")
    client = anthropic.Anthropic(timeout=API_TIMEOUT_SECONDS, max_retries=2)
    cfg = yaml.safe_load(open(args.config))
    rng = random.Random(args.seed)
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "examples.jsonl"
    already = done_sources(out_path)
    pool_of_seeds = pick_sources(load_jsonl(args.examples), args.count + len(already), rng, args.xlsx, args.max_file_kb)
    sources = [e for e in pool_of_seeds if e["id"] not in already]
    print(f"{len(sources)} seed cells ({len(already)} already done)", flush=True)

    recalc = Recalculator(timeout=cfg["recalc"]["timeout_s"])
    tally = collections.Counter()
    with ThreadPoolExecutor(args.concurrency) as pool, open(out_path, "a") as f:
        futures = {pool.submit(ask_model, client, args.model, e, args.preferred): e for e in sources}
        for i, future in enumerate(as_completed(futures), 1):
            example, proposal = futures[future], future.result()
            if not proposal_is_valid(proposal, example):
                tally["rejected_proposal"] += 1
                continue
            started = time.time()
            try:
                record = apply_proposal(example, proposal, args.xlsx, cfg, recalc, rng)
            except Exception as ex:
                print(f"apply failed for {example['workbook']}: {type(ex).__name__}", file=sys.stderr, flush=True)
                record = None
            if time.time() - started > SLOW_APPLY_SECONDS:
                print(f"slow apply {time.time() - started:.0f}s for {example['workbook']}", file=sys.stderr, flush=True)
            if record is None:
                tally["rejected_after_apply"] += 1
                continue
            record["id"] = f"assisted-{example['id']}"
            record["source_id"] = example["id"]
            tally[record["type"]] += 1
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
            f.flush()
            if i % 25 == 0:
                print(f"{i}/{len(sources)} seeds, {dict(tally)}", flush=True)
    print(json.dumps(dict(tally), indent=1))


if __name__ == "__main__":
    main()
