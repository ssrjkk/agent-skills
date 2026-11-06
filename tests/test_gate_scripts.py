"""In-process tests for the repo gate scripts (fences, interop, anti-patterns,
list-skills, audit_skills, _console). Subprocess smoke runs already exist in
CI; these cover the gate logic branch-by-branch and make it measurable."""

from __future__ import annotations

import io
import json
import sys
from pathlib import Path
from typing import Any

from tests.load_scripts import load_script

ROOT = Path(__file__).resolve().parent.parent


def _skill_md(name: str, description: str = "A test skill for gates") -> str:
    return (
        "---\n"
        f"name: {name}\n"
        f"description: {description}\n"
        "category: qa\n"
        "tags: [testing]\n"
        "models: [sonnet]\n"
        "version: 1.0.0\n"
        "created: 2026-09-01\n"
        "updated: 2026-09-28\n"
        "---\n# Skill\n"
        "## Quick Start\n```python\nprint('hi')\n```\n"
        "## When to Use\n- when needed\n"
        "## Step-by-Step\n1. do it\n"
        "## Examples\n```python\nx = 1\n```\n"
        "## Validation\nrun tests\n"
    )


class TestPythonFences:
    def test_valid_block_passes(self, tmp_path: Path):
        mod = load_script("check_python_fences.py")
        assert mod.check_block("```python\nx = 1\n```\n", tmp_path / "a.md") == []

    def test_syntax_error_reported(self, tmp_path: Path):
        mod = load_script("check_python_fences.py")
        errors = mod.check_block("```python\ndef broken(:\n```\n", tmp_path / "a.md")
        assert len(errors) == 1 and "python block #1" in errors[0]

    def test_skip_markers_ignored(self, tmp_path: Path):
        mod = load_script("check_python_fences.py")
        src = "```python\n... rest of implementation\n```\n```python\npass  # placeholder\n```\n"
        assert mod.check_block(src, tmp_path / "a.md") == []

    def test_main_passes_on_real_repo(self):
        mod = load_script("check_python_fences.py")
        assert mod.main() == 0


class TestAgentInterop:
    def _write(self, tmp_path: Path, name: str, text: str) -> Path:
        d = tmp_path / "qa" / name
        d.mkdir(parents=True)
        (d / "SKILL.md").write_text(text, encoding="utf-8")
        return d

    def test_valid_skill(self, tmp_path: Path):
        mod = load_script("check_agent_interop.py")
        self._write(tmp_path, "good-skill", _skill_md("good-skill"))
        errors, seen = mod.collect_errors(tmp_path)
        assert errors == [] and seen == {"good-skill"}

    def test_name_dir_mismatch(self, tmp_path: Path):
        mod = load_script("check_agent_interop.py")
        self._write(tmp_path, "dir-name", _skill_md("fm-name"))
        errors, _ = mod.collect_errors(tmp_path)
        assert any("E_ASSET3" in e and "!=" in e for e in errors)

    def test_missing_name_and_desc(self, tmp_path: Path):
        mod = load_script("check_agent_interop.py")
        text = _skill_md("x").replace("name: x\n", "").replace("description: A test skill for gates\n", "")
        self._write(tmp_path, "x", text)
        errors, _ = mod.collect_errors(tmp_path)
        assert any("E_ASSET1" in e for e in errors)
        assert any("E_ASSET2" in e for e in errors)

    def test_multiline_description(self, tmp_path: Path):
        mod = load_script("check_agent_interop.py")
        self._write(tmp_path, "multi", _skill_md("multi").replace(
            "description: A test skill for gates", 'description: |\n    line one\n    line two'))
        errors, _ = mod.collect_errors(tmp_path)
        assert any("E_ASSET4" in e for e in errors)

    def test_too_long_description(self, tmp_path: Path):
        mod = load_script("check_agent_interop.py")
        self._write(tmp_path, "long", _skill_md("long", "x" * 2000))
        errors, _ = mod.collect_errors(tmp_path)
        assert any("E_ASSET5" in e for e in errors)

    def test_duplicate_names(self, tmp_path: Path):
        mod = load_script("check_agent_interop.py")
        d1 = tmp_path / "qa1" / "dup"
        d2 = tmp_path / "qa2" / "dup"
        for d in (d1, d2):
            d.mkdir(parents=True)
            (d / "SKILL.md").write_text(_skill_md("dup"), encoding="utf-8")
        errors, _ = mod.collect_errors(tmp_path)
        assert any("E_ASSET8" in e for e in errors)

    def test_malformed_frontmatter(self, tmp_path: Path):
        mod = load_script("check_agent_interop.py")
        self._write(tmp_path, "broken", "no frontmatter here")
        errors, _ = mod.collect_errors(tmp_path)
        assert any("E_ASSET7" in e for e in errors)

    def test_main_passes_on_real_repo(self):
        mod = load_script("check_agent_interop.py")
        assert mod.main() == 0


class TestAntiPatterns:
    def _catalog(self, tmp_path: Path, skills: list[dict[str, Any]]) -> Path:
        path = tmp_path / "catalog.json"
        path.write_text(json.dumps({"skills": skills}), encoding="utf-8")
        return path

    def test_clean_catalog(self, tmp_path: Path, capsys):
        mod = load_script("detect_anti_patterns.py")
        cat = self._catalog(tmp_path, [{
            "name": "solid-skill", "description": "Builds deploy pipelines",
            "tags": ["docker", "ci"], "models": ["sonnet"],
        }])
        assert mod.detect_patterns(cat) == 0
        assert "No anti-patterns detected" in capsys.readouterr().out

    def test_all_issue_kinds_reported(self, tmp_path: Path, capsys):
        mod = load_script("detect_anti_patterns.py")
        cat = self._catalog(tmp_path, [{
            "name": "test-skill", "description": "Learn about things",
            "tags": ["general", "general"], "models": ["gpt-4", "claude-3"],
        }])
        assert mod.detect_patterns(cat) == 0
        out = capsys.readouterr().out
        assert "Learn about" in out or "learn about" in out
        assert "test-skill" in out
        assert "Duplicate tags" in out
        assert "Default model set" in out

    def test_main_on_real_catalog(self, monkeypatch):
        mod = load_script("detect_anti_patterns.py")
        monkeypatch.setattr(sys, "argv", ["detect_anti_patterns.py", str(ROOT / "skills_catalog.json")])
        assert mod.main() == 0


class TestListSkills:
    def test_lists_by_domain(self, tmp_path: Path, monkeypatch, capsys):
        mod = load_script("list-skills.py")
        (tmp_path / "skills_catalog.json").write_text(json.dumps({
            "metadata": {"total_skills": 2, "total_ru": 1},
            "skills": [
                {"name": "alpha", "category": "backend", "has_ru": True},
                {"name": "beta", "category": "frontend", "has_ru": False},
            ],
        }), encoding="utf-8")
        monkeypatch.chdir(tmp_path)
        assert mod.main() == 0
        out = capsys.readouterr().out
        assert "Total: 2 skills, 1 RU, 2 domains" in out
        assert "- alpha" in out

    def test_missing_catalog_returns_1(self, tmp_path: Path, monkeypatch, capsys):
        mod = load_script("list-skills.py")
        monkeypatch.chdir(tmp_path)
        assert mod.main() == 1
        assert "not found" in capsys.readouterr().err


class TestConsoleScript:
    def test_scripts_copy_reconfigures(self):
        mod = load_script("_console.py")
        buf = io.BytesIO()
        wrapper = io.TextIOWrapper(buf, encoding="ascii")
        old, sys.stdout = sys.stdout, wrapper
        try:
            mod.ensure_utf8_console()
            assert sys.stdout.encoding == "utf-8"
        finally:
            sys.stdout = old


class TestAuditSkills:
    def _write_skill(self, tmp_path: Path, body_extra: str = "", ru: str | None = "x" * 200) -> Path:
        body = (
            "---\nname: audited\ndescription: A thorough skill for audit testing with long text\n"
            "category: qa\ntags: [t]\nmodels: [sonnet]\nversion: 1.0.0\n---\n# T\n"
            "## Quick Start\n```python\nx = 1\n```\n## When to Use\n- use\n"
            "## Step-by-Step\n1. go\n## Examples\n```python\ny = 2\n```\n"
            "## Validation\nok\n## Dependencies\nnone\n" + body_extra
        )
        d = tmp_path / "qa" / "audited"
        d.mkdir(parents=True)
        (d / "SKILL.md").write_text(body, encoding="utf-8")
        if ru is not None:
            (d / "SKILL.ru.md").write_text("---\n---\n" + ru, encoding="utf-8")
        return d / "SKILL.md"

    def test_full_skill_scores_high(self, tmp_path: Path):
        mod = load_script("audit_skills.py")
        result = mod.audit_skill(self._write_skill(tmp_path, body_extra="\n" * 40))
        assert result["score"] >= 80
        assert result["errors"] == []

    def test_missing_frontmatter(self, tmp_path: Path):
        mod = load_script("audit_skills.py")
        p = tmp_path / "s.md"
        p.write_text("no frontmatter", encoding="utf-8")
        assert mod.audit_skill(p)["errors"] == ["Missing frontmatter"]

    def test_malformed_frontmatter(self, tmp_path: Path):
        mod = load_script("audit_skills.py")
        p = tmp_path / "s.md"
        p.write_text("--- broken", encoding="utf-8")
        assert mod.audit_skill(p)["errors"] == ["Malformed frontmatter"]

    def test_yaml_error(self, tmp_path: Path):
        mod = load_script("audit_skills.py")
        p = tmp_path / "s.md"
        p.write_text("---\n: : :\nbad [\n---\nbody", encoding="utf-8")
        assert mod.audit_skill(p)["errors"] == ["YAML parse error"]

    def test_missing_ru_flagged(self, tmp_path: Path):
        mod = load_script("audit_skills.py")
        result = mod.audit_skill(self._write_skill(tmp_path, ru=None))
        assert any("Missing RU" in w for w in result["warnings"])

    def test_stub_ru_flagged(self, tmp_path: Path):
        mod = load_script("audit_skills.py")
        result = mod.audit_skill(self._write_skill(tmp_path, ru="кратко"))
        assert any("stub" in w for w in result["warnings"])

    def test_main_json_csv_reports(self, tmp_path: Path, monkeypatch, capsys):
        mod = load_script("audit_skills.py")
        self._write_skill(tmp_path)
        j = tmp_path / "report.json"
        c = tmp_path / "report.csv"
        monkeypatch.setattr(sys, "argv", [
            "audit_skills.py", "--dir", str(tmp_path), "--top", "5",
            "--json", str(j), "--csv", str(c),
        ])
        assert mod.main() == 0
        report = json.loads(j.read_text(encoding="utf-8"))
        assert report["audited"] == 1 and report["results"][0]["name"] == "audited"
        assert "audited" in c.read_text(encoding="utf-8")
        assert "AUDIT REPORT" in capsys.readouterr().out
