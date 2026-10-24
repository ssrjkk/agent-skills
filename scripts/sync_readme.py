#!/usr/bin/env python3
"""Sync README.md with the skills catalog (source of truth: skills_catalog.json).

Updates: badges (skills/domains counts), Stats table, Skills-by-domain table
(full descriptions, no truncation), Domains inline list, headline counts,
and the IT Roadmaps link. Run `make sync-readme` after adding skills.

`--check` exits 1 when README is stale (CI-friendly, writes nothing).
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "skills_catalog.json"
README = ROOT / "README.md"


def load_catalog() -> dict:
    return json.loads(CATALOG.read_text(encoding="utf-8"))


def table_rows(skills: list[dict]) -> list[str]:
    rows = [
        "| Domain | Skill | Description |",
        "|--------|-------|-------------|",
    ]
    for s in sorted(skills, key=lambda x: (x["category"], x["name"])):
        rows.append(f"| `{s['category']}` | `{s['name']}` | {s['description'].strip()} |")
    return rows


def domains_line(domains: list[str]) -> list[str]:
    parts = [f"`{d}`" for d in sorted(domains)]
    lines, cur = [], ""
    for p in parts:
        piece = ("" if not cur else " · ") + p
        if len(cur) + len(piece) > 76:
            lines.append(cur + " ·")
            cur = p
        else:
            cur += piece
    if cur:
        lines.append(cur)
    return lines


def render(readme: str, data: dict) -> str:
    meta = data["metadata"]
    skills = data["skills"]
    total, total_ru = meta["total_skills"], meta["total_ru"]
    domains = sorted(meta["domains"])

    out = readme
    out = re.sub(r"badge/skills-\d+-blue", f"badge/skills-{total}-blue", out)
    out = re.sub(r"badge/domains-\d+-orange", f"badge/domains-{len(domains)}-orange", out)
    out = re.sub(r"\| Total skills \| \*\*\d+\*\* \|", f"| Total skills | **{total}** |", out)
    out = re.sub(
        r"\| Russian translations \| \*\*\d+ \(\d+%\)\*\* \|",
        f"| Russian translations | **{total_ru} ({round(total_ru / total * 100)}%)** |",
        out,
    )
    out = re.sub(r"\| Domains \| \*\*\d+\*\* \|", f"| Domains | **{len(domains)}** |", out)
    out = re.sub(r"\b100 production-grade\b", f"{total} production-grade", out)
    out = re.sub(r"\b100 hand-reviewed\b", f"{total} hand-reviewed", out)

    lines = out.split("\n")
    try:
        start = next(i for i, ln in enumerate(lines) if ln.strip() == "## Skills by domain")
    except StopIteration:
        print("README: '## Skills by domain' not found", file=sys.stderr)
        return out
    hdr = next(i for i in range(start, len(lines)) if lines[i].startswith("| Domain"))
    end = hdr
    while end + 1 < len(lines) and lines[end + 1].startswith("|"):
        end += 1
    lines[hdr : end + 1] = table_rows(skills)

    try:
        dstart = next(i for i, ln in enumerate(lines) if re.fullmatch(r"## Domains \(\d+\)", ln.strip()))
    except StopIteration:
        dstart = None
    if dstart is not None:
        lines[dstart] = f"## Domains ({len(domains)})"
        dend = dstart + 1
        while dend < len(lines) and lines[dend].startswith("`"):
            dend += 1
        lines[dstart + 1 : dend] = domains_line(domains)

    text = "\n".join(lines)
    rm_link = "- [IT Roadmaps](https://ssrjkk.github.io/agent-skills/roadmaps.html) (every direction, soon)"
    if rm_link not in text:
        text = text.replace(
            "- [Issue Tracker](https://github.com/ssrjkk/agent-skills/issues)",
            "- [Issue Tracker](https://github.com/ssrjkk/agent-skills/issues)\n" + rm_link,
            1,
        )
    return text


def main() -> int:
    data = load_catalog()
    current = README.read_text(encoding="utf-8")
    updated = render(current, data)
    if "--check" in sys.argv:
        if updated != current:
            print("README.md is stale: run `make sync-readme`", file=sys.stderr)
            return 1
        print(f"README in sync: {data['metadata']['total_skills']} skills.")
        return 0
    README.write_text(updated, encoding="utf-8")
    print(f"README synced: {data['metadata']['total_skills']} skills, {len(data['metadata']['domains'])} domains.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
