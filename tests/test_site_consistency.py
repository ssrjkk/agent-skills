"""Tests for scripts/check_site_consistency.py.

Positive path runs against the real repo (docs are committed, so this doubles
as a CI guard); negative paths build a minimal site in tmp and break exactly
one invariant at a time.
"""

from __future__ import annotations

import json
from pathlib import Path

import yaml

from tests.load_scripts import load_script

ROOT = Path(__file__).resolve().parent.parent

PAGE_ROOT = (
    "<!DOCTYPE html><html><head><link href=\"style.css\"></head>"
    "<body><div><p>hi</p></div><script src=\"site.js\"></script></body></html>"
)
PAGE_SUB = (
    "<!DOCTYPE html><html><head><link href=\"../style.css\"></head>"
    "<body><div><p>hi</p></div><script src=\"../site.js\"></script></body></html>"
)


def _mini_site(root: Path) -> None:
    docs = root / "docs"
    (docs / "skills").mkdir(parents=True)
    (docs / "domains").mkdir()
    (docs / "roadmaps").mkdir()
    (docs / "guides").mkdir()
    (root / "assets").mkdir()
    (root / "assets" / "site.js").write_text(
        (ROOT / "assets" / "site.js").read_text(encoding="utf-8"), encoding="utf-8"
    )
    (root / "roadmaps").mkdir()
    (root / "roadmaps" / "guides").mkdir()
    catalog = {
        "metadata": {"domains": ["qa"]},
        "skills": [{"name": "alpha", "category": "qa"}],
    }
    (root / "skills_catalog.json").write_text(json.dumps(catalog), encoding="utf-8")
    (docs / "search-index.json").write_text(json.dumps([
        {"name": "alpha", "category": "qa", "content": "c", "content_ru": "к"},
    ]), encoding="utf-8")
    (docs / "site.js").write_text((ROOT / "assets" / "site.js").read_text(encoding="utf-8"), encoding="utf-8")
    (docs / "style.css").write_text("body{}", encoding="utf-8")
    (docs / "index.html").write_text(PAGE_ROOT, encoding="utf-8")
    (docs / "guides.html").write_text(PAGE_ROOT, encoding="utf-8")
    (docs / "roadmaps.html").write_text(PAGE_ROOT, encoding="utf-8")
    (docs / "skills" / "alpha.html").write_text(PAGE_SUB, encoding="utf-8")
    (docs / "domains" / "qa.html").write_text(PAGE_SUB, encoding="utf-8")
    (root / "roadmaps" / "frontend.json").write_text(json.dumps({
        "slug": "frontend", "name": "Frontend", "icon": "x", "tagline": "t",
        "status": "soon", "eta": "soon",
        "stages": [{"title": "S", "items": ["a"], "status": "soon"}],
    }), encoding="utf-8")
    (docs / "roadmaps" / "frontend.html").write_text(PAGE_SUB, encoding="utf-8")
    (docs / "roadmaps.json").write_text(json.dumps({"tracks": [{"slug": "frontend"}]}), encoding="utf-8")
    (root / "roadmaps" / "guides" / "01_Map.md").write_text("# Map\n\ntext\n", encoding="utf-8")
    (docs / "guides" / "01_Map.html").write_text(PAGE_SUB, encoding="utf-8")


def test_real_repo_is_consistent():
    mod = load_script("check_site_consistency.py")
    assert mod.main() == 0


def test_mini_site_passes(tmp_path: Path, capsys):
    mod = load_script("check_site_consistency.py")
    _mini_site(tmp_path)
    assert mod.main(tmp_path) == 0
    assert "1 guides" in capsys.readouterr().out


def _broken(tmp_path: Path, mutate) -> str:
    _mini_site(tmp_path)
    mutate(tmp_path)
    mod = load_script("check_site_consistency.py")
    import contextlib
    import io

    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        code = mod.main(tmp_path)
    assert code == 1
    return buf.getvalue()


def test_missing_skill_page_detected(tmp_path: Path):
    out = _broken(tmp_path, lambda r: (r / "docs" / "skills" / "alpha.html").unlink())
    assert "missing skill page: alpha" in out


def test_search_index_drift_detected(tmp_path: Path):
    def mutate(r: Path) -> None:
        idx = json.loads((r / "docs" / "search-index.json").read_text(encoding="utf-8"))
        idx.append({"name": "ghost", "category": "qa", "content": "", "content_ru": ""})
        (r / "docs" / "search-index.json").write_text(json.dumps(idx), encoding="utf-8")
    out = _broken(tmp_path, mutate)
    assert "search-index has unknown skills" in out


def test_broken_link_detected(tmp_path: Path):
    def mutate(r: Path) -> None:
        page = r / "docs" / "index.html"
        page.write_text(
            page.read_text(encoding="utf-8").replace(
                "<body>", "<body><a href=\"skills/nope.html\">x</a>"),
            encoding="utf-8",
        )
    out = _broken(tmp_path, mutate)
    assert "broken link: skills/nope.html" in out


def test_unbalanced_divs_detected(tmp_path: Path):
    def mutate(r: Path) -> None:
        page = r / "docs" / "index.html"
        page.write_text(
            page.read_text(encoding="utf-8").replace("</div>", ""),
            encoding="utf-8",
        )
    out = _broken(tmp_path, mutate)
    assert "unbalanced <div>" in out


def test_site_js_must_match_source(tmp_path: Path):
    def mutate(r: Path) -> None:
        (r / "docs" / "site.js").write_text("// drifted", encoding="utf-8")
    out = _broken(tmp_path, mutate)
    assert "site.js differs from assets/site.js" in out


def test_roadmap_page_missing_detected(tmp_path: Path):
    out = _broken(tmp_path, lambda r: (r / "docs" / "roadmaps" / "frontend.html").unlink())
    assert "missing roadmap page: frontend" in out


def test_guide_page_missing_detected(tmp_path: Path):
    out = _broken(tmp_path, lambda r: (r / "docs" / "guides" / "01_Map.html").unlink())
    assert "missing guide page: 01_Map" in out


def test_guides_overview_missing_detected(tmp_path: Path):
    out = _broken(tmp_path, lambda r: (r / "docs" / "guides.html").unlink())
    assert "missing guides.html overview" in out


def test_wrong_css_path_detected(tmp_path: Path):
    def mutate(r: Path) -> None:
        p = r / "docs" / "skills" / "alpha.html"
        p.write_text(PAGE_SUB.replace("../style.css", "style.css"), encoding="utf-8")
    out = _broken(tmp_path, mutate)
    assert "wrong css path" in out


def test_missing_domain_page_detected(tmp_path: Path):
    out = _broken(tmp_path, lambda r: (r / "docs" / "domains" / "qa.html").unlink())
    assert "missing domain page: qa" in out


def test_bad_track_status_detected(tmp_path: Path):
    def mutate(r: Path) -> None:
        p = r / "roadmaps" / "frontend.json"
        data = json.loads(p.read_text(encoding="utf-8"))
        data["status"] = "wip"
        p.write_text(json.dumps(data), encoding="utf-8")
    out = _broken(tmp_path, mutate)
    assert "bad status" in out


def test_pages_artifact_comes_from_one_checked_matrix_build():
    workflow = yaml.safe_load((ROOT / ".github" / "workflows" / "validate.yml").read_text(encoding="utf-8"))
    validate = workflow["jobs"]["validate"]
    steps = validate["steps"]
    uploads = [step for step in steps if step.get("uses", "").startswith("actions/upload-pages-artifact@")]
    assert len(uploads) == 1
    upload = uploads[0]
    assert upload["with"]["path"] == "docs"
    assert "matrix.python-version == '3.12'" in upload["if"]
    assert "github.ref == 'refs/heads/main'" in upload["if"]
    assert "vars.DEPLOY_PAGES == 'true'" in upload["if"]
    assert validate["strategy"]["matrix"]["python-version"].count("3.12") == 1
    upload_index = steps.index(upload)
    for name in (
        "Generate catalog",
        "Run tests with coverage",
        "Build documentation site",
        "Verify site consistency (links, CSS paths, search index)",
        "Verify catalog consistency",
        "Verify responsive site in Chromium",
    ):
        gate = next(step for step in steps if step.get("name") == name)
        assert steps.index(gate) < upload_index
        assert not gate.get("continue-on-error", False)


def test_pages_deploy_consumes_artifact_without_recreating_docs():
    workflow = yaml.safe_load((ROOT / ".github" / "workflows" / "validate.yml").read_text(encoding="utf-8"))
    deploy = workflow["jobs"]["deploy-pages"]
    assert deploy["needs"] == "validate"
    assert "github.ref == 'refs/heads/main'" in deploy["if"]
    assert "vars.DEPLOY_PAGES == 'true'" in deploy["if"]
    steps = deploy["steps"]
    assert not any("run" in step for step in steps)
    assert not any(step.get("uses", "").startswith(("actions/checkout@", "actions/upload-pages-artifact@")) for step in steps)
    assert sum(step.get("uses", "").startswith("actions/deploy-pages@") for step in steps) == 1
