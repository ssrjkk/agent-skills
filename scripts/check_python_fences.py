#!/usr/bin/env python3
"""Validate that every ```python code fence in SKILL.md files is syntactically valid.

Catches typos in skill examples before they ship. Skips blocks that are
intentionally incomplete (contain `...` or pseudo-code).
"""

from __future__ import annotations

import ast
import re
import sys
from pathlib import Path

FENCE = re.compile(r"```python\n(.*?)```", re.DOTALL)
SKIP_MARKERS = ("...", "pass  #", "yield from mock", "return None  #")


def check_block(src: str, path: Path) -> list[str]:
    errors = []
    blocks = FENCE.findall(src)
    for i, block in enumerate(blocks, 1):
        if any(m in block for m in SKIP_MARKERS):
            continue
        try:
            ast.parse(block)
        except SyntaxError as exc:
            errors.append(f"{path}: python block #{i}: {exc}")
    return errors


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    errors: list[str] = []
    for sk in sorted((root / ".claude" / "skills").rglob("SKILL.md")):
        try:
            src = sk.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            errors.append(f"{sk}: cannot read ({exc})")
            continue
        errors.extend(check_block(src, sk))

    if errors:
        print(f"Python fence check failed: {len(errors)} issue(s)")
        for e in errors:
            print(f"  {e}")
        return 1
    print("All python code fences are syntactically valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())