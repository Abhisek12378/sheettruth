"""Verify agent and structure checks on tiny synthetic workbooks."""
import sys
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from test_mutators import make_wb  # noqa: E402
from sheettruth.shape import shape_findings  # noqa: E402
from sheettruth.verify import Finding, Verifier  # noqa: E402


def amount_table(extra=None):
    rows = {"A1": "Item", "B1": "Qty", "C1": "Price", "D1": "Amount"}
    for r in range(2, 13):
        rows.update({f"A{r}": f"item {r}", f"B{r}": r, f"C{r}": 10, f"D{r}": f"=B{r}*C{r}"})
    rows.update(extra or {})
    return rows


def test_shape_finds_typed_over_value_and_odd_formula(tmp_path):
    wb = make_wb(tmp_path, amount_table({"D5": 50, "D10": "=B9*C10"}), "shape.xlsx")
    found = {(f.addr, f.kind, f.implied_formula) for f in shape_findings(wb)}
    assert ("D5", "hardcoded_value", "=B5*C5") in found
    assert ("D10", "odd_one_out", "=B10*C10") in found


def test_shape_quiet_on_clean_run(tmp_path):
    wb = make_wb(tmp_path, amount_table(), "clean.xlsx")
    assert shape_findings(wb) == []


def test_peer_pattern_supports_fix_that_matches_neighbours(tmp_path):
    wb = make_wb(tmp_path, amount_table({"D7": "=B6*C7"}), "peer.xlsx")
    result = Verifier(None).verify(wb, str(tmp_path / "peer.xlsx"), Finding("Sheet1", "D7", "=B6*C7", "=B7*C7", "wrong_reference"))
    assert result.outcome == "passed"
    assert any(c.name == "peer_pattern" and c.result == "supports" for c in result.checks)


def test_peer_pattern_contradicts_fix_that_breaks_the_run(tmp_path):
    wb = make_wb(tmp_path, amount_table(), "peer2.xlsx")
    result = Verifier(None).verify(wb, str(tmp_path / "peer2.xlsx"), Finding("Sheet1", "D4", "=B4*C4", "=B4/C4", "wrong_operator"))
    assert result.outcome == "failed"


def test_range_delta_supports_adding_real_rows(tmp_path):
    rows = amount_table({"A14": "Total", "D14": "=SUM(D2:D10)"})
    wb = make_wb(tmp_path, rows, "range.xlsx")
    result = Verifier(None).verify(wb, str(tmp_path / "range.xlsx"), Finding("Sheet1", "D14", "=SUM(D2:D10)", "=SUM(D2:D12)", "skipped_rows"))
    assert result.outcome == "passed"


def test_range_delta_contradicts_adding_blank_rows(tmp_path):
    rows = amount_table({"A14": "Total", "D14": "=SUM(D2:D12)"})
    wb = make_wb(tmp_path, rows, "blank.xlsx")
    result = Verifier(None).verify(wb, str(tmp_path / "blank.xlsx"), Finding("Sheet1", "D14", "=SUM(D2:D12)", "=SUM(D2:D13)", "skipped_rows"))
    assert result.outcome == "failed"


def test_no_check_when_nothing_applies(tmp_path):
    rows = {"A1": "x", "B1": 1, "A2": "y", "B2": 2, "A3": "z", "B3": "=B1+B2"}
    wb = make_wb(tmp_path, rows, "none.xlsx")
    result = Verifier(None).verify(wb, str(tmp_path / "none.xlsx"), Finding("Sheet1", "B3", "=B1+B2", "=B1-B2", "wrong_sign"))
    assert result.outcome == "no_independent_check"


def test_sibling_sheets_contradict_a_fix_that_breaks_the_template(tmp_path):
    import openpyxl
    from sheettruth.windows.cellinfo import Workbook
    wb = openpyxl.Workbook()
    for i, name in enumerate(["Unit A", "Unit B", "Unit C", "Unit D"]):
        ws = wb.active if i == 0 else wb.create_sheet()
        ws.title = name
        ws["A1"], ws["B1"], ws["A2"], ws["B2"], ws["A3"], ws["B3"] = "Revenue", 100 + i, "Costs", 60, "Margin", "=B1-B2"
    path = tmp_path / "units.xlsx"
    wb.save(path)
    result = Verifier(None).verify(Workbook(str(path)), str(path), Finding("Unit A", "B3", "=B1-B2", "=B2-B1", "wrong_sign"))
    assert result.outcome == "failed"
    assert any(c.name == "sibling_sheets" and c.result == "contradicts" for c in result.checks)
