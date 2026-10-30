"""Decide which indexed training workbooks are allowed, by removing anything close to the 30 test workbooks.

Drops a training workbook when:
  - its sha256 equals a test workbook's, or equals another training workbook's (exact duplicate), or
  - its file name (stem, lowercased, digits stripped) matches a test workbook's, or
  - the share of a test workbook's labels found in it is >= threshold (template leakage).

Usage:
  python scripts/filter_leakage.py data/index/enron/workbooks.jsonl data/test/enron_errors_xlsx data/index/enron/allowed.json --threshold 0.6
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sheettruth.windows.cellinfo import Workbook, label_text  # noqa: E402


def norm_name(p: str) -> str:
    return re.sub(r"[\d_\-\s\.]+", "", Path(p).stem.lower())


def test_profiles(test_dir: Path) -> list[dict]:
    out = []
    for p in sorted(test_dir.rglob("*.xlsx")):
        labels = set()
        try:
            wb = Workbook(str(p))
            for sh in wb.sheets.values():
                for c in sh.cells.values():
                    if c.is_text:
                        labels.add(label_text(c.value).lower())
        except Exception:
            pass
        out.append({"path": str(p), "sha": hashlib.sha256(p.read_bytes()).hexdigest(),
                    "name": norm_name(p.name), "labels": labels})
    return out


def drop_reason(workbook: dict, tests: list[dict], seen_sha: set[str], threshold: float) -> str | None:
    """Why a training workbook must be excluded, or None if it may be used."""
    if "error" in workbook:
        return "unreadable"
    if workbook["sha256"] in {t["sha"] for t in tests}:
        return "same_file_as_test"
    if workbook["sha256"] in seen_sha:
        return "duplicate_in_train"
    test_names = {t["name"] for t in tests if len(t["name"]) >= 6}
    if norm_name(workbook["path"]) in test_names:
        return "same_name_as_test"
    labels = set(workbook.get("labels", []))
    for t in tests:
        if len(t["labels"]) < 8 or not labels:
            continue
        share = len(t["labels"] & labels) / len(t["labels"])
        if share >= threshold:
            return f"label_overlap_{share:.2f}_with_{Path(t['path']).name}"
    return None


def summarise(dropped: list[tuple[str, str]]) -> None:
    from collections import Counter
    kinds = Counter(r.split("_with_")[0] if r.startswith("label_overlap") else r for _, r in dropped)
    print(kinds.most_common(6))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("workbooks_jsonl")
    ap.add_argument("test_dir")
    ap.add_argument("out_json")
    ap.add_argument("--threshold", type=float, default=0.6)
    args = ap.parse_args()

    tests = test_profiles(Path(args.test_dir))
    allowed, dropped, seen_sha = [], [], set()
    for line in open(args.workbooks_jsonl):
        workbook = json.loads(line)
        reason = drop_reason(workbook, tests, seen_sha, args.threshold)
        if "sha256" in workbook:
            seen_sha.add(workbook["sha256"])
        if reason:
            dropped.append((workbook["path"], reason))
        else:
            allowed.append(workbook["path"])
    Path(args.out_json).write_text(json.dumps({"allowed": allowed, "dropped": dropped}, indent=1))
    print(f"allowed {len(allowed)}, dropped {len(dropped)}")
    summarise(dropped)


if __name__ == "__main__":
    main()
