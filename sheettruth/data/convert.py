"""Convert a legacy .xls workbook to .xlsx with LibreOffice, keeping its formulas.

The audit pipeline reads .xlsx only. Uploads in the old binary format are converted once on
arrival; the converted copy is what gets audited and corrected. LibreOffice is the same engine
used for recalculation, so a server that can recalculate can also convert.
"""
from __future__ import annotations

import os
import platform
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Optional

from sheettruth.data.recalc import find_soffice

CONVERTIBLE_SUFFIXES = (".xls",)


def conversion_available() -> bool:
    return find_soffice() is not None


def _env() -> dict:
    env = os.environ.copy()
    env["SAL_USE_VCLPLUGIN"] = "svp"
    return env


def convert_workbook(src: Path, target_format: str = "xlsx", timeout: int = 120,
                     soffice: Optional[str] = None) -> Path:
    """Write src next to itself in target_format and return the new path. Raises RuntimeError
    with a short reason when LibreOffice is missing, fails or produces nothing."""
    binary = soffice or find_soffice()
    if binary is None:
        raise RuntimeError("libreoffice_unavailable")
    src = Path(src).resolve()
    out_dir = src.parent
    with tempfile.TemporaryDirectory(prefix="st-lo-convert-") as profile:
        cmd = [binary, "--headless", "--norestore", f"-env:UserInstallation={Path(profile).as_uri()}",
               "--convert-to", target_format, "--outdir", str(out_dir), str(src)]
        if platform.system() == "Linux" and shutil.which("timeout"):
            cmd = ["timeout", str(timeout)] + cmd
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 15, env=_env())
        except subprocess.TimeoutExpired as exc:
            raise RuntimeError("timeout") from exc
    out = out_dir / f"{src.stem}.{target_format}"
    if result.returncode != 0 or not out.exists():
        raise RuntimeError(f"soffice_exit_{result.returncode}")
    return out


def xls_to_xlsx(data: bytes, filename: str, timeout: int = 120) -> tuple[bytes, str]:
    """Convert the bytes of an .xls upload. Returns the .xlsx bytes and the new file name."""
    with tempfile.TemporaryDirectory(prefix="st-xls-") as folder:
        src = Path(folder) / Path(filename).name
        src.write_bytes(data)
        out = convert_workbook(src, "xlsx", timeout)
        return out.read_bytes(), out.name
