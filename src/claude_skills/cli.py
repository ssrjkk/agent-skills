#!/usr/bin/env python3
"""Claude Skills Library CLI - validate, analyze, and manage skills.

The same ``SKILL.md`` format works across AI agents (Claude Code, OpenCode,
Cursor, Windsurf, etc.) thanks to the universal Agent Skills file layout.
"""

from __future__ import annotations

import json as json_lib
import time
from pathlib import Path

import click
from colorama import Fore, Style  # type: ignore[import-untyped]

from claude_skills.catalog import CatalogBuilder
from claude_skills.models import QualityScore, SkillFile, parse_frontmatter
from claude_skills.quality import QualityAnalyzer, QualityReport
from claude_skills.validator import ValidationPipeline

DEFAULT_SKILLS = ".claude/skills"


def resolve_skills_dir(dir_value: str | None) -> str:
    if dir_value is None:
        return DEFAULT_SKILLS
    path = Path(dir_value)
    if not path.is_dir():
        raise click.ClickException(f"Skills directory not found: {path}")
    return str(path)


@click.group()
def cli():
    """Claude Skills Library CLI v3.4.0 - Production Ready."""


@cli.command()
@click.option('--dir', type=click.Path(), default=None, help=f'Skills dir (default: {DEFAULT_SKILLS})')
@click.option('--json', type=click.Path(), help='Output JSON report')
def stats(dir: str | None, json: str | None):
    """Show library statistics."""
    start = time.perf_counter()

    builder = CatalogBuilder(base=resolve_skills_dir(dir))
    catalog = builder.build_catalog()

    print(f"\n{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Claude Skills Library - Statistics{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}\n")

    print(f"  Total skills: {Fore.YELLOW}{catalog.metadata.total_skills}{Style.RESET_ALL}")
    print(f"  Bilingual coverage: {Fore.YELLOW}{catalog.metadata.total_ru}/{catalog.metadata.total_skills}{Style.RESET_ALL}")
    print(f"  Domains: {Fore.YELLOW}{len(catalog.metadata.domains)}{Style.RESET_ALL}")
    print(f"  Schema version: {Fore.YELLOW}v{catalog.metadata.schema_version}{Style.RESET_ALL}")

    duration = time.perf_counter() - start
    print(f"\n    Completed in {Fore.CYAN}{duration:.2f}s{Style.RESET_ALL}\n")

    if json:
        report = {
            "total_skills": catalog.metadata.total_skills,
            "total_ru": catalog.metadata.total_ru,
            "domains": catalog.metadata.domains,
            "schema_version": catalog.metadata.schema_version,
        }
        Path(json).write_text(json_lib.dumps(report, indent=2), encoding="utf-8")
        print(f"   Report saved to {Fore.CYAN}{json}{Style.RESET_ALL}\n")


@cli.command()
@click.option('--dir', type=click.Path(), default=None, help=f'Skills dir (default: {DEFAULT_SKILLS})')
@click.option('--json', type=click.Path(), help='Output JSON report')
def validate(dir: str | None, json: str | None):
    """Validate all skills (EN + RU)."""
    start = time.perf_counter()

    skills_dir = resolve_skills_dir(dir)
    pipeline = ValidationPipeline(Path(skills_dir))
    en_results = pipeline.run_all()
    ru_results = pipeline.run_ru_all()

    combined: dict[str, list] = {}
    for name, results in en_results.items():
        combined[name] = list(results)
    for name, results in ru_results.items():
        combined.setdefault(name, []).extend(results)

    report = pipeline.report(combined)

    print(f"\n{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Validation Report{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}\n")

    print(f"  Total skills: {Fore.YELLOW}{report['total']}{Style.RESET_ALL}")
    print(f"  {Fore.RED}Errors: {report['errors']}{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}Warnings: {report['warnings']}{Style.RESET_ALL}")
    print(f"  {Fore.BLUE}Info: {report['info']}{Style.RESET_ALL}")

    if report['error_details']:
        print(f"\n  {Fore.RED}Top errors:{Style.RESET_ALL}")
        for error in report['error_details'][:5]:
            print(f"    {error}")

    duration = time.perf_counter() - start
    print(f"\n    Completed in {Fore.CYAN}{duration:.2f}s{Style.RESET_ALL}\n")

    if json:
        Path(json).write_text(json_lib.dumps(report, indent=2), encoding="utf-8")
        print(f"   Report saved to {Fore.CYAN}{json}{Style.RESET_ALL}\n")


@cli.command()
@click.option('--dir', type=click.Path(), default=None, help=f'Skills dir (default: {DEFAULT_SKILLS})')
@click.option('--json', type=click.Path(), help='Output JSON report')
@click.option('--top', type=int, default=10, help='Show top N skills')
def quality(dir: str | None, json: str | None, top: int):
    """Analyze quality of all skills."""
    start = time.perf_counter()

    builder = CatalogBuilder(base=resolve_skills_dir(dir))
    catalog = builder.build_catalog()
    analyzer = QualityAnalyzer()

    scores: dict[str, QualityScore] = {}
    skills_detail: list[dict] = []
    for skill in catalog.skills:
        en_path = skill.path
        ru_path = en_path.parent / "SKILL.ru.md"
        en_raw = en_path.read_text(encoding="utf-8")
        ru_raw = ru_path.read_text(encoding="utf-8") if ru_path.exists() else ""

        fm_en, body_en, ok_en = parse_frontmatter(en_raw)
        fm_ru, body_ru, _ = parse_frontmatter(ru_raw)
        if not ok_en:
            continue

        sf = SkillFile(
            en_path=en_path,
            ru_path=ru_path if skill.has_ru else None,
            en_content=en_raw,
            ru_content=ru_raw,
            en_frontmatter=fm_en or {},
            ru_frontmatter=fm_ru or {},
            en_body=body_en,
            ru_body=body_ru,
        )
        score = analyzer.analyze(sf)
        scores[skill.name] = score
        skills_detail.append({
            "name": skill.name,
            "category": skill.category,
            "path": str(skill.path.as_posix()),
            "grade": score.grade,
            "score": round(score.overall, 2),
            "completeness": round(score.completeness, 2),
            "depth": round(score.depth, 2),
            "code_quality": round(score.code_quality, 2),
            "freshness": round(score.freshness, 2),
            "bilingual": round(score.bilingual, 2),
            "has_ru": skill.has_ru,
        })

    report = QualityReport(scores)
    avg = report.average
    dist = report.grade_distribution

    print(f"\n{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Quality Report{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}\n")

    print(f"  Skills analyzed: {Fore.YELLOW}{len(scores)}{Style.RESET_ALL}")
    print(f"  Average completeness: {Fore.YELLOW}{avg.completeness:.1f}%{Style.RESET_ALL}")
    print(f"  Average depth:        {Fore.YELLOW}{avg.depth:.1f}%{Style.RESET_ALL}")
    print(f"  Average code quality: {Fore.YELLOW}{avg.code_quality:.1f}%{Style.RESET_ALL}")
    print(f"  Average freshness:    {Fore.YELLOW}{avg.freshness:.1f}%{Style.RESET_ALL}")
    print(f"  Average bilingual:    {Fore.YELLOW}{avg.bilingual:.1f}%{Style.RESET_ALL}")
    print(f"\n  Overall score: {Fore.GREEN}{avg.overall:.1f}% ({avg.grade}){Style.RESET_ALL}\n")

    for grade in ["A", "B", "C", "D", "F"]:
        print(f"    {grade}: {dist.get(grade, 0)}")

    print(f"\n   Top {top} skills:")
    for i, (name, score) in enumerate(report.top_skills(top), 1):
        print(f"    {i}. {Fore.CYAN}{name}{Style.RESET_ALL} - {score.overall:.1f}% ({score.grade})")

    duration = time.perf_counter() - start
    print(f"\n    Completed in {Fore.CYAN}{duration:.2f}s{Style.RESET_ALL}\n")

    if json:
        data = {
            "average": {
                "completeness": avg.completeness,
                "depth": avg.depth,
                "code_quality": avg.code_quality,
                "freshness": avg.freshness,
                "bilingual": avg.bilingual,
                "overall": avg.overall,
                "grade": avg.grade,
            },
            "grade_distribution": dist,
            "total_skills": len(scores),
            "skills": skills_detail,
        }
        Path(json).write_text(json_lib.dumps(data, indent=2), encoding="utf-8")
        print(f"   Report saved to {Fore.CYAN}{json}{Style.RESET_ALL}\n")


@cli.command()
@click.argument('query')
@click.option('--dir', type=click.Path(), default=None, help=f'Skills dir (default: {DEFAULT_SKILLS})')
@click.option('--domain', help='Filter by domain')
@click.option('--limit', type=int, default=10, help='Max results')
def search(query: str, dir: str | None, domain: str | None, limit: int):
    """Search skills."""
    builder = CatalogBuilder(base=resolve_skills_dir(dir))
    catalog = builder.build_catalog()

    print(f"\n{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Search Results for: {query}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}\n")

    results = []
    for skill in catalog.skills:
        if domain and skill.category != domain:
            continue

        score = 0
        if query.lower() in skill.name.lower():
            score += 50
        if query.lower() in skill.description.lower():
            score += 25
        if any(query.lower() in tag.lower() for tag in skill.tags):
            score += 10

        if score > 0:
            results.append((skill, score))

    results.sort(key=lambda x: x[1], reverse=True)

    if not results:
        print(f"  {Fore.YELLOW}No skills found matching '{query}'{Style.RESET_ALL}\n")
        return

    for i, (skill, score) in enumerate(results[:limit], 1):
        print(f"  {i}. {Fore.CYAN}{skill.name}{Style.RESET_ALL}")
        print(f"     {skill.description[:60]}...")
        print(f"      {skill.category} |  {', '.join(skill.languages)}")
        print()


@cli.command()
@click.option('--dir', type=click.Path(), default=None, help=f'Skills dir (default: {DEFAULT_SKILLS})')
@click.option('--output', type=click.Path(), default='skills_catalog.json', help='Output catalog path')
def catalog(dir: str | None, output: str):
    """Regenerate catalog."""
    start = time.perf_counter()

    builder = CatalogBuilder(base=resolve_skills_dir(dir))
    cat = builder.build_catalog()
    builder.to_json(cat, path=Path(output))

    duration = time.perf_counter() - start

    print(f"\n{Fore.GREEN}Catalog regenerated{Style.RESET_ALL}")
    print(f"  Skills: {cat.metadata.total_skills}")
    print(f"  Time: {duration:.2f}s\n")


if __name__ == '__main__':
    cli()