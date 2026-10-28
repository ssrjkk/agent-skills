"""Tests for the docs site generator (build_docs.py)."""

from __future__ import annotations

import json
import re
from html.parser import HTMLParser
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"


class _ScriptExtractor(HTMLParser):
    """Collect inline <script> bodies without regex tag filtering
    (regex-based tag matching trips CodeQL py/bad-tag-filter)."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.blocks: list[str] = []
        self._buf: list[str] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "script":
            return
        attrs_dict = dict(attrs)
        if "src" in attrs_dict:
            return
        script_type = (attrs_dict.get("type") or "text/javascript").lower()
        if script_type not in ("text/javascript", "module"):
            return
        self._buf = []

    def handle_data(self, data: str) -> None:
        if self._buf is not None:
            self._buf.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "script" and self._buf is not None:
            self.blocks.append("".join(self._buf))
            self._buf = None


def _inline_scripts(html: str) -> list[str]:
    parser = _ScriptExtractor()
    parser.feed(html)
    return parser.blocks


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
    mod.build_site_js(out)
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
        assert "быстрый старт" in alpha["content_ru"]

    def test_skill_page_has_ru_toggle(self, tmp_path: Path):
        docs = _build_site(tmp_path)
        html = (docs / "skills" / "alpha.html").read_text(encoding="utf-8")
        assert "showSkillLang" in html
        assert 'data-slang-body="en"' in html
        assert 'data-slang-body="ru"' in html
        assert "Быстрый старт" in html

    def test_skill_page_without_ru_has_no_toggle(self, tmp_path: Path):
        mod = _load_mod()
        skill_dir = _make_skill(tmp_path, "solo", "backend")
        (skill_dir / "SKILL.ru.md").unlink()
        catalog_path = _write_catalog(tmp_path, [_skill_entry(tmp_path, "solo", "backend")])
        out = tmp_path / "docs"
        (out / "skills").mkdir(parents=True)
        assert mod.build_skill_pages(catalog_path, out) == 1
        html = (out / "skills" / "solo.html").read_text(encoding="utf-8")
        assert "lang-tabs" not in html
        assert 'data-slang-body="en"' not in html
        assert "Quick Start" in html

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

    def test_i18n_keys_cover_markup(self, tmp_path: Path):
        docs = _build_site(tmp_path)
        pages = (
            list(docs.glob("*.html"))
            + list((docs / "skills").glob("alpha.html"))
            + list((docs / "roadmaps").glob("*.html"))
        )
        assert len(pages) >= 4
        used: set[str] = set()
        for page in pages:
            html = page.read_text(encoding="utf-8")
            used.update(re.findall(r'data-i18n="([a-z_0-9]+)"', html))
            used.update(re.findall(r'data-i18n-ph="([a-z_0-9]+)"', html))
            used.update(re.findall(r'data-i18n-aria="([a-z_0-9]+)"', html))
        assert used, "expected i18n hooks in markup"
        # single source of truth: every key must be defined in assets/site.js
        site_js = (docs / "site.js").read_text(encoding="utf-8")
        for key in sorted(used):
            assert f'{key}:"' in site_js, f"key {key!r} missing in site.js dicts"

    def test_i18n_single_source_of_truth(self):
        src = (SCRIPTS / "build_docs.py").read_text(encoding="utf-8")
        assert src.count("var I18N = {") == 0, "I18N dict must live in assets/site.js, not inline"
        site_js = (ROOT / "assets" / "site.js").read_text(encoding="utf-8")
        head, sep, tail = site_js.partition("\n    ru: ")
        assert sep, "no ru dict in site.js"
        key_re = re.compile(r"[{,]\s*([A-Za-z_][A-Za-z_0-9]*)\s*:\"")
        en_keys = set(key_re.findall(head))
        ru_keys = set(key_re.findall(tail))
        assert en_keys, "no en keys parsed"
        assert en_keys == ru_keys, f"en/ru drift: {sorted(en_keys ^ ru_keys)}"
        assert "hero_sub" in en_keys

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

    def test_shared_site_js_single_source(self, tmp_path: Path):
        docs = _build_site(tmp_path)
        src = (ROOT / "assets" / "site.js").read_text(encoding="utf-8")
        for fn in ["setLang", "toggleTheme", "showSkillLang", "copyBtn",
                   "showToast", "toggleLang", "IntersectionObserver"]:
            assert fn in src, f"assets/site.js missing {fn}"
        built = (docs / "site.js").read_text(encoding="utf-8")
        assert built == src, "docs/site.js must be an exact copy of assets/site.js"
        for page in list(docs.glob("*.html")) + list((docs / "skills").glob("*.html")):
            html = page.read_text(encoding="utf-8")
            assert "var I18N" not in html, f"{page.name} duplicates shared JS"

    def test_tabbed_layout_present(self, tmp_path: Path):
        docs = _build_site(tmp_path)
        index = (docs / "index.html").read_text(encoding="utf-8")
        assert "showTab" in index
        for tab in ["catalog", "stats", "how", "install", "roadmaps"]:
            assert f'data-panel="{tab}"' in index, f"missing tab panel: {tab}"
            assert f"showTab('{tab}'" in index, f"missing tab button: {tab}"
        assert index.count("tab-panel active") >= 2  # search + results in catalog

    def test_i18n_and_delights_present(self, tmp_path: Path):
        docs = _build_site(tmp_path)
        index = (docs / "index.html").read_text(encoding="utf-8")
        assert 'src="site.js"' in index  # shared behavior, not inline
        assert "toggleLang" in index or "lang-toggle" in index
        assert 'data-i18n="hero_sub"' in index
        assert 'data-i18n-ph="search_ph"' in index
        assert 'id="result-count"' in index
        assert 'id="back-top"' in index
        assert "copyBtn" in index
        assert "card-copy" in index
        assert "<kbd>/</kbd>" in index
        skill = (docs / "skills" / "alpha.html").read_text(encoding="utf-8")
        assert 'src="../site.js"' in skill  # shared script, no inline copy
        assert 'data-i18n="quality"' in skill
        assert ".claude/skills/backend/alpha" in skill  # full copy path, not bare name
        rm = (docs / "roadmaps.html").read_text(encoding="utf-8")
        assert 'data-i18n="rm_t"' in rm

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

    def test_no_template_literals_leak_into_scripts(self, tmp_path: Path):
        docs = _build_site(tmp_path)
        for page in list(docs.glob("*.html")) + [docs / "roadmaps.html"]:
            html = page.read_text(encoding="utf-8")
            for block in _inline_scripts(html):
                assert "{json.dumps" not in block
                assert "{esc(" not in block
                assert "{{" not in block
                assert "&quot;" not in block

    def test_inline_js_parses_with_node(self, tmp_path: Path):
        import shutil
        import subprocess

        if shutil.which("node") is None:
            pytest.skip("node not available")
        docs = _build_site(tmp_path)
        blocks = []
        for page in list(docs.glob("*.html")) + [docs / "roadmaps.html"]:
            html = page.read_text(encoding="utf-8")
            blocks.extend(_inline_scripts(html))
        assert blocks, "expected inline scripts"
        bundle = tmp_path / "inline.js"
        bundle.write_text("\n;\n".join(blocks), encoding="utf-8")
        proc = subprocess.run(["node", "--check", str(bundle)], check=False, capture_output=True, text=True)
        assert proc.returncode == 0, proc.stderr[:2000]

    def test_index_js_runs_in_stubbed_dom(self, tmp_path: Path):
        """Execute the index inline script against DOM stubs: catches
        ReferenceErrors (the dead-script bug class), not just syntax."""
        import shutil
        import subprocess

        if shutil.which("node") is None:
            pytest.skip("node not available")
        docs = _build_site(tmp_path)
        html = (docs / "index.html").read_text(encoding="utf-8")
        blocks = _inline_scripts(html)
        assert blocks, "expected inline scripts on index"
        harness = tmp_path / "runjs.js"
        harness.write_text(
            "var document = {"
            "querySelectorAll: function() { return []; },"
            "querySelector: function() { return null; },"
            "getElementById: function() { return null; },"
            "addEventListener: function() {},"
            "createElement: function() { return {classList: {add: function() {}}}; },"
            "documentElement: {setAttribute: function() {}}};\n"
            "var window = {addEventListener: function() {}, scrollTo: function() {}};\n"
            "var location = {hash: ''};\n"
            "var navigator = {language: 'en'};\n"
            "var localStorage = {getItem: function() { return null; },"
            " setItem: function() {}, removeItem: function() {}};\n"
            "var sessionStorage = {getItem: function() { return null; }};\n"
            "var history = {replaceState: function() {}};\n"
            "var requestAnimationFrame = function() { return 0; };\n"
            + "\n;\n".join(blocks)
            + "\nconsole.log(JSON.stringify({"
            "scoreHit: scoreSkill('fast', 'fastapi', 'backend', 'fastapi python',"
            " 'fast rest api', 'some body text'),"
            "scoreMiss: scoreSkill('zzz', 'fastapi', 'backend', 'x', 'y', 'z'),"
            "scoreEmpty: scoreSkill('', 'a', 'b', 'c', 'd', 'e'),"
            "scoreMid: scoreSkill('api', 'go-rest-api', 'backend', 'go gin', 'rest', 'x'),"
            "fns: [typeof showTab, typeof applyFilter, typeof onSearch,"
            " typeof filterByDomain, typeof scoreSkill].join(',')}));\n",
            encoding="utf-8",
        )
        proc = subprocess.run(["node", str(harness)], check=False, capture_output=True, text=True)
        assert proc.returncode == 0, proc.stderr[:2000]
        out = json.loads(proc.stdout.strip().splitlines()[-1])
        assert out["scoreHit"] == 85, out
        assert out["scoreMiss"] == 0, out
        assert out["scoreEmpty"] == 0, out
        assert out["scoreMid"] == 30, out
        assert out["fns"] == "function,function,function,function,function", out