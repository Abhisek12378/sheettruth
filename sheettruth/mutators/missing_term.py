"""missing_term: leave one labelled term out of a sum of cell references.

Fires only when the formula is a plain addition or subtraction of three or more single-cell
references on the same sheet, so dropping one term leaves a formula that still looks complete.
The dropped term must have a label; the window then shows the labelled value that is left out.
"""
from __future__ import annotations

from typing import Optional

from sheettruth.mutators.base import Mutation, Mutator
from sheettruth.mutators.common import ref_label, top_level_operators
from sheettruth.windows.cellinfo import CellContext, parse_refs

MIN_TERMS = 3


class MissingTerm(Mutator):
    name = "missing_term"
    version = "1"

    def _terms(self, ctx: CellContext) -> list[tuple[int, int, str]]:
        """(start, end, operator before) of every top-level term, or [] when the shape does not fit."""
        f = ctx.cell.formula
        ops = top_level_operators(f)
        if len(ops) < MIN_TERMS - 1 or any(o not in "+-" for _, o in ops):
            return []
        bounds = [1] + [i + 1 for i, _ in ops]
        ends = [i for i, _ in ops] + [len(f)]
        terms = []
        for k, (s, e) in enumerate(zip(bounds, ends)):
            text = f[s:e].strip()
            refs = parse_refs("=" + text, ctx.sheet.name)
            if len(refs) != 1 or refs[0].is_range or refs[0].sheet != ctx.sheet.name or refs[0].text != text:
                return []
            terms.append((s, e, ops[k - 1][1] if k else "+"))
        return terms

    def _droppable(self, ctx: CellContext) -> list[tuple[int, int, str, str]]:
        f = ctx.cell.formula
        out = []
        for k, (s, e, op) in enumerate(self._terms(ctx)):
            if k == 0:
                continue
            ref = parse_refs("=" + f[s:e].strip(), ctx.sheet.name)[0]
            label = ref_label(ctx, ref)
            if label:
                out.append((s, e, op, label))
        return out

    def applies(self, ctx: CellContext) -> bool:
        return bool(self._droppable(ctx))

    def mutate(self, ctx: CellContext, rng) -> Optional[Mutation]:
        options = self._droppable(ctx)
        if not options:
            return None
        s, e, op, label = rng.choice(options)
        f = ctx.cell.formula
        term = f[s:e].strip()
        broken = (f[:s - 1] + f[e:]).rstrip()
        verb = "added" if op == "+" else "subtracted"
        return Mutation(
            broken_formula=broken, expected_formula=f, error_type=self.name,
            reason_template=f'"{label}" ({term}) should be {verb} here but is left out.',
            touched_cells=[term],
        )
