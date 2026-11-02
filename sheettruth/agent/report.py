"""Markdown and JSON rendering of an audit."""
from __future__ import annotations

import json
from pathlib import Path


def evidence_text(verification: dict) -> str:
    kept = [c for c in verification["checks"] if c["result"] in ("supports", "contradicts")]
    return "; ".join(f"{c['name']} {c['result']}: {c['detail']}" for c in kept) or "no independent check applied"


def _finding_row(f: dict) -> str:
    run = f"{len(f['run_cells'])} cells" if len(f["run_cells"]) > 1 else "1 cell"
    return (f"| {f['sheet']}!{f['addr']} | {run} | {f['p_error']:.2f} | {f['type'] or ''} | `{f['formula'][:50]}` | "
            f"`{(f['expected'] or '')[:50]}` | {f['verification']['outcome']} | {evidence_text(f['verification'])} |")


def _structure_row(s: dict) -> str:
    return f"| {s['sheet']}!{s['addr']} | {s['kind']} | `{s['current'][:40]}` | `{s['implied_formula'][:40]}` | {s['detail']} |"


def render_markdown(name: str, n_cells: int, n_windows: int, findings: list[dict], structure: list[dict],
                    threshold: float) -> str:
    outcomes = {k: sum(1 for f in findings if f["verification"]["outcome"] == k)
                for k in ("passed", "failed", "no_independent_check")}
    lines = [f"# Audit of {name}", "",
             f"Formula cells scanned: {n_cells} in {n_windows} windows. Flagged at P(error) >= {threshold}: {len(findings)} "
             f"(verified {outcomes['passed']}, contradicted {outcomes['failed']}, unverifiable {outcomes['no_independent_check']}). "
             f"Structure findings: {len(structure)}.", "",
             "## Model findings", "",
             "| cell | run | P(error) | type | formula | proposed fix | verification | evidence |",
             "|---|---|---|---|---|---|---|---|"]
    lines += [_finding_row(f) for f in findings]
    lines += ["", "## Structure findings (no model involved)", "",
              "| cell | kind | current | implied formula | detail |", "|---|---|---|---|---|"]
    lines += [_structure_row(s) for s in structure]
    return "\n".join(lines) + "\n"


def write_outputs(out: Path, markdown_text: str, detail: dict) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(markdown_text)
    out.with_suffix(".json").write_text(json.dumps(detail, indent=1, default=str))
