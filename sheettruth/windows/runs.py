"""Group a sheet's in-scope formula cells into runs and build one context window per run.

Cells that share a sheet, an R1C1 formula and sit next to each other form one run, such as a
filled-down column of the same formula. One window is built per run, for its top-left cell, and a
verdict for that cell applies to the whole run.
"""
from __future__ import annotations

import collections

from sheettruth.windows.builder import WindowConfig, build_window
from sheettruth.windows.cellinfo import Workbook, build_context


def window_config(cfg: dict) -> WindowConfig:
    allowed = WindowConfig.__dataclass_fields__
    return WindowConfig(**{k: v for k, v in cfg["window"].items() if k in allowed})


def contiguous_runs(cells: set[tuple[int, int]]) -> list[list[tuple[int, int]]]:
    """Split a set of (row, col) into groups of cells that touch vertically or horizontally."""
    runs, todo = [], set(cells)
    while todo:
        start = min(todo)
        run, stack = [], [start]
        todo.discard(start)
        while stack:
            r, c = stack.pop()
            run.append((r, c))
            for nb in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if nb in todo:
                    todo.discard(nb)
                    stack.append(nb)
        runs.append(sorted(run))
    return runs


def sheet_runs(wb: Workbook, sheet_name: str, max_header_levels: int) -> tuple[list[dict], int]:
    """Runs of in-scope formula cells on one sheet, plus the count of out-of-scope formula cells."""
    sh = wb.sheet(sheet_name)
    groups: dict[str, set[tuple[int, int]]] = collections.defaultdict(set)
    out_of_scope = 0
    for cell in sh.formula_cells():
        ctx = build_context(wb, sheet_name, cell.addr, max_header_levels)
        if ctx is None:
            continue
        if not ctx.in_scope:
            out_of_scope += 1
            continue
        groups[ctx.r1c1].add((cell.row, cell.col))
    runs = []
    for r1c1, cells in groups.items():
        for run in contiguous_runs(cells):
            runs.append({"sheet": sheet_name, "r1c1": r1c1, "cells": [sh.get(r, c).addr for r, c in run]})
    return runs, out_of_scope


def workbook_records(case: int, name: str, path: str, cfg: dict) -> tuple[list[dict], int]:
    """One window record per run for every sheet of the workbook, plus the out-of-scope cell count."""
    wb = Workbook(path)
    wcfg = window_config(cfg)
    levels = cfg["window"]["max_header_levels"]
    records, out_of_scope = [], 0
    for sheet_name in wb.sheetnames:
        runs, skipped = sheet_runs(wb, sheet_name, levels)
        out_of_scope += skipped
        for run in runs:
            ctx = build_context(wb, sheet_name, run["cells"][0], levels)
            window = build_window(ctx, wcfg)
            records.append({
                "id": f"{case}:{sheet_name}!{run['cells'][0]}", "ss": case, "workbook": name,
                "sheet": sheet_name, "addr": run["cells"][0], "run_cells": run["cells"],
                "formula": ctx.cell.formula, "r1c1": run["r1c1"], "window": window.text,
                "tokens": window.tokens, "truncated": window.truncated,
                "unsupported_reason": window.unsupported_reason,
            })
    return records, out_of_scope
