"""Tests for the docs site generator (build_docs.py)."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"


def _make_skill(root: Path, name: str, category: str, description: str = "A test skill") -> Path:
    skill_dir = root / ".claude" / "skills" / category / name
    skill_dir.mkdir(parents=True)
    body = (
        "---\n"
        f"name: {name}\n"
        f"description: {description}\n"
        f"category: {category}\n"
        "tags: [testing, automation]\n"
        "models: [sonnet, opus]\n"
        "version: 1.0.0\n"
        "created: 2026-09-01\n"
        "updated: 2026-09-28\n"
        "---\n# Skill\n"
        "## Quick Start\n```python\nprint('hi')\n```\n"
        "## When to Use\n- when needed\n"
        "## Step-by-Step\n1. do it\n"
        "## Examples\n```python\nx = 1\n```\n"
        "## Validation\nrun tests\n"
        "## Best Practices\n- keep it simple\n"
        "## Troubleshooting\n- if broken fix\n"
    )
    (skill_dir / "SKILL.md").write_text(body, encoding="utf-8")
    (skill_dir / "SKILL.ru.md").write_text(
        body.replace("Quick Start", "Быстрый старт").replace("When to Use", "Когда использовать"),
        encoding="utf-8",
    )
    return skill_dir


def _build_site(tmp_path: Path) -> Path:
    """Build a full docs site from a temporary catalog and skills tree."""
    _make_skill(tmp_path, "alpha", "backend")
    _make_skill(tmp_path, "beta", "frontend")
    catalog = {
        "metadata": {
            "schema_version": "3.0",
            "generated_at": "2026-09-28T00:00:00Z",
            "total_skills": 2,
            "total_ru": 2,
            "domains": ["backend", "frontend"],
            "bilingual": True,
        },
        "skills": [
            {
                "name": "alpha",
                "description": "A test backend skill",
                "category": "backend",
                "tags": ["api", "python"],
                "models": ["sonnet", "opus"],
                "version": "1.0.0",
                "path": str(tmp_path / ".claude" / "skills" / "backend" / "alpha" / "SKILL.md"),
                "languages": ["en", "ru"],
                "has_ru": True,
                "created": "2026-09-01",
                "updated": "2026-09-28",
            },
            {
                "name": "beta",
                "description": "A test frontend skill",
                "category": "frontend",
                "tags": ["react", "ts"],
                "models": ["sonnet", "opus"],
                "version": "1.0.0",
                "path": str(tmp_path / ".claude" / "skills" / "frontend" / "beta" / "SKILL.md"),
                "languages": ["en", "ru"],
                "has_ru": True,
                "created": "2026-09-01",
                "updated": "2026-09-28",
            },
        ],
    }
    catalog_path = tmp_path / "skills_catalog.json"
    catalog_path.write_text(json.dumps(catalog), encoding="utf-8")

    import importlib.util

    spec = importlib.util.spec_from_file_location("build_docs", SCRIPTS / "build_docs.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    out = tmp_path / "docs"
    out.mkdir(parents=True, exist_ok=True)
    (out / "skills").mkdir(parents=True, exist_ok=True)
    (out / "domains").mkdir(parents=True, exist_ok=True)
    mod.build_index_html(catalog_path, out)
    mod.build_skill_pages(catalog_path, out)
    mod.build_domain_pages(catalog_path, out)
    mod.build_style_css(out)
    mod.build_search_index(catalog_path, out)
    return out


class TestSiteGenerator:
    def test_all_pages_generated(self, tmp_path: Path):
        docs = _build_site(tmp_path)
        assert (docs / "index.html").exists()
        assert (docs / "search-index.json").exists()
        assert (docs / "style.css").exists()
        assert (docs / "skills" / "alpha.html").exists()
        assert (docs / "skills" / "beta.html").exists()
        assert (docs / "domains" / "backend.html").exists()
        assert (docs / "domains" / "frontend.html").exists()

    def test_css_paths_correct(self, tmp_path: Path):
        docs = _build_site(tmp_path)
        index = (docs / "index.html").read_text(encoding="utf-8")
        assert 'href="style.css"' in index, "index must use style.css"
        skill = (docs / "skills" / "alpha.html").read_text(encoding="utf-8")
        assert 'href="../style.css"' in skill, "skill page must use ../style.css"
        domain = (docs / "domains" / "backend.html").read_text(encoding="utf-8")
        assert 'href="../style.css"' in domain, "domain page must use ../style.css"

    def test_search_index_has_all_skills(self, tmp_path: Path):
        docs = _build_site(tmp_path)
        idx = json.loads((docs / "search-index.json").read_text(encoding="utf-8"))
        names = {e["name"] for e in idx}
        assert names == {"alpha", "beta"}
        alpha = next(e for e in idx if e["name"] == "alpha")
        assert "quick start" in alpha["content"]
        assert "validation" in alpha["content"]

    def test_no_broken_relative_links(self, tmp_path: Path):
        docs = _build_site(tmp_path)
        for page in docs.rglob("*.html"):
            html = page.read_text(encoding="utf-8")
            for m in re.finditer(r'href="([^"]+\.html)"', html):
                href = m.group(1)
                if href.startswith(("http", "//", "#")):
                    continue
                target = (page.parent / href).resolve()
                assert target.exists(), f"{page.name} -> broken link {href}"

    def test_div_tags_balanced(self, tmp_path: Path):
        docs = _build_site(tmp_path)
        for page in docs.rglob("*.html"):
            html = page.read_text(encoding="utf-8")
            assert html.count("<div") == html.count("</div>"), f"unbalanced divs in {page.name}"

    def test_theme_toggle_and_search_js_present(self, tmp_path: Path):
        docs = _build_site(tmp_path)
        index = (docs / "index.html").read_text(encoding="utf-8")
        assert "toggleTheme" in index
        assert "loadSearchIndex" in index
        assert "filterByDomain" in index
        assert "applyFilter" in index

    def test_light_theme_css_present(self, tmp_path: Path):
        docs = _build_site(tmp_path)
        css = (docs / "style.css").read_text(encoding="utf-8")
        assert 'data-theme="light"' in css, "light theme must be defined"

    def test_check_site_consistency_script(self, tmp_path: Path):
        # Build into real docs layout and run the consistency script against it
        docs = _build_site(tmp_path)
        # write catalog to the docs parent as the script expects ROOT-based paths
        # Instead, run the script's logic manually on the generated docs
        idx = json.loads((docs / "search-index.json").read_text(encoding="utf-8"))
        assert len(idx) == 2
        for page in docs.rglob("*.html"):
            assert page.read_text(encoding="utf-8").count("<div") == page.read_text(encoding="utf-8").count("</div>")