"""Web application: upload a workbook, follow the audit as it runs, read and download the result.

The API runs the same pipeline as scripts/audit_workbook.py (structure checks, context windows,
model verdicts, verify agent, second opinion). Audits run in a background worker one at a time;
the browser polls for progress. The React front end (webapp/frontend) is served from
webapp/backend/static once it is built.

Start:
  pip install -r requirements.txt
  python -m modal deploy training/predict_glimmer_modal.py        (once)
  set SHEETTRUTH_REVIEWER_BASE_URL, SHEETTRUTH_REVIEWER_MODEL, SHEETTRUTH_REVIEWER_API_KEY for the second opinion
  uvicorn webapp.backend.server:app --host 0.0.0.0 --port 8000

Environment:
  SHEETTRUTH_ADAPTER       adapter directory on the Modal volume (default: the released adapter)
  SHEETTRUTH_PREDICTIONS   optional JSONL of saved verdicts; used instead of the model (offline demo and tests)
  SHEETTRUTH_UPLOAD_DIR    where uploads and results are kept (default: data/uploads)
"""
from __future__ import annotations

import os
import shutil
import sys
import warnings
from pathlib import Path
from typing import Callable

import yaml
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

warnings.filterwarnings("ignore")
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from webapp.backend.jobs import JobStore  # noqa: E402
from sheettruth.agent.graph import AuditGraph  # noqa: E402
from sheettruth.agent.model_client import ModalPredictorClient, SavedPredictionsClient  # noqa: E402
from sheettruth.agent.reviewer import HostedReviewer, NoReviewer  # noqa: E402
from sheettruth.data.convert import CONVERTIBLE_SUFFIXES, conversion_available, xls_to_xlsx  # noqa: E402
from sheettruth.data.recalc import Recalculator  # noqa: E402
from sheettruth.verify import Verifier  # noqa: E402

ADAPTER_DIR = os.environ.get("SHEETTRUTH_ADAPTER", "/models/glimmer-sheettruth-v2/adapter")
SAVED_PREDICTIONS = os.environ.get("SHEETTRUTH_PREDICTIONS", "")
UPLOAD_DIR = Path(os.environ.get("SHEETTRUTH_UPLOAD_DIR", ROOT / "data" / "uploads"))
STATIC_DIR = Path(__file__).resolve().parent / "static"
CONFIG = yaml.safe_load(open(ROOT / "configs" / "default.yaml"))
MAX_UPLOAD_BYTES = 25 * 1024 * 1024
ALLOWED_SUFFIXES = (".xlsx", ".xlsm") + CONVERTIBLE_SUFFIXES
XLS_UNAVAILABLE = ("this server cannot convert .xls files right now; save the workbook as .xlsx in Excel "
                   "and upload that instead")


def build_graph() -> AuditGraph:
    model = SavedPredictionsClient(SAVED_PREDICTIONS) if SAVED_PREDICTIONS else ModalPredictorClient(ADAPTER_DIR)
    reviewer = HostedReviewer()
    return AuditGraph(model, Verifier(Recalculator(timeout=CONFIG["recalc"]["timeout_s"])),
                      reviewer if reviewer.configured else NoReviewer())


GRAPH = build_graph()


def run_audit(path: str, threshold: float, out_path: str, on_step: Callable[[str, dict], None]) -> dict:
    return GRAPH.run(path, CONFIG, threshold, out_path, on_step)


STORE = JobStore(UPLOAD_DIR, run_audit)
app = FastAPI(title="SheetTruth")


@app.get("/api/health")
def health() -> dict:
    return {
        "model": "saved predictions" if SAVED_PREDICTIONS else f"Modal predictor ({ADAPTER_DIR})",
        "recalculation": shutil.which("soffice") is not None,
        "reviewer": isinstance(GRAPH.reviewer, HostedReviewer),
        "conversion": conversion_available(),
        "queued": STORE.queue.qsize(),
    }


@app.get("/api/audits")
def list_audits() -> list[dict]:
    return [job.to_dict() for job in STORE.list()]


@app.post("/api/audits", status_code=201)
async def create_audit(file: UploadFile = File(...), threshold: float = Form(0.5)) -> dict:
    name = Path(file.filename or "").name
    if not name.lower().endswith(ALLOWED_SUFFIXES):
        raise HTTPException(400, "please upload an .xlsx, .xlsm or .xls workbook")
    if not 0.0 < threshold <= 1.0:
        raise HTTPException(400, "threshold must be between 0 and 1")
    data = await file.read()
    if len(data) > MAX_UPLOAD_BYTES:
        raise HTTPException(413, "workbook larger than 25 MB")
    if name.lower().endswith(CONVERTIBLE_SUFFIXES):
        data, name = _convert_legacy_upload(data, name)
    job = STORE.create(name, data, threshold)
    return job.to_dict()


def _convert_legacy_upload(data: bytes, name: str) -> tuple[bytes, str]:
    """Turn an .xls upload into the .xlsx the pipeline reads, or explain why that is not possible."""
    if not conversion_available():
        raise HTTPException(400, XLS_UNAVAILABLE)
    try:
        return xls_to_xlsx(data, name, timeout=CONFIG["recalc"]["timeout_s"])
    except RuntimeError as exc:
        raise HTTPException(400, f"the .xls file could not be converted ({exc}); save it as .xlsx and try again")


@app.get("/api/audits/{job_id}")
def get_audit(job_id: str) -> dict:
    job = _job_or_404(job_id)
    return {**job.to_dict(), "result": STORE.detail(job)}


@app.get("/api/audits/{job_id}/report.md")
def download_report_markdown(job_id: str) -> FileResponse:
    job = _job_or_404(job_id)
    return _file_or_404(STORE.report_path(job, ".md"), f"{Path(job.filename).stem}_audit.md", "text/markdown")


@app.get("/api/audits/{job_id}/report.json")
def download_report_json(job_id: str) -> FileResponse:
    job = _job_or_404(job_id)
    return _file_or_404(STORE.report_path(job, ".json"), f"{Path(job.filename).stem}_audit.json", "application/json")


@app.get("/api/audits/{job_id}/corrected.xlsx")
def download_corrected_workbook(job_id: str) -> FileResponse:
    job = _job_or_404(job_id)
    path = STORE.ensure_corrected_copy(job)
    if path is None:
        raise HTTPException(409, "the audit has not finished")
    return FileResponse(path, filename=path.name,
                        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


def _job_or_404(job_id: str):
    job = STORE.get(job_id)
    if job is None:
        raise HTTPException(404, "no such audit")
    return job


def _file_or_404(path: Path, download_name: str, media_type: str) -> FileResponse:
    if not path.exists():
        raise HTTPException(409, "the audit has not finished")
    return FileResponse(path, filename=download_name, media_type=media_type)


@app.get("/api")
def api_index() -> JSONResponse:
    return JSONResponse({"audits": "/api/audits", "health": "/api/health", "front_end_built": STATIC_DIR.exists()})


if STATIC_DIR.exists():
    app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")
