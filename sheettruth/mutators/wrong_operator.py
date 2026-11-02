"""wrong_operator: a product written as a division, or parentheses left out.

Two shapes:
  A. =B5*C$2  ->  =B5/C$2      (the multiplier is divided by instead; units come out wrong)
  B. =(B12-C12)/C12  ->  =B12-C12/C12   (the grouping is lost, so only the last term is divided)
Shape A fires on a two-operand product where the second operand has a label. Shape B fires on a
parenthesised sum or difference followed by a single * or / and one more operand.
"""
from __future__ import annotations

import re
from typing import Optional

from sheettruth.mutators.base import Mutation, Mutator
from sheettruth.mutators.common import ref_label, top_level_operators
from sheettruth.windows.cellinfo import CellContext, parse_refs

GROUPED = re.compile(r"^=\s*\(([^()]+[+-][^()]+)\)\s*([*/])\s*([^()+\-*/]+)\s*$")


class WrongOperator(Mutator):
    name = "wrong_operator"
    version = "1"

    def _product(self, ctx: CellContext) -> Optional[tuple[int, str]]:
        """(position of the single top-level *, label of the right operand) for a two-operand product."""
        f = ctx.cell.formula
        ops = top_level_operators(f)
        if len(ops) != 1 or ops[0][1] != "*" or "(" in f:
            return None
        right = f[ops[0][0] + 1:].strip()
        refs = parse_refs("=" + right, ctx.sheet.name)
        if len(refs) != 1 or refs[0].is_range:
            return None
        label = ref_label(ctx, refs[0])
        return (ops[0][0], label) if label else None

    def _grouped(self, ctx: CellContext) -> Optional[re.Match]:
        m = GROUPED.match(ctx.cell.formula)
        return m if m and parse_refs(ctx.cell.formula, ctx.sheet.name) else None

    def applies(self, ctx: CellContext) -> bool:
        return self._product(ctx) is not None or self._grouped(ctx) is not None

    def mutate(self, ctx: CellContext, rng) -> Optional[Mutation]:
        f = ctx.cell.formula
        grouped = self._grouped(ctx)
        product = self._product(ctx)
        if grouped and (not product or rng.random() < 0.5):
            inner, op, tail = grouped.group(1).strip(), grouped.group(2), grouped.group(3).strip()
            verb = "dividing by" if op == "/" else "multiplying by"
            return Mutation(
                broken_formula=f"={inner}{op}{tail}", expected_formula=f, error_type=self.name,
                reason_template=f'Parentheses are missing: "{inner}" must be computed before {verb} {tail}.',
                touched_cells=[r.a1() for r in parse_refs(f, ctx.sheet.name)],
            )
        if not product:
            return None
        pos, label = product
        right = f[pos + 1:].strip()
        return Mutation(
            broken_formula=f[:pos] + "/" + f[pos + 1:], expected_formula=f, error_type=self.name,
            reason_template=f'The formula divides by "{label}" ({right}) where a product is expected.',
            touched_cells=[right],
        )
