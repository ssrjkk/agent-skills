#!/usr/bin/env python3
"""Verify skills are consumable by the universal Agent Skills format.

Multiple agents (Claude Code, OpenCode, Cursor, Windsurf, stakpak, tau, etc.)
read the same ``SKILL.md`` file with YAML frontmatter. They are lenient about
unknown fields, but strictly require:

* ``name``   - lowercase words separated by hyphens (regex ``[a-z0-9-]+``)
* ``description`` - a single-line, human-readable summary (in dependencies)

This script enforces those cross-agent invariants plus a few hygiene rules
so every skill in the repo is genuinely portable.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from claude_skills.models import parse_frontmatter

NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]*[a-z0-9]$|^[a-z0-9]$")
DESC_MAX = 1024

MISSING_NAME = "E_ASSET1"
MISSING_DESC = "E_ASSET2"
BAD_NAME = "E_ASSET3"
MULTILINE_DESC = "E_ASSET4"
LONG_DESC = "E_ASSET5"
NO_FM = "E_ASSET6"
BAD_FM = "E_ASSET7"
DUPLICATE_NAME = "E_ASSET8"


def main() -> int:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from _console import ensure_utf8_console
    ensure_utf8_console()
    root = Path(__file__).resolve().parent.parent
    skills_dir = root / ".claude" / "skills"
    errors: list[str] = []
    seen: set[str] = set()

    for sk in sorted(skills_dir.rglob("SKILL.md")):
        name_in_dir = sk.parent.name
        try:
            content = sk.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            errors.append(f"[{NO_FM}] {sk}: cannot read ({exc})")
            continue

        fm, _body, ok = parse_frontmatter(content)
        if not ok or fm is None:
            errors.append(f"[{BAD_FM}] {sk}: malformed or missing frontmatter")
            continue

        name = str(fm.get("name", ""))
        description = str(fm.get("description", ""))

        if not name:
            errors.append(f"[{MISSING_NAME}] {sk}: frontmatter has no 'name'")
        elif name != name_in_dir:
            errors.append(f"[{BAD_NAME}] {sk}: name '{name}' != dir '{name_in_dir}'")
        elif not NAME_RE.match(name):
            errors.append(f"[{BAD_NAME}] {sk}: name '{name}' not portable (lowercase+hyphens)")

        if not description:
            errors.append(f"[{MISSING_DESC}] {sk}: frontmatter has no 'description'")
        if "\n" in description or "\r" in description:
            errors.append(f"[{MULTILINE_DESC}] {sk}: description must be a single line")
        if len(description) > DESC_MAX:
            errors.append(f"[{LONG_DESC}] {sk}: description too long ({len(description)} > {DESC_MAX})")

        if name:
            if name in seen:
                errors.append(f"[{DUPLICATE_NAME}] {sk}: duplicate skill name '{name}'")
            seen.add(name)

    if errors:
        print(f"Agent-interop check failed: {len(errors)} error(s)")
        for e in errors:
            print(f"  {e}")
        return 1

    print(f"All {len(seen)} skills are portable (universal Agent Skills format).")
    return 0


if __name__ == "__main__":
    sys.exit(main())