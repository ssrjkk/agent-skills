"""Tests for CLI commands."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from click.testing import CliRunner

from claude_skills.cli import cli


def _strip_ansi(text: str) -> str:
    import re
    return re.sub(r"\x1b\[[0-9;]*m", "", text)


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
        "---\n# Skill\n"
        "## Quick Start\ncode sample\n"
        "## Validation\nrun tests\n"
    )
    (skill_dir / "SKILL.md").write_text(body, encoding="utf-8")
    (skill_dir / "SKILL.ru.md").write_text(body.replace("Quick Start", "Быстрый старт"), encoding="utf-8")
    return skill_dir



class TestCliImport:
    def test_cli_group(self):
        names = sorted(cli.commands.keys())
        assert set(names) == {"stats", "validate", "quality", "search", "catalog", "install"}

    def test_cli_help(self):
        import subprocess
        import sys
        result = subprocess.run(
            [sys.executable, "-m", "claude_skills.cli", "--help"],
            capture_output=True, text=True, check=False
        )
        assert result.returncode == 0
        for name in ("stats", "validate", "quality", "search", "catalog", "install"):
            assert name in result.stdout


class TestCommandSearch:
    def test_search_found(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        _make_skill(tmp_path, "my-tester", "qa")
        monkeypatch.chdir(tmp_path)
        result = CliRunner().invoke(cli, ["search", "tester"])
        assert result.exit_code == 0
        assert "my-tester" in result.output

    def test_search_not_found(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.chdir(tmp_path)
        result = CliRunner().invoke(cli, ["search", "zzznotfound"])
        assert result.exit_code == 0
        assert "No skills found" in result.output

    def test_search_with_dir(self, tmp_path: Path):
        _make_skill(tmp_path, "dir-tester", "qa")
        result = CliRunner().invoke(cli, ["search", "tester", "--dir", str(tmp_path / ".claude" / "skills")])
        assert result.exit_code == 0
        assert "dir-tester" in result.output


class TestCommandCatalog:
    def test_catalog_regenerates(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        _make_skill(tmp_path, "test-skill", "qa")
        monkeypatch.chdir(tmp_path)
        result = CliRunner().invoke(cli, ["catalog"])
        assert result.exit_code == 0
        catalog = json.loads((tmp_path / "skills_catalog.json").read_text(encoding="utf-8"))
        assert catalog["metadata"]["total_skills"] == 1

    def test_catalog_with_missing_skills(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.chdir(tmp_path)
        result = CliRunner().invoke(cli, ["catalog"])
        assert result.exit_code == 0
        catalog = json.loads((tmp_path / "skills_catalog.json").read_text(encoding="utf-8"))
        assert catalog["metadata"]["total_skills"] == 0

    def test_catalog_custom_dir_and_output(self, tmp_path: Path):
        _make_skill(tmp_path, "out-skill", "qa")
        out = tmp_path / "custom_catalog.json"
        result = CliRunner().invoke(
            cli, ["catalog", "--dir", str(tmp_path / ".claude" / "skills"), "--output", str(out)]
        )
        assert result.exit_code == 0
        catalog = json.loads(out.read_text(encoding="utf-8"))
        assert catalog["metadata"]["total_skills"] == 1
        assert catalog["skills"][0]["name"] == "out-skill"


class TestCommandValidate:
    def test_validate_clean_skill(self, tmp_path: Path):
        _make_skill(tmp_path, "ok-skill", "qa")
        result = CliRunner().invoke(cli, ["validate", "--dir", str(tmp_path / ".claude" / "skills")])
        assert result.exit_code == 0
        output = _strip_ansi(result.output)
        assert "Total skills: 1" in output
        assert "Errors: 0" in output

    def test_validate_validates_ru_too(self, tmp_path: Path):
        skill_dir = _make_skill(tmp_path, "ru-skill", "qa")
        (skill_dir / "SKILL.ru.md").write_text(
            "---\nname: ru-skill\ndescription: desc-ru\ncategory: qa\n"
            "tags: [test]\nmodels: [sonnet]\nversion: 1.0.0\nlanguage: ru\n---\n# Skill\n"
            "## Быстрый старт\ncode\n## Валидация\nrun\n",
            encoding="utf-8",
        )
        result = CliRunner().invoke(cli, ["validate", "--dir", str(tmp_path / ".claude" / "skills")])
        assert result.exit_code == 0
        assert "Errors: 0" in _strip_ansi(result.output)


class TestCommandStats:
    def test_stats(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        _make_skill(tmp_path, "stat-skill", "qa")
        monkeypatch.chdir(tmp_path)
        result = CliRunner().invoke(cli, ["stats"])
        assert result.exit_code == 0
        assert "Total skills: 1" in _strip_ansi(result.output)

    def test_stats_respects_dir(self, tmp_path: Path):
        _make_skill(tmp_path, "dir-skill", "qa")
        result = CliRunner().invoke(cli, ["stats", "--dir", str(tmp_path / ".claude" / "skills")])
        assert result.exit_code == 0
        assert "Total skills: 1" in _strip_ansi(result.output)

    def test_stats_json_report(self, tmp_path: Path):
        _make_skill(tmp_path, "json-skill", "qa")
        out = tmp_path / "stats.json"
        result = CliRunner().invoke(cli, ["stats", "--dir", str(tmp_path / ".claude" / "skills"), "--json", str(out)])
        assert result.exit_code == 0
        data = json.loads(out.read_text(encoding="utf-8"))
        assert data["total_skills"] == 1
        assert "domains" in data


class TestCommandQuality:
    def test_quality_json_report(self, tmp_path: Path):
        _make_skill(tmp_path, "quality-skill", "qa")
        out = tmp_path / "quality.json"
        result = CliRunner().invoke(
            cli, ["quality", "--dir", str(tmp_path / ".claude" / "skills"), "--json", str(out)]
        )
        assert result.exit_code == 0
        data = json.loads(out.read_text(encoding="utf-8"))
        assert data["total_skills"] == 1
        assert len(data["skills"]) == 1
        assert data["skills"][0]["name"] == "quality-skill"
        assert "grade" in data["skills"][0]
        assert "score" in data["skills"][0]