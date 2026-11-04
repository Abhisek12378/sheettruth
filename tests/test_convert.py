"""Legacy .xls uploads: converted with LibreOffice when it is present, refused clearly when not."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sheettruth.data import convert  # noqa: E402

ROWS = [["Item", "Amount"], ["Rent", 100], ["Salaries", 400], ["Total", "=SUM(B2:B3)"]]


def _write_xlsx(path: Path) -> Path:
    import openpyxl

    wb = openpyxl.Workbook()
    ws = wb.active
    for row in ROWS:
        ws.append(row)
    wb.save(path)
    return path


@pytest.mark.skipif(not convert.conversion_available(), reason="LibreOffice is not installed")
def test_xls_round_trip_keeps_formulas(tmp_path):
    import openpyxl

    original = _write_xlsx(tmp_path / "budget.xlsx")
    legacy = convert.convert_workbook(original, "xls")
    assert legacy.suffix == ".xls"

    data, name = convert.xls_to_xlsx(legacy.read_bytes(), legacy.name)
    assert name == "budget.xlsx"
    out = tmp_path / "back.xlsx"
    out.write_bytes(data)
    ws = openpyxl.load_workbook(out).active
    assert ws["B4"].value == "=SUM(B2:B3)"
    assert ws["A2"].value == "Rent"


def test_xls_upload_refused_without_libreoffice(tmp_path, monkeypatch):
    monkeypatch.setenv("SHEETTRUTH_PREDICTIONS", str(tmp_path / "none.jsonl"))
    monkeypatch.setenv("SHEETTRUTH_UPLOAD_DIR", str(tmp_path / "uploads"))
    (tmp_path / "none.jsonl").write_text("")
    for name in [m for m in sys.modules if m.startswith("webapp.")]:
        del sys.modules[name]
    from fastapi.testclient import TestClient
    from webapp.backend import server

    monkeypatch.setattr(server, "conversion_available", lambda: False)
    client = TestClient(server.app)
    response = client.post("/api/audits", files={"file": ("old.xls", b"not really a workbook")},
                           data={"threshold": "0.5"})
    assert response.status_code == 400
    assert ".xlsx" in response.json()["detail"]


def test_other_suffixes_still_refused(tmp_path, monkeypatch):
    monkeypatch.setenv("SHEETTRUTH_PREDICTIONS", str(tmp_path / "none.jsonl"))
    monkeypatch.setenv("SHEETTRUTH_UPLOAD_DIR", str(tmp_path / "uploads"))
    (tmp_path / "none.jsonl").write_text("")
    for name in [m for m in sys.modules if m.startswith("webapp.")]:
        del sys.modules[name]
    from fastapi.testclient import TestClient
    from webapp.backend import server

    client = TestClient(server.app)
    response = client.post("/api/audits", files={"file": ("notes.csv", b"a,b")}, data={"threshold": "0.5"})
    assert response.status_code == 400
