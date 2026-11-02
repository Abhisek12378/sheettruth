"""double_count: add a cell that is already inside the summed range, or extend a range over a subtotal.

Two variants, chosen at random when both are possible:
  A. =SUM(C5:C12)  ->  =SUM(C5:C12)+C10        (C10 is inside the range and has a label)
  B. =SUM(C5:C12)  ->  =SUM(C5:C13)            (C13 is a subtotal/total of cells inside the range)
Variant B fires only when the cell just past the range end is itself a formula that sums cells
inside the range, which is exactly how real double counts happen.
"""
from __future__ import annotations

from sheettruth.mutators.base import Mutation, Mutator
from sheettruth.mutators.common import col_header, replace_once, row_label, shift_ref_text, single_agg_call
from sheettruth.windows.cellinfo import CellContext, term_leaf_cells


class DoubleCount(Mutator):
    name = "double_count"
    version = "1"

    def _candidate(self, ctx: CellContext):
        call = single_agg_call(ctx.cell.formula)
        if not call or call[0] != "SUM" or len(ctx.refs) != 1:
            return None
        ref = ctx.refs[0]
        if not (ref.is_vertical or ref.is_horizontal) or ref.size() < 3:
            return None
        sh = ctx.wb.sheet(ref.sheet)
        return (ref, sh) if sh is not None else None

    def _inside_with_label(self, ref, sh):
        out = []
        for (r, c) in ref.cells():
            cell = sh.get(r, c)
            if not (cell.is_number or cell.is_formula):
                continue
            lab = row_label(sh, r, c) if ref.is_vertical else col_header(sh, r, c)
            if lab:
                out.append((cell, lab))
        return out

    def _subtotal_after(self, ref, sh, target=None):
        """The cell just past the range end, if it is a formula summing cells inside the range.
        The target cell itself never qualifies: extending onto it would create a circular reference."""
        r, c = (ref.r2 + 1, ref.c1) if ref.is_vertical else (ref.r1, ref.c2 + 1)
        cell = sh.get(r, c)
        if target is not None and (r, c) == (target.row, target.col):
            return None
        if not cell.is_formula:
            return None
        leaf = term_leaf_cells(cell.formula, sh.name)
        inside = {(sh.name, rr, cc) for (rr, cc) in ref.cells()}
        if leaf and leaf & inside:
            return cell
        return None

    def applies(self, ctx: CellContext) -> bool:
        cand = self._candidate(ctx)
        if not cand:
            return False
        ref, sh = cand
        return bool(self._inside_with_label(ref, sh)) or self._subtotal_after(ref, sh, ctx.cell) is not None

    def mutate(self, ctx: CellContext, rng):
        cand = self._candidate(ctx)
        if not cand:
            return None
        ref, sh = cand
        f = ctx.cell.formula
        sub = self._subtotal_after(ref, sh, ctx.cell)
        inside = self._inside_with_label(ref, sh)
        use_b = sub is not None and (not inside or rng.random() < 0.5)
        if use_b:
            if ref.is_vertical:
                new = shift_ref_text(ref, ref.r1, ref.r2 + 1, ref.c1, ref.c1)
            else:
                new = shift_ref_text(ref, ref.r1, ref.r1, ref.c1, ref.c2 + 1)
            broken = replace_once(f, ref.text, new)
            if not broken:
                return None
            lab = row_label(sh, sub.row, sub.col) or col_header(sh, sub.row, sub.col) or sub.addr
            return Mutation(broken, f, self.name,
                            f'The range now includes "{lab}" ({sub.addr}), a subtotal of cells already in the range.',
                            [sub.addr])
        cell, lab = rng.choice(inside)
        prefix = "" if ref.sheet == ctx.sheet.name else f"'{ref.sheet}'!"
        broken = f + "+" + prefix + cell.addr
        return Mutation(broken, f, self.name,
                        f'"{lab}" ({cell.addr}) is already inside the summed range and is added again.',
                        [cell.addr])
