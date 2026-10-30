#!/usr/bin/env python3
"""Audit top skills: check real quality, working examples, usefulness."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

from claude_skills.models import QualityScore, SkillFile
from claude_skills.quality import QualityAnalyzer


def audit_skill(skill_path: Path) -> dict:
    """Audit a single skill: returns score 0-100 with details."""
    sk_file = SkillFile(en_path=skill_path)

    try:
        content = skill_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return {"score": 0, "errors": ["Cannot read file"]}

    sk_file.en_content = content

    # Parse frontmatter
    if not content.startswith("---"):
        return {"score": 0, "errors": ["Missing frontmatter"]}
    end = content.find("---", 3)
    if end < 0:
        return {"score": 0, "errors": ["Malformed frontmatter"]}
    try:
        fm = yaml.safe_load(content[3:end].strip()) or {}
    except yaml.YAMLError:
        return {"score": 0, "errors": ["YAML parse error"]}

    sk_file.en_frontmatter = fm
    sk_file.en_body = content[end + 3 :].strip()
    body = sk_file.en_body
    errors: list[str] = []
    warnings: list[str] = []
    score = 0

    # 1. Frontmatter completeness (20 pts)
    required = {"name", "description", "category", "tags", "models", "version"}
    present = {k for k in required if k in fm}
    score += 20 * len(present) / len(required)
    if missing := required - present:
        errors.append(f"Missing frontmatter: {missing}")

    # 2. Description quality (10 pts)
    desc = (fm.get("description", "") or "").strip()
    if len(desc) > 50:
        score += 10
    elif len(desc) > 20:
        score += 5
    else:
        warnings.append("Description too short")

    # 3. Body depth (20 pts)
    body_lines = body.strip().split("\n") if body else []
    if len(body_lines) >= 50:
        score += 20
    elif len(body_lines) >= 30:
        score += 15
    elif len(body_lines) >= 15:
        score += 8
    else:
        warnings.append(f"Body too short ({len(body_lines)} lines)")

    # 4. Code examples (20 pts)
    fence_count = body.count("```")
    if fence_count >= 4:
        score += 20
    elif fence_count >= 2:
        score += 12
    elif fence_count > 0:
        score += 5
    else:
        warnings.append("No code examples")

    # 5. Required sections (20 pts)
    sections = ["Quick Start", "When to Use", "Step-by-Step", "Examples", "Validation", "Dependencies"]
    found_sections = [s for s in sections if s in body or f" {s}" in body or f" {s}" in body]
    score += 20 * len(found_sections) / len(sections)
    if len(found_sections) < 3:
        warnings.append(f"Only {len(found_sections)}/{len(sections)} sections found")

    # 6. Bilingual (10 pts)
    ru_path = skill_path.parent / "SKILL.ru.md"
    if ru_path.exists():
        ru_content = ru_path.read_text(encoding="utf-8")
        ru_body = ""
        end_ru = ru_content.find("---", 3)
        if end_ru > 0:
            ru_body = ru_content[end_ru + 3 :].strip()
        if len(ru_body) > 100:
            score += 10
        elif len(ru_body) > 30:
            score += 5
        else:
            warnings.append("RU translation is a stub")
    else:
        warnings.append("Missing RU translation")

    return {"score": round(score, 1), "errors": errors, "warnings": warnings, "sections_found": len(found_sections)}


def audit_quality_score(skill_path: Path) -> QualityScore:
    """Get SDK quality score for a skill."""
    analyzer = QualityAnalyzer()
    content = skill_path.read_text(encoding="utf-8")
    sf = SkillFile(en_path=skill_path, en_content=content)
    end = content.find("---", 3)
    if end > 0:
        try:
            sf.en_frontmatter = yaml.safe_load(content[3:end].strip()) or {}
        except yaml.YAMLError:
            sf.en_frontmatter = {}
        sf.en_body = content[end + 3 :].strip()
    ru = skill_path.parent / "SKILL.ru.md"
    if ru.exists():
        sf.ru_path = ru
        sf.ru_content = ru.read_text(encoding="utf-8")
    return analyzer.analyze(sf)


def main() -> int:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from _console import ensure_utf8_console
    ensure_utf8_console()
    parser = argparse.ArgumentParser(description="Audit skill quality")
    parser.add_argument("--dir", default=".claude/skills", help="Skills directory")
    parser.add_argument("--top", type=int, default=50, help="Number of skills to audit")
    parser.add_argument("--json", help="Output JSON report")
    parser.add_argument("--csv", help="Output CSV report")
    args = parser.parse_args()

    skills_dir = Path(args.dir)
    all_skills = sorted(skills_dir.rglob("SKILL.md"))
    total = len(all_skills)

    results = []
    for sk_path in all_skills[: args.top]:
        name = sk_path.parent.name
        audit = audit_skill(sk_path)
        qs = audit_quality_score(sk_path)
        results.append({
            "name": name,
            "category": sk_path.parent.parent.name,
            "audit_score": audit["score"],
            "quality_overall": round(qs.overall, 1),
            "quality_grade": qs.grade,
            "sections": audit["sections_found"],
            "errors": audit["errors"],
            "warnings": audit["warnings"],
        })

    # Summary
    avg_audit = sum(r["audit_score"] for r in results) / len(results) if results else 0
    avg_quality = sum(r["quality_overall"] for r in results) / len(results) if results else 0
    grades = {}
    for r in results:
        grades[r["quality_grade"]] = grades.get(r["quality_grade"], 0) + 1

    print(f"=== AUDIT REPORT: Top {len(results)} of {total} skills ===")
    print(f"Average audit score:  {avg_audit:.1f}/100")
    print(f"Average quality:      {avg_quality:.1f}%")
    print(f"Grade distribution:   {dict(sorted(grades.items()))}")

    print("\nTop 10 skills:")
    for r in sorted(results, key=lambda x: x["audit_score"], reverse=True)[:10]:
        err = f" ({len(r['errors'])} errors)" if r["errors"] else ""
        warn = f" ({len(r['warnings'])} warnings)" if r["warnings"] else ""
        print(f"  {r['name']:35s} {r['audit_score']:5.1f} ({r['quality_grade']}){err}{warn}")

    print("\nBottom 5 skills:")
    for r in sorted(results, key=lambda x: x["audit_score"])[:5]:
        print(f"  {r['name']:35s} {r['audit_score']:5.1f} ({r['quality_grade']})")
        for e in r["errors"]:
            print(f"    ERROR: {e}")
        for w in r["warnings"]:
            print(f"    WARN:  {w}")

    if args.json:
        Path(args.json).write_text(
            json.dumps({"total": total, "audited": len(results), "avg_audit_score": avg_audit,
                        "results": results}, indent=2),
            encoding="utf-8",
        )
        print(f"\nReport saved to {args.json}")

    if args.csv:
        import csv
        with open(args.csv, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["name", "category", "audit_score", "quality_overall",
                                               "quality_grade", "sections", "errors", "warnings"])
            w.writeheader()
            for r in results:
                r["errors"] = "; ".join(r["errors"])
                r["warnings"] = "; ".join(r["warnings"])
                w.writerow(r)
        print(f"CSV saved to {args.csv}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
