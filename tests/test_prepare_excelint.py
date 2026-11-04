"""Tests for the ExceLint benchmark preparation: file naming, sheet matching, run grouping."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import prepare_excelint_benchmark as pe  # noqa: E402


def test_safe_name_decodes_and_strips_odd_characters():
    assert pe.safe_name("04%20En%20R&D-CRB-SOR#A8312.xlsx") == "04 En R_D-CRB-SOR_A8312.xlsx"
    assert pe.safe_name("01sumdat.xlsx") == "01sumdat.xlsx"


def test_match_sheet_ignores_spacing_and_case_and_accepts_prefixes():
    names = ["General PTSA Budget", "Summary", "FY 2002 detail"]
    assert pe.match_sheet("General PTSA  Budget", names) == "General PTSA Budget"
    assert pe.match_sheet("summary", names) == "Summary"
    assert pe.match_sheet("FY 2002", names) == "FY 2002 detail"
    assert pe.match_sheet("Missing", names) is None


def test_group_formula_cells_joins_adjacent_cells_with_the_same_relative_formula():
    cells = [(7, 12, "=AVERAGE(B7:J7)"), (12, 12, "=AVERAGE(B12:J12)"), (13, 12, "=AVERAGE(B13:J13)"),
             (20, 12, "=SUM(B20:J20)")]
    runs = sorted(pe.group_formula_cells(cells))
    assert runs == [[(7, 12)], [(12, 12), (13, 12)], [(20, 12)]]
