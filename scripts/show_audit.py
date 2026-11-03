"""Print the findings of an audit from its JSON detail file, one block per finding.

Usage:
  python scripts/show_audit.py reports/audit_book.json
  python scripts/show_audit.py data/uploads/<job id>/report.json
"""
from __future__ import annotations

import json
import sys


def print_finding(finding: dict) -> None:
    print(f"{finding['sheet']}!{finding['addr']}  {finding['status']}  P(error)={finding['p_error']:.2f}  "
          f"{finding['type']}  {finding['formula']} -> {finding['expected']}")
    print(f"  reason: {finding.get('reason', '')}")
    for check in finding["verification"]["checks"]:
        if check["result"] in ("supports", "contradicts"):
            print(f"  {check['name']}: {check['result']}: {check['detail']}")
    review = finding.get("review")
    if review:
        print(f"  reviewer: {review['verdict']}: {review['reason']}")


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    detail = json.load(open(sys.argv[1]))
    print(f"workbook: {detail['workbook']}  threshold: {detail['threshold']}  findings: {len(detail['findings'])}")
    for finding in detail["findings"]:
        print()
        print_finding(finding)


if __name__ == "__main__":
    main()
