"""Prepare the ExceLint benchmark as a second held-out test set.

The ExceLint project (Barowy, Berger and Zorn, OOPSLA 2018) audited 70 spreadsheets from the
CUSTODES suite by hand and published the workbooks as .xlsx together with a per-cell annotation
file. This script turns that material into the layout the test tools expect:

  <xlsx-out>/<case>/<workbook>.xlsx        one folder per case, numbered in file-name order
  <overview-out>                           the same record shape as the Enron overview, one
                                           record per documented error

Annotated cells that hold a formula are grouped into one documented error per run (same sheet,
same R1C1 formula, adjacent cells), which matches how windows are built. Annotated cells that
hold a plain value are recorded with cell_type "Value" so the evaluation skips them. The audit
does not say what the correct formula is, so corrected_formula is left empty and the "exact fix"
column of the evaluation is not meaningful for this set.

Usage:
  python scripts/prepare_excelint_benchmark.py --source data/raw/excelint/test \\
      --xlsx-out data/test/excelint_xlsx --overview-out data/test/excelint_overview.json
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import shutil
import sys
import urllib.parse
import warnings
from pathlib import Path

import openpyxl
from openpyxl.utils import get_column_letter

warnings.filterwarnings("ignore")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sheettruth.windows.cellinfo import to_r1c1  # noqa: E402
from sheettruth.windows.runs import contiguous_runs  # noqa: E402

SAFE_CHARS = re.compile(r"[^A-Za-z0-9._ -]+")


def safe_name(raw: str) -> str:
    """Decode URL escapes in a benchmark file name and keep only plain characters."""
    decoded = urllib.parse.unquote(raw)
    stem, dot, ext = decoded.rpartition(".")
    return SAFE_CHARS.sub("_", stem).strip() + dot + ext


def norm_sheet(name: str) -> str:
    return re.sub(r"\s+", " ", name).strip().lower()


def match_sheet(wanted: str, sheetnames: list[str]) -> str | None:
    """Sheet whose name equals the annotation's, ignoring spacing and case, else a prefix match."""
    target = norm_sheet(wanted)
    by_norm = {norm_sheet(s): s for s in sheetnames}
    if target in by_norm:
        return by_norm[target]
    for norm, original in by_norm.items():
        if norm.startswith(target) or target.startswith(norm):
            return original
    return None


def group_formula_cells(cells: list[tuple[int, int, str]]) -> list[list[tuple[int, int]]]:
    """Runs of adjacent cells with the same R1C1 formula; input tuples are (row, col, formula)."""
    by_r1c1: dict[str, set[tuple[int, int]]] = collections.defaultdict(set)
    for row, col, formula in cells:
        by_r1c1[to_r1c1(formula, row, col)].add((row, col))
    runs = []
    for members in by_r1c1.values():
        runs.extend(contiguous_runs(members))
    return runs


def addr(row: int, col: int) -> str:
    return f"{get_column_letter(col)}{row}"


def error_record(err: int, case: int, file_name: str, sheet: str, cells: list[str], cell_type: str,
                 formula: str) -> dict:
    return {
        "err": err, "ss": case, "faulty_file": file_name, "faulty_sheet": sheet,
        "faulty_cells": "; ".join(cells), "corrected_file": "", "corrected_sheet": "",
        "corrected_cells": "", "type": "Quantitative", "subtype": "", "cell_type": cell_type,
        "change": "", "info": "ExceLint audit: formula error",
        "faulty": {"cell": cells[0], "formula": formula, "row_label": "", "col_header": ""},
        "corrected": {"cell": cells[0], "formula": "", "row_label": "", "col_header": ""},
    }


def sheet_records(ws, bugs: list[list[int]], err_start: int, case: int, file_name: str) -> list[dict]:
    """Documented errors for one sheet: one per formula run, one per annotated value cell."""
    formula_cells, records, err = [], [], err_start
    for col, row, _kind in bugs:
        value = ws.cell(row=row, column=col).value
        if isinstance(value, str) and value.startswith("="):
            formula_cells.append((row, col, value))
            continue
        records.append(error_record(err, case, file_name, ws.title, [addr(row, col)], "Value", ""))
        err += 1
    for run in group_formula_cells(formula_cells):
        cells = [addr(r, c) for r, c in run]
        formula = ws.cell(row=run[0][0], column=run[0][1]).value
        records.append(error_record(err, case, file_name, ws.title, cells, "Formula", formula))
        err += 1
    return records


def prepare(source: Path, xlsx_out: Path, overview_out: Path) -> None:
    annotations = json.load(open(source / "annotations-processed.json"))
    overview, missing_sheets, err = [], [], 1
    for case, raw_name in enumerate(sorted(annotations), start=1):
        file_name = safe_name(raw_name)
        target = xlsx_out / str(case) / file_name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source / "subjects_xlsx" / raw_name, target)
        book = openpyxl.load_workbook(target)
        for sheet_name, data in annotations[raw_name].items():
            if not data["bugs"]:
                continue
            found = match_sheet(sheet_name, book.sheetnames)
            if found is None:
                missing_sheets.append((file_name, sheet_name))
                continue
            records = sheet_records(book[found], data["bugs"], err, case, file_name)
            overview.extend(records)
            err += len(records)
    overview_out.write_text(json.dumps(overview, indent=1, ensure_ascii=False))
    formula = [e for e in overview if e["cell_type"] == "Formula"]
    cells = sum(len(e["faulty_cells"].split("; ")) for e in formula)
    print(f"{len(annotations)} workbooks copied to {xlsx_out}")
    print(f"{len(formula)} formula errors covering {cells} cells, "
          f"{len(overview) - len(formula)} value cells (skipped by the evaluation)")
    print(f"workbooks with formula errors: {len({e['ss'] for e in formula})}")
    for file_name, sheet_name in missing_sheets:
        print(f"sheet not found: {file_name} / {sheet_name}", file=sys.stderr)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--source", required=True, help="the ExceLint-core test folder")
    ap.add_argument("--xlsx-out", default="data/test/excelint_xlsx")
    ap.add_argument("--overview-out", default="data/test/excelint_overview.json")
    args = ap.parse_args()
    prepare(Path(args.source), Path(args.xlsx_out), Path(args.overview_out))


if __name__ == "__main__":
    main()
