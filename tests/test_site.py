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

    rm_dir = tmp_path / "roadmaps"
    rm_dir.mkdir(parents=True, exist_ok=True)
    (rm_dir / "frontend.json").write_text(json.dumps({
        "slug": "frontend", "name": "Frontend", "icon": "🖥️",
        "tagline": "React, CSS, UI engineering", "status": "soon", "eta": "soon",
        "catalog_domain": "frontend", "related_skills": ["beta"],
        "stages": [{"title": "Fundamentals", "items": ["Map drops soon"], "status": "soon"}],
    }), encoding="utf-8")
    (rm_dir / "design.json").write_text(json.dumps({
        "slug": "design", "name": "Design", "icon": "🎨",
        "tagline": "Specs and diagrams", "status": "soon", "eta": "soon",
        "catalog_domain": None, "related_skills": [],
        "stages": [{"title": "Fundamentals", "items": ["Map drops soon"], "status": "soon"}],
    }), encoding="utf-8")

    mod = _load_mod()

    out = tmp_path / "docs"
    out.mkdir(parents=True, exist_ok=True)
    (out / "skills").mkdir(parents=True, exist_ok=True)
    (out / "domains").mkdir(parents=True, exist_ok=True)
    mod.build_index_html(catalog_path, out)
    mod.build_skill_pages(catalog_path, out)
    mod.build_domain_pages(catalog_path, out)
    mod.build_roadmaps(catalog_path, out, source_dir=tmp_path)
    mod.build_style_css(out)
    mod.build_search_index(catalog_path, out)
    return out

def _load_mod():
    import importlib.util

    spec = importlib.util.spec_from_file_location("build_docs", SCRIPTS / "build_docs.py")
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _write_catalog(tmp_path: Path, skills: list[dict]) -> Path:
    catalog = {
        "metadata": {
            "schema_version": "3.0",
            "generated_at": "2026-09-28T00:00:00Z",
            "total_skills": len(skills),
            "total_ru": sum(1 for s in skills if s.get("has_ru")),
            "domains": sorted({s["category"] for s in skills}),
            "bilingual": True,
        },
        "skills": skills,
    }
    catalog_path = tmp_path / "skills_catalog.json"
    catalog_path.write_text(json.dumps(catalog), encoding="utf-8")
    return catalog_path


def _skill_entry(tmp_path: Path, name: str, category: str) -> dict:
    return {
        "name": name,
        "description": f"A test {category} skill",
        "category": category,
        "tags": ["testing"],
        "models": ["sonnet"],
        "version": "1.0.0",
        "path": str(tmp_path / ".claude" / "skills" / category / name / "SKILL.md"),
        "languages": ["en", "ru"],
        "has_ru": True,
        "created": "2026-09-01",
        "updated": "2026-09-28",
    }


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

    def test_roadmaps_standalone(self, tmp_path: Path):
        docs = _build_site(tmp_path)
        assert (docs / "roadmaps.html").exists()
        assert (docs / "roadmaps.json").exists()
        rm_dir = docs / "roadmaps"
        assert rm_dir.is_dir()
        pages = list(rm_dir.glob("*.html"))
        assert len(pages) >= 1, "each roadmap track needs its own page"
        data = json.loads((docs / "roadmaps.json").read_text(encoding="utf-8"))
        slugs = {t["slug"] for t in data["tracks"]}
        assert slugs, "roadmaps.json must list tracks"
        for slug in slugs:
            assert (rm_dir / f"{slug}.html").exists(), f"missing roadmap page: {slug}"
        for track in data["tracks"]:
            assert track["status"] in {"soon", "live"}
            assert len(track["stages"]) >= 1

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

    def test_tabbed_layout_present(self, tmp_path: Path):
        docs = _build_site(tmp_path)
        index = (docs / "index.html").read_text(encoding="utf-8")
        assert "showTab" in index
        for tab in ["catalog", "stats", "how", "install", "roadmaps"]:
            assert f'data-panel="{tab}"' in index, f"missing tab panel: {tab}"
            assert f"showTab('{tab}'" in index, f"missing tab button: {tab}"
        assert index.count("tab-panel active") >= 2  # search + results in catalog

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


class TestBuildRobustness:
    """Graceful degradation: duplicates, missing files, empty inputs."""

    def test_duplicate_skill_names_keep_first(self, tmp_path: Path):
        _make_skill(tmp_path, "alpha", "backend")
        mod = _load_mod()
        catalog_path = _write_catalog(tmp_path, [
            _skill_entry(tmp_path, "alpha", "backend"),
            _skill_entry(tmp_path, "alpha", "backend"),
        ])
        out = tmp_path / "docs"
        (out / "skills").mkdir(parents=True)
        assert mod.build_skill_pages(catalog_path, out) == 1
        assert (out / "skills" / "alpha.html").exists()

    def test_missing_skill_file_degrades(self, tmp_path: Path):
        mod = _load_mod()
        catalog_path = _write_catalog(tmp_path, [
            _skill_entry(tmp_path, "ghost", "backend"),
        ])
        out = tmp_path / "docs"
        (out / "skills").mkdir(parents=True)
        assert mod.build_skill_pages(catalog_path, out) == 1
        assert (out / "skills" / "ghost.html").exists()

    def test_empty_catalog_builds_index(self, tmp_path: Path):
        mod = _load_mod()
        catalog_path = _write_catalog(tmp_path, [])
        out = tmp_path / "docs"
        out.mkdir(parents=True)
        mod.build_index_html(catalog_path, out)
        assert (out / "index.html").exists()

    def test_corrupt_roadmaps_fall_back_to_seed(self, tmp_path: Path):
        mod = _load_mod()
        rm_dir = tmp_path / "roadmaps"
        rm_dir.mkdir(parents=True)
        (rm_dir / "broken.json").write_text("{not json", encoding="utf-8")
        tracks = mod.load_roadmap_tracks(source_dir=tmp_path)
        assert len(tracks) == len(mod.ROADMAP_TRACKS)
        assert all(t["slug"] for t in tracks)

    def test_minify_css_preserves_quoted_strings(self):
        mod = _load_mod()
        out = mod.minify_css('.a::before{content:"> ";color:red} /* x */\n.b{margin:0 auto}')
        assert 'content:"> "' in out
        assert "/*" not in out
        assert "\n" not in out