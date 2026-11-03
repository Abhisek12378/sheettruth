"""Write a copy of the audited workbook with selected fixes applied.

A finding covers one run of identical formulas. The proposed fix is written into the finding's
target cell and translated into every other cell of the run, the same way a fix would be filled
down by hand. Only findings whose status is in the accepted set are applied; the original file is
never changed.
"""
from __future__ import annotations

from pathlib import Path

import openpyxl
from openpyxl.formula.translate import Translator

DEFAULT_ACCEPTED = ("confirmed",)


def applicable_findings(findings: list[dict], accepted: tuple[str, ...] = DEFAULT_ACCEPTED) -> list[dict]:
    """Findings that carry a proposed fix and an accepted status."""
    return [f for f in findings if f.get("expected") and f.get("status") in accepted]


def write_corrected_copy(source: str, destination: str, findings: list[dict],
                         accepted: tuple[str, ...] = DEFAULT_ACCEPTED) -> int:
    """Save a copy of `source` at `destination` with the accepted fixes written in. Returns the
    number of cells changed. Cached values are left as they are; the file recalculates on open."""
    wb = openpyxl.load_workbook(source)
    changed = 0
    for finding in applicable_findings(findings, accepted):
        if finding["sheet"] not in wb.sheetnames:
            continue
        ws = wb[finding["sheet"]]
        for addr in finding.get("run_cells") or [finding["addr"]]:
            ws[addr] = Translator(finding["expected"], origin=finding["addr"]).translate_formula(addr)
            changed += 1
    Path(destination).parent.mkdir(parents=True, exist_ok=True)
    wb.save(destination)
    return changed
