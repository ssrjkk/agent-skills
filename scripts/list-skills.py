#!/usr/bin/env python3
"""List all skills from the catalog organized by domain."""

import json
import sys
from collections import defaultdict
from pathlib import Path


def main() -> int:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from _console import ensure_utf8_console
    ensure_utf8_console()
    catalog_path = Path("skills_catalog.json")
    if not catalog_path.exists():
        print("skills_catalog.json not found. Run `make catalog` first.", file=sys.stderr)
        return 1

    with open(catalog_path, encoding="utf-8") as f:
        data = json.load(f)

    by_domain = defaultdict(list)
    for s in data["skills"]:
        by_domain[s["category"]].append(s["name"])

    total = data["metadata"]["total_skills"]
    total_ru = data["metadata"]["total_ru"]
    domains = len(by_domain)

    print(f"Total: {total} skills, {total_ru} RU, {domains} domains")
    for d in sorted(by_domain):
        names = by_domain[d]
        ru = sum(1 for s in data["skills"] if s["category"] == d and s.get("has_ru"))
        print(f"\n  {d} ({len(names)} skills, {ru} RU):")
        for n in sorted(names):
            print(f"    - {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
