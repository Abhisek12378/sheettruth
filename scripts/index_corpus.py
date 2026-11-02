"""Index every formula cell in a folder of .xlsx workbooks.

Writes two files:
  OUT_DIR/workbooks.jsonl  one line per workbook: path, sha256, sheets, label set, counts
  OUT_DIR/cells.jsonl      one line per formula cell: workbook, sheet, addr, formula, r1c1, funcs, in_scope, block_id

block_id groups contiguous cells (same column or same row) that share the same R1C1 formula,
so a dragged column of 300 identical formulas can be sampled as one block later.

Files above --max-file-mb are recorded as skipped without being opened: openpyxl holds a workbook
in memory at many times its size on disk, and very large workbooks are data dumps rather than
models. Each worker runs under a hard memory limit so a single oversized file fails cleanly instead
of taking the whole pool down. --resume appends to an existing index and skips workbooks already in it.

Usage:
  python scripts/index_corpus.py data/xlsx/enron data/index/enron --workers 4 --resume
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import resource
import sys
import warnings
from multiprocessing import Pool
from pathlib import Path

warnings.filterwarnings("ignore")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sheettruth.windows.cellinfo import IN_SCOPE_FUNCS, Workbook, functions_in, label_text, to_r1c1  # noqa: E402

MAX_CELLS_PER_SHEET = 200_000   # skip monster sheets
WORKER_MEMORY_BYTES = 4_000 * 1024 * 1024
TASKS_PER_WORKER_BEFORE_RECYCLE = 25



def _column_major(cell) -> tuple[int, int]:
    return (cell.col, cell.row)

def _worker_init() -> None:
    """Cap each worker's address space so an oversized workbook raises MemoryError instead of being OOM-killed."""
    warnings.filterwarnings("ignore")
    try:
        resource.setrlimit(resource.RLIMIT_AS, (WORKER_MEMORY_BYTES, WORKER_MEMORY_BYTES))
    except (ValueError, OSError):
        pass


def assign_block_ids(sh) -> dict[tuple[int, int], str]:
    """Group contiguous formula cells (down a column or along a row) that share the same R1C1 formula."""
    block_of: dict[tuple[int, int], str] = {}
    for c in sorted(sh.formula_cells(), key=_column_major):
        r1c1 = to_r1c1(c.formula, c.row, c.col)
        neighbours = (block_of.get((c.row - 1, c.col)), block_of.get((c.row, c.col - 1)))
        same = [b for b in neighbours if b and b.split("::")[0] == r1c1]
        block_of[(c.row, c.col)] = same[0] if same else f"{r1c1}::{sh.name}!{c.addr}"
    return {k: hashlib.md5(v.encode()).hexdigest()[:12] for k, v in block_of.items()}


def index_one(args: tuple[str, str]) -> tuple[dict, list[dict]]:
    """Index one workbook. Never raises: any failure is returned as a record with an error field."""
    path, root = args
    rel = os.path.relpath(path, root)
    try:
        return _index_workbook(path, rel)
    except MemoryError:
        return {"path": rel, "error": "memory_limit"}, []
    except Exception as ex:
        return {"path": rel, "error": str(ex)[:120]}, []


def _index_workbook(path: str, rel: str) -> tuple[dict, list[dict]]:
    sha = hashlib.sha256(Path(path).read_bytes()).hexdigest()
    wb = Workbook(path)
    labels: set[str] = set()
    cells_out: list[dict] = []
    n_formula = 0
    for sh in wb.sheets.values():
        if len(sh.cells) > MAX_CELLS_PER_SHEET:
            continue
        labels.update(label_text(c.value).lower() for c in sh.cells.values() if c.is_text)
        blocks = assign_block_ids(sh)
        for c in sorted(sh.formula_cells(), key=_column_major):
            n_formula += 1
            funcs = functions_in(c.formula)
            cells_out.append({
                "workbook": rel, "sheet": sh.name, "addr": c.addr,
                "formula": c.formula[:300], "r1c1": to_r1c1(c.formula, c.row, c.col)[:300], "funcs": funcs,
                "in_scope": all(f in IN_SCOPE_FUNCS for f in funcs),
                "has_cache": c.value is not None, "block_id": blocks[(c.row, c.col)],
            })
    meta = {"path": rel, "sha256": sha, "sheets": wb.sheetnames,
            "n_labels": len(labels), "labels": sorted(labels)[:2000], "n_formula_cells": n_formula}
    return meta, cells_out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("xlsx_dir")
    ap.add_argument("out_dir")
    ap.add_argument("--workers", type=int, default=3, help="keep workers x 4 GB under the machine's RAM")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--max-file-mb", type=float, default=3.0, help="skip workbooks larger than this on disk")
    ap.add_argument("--resume", action="store_true", help="append to an existing index, skipping workbooks already in it")
    a = ap.parse_args()
    root = str(Path(a.xlsx_dir).resolve())
    out = Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)

    done = already_indexed(out) if a.resume else set()
    files = sorted(str(p) for p in Path(root).rglob("*.xlsx") if os.path.relpath(p, root) not in done)
    if a.limit:
        files = files[: a.limit]
    small, large = split_by_size(files, a.max_file_mb * 1024 * 1024)
    print(f"{len(files)} workbooks to index ({len(done)} already done), {len(large)} skipped as oversized, {a.workers} workers", flush=True)

    mode = "a" if a.resume else "w"
    n_cells = n_err = 0
    with open(out / "workbooks.jsonl", mode) as fw, open(out / "cells.jsonl", mode) as fc:
        for path in large:
            fw.write(json.dumps({"path": os.path.relpath(path, root), "error": "oversized_skipped"}) + "\n")
        with Pool(a.workers, initializer=_worker_init, maxtasksperchild=TASKS_PER_WORKER_BEFORE_RECYCLE) as pool:
            jobs = ((f, root) for f in small)
            for i, (meta, cells) in enumerate(pool.imap_unordered(index_one, jobs, chunksize=1), 1):
                if "error" in meta:
                    n_err += 1
                fw.write(json.dumps(meta) + "\n")
                for c in cells:
                    fc.write(json.dumps(c) + "\n")
                n_cells += len(cells)
                if i % 100 == 0:
                    print(f"{i}/{len(small)} workbooks, {n_cells} formula cells, {n_err} unreadable", flush=True)
    print(f"done: {len(small)} workbooks, {n_cells} formula cells, {n_err} unreadable, {len(large)} oversized skipped", flush=True)


def already_indexed(out: Path) -> set[str]:
    path = out / "workbooks.jsonl"
    if not path.exists():
        return set()
    return {json.loads(line)["path"] for line in open(path) if line.strip()}


def split_by_size(files: list[str], max_bytes: float) -> tuple[list[str], list[str]]:
    small = [f for f in files if os.path.getsize(f) <= max_bytes]
    large = [f for f in files if os.path.getsize(f) > max_bytes]
    return small, large


if __name__ == "__main__":
    main()
