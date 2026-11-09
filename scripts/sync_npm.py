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
