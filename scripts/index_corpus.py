"""Index every formula cell in a folder of .xlsx workbooks.

Writes two files:
  OUT_DIR/workbooks.jsonl  one line per workbook: path, sha256, sheets, label set, counts
  OUT_DIR/cells.jsonl      one line per formula cell: workbook, sheet, addr, formula, r1c1, funcs, in_scope, block_id

block_id groups contiguous cells (same column or same row) that share the same R1C1 formula,
so a dragged column of 300 identical formulas can be sampled as one block later.

Usage:
  python scripts/index_corpus.py data/xlsx/enron data/index/enron --workers 4
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import warnings
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

warnings.filterwarnings("ignore")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sheettruth.windows.cellinfo import IN_SCOPE_FUNCS, Workbook, functions_in, label_text, to_r1c1  # noqa: E402

MAX_CELLS_PER_SHEET = 200_000   # skip monster sheets


def assign_block_ids(sh) -> dict[tuple[int, int], str]:
    """Group contiguous formula cells (down a column or along a row) that share the same R1C1 formula."""
    block_of: dict[tuple[int, int], str] = {}
    for c in sorted(sh.formula_cells(), key=lambda x: (x.col, x.row)):
        r1c1 = to_r1c1(c.formula, c.row, c.col)
        neighbours = (block_of.get((c.row - 1, c.col)), block_of.get((c.row, c.col - 1)))
        same = [b for b in neighbours if b and b.split("::")[0] == r1c1]
        block_of[(c.row, c.col)] = same[0] if same else f"{r1c1}::{sh.name}!{c.addr}"
    return block_of


def index_one(path: str, root: str) -> tuple[dict, list[dict]] | None:
    try:
        sha = hashlib.sha256(Path(path).read_bytes()).hexdigest()
        wb = Workbook(path)
    except Exception as ex:
        return {"path": os.path.relpath(path, root), "error": str(ex)[:120]}, []
    labels: set[str] = set()
    cells_out: list[dict] = []
    n_formula = 0
    for sh in wb.sheets.values():
        if len(sh.cells) > MAX_CELLS_PER_SHEET:
            continue
        for c in sh.cells.values():
            if c.is_text:
                labels.add(label_text(c.value).lower())
        blocks = assign_block_ids(sh)
        for c in sorted(sh.formula_cells(), key=lambda x: (x.col, x.row)):
            n_formula += 1
            r1c1 = to_r1c1(c.formula, c.row, c.col)
            bid = blocks[(c.row, c.col)]
            funcs = functions_in(c.formula)
            cells_out.append({
                "workbook": os.path.relpath(path, root), "sheet": sh.name, "addr": c.addr,
                "formula": c.formula[:300], "r1c1": r1c1[:300], "funcs": funcs,
                "in_scope": all(f in IN_SCOPE_FUNCS for f in funcs),
                "has_cache": c.value is not None, "block_id": hashlib.md5(bid.encode()).hexdigest()[:12],
            })
    meta = {"path": os.path.relpath(path, root), "sha256": sha, "sheets": wb.sheetnames,
            "n_labels": len(labels), "labels": sorted(labels)[:2000], "n_formula_cells": n_formula}
    return meta, cells_out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("xlsx_dir")
    ap.add_argument("out_dir")
    ap.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2) - 1))
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()
    root = str(Path(a.xlsx_dir).resolve())
    files = sorted(str(p) for p in Path(root).rglob("*.xlsx"))
    if a.limit:
        files = files[: a.limit]
    out = Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    print(f"{len(files)} workbooks, {a.workers} workers")
    n_cells = n_err = 0
    with open(out / "workbooks.jsonl", "w") as fw, open(out / "cells.jsonl", "w") as fc:
        with ProcessPoolExecutor(a.workers) as ex:
            futs = [ex.submit(index_one, f, root) for f in files]
            for i, fut in enumerate(as_completed(futs), 1):
                res = fut.result()
                if res is None:
                    continue
                meta, cells = res
                if "error" in meta:
                    n_err += 1
                fw.write(json.dumps(meta) + "\n")
                for c in cells:
                    fc.write(json.dumps(c) + "\n")
                n_cells += len(cells)
                if i % 100 == 0:
                    print(f"{i}/{len(files)} workbooks, {n_cells} formula cells, {n_err} unreadable")
    print(f"done: {len(files)} workbooks, {n_cells} formula cells, {n_err} unreadable")


if __name__ == "__main__":
    main()
