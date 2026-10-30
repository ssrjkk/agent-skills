"""Shared console helper for scripts/ (stdlib only, no package dependency).

Every script entrypoint should call ``ensure_utf8_console()`` first so
non-ASCII skill names, descriptions and paths never crash on Windows
(cp1251 consoles) or C-locale containers/VMs.
"""

from __future__ import annotations

import contextlib
import sys


def ensure_utf8_console() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if not callable(reconfigure):
            continue
        with contextlib.suppress(OSError, ValueError):
            reconfigure(encoding="utf-8")
