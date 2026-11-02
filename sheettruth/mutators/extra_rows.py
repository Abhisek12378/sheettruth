"""extra_rows: extend a range by one or two cells so that it reaches into a cell that is not part
of the block, such as a price or rate row above the data, or a different kind of figure below it.

Fires only when the formula is a single aggregator over one vertical or horizontal range and the
cell just past the chosen end is a non-blank number or formula that looks foreign to the block: a
parameter-like label, a different number format, or a magnitude far from the block's values.
"""
from __future__ import annotations

import statistics
from typing import Optional

from sheettruth.mutators.base import Mutation, Mutator
from sheettruth.mutators.common import col_header, is_parameter_label, replace_once, row_label, shift_ref_text, single_agg_call
from sheettruth.windows.cellinfo import Cell, CellContext, Ref, Sheet

MIN_RANGE_SIZE = 3
EXTEND_AT_START_PROBABILITY = 0.6
MAGNITUDE_RATIO = 20.0


def _label(sheet: Sheet, cell: Cell, vertical: bool) -> str:
    return row_label(sheet, cell.row, cell.col) if vertical else col_header(sheet, cell.row, cell.col)


def _looks_foreign(cell: Cell, label: str, block: list[Cell]) -> bool:
    """A labelled parameter, a different number format, or a value far from the block's typical size."""
    if is_parameter_label(label):
        return True
    formats = [c.number_format for c in block if c.is_number]
    if formats and cell.number_format != max(set(formats), key=formats.count):
        return True
    values = [abs(c.value) for c in block if c.is_number and c.value]
    if values and cell.is_number and cell.value:
        ratio = abs(cell.value) / statistics.median(values)
        return ratio > MAGNITUDE_RATIO or ratio < 1 / MAGNITUDE_RATIO
    return False


class ExtraRows(Mutator):
    name = "extra_rows"
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

    def _options(self, ctx: CellContext) -> list[tuple[str, Ref, Sheet, bool, Cell, str]]:
        """(func, ref, sheet, at_start, foreign cell, its label) for each end that can be extended."""
        candidate = self._candidate(ctx)
        if not candidate:
            return []
        func, ref, sheet = candidate
        block = [sheet.get(r, c) for (r, c) in ref.cells()]
        out = []
        for at_start in (True, False):
            if ref.is_vertical:
                r = ref.r1 - 1 if at_start else ref.r2 + 1
                cell = sheet.get(r, ref.c1) if r >= 1 else None
            else:
                c = ref.c1 - 1 if at_start else ref.c2 + 1
                cell = sheet.get(ref.r1, c) if c >= 1 else None
            if cell is None or not (cell.is_number or cell.is_formula) or cell.addr == ctx.cell.addr:
                continue
            label = _label(sheet, cell, ref.is_vertical)
            if _looks_foreign(cell, label, block):
                out.append((func, ref, sheet, at_start, cell, label))
        return out

    def applies(self, ctx: CellContext) -> bool:
        return bool(self._options(ctx))

    def mutate(self, ctx: CellContext, rng) -> Optional[Mutation]:
        options = self._options(ctx)
        if not options:
            return None
        starts = [o for o in options if o[3]]
        pick = starts if starts and rng.random() < EXTEND_AT_START_PROBABILITY else options
        func, ref, sheet, at_start, cell, label = rng.choice(pick)
        if ref.is_vertical:
            new = shift_ref_text(ref, ref.r1 - 1 if at_start else ref.r1, ref.r2 if at_start else ref.r2 + 1, ref.c1, ref.c1)
        else:
            new = shift_ref_text(ref, ref.r1, ref.r1, ref.c1 - 1 if at_start else ref.c1, ref.c2 if at_start else ref.c2 + 1)
        broken = replace_once(ctx.cell.formula, ref.text, new)
        if not broken:
            return None
        shown = label or cell.addr
        return Mutation(
            broken_formula=broken, expected_formula=ctx.cell.formula, error_type=self.name,
            reason_template=f'The {func} range reaches into "{shown}" ({cell.addr}), which is not part of the block.',
            touched_cells=[cell.addr],
        )
