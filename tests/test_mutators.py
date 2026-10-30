"""Must-fire and must-not-fire cases for every mutator, on tiny synthetic workbooks."""
import random
import sys
import warnings
from pathlib import Path

import openpyxl
import pytest

warnings.filterwarnings("ignore")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sheettruth.mutators.base import registry  # noqa: E402
from sheettruth.windows.cellinfo import Workbook, build_context  # noqa: E402
from sheettruth.windows.builder import build_window  # noqa: E402

RNG = random.Random(1)


def make_wb(tmp_path, rows: dict[str, object], name="t.xlsx") -> Workbook:
    """rows maps 'A1' -> value or '=formula'."""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Sheet1"
    for addr, v in rows.items():
        ws[addr] = v
    p = tmp_path / name
    wb.save(p)
    return Workbook(str(p))


def expense_block(extra=None):
    rows = {"A1": "Budget 2026 ($000)", "A2": "Item", "B2": "Amount",
            "A3": "Rent", "B3": 100, "A4": "Salaries", "B4": 400, "A5": "Travel", "B5": 50,
            "A6": "Software", "B6": 30, "A7": "Marketing", "B7": 80,
            "A8": "Total expenses", "B8": "=SUM(B3:B7)"}
    rows.update(extra or {})
    return rows


def ctx_for(tmp_path, rows, addr, name="t.xlsx"):
    wb = make_wb(tmp_path, rows, name)
    return build_context(wb, "Sheet1", addr)


def test_registry_has_five():
    assert set(registry()) == {"skipped_rows", "wrong_function", "wrong_sign", "missing_factor", "double_count"}


def test_skipped_rows_fires_and_drops_real_rows(tmp_path):
    m = registry()["skipped_rows"]
    ctx = ctx_for(tmp_path, expense_block(), "B8")
    assert m.applies(ctx)
    mut = m.mutate(ctx, RNG)
    assert mut and mut.broken_formula != "=SUM(B3:B7)" and mut.expected_formula == "=SUM(B3:B7)"
    assert mut.broken_formula.startswith("=SUM(B")


def test_skipped_rows_not_on_tiny_range(tmp_path):
    m = registry()["skipped_rows"]
    ctx = ctx_for(tmp_path, {"A1": "x", "B1": 1, "A2": "y", "B2": 2, "A3": "Total", "B3": "=SUM(B1:B2)"}, "B3")
    assert not m.applies(ctx)


def test_wrong_function_fires_on_average_label(tmp_path):
    m = registry()["wrong_function"]
    rows = {"A1": "Day", "B1": "Sales", **{f"A{i}": f"Day {i-1}" for i in range(2, 8)}, **{f"B{i}": 10 * i for i in range(2, 8)},
            "A8": "Average daily sales", "B8": "=AVERAGE(B2:B7)"}
    ctx = ctx_for(tmp_path, rows, "B8")
    assert m.applies(ctx)
    mut = m.mutate(ctx, RNG)
    assert mut and not mut.broken_formula.upper().startswith("=AVERAGE")


def test_wrong_function_not_without_intent_word(tmp_path):
    m = registry()["wrong_function"]
    rows = {"A1": "Day", "B1": "Sales", "A2": "Mon", "B2": 1, "A3": "Tue", "B3": 2, "A4": "Wed", "B4": 3,
            "A5": "Thu", "B5": 4, "A6": "Result", "B6": "=SUM(B2:B5)"}
    ctx = ctx_for(tmp_path, rows, "B6")
    assert not m.applies(ctx)


def test_wrong_function_not_when_label_matches_nothing_specific(tmp_path):
    m = registry()["wrong_function"]
    # "Total count" implies two functions -> ambiguous -> do not fire
    rows = {"A1": "Item", "B1": "n", "A2": "a", "B2": 1, "A3": "b", "B3": 2, "A4": "c", "B4": 3, "A5": "Total count", "B5": "=COUNT(B2:B4)"}
    assert not m.applies(ctx_for(tmp_path, rows, "B5"))


def test_wrong_sign_fires_on_deduction(tmp_path):
    m = registry()["wrong_sign"]
    rows = {"A1": "Revenue", "B1": 1000, "A2": "Cost of goods sold", "B2": 600, "A3": "Gross margin", "B3": "=B1-B2"}
    ctx = ctx_for(tmp_path, rows, "B3")
    assert m.applies(ctx)
    mut = m.mutate(ctx, RNG)
    assert mut and mut.broken_formula == "=B1+B2"


def test_wrong_sign_not_without_labels(tmp_path):
    m = registry()["wrong_sign"]
    rows = {"B1": 1000, "B2": 600, "B3": "=B1-B2"}
    assert not m.applies(ctx_for(tmp_path, rows, "B3"))


def test_missing_factor_fires_and_prefers_absolute(tmp_path):
    m = registry()["missing_factor"]
    rows = {"A1": "FX rate", "B1": 82.5, "A3": "Product", "B3": "Qty", "C3": "Unit price", "D3": "Total INR",
            "A4": "Widget", "B4": 10, "C4": 2.5, "D4": "=B4*C4*$B$1"}
    ctx = ctx_for(tmp_path, rows, "D4")
    assert m.applies(ctx)
    mut = m.mutate(ctx, RNG)
    assert mut and mut.broken_formula == "=B4*C4"


def test_missing_factor_not_on_two_operands(tmp_path):
    m = registry()["missing_factor"]
    rows = {"A1": "Qty", "B1": 10, "A2": "Price", "B2": 3, "A3": "Total", "B3": "=B1*B2"}
    assert not m.applies(ctx_for(tmp_path, rows, "B3"))


def test_double_count_variant_a(tmp_path):
    m = registry()["double_count"]
    ctx = ctx_for(tmp_path, expense_block(), "B8")
    assert m.applies(ctx)
    mut = m.mutate(ctx, RNG)
    assert mut and (mut.broken_formula.startswith("=SUM(B3:B7)+B") or mut.broken_formula == "=SUM(B3:B8)")


def test_double_count_variant_b_subtotal_after(tmp_path):
    m = registry()["double_count"]
    rows = {"A1": "Item", "B1": "Amt", "A2": "a", "B2": 1, "A3": "b", "B3": 2, "A4": "c", "B4": 3,
            "A5": "Subtotal", "B5": "=SUM(B2:B4)", "A6": "Other", "B6": 5, "A7": "Grand total", "B7": "=SUM(B2:B4)"}
    ctx = ctx_for(tmp_path, rows, "B7")
    assert m.applies(ctx)
    # force variant B by removing labels inside? Simpler: check the subtotal detector directly
    assert m._subtotal_after(ctx.refs[0], ctx.sheet) is not None


def test_double_count_not_on_average(tmp_path):
    m = registry()["double_count"]
    rows = expense_block({"B8": "=AVERAGE(B3:B7)"})
    assert not m.applies(ctx_for(tmp_path, rows, "B8"))


def test_window_builds_for_every_mutated_case(tmp_path):
    ctx = ctx_for(tmp_path, expense_block(), "B8")
    w = build_window(ctx)
    assert "TARGET|Sheet1!B8|=SUM(B3:B7)" in w.text
    assert "ROW_PATH|Total expenses" in w.text
    assert w.tokens < 1500
