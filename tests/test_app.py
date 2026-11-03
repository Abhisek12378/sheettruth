"""The web API end to end with saved verdicts: create an audit, poll it, download the outputs."""
import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sheettruth.agent.fixes import write_corrected_copy  # noqa: E402

ROWS = [["Item", "Amount"], ["Rent", 100], ["Salaries", 400], ["Travel", 50], ["Marketing", 80], ["Total", "=SUM(B2:B4)"]]


def _write_book(path: Path, rows: list[list]) -> str:
    import openpyxl

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Sheet1"
    for row in rows:
        ws.append(row)
    wb.save(path)
    return str(path)


def _saved_predictions(path: Path) -> None:
    verdict = {"id": "x:Sheet1!B6", "verdict": "error", "type": "skipped_rows", "expected": "=SUM(B2:B5)",
               "reason": "The SUM range stops short: Marketing is left out.", "p_error": 0.97, "parsed": True}
    path.write_text(json.dumps(verdict) + "\n")


def _wait_until_done(client, job_id: str, timeout_s: float = 60.0) -> dict:
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        job = client.get(f"/api/audits/{job_id}").json()
        if job["status"] in ("done", "failed"):
            return job
        time.sleep(0.2)
    raise AssertionError("the audit did not finish in time")


def test_audit_job_lifecycle(tmp_path, monkeypatch):
    _saved_predictions(tmp_path / "preds.jsonl")
    monkeypatch.setenv("SHEETTRUTH_PREDICTIONS", str(tmp_path / "preds.jsonl"))
    monkeypatch.setenv("SHEETTRUTH_UPLOAD_DIR", str(tmp_path / "uploads"))
    for name in [m for m in sys.modules if m.startswith("webapp.")]:
        del sys.modules[name]
    from fastapi.testclient import TestClient
    from webapp.backend.server import app

    client = TestClient(app)
    book = _write_book(tmp_path / "budget.xlsx", ROWS)
    with open(book, "rb") as f:
        created = client.post("/api/audits", files={"file": ("budget.xlsx", f)}, data={"threshold": "0.5"})
    assert created.status_code == 201
    job = _wait_until_done(client, created.json()["id"])
    assert job["status"] == "done", job["error"]
    assert [s["node"] for s in job["steps"]][:3] == ["load_workbook", "structure_checks", "build_windows"]
    assert job["summary"]["flagged"] == 1
    assert job["result"]["findings"][0]["addr"] == "B6"
    assert client.get(f"/api/audits/{job['id']}/report.md").status_code == 200
    assert client.get(f"/api/audits/{job['id']}/corrected.xlsx").status_code == 200
    assert client.get("/api/audits/nope").status_code == 404
    assert client.post("/api/audits", files={"file": ("notes.txt", b"hello")}).status_code == 400


def test_corrected_copy_applies_confirmed_fix_to_the_run(tmp_path):
    import openpyxl

    book = _write_book(tmp_path / "t.xlsx", [["a", "=SUM(B2:B3)", "=SUM(C2:C3)"], [1, 2, 3], [4, 5, 6], [7, 8, 9]])
    findings = [{"sheet": "Sheet1", "addr": "B1", "run_cells": ["B1", "C1"], "expected": "=SUM(B2:B4)", "status": "confirmed"},
                {"sheet": "Sheet1", "addr": "A1", "run_cells": ["A1"], "expected": "=1", "status": "disputed"}]
    changed = write_corrected_copy(book, str(tmp_path / "fixed.xlsx"), findings)
    ws = openpyxl.load_workbook(tmp_path / "fixed.xlsx")["Sheet1"]
    assert changed == 2
    assert ws["B1"].value == "=SUM(B2:B4)" and ws["C1"].value == "=SUM(C2:C4)" and ws["A1"].value == "a"
    assert os.path.exists(book)
