"""Tests for catalog builder."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from claude_skills.catalog import CatalogBuilder


class TestCatalogBuilder:
    @pytest.fixture
    def builder(self, tmp_path: Path):
        skills_dir = tmp_path / ".claude" / "skills" / "qa" / "test-skill"
        skills_dir.mkdir(parents=True)
        en_skill = skills_dir / "SKILL.md"
        en_skill.write_text(
            "---\n"
            "name: test-skill\n"
            "description: A test skill\n"
            "category: qa\n"
            "tags: [testing, automation]\n"
            "models: [sonnet, opus]\n"
            "version: 1.0.0\n"
            "created: 2026-01-01\n"
            "---\n"
            "# Test Skill\n\n"
            "Quick Start section content\n\n"
            "Validation section content\n"
        )
        ru_skill = skills_dir / "SKILL.ru.md"
        ru_skill.write_text(
            "---\n"
            "name: test-skill\n"
            "description: Тестовый навык\n"
            "category: qa\n"
            "tags: [testing, russian]\n"
            "models: [sonnet, opus]\n"
            "version: 1.0.0\n"
            "language: ru\n"
            "original: test-skill\n"
            "---\n"
            "# Тестовый навык\n"
        )
        return CatalogBuilder(root=tmp_path)

    def test_scan_returns_skills(self, builder: CatalogBuilder):
        skills = builder.scan()
        assert len(skills) == 1
        assert skills[0].name == "test-skill"
        assert skills[0].category == "qa"
        assert skills[0].tags == ["testing", "automation"]
        assert skills[0].has_ru

    def test_build_catalog(self, builder: CatalogBuilder):
        catalog = builder.build_catalog()
        assert catalog.metadata.total_skills == 1
        assert catalog.metadata.total_ru == 1
        assert "qa" in catalog.metadata.domains
        assert catalog.skills[0].description == "A test skill"

    def test_to_json(self, builder: CatalogBuilder):
        catalog = builder.build_catalog()
        text = builder.to_json(catalog)
        data = json.loads(text)
        assert data["metadata"]["total_skills"] == 1
        assert len(data["skills"]) == 1
        assert data["skills"][0]["name"] == "test-skill"
        assert data["skills"][0]["tags"] == ["testing", "automation"]

    def test_to_json_writes_file(self, builder: CatalogBuilder, tmp_path: Path):
        catalog = builder.build_catalog()
        out = tmp_path / "catalog.json"
        builder.to_json(catalog, path=out)
        assert out.exists()
        data = json.loads(out.read_text(encoding="utf-8"))
        assert data["metadata"]["total_skills"] == 1

    def test_from_json(self, builder: CatalogBuilder, tmp_path: Path):
        catalog_in = builder.build_catalog()
        path = tmp_path / "catalog.json"
        builder.to_json(catalog_in, path=path)
        catalog_out = CatalogBuilder.from_json(path)
        assert catalog_out.metadata.total_skills == 1
        assert catalog_out.skills[0].name == "test-skill"

    def test_scan_skips_missing_frontmatter(self, tmp_path: Path):
        skills_dir = tmp_path / ".claude" / "skills" / "qa" / "no-fm"
        skills_dir.mkdir(parents=True)
        (skills_dir / "SKILL.md").write_text("# No frontmatter here\ncontent")
        builder = CatalogBuilder(root=tmp_path)
        skills = builder.scan()
        assert len(skills) == 0
        assert builder.skipped == ["qa/no-fm/SKILL.md"]

    def test_parse_list_from_yaml_list(self, builder: CatalogBuilder):
        result = builder._parse_list(["a", "b", "c"])
        assert result == ["a", "b", "c"]

    def test_parse_list_from_string(self, builder: CatalogBuilder):
        result = builder._parse_list("[a, b, c]")
        assert result == ["a", "b", "c"]

    def test_parse_list_empty(self, builder: CatalogBuilder):
        assert builder._parse_list([]) == []
        assert builder._parse_list("") == []
        assert builder._parse_list("[]") == []

    def test_parse_list_non_string_value(self, builder: CatalogBuilder):
        assert builder._parse_list(42) == []
        assert builder._parse_list(None) == []

    def test_unreadable_frontmatter_skipped(self, tmp_path: Path):
        skills_dir = tmp_path / ".claude" / "skills" / "qa" / "bad-enc"
        skills_dir.mkdir(parents=True)
        (skills_dir / "SKILL.md").write_bytes(b"\xff\xfe\x00\xff not valid utf-8")
        builder = CatalogBuilder(root=tmp_path)
        skills = builder.scan()
        assert len(skills) == 0

    def test_missing_directory(self, tmp_path: Path):
        builder = CatalogBuilder(root=tmp_path)
        skills = builder.scan()
        assert skills == []


class TestCatalogBuilderDuplicate:
    def test_scan_deduplicates(self, tmp_path: Path):
        dir1 = tmp_path / ".claude" / "skills" / "qa" / "same-name"
        dir1.mkdir(parents=True)
        (dir1 / "SKILL.md").write_text(
            "---\nname: same-name\ndescription: First\ncategory: qa\ntags: []\nmodels: []\nversion: 1.0.0\n---\nContent"
        )
        dir2 = tmp_path / ".claude" / "skills" / "ai" / "same-name"
        dir2.mkdir(parents=True)
        (dir2 / "SKILL.md").write_text(
            "---\nname: same-name\ndescription: Second\ncategory: ai\ntags: []\nmodels: []\nversion: 1.0.0\n---\nContent"
        )
        builder = CatalogBuilder(root=tmp_path)
        skills = builder.scan()
        assert len(skills) == 1
        # sorted order: ai/same-name wins, qa/same-name is reported, not dropped silently
        assert skills[0].category == "ai"
        assert builder.duplicates == ["same-name (qa/same-name/SKILL.md)"]

    def test_from_json_rejects_nameless_entry(self, tmp_path: Path):
        path = tmp_path / "catalog.json"
        path.write_text(
            json.dumps({"metadata": {}, "skills": [{"description": "no name here"}]}),
            encoding="utf-8",
        )
        with pytest.raises(ValueError, match="no 'name'"):
            CatalogBuilder.from_json(path)
