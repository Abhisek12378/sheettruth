"""The audit workflow as a LangGraph state graph.

    load_workbook -> structure_checks -> build_windows -> score_windows -> select_findings
        -> (nothing flagged) -> write_report
        -> (findings)        -> verify_findings -> second_opinion -> write_report

Each node is a plain function over the shared AuditState. The model is reached through a
ModelClient, the verify agent through a Verifier, the second opinion through a ReviewerClient, so
the same graph runs against the deployed model, against saved verdicts, with or without
LibreOffice, with or without a reviewer. The `notes` list is the run log the report and the web
page show.

Final status of a finding (workbook facts first, reviewer opinion second, model claim last):
  contradicted   a code check speaks against it
  confirmed      a code check supports it, or no code check applied and the reviewer calls it a real error
  disputed       no code check applied and the reviewer calls it not an error
  unverified     nothing could be tested and the reviewer could not tell
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional, TypedDict

from langgraph.graph import END, START, StateGraph

from sheettruth.agent.model_client import ModelClient, window_key
from sheettruth.agent.report import render_markdown, write_outputs
from sheettruth.agent.reviewer import NoReviewer, ReviewerClient
from sheettruth.shape import shape_findings
from sheettruth.verify import Finding, Verifier
from sheettruth.windows.cellinfo import Workbook
from sheettruth.windows.runs import workbook_records


class AuditState(TypedDict, total=False):
    workbook_path: str
    threshold: float
    config: dict
    out_path: str
    structure: list[dict]
    records: list[dict]
    out_of_scope: int
    verdicts: dict[str, dict]
    flagged: list[dict]
    findings: list[dict]
    report_markdown: str
    notes: list[str]


class AuditGraph:
    """Builds and runs the audit workflow for one workbook."""

    def __init__(self, model: ModelClient, verifier: Verifier, reviewer: Optional[ReviewerClient] = None):
        self.model = model
        self.verifier = verifier
        self.reviewer = reviewer or NoReviewer()
        self.graph = self._build()

    # -- nodes ------------------------------------------------------------------------------

    def load_workbook(self, state: AuditState) -> AuditState:
        wb = Workbook(state["workbook_path"])
        sheets = ", ".join(wb.sheetnames)
        return {"notes": state.get("notes", []) + [f"loaded {Path(state['workbook_path']).name}: sheets {sheets}"]}

    def structure_checks(self, state: AuditState) -> AuditState:
        wb = Workbook(state["workbook_path"])
        structure = [f.to_dict() for f in shape_findings(wb)]
        return {"structure": structure, "notes": state["notes"] + [f"structure checks: {len(structure)} findings"]}

    def build_windows(self, state: AuditState) -> AuditState:
        path = state["workbook_path"]
        records, out_of_scope = workbook_records(0, Path(path).name, path, state["config"])
        n_cells = sum(len(r["run_cells"]) for r in records)
        note = f"windows: {len(records)} runs covering {n_cells} formula cells, {out_of_scope} cells out of scope"
        return {"records": records, "out_of_scope": out_of_scope, "notes": state["notes"] + [note]}

    def score_windows(self, state: AuditState) -> AuditState:
        verdicts = self.model.score(state["records"]) if state["records"] else {}
        return {"verdicts": verdicts, "notes": state["notes"] + [f"model verdicts: {len(verdicts)}"]}

    def select_findings(self, state: AuditState) -> AuditState:
        flagged = []
        for rec in state["records"]:
            v = state["verdicts"].get(window_key(rec))
            if v and (v.get("p_error", 0.0) >= state["threshold"] or v.get("verdict") == "error"):
                flagged.append(_candidate(rec, v))
        flagged.sort(key=_error_probability, reverse=True)
        return {"flagged": flagged, "notes": state["notes"] + [f"flagged at P(error) >= {state['threshold']}: {len(flagged)}"]}

    def verify_findings(self, state: AuditState) -> AuditState:
        wb = Workbook(state["workbook_path"])
        findings = []
        for cand in state["flagged"]:
            finding = Finding(cand["sheet"], cand["addr"], cand["formula"], cand["expected"], cand["type"],
                              cand["reason"], cand["p_error"])
            result = self.verifier.verify(wb, state["workbook_path"], finding)
            findings.append({**cand, "verification": result.to_dict()})
        outcomes = {k: sum(1 for f in findings if f["verification"]["outcome"] == k)
                    for k in ("passed", "failed", "no_independent_check")}
        return {"findings": findings, "notes": state["notes"] + [f"verify agent: {outcomes}"]}

    def second_opinion(self, state: AuditState) -> AuditState:
        """Findings not contradicted by code go to the reviewer; every finding gets a final status."""
        findings = state["findings"]
        to_review = [f for f in findings if f["verification"]["outcome"] != "failed"]
        reviews = self.reviewer.review(to_review)
        for finding, review in zip(to_review, reviews):
            finding["review"] = review.to_dict()
        for finding in findings:
            finding["status"] = final_status(finding)
        statuses = {k: sum(1 for f in findings if f["status"] == k) for k in ("confirmed", "unverified", "disputed", "contradicted")}
        return {"findings": findings, "notes": state["notes"] + [f"second opinion on {len(to_review)}; status {statuses}"]}

    def write_report(self, state: AuditState) -> AuditState:
        findings = state.get("findings", [])
        n_cells = sum(len(r["run_cells"]) for r in state["records"])
        markdown_text = render_markdown(Path(state["workbook_path"]).name, n_cells, len(state["records"]), findings,
                                        state["structure"], state["threshold"])
        if state.get("out_path"):
            detail = {"workbook": state["workbook_path"], "threshold": state["threshold"], "findings": findings,
                      "structure": state["structure"], "notes": state["notes"]}
            write_outputs(Path(state["out_path"]), markdown_text, detail)
        return {"findings": findings, "report_markdown": markdown_text,
                "notes": state["notes"] + ["report written"]}

    # -- wiring -----------------------------------------------------------------------------

    @staticmethod
    def _after_select(state: AuditState) -> str:
        return "verify_findings" if state["flagged"] else "write_report"

    def _build(self):
        g = StateGraph(AuditState)
        for name in ("load_workbook", "structure_checks", "build_windows", "score_windows", "select_findings",
                     "verify_findings", "second_opinion", "write_report"):
            g.add_node(name, getattr(self, name))
        g.add_edge(START, "load_workbook")
        g.add_edge("load_workbook", "structure_checks")
        g.add_edge("structure_checks", "build_windows")
        g.add_edge("build_windows", "score_windows")
        g.add_edge("score_windows", "select_findings")
        g.add_conditional_edges("select_findings", self._after_select, ["verify_findings", "write_report"])
        g.add_edge("verify_findings", "second_opinion")
        g.add_edge("second_opinion", "write_report")
        g.add_edge("write_report", END)
        return g.compile()

    def run(self, workbook_path: str, config: dict, threshold: float = 0.5, out_path: Optional[str] = None) -> AuditState:
        initial: AuditState = {"workbook_path": workbook_path, "config": config, "threshold": threshold,
                               "out_path": out_path or "", "notes": []}
        return self.graph.invoke(initial)


def _candidate(record: dict, verdict: dict) -> dict:
    return {"sheet": record["sheet"], "addr": record["addr"], "run_cells": record["run_cells"],
            "formula": record["formula"], "window": record["window"], "type": verdict.get("type"),
            "expected": verdict.get("expected"), "reason": verdict.get("reason", ""), "p_error": verdict.get("p_error", 0.0)}


def final_status(finding: dict) -> str:
    """Workbook facts outrank the reviewer's opinion, which outranks the model's own claim."""
    outcome = finding["verification"]["outcome"]
    review = finding.get("review", {}).get("verdict", "cannot_tell")
    if outcome == "failed":
        return "contradicted"
    if outcome == "passed" or review == "real_error":
        return "confirmed"
    if review == "not_error":
        return "disputed"
    return "unverified"


def _error_probability(candidate: dict) -> float:
    return candidate["p_error"]
