"""Small web front end: upload a workbook, get the audit report.

Runs the same pipeline as scripts/audit_workbook.py (structure checks, windows, model verdicts,
verify agent) and renders the Markdown report as a page. Meant for a single machine that has
LibreOffice and Modal credentials; audits run one at a time.

Start:
  pip install fastapi uvicorn python-multipart markdown
  python -m modal deploy training/predict_glimmer_modal.py        (once)
  set SHEETTRUTH_REVIEWER_BASE_URL, SHEETTRUTH_REVIEWER_MODEL, SHEETTRUTH_REVIEWER_API_KEY for the second opinion
  uvicorn app.server:app --host 0.0.0.0 --port 8000
"""
from __future__ import annotations

import os
import sys
import tempfile
import threading
import warnings
from pathlib import Path

import markdown
import yaml
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import HTMLResponse

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from sheettruth.agent.graph import AuditGraph  # noqa: E402
from sheettruth.agent.model_client import ModalPredictorClient  # noqa: E402
from sheettruth.agent.reviewer import HostedReviewer, NoReviewer  # noqa: E402
from sheettruth.data.recalc import Recalculator  # noqa: E402
from sheettruth.verify import Verifier  # noqa: E402

ADAPTER_DIR = os.environ.get("SHEETTRUTH_ADAPTER", "/models/glimmer-sheettruth-v2/adapter")
CONFIG = yaml.safe_load(open(ROOT / "configs" / "default.yaml"))
REPORT_DIR = ROOT / "reports" / "uploads"
LOCK = threading.Lock()

app = FastAPI(title="SheetTruth")

PAGE = """<!doctype html><html><head><meta charset="utf-8"><title>SheetTruth</title>
<style>
 body{{font-family:system-ui,sans-serif;max-width:1100px;margin:2rem auto;padding:0 1rem;color:#1a1a1a}}
 table{{border-collapse:collapse;width:100%;font-size:14px}} th,td{{border:1px solid #ddd;padding:6px 8px;vertical-align:top}}
 th{{background:#f4f4f4;text-align:left}} code{{background:#f6f6f6;padding:1px 4px}}
 form{{margin:1.5rem 0;padding:1rem;border:1px solid #ddd;border-radius:8px}}
 .muted{{color:#666}}
</style></head><body>
<h1>SheetTruth</h1>
<p class="muted">Finds formulas that compute the wrong thing, then checks each finding against the workbook itself.</p>
<form method="post" action="/audit" enctype="multipart/form-data">
 <input type="file" name="file" accept=".xlsx" required>
 <label>Flag at P(error) &ge; <input type="number" name="threshold" value="0.5" min="0" max="1" step="0.05" style="width:5em"></label>
 <button type="submit">Audit</button>
 <span class="muted">An audit takes one to several minutes depending on the workbook.</span>
</form>
{body}
</body></html>"""


def build_graph() -> AuditGraph:
    reviewer = HostedReviewer()
    return AuditGraph(ModalPredictorClient(ADAPTER_DIR), Verifier(Recalculator(timeout=CONFIG["recalc"]["timeout_s"])),
                      reviewer if reviewer.configured else NoReviewer())


GRAPH = build_graph()


def run_audit(path: str, threshold: float) -> str:
    """The audit graph on one file; returns the Markdown report and stores the detail under reports/uploads."""
    out = REPORT_DIR / (Path(path).stem + ".md")
    state = GRAPH.run(path, CONFIG, threshold, str(out))
    return state["report_markdown"]


@app.get("/", response_class=HTMLResponse)
def home() -> str:
    return PAGE.format(body="")


@app.post("/audit", response_class=HTMLResponse)
async def audit_upload(file: UploadFile = File(...), threshold: float = Form(0.5)) -> str:
    data = await file.read()
    with tempfile.TemporaryDirectory(prefix="st-upload-") as tmp:
        path = os.path.join(tmp, Path(file.filename or "book.xlsx").name)
        Path(path).write_bytes(data)
        with LOCK:
            report_md = run_audit(path, threshold)
    html = markdown.markdown(report_md, extensions=["tables"])
    return PAGE.format(body=html)
