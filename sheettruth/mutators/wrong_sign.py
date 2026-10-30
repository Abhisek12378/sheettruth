"""wrong_sign: flip a top-level minus to plus (or plus to minus) in an arithmetic formula.

Fires when the formula has a top-level + or - between cell references and the operand on the
right of that operator has a label (so the model can read what is being added or subtracted).
Prefers flipping a minus whose operand label carries deduction words (cost, loss, tax, less...).
"""
from __future__ import annotations

from sheettruth.mutators.base import Mutation, Mutator
from sheettruth.mutators.common import DEDUCTION_WORDS, label_for_ref, top_level_operators
from sheettruth.windows.cellinfo import CellContext, parse_refs


class WrongSign(Mutator):
    name = "wrong_sign"
    version = "1"

    def _options(self, ctx: CellContext):
        f = ctx.cell.formula
        ops = [(i, o) for i, o in top_level_operators(f) if o in "+-"]
        out = []
        for i, o in ops:
            # operand text right after the operator, up to the next top-level operator
            nxt = [j for j, _ in top_level_operators(f) if j > i]
            end = nxt[0] if nxt else len(f)
            operand = f[i + 1:end].strip()
            refs = parse_refs("=" + operand, ctx.sheet.name)
            if len(refs) != 1 or refs[0].is_range and refs[0].size() > 1 and "SUM" not in operand.upper():
                continue
            label = label_for_ref(ctx, refs[0])
            if not label:
                continue
            deduction = any(w in label.lower() for w in DEDUCTION_WORDS)
            out.append((i, o, operand, label, deduction))
        return out

    def applies(self, ctx: CellContext) -> bool:
        return bool(self._options(ctx))

    def mutate(self, ctx: CellContext, rng):
        opts = self._options(ctx)
        if not opts:
            return None
        # prefer a minus with a deduction-word label; those are the realistic accidents
        pref = [o for o in opts if o[1] == "-" and o[4]] or [o for o in opts if o[1] == "-"] or opts
        i, o, operand, label, _ = rng.choice(pref)
        f = ctx.cell.formula
        new_op = "+" if o == "-" else "-"
        broken = f[:i] + new_op + f[i + 1:]
        verb = "added" if new_op == "+" else "subtracted"
        return Mutation(
            broken_formula=broken, expected_formula=f, error_type=self.name,
            reason_template=f'"{label}" ({operand}) is {verb} here but should be {"subtracted" if new_op == "+" else "added"}.',
            touched_cells=[r.a1() for r in parse_refs("=" + operand, ctx.sheet.name)],
        )
