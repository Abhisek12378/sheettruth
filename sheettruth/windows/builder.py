"""Render the context window for one formula cell as tagged, pipe-separated records.

The same builder produces training examples and inference prompts, so the model never sees a
layout it was not trained on. The design and the reason for each section are documented in
docs/window_design.md.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Callable, Optional

import tiktoken
from openpyxl.utils import get_column_letter

from sheettruth.windows.cellinfo import (
    Cell,
    CellContext,
    Ref,
    Sheet,
    Workbook,
    additive_terms,
    has_total_word,
    label_text,
    term_leaf_cells,
    to_r1c1,
)

UNIT_PATTERN = re.compile(
    r"(\$|%|thousand|million|billion|\b000s?\b|\(000\)|MW|MMBtu|USD|EUR|GBP|INR|lakh|crore|\bin \w+)",
    re.IGNORECASE,
)
STRUCTURAL_NOTES = ("sums_cells_inside_range", "total_word", "formula_among_values", "hardcoded_among_formulas", "hidden")
DROP_ORDER_WHEN_OVER_BUDGET = ("ASSUMPTION", "PEER_DIFF", "COL|", "ROW|", "IN_RANGE_NOTE", "GRID")
CHARS_PER_TOKEN_ESTIMATE = 3.5

_encoder = None


@dataclass
class WindowConfig:
    """Knobs for the window layout. Defaults match configs/default.yaml."""

    grid_radius: int = 2
    col_above: int = 10
    col_below: int = 3
    row_left: int = 3
    row_right: int = 3
    row_right_extended: int = 5
    range_head: int = 3
    range_tail: int = 5
    boundary_scan: int = 5
    max_assumptions: int = 10
    max_tokens: int = 1500
    max_range_notes: int = 8


@dataclass
class Window:
    text: str
    tokens: int
    truncated: bool
    unsupported_reason: Optional[str]


# ----------------------------------------------------------------------------------------------
# formatting helpers
# ----------------------------------------------------------------------------------------------

def count_tokens(text: str) -> int:
    """Token count with the cl100k tokenizer when available, else a character-based estimate."""
    global _encoder
    if _encoder is None:
        try:
            _encoder = tiktoken.get_encoding("cl100k_base")
        except Exception:
            _encoder = False
    if _encoder:
        return len(_encoder.encode(text))
    return int(len(text) / CHARS_PER_TOKEN_ESTIMATE) + 1


def esc(text: str) -> str:
    """Make a string safe inside a pipe-separated record."""
    return text.replace("|", "/").replace("\n", " ")


def fmt_val(cell: Cell) -> str:
    if cell.is_blank:
        return "(blank)"
    if cell.is_error:
        return cell.value
    if cell.is_formula and cell.value is None:
        return "(nocache)"
    value = cell.value
    if isinstance(value, bool):
        return str(value)
    if isinstance(value, (int, float)):
        if float(value).is_integer() and abs(value) < 1e15:
            return str(int(value))
        return f"{value:.6g}"
    if isinstance(value, str):
        return '"' + esc(label_text(value)) + '"'
    return str(value)[:40]


def fmt_formula(cell: Cell) -> str:
    return esc(cell.formula or "")[:160]


def row_label(sheet: Sheet, row: int, col: int) -> str:
    """Nearest text to the left in the same row."""
    for c in range(col - 1, 0, -1):
        cell = sheet.get(row, c)
        if cell.is_text:
            return label_text(cell.value)
    return ""


def col_header(sheet: Sheet, row: int, col: int) -> str:
    """Nearest text above in the same column."""
    for r in range(row - 1, 0, -1):
        cell = sheet.get(r, col)
        if cell.is_text:
            return label_text(cell.value)
    return ""


def cell_record(tag: str, sheet: Sheet, cell: Cell, label: str = "") -> str:
    formula = fmt_formula(cell) if cell.is_formula else ""
    return f"{tag}|{sheet.name}!{cell.addr}|{esc(label)}|{formula}|{fmt_val(cell)}"


# ----------------------------------------------------------------------------------------------
# sections
# ----------------------------------------------------------------------------------------------

def sheet_title_and_unit_notes(sheet: Sheet, max_notes: int = 3) -> tuple[str, list[str]]:
    """Title text from the first row, plus up to a few unit or scale notes near the top."""
    title = ""
    for c in range(1, min(sheet.max_col, 8) + 1):
        cell = sheet.get(1, c)
        if cell.is_text:
            title = label_text(cell.value)
            break
    notes: list[str] = []
    for r in range(1, min(sheet.max_row, 8) + 1):
        for c in range(1, min(sheet.max_col, 12) + 1):
            cell = sheet.get(r, c)
            if not cell.is_text or not UNIT_PATTERN.search(cell.value):
                continue
            text = label_text(cell.value)
            if text != title:
                notes.append(f"{cell.addr}={text}")
            if len(notes) >= max_notes:
                return title, notes
    return title, notes


def header_lines(ctx: CellContext) -> list[str]:
    sheet, cell = ctx.sheet, ctx.cell
    title, notes = sheet_title_and_unit_notes(sheet)
    lines = [
        f"TARGET|{sheet.name}!{cell.addr}|{fmt_formula(cell)}|value={fmt_val(cell)}|fmt={cell.number_format}|bold={int(cell.bold)}",
        f"TARGET_R1C1|{esc(ctx.r1c1)}",
    ]
    if cell.comment:
        lines.append(f"TARGET_COMMENT|{esc(label_text(cell.comment))}")
    lines.append("ROW_PATH|" + (" > ".join(esc(p) for p in ctx.row_path) or "(none)"))
    lines.append("COL_PATH|" + (" > ".join(esc(p) for p in ctx.col_path) or "(none)"))
    lines.append(f"SHEET|{sheet.name}|title={esc(title) or '(none)'}|sheets_in_workbook={len(ctx.wb.sheetnames)}")
    lines.extend(f"UNIT_NOTE|{esc(n)}" for n in notes)
    return lines


def grid_lines(sheet: Sheet, row: int, col: int, radius: int) -> list[str]:
    """A small 2D grid around the target with explicit column letters and row numbers."""
    cols = [c for c in range(col - radius, col + radius + 1) if c >= 1]
    lines = ["GRID|row\\col|" + "|".join(get_column_letter(c) for c in cols)]
    for r in range(row - radius, row + radius + 1):
        if r < 1:
            continue
        cells = []
        for c in cols:
            cell = sheet.get(r, c)
            cells.append(f"{fmt_formula(cell)} -> {fmt_val(cell)}" if cell.is_formula else fmt_val(cell))
        marker = "*" if r == row else ""
        lines.append(f"GRID|{marker}{r}|" + "|".join(cells))
    return lines


def blank_run_line(sheet_name: str, letter: str, blank_run: list[int]) -> list[str]:
    """One collapsed line for a run of blank cells in a column, or nothing for an empty run."""
    if len(blank_run) == 1:
        return [f"COL|{sheet_name}!{letter}{blank_run[0]}|||(blank)"]
    if blank_run:
        return [f"COL|{sheet_name}!{letter}{blank_run[0]}:{letter}{blank_run[-1]}|||({len(blank_run)} blank cells)"]
    return []


def column_context_lines(sheet: Sheet, row: int, col: int, above: int, below: int, skip_rows: set[int]) -> list[str]:
    """Cells above and below the target in its column, with blank runs collapsed."""
    lines: list[str] = []
    blank_run: list[int] = []
    letter = get_column_letter(col)
    rows = list(range(max(1, row - above), row)) + list(range(row + 1, row + below + 1))
    for r in rows:
        if r in skip_rows:
            continue
        cell = sheet.get(r, col)
        if cell.is_blank:
            blank_run.append(r)
            continue
        lines += blank_run_line(sheet.name, letter, blank_run)
        blank_run = []
        lines.append(cell_record("COL", sheet, cell, row_label(sheet, r, col)))
    lines += blank_run_line(sheet.name, letter, blank_run)
    return lines


def row_context_lines(sheet: Sheet, row: int, col: int, left: int, right: int, skip_cols: set[int]) -> list[str]:
    """Non-blank cells left and right of the target in its row."""
    cols = list(range(max(1, col - left), col)) + list(range(col + 1, col + right + 1))
    lines = []
    for c in cols:
        cell = sheet.get(row, c)
        if c in skip_cols or cell.is_blank:
            continue
        lines.append(cell_record("ROW", sheet, cell, col_header(sheet, row, c)))
    return lines


def axis_peer_lines(sheet: Sheet, axis: str, positions: list[tuple[int, int]], r1c1: str, max_diff: int) -> list[str]:
    """Peer summary for one axis: how many formula cells share the target's R1C1, and the ones that differ."""
    peers = [sheet.get(r, c) for (r, c) in positions]
    peers = [p for p in peers if p.is_formula]
    if not peers:
        return [f"PEERS_{axis}|none"]
    same = [p for p in peers if to_r1c1(p.formula, p.row, p.col) == r1c1]
    lines = [f"PEERS_{axis}|formula_cells={len(peers)}|same_r1c1={len(same)}"]
    for p in [p for p in peers if p not in same][:max_diff]:
        lines.append(f"PEER_DIFF|{sheet.name}!{p.addr}|{esc(to_r1c1(p.formula, p.row, p.col))}|{fmt_formula(p)}|{fmt_val(p)}")
    return lines


def peer_lines(sheet: Sheet, target: Cell, r1c1: str, max_diff: int = 3) -> list[str]:
    """Formula cells in the same row and column: how many share the target's R1C1, and the ones that differ."""
    row_positions = [(target.row, c) for c in range(max(1, target.col - 8), target.col + 9) if c != target.col]
    col_positions = [(r, target.col) for r in range(max(1, target.row - 15), target.row + 16) if r != target.row]
    return (axis_peer_lines(sheet, "ROW", row_positions, r1c1, max_diff)
            + axis_peer_lines(sheet, "COL", col_positions, r1c1, max_diff))


def sign_summary(cells: list[Cell]) -> str:
    numbers = [c.value for c in cells if c.is_number]
    blanks = sum(1 for c in cells if c.is_blank)
    if not numbers:
        return f"no_numbers|blanks={blanks}"
    positives = sum(1 for v in numbers if v > 0)
    negatives = sum(1 for v in numbers if v < 0)
    if negatives == 0:
        kind = "all_positive"
    elif positives == 0:
        kind = "all_negative"
    else:
        kind = f"mixed(pos={positives},neg={negatives})"
    return f"{kind}|min={min(numbers):.6g}|max={max(numbers):.6g}|numbers={len(numbers)}|blanks={blanks}"


@dataclass
class LinearRange:
    """A one-dimensional range (a column segment or a row segment) and accessors along it."""

    sheet: Sheet
    ref: Ref
    along_rows: bool

    @property
    def indexes(self) -> list[int]:
        if self.along_rows:
            return list(range(self.ref.r1, self.ref.r2 + 1))
        return list(range(self.ref.c1, self.ref.c2 + 1))

    def cell(self, i: int) -> Cell:
        return self.sheet.get(i, self.ref.c1) if self.along_rows else self.sheet.get(self.ref.r1, i)

    def label(self, i: int) -> str:
        if self.along_rows:
            return row_label(self.sheet, i, self.ref.c1)
        return col_header(self.sheet, self.ref.r1, i)

    def is_hidden(self, i: int) -> bool:
        return self.along_rows and i in self.sheet.hidden_rows


def cell_kind_tags(rng: LinearRange, cell: Cell, inside: set[tuple[int, int]], mostly_formulas: bool) -> list[str]:
    """Tags about what kind of cell sits inside the range: a subtotal of the range, a formula among
    values, or a typed number among formulas."""
    if cell.is_formula:
        leaves = term_leaf_cells(cell.formula, rng.sheet.name)
        if leaves and any(s == rng.sheet.name and (r, c) in inside for (s, r, c) in leaves):
            return ["sums_cells_inside_range"]
        return [] if mostly_formulas else ["formula_among_values"]
    if cell.is_number and mostly_formulas:
        return ["hardcoded_among_formulas"]
    return []


def range_anomaly_tags(rng: LinearRange, i: int, inside: set[tuple[int, int]], mostly_formulas: bool) -> list[str]:
    """Why a cell inside a range deserves attention. Empty when it is an ordinary data cell."""
    cell = rng.cell(i)
    tags = cell_kind_tags(rng, cell, inside, mostly_formulas)
    flags = (("total_word", has_total_word(rng.label(i))), ("bold", cell.bold), ("blank", cell.is_blank),
             ("hidden", rng.is_hidden(i)), ("negative", cell.is_number and cell.value < 0))
    tags.extend(name for name, on in flags if on)
    return tags


def linear_range_lines(rng: LinearRange, cfg: WindowConfig) -> list[str]:
    """Head, tail, anomalies and an omitted-count line for a one-dimensional range."""
    idxs = rng.indexes
    inside = set(rng.ref.cells())
    n_formula = sum(1 for i in idxs if rng.cell(i).is_formula)
    mostly_formulas = n_formula * 2 > len(idxs)

    head = idxs[: cfg.range_head]
    tail = idxs[-cfg.range_tail:] if len(idxs) > cfg.range_head + cfg.range_tail else idxs[cfg.range_head:]
    shown = set(head) | set(tail)

    notes = []
    for i in idxs:
        if i in shown:
            continue
        tags = range_anomaly_tags(rng, i, inside, mostly_formulas)
        if tags:
            notes.append((0 if any(t in STRUCTURAL_NOTES for t in tags) else 1, i, tags))
    notes.sort()
    notes = notes[: cfg.max_range_notes]

    lines = [cell_record("IN_RANGE", rng.sheet, rng.cell(i), rng.label(i)) for i in head]
    for _, i, tags in notes:
        cell = rng.cell(i)
        formula = fmt_formula(cell) if cell.is_formula else ""
        lines.append(f"IN_RANGE_NOTE|{rng.sheet.name}!{cell.addr}|{esc(rng.label(i))}|{formula}|{fmt_val(cell)}|{','.join(tags)}")
    omitted = len(idxs) - len(shown) - len(notes)
    if omitted > 0:
        lines.append(f"IN_RANGE_OMITTED|{omitted} ordinary cells not shown")
    lines.extend(cell_record("IN_RANGE", rng.sheet, rng.cell(i), rng.label(i)) for i in tail)
    return lines


def boundary_lines(rng: LinearRange, cfg: WindowConfig, target: Cell, target_sheet: str) -> list[str]:
    """Cells just before the start and just after the end of a range."""
    idxs = rng.indexes
    before = [i for i in range(idxs[0] - cfg.boundary_scan, idxs[0]) if i >= 1]
    after = list(range(idxs[-1] + 1, idxs[-1] + cfg.boundary_scan + 1))
    lines = []
    for tag, positions in (("BEFORE_RANGE", before), ("AFTER_RANGE", after)):
        for i in positions:
            cell = rng.cell(i)
            if cell.addr == target.addr and rng.sheet.name == target_sheet:
                lines.append(f"{tag}|{rng.sheet.name}!{cell.addr}|(target cell)")
            else:
                lines.append(cell_record(tag, rng.sheet, cell, rng.label(i)))
    return lines


def single_ref_line(sheet: Sheet, ref: Ref) -> str:
    cell = sheet.get(ref.r1, ref.c1)
    formula = fmt_formula(cell) if cell.is_formula else ""
    return (f"REF_CELL|{sheet.name}!{cell.addr}|{esc(row_label(sheet, ref.r1, ref.c1))}|"
            f"{esc(col_header(sheet, ref.r1, ref.c1))}|{formula}|{fmt_val(cell)}|fmt={cell.number_format}")


def two_d_range_lines(sheet: Sheet, ref: Ref) -> list[str]:
    corners = ((ref.r1, ref.c1), (ref.r1, ref.c2), (ref.r2, ref.c1), (ref.r2, ref.c2))
    lines = [f"REF_RANGE_2D|rows={ref.r2 - ref.r1 + 1}|cols={ref.c2 - ref.c1 + 1}"]
    lines.extend(cell_record("IN_RANGE", sheet, sheet.get(r, c), row_label(sheet, r, c)) for (r, c) in corners)
    return lines


def collapsed_range_lines(sheet: Sheet, ref: Ref, cfg: WindowConfig, target: Cell, target_sheet: str) -> list[str]:
    """A one-cell range written as F25:F25. Its direction is unknown, so both the cells above and
    below and the cells left and right are shown, the way a real range's boundaries would be."""
    cell = sheet.get(ref.r1, ref.c1)
    lines = [f"REF_RANGE|{sheet.name}!{esc(ref.text)}|cells=1|written_as_range|{sign_summary([cell])}",
             cell_record("IN_RANGE", sheet, cell, row_label(sheet, ref.r1, ref.c1))]
    for along_rows in (True, False):
        lines.extend(boundary_lines(LinearRange(sheet, ref, along_rows), cfg, target, target_sheet))
    return lines


def reference_lines(wb: Workbook, ref: Ref, cfg: WindowConfig, target: Cell, target_sheet: str) -> list[str]:
    """Everything the window says about one reference in the target formula."""
    sheet = wb.sheet(ref.sheet)
    if sheet is None:
        return [f"REF|{esc(ref.text)}|unresolved_sheet"]
    if ref.written_as_range:
        return collapsed_range_lines(sheet, ref, cfg, target, target_sheet)
    if not ref.is_range:
        return [single_ref_line(sheet, ref)]
    cells = [sheet.get(r, c) for (r, c) in ref.cells()]
    lines = [f"REF_RANGE|{sheet.name}!{ref.a1()}|cells={ref.size()}|{sign_summary(cells)}"]
    if ref.is_vertical or ref.is_horizontal:
        rng = LinearRange(sheet, ref, along_rows=ref.is_vertical)
        lines.extend(linear_range_lines(rng, cfg))
        lines.extend(boundary_lines(rng, cfg, target, target_sheet))
    else:
        lines.extend(two_d_range_lines(sheet, ref))
    return lines


def overlap_lines(ctx: CellContext, max_cells: int = 6) -> list[str]:
    """Leaf cells that more than one additive term of the formula counts."""
    terms = additive_terms(ctx.cell.formula)
    if len(terms) < 2:
        return []
    contributors: dict[tuple[str, int, int], list[str]] = {}
    for term in terms:
        for key in term_leaf_cells(term, ctx.sheet.name) or ():
            contributors.setdefault(key, []).append(term)
    duplicated = sorted((k, v) for k, v in contributors.items() if len(v) >= 2)
    if not duplicated:
        return ["OVERLAP|none"]
    lines = [f"OVERLAP|leaf_cells_counted_twice={len(duplicated)}"]
    for (sheet_name, r, c), via in duplicated[:max_cells]:
        lines.append(f"OVERLAP_CELL|{sheet_name}!{get_column_letter(c)}{r}|via={' & '.join(esc(t) for t in via)}")
    return lines


def _reference_count(candidate: tuple) -> int:
    return candidate[0]


def assumption_lines(wb: Workbook, sheet: Sheet, cfg: WindowConfig, exclude: set[tuple[int, int]]) -> list[str]:
    """Labelled constants on the sheet that two or more formulas reference absolutely."""
    counts = wb.reference_counts().get(sheet.name, {})
    candidates = []
    for (r, c), n in counts.items():
        cell = sheet.get(r, c)
        if n < 2 or (r, c) in exclude or not cell.is_number or cell.is_formula:
            continue
        label = row_label(sheet, r, c) or col_header(sheet, r, c)
        if label:
            candidates.append((n, cell, label))
    candidates.sort(key=_reference_count, reverse=True)
    return [f"ASSUMPTION|{sheet.name}!{cell.addr}|{esc(label)}|{fmt_val(cell)}|used_by={n}|fmt={cell.number_format}"
            for n, cell, label in candidates[: cfg.max_assumptions]]


# ----------------------------------------------------------------------------------------------
# assembly
# ----------------------------------------------------------------------------------------------

def context_lines(ctx: CellContext, cfg: WindowConfig) -> list[str]:
    sheet, cell = ctx.sheet, ctx.cell
    grid_rows = set(range(cell.row - cfg.grid_radius, cell.row + cfg.grid_radius + 1))
    grid_cols = set(range(cell.col - cfg.grid_radius, cell.col + cfg.grid_radius + 1))
    references_own_row = any(r.sheet == sheet.name and r.r1 == cell.row == r.r2 for r in ctx.refs)
    right = cfg.row_right_extended if references_own_row else cfg.row_right
    lines = grid_lines(sheet, cell.row, cell.col, cfg.grid_radius)
    lines += column_context_lines(sheet, cell.row, cell.col, cfg.col_above, cfg.col_below, grid_rows)
    lines += row_context_lines(sheet, cell.row, cell.col, cfg.row_left, right, grid_cols)
    lines += peer_lines(sheet, cell, ctx.r1c1)
    return lines


def all_reference_lines(ctx: CellContext, cfg: WindowConfig) -> list[str]:
    lines: list[str] = []
    seen: set[tuple] = set()
    for ref in ctx.refs:
        key = (ref.sheet, ref.r1, ref.c1, ref.r2, ref.c2)
        if key in seen:
            continue
        seen.add(key)
        lines += reference_lines(ctx.wb, ref, cfg, ctx.cell, ctx.sheet.name)
    if not ctx.refs:
        lines.append("REF|none_parsed")
    lines += overlap_lines(ctx)
    referenced = set()
    if sum(r.size() for r in ctx.refs) < 5000:
        referenced = {(r, c) for ref in ctx.refs if ref.sheet == ctx.sheet.name for (r, c) in ref.cells()}
    lines += assumption_lines(ctx.wb, ctx.sheet, cfg, referenced)
    return lines


def fit_to_budget(lines: list[str], max_tokens: int) -> Window:
    """Drop the least important sections, in a fixed order, until the window fits."""
    text = "\n".join(lines)
    tokens = count_tokens(text)
    if tokens <= max_tokens:
        return Window(text, tokens, False, None)
    for tag in DROP_ORDER_WHEN_OVER_BUDGET:
        lines = [line for line in lines if not line.startswith(tag)]
        text = "\n".join(lines)
        tokens = count_tokens(text)
        if tokens <= max_tokens:
            return Window(text, tokens, True, None)
    return Window(text, tokens, True, "truncated_evidence")


def build_window(ctx: CellContext, cfg: WindowConfig = WindowConfig()) -> Window:
    """Build the full context window for one formula cell."""
    lines = header_lines(ctx) + context_lines(ctx, cfg) + all_reference_lines(ctx, cfg)
    return fit_to_budget(lines, cfg.max_tokens)
