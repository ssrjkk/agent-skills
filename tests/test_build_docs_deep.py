"""Deep tests for scripts/build_docs.py: entrypoint, SEO files, helpers,
guide rendering edges, and a real-repo portal smoke build."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"


def _load() -> Any:
    import importlib.util

    spec = importlib.util.spec_from_file_location("build_docs_deep", SCRIPTS / "build_docs.py")
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class TestHelpers:
    def test_json_for_script_never_breaks_out(self):
        mod = _load()
        out = mod.json_for_script({"x": "</script><script>alert(1)</script>"})
        assert "</script>" not in out
        assert "\\u003c" in out

    def test_rm_soon_hero_branches(self):
        mod = _load()
        assert mod.rm_soon_hero(0, 2) == "soon everywhere"
        assert mod.rm_soon_hero(0, 0) == "soon everywhere"
        assert mod.rm_soon_hero(20, 0) == "all 20 live"

    def test_skill_metrics_missing_file(self, tmp_path: Path):
        mod = _load()
        m = mod.skill_metrics(str(tmp_path / "nope.md"))
        assert m["score"] == 0 and m["lines"] == 0

    def test_skill_metrics_scores(self, tmp_path: Path):
        mod = _load()
        p = tmp_path / "s.md"
        body = "---\n---\n# S\n" + "\n".join(f"line {i}" for i in range(100)) + "\n"
        body += "```python\nx=1\n```\n" * 4
        body += "\n## A\n\n## B\n\n## C\n\n## D\n\n## E\n\n## F\n\n## G\n"
        p.write_text(body, encoding="utf-8")
        m = mod.skill_metrics(str(p))
        assert m["score"] == 100 and m["blocks"] == 4

    def test_skill_search_text_excludes_fences(self, tmp_path: Path):
        mod = _load()
        p = tmp_path / "s.md"
        p.write_text("## Head\n- bullet\n```python\nSECRET_TOKEN = 1\n```\n> quote\n", encoding="utf-8")
        text = mod.skill_search_text(p)
        assert "head" in text and "bullet" in text and "quote" in text
        assert "secret_token" not in text

    def test_guide_track_mapping_boundaries(self):
        mod = _load()
        assert mod._guide_track(1) == "devops"
        assert mod._guide_track(20) == "devops"
        assert mod._guide_track(21) == "frontend"
        assert mod._guide_track(22) == "frontend"
        assert mod._guide_track(23) == "education"
        assert mod._guide_track(24) is None
        assert mod._guide_track(0) is None

    def test_guide_tier_mapping(self):
        mod = _load()
        assert mod._guide_tier("00_README") == "meta"
        assert mod._guide_tier("01_X") == "foundation"
        assert mod._guide_tier("03_X") == "foundation"
        assert mod._guide_tier("04_X") == "cloud"
        assert mod._guide_tier("13_X") == "cloud"
        assert mod._guide_tier("14_X") == "principal"
        assert mod._guide_tier("20_X") == "principal"
        assert mod._guide_tier("21_X") == "vibe"
        assert mod._guide_tier("23_X") == "vibe"
        assert mod._guide_tier("Resume_Sergey_DevOps") == "career"

    def test_load_guides_real_repo_sorted(self):
        mod = _load()
        guides = mod.load_guides(ROOT)
        assert len(guides) == 25
        assert guides[0]["slug"].startswith("00_")
        assert guides[-1]["slug"].startswith("Resume_")
        numbers = [g["number"] for g in guides if g["number"]]
        assert numbers == sorted(numbers)


class TestGuideRenderer:
    def test_ordered_list_and_hr(self):
        mod = _load()
        html = mod.render_guide_markdown("1. один\n2. два\n\n---\n")
        assert "<ol>" in html and "<li>один</li>" in html and "<hr>" in html

    def test_task_list_uppercase_x(self):
        mod = _load()
        html = mod.render_guide_markdown("- [X] готово\n- [ ] нет")
        assert " checked" in html and "готово" in html and "нет" in html

    def test_paragraphs_join_soft_lines(self):
        mod = _load()
        html = mod.render_guide_markdown("строка раз\nстрока два")
        assert "<p>строка раз строка два</p>" in html

    def test_table_without_trailing_pipe(self):
        mod = _load()
        html = mod.render_guide_markdown("| a | b |\n|---|---|\n| 1 | 2 ")
        assert "<th>a</th>" in html and "<td>1</td>" in html

    def test_relative_link_dropped_kept_as_text(self):
        mod = _load()
        html = mod.render_guide_markdown("[файл](roadmaps/devops.json)")
        assert "href=" not in html and "[файл](roadmaps/devops.json)" in html

    def test_heading_escaping(self):
        mod = _load()
        html = mod.render_guide_markdown("## <b>&amp;</b>")
        assert "&lt;b&gt;" in html and "&amp;amp;" in html

    def test_skill_body_renderer_basics(self):
        mod = _load()
        html = mod.render_skill_body("# H1\n## H2\n### H3\n- a\n> q\n1. n\ntext")
        assert "<h1>H1</h1>" in html and "<h2>H2</h2>" in html and "<h3>H3</h3>" in html
        assert "<li>a</li>" in html and "<blockquote>q</blockquote>" in html


class TestEntrypointAndSeo:
    def test_main_end_to_end_in_tmp(self, tmp_path: Path, monkeypatch):
        import json as json_lib

        # minimal tree the builder accepts
        skill_dir = tmp_path / ".claude" / "skills" / "qa" / "alpha"
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text(
            "---\nname: alpha\ndescription: d\ncategory: qa\ntags: [t]\nmodels: [sonnet]\n"
            "version: 1.0.0\ncreated: 2026-09-01\nupdated: 2026-09-28\n---\n"
            "# S\n## A\n```python\nx=1\n```\n" * 12,
            encoding="utf-8",
        )
        catalog = {
            "metadata": {"schema_version": "3.0", "generated_at": "2026-09-28T00:00:00Z",
                         "total_skills": 1, "total_ru": 0, "domains": ["qa"], "bilingual": False},
            "skills": [{"name": "alpha", "description": "d", "category": "qa", "tags": ["t"],
                        "models": ["sonnet"], "version": "1.0.0",
                        "path": str(skill_dir / "SKILL.md"),
                        "languages": ["en"], "has_ru": False,
                        "created": "2026-09-01", "updated": "2026-09-28"}],
        }
        cat_path = tmp_path / "skills_catalog.json"
        cat_path.write_text(json_lib.dumps(catalog), encoding="utf-8")

        # main() is the repo entrypoint: it reads roadmaps/ and
        # roadmaps/guides/ from the repository root by design, so the tmp
        # build asserts against the real 20 tracks and 25 guides.
        mod = _load()
        out = tmp_path / "docs"
        monkeypatch.setattr(sys, "argv", [
            "build_docs.py", "--catalog", str(cat_path), "--output-dir", str(out), "--jobs", "2",
        ])
        assert mod.main() == 0
        assert (out / "guides" / "01_Linux_and_Networking_Map.html").exists()
        assert len(list((out / "guides").glob("*.html"))) == 25
        assert (out / "skills_catalog.json").exists()  # copied byte-exact
        assert (out / "roadmaps" / "devops.html").exists()

    def test_build_seo_files_include_guides(self, tmp_path: Path):
        mod = _load()
        cat = tmp_path / "skills_catalog.json"
        cat.write_text(
            '{"metadata": {"domains": [], "total_skills": 0, "total_ru": 0}, "skills": []}',
            encoding="utf-8",
        )
        out = tmp_path / "docs"
        out.mkdir()
        mod.build_seo_files(out, cat)
        sitemap = (out / "sitemap.xml").read_text(encoding="utf-8")
        assert f"<loc>{mod.BASE}guides.html</loc>" in sitemap
        assert f"<loc>{mod.BASE}roadmaps.html</loc>" in sitemap
        robots = (out / "robots.txt").read_text(encoding="utf-8")
        assert f"Sitemap: {mod.BASE}sitemap.xml" in robots


class TestRealRepoPortalSmoke:
    """Full portal build from the real catalog, roadmaps and guides."""

    def test_real_repo_builds_honest_portal(self, tmp_path: Path):
        if not (ROOT / "roadmaps" / "devops.json").exists() or not (ROOT / "skills_catalog.json").exists():
            pytest.skip("real repo data not present")
        mod = _load()
        out = tmp_path / "docs"
        out.mkdir()
        # build_index_html reads roadmaps from output_dir.parent (repo layout)
        import shutil as _shutil

        _shutil.copytree(ROOT / "roadmaps", tmp_path / "roadmaps")
        mod.build_index_html(ROOT / "skills_catalog.json", out)
        mod.build_roadmaps(out, source_dir=ROOT)
        mod.build_guides(out, source_dir=ROOT)
        mod.build_style_css(out)
        mod.build_site_js(out)
        mod.build_seo_files(out, ROOT / "skills_catalog.json")

        tracks = list((out / "roadmaps").glob("*.html"))
        guides = list((out / "guides").glob("*.html"))
        assert len(tracks) == 20
        assert len(guides) == 25

        index = (out / "index.html").read_text(encoding="utf-8")
        assert 'class="live-dot">live</span>' in index
        assert "all 20 live" in index
        assert 'href="guides.html"' in index

        rm_overview = (out / "roadmaps.html").read_text(encoding="utf-8")
        assert "Every track is live" in rm_overview
        assert "· 20 live" in rm_overview

        devops = (out / "roadmaps" / "devops.html").read_text(encoding="utf-8")
        assert 'href="../guides/01_Linux_and_Networking_Map.html"' in devops
        assert 'href="../guides/20_HandsOn_Troubleshooting_Simulator_Guide.html"' in devops

        guide = (out / "guides" / "01_Linux_and_Networking_Map.html").read_text(encoding="utf-8")
        assert 'href="../roadmaps/devops.html"' in guide
        assert "TechArticle" in guide
        assert guide.count("<h1") == 1

        sitemap = (out / "sitemap.xml").read_text(encoding="utf-8")
        assert "guides/01_Linux_and_Networking_Map.html" in sitemap
        assert sitemap.count("<url>") >= 120 + 20 + 27 + 2
