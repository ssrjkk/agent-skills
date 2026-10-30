"""Tests for UTF-8 console hardening.

Regression cover: on Windows (cp1251) or C-locale VMs/containers, printing
a Cyrillic skill name, description or path used to raise UnicodeEncodeError.
"""

from __future__ import annotations

import io
import sys
from pathlib import Path
from typing import Any

from click.testing import CliRunner

from claude_skills import ensure_utf8_console
from claude_skills.cli import cli


def _make_skill(root: Path, name: str, category: str, description: str) -> Path:
    skill_dir = root / ".claude" / "skills" / category / name
    skill_dir.mkdir(parents=True)
    body = (
        "---\n"
        f"name: {name}\n"
        f"description: {description}\n"
        f"category: {category}\n"
        "tags: [testing]\n"
        "models: [sonnet]\n"
        "version: 1.0.0\n"
        "created: 2026-09-01\n"
        "updated: 2026-09-28\n"
        "---\n# Skill\n"
        "## Quick Start\n```python\nprint('hi')\n```\n"
        "## When to Use\n- when needed\n"
        "## Step-by-Step\n1. do it\n"
        "## Examples\n```python\nx = 1\n```\n"
        "## Validation\nrun tests\n"
    )
    (skill_dir / "SKILL.md").write_text(body, encoding="utf-8")
    return skill_dir


def test_ensure_utf8_console_reconfigures_ascii_stream():
    buf = io.BytesIO()
    wrapper = io.TextIOWrapper(buf, encoding="ascii")
    old, sys.stdout = sys.stdout, wrapper
    try:
        ensure_utf8_console()
        assert sys.stdout.encoding == "utf-8"
    finally:
        sys.stdout = old


def test_ensure_utf8_console_never_raises(capsys):
    with capsys.disabled():
        ensure_utf8_console()


def test_ensure_utf8_console_skips_plain_objects():
    class Plain:
        pass

    import sys

    old = sys.stdout
    sys.stdout = Plain()
    try:
        ensure_utf8_console()
    finally:
        sys.stdout = old


def test_ensure_utf8_console_tolerates_broken_streams():
    class Broken(io.TextIOWrapper):
        def reconfigure(self, *_args: Any, **_kwargs: Any) -> None:
            raise OSError("frozen stream")

    import sys

    buf = io.BytesIO()
    old, sys.stdout = sys.stdout, Broken(buf)
    try:
        ensure_utf8_console()
    finally:
        sys.stdout = old


def test_search_prints_cyrillic_description(tmp_path: Path):
    _make_skill(tmp_path, "console-test", "qa", "Тестовая проверка консоли и кириллицы")
    result = CliRunner().invoke(
        cli, ["search", "тест", "--dir", str(tmp_path / ".claude" / "skills")]
    )
    assert result.exit_code == 0
    assert "Тестовая" in result.output
