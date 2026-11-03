"""Build the context window for one formula cell, optionally compare it with a saved window, and
score it with the deployed model.

Usage:
  python scripts/score_cell.py --workbook path/to/book.xlsx --sheet Sheet1 --cell F28
  python scripts/score_cell.py --workbook path/to/book.xlsx --sheet Sheet1 --cell F28 \\
      --reference data/test/windows.jsonl --reference-id "1:Sheet1!F28"
  python scripts/score_cell.py ... --no-score          (window only, no model call)

The comparison shows whether the window built now matches the one scored during evaluation; the
score shows what the model answers for it today.
"""
from __future__ import annotations

import argparse
import difflib
import json
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sheettruth.agent.model_client import ModalPredictorClient  # noqa: E402
from sheettruth.windows.runs import workbook_records  # noqa: E402

DEFAULT_ADAPTER = "/models/glimmer-sheettruth-v2/adapter"


def find_record(records: list[dict], sheet: str, cell: str) -> dict:
    for record in records:
        if record["sheet"] == sheet and cell in record["run_cells"]:
            return record
    sys.exit(f"no formula run covers {sheet}!{cell}")


def load_reference(path: str, record_id: str) -> dict:
    with open(path) as f:
        for line in f:
            if line.strip() and json.loads(line)["id"] == record_id:
                return json.loads(line)
    sys.exit(f"{record_id} not found in {path}")


def show_difference(saved: str, current: str) -> None:
    if saved == current:
        print("window: identical to the saved one")
        return
    print("window: differs from the saved one (- saved, + current)")
    for line in difflib.unified_diff(saved.splitlines(), current.splitlines(), lineterm="", n=0):
        print(line)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--workbook", required=True)
    ap.add_argument("--sheet", required=True)
    ap.add_argument("--cell", required=True)
    ap.add_argument("--config", default="configs/default.yaml")
    ap.add_argument("--reference", default="", help="jsonl of saved windows to compare with")
    ap.add_argument("--reference-id", default="", help="id of the saved window, such as 1:Sheet1!F28")
    ap.add_argument("--adapter-dir", default=DEFAULT_ADAPTER)
    ap.add_argument("--no-score", action="store_true")
    args = ap.parse_args()

    cfg = yaml.safe_load(open(args.config))
    records, _ = workbook_records(0, Path(args.workbook).name, args.workbook, cfg)
    record = find_record(records, args.sheet, args.cell)
    print(f"run {record['run_cells']}  formula {record['formula']}  tokens {record['tokens']}")
    if args.reference:
        show_difference(load_reference(args.reference, args.reference_id)["window"], record["window"])
    else:
        print(record["window"])
    if args.no_score:
        return
    verdict = ModalPredictorClient(args.adapter_dir).score([record])[f"{record['sheet']}!{record['addr']}"]
    print(json.dumps({k: verdict.get(k) for k in ("verdict", "p_error", "type", "expected", "reason")}, indent=1))


if __name__ == "__main__":
    main()
