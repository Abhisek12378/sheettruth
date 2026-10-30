"""Workbook model and per-cell context extraction.

Loads an .xlsx twice (formulas and cached values), exposes a simple grid, and
derives everything the window builder and the mutators need about one cell:
tokens, references, R1C1 form, header paths, peers, additive terms.

No LLM here. Everything is deterministic.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Iterable, Optional

import openpyxl
from openpyxl.formula import Tokenizer
from openpyxl.utils import column_index_from_string, get_column_letter

ERROR_VALUES = {"#REF!", "#VALUE!", "#DIV/0!", "#NAME?", "#N/A", "#NUM!", "#NULL!"}
TOTAL_WORDS = ("total", "subtotal", "sub-total", "sum", "grand", "net")
IN_SCOPE_FUNCS = {"SUM", "AVERAGE", "COUNT", "MIN", "MAX"}

_REF_RE = re.compile(
    r"^(?:(?P<sheet>'[^']+'|[A-Za-z0-9_\.]+)!)?"
    r"(?P<c1>\$?[A-Za-z]{1,3})(?P<r1>\$?\d+)"
    r"(?::(?P<c2>\$?[A-Za-z]{1,3})(?P<r2>\$?\d+))?$"
)


@dataclass
class Cell:
    row: int
    col: int
    formula: Optional[str]      # "=..." or None
    value: object               # cached value after recalculation, may be None
    number_format: str = "General"
    bold: bool = False
    comment: Optional[str] = None

    @property
    def addr(self) -> str:
        return f"{get_column_letter(self.col)}{self.row}"

    @property
    def is_formula(self) -> bool:
        return isinstance(self.formula, str) and self.formula.startswith("=")

    @property
    def is_text(self) -> bool:
        return isinstance(self.value, str) and not self.is_formula and self.value.strip() != ""

    @property
    def is_number(self) -> bool:
        return isinstance(self.value, (int, float)) and not isinstance(self.value, bool)

    @property
    def is_blank(self) -> bool:
        return self.formula is None and (self.value is None or (isinstance(self.value, str) and self.value.strip() == ""))

    @property
    def is_error(self) -> bool:
        return isinstance(self.value, str) and self.value in ERROR_VALUES


@dataclass
class Sheet:
    name: str
    cells: dict[tuple[int, int], Cell] = field(default_factory=dict)
    hidden_rows: set[int] = field(default_factory=set)
    merged_top_left: dict[tuple[int, int], tuple[int, int]] = field(default_factory=dict)
    max_row: int = 0
    max_col: int = 0

    def get(self, row: int, col: int) -> Cell:
        c = self.cells.get((row, col))
        if c is None:
            # merged continuation cells read from their anchor
            anchor = self.merged_top_left.get((row, col))
            if anchor and anchor in self.cells:
                return self.cells[anchor]
            return Cell(row, col, None, None)
        return c

    def formula_cells(self) -> Iterable[Cell]:
        return (c for c in self.cells.values() if c.is_formula)


FULLY_ABSOLUTE_REF = re.compile(r"\$[A-Za-z]{1,3}\$\d")
MAX_RANGE_FOR_REFERENCE_INDEX = 50


def _merged_anchor_map(ws) -> dict[tuple[int, int], tuple[int, int]]:
    """Map every non-anchor cell of a merged range to the range's top-left cell."""
    anchors: dict[tuple[int, int], tuple[int, int]] = {}
    for rng in ws.merged_cells.ranges:
        top_left = (rng.min_row, rng.min_col)
        for r in range(rng.min_row, rng.max_row + 1):
            for c in range(rng.min_col, rng.max_col + 1):
                if (r, c) != top_left:
                    anchors[(r, c)] = top_left
    return anchors


def _hidden_rows(ws) -> set[int]:
    return {r for r, dim in ws.row_dimensions.items() if dim.hidden}


def _make_cell(cf, cached_value, strip_formula_values: bool) -> Cell:
    """Build a Cell from an openpyxl formula cell and its cached value."""
    is_formula = isinstance(cf.value, str) and cf.value.startswith("=")
    formula = cf.value if is_formula else None
    value = cached_value if is_formula else cf.value
    if is_formula and strip_formula_values:
        value = None
    comment = cf.comment.text.strip() if cf.comment and cf.comment.text else None
    return Cell(
        row=cf.row, col=cf.column, formula=formula, value=value,
        number_format=cf.number_format or "General",
        bold=bool(cf.font and cf.font.bold),
        comment=comment,
    )


def _load_sheet(ws_formulas, ws_values, strip_formula_values: bool) -> Sheet:
    sheet = Sheet(name=ws_formulas.title, max_row=ws_formulas.max_row or 0, max_col=ws_formulas.max_column or 0)
    sheet.merged_top_left = _merged_anchor_map(ws_formulas)
    sheet.hidden_rows = _hidden_rows(ws_formulas)
    for row in ws_formulas.iter_rows():
        for cf in row:
            if cf.value is None:
                continue
            cached = ws_values.cell(row=cf.row, column=cf.column).value
            sheet.cells[(cf.row, cf.column)] = _make_cell(cf, cached, strip_formula_values)
    return sheet


def _normalise_sheet_name(name: str) -> str:
    return re.sub(r"\s+", "", name.lower())


class Workbook:
    """Formulas plus cached values for one .xlsx, read once.

    strip_formula_values=True hides the cached value of every formula cell. It is used when a
    corrupted copy could not be recalculated, so stale values never reach the model.
    """

    def __init__(self, path: str, strip_formula_values: bool = False):
        self.path = path
        self.strip_formula_values = strip_formula_values
        wb_formulas = openpyxl.load_workbook(path, data_only=False)
        wb_values = openpyxl.load_workbook(path, data_only=True)
        self.sheetnames = list(wb_formulas.sheetnames)
        self.sheets: dict[str, Sheet] = {
            name: _load_sheet(wb_formulas[name], wb_values[name], strip_formula_values)
            for name in self.sheetnames
        }
        self._ref_index: Optional[dict[str, dict[tuple[int, int], int]]] = None

    def sheet(self, name: str) -> Optional[Sheet]:
        """Look a sheet up by name, tolerating case and whitespace differences."""
        if name in self.sheets:
            return self.sheets[name]
        by_norm = {_normalise_sheet_name(k): k for k in self.sheets}
        return self.sheets.get(by_norm.get(_normalise_sheet_name(name), ""))

    def reference_counts(self) -> dict[str, dict[tuple[int, int], int]]:
        """How many formulas reference each cell through a fully absolute ($B$2) reference, per sheet.

        Only fully absolute references count. Assumptions such as rates and factors are almost
        always referenced that way, while table inputs are referenced relatively.
        """
        if self._ref_index is not None:
            return self._ref_index
        index: dict[str, dict[tuple[int, int], int]] = {n: {} for n in self.sheets}
        for sheet in self.sheets.values():
            for cell in sheet.formula_cells():
                for ref in parse_refs(cell.formula, sheet.name):
                    if ref.size() > MAX_RANGE_FOR_REFERENCE_INDEX or ref.sheet not in index:
                        continue
                    if not FULLY_ABSOLUTE_REF.search(ref.text):
                        continue
                    for key in ref.cells():
                        index[ref.sheet][key] = index[ref.sheet].get(key, 0) + 1
        self._ref_index = index
        return index


@dataclass(frozen=True)
class Ref:
    sheet: str
    r1: int
    c1: int
    r2: int
    c2: int
    text: str                      # as written, e.g. "$B10" or "Detail!F3:F17"
    abs_col1: bool = False
    abs_row1: bool = False

    @property
    def is_range(self) -> bool:
        return (self.r1, self.c1) != (self.r2, self.c2)

    @property
    def is_vertical(self) -> bool:
        return self.c1 == self.c2 and self.r1 != self.r2

    @property
    def is_horizontal(self) -> bool:
        return self.r1 == self.r2 and self.c1 != self.c2

    def size(self) -> int:
        return (self.r2 - self.r1 + 1) * (self.c2 - self.c1 + 1)

    def cells(self):
        for r in range(self.r1, self.r2 + 1):
            for c in range(self.c1, self.c2 + 1):
                yield (r, c)

    def a1(self) -> str:
        a = f"{get_column_letter(self.c1)}{self.r1}"
        if self.is_range:
            a += f":{get_column_letter(self.c2)}{self.r2}"
        return a


def _strip_sheet(s: str) -> str:
    s = s.strip()
    if s.startswith("'") and s.endswith("'"):
        s = s[1:-1]
    return s


def parse_refs(formula: str, default_sheet: str) -> list[Ref]:
    """All cell/range references in a formula, in order. Named ranges and whole-column refs are skipped."""
    out: list[Ref] = []
    try:
        toks = Tokenizer(formula).items
    except Exception:
        return out
    for t in toks:
        if t.type != "OPERAND" or t.subtype != "RANGE":
            continue
        m = _REF_RE.match(t.value)
        if not m:
            continue
        sheet = _strip_sheet(m.group("sheet")) if m.group("sheet") else default_sheet
        c1 = column_index_from_string(m.group("c1").replace("$", "").upper())
        r1 = int(m.group("r1").replace("$", ""))
        if m.group("c2"):
            c2 = column_index_from_string(m.group("c2").replace("$", "").upper())
            r2 = int(m.group("r2").replace("$", ""))
        else:
            c2, r2 = c1, r1
        r1, r2 = min(r1, r2), max(r1, r2)
        c1, c2 = min(c1, c2), max(c1, c2)
        out.append(Ref(sheet, r1, c1, r2, c2, t.value,
                       abs_col1=m.group("c1").startswith("$"), abs_row1=m.group("r1").startswith("$")))
    return out


def to_r1c1(formula: str, row: int, col: int) -> str:
    """Relative R1C1 form of an A1 formula, anchored at (row, col). Absolute parts stay absolute."""
    try:
        toks = Tokenizer(formula).items
    except Exception:
        return formula
    parts = ["="]
    for t in toks:
        if t.type == "OPERAND" and t.subtype == "RANGE":
            m = _REF_RE.match(t.value)
            if m:
                prefix = (m.group("sheet") + "!") if m.group("sheet") else ""
                def one(cs, rs):
                    c = column_index_from_string(cs.replace("$", "").upper())
                    r = int(rs.replace("$", ""))
                    rc = f"R{r}" if rs.startswith("$") else (f"R[{r - row}]" if r != row else "R")
                    cc = f"C{c}" if cs.startswith("$") else (f"C[{c - col}]" if c != col else "C")
                    return rc + cc
                s = prefix + one(m.group("c1"), m.group("r1"))
                if m.group("c2"):
                    s += ":" + one(m.group("c2"), m.group("r2"))
                parts.append(s)
                continue
        parts.append(t.value)
    return "".join(parts)


def functions_in(formula: str) -> list[str]:
    try:
        return [t.value[:-1].upper() for t in Tokenizer(formula).items if t.type == "FUNC" and t.subtype == "OPEN"]
    except Exception:
        return []


def additive_terms(formula: str) -> list[str]:
    """Split the top level of a formula on + and - (outside parentheses). Returns signed term strings."""
    body = formula[1:] if formula.startswith("=") else formula
    terms, depth, cur, sign = [], 0, "", "+"
    i = 0
    while i < len(body):
        ch = body[i]
        if ch == '"':
            j = body.find('"', i + 1)
            j = len(body) - 1 if j < 0 else j
            cur += body[i:j + 1]
            i = j + 1
            continue
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if depth == 0 and ch in "+-" and cur.strip() and cur.strip()[-1] not in "*/^(,=<>&":
            terms.append(sign + cur.strip())
            cur, sign = "", ch
            i += 1
            continue
        cur += ch
        i += 1
    if cur.strip():
        terms.append(sign + cur.strip())
    return terms


def term_leaf_cells(term: str, default_sheet: str) -> Optional[set[tuple[str, int, int]]]:
    """Cells a purely additive term contributes: a cell, a range, or SUM(...) of ranges. None if not additive."""
    t = term.lstrip("+-").strip()
    if t.startswith("(") and t.endswith(")"):
        t = t[1:-1]
    funcs = functions_in("=" + t)
    if funcs and funcs != ["SUM"]:
        return None
    if re.search(r"[*/^]", t):
        return None
    refs = parse_refs("=" + t, default_sheet)
    if not refs:
        return None
    out: set[tuple[str, int, int]] = set()
    for r in refs:
        if r.size() > 2000:
            return None
        for (rr, cc) in r.cells():
            out.add((r.sheet, rr, cc))
    return out


def label_text(v) -> str:
    return re.sub(r"\s+", " ", str(v)).strip()[:60]


def has_total_word(s: str) -> bool:
    s = s.lower()
    return any(w in s for w in TOTAL_WORDS)


@dataclass
class CellContext:
    wb: Workbook
    sheet: Sheet
    cell: Cell
    refs: list[Ref]
    r1c1: str
    funcs: list[str]
    row_path: list[str]
    col_path: list[str]

    @property
    def in_scope(self) -> bool:
        """True when the formula's functions are all in scope (or it has none, i.e. plain arithmetic)."""
        return all(f in IN_SCOPE_FUNCS for f in self.funcs)


def _text_at(sh: Sheet, r: int, c: int) -> Optional[str]:
    cell = sh.get(r, c)
    if cell.is_text:
        return label_text(cell.value)
    return None


def _left_labels(sh: Sheet, row: int, col: int, max_labels: int = 2) -> tuple[list[str], list[int]]:
    """Text cells to the left of the target in its row, nearest first, with their columns."""
    labels: list[str] = []
    columns: list[int] = []
    for c in range(col - 1, 0, -1):
        text = _text_at(sh, row, c)
        if text:
            labels.append(text)
            columns.append(c)
            if len(labels) >= max_labels:
                break
    return labels, columns


def _is_section_header(sh: Sheet, row: int, col: int) -> bool:
    """A bold text cell, or a text cell whose row holds no numbers or formulas to its right."""
    cell = sh.get(row, col)
    if cell.bold:
        return True
    right_edge = min(sh.max_col, col + 12) + 1
    return not any(sh.get(row, c).is_number or sh.get(row, c).is_formula for c in range(col + 1, right_edge))


def _section_headers_above(sh: Sheet, row: int, anchor_col: int, exclude: list[str], limit: int) -> list[str]:
    """Walk up the label column(s) collecting section headers, nearest first."""
    found: list[str] = []
    columns = [c for c in (anchor_col, anchor_col - 1, anchor_col + 1) if c >= 1]
    for r in range(row - 1, 0, -1):
        if len(found) >= limit:
            break
        for c in columns:
            text = _text_at(sh, r, c)
            if text and text not in exclude and text not in found and _is_section_header(sh, r, c):
                found.append(text)
                break
    return found


def row_header_path(sh: Sheet, row: int, col: int, max_levels: int = 3) -> list[str]:
    """Nearest label(s) to the left, then the section headers above them."""
    labels, columns = _left_labels(sh, row, col)
    anchor_col = min(columns) if columns else 1
    remaining = max_levels + 1 - len(labels)
    headers = _section_headers_above(sh, row, anchor_col, labels, remaining) if remaining > 0 else []
    return (labels + headers)[: max_levels + 1]


def col_header_path(sh: Sheet, row: int, col: int, max_levels: int = 3) -> list[str]:
    path: list[str] = []
    for r in range(row - 1, 0, -1):
        t = _text_at(sh, r, col)
        if t and t not in path:
            path.append(t)
            if len(path) >= max_levels:
                break
    return path


def build_context(wb: Workbook, sheet_name: str, addr: str, max_header_levels: int = 3) -> Optional[CellContext]:
    sh = wb.sheet(sheet_name)
    if sh is None:
        return None
    m = re.match(r"^\$?([A-Za-z]{1,3})\$?(\d+)$", addr)
    if not m:
        return None
    col = column_index_from_string(m.group(1).upper())
    row = int(m.group(2))
    cell = sh.get(row, col)
    if not cell.is_formula:
        return None
    refs = parse_refs(cell.formula, sh.name)
    return CellContext(
        wb=wb, sheet=sh, cell=cell, refs=refs,
        r1c1=to_r1c1(cell.formula, row, col),
        funcs=functions_in(cell.formula),
        row_path=row_header_path(sh, row, col, max_header_levels),
        col_path=col_header_path(sh, row, col, max_header_levels),
    )
