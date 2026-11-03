"""Score model verdicts on the held-out test workbooks against the documented errors.

A documented error counts as found when a window whose run covers one of its faulty cells was
given an "error" verdict. A window with an "error" verdict whose run touches no documented faulty
cell in that workbook is a false alarm. Errors on cells that got no window (formula outside the
supported set, or no formula in the converted file) are reported as not covered, so the recall on
covered errors and the recall on all errors are both shown.

Usage:
  python scripts/evaluate_enron.py --predictions data/test/predictions.jsonl \\
      --windows data/test/windows.jsonl --overview data/test/enron_errors_overview.json \\
      --out reports/enron_eval.md
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import sys
from pathlib import Path

from openpyxl.utils import get_column_letter, range_boundaries

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sheettruth.agent.reviewer import HostedReviewer  # noqa: E402
from sheettruth.data.recalc import Recalculator  # noqa: E402
from sheettruth.verify import Finding, Verifier  # noqa: E402
from sheettruth.windows.cellinfo import Workbook  # noqa: E402

CELL_OR_RANGE = re.compile(r"\$?[A-Z]{1,3}\$?\d+(?::\$?[A-Z]{1,3}\$?\d+)?")


SWEEP = (0.02, 0.05, 0.1, 0.2, 0.3, 0.5)
REVIEW_CHUNK = 8


def flagged_at(predictions: list[dict], threshold: float) -> dict[str, dict]:
    """Verdicts after applying an error-probability threshold; predictions without probabilities keep
    their stated verdict."""
    out = {}
    for p in predictions:
        p = dict(p)
        if "p_error" in p:
            quiet = "unsupported" if p.get("verdict") == "unsupported" else "ok"
            p["verdict"] = "error" if p["p_error"] >= threshold else quiet
        out[p["id"]] = p
    return out


def load_jsonl(path: str) -> list[dict]:
    with open(path) as f:
        return [json.loads(line) for line in f if line.strip()]


def norm_sheet(name: str) -> str:
    return re.sub(r"\s+", " ", (name or "").strip().lower())


def expand_cells(spec: str) -> set[str]:
    """'F28:G28; M22' -> {'F28', 'G28', 'M22'}; words such as 'etc.' are ignored."""
    cells: set[str] = set()
    for token in CELL_OR_RANGE.findall((spec or "").upper().replace("$", "")):
        c1, r1, c2, r2 = range_boundaries(token if ":" in token else f"{token}:{token}")
        for r in range(r1, r2 + 1):
            for c in range(c1, c2 + 1):
                cells.add(f"{get_column_letter(c)}{r}")
    return cells


def documented_errors(overview: list[dict]) -> list[dict]:
    out = []
    for e in overview:
        if e["cell_type"] != "Formula" or not e["faulty_file"]:
            continue
        out.append({"err": e["err"], "ss": e["ss"], "sheet": norm_sheet(e["faulty_sheet"]),
                    "cells": expand_cells(e["faulty_cells"]), "info": e["info"],
                    "faulty_formula": e["faulty"].get("formula"), "corrected_formula": e["corrected"].get("formula")})
    return out


def normalise_formula(f) -> str:
    return re.sub(r"\s+|\$", "", str(f or "")).upper().replace("=+", "=")


def index_windows(windows: list[dict]) -> dict[tuple[int, str, str], dict]:
    """(case, sheet, cell) -> window record, for every cell in every run."""
    index = {}
    for w in windows:
        for cell in w["run_cells"]:
            index[(w["ss"], norm_sheet(w["sheet"]), cell)] = w
    return index


def judge_error(err: dict, by_cell: dict, verdicts: dict) -> dict:
    """Status of one documented error given the verdicts of the windows covering its cells."""
    covering = {w["id"]: w for cell in err["cells"] if (w := by_cell.get((err["ss"], err["sheet"], cell)))}
    if not covering:
        return {**err, "status": "not_covered", "window_ids": [], "predicted_type": None, "expected_match": False}
    preds = {wid: verdicts.get(wid) for wid in covering}
    hits = [wid for wid, p in preds.items() if p and p["verdict"] == "error"]
    if hits:
        p = verdicts[hits[0]]
        match = normalise_formula(p.get("expected")) == normalise_formula(err["corrected_formula"])
        return {**err, "status": "found", "window_ids": hits, "predicted_type": p.get("type"),
                "expected_match": match, "reason": p.get("reason", "")}
    status = "unsupported" if all(p and p["verdict"] == "unsupported" for p in preds.values()) else "missed"
    return {**err, "status": status, "window_ids": list(covering), "predicted_type": None, "expected_match": False}


def false_alarms(windows: list[dict], verdicts: dict, errors: list[dict]) -> list[dict]:
    faulty = collections.defaultdict(set)
    for e in errors:
        for cell in e["cells"]:
            faulty[(e["ss"], e["sheet"])].add(cell)
    out = []
    for w in windows:
        p = verdicts.get(w["id"])
        if not p or p["verdict"] != "error":
            continue
        if not set(w["run_cells"]) & faulty[(w["ss"], norm_sheet(w["sheet"]))]:
            out.append({**w, "pred": p})
    return out


def write_report(path: Path, results: list[dict], alarms: list[dict], n_windows: int, n_flagged: int) -> dict:
    counts = collections.Counter(r["status"] for r in results)
    covered = len(results) - counts["not_covered"]
    summary = {"errors": len(results), "covered": covered, "found": counts["found"], "missed": counts["missed"],
               "unsupported": counts["unsupported"], "not_covered": counts["not_covered"],
               "windows": n_windows, "flagged_windows": n_flagged, "false_alarm_windows": len(alarms),
               "recall_covered": round(counts["found"] / covered, 3) if covered else 0.0,
               "recall_all": round(counts["found"] / len(results), 3) if results else 0.0,
               "precision_windows": round((n_flagged - len(alarms)) / n_flagged, 3) if n_flagged else 0.0}
    lines = ["# Held-out evaluation", "", "| metric | value |", "|---|---|"]
    lines += [f"| {k} | {v} |" for k, v in summary.items()]
    lines += ["", "## Documented errors", "", "| err | case | sheet | cells | category | status | predicted type | fix matches | model reason |",
              "|---|---|---|---|---|---|---|---|---|"]
    for r in results:
        cells = ", ".join(sorted(r["cells"]))[:40]
        lines.append(f"| {r['err']} | {r['ss']} | {r['sheet']} | {cells} | {r['info']} | {r['status']} | "
                     f"{r['predicted_type'] or ''} | {'yes' if r['expected_match'] else ''} | {r.get('reason', '')} |")
    by_info = collections.defaultdict(collections.Counter)
    for r in results:
        by_info[r["info"]][r["status"]] += 1
    lines += ["", "## By category", "", "| category | found | missed | unsupported | not covered |", "|---|---|---|---|---|"]
    for info, c in sorted(by_info.items()):
        lines.append(f"| {info} | {c['found']} | {c['missed']} | {c['unsupported']} | {c['not_covered']} |")
    lines += ["", f"## False alarms ({len(alarms)})", "", "| id | formula | type | reason |", "|---|---|---|---|"]
    for a in alarms:
        lines.append(f"| {a['id']} | `{a['formula'][:60]}` | {a['pred'].get('type')} | {a['pred'].get('reason', '')} |")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n")
    return summary


def apply_verifier(windows: list[dict], verdicts: dict[str, dict], xlsx_dir: str, mode: str = "drop_failed",
                   cache_path: str = "") -> dict[str, dict]:
    """Run the verify agent on every flagged window and record the outcome on the verdict. In
    drop_failed mode a contradicted finding is set back to ok; in passed_only mode every finding
    without a supporting check is set back to ok. Outcomes are cached in cache_path so a rerun
    with another mode or threshold does not repeat the recalculations."""
    cache = {}
    if cache_path and Path(cache_path).exists():
        cache = {r["id"]: r["verification"] for r in load_jsonl(cache_path)}
    verifier = Verifier(Recalculator(timeout=120))
    by_case: dict[tuple[int, str], list[dict]] = collections.defaultdict(list)
    for w in windows:
        if verdicts.get(w["id"], {}).get("verdict") == "error":
            by_case[(w["ss"], w["workbook"])].append(w)
    for (ss, name), ws in sorted(by_case.items()):
        path = str(Path(xlsx_dir) / str(ss) / name)
        wb = Workbook(path)
        for w in ws:
            v = verdicts[w["id"]]
            if w["id"] not in cache:
                finding = Finding(w["sheet"], w["addr"], w["formula"], v.get("expected"), v.get("type"), v.get("reason", ""))
                cache[w["id"]] = verifier.verify(wb, path, finding).outcome
            v["verification"] = cache[w["id"]]
            if v["verification"] == "failed" or (mode == "passed_only" and v["verification"] != "passed"):
                v["verdict"] = "ok"
        print(f"verified case {ss}: {len(ws)} flagged", flush=True)
    if cache_path:
        write_jsonl(cache_path, [{"id": k, "verification": o} for k, o in cache.items()])
    return verdicts


def load_review_cache(cache_path: str) -> dict[str, dict]:
    """Cached reviews, leaving out the ones that failed for a technical reason so they are asked again."""
    if not cache_path or not Path(cache_path).exists():
        return {}
    return {r["id"]: r["review"] for r in load_jsonl(cache_path) if not _technical_failure(r["review"])}


def _technical_failure(review: dict) -> bool:
    reason = review.get("reason", "")
    return reason.startswith("reviewer unavailable") or reason == "reviewer reply could not be parsed"


def fetch_reviews(flagged: list[dict], verdicts: dict[str, dict], cache: dict[str, dict], cache_path: str) -> None:
    """Ask the reviewer about every flagged window not yet in the cache. Reviews are requested in
    small chunks and the cache is saved after each chunk, so an interrupted run loses little."""
    todo = [w for w in flagged if w["id"] not in cache]
    reviewer = HostedReviewer()
    if todo and not reviewer.configured:
        sys.exit("set SHEETTRUTH_REVIEWER_BASE_URL, SHEETTRUTH_REVIEWER_MODEL and SHEETTRUTH_REVIEWER_API_KEY")
    items = [{**w, "type": verdicts[w["id"]].get("type"), "expected": verdicts[w["id"]].get("expected"),
              "reason": verdicts[w["id"]].get("reason", "")} for w in todo]
    print(f"reviewer: {len(todo)} windows to review, {len(flagged) - len(todo)} from cache", flush=True)
    for start in range(0, len(todo), REVIEW_CHUNK):
        chunk_windows = todo[start:start + REVIEW_CHUNK]
        for w, review in zip(chunk_windows, reviewer.review(items[start:start + REVIEW_CHUNK])):
            cache[w["id"]] = review.to_dict()
        if cache_path:
            write_jsonl(cache_path, [{"id": k, "review": r} for k, r in cache.items()])
        print(f"reviewer: {start + len(chunk_windows)}/{len(todo)} done", flush=True)


def apply_reviewer(windows: list[dict], verdicts: dict[str, dict], cache_path: str) -> dict[str, dict]:
    """Second opinion on every window still flagged after the code checks. A finding the reviewer
    calls not_error is set back to ok unless a code check supported it (workbook facts outrank the
    reviewer). Reviews are cached so reruns do not repeat the calls."""
    cache = load_review_cache(cache_path)
    flagged = [w for w in windows if verdicts.get(w["id"], {}).get("verdict") == "error"]
    fetch_reviews(flagged, verdicts, cache, cache_path)
    for w in flagged:
        v = verdicts[w["id"]]
        v["review"] = cache[w["id"]]
        if v["review"]["verdict"] == "not_error" and v.get("verification") != "passed":
            v["verdict"] = "ok"
    return verdicts


def write_jsonl(path: str, rows: list[dict]) -> None:
    with open(path, "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--predictions", default="data/test/predictions.jsonl")
    ap.add_argument("--windows", default="data/test/windows.jsonl")
    ap.add_argument("--overview", default="data/test/enron_errors_overview.json")
    ap.add_argument("--out", default="reports/enron_eval.md")
    ap.add_argument("--threshold", type=float, default=0.5, help="flag a window when P(error) is at least this")
    ap.add_argument("--verify", action="store_true", help="run the verify agent on flagged windows")
    ap.add_argument("--verify-mode", choices=["drop_failed", "passed_only"], default="drop_failed")
    ap.add_argument("--verify-cache", default="", help="jsonl of verification outcomes, reused across runs")
    ap.add_argument("--review", action="store_true", help="send the remaining flagged windows to the reviewer model")
    ap.add_argument("--review-cache", default="", help="jsonl of reviewer verdicts, reused across runs")
    ap.add_argument("--xlsx-dir", default="data/test/enron_errors_xlsx")
    ap.add_argument("--ids", default="", help="file with one window id per line; only those windows are scored")
    args = ap.parse_args()

    windows = load_jsonl(args.windows)
    if args.ids:
        wanted = {line.strip() for line in open(args.ids) if line.strip()}
        windows = [w for w in windows if w["id"] in wanted]
    predictions = load_jsonl(args.predictions)
    errors = documented_errors(json.load(open(args.overview)))
    by_cell = index_windows(windows)
    print("threshold sweep (found of covered errors / false-alarm windows):")
    for t in SWEEP:
        v = flagged_at(predictions, t)
        found = sum(judge_error(e, by_cell, v)["status"] == "found" for e in errors)
        print(f"  P(error) >= {t:<5} found {found:>2}  false alarms {len(false_alarms(windows, v, errors)):>4}")
    verdicts = flagged_at(predictions, args.threshold)
    if args.verify:
        verdicts = apply_verifier(windows, verdicts, args.xlsx_dir, args.verify_mode, args.verify_cache)
    if args.review:
        verdicts = apply_reviewer(windows, verdicts, args.review_cache)
    results = [judge_error(e, by_cell, verdicts) for e in errors]
    alarms = false_alarms(windows, verdicts, errors)
    n_flagged = sum(1 for w in windows if verdicts.get(w["id"], {}).get("verdict") == "error")
    summary = write_report(Path(args.out), results, alarms, len(windows), n_flagged)
    summary["threshold"] = args.threshold
    print(json.dumps(summary, indent=1))
    for r in results:
        print(f"err {r['err']:>2} case {r['ss']:>2} {r['status']:<12} {r['info']}")
    print(f"report written to {args.out}")


if __name__ == "__main__":
    main()
