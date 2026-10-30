"""Helpers shared by the mutators."""
from __future__ import annotations

import re
from typing import Optional

from openpyxl.formula import Tokenizer
from openpyxl.utils import get_column_letter

from sheettruth.windows.cellinfo import CellContext, Ref, Sheet, label_text

AGG_FUNCS = ("SUM", "AVERAGE", "COUNT", "MIN", "MAX")

INTENT_WORDS = {
    "SUM": ("total", "sum", "net", "gross", "aggregate", "combined", "overall"),
    "AVERAGE": ("average", "avg", "mean", "per day", "per month", "daily rate", "typical"),
    "COUNT": ("count", "number of", "no. of", "# of", "headcount", "how many", "qty of"),
    "MAX": ("max", "maximum", "highest", "peak", "largest"),
    "MIN": ("min", "minimum", "lowest", "smallest", "floor"),
}

DEDUCTION_WORDS = ("less", "cost", "expense", "loss", "tax", "discount", "liabilit", "outflow",
                   "deduction", "minus", "paid", "payment", "charge", "fee", "depreciation", "rebate")


def row_label(sh: Sheet, row: int, col: int) -> str:
    for c in range(col - 1, 0, -1):
        cell = sh.get(row, c)
        if cell.is_text:
            return label_text(cell.value)
    return ""


def col_header(sh: Sheet, row: int, col: int) -> str:
    for r in range(row - 1, 0, -1):
        cell = sh.get(r, col)
        if cell.is_text:
            return label_text(cell.value)
    return ""


def label_for_ref(ctx: CellContext, ref: Ref) -> str:
    sh = ctx.wb.sheet(ref.sheet) or ctx.sheet
    return row_label(sh, ref.r1, ref.c1) or col_header(sh, ref.r1, ref.c1)


def target_labels(ctx: CellContext) -> str:
    """Row path plus column path, lowercased, for intent-word checks."""
    return " | ".join(ctx.row_path + ctx.col_path).lower()


def intent_function(labels: str) -> Optional[str]:
    """Which aggregator the labels call for, if exactly one is implied."""
    hits = [f for f, words in INTENT_WORDS.items() if any(w in labels for w in words)]
    return hits[0] if len(hits) == 1 else None


def single_agg_call(formula: str) -> Optional[tuple[str, str]]:
    """If the formula is exactly =FUNC(single_range), return (FUNC, range_text)."""
    m = re.match(r"^=\s*(SUM|AVERAGE|COUNT|MIN|MAX)\s*\(\s*([^(),]+)\s*\)\s*$", formula, re.I)
    if not m:
        return None
    return m.group(1).upper(), m.group(2).strip()


def replace_once(formula: str, old: str, new: str) -> Optional[str]:
    """Replace the first exact occurrence of a token text, or None if it is not present once."""
    if formula.count(old) != 1:
        return None
    return formula.replace(old, new, 1)


def shift_ref_text(ref: Ref, new_r1: int, new_r2: int, new_c1: int, new_c2: int) -> str:
    """Rebuild a range text keeping the original $ anchors and sheet prefix."""
    m = re.match(r"^(?P<sheet>(?:'[^']+'|[A-Za-z0-9_\.]+)!)?(?P<c1>\$?)[A-Za-z]{1,3}(?P<r1>\$?)\d+(?::(?P<c2>\$?)[A-Za-z]{1,3}(?P<r2>\$?)\d+)?$", ref.text)
    sheet = (m.group("sheet") or "") if m else ""
    c1d, r1d = ((m.group("c1") or ""), (m.group("r1") or "")) if m else ("", "")
    c2d, r2d = ((m.group("c2") or ""), (m.group("r2") or "")) if m else ("", "")
    a = f"{sheet}{c1d}{get_column_letter(new_c1)}{r1d}{new_r1}"
    if (new_r1, new_c1) != (new_r2, new_c2):
        a += f":{c2d}{get_column_letter(new_c2)}{r2d}{new_r2}"
    return a


def top_level_operators(formula: str) -> list[tuple[int, str]]:
    """Positions of + - * / at parenthesis depth 0 (outside strings)."""
    out, depth, i = [], 0, 1 if formula.startswith("=") else 0
    while i < len(formula):
        ch = formula[i]
        if ch == '"':
            j = formula.find('"', i + 1)
            i = (len(formula) if j < 0 else j) + 1
            continue
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        elif depth == 0 and ch in "+-*/":
            out.append((i, ch))
        i += 1
    return out


def is_pure_product(formula: str) -> bool:
    ops = top_level_operators(formula)
    return len(ops) >= 2 and all(o == "*" for _, o in ops)
