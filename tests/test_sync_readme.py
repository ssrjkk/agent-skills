"""Tests for scripts/sync_readme.py (README <-> catalog synchronization).

Covers the live-roadmaps line regression (in-place replacement, never
duplication) introduced when the roadmap count went 3 -> 20.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from tests.load_scripts import load_script


def _load() -> Any:
    return load_script("sync_readme.py")


def _catalog(tmp_path: Path, skills: list[dict[str, Any]] | None = None) -> Path:
    skills = skills or [
        {"name": "alpha", "category": "backend", "description": "Backend skill  "},
        {"name": "beta", "category": "frontend", "description": "Frontend skill"},
    ]
    catalog = {
        "metadata": {
            "total_skills": len(skills),
            "total_ru": len(skills),
            "domains": sorted({s["category"] for s in skills}),
        },
        "skills": skills,
    }
    path = tmp_path / "skills_catalog.json"
    path.write_text(json.dumps(catalog), encoding="utf-8")
    return path


def _readme(base_text: str | None = None) -> str:
    text = base_text or (
        "# Title\n\n"
        "![skills](badge/skills-1-blue)\n"
        "![domains](badge/domains-1-orange)\n\n"
        "| Metric | Value |\n|---|---|\n"
        "| Total skills | **1** |\n"
        "| Russian translations | **1 (100%)** |\n"
        "| Domains | **1** |\n\n"
        "100 production-grade and 100 hand-reviewed skills.\n\n"
        "## Skills by domain\n\n"
        "| Domain | Skill | Description |\n"
        "|--------|-------|-------------|\n"
        "| `backend` | `alpha` | old desc |\n\n"
        "## Domains (1)\n\n"
        "`backend`\n\n"
        "- [Issue Tracker](https://github.com/ssrjkk/agent-skills/issues)\n"
    )
    return text


def _tracks(tmp_path: Path, statuses: list[str]) -> None:
    tdir = tmp_path / "roadmaps"
    tdir.mkdir(exist_ok=True)
    for i, st in enumerate(statuses):
        (tdir / f"t{i}.json").write_text(
            json.dumps({"slug": f"t{i}", "status": st}), encoding="utf-8"
        )


def test_badges_and_counts_updated(tmp_path: Path):
    mod = _load()
    cat = _catalog(tmp_path)
    readme = _readme()
    out = mod.render(readme, json.loads(cat.read_text(encoding="utf-8")))
    assert "badge/skills-2-blue" in out
    assert "badge/domains-2-orange" in out
    assert "| Total skills | **2** |" in out
    assert "| Domains | **2** |" in out
    assert "| Russian translations | **2 (100%)** |" in out
    assert "2 production-grade" in out
    assert "2 hand-reviewed" in out
    assert "| `frontend` | `beta` | Frontend skill |" in out


def test_roadmaps_line_replaced_in_place_never_duplicated(tmp_path: Path):
    mod = _load()
    mod.ROOT = tmp_path
    _tracks(tmp_path, ["live", "live"])
    stale = "- [IT Roadmaps](https://ssrjkk.github.io/agent-skills/roadmaps.html) (3 of 20 maps live: backend, QA, AI/ML)"
    readme = _readme()
    readme = readme.replace(
        "- [Issue Tracker](https://github.com/ssrjkk/agent-skills/issues)",
        "- [Issue Tracker](https://github.com/ssrjkk/agent-skills/issues)\n" + stale,
    )
    out = mod.render(readme, json.loads(_catalog(tmp_path).read_text(encoding="utf-8")))
    assert out.count("- [IT Roadmaps](") == 1, "roadmaps line must never duplicate"
    assert "3 of 20" not in out
    assert "(all 2 maps live — EN + RU)" in out


def test_roadmaps_line_inserted_after_issue_tracker(tmp_path: Path):
    mod = _load()
    mod.ROOT = tmp_path
    _tracks(tmp_path, ["live", "soon"])
    out = mod.render(_readme(), json.loads(_catalog(tmp_path).read_text(encoding="utf-8")))
    assert out.count("- [IT Roadmaps](") == 1
    issue = out.index("- [Issue Tracker]")
    road = out.index("- [IT Roadmaps](")
    assert issue < road
    assert "(1 of 2 maps live)" in out


def test_zero_live_says_soon(tmp_path: Path):
    mod = _load()
    mod.ROOT = tmp_path
    _tracks(tmp_path, ["soon", "soon"])
    out = mod.render(_readme(), json.loads(_catalog(tmp_path).read_text(encoding="utf-8")))
    assert "(every direction, soon)" in out


def test_partial_live_drops_hardcoded_track_names(tmp_path: Path):
    mod = _load()
    mod.ROOT = tmp_path
    _tracks(tmp_path, ["live", "soon"])
    out = mod.render(_readme(), json.loads(_catalog(tmp_path).read_text(encoding="utf-8")))
    assert "(1 of 2 maps live)" in out
    assert "backend, QA, AI/ML" not in out


def test_single_track_counts_as_all_live(tmp_path: Path):
    mod = _load()
    mod.ROOT = tmp_path
    _tracks(tmp_path, ["live"])
    out = mod.render(_readme(), json.loads(_catalog(tmp_path).read_text(encoding="utf-8")))
    assert "(all 1 maps live — EN + RU)" in out


def test_domains_line_wraps_long_lists():
    mod = _load()
    one_line = mod.domains_line(["a", "b"])
    assert len(one_line) == 1
    many = mod.domains_line([f"domain-{i:02d}" for i in range(30)])
    assert len(many) > 1
    assert all(ln.startswith("`") for ln in many)


def test_table_rows_sorted_by_category_then_name():
    mod = _load()
    rows = mod.table_rows([
        {"category": "b", "name": "z", "description": " d "},
        {"category": "a", "name": "m", "description": " c "},
    ])
    assert rows[2] == "| `a` | `m` | c |"
    assert rows[3] == "| `b` | `z` | d |"


def test_main_check_flags_stale_readme(tmp_path: Path, monkeypatch, capsys):
    mod = _load()
    cat = _catalog(tmp_path)
    readme_path = tmp_path / "README.md"
    readme_path.write_text(_readme(), encoding="utf-8")
    monkeypatch.setattr(mod, "CATALOG", cat)
    monkeypatch.setattr(mod, "README", readme_path)
    monkeypatch.setattr(sys, "argv", ["sync_readme.py", "--check"])
    assert mod.main() == 1
    assert "stale" in capsys.readouterr().err


def test_main_writes_then_check_passes(tmp_path: Path, monkeypatch, capsys):
    mod = _load()
    mod.ROOT = tmp_path
    _tracks(tmp_path, ["live"])
    cat = _catalog(tmp_path)
    readme_path = tmp_path / "README.md"
    readme_path.write_text(_readme(), encoding="utf-8")
    monkeypatch.setattr(mod, "CATALOG", cat)
    monkeypatch.setattr(mod, "README", readme_path)
    monkeypatch.setattr(sys, "argv", ["sync_readme.py"])
    assert mod.main() == 0
    written = readme_path.read_text(encoding="utf-8")
    assert "badge/skills-2-blue" in written
    monkeypatch.setattr(sys, "argv", ["sync_readme.py", "--check"])
    assert mod.main() == 0
    assert "in sync" in capsys.readouterr().out
