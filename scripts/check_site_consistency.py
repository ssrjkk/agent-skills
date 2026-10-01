#!/usr/bin/env python3
"""Verify the generated docs site is consistent and self-contained.

Checks:
  1. search-index.json has an entry for every skill in the catalog.
  2. Every skill and domain has a generated HTML page.
  3. Every internal relative link resolves to an existing file.
  4. CSS paths are correct for each page depth (index vs subpages).
  5. Div tags are balanced (no broken layout from unclosed elements).
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    docs = root / "docs"
    errors: list[str] = []

    catalog = json.loads((root / "skills_catalog.json").read_text(encoding="utf-8"))
    skills = catalog["skills"]
    names = {s["name"] for s in skills}
    domains = set(catalog["metadata"]["domains"])

    # 1. search-index consistency
    idx_path = docs / "search-index.json"
    if not idx_path.exists():
        errors.append("search-index.json missing")
    else:
        idx = json.loads(idx_path.read_text(encoding="utf-8"))
        idx_names = {e["name"] for e in idx}
        missing = names - idx_names
        extra = idx_names - names
        if missing:
            errors.append(f"search-index missing skills: {sorted(missing)[:5]}")
        if extra:
            errors.append(f"search-index has unknown skills: {sorted(extra)[:5]}")

    # 2. every skill/domain has a page
    for name in names:
        if not (docs / "skills" / f"{name}.html").exists():
            errors.append(f"missing skill page: {name}")
    for d in domains:
        if not (docs / "domains" / f"{d}.html").exists():
            errors.append(f"missing domain page: {d}")

    # 3. relative links resolve
    for page in list(docs.rglob("*.html")):
        html = page.read_text(encoding="utf-8")
        for m in re.finditer(r'href="([^"]+\.html)"', html):
            href = m.group(1)
            if href.startswith(("http", "//", "#")):
                continue
            target = (page.parent / href).resolve()
            if not target.exists():
                errors.append(f"{page.name} -> broken link: {href}")

        # 4. css path correct
        if page.name == "index.html":
            expect_css = "style.css"
        else:
            expect_css = "../style.css"
        if f'href="{expect_css}"' not in html:
            errors.append(f"{page.name} -> wrong css path (expected {expect_css})")

        # 5. div balance
        if html.count("<div") != html.count("</div>"):
            errors.append(f"{page.name} -> unbalanced <div> tags")

    if errors:
        print(f"Site consistency check failed: {len(errors)} issue(s)")
        for e in errors[:25]:
            print(f"  {e}")
        return 1
    print(f"Site consistent: {len(names)} skills, {len(domains)} domains, all pages valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())