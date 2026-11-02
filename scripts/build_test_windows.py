"""Build context windows for every in-scope formula cell of the held-out test workbooks.

Cells that share a sheet, an R1C1 formula and sit next to each other form one run (a filled-down
column of the same formula, say). One window is built per run, for its top-left cell, and the
verdict for that cell is applied to the whole run at evaluation time. Cells whose formula uses a
function outside the supported set are listed in the summary but get no window.

Usage:
  python scripts/build_test_windows.py --overview data/test/enron_errors_overview.json \\
      --xlsx-dir data/test/enron_errors_xlsx --out data/test/windows.jsonl
"""
from __future__ import annotations

import argparse
import json
import sys
import warnings
from pathlib import Path

import yaml

warnings.filterwarnings("ignore")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sheettruth.windows.runs import workbook_records  # noqa: E402


def test_workbooks(overview: list[dict]) -> list[tuple[int, str]]:
    """(case id, faulty file name as .xlsx) for every case that is a formula error."""
    seen = []
    for e in overview:
        if e["cell_type"] != "Formula" or not e["faulty_file"]:
            continue
        name = e["faulty_file"].rsplit(".", 1)[0] + ".xlsx"
        if (e["ss"], name) not in seen:
            seen.append((e["ss"], name))
    return seen


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--overview", default="data/test/enron_errors_overview.json")
    ap.add_argument("--xlsx-dir", default="data/test/enron_errors_xlsx")
    ap.add_argument("--config", default="configs/default.yaml")
    ap.add_argument("--out", default="data/test/windows.jsonl")
    args = ap.parse_args()

    cfg = yaml.safe_load(open(args.config))
    overview = json.load(open(args.overview))
    total_runs = total_cells = total_out = 0
    with open(args.out, "w") as out:
        for ss, name in test_workbooks(overview):
            path = str(Path(args.xlsx_dir) / str(ss) / name)
            records, out_of_scope = workbook_records(ss, name, path, cfg)
            cells = sum(len(r["run_cells"]) for r in records)
            total_runs, total_cells, total_out = total_runs + len(records), total_cells + cells, total_out + out_of_scope
            print(f"case {ss:>2} {name}: {len(records)} windows covering {cells} cells, {out_of_scope} out of scope", flush=True)
            for r in records:
                out.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"total: {total_runs} windows covering {total_cells} cells; {total_out} out-of-scope cells skipped")


if __name__ == "__main__":
    main()
