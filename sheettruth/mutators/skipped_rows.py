"""skipped_rows: shrink a range so that one to three real data cells fall outside the aggregate.

Fires only when the formula is a single aggregator over one vertical or horizontal range of at
least four cells, and the cells dropped are non-blank and labelled. The dropped cells visibly
belong to the block, which keeps the injected error both real and learnable.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from sheettruth.mutators.base import Mutation, Mutator
from sheettruth.mutators.common import col_header, replace_once, row_label, shift_ref_text, single_agg_call
from sheettruth.windows.cellinfo import Cell, CellContext, Ref, Sheet

MIN_RANGE_SIZE = 4
DROP_COUNT_CHOICES = (1, 1, 2, 3)
SHRINK_FROM_END_PROBABILITY = 0.75


@dataclass
class Shrink:
    new_range_text: str
    dropped: list[Cell]
    labels: list[str]


def _shrink_vertical(ref: Ref, sheet: Sheet, k: int, from_end: bool) -> Shrink:
    if from_end:
        rows = range(ref.r2 - k + 1, ref.r2 + 1)
        text = shift_ref_text(ref, ref.r1, ref.r2 - k, ref.c1, ref.c1)
    else:
        rows = range(ref.r1, ref.r1 + k)
        text = shift_ref_text(ref, ref.r1 + k, ref.r2, ref.c1, ref.c1)
    dropped = [sheet.get(r, ref.c1) for r in rows]
    return Shrink(text, dropped, [row_label(sheet, c.row, c.col) for c in dropped])


def _shrink_horizontal(ref: Ref, sheet: Sheet, k: int, from_end: bool) -> Shrink:
    if from_end:
        cols = range(ref.c2 - k + 1, ref.c2 + 1)
        text = shift_ref_text(ref, ref.r1, ref.r1, ref.c1, ref.c2 - k)
    else:
        cols = range(ref.c1, ref.c1 + k)
        text = shift_ref_text(ref, ref.r1, ref.r1, ref.c1 + k, ref.c2)
    dropped = [sheet.get(ref.r1, c) for c in cols]
    return Shrink(text, dropped, [col_header(sheet, c.row, c.col) for c in dropped])


class SkippedRows(Mutator):
    name = "skipped_rows"
    version = "1"

    def _candidate(self, ctx: CellContext) -> Optional[tuple[str, Ref, Sheet]]:
        call = single_agg_call(ctx.cell.formula)
        if not call or len(ctx.refs) != 1:
            return None
        ref = ctx.refs[0]
        if not (ref.is_vertical or ref.is_horizontal) or ref.size() < MIN_RANGE_SIZE:
            return None
        sheet = ctx.wb.sheet(ref.sheet)
        return (call[0], ref, sheet) if sheet is not None else None

    def applies(self, ctx: CellContext) -> bool:
        candidate = self._candidate(ctx)
        if not candidate:
            return False
        _, ref, sheet = candidate
        if ref.is_vertical:
            last = sheet.get(ref.r2, ref.c1)
            label = row_label(sheet, ref.r2, ref.c1)
        else:
            last = sheet.get(ref.r1, ref.c2)
            label = col_header(sheet, ref.r1, ref.c2)
        return (last.is_number or last.is_formula) and bool(label)

    def mutate(self, ctx: CellContext, rng) -> Optional[Mutation]:
        candidate = self._candidate(ctx)
        if not candidate:
            return None
        func, ref, sheet = candidate
        k = min(rng.choice(DROP_COUNT_CHOICES), ref.size() - 2)
        from_end = rng.random() < SHRINK_FROM_END_PROBABILITY
        shrink = (_shrink_vertical if ref.is_vertical else _shrink_horizontal)(ref, sheet, k, from_end)
        if any(c.is_blank for c in shrink.dropped):
            return None
        broken = replace_once(ctx.cell.formula, ref.text, shrink.new_range_text)
        if not broken:
            return None
        names = ", ".join(l for l in shrink.labels if l) or ", ".join(c.addr for c in shrink.dropped)
        return Mutation(
            broken_formula=broken,
            expected_formula=ctx.cell.formula,
            error_type=self.name,
            reason_template=f"The {func} range stops short: {names} belong to the same block but are left out.",
            touched_cells=[c.addr for c in shrink.dropped],
        )
