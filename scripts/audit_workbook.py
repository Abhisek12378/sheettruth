"""Audit one workbook end to end with the audit graph.

Steps (see sheettruth/agent/graph.py): structure checks, one context window per run of identical
formulas, model verdicts, the verify agent on every flagged cell, then a Markdown report and a
JSON file with the full detail.

Usage:
  python scripts/audit_workbook.py path/to/book.xlsx --out reports/audit_book.md
  python scripts/audit_workbook.py path/to/book.xlsx --out reports/audit_book.md --threshold 0.3
  python scripts/audit_workbook.py path/to/book.xlsx --out r.md --predictions data/test/predictions.jsonl

The model is reached through the Modal app deployed with:
  python -m modal deploy training/predict_glimmer_modal.py
"""
from __future__ import annotations

import argparse
import sys
import warnings
from pathlib import Path

import yaml

warnings.filterwarnings("ignore")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sheettruth.agent.graph import AuditGraph  # noqa: E402
from sheettruth.agent.model_client import ModalPredictorClient, SavedPredictionsClient  # noqa: E402
from sheettruth.data.recalc import Recalculator  # noqa: E402
from sheettruth.verify import Verifier  # noqa: E402

DEFAULT_ADAPTER = "/models/glimmer-sheettruth-v2/adapter"


def parse_args():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("workbook")
    ap.add_argument("--out", required=True, help="Markdown report path; a .json with full detail is written next to it")
    ap.add_argument("--config", default="configs/default.yaml")
    ap.add_argument("--threshold", type=float, default=0.5)
    ap.add_argument("--adapter-dir", default=DEFAULT_ADAPTER)
    ap.add_argument("--predictions", default="", help="reuse verdicts from this file instead of calling the model")
    ap.add_argument("--no-verify", action="store_true", help="skip LibreOffice recalculation in the verify agent")
    return ap.parse_args()


def main() -> None:
    args = parse_args()
    cfg = yaml.safe_load(open(args.config))
    model = SavedPredictionsClient(args.predictions) if args.predictions else ModalPredictorClient(args.adapter_dir)
    verifier = Verifier(None if args.no_verify else Recalculator(timeout=cfg["recalc"]["timeout_s"]))
    state = AuditGraph(model, verifier).run(args.workbook, cfg, args.threshold, args.out)
    for note in state["notes"]:
        print(note)
    print(f"report written to {args.out}")


if __name__ == "__main__":
    main()
