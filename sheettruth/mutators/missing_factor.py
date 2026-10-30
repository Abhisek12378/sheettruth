"""missing_factor: drop one multiplier from a product of three or more cell references.

Fires only when the formula is a pure product (only * at the top level) with at least three
operands, and the operand we drop points to a cell that has a label or header (a rate, factor,
units...). We prefer dropping an absolutely-referenced operand ($C$8): those are the assumptions
people forget.
"""
from __future__ import annotations

import re

from sheettruth.mutators.base import Mutation, Mutator
from sheettruth.mutators.common import is_pure_product, label_for_ref, top_level_operators
from sheettruth.windows.cellinfo import CellContext, parse_refs


class MissingFactor(Mutator):
    name = "missing_factor"
    version = "1"

    def _operands(self, ctx: CellContext):
        f = ctx.cell.formula
        if not is_pure_product(f):
            return []
        ops = [i for i, _ in top_level_operators(f)]
        bounds = [1] + [i + 1 for i in ops]
        ends = ops + [len(f)]
        out = []
        for k, (s, e) in enumerate(zip(bounds, ends)):
            text = f[s:e].strip()
            refs = parse_refs("=" + text, ctx.sheet.name)
            if len(refs) != 1 or refs[0].is_range:
                out.append((k, text, None, ""))
                continue
            out.append((k, text, refs[0], label_for_ref(ctx, refs[0])))
        return out

    def applies(self, ctx: CellContext) -> bool:
        ops = self._operands(ctx)
        if len(ops) < 3:
            return False
        return any(ref is not None and label for _, _, ref, label in ops)

    def mutate(self, ctx: CellContext, rng):
        ops = self._operands(ctx)
        droppable = [o for o in ops if o[2] is not None and o[3]]
        if len(ops) < 3 or not droppable:
            return None
        abs_first = [o for o in droppable if "$" in o[1]] or droppable
        k, text, ref, label = rng.choice(abs_first)
        f = ctx.cell.formula
        # remove "*text" or "text*" exactly once at the top level
        if k == 0:
            pat = re.escape(text) + r"\s*\*\s*"
        else:
            pat = r"\s*\*\s*" + re.escape(text)
        broken, n = re.subn(pat, "", f, count=1)
        if n != 1 or broken == f:
            return None
        return Mutation(
            broken_formula=broken, expected_formula=f, error_type=self.name,
            reason_template=f'The product leaves out "{label}" ({text}), which the neighbouring cells apply.',
            touched_cells=[ref.a1()],
        )
