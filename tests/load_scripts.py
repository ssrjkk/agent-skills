"""Load scripts/*.py as modules for in-process testing.

The repo gates live in scripts/ (not an importable package); several are
covered in CI only as subprocesses, which coverage.py cannot see. Loading
them in-process brings the gate logic itself under test and measurement.
"""

from __future__ import annotations

import importlib.util
import itertools
from pathlib import Path
from typing import Any

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"

_counter = itertools.count()


def load_script(name: str) -> Any:
    """Import scripts/<name> under a unique module name (no sys.modules
    registration, so repeated calls re-execute cleanly)."""
    spec = importlib.util.spec_from_file_location(
        f"_gate_script_{next(_counter)}_{name.replace('-', '_').replace('.', '_')}",
        SCRIPTS / name,
    )
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod
