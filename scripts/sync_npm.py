"""Sync the npm catalog snapshot with the freshly generated skills_catalog.json.

The npm tarball ships skills_catalog.json for the Node API; without this
sync the published snapshot drifts behind the real catalog.

Usage:
    python scripts/sync_npm.py            # copy the fresh catalog into npm/
    python scripts/sync_npm.py --check    # CI mode: exit 1 when stale
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    src = ROOT / "skills_catalog.json"
    dst = ROOT / "npm" / "skills_catalog.json"
    if "--check" in sys.argv:
        if not src.exists():
            print("skills_catalog.json missing — run `make catalog` first", file=sys.stderr)
            return 1
        if not dst.exists():
            print("npm/skills_catalog.json missing: run `make sync-npm`", file=sys.stderr)
            return 1
        # semantic comparison: generated_at changes on every rebuild and must
        # not fail the check; real drift (skills added/removed/edited) must.
        def semantic(path: Path) -> dict:
            data = json.loads(path.read_text(encoding="utf-8"))
            data.get("metadata", {}).pop("generated_at", None)
            return data

        if semantic(src) != semantic(dst):
            print("npm/skills_catalog.json is stale: run `make sync-npm`", file=sys.stderr)
            new_data, old_data = semantic(src), semantic(dst)
            shown = 0

            def walk(x, y, path="") -> None:
                nonlocal shown
                if shown >= 5 or x == y:
                    return
                if type(x) is not type(y):
                    print(f"  {path}: {x!r} != {y!r}"[:200], file=sys.stderr)
                    shown += 1
                    return
                if isinstance(x, dict):
                    for k in sorted(set(x) | set(y)):
                        walk(x.get(k), y.get(k), f"{path}.{k}")
                elif isinstance(x, list):
                    for i in range(max(len(x), len(y))):
                        walk(x[i] if i < len(x) else None, y[i] if i < len(y) else None, f"{path}[{i}]")
                elif x != y:
                    print(f"  {path}: {x!r} != {y!r}"[:200], file=sys.stderr)
                    shown += 1

            walk(new_data, old_data)
            return 1
        print("npm catalog snapshot in sync.")
        return 0
    if not src.exists():
        print("skills_catalog.json missing — run `make catalog` first", file=sys.stderr)
        return 1
    shutil.copyfile(src, dst)
    print(f"Catalog copied to {dst}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
