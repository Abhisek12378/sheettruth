"""Independent checks on a flagged formula cell.

The meaning model says "this formula is wrong, here is the fix". Nothing here trusts that claim.
Each check looks at the workbook itself:

  recalculated_fix   the fix is written into a copy and recalculated; the value must change and
                     must not turn into an error
  peer_pattern       formulas next to the target that share one R1C1 shape: does the fix match
                     them while the current formula does not?
  sibling_sheets     the same cell on the workbook's other sheets (a template repeated per unit or
                     per month): does the fix match what the siblings do, or does the current
                     formula already agree with them?
  range_delta        the cells a range fix adds or drops: real labelled numbers support a range
                     extension, blanks and text contradict any fix; for a dropped cell, whether it
                     looks foreign to the block. For a moved reference or an added term the added
                     cell holding a value is only a precondition, not evidence
  double_count       the current formula really counts a cell twice, or sums a subtotal of itself
  value_plausibility after the fix, the target's value sits closer to its peers than before

A finding passes when at least one check supports it, fails when checks only contradict it, and
is reported as "no_independent_check" when nothing could be tested. Recalculation and the value
change are necessary conditions: they can sink a finding but never carry it on their own.
"""
from __future__ import annotations

import os
import statistics
import tempfile
from dataclasses import dataclass, field
from typing import Optional

import openpyxl

from sheettruth.data.recalc import Recalculator
from sheettruth.mutators.common import col_header, is_parameter_label, row_label
from sheettruth.windows.cellinfo import (Cell, Sheet, Workbook, additive_terms, parse_refs, term_leaf_cells,
                                         to_r1c1)

RANGE_TYPES = {"skipped_rows", "extra_rows", "wrong_reference", "missing_term"}
RANGE_SUPPORT_TYPES = {"skipped_rows", "extra_rows"}   # for these, what the fix adds or drops is evidence in itself
PEER_SPAN = 15
MIN_PEERS = 3
PLAUSIBILITY_FACTOR = 2.0


@dataclass
class Finding:
    sheet: str
    addr: str
    formula: str
    expected: Optional[str]
    type: Optional[str]
    reason: str = ""
    p_error: float = 0.0


@dataclass
class Check:
    name: str
    result: str          # supports | contradicts | neutral | skipped
    detail: str


@dataclass
class Verification:
    outcome: str         # passed | failed | no_independent_check
    checks: list[Check] = field(default_factory=list)
    old_value: object = None
    new_value: object = None

    def to_dict(self) -> dict:
        return {"outcome": self.outcome, "old_value": self.old_value, "new_value": self.new_value,
                "checks": [c.__dict__ for c in self.checks]}


def _is_number(v) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _label(sheet: Sheet, cell: Cell) -> str:
    return row_label(sheet, cell.row, cell.col) or col_header(sheet, cell.row, cell.col)


def _peers(sheet: Sheet, target: Cell) -> list[Cell]:
    positions = [(target.row, c) for c in range(max(1, target.col - PEER_SPAN), target.col + PEER_SPAN + 1)]
    positions += [(r, target.col) for r in range(max(1, target.row - PEER_SPAN), target.row + PEER_SPAN + 1)]
    return [sheet.get(r, c) for (r, c) in positions
            if (r, c) != (target.row, target.col) and sheet.get(r, c).is_formula]


def _referenced_cells(formula: str, sheet_name: str) -> set[tuple[str, int, int]]:
    cells: set[tuple[str, int, int]] = set()
    for ref in parse_refs(formula, sheet_name):
        if ref.size() <= 5000:
            cells.update((ref.sheet, r, c) for (r, c) in ref.cells())
    return cells


class Verifier:
    def __init__(self, recalculator: Optional[Recalculator] = None):
        self.recalc = recalculator

    # -- individual checks ------------------------------------------------------------------

    def check_recalculated_fix(self, wb_path: str, finding: Finding) -> tuple[Check, object]:
        """Write the fix into a copy, recalculate, read the new value. Returns the check and the value."""
        if self.recalc is None or not self.recalc.ready:
            return Check("recalculated_fix", "skipped", "LibreOffice not available"), None
        with tempfile.TemporaryDirectory(prefix="st-verify-") as tmp:
            copy = os.path.join(tmp, "copy.xlsx")
            book = openpyxl.load_workbook(wb_path)
            book[finding.sheet][finding.addr] = finding.expected
            book.save(copy)
            ok, status = self.recalc.recalc(copy)
            if not ok:
                return Check("recalculated_fix", "skipped", f"recalculation failed: {status}"), None
            value = openpyxl.load_workbook(copy, data_only=True)[finding.sheet][finding.addr].value
        if isinstance(value, str) and value.startswith("#"):
            return Check("recalculated_fix", "contradicts", f"the fix evaluates to {value}"), value
        return Check("recalculated_fix", "neutral", f"the fix evaluates to {value!r}"), value

    def check_value_change(self, old_value, new_value) -> Check:
        if new_value is None:
            return Check("value_change", "skipped", "no recalculated value")
        if _is_number(old_value) and _is_number(new_value) and abs(old_value - new_value) < 1e-9:
            return Check("value_change", "neutral", "the fix does not change the cell's value with today's data")
        return Check("value_change", "neutral", f"value changes from {old_value!r} to {new_value!r}")

    def check_peer_pattern(self, sheet: Sheet, target: Cell, finding: Finding) -> Check:
        peers = _peers(sheet, target)
        if len(peers) < MIN_PEERS:
            return Check("peer_pattern", "skipped", f"only {len(peers)} neighbouring formulas")
        shapes = [to_r1c1(p.formula, p.row, p.col) for p in peers]
        majority = max(set(shapes), key=shapes.count)
        n_major = shapes.count(majority)
        current = to_r1c1(finding.formula, target.row, target.col)
        fixed = to_r1c1(finding.expected, target.row, target.col)
        if fixed == majority and current != majority:
            return Check("peer_pattern", "supports", f"the fix matches {n_major} of {len(peers)} neighbouring formulas")
        if current == majority and fixed != majority:
            return Check("peer_pattern", "contradicts",
                         f"the formula already matches {n_major} of {len(peers)} neighbours; the fix would make it the odd one out")
        return Check("peer_pattern", "skipped", "neighbours do not share one formula shape")

    def check_sibling_sheets(self, wb: Workbook, sheet: Sheet, target: Cell, finding: Finding) -> Check:
        """Same address on the other sheets. Sheets built from one template repeat the same formula
        there, which is evidence about what this cell was meant to hold."""
        siblings = [other.get(target.row, target.col) for name, other in wb.sheets.items() if name != sheet.name]
        siblings = [c for c in siblings if c.is_formula]
        if len(siblings) < MIN_PEERS:
            return Check("sibling_sheets", "skipped", f"only {len(siblings)} other sheets hold a formula at {target.addr}")
        shapes = [to_r1c1(c.formula, c.row, c.col) for c in siblings]
        majority = max(set(shapes), key=shapes.count)
        n_major = shapes.count(majority)
        if n_major < MIN_PEERS:
            return Check("sibling_sheets", "skipped", "other sheets do not share one formula shape at this address")
        current = to_r1c1(finding.formula, target.row, target.col)
        fixed = to_r1c1(finding.expected, target.row, target.col)
        if fixed == majority and current != majority:
            return Check("sibling_sheets", "supports", f"the fix matches {n_major} of {len(siblings)} sibling sheets at {target.addr}")
        if current == majority and fixed != majority:
            return Check("sibling_sheets", "contradicts",
                         f"{n_major} of {len(siblings)} sibling sheets hold the same formula at {target.addr}; the fix would break the template")
        return Check("sibling_sheets", "skipped", "neither formula matches the sibling sheets")

    def check_range_delta(self, wb: Workbook, sheet: Sheet, finding: Finding) -> Check:
        if finding.type not in RANGE_TYPES:
            return Check("range_delta", "skipped", "not a range or reference fix")
        current = _referenced_cells(finding.formula, sheet.name)
        fixed = _referenced_cells(finding.expected, sheet.name)
        added = sorted(fixed - current)
        dropped = sorted(current - fixed)
        if not added and not dropped:
            return Check("range_delta", "skipped", "the fix references the same cells")
        if finding.type == "extra_rows":
            return self._dropped_cells_check(wb, dropped, finding)
        return self._added_cells_check(wb, added, finding.type in RANGE_SUPPORT_TYPES)

    def _added_cells_check(self, wb: Workbook, added: list[tuple[str, int, int]], can_support: bool) -> Check:
        """Cells the fix brings in. Blank or text cells contradict any fix. Real values support a
        range extension; for a moved reference or an added term they are only a precondition,
        since the model chose that cell because it holds a value."""
        cells = [wb.sheet(s).get(r, c) for (s, r, c) in added if wb.sheet(s) is not None]
        if not cells:
            return Check("range_delta", "skipped", "the fix adds no cells")
        real = [c for c in cells if c.is_number or c.is_formula]
        if not real:
            return Check("range_delta", "contradicts", f"the {len(cells)} cells the fix adds are blank or text")
        labelled = [c for c in real if _label(wb.sheet(added[0][0]), c)]
        detail = f"the fix adds {len(real)} real values ({len(labelled)} labelled) such as {real[0].addr}={real[0].value!r}"
        return Check("range_delta", "supports" if can_support else "neutral", detail)

    def _dropped_cells_check(self, wb: Workbook, dropped: list[tuple[str, int, int]], finding: Finding) -> Check:
        if not dropped:
            return Check("range_delta", "skipped", "the fix drops no cells")
        sheet = wb.sheet(dropped[0][0])
        kept = [sheet.get(r, c) for (s, r, c) in _referenced_cells(finding.expected, sheet.name) if s == sheet.name]
        foreign = []
        for (s, r, c) in dropped:
            cell = sheet.get(r, c)
            if is_parameter_label(_label(sheet, cell)) or self._format_differs(cell, kept) or self._magnitude_differs(cell, kept):
                foreign.append(cell)
        if foreign:
            return Check("range_delta", "supports",
                         f"dropped cell {foreign[0].addr} ({_label(sheet, foreign[0]) or 'no label'}) looks foreign to the block")
        return Check("range_delta", "contradicts", "the dropped cells look like ordinary members of the block")

    @staticmethod
    def _format_differs(cell: Cell, block: list[Cell]) -> bool:
        formats = [b.number_format for b in block if b.is_number]
        return bool(formats) and cell.number_format != max(set(formats), key=formats.count)

    @staticmethod
    def _magnitude_differs(cell: Cell, block: list[Cell]) -> bool:
        values = [abs(b.value) for b in block if b.is_number and b.value]
        if not values or not cell.is_number or not cell.value:
            return False
        ratio = abs(cell.value) / statistics.median(values)
        return ratio > 20 or ratio < 0.05

    def check_double_count(self, sheet: Sheet, finding: Finding) -> Check:
        if finding.type != "double_count":
            return Check("double_count", "skipped", "not a double-count finding")
        terms = additive_terms(finding.formula)
        leaves: dict[tuple[str, int, int], int] = {}
        for term in terms:
            for key in term_leaf_cells(term, sheet.name) or ():
                leaves[key] = leaves.get(key, 0) + 1
        twice = [k for k, n in leaves.items() if n >= 2]
        if twice:
            s, r, c = twice[0]
            return Check("double_count", "supports", f"{sheet.get(r, c).addr} is counted by two terms of the formula")
        inside = set(leaves)
        for (s, r, c) in list(inside):
            cell = sheet.get(r, c)
            if cell.is_formula and (term_leaf_cells(cell.formula, sheet.name) or set()) & inside:
                return Check("double_count", "supports", f"{cell.addr} inside the range is a subtotal of other cells in it")
        return Check("double_count", "contradicts", "no cell is counted twice by the current formula")

    def check_value_plausibility(self, sheet: Sheet, target: Cell, old_value, new_value) -> Check:
        peers = [p.value for p in _peers(sheet, target) if _is_number(p.value)]
        if new_value is None or len(peers) < MIN_PEERS or not _is_number(old_value) or not _is_number(new_value):
            return Check("value_plausibility", "skipped", "not enough numeric peers or no recalculated value")
        centre = statistics.median(peers)
        before, after = abs(old_value - centre), abs(new_value - centre)
        if after * PLAUSIBILITY_FACTOR <= before:
            return Check("value_plausibility", "supports", f"fixed value {new_value!r} is closer to the peer median {centre!r}")
        if before * PLAUSIBILITY_FACTOR <= after:
            return Check("value_plausibility", "contradicts", f"fixed value {new_value!r} is farther from the peer median {centre!r}")
        return Check("value_plausibility", "skipped", "fix does not move the value much relative to peers")

    # -- orchestration ----------------------------------------------------------------------

    def verify(self, wb: Workbook, wb_path: str, finding: Finding) -> Verification:
        sheet = wb.sheet(finding.sheet)
        if sheet is None or not finding.expected:
            return Verification("no_independent_check", [Check("setup", "skipped", "no sheet or no proposed fix")])
        target = next((c for c in sheet.formula_cells() if c.addr == finding.addr), None)
        if target is None:
            return Verification("no_independent_check", [Check("setup", "skipped", "target is not a formula cell")])
        recalc_check, new_value = self.check_recalculated_fix(wb_path, finding)
        checks = [
            recalc_check,
            self.check_value_change(target.value, new_value),
            self.check_peer_pattern(sheet, target, finding),
            self.check_sibling_sheets(wb, sheet, target, finding),
            self.check_range_delta(wb, sheet, finding),
            self.check_double_count(sheet, finding),
            self.check_value_plausibility(sheet, target, target.value, new_value),
        ]
        return Verification(_outcome(checks), checks, target.value, new_value)


def _outcome(checks: list[Check]) -> str:
    """Supported by at least one check: passed. Only contradicted: failed. Otherwise nothing could be
    tested. Recalculation and value change are necessary conditions, so they can only contradict."""
    results = {c.result for c in checks}
    if "supports" in results:
        return "passed"
    if "contradicts" in results:
        return "failed"
    return "no_independent_check"
