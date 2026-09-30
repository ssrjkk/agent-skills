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


def _make_skill(root: Path, name: str, category: str, description: str = "A test skill", tags: str = "testing, automation") -> Path:
    skill_dir = root / ".claude" / "skills" / category / name
    skill_dir.mkdir(parents=True)
    body = (
        "---\n"
        f"name: {name}\n"
        f"description: {description}\n"
        f"category: {category}\n"
        f"tags: [{tags}]\n"
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

    def test_search_domain_filter(self, tmp_path: Path):
        _make_skill(tmp_path, "domain-hit", "qa")
        _make_skill(tmp_path, "domain-miss", "backend")
        result = CliRunner().invoke(
            cli, ["search", "domain", "--dir", str(tmp_path / ".claude" / "skills"), "--domain", "qa"]
        )
        assert result.exit_code == 0
        assert "domain-hit" in result.output
        assert "domain-miss" not in result.output

    def test_search_ranks_by_description_and_tags(self, tmp_path: Path):
        _make_skill(tmp_path, "desc-skill", "qa", description="contains unique-foo keyword")
        _make_skill(tmp_path, "tag-skill", "qa")
        result = CliRunner().invoke(cli, ["search", "unique-foo", "--dir", str(tmp_path / ".claude" / "skills")])
        assert result.exit_code == 0
        assert "desc-skill" in result.output

    def test_search_by_tag(self, tmp_path: Path):
        _make_skill(tmp_path, "tag-matched", "qa", tags="special-tag, x")
        _make_skill(tmp_path, "tag-other", "qa")
        result = CliRunner().invoke(cli, ["search", "special-tag", "--dir", str(tmp_path / ".claude" / "skills")])
        assert result.exit_code == 0
        assert "tag-matched" in result.output


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

    def test_validate_json_report(self, tmp_path: Path):
        _make_skill(tmp_path, "json-skill", "qa")
        out = tmp_path / "validate.json"
        result = CliRunner().invoke(
            cli, ["validate", "--dir", str(tmp_path / ".claude" / "skills"), "--json", str(out)]
        )
        assert result.exit_code == 0
        data = json.loads(out.read_text(encoding="utf-8"))
        assert data["errors"] == 0
        assert data["total"] >= 1


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
        assert "score" in data["skills"][0]

    def test_quality_output_alias(self, tmp_path: Path):
        """--output works as an alias for --json."""
        _make_skill(tmp_path, "alias-skill", "qa")
        out = tmp_path / "quality_alias.json"
        result = CliRunner().invoke(
            cli, ["quality", "--dir", str(tmp_path / ".claude" / "skills"), "--output", str(out)]
        )
        assert result.exit_code == 0
        assert out.exists()
        data = json.loads(out.read_text(encoding="utf-8"))
        assert data["skills"][0]["name"] == "alias-skill"

    def test_quality_skips_broken_frontmatter(self, tmp_path: Path):
        broken = tmp_path / ".claude" / "skills" / "qa" / "broken"
        broken.mkdir(parents=True)
        (broken / "SKILL.md").write_text("---\nname: {unclosed\n---\n## Quick Start\nx\n", encoding="utf-8")
        result = CliRunner().invoke(cli, ["quality", "--dir", str(tmp_path / ".claude" / "skills")])
        assert result.exit_code == 0
        assert "Skills analyzed: 0" in _strip_ansi(result.output)


class TestCommandValidateErrors:
    def _write_broken_skill(self, root: Path, name: str) -> Path:
        skill_dir = root / ".claude" / "skills" / "qa" / name
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text(
            "---\nname: wrong-name\ncategory: qa\n---\nshort\n", encoding="utf-8"
        )
        return skill_dir

    def test_validate_reports_errors(self, tmp_path: Path):
        self._write_broken_skill(tmp_path, "broken-skill")
        result = CliRunner().invoke(cli, ["validate", "--dir", str(tmp_path / ".claude" / "skills")])
        assert result.exit_code == 0
        output = _strip_ansi(result.output)
        assert "Errors: 1" in output

    def test_validate_missing_dir_errors(self, tmp_path: Path):
        result = CliRunner().invoke(cli, ["validate", "--dir", str(tmp_path / "nope")])
        assert result.exit_code != 0
        assert "not found" in _strip_ansi(result.output)


class TestCommandInstall:
    def test_install_single_skill(self, tmp_path: Path):
        _make_skill(tmp_path, "install-me", "qa")
        target = tmp_path / "target" / ".claude" / "skills"
        result = CliRunner().invoke(
            cli, ["install", "install-me", "--target", str(target), "--dir", str(tmp_path / ".claude" / "skills")]
        )
        assert result.exit_code == 0
        assert (target / "qa" / "install-me" / "SKILL.md").exists()

    def test_install_missing_skill(self, tmp_path: Path):
        _make_skill(tmp_path, "other", "qa")
        result = CliRunner().invoke(
            cli, ["install", "ghost", "--target", str(tmp_path / "target"), "--dir", str(tmp_path / ".claude" / "skills")]
        )
        assert result.exit_code != 0
        assert "not found" in _strip_ansi(result.output)

    def test_install_overwrites_existing(self, tmp_path: Path):
        _make_skill(tmp_path, "dup", "qa")
        target = tmp_path / "target" / ".claude" / "skills"
        CliRunner().invoke(cli, ["install", "dup", "--target", str(target), "--dir", str(tmp_path / ".claude" / "skills")])
        # second install overwrites without error
        result = CliRunner().invoke(
            cli, ["install", "dup", "--target", str(target), "--dir", str(tmp_path / ".claude" / "skills")]
        )
        assert result.exit_code == 0
        assert "already exists" in _strip_ansi(result.output)

    def test_install_defaults_to_home_claude(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        _make_skill(tmp_path, "default-home", "qa")
        fake_home = tmp_path / "fakehome"
        fake_home.mkdir()
        monkeypatch.setattr("pathlib.Path.home", lambda: fake_home)
        result = CliRunner().invoke(
            cli, ["install", "default-home", "--dir", str(tmp_path / ".claude" / "skills")]
        )
        assert result.exit_code == 0
        assert (fake_home / ".claude" / "skills" / "qa" / "default-home" / "SKILL.md").exists()

    def test_install_not_in_bundled_fails(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
        _make_skill(tmp_path, "local-only", "qa")
        monkeypatch.chdir(tmp_path)
        result = CliRunner().invoke(cli, ["install", "local-only", "--target", str(tmp_path / "out")])
        # not in bundled library -> not found without --dir
        assert result.exit_code != 0
        assert "not found" in _strip_ansi(result.output)