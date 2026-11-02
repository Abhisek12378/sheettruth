"""The audit graph end to end on a tiny workbook, with a stub model and no LibreOffice."""
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from test_mutators import make_wb  # noqa: E402
from test_verify import amount_table  # noqa: E402
from sheettruth.agent.graph import AuditGraph  # noqa: E402
from sheettruth.verify import Verifier  # noqa: E402

CONFIG = yaml.safe_load(open(Path(__file__).resolve().parents[1] / "configs" / "default.yaml"))


class StubModel:
    """Flags one known cell and calls everything else ok."""

    def score(self, records):
        out = {}
        for r in records:
            key = f"{r['sheet']}!{r['addr']}"
            if r["addr"] == "D14":
                out[key] = {"verdict": "error", "type": "skipped_rows", "expected": "=SUM(D2:D12)",
                            "reason": "range stops short", "p_error": 0.9}
            else:
                out[key] = {"verdict": "ok", "type": None, "expected": None, "reason": "", "p_error": 0.01}
        return out


def test_graph_runs_all_nodes_and_verifies(tmp_path):
    rows = amount_table({"A14": "Total", "D14": "=SUM(D2:D10)", "D5": 50})
    make_wb(tmp_path, rows, "book.xlsx")
    out = tmp_path / "report.md"
    state = AuditGraph(StubModel(), Verifier(None)).run(str(tmp_path / "book.xlsx"), CONFIG, 0.5, str(out))
    assert [f["addr"] for f in state["findings"]] == ["D14"]
    assert state["findings"][0]["verification"]["outcome"] == "passed"
    assert any(s["kind"] == "hardcoded_value" and s["addr"] == "D5" for s in state["structure"])
    assert out.exists() and out.with_suffix(".json").exists()
    assert "D14" in state["report_markdown"]


def test_graph_skips_verify_when_nothing_flagged(tmp_path):
    make_wb(tmp_path, amount_table(), "clean.xlsx")
    state = AuditGraph(StubModel(), Verifier(None)).run(str(tmp_path / "clean.xlsx"), CONFIG, 0.5)
    assert state["findings"] == []
    assert not any(n.startswith("verify agent") for n in state["notes"])


class StubReviewer:
    """Calls every finding a real error, with a fixed reason."""

    def review(self, items):
        from sheettruth.agent.reviewer import Review
        return [Review("real_error", "stub reviewer") for _ in items]


def test_graph_records_reviewer_verdict_and_status(tmp_path):
    rows = amount_table({"A14": "Total", "D14": "=SUM(D2:D10)"})
    make_wb(tmp_path, rows, "book.xlsx")
    state = AuditGraph(StubModel(), Verifier(None), StubReviewer()).run(str(tmp_path / "book.xlsx"), CONFIG, 0.5)
    finding = state["findings"][0]
    assert finding["review"] == {"verdict": "real_error", "reason": "stub reviewer"}
    assert finding["status"] == "confirmed"
    assert "reviewer" in state["report_markdown"]
