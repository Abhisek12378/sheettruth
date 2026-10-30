"""Render the context window for every formula error in the Enron Errors Corpus next to the known fix.

Usage:
  python scripts/audit_windows.py data/test/enron_errors_overview.json data/test/enron_errors_xlsx reports/window_audit.md
"""
from __future__ import annotations

import json
import re
import sys
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from openpyxl.utils import get_column_letter, range_boundaries  # noqa: E402

from sheettruth.windows.builder import build_window  # noqa: E402
from sheettruth.windows.cellinfo import Workbook, build_context  # noqa: E402


def first_cell(cells: str) -> str:
    part = str(cells).split(";")[0].replace("etc.", "").strip()
    if ":" in part:
        c1, r1, _, _ = range_boundaries(part)
        return f"{get_column_letter(c1)}{r1}"
    return part


def main(overview, xlsx_root, out_md):
    errors = json.loads(Path(overview).read_text())
    xlsx_root = Path(xlsx_root)
    lines = ["# Window audit on the Enron Errors Corpus\n",
             "For each formula error: the corpus fix, then the window the model would see. ",
             "Question for the reader: can you see the fix from the window alone?\n"]
    stats = {"rendered": 0, "skipped": 0, "over_budget": 0}
    for e in errors:
        if e["cell_type"] != "Formula" or not e["faulty_file"]:
            stats["skipped"] += 1
            continue
        path = xlsx_root / str(e["ss"]) / (Path(e["faulty_file"]).stem + ".xlsx")
        sheet = str(e["faulty_sheet"]).split(",")[0].strip()
        addr = first_cell(e["faulty_cells"])
        lines.append(f"\n## Error {e['err']}: {e['faulty_file']} / {sheet}!{e['faulty_cells']}\n")
        lines.append(f"- corpus type: {e['type']} / {e['subtype'] or ''} / {e['info']}")
        lines.append(f"- faulty formula: `{e['faulty'].get('formula', '')}`")
        lines.append(f"- corpus fix: `{e['corrected'].get('formula', '') or '(unfixed by authors)'}`\n")
        try:
            wb = Workbook(str(path))
            ctx = build_context(wb, sheet, addr)
            if ctx is None:
                lines.append("_target cell has no formula or sheet not found_\n")
                stats["skipped"] += 1
                continue
            w = build_window(ctx)
        except Exception as ex:
            lines.append(f"_failed: {ex}_\n")
            stats["skipped"] += 1
            continue
        stats["rendered"] += 1
        if w.truncated:
            stats["over_budget"] += 1
        lines.append(f"tokens~{w.tokens} truncated={w.truncated} unsupported={w.unsupported_reason}\n")
        lines.append("```\n" + w.text + "\n```\n")
    lines.insert(3, f"\nRendered {stats['rendered']}, skipped {stats['skipped']}, over budget {stats['over_budget']}.\n")
    Path(out_md).parent.mkdir(parents=True, exist_ok=True)
    Path(out_md).write_text("\n".join(lines))
    print(stats)


if __name__ == "__main__":
    main(*sys.argv[1:4])
