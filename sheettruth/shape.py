"""Structure checks that need no model.

  hardcoded_value   a plain number sitting inside a run of formulas that share one R1C1 shape,
                    the way a typed-over formula looks
  odd_one_out       a formula whose R1C1 shape differs from the shared shape of the formulas on
                    both sides of it in the same row or column

Both come with the formula the run implies for that cell, translated from a neighbour.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from openpyxl.formula.translate import Translator

from sheettruth.windows.cellinfo import Cell, Sheet, Workbook, to_r1c1

MIN_RUN_EACH_SIDE = 2


@dataclass
class ShapeFinding:
    sheet: str
    addr: str
    kind: str
    current: str
    implied_formula: str
    detail: str

    def to_dict(self) -> dict:
        return self.__dict__


def _shape(cell: Cell) -> Optional[str]:
    return to_r1c1(cell.formula, cell.row, cell.col) if cell.is_formula else None


def _run_shape(cells: list[Cell]) -> Optional[str]:
    """The single R1C1 shape shared by all cells, or None."""
    shapes = {_shape(c) for c in cells}
    return shapes.pop() if len(shapes) == 1 and None not in shapes else None


def _line_findings(sheet: Sheet, line: list[Cell]) -> list[ShapeFinding]:
    """Findings along one row or one column of cells."""
    out = []
    for i in range(MIN_RUN_EACH_SIDE, len(line) - MIN_RUN_EACH_SIDE):
        before = line[i - MIN_RUN_EACH_SIDE:i]
        after = line[i + 1:i + 1 + MIN_RUN_EACH_SIDE]
        shape = _run_shape(before + after)
        if shape is None:
            continue
        cell = line[i]
        if _shape(cell) == shape:
            continue
        implied = Translator(before[-1].formula, origin=before[-1].addr).translate_formula(cell.addr)
        if cell.is_number:
            out.append(ShapeFinding(sheet.name, cell.addr, "hardcoded_value", str(cell.value), implied,
                                    f"a typed number between formulas that all read {shape}"))
        elif cell.is_formula:
            out.append(ShapeFinding(sheet.name, cell.addr, "odd_one_out", cell.formula, implied,
                                    f"formula shape differs from the {len(before) + len(after)} formulas around it ({shape})"))
    return out


def shape_findings(wb: Workbook) -> list[ShapeFinding]:
    """Structure findings for every sheet, each cell reported once."""
    out: list[ShapeFinding] = []
    for sheet in wb.sheets.values():
        seen: set[str] = set()
        columns = {c for (r, c) in sheet.cells}
        rows = {r for (r, c) in sheet.cells}
        lines = [[sheet.get(r, c) for r in range(1, sheet.max_row + 1)] for c in sorted(columns)]
        lines += [[sheet.get(r, c) for c in range(1, sheet.max_col + 1)] for r in sorted(rows)]
        for line in lines:
            for f in _line_findings(sheet, line):
                if f.addr not in seen:
                    seen.add(f.addr)
                    out.append(f)
    return out
