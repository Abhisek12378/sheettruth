"""Audit jobs: one folder per uploaded workbook, one background worker, progress by polling.

An audit takes from one to several minutes (model calls, LibreOffice recalculation, reviewer
calls), so the web API never runs it inside a request. A job is created, queued, and processed by
a single worker thread; the browser polls the job until it is done. Every job is saved as a JSON
file in its own folder next to the uploaded workbook, so the history survives a restart.
"""
from __future__ import annotations

import json
import queue
import threading
import time
import traceback
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Callable, Optional

from sheettruth.agent.fixes import write_corrected_copy

STEP_LABELS = {
    "load_workbook": "Opening the workbook",
    "structure_checks": "Structure checks",
    "build_windows": "Building context windows",
    "score_windows": "Model verdicts",
    "select_findings": "Selecting findings",
    "verify_findings": "Verify agent",
    "second_opinion": "Second opinion",
    "write_report": "Writing the report",
}
STATUS_KEYS = ("confirmed", "unverified", "disputed", "contradicted")


@dataclass
class Job:
    id: str
    filename: str
    threshold: float
    created_at: float
    status: str = "queued"               # queued | running | done | failed
    steps: list[dict] = field(default_factory=list)
    error: str = ""
    summary: dict = field(default_factory=dict)
    finished_at: Optional[float] = None

    def to_dict(self) -> dict:
        return asdict(self)


class JobStore:
    """Keeps jobs on disk under `root/<job id>/` and runs them one at a time."""

    def __init__(self, root: Path, run_audit: Callable[[str, float, str, Callable[[str, dict], None]], dict]):
        self.root = root
        self.run_audit = run_audit
        self.jobs: dict[str, Job] = {}
        self.lock = threading.Lock()
        self.queue: queue.Queue[str] = queue.Queue()
        self.root.mkdir(parents=True, exist_ok=True)
        self._load_existing()
        self.worker = threading.Thread(target=self._work, name="audit-worker", daemon=True)
        self.worker.start()

    # -- paths ------------------------------------------------------------------------------

    def folder(self, job_id: str) -> Path:
        return self.root / job_id

    def workbook_path(self, job: Job) -> Path:
        return self.folder(job.id) / job.filename

    def report_path(self, job: Job, suffix: str) -> Path:
        return self.folder(job.id) / f"report{suffix}"

    def corrected_path(self, job: Job) -> Path:
        stem = Path(job.filename).stem
        return self.folder(job.id) / f"{stem}_corrected.xlsx"

    # -- public API -------------------------------------------------------------------------

    def create(self, filename: str, data: bytes, threshold: float) -> Job:
        job = Job(id=uuid.uuid4().hex[:12], filename=Path(filename).name, threshold=threshold, created_at=time.time())
        self.folder(job.id).mkdir(parents=True, exist_ok=True)
        self.workbook_path(job).write_bytes(data)
        with self.lock:
            self.jobs[job.id] = job
        self._save(job)
        self.queue.put(job.id)
        return job

    def get(self, job_id: str) -> Optional[Job]:
        with self.lock:
            return self.jobs.get(job_id)

    def list(self) -> list[Job]:
        with self.lock:
            return sorted(self.jobs.values(), key=_newest_first)

    def detail(self, job: Job) -> Optional[dict]:
        """The full audit result (findings, structure findings, run notes) once the job is done."""
        path = self.report_path(job, ".json")
        if job.status != "done" or not path.exists():
            return None
        return json.loads(path.read_text())

    def ensure_corrected_copy(self, job: Job) -> Optional[Path]:
        """The workbook with confirmed fixes applied, written on first request."""
        detail = self.detail(job)
        if detail is None:
            return None
        path = self.corrected_path(job)
        if not path.exists():
            write_corrected_copy(str(self.workbook_path(job)), str(path), detail["findings"])
        return path

    # -- worker -----------------------------------------------------------------------------

    def _work(self) -> None:
        while True:
            job_id = self.queue.get()
            job = self.get(job_id)
            if job is not None:
                self._run(job)
            self.queue.task_done()

    def _run(self, job: Job) -> None:
        job.status = "running"
        job.steps = []
        self._save(job)
        try:
            state = self.run_audit(str(self.workbook_path(job)), job.threshold, str(self.report_path(job, ".md")),
                                   StepRecorder(self, job))
            job.summary = summarise(state)
            job.status = "done"
        except Exception as ex:                      # the job must record any failure, whatever its type
            job.status = "failed"
            job.error = f"{type(ex).__name__}: {ex}"
            traceback.print_exc()
        job.finished_at = time.time()
        self._save(job)

    def record_step(self, job: Job, node: str, state: dict) -> None:
        note = state["notes"][-1] if state.get("notes") else ""
        job.steps.append({"node": node, "label": STEP_LABELS.get(node, node), "note": note, "at": time.time()})
        self._save(job)

    # -- persistence ------------------------------------------------------------------------

    def _save(self, job: Job) -> None:
        (self.folder(job.id) / "job.json").write_text(json.dumps(job.to_dict(), indent=1))

    def _load_existing(self) -> None:
        for path in self.root.glob("*/job.json"):
            job = Job(**json.loads(path.read_text()))
            if job.status in ("queued", "running"):   # interrupted by a restart; it will not resume
                job.status = "failed"
                job.error = "the server stopped before this audit finished"
                self._save(job)
            self.jobs[job.id] = job


class StepRecorder:
    """Callable handed to the audit graph; appends one progress entry per finished node."""

    def __init__(self, store: JobStore, job: Job):
        self.store = store
        self.job = job

    def __call__(self, node: str, state: dict) -> None:
        self.store.record_step(self.job, node, state)


def summarise(state: dict) -> dict:
    """Counts shown in the job list and at the top of the result page."""
    findings = state.get("findings", [])
    records = state.get("records", [])
    return {
        "formula_cells": sum(len(r["run_cells"]) for r in records),
        "windows": len(records),
        "out_of_scope": state.get("out_of_scope", 0),
        "flagged": len(findings),
        "by_status": {k: sum(1 for f in findings if f.get("status") == k) for k in STATUS_KEYS},
        "structure_findings": len(state.get("structure", [])),
    }


def _newest_first(job: Job) -> float:
    return -job.created_at
