"""wrong_function: swap the aggregator when the label names the intent.

Fires only when the formula is exactly one aggregator over one range AND the row/column labels
imply that same aggregator (e.g. "Average daily volume" with AVERAGE). Then we swap to a different
function, so the mismatch between label and formula is the learnable signal.
"""
from __future__ import annotations

from sheettruth.mutators.base import Mutation, Mutator
from sheettruth.mutators.common import AGG_FUNCS, intent_function, single_agg_call, target_labels
from sheettruth.windows.cellinfo import CellContext

# realistic swaps, weighted toward the ones seen in real incidents
SWAPS = {
    "SUM": ["AVERAGE", "AVERAGE", "COUNT", "MAX"],
    "AVERAGE": ["SUM", "SUM", "MAX", "MIN"],
    "COUNT": ["SUM", "SUM", "AVERAGE"],
    "MAX": ["MIN", "AVERAGE", "SUM"],
    "MIN": ["MAX", "AVERAGE", "SUM"],
}


class WrongFunction(Mutator):
    name = "wrong_function"
    version = "1"

    def applies(self, ctx: CellContext) -> bool:
        call = single_agg_call(ctx.cell.formula)
        if not call or len(ctx.refs) != 1 or ctx.refs[0].size() < 2:
            return False
        func, _ = call
        return intent_function(target_labels(ctx)) == func

    def mutate(self, ctx: CellContext, rng):
        call = single_agg_call(ctx.cell.formula)
        if not call:
            return None
        func, rng_text = call
        new_func = rng.choice(SWAPS[func])
        broken = ctx.cell.formula.replace(func + "(", new_func + "(", 1)
        if broken == ctx.cell.formula:
            # case-insensitive write in the original
            import re
            broken = re.sub(r"^=\s*" + func, "=" + new_func, ctx.cell.formula, count=1, flags=re.I)
        label = ctx.row_path[0] if ctx.row_path else (ctx.col_path[0] if ctx.col_path else "the label")
        return Mutation(
            broken_formula=broken, expected_formula=ctx.cell.formula, error_type=self.name,
            reason_template=f'"{label}" calls for {func}, but the formula uses {new_func}.',
            touched_cells=[],
        )
