"""Convert every .xls under RAW_DIR to .xlsx under XLSX_DIR, in parallel, keeping relative paths.

Skips files already converted. Logs failures to XLSX_DIR/convert_failures.txt.
Works on Linux, macOS and Windows as long as LibreOffice (soffice) is installed.

Usage:
  python scripts/convert_corpus.py data/raw/enron data/xlsx/enron --workers 4
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


def find_soffice() -> str:
    for name in ("soffice", "libreoffice", "soffice.exe"):
        p = shutil.which(name)
        if p:
            return p
    for p in (r"C:\Program Files\LibreOffice\program\soffice.exe",
              "/Applications/LibreOffice.app/Contents/MacOS/soffice"):
        if Path(p).exists():
            return p
    sys.exit("LibreOffice not found. Install it and make sure 'soffice' is on PATH.")


def convert_one(soffice: str, src: Path, dst_dir: Path, timeout: int) -> tuple[Path, bool, str]:
    dst_dir.mkdir(parents=True, exist_ok=True)
    out = dst_dir / (src.stem + ".xlsx")
    if out.exists():
        return src, True, "exists"
    # each worker gets its own profile dir, otherwise parallel soffice calls fight over the lock
    with tempfile.TemporaryDirectory() as prof:
        cmd = [soffice, f"-env:UserInstallation=file://{prof}", "--headless", "--norestore",
               "--convert-to", "xlsx", "--outdir", str(dst_dir), str(src)]
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            return src, False, "timeout"
    if out.exists():
        return src, True, "ok"
    return src, False, (r.stderr or r.stdout or "no output").strip()[:200]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("raw_dir")
    ap.add_argument("xlsx_dir")
    ap.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2) // 2))
    ap.add_argument("--timeout", type=int, default=120)
    ap.add_argument("--limit", type=int, default=0, help="convert only the first N files (for a quick test)")
    a = ap.parse_args()

    soffice = find_soffice()
    raw, out = Path(a.raw_dir), Path(a.xlsx_dir)
    files = sorted(p for p in raw.rglob("*") if p.suffix.lower() in (".xls", ".xlsx", ".xlsm"))
    if a.limit:
        files = files[: a.limit]
    print(f"{len(files)} files, {a.workers} workers")
    fails = []
    done = 0
    with ThreadPoolExecutor(a.workers) as ex:
        futs = {ex.submit(convert_one, soffice, p, out / p.parent.relative_to(raw), a.timeout): p for p in files}
        for f in as_completed(futs):
            src, ok, msg = f.result()
            done += 1
            if not ok:
                fails.append(f"{src}\t{msg}")
            if done % 100 == 0:
                print(f"{done}/{len(files)} done, {len(fails)} failed")
    out.mkdir(parents=True, exist_ok=True)
    (out / "convert_failures.txt").write_text("\n".join(fails))
    print(f"finished: {done - len(fails)} ok, {len(fails)} failed. Failures listed in {out / 'convert_failures.txt'}")


if __name__ == "__main__":
    main()
