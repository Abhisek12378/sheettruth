"""Recalculate every formula in an .xlsx with LibreOffice, in place.

Why this exists: after we inject an error, the cached values in the file still reflect the
original formula. If the model saw those, it would learn "value disagrees with formula", a signal
that never exists in a real broken sheet. So every corrupted copy is recalculated before its
window is built. If LibreOffice cannot do it, the caller strips cached values instead.

Approach (same as the openpyxl community recalc scripts): install a tiny Basic macro into a
private LibreOffice profile once, then run soffice headless with that macro on each file.
"""
from __future__ import annotations

import os
import platform
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Optional

MACRO = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE script:module PUBLIC "-//OpenOffice.org//DTD OfficeDocument 1.0//EN" "module.dtd">
<script:module xmlns:script="http://openoffice.org/2000/script" script:name="Module1" script:language="StarBasic">
    Sub RecalculateAndSave()
      ThisComponent.calculateAll()
      ThisComponent.store()
      ThisComponent.close(True)
    End Sub
</script:module>"""


def find_soffice() -> Optional[str]:
    for name in ("soffice", "libreoffice", "soffice.exe"):
        p = shutil.which(name)
        if p:
            return p
    for p in (r"C:\Program Files\LibreOffice\program\soffice.exe",
              "/Applications/LibreOffice.app/Contents/MacOS/soffice"):
        if Path(p).exists():
            return p
    return None


class Recalculator:
    """One instance per worker process. Creates its own LibreOffice profile with the macro installed."""

    def __init__(self, timeout: int = 120):
        self.soffice = find_soffice()
        self.timeout = timeout
        self._tmp = tempfile.TemporaryDirectory(prefix="st-lo-profile-")
        self.profile = Path(self._tmp.name)
        self.ready = False
        if self.soffice:
            self.ready = self._install_macro()

    def _env(self) -> dict:
        """Environment for headless runs: the plain (svp) backend needs no display server."""
        env = os.environ.copy()
        env["SAL_USE_VCLPLUGIN"] = "svp"
        return env

    def _install_macro(self) -> bool:
        url = self.profile.as_uri()
        try:
            subprocess.run([self.soffice, "--headless", "--terminate_after_init", f"-env:UserInstallation={url}"],
                           capture_output=True, timeout=60, env=self._env())
        except Exception:
            return False
        macro_dir = self.profile / "user" / "basic" / "Standard"
        if not macro_dir.exists():
            return False
        (macro_dir / "Module1.xba").write_text(MACRO)
        return True

    def recalc(self, xlsx_path: str) -> tuple[bool, str]:
        """Recalculate in place. Returns (ok, message)."""
        if not self.ready:
            return False, "libreoffice_unavailable"
        p = Path(xlsx_path).resolve()
        before = (p.stat().st_mtime_ns, p.stat().st_size)
        cmd = [self.soffice, "--headless", "--norestore", f"-env:UserInstallation={self.profile.as_uri()}",
               "vnd.sun.star.script:Standard.Module1.RecalculateAndSave?language=Basic&location=application", str(p)]
        if platform.system() == "Linux" and shutil.which("timeout"):
            cmd = ["timeout", str(self.timeout)] + cmd
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=self.timeout + 15, env=self._env())
        except subprocess.TimeoutExpired:
            return False, "timeout"
        if r.returncode not in (0,):
            return False, f"soffice_exit_{r.returncode}"
        after = (p.stat().st_mtime_ns, p.stat().st_size)
        if after == before:
            return False, "file_not_rewritten"
        return True, "ok"
