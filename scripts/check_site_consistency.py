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
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from _console import ensure_utf8_console
    ensure_utf8_console()
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

    # 2b. roadmaps: source files <-> generated pages (independent from skills)
    rm_src = root / "roadmaps"
    rm_required = {"slug", "name", "icon", "tagline", "status", "eta", "stages"}
    rm_slugs: set[str] = set()
    if not rm_src.is_dir():
        errors.append("roadmaps/ source directory missing")
    else:
        for path in sorted(rm_src.glob("*.json")):
            try:
                track = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as e:
                errors.append(f"roadmaps/{path.name} unreadable: {e}")
                continue
            missing_keys = rm_required - set(track)
            if missing_keys:
                errors.append(f"roadmaps/{path.name} missing keys: {sorted(missing_keys)}")
            if track.get("slug") != path.stem:
                errors.append(f"roadmaps/{path.name} slug mismatch: {track.get('slug')!r}")
            if track.get("status") not in {"soon", "live"}:
                errors.append(f"roadmaps/{path.name} bad status: {track.get('status')!r}")
            rm_slugs.add(path.stem)
            if not (docs / "roadmaps" / f"{path.stem}.html").exists():
                errors.append(f"missing roadmap page: {path.stem}")
        if not (docs / "roadmaps.html").exists():
            errors.append("missing roadmaps.html overview")
        compiled = docs / "roadmaps.json"
        if not compiled.exists():
            errors.append("roadmaps.json missing from docs")
        else:
            try:
                compiled_slugs = {t["slug"] for t in json.loads(compiled.read_text(encoding="utf-8"))["tracks"]}
                if compiled_slugs != rm_slugs:
                    errors.append(f"roadmaps.json out of sync: {sorted(rm_slugs - compiled_slugs)[:5]} missing")
            except (OSError, json.JSONDecodeError, KeyError) as e:
                errors.append(f"roadmaps.json invalid: {e}")

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
        if page.parent == docs:
            expect_css = "style.css"
            expect_js = 'src="site.js"'
        else:
            expect_css = "../style.css"
            expect_js = 'src="../site.js"'
        if f'href="{expect_css}"' not in html:
            errors.append(f"{page.name} -> wrong css path (expected {expect_css})")
        if expect_js not in html:
            errors.append(f"{page.name} -> missing shared script ({expect_js})")

        # 5. div balance
        if html.count("<div") != html.count("</div>"):
            errors.append(f"{page.name} -> unbalanced <div> tags")

    # 6. shared script in sync with source
    site_built = docs / "site.js"
    site_src = root / "assets" / "site.js"
    if not site_built.exists():
        errors.append("docs/site.js missing (run make docs)")
    elif not site_src.exists():
        errors.append("assets/site.js source missing")
    elif site_built.read_text(encoding="utf-8") != site_src.read_text(encoding="utf-8"):
        errors.append("docs/site.js differs from assets/site.js (run make docs)")

    if errors:
        print(f"Site consistency check failed: {len(errors)} issue(s)")
        for e in errors[:25]:
            print(f"  {e}")
        return 1
    print(f"Site consistent: {len(names)} skills, {len(domains)} domains, {len(rm_slugs)} roadmaps, all pages valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())