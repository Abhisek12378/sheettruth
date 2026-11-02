"""wrong_reference: point one relative single-cell reference at a neighbouring row instead.

This is the classic slip in a filled-down formula: =G24*H25 where G25 was meant, or =D5*1500
where the row's own value sits in D10. Fires only when the formula has a relative single-cell
reference on the same sheet whose row is not anchored, and the cell one to three rows away is a
non-blank number or formula with a label, so the window can show which value belongs here.
"""
from __future__ import annotations

from typing import Optional

from sheettruth.mutators.base import Mutation, Mutator
from sheettruth.mutators.common import replace_once, row_label, shift_ref_text
from sheettruth.windows.cellinfo import CellContext, Ref, parse_refs

SHIFT_CHOICES = (-1, 1, -1, 1, -2, 2, -3, 3)
MAX_REFS = 6


class WrongReference(Mutator):
    name = "wrong_reference"
    version = "1"

    def _movable(self, ctx: CellContext) -> list[Ref]:
        f = ctx.cell.formula
        refs = parse_refs(f, ctx.sheet.name)
        if not refs or len(refs) > MAX_REFS:
            return []
        return [r for r in refs if not r.is_range and not r.abs_row1 and r.sheet == ctx.sheet.name
                and f.count(r.text) == 1]

    def _shifted(self, ctx: CellContext, ref: Ref, delta: int):
        """The cell `delta` rows away, if it can plausibly stand in for the original."""
        row = ref.r1 + delta
        if row < 1 or (row, ref.c1) == (ctx.cell.row, ctx.cell.col):
            return None
        cell = ctx.sheet.get(row, ref.c1)
        if not (cell.is_number or cell.is_formula):
            return None
        return cell

    def applies(self, ctx: CellContext) -> bool:
        return any(self._shifted(ctx, r, d) is not None for r in self._movable(ctx) for d in (-1, 1))

    def mutate(self, ctx: CellContext, rng) -> Optional[Mutation]:
        refs = self._movable(ctx)
        rng.shuffle(refs)
        for ref in refs:
            for delta in rng.sample(SHIFT_CHOICES, len(SHIFT_CHOICES)):
                cell = self._shifted(ctx, ref, delta)
                if cell is None:
                    continue
                new_text = shift_ref_text(ref, cell.row, cell.row, ref.c1, ref.c1)
                broken = replace_once(ctx.cell.formula, ref.text, new_text)
                if not broken:
                    continue
                old_label = row_label(ctx.sheet, ref.r1, ref.c1) or ref.a1()
                new_label = row_label(ctx.sheet, cell.row, cell.col) or cell.addr
                return Mutation(
                    broken_formula=broken, expected_formula=ctx.cell.formula, error_type=self.name,
                    reason_template=f'"{new_label}" ({cell.addr}) is used where "{old_label}" ({ref.a1()}) belongs.',
                    touched_cells=[cell.addr, ref.a1()],
                )
        return None
