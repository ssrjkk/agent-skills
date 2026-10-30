"""Tests for data models."""

from __future__ import annotations

from pathlib import Path

import pytest

from claude_skills.models import (
    Catalog,
    CatalogMetadata,
    QualityScore,
    Severity,
    Skill,
    SkillFile,
    SkillSet,
    ValidationResult,
    parse_frontmatter,
)


class TestSkill:
    def test_valid_name(self):
        assert Skill(name="test-skill", description="", category="qa", tags=[], models=[], version="1.0.0", path=Path("")).is_valid_name

    def test_invalid_name_with_uppercase(self):
        assert not Skill(name="Test-Skill", description="", category="qa", tags=[], models=[], version="1.0.0", path=Path("")).is_valid_name

    def test_invalid_name_with_leading_digit(self):
        assert Skill(name="123-test", description="", category="qa", tags=[], models=[], version="1.0.0", path=Path("")).is_valid_name

    def test_single_char_name(self):
        assert Skill(name="a", description="", category="qa", tags=[], models=[], version="1.0.0", path=Path("")).is_valid_name

    def test_valid_semver(self):
        assert Skill(name="t", description="", category="qa", tags=[], models=[], version="1.0.0", path=Path("")).is_valid_semver

    def test_two_part_version_matches_validator(self):
        # unified with W014 (^\d+\.\d+(\.\d+)?$) and the shipped RU files ("1.0")
        assert Skill(name="t", description="", category="qa", tags=[], models=[], version="1.0", path=Path("")).is_valid_semver

    def test_invalid_semver(self):
        assert not Skill(name="t", description="", category="qa", tags=[], models=[], version="1.0-beta", path=Path("")).is_valid_semver

    def test_invalid_version_format(self):
        assert not Skill(name="t", description="", category="qa", tags=[], models=[], version="v1.0.0", path=Path("")).is_valid_semver

    def test_dir_path(self):
        skill = Skill(name="t", description="", category="qa", tags=[], models=[], version="1.0.0", path=Path(".claude/skills/qa/t/SKILL.md"))
        assert skill.dir_path.name == "t"

    def test_category_path(self):
        skill = Skill(name="t", description="", category="qa", tags=[], models=[], version="1.0.0", path=Path(".claude/skills/qa/t/SKILL.md"))
        assert skill.category_path == "qa"

    def test_category_path_empty(self):
        skill = Skill(name="t", description="", category="qa", tags=[], models=[], version="1.0.0", path=Path(""))
        assert skill.category_path == ""


class TestQualityScore:
    def test_overall_calculation(self):
        score = QualityScore(completeness=100, depth=100, code_quality=100, freshness=100, bilingual=100)
        assert score.overall == 100.0

    def test_partial_score(self):
        score = QualityScore(completeness=50, depth=50, code_quality=50, freshness=50, bilingual=50)
        assert score.overall == 50.0

    def test_grade_a(self):
        assert QualityScore(completeness=100, depth=100, code_quality=100, freshness=100, bilingual=100).grade == "A"

    def test_grade_f(self):
        assert QualityScore(completeness=0, depth=0, code_quality=0, freshness=0, bilingual=0).grade == "F"

    def test_grade_boundaries(self):
        assert QualityScore(completeness=90, depth=90, code_quality=90, freshness=90, bilingual=90).grade == "A"
        assert QualityScore(completeness=80, depth=80, code_quality=80, freshness=80, bilingual=80).grade == "B"
        assert QualityScore(completeness=65, depth=65, code_quality=65, freshness=65, bilingual=65).grade == "C"
        assert QualityScore(completeness=50, depth=50, code_quality=50, freshness=50, bilingual=50).grade == "D"


class TestValidationResult:
    def test_str_format_error(self):
        vr = ValidationResult("path/to/skill", Severity.ERROR, "E001", "Test error")
        assert "ERROR" in str(vr)
        assert "E001" in str(vr)
        assert "Test error" in str(vr)

    def test_str_format_warning(self):
        vr = ValidationResult("path/to/skill", Severity.WARNING, "W001", "Test warning")
        assert "WARNING" in str(vr)

    def test_str_with_line(self):
        vr = ValidationResult("path/to/skill", Severity.ERROR, "E001", "Error", line=42)
        assert ":42" in str(vr)


class TestParseFrontmatter:
    def test_valid_frontmatter(self):
        fm, body, ok = parse_frontmatter("---\nname: test\n---\n# Body\ncontent")
        assert ok
        assert fm == {"name": "test"}
        assert "# Body\ncontent" in body

    def test_crlf_frontmatter(self):
        fm, body, ok = parse_frontmatter("---\r\nname: test\r\nversion: 1.0.0\r\n---\r\n## Section\r\ntext")
        assert ok
        assert fm is not None
        assert fm["name"] == "test"
        assert fm["version"] == "1.0.0"
        assert body.startswith("## Section")

    def test_missing_frontmatter(self):
        fm, _body, ok = parse_frontmatter("Just text without frontmatter")
        assert not ok
        assert fm is None

    def test_empty_frontmatter(self):
        fm, _body, ok = parse_frontmatter("---\n---\nbody content")
        assert not ok
        assert fm is None

    def test_non_dict_frontmatter(self):
        fm, _body, ok = parse_frontmatter("---\n[1, 2, 3]\n---\nbody")
        assert not ok
        assert fm is None

    def test_missing_closing_delimiter(self):
        fm, _body, ok = parse_frontmatter("---\nname: test\nno closing marker")
        assert not ok
        assert fm is None

    def test_invalid_yaml_error(self):
        fm, _body, ok = parse_frontmatter("---\nname: [unclosed\n---\nbody")
        assert not ok
        assert fm is None


class TestCatalog:
    @pytest.fixture
    def catalog(self):
        metadata = CatalogMetadata(
            total_skills=3, total_ru=1, domains=["ai", "backend", "qa"], bilingual=True
        )
        skills = [
            Skill(name="skill1", description="desc1", category="qa", tags=["test"], models=["sonnet"], version="1.0.0", path=Path(""), created="2026-01-01"),
            Skill(name="skill2", description="desc2", category="ai", tags=["ml"], models=["opus"], version="1.0.0", path=Path(""), has_ru=True),
            Skill(name="skill3", description="desc3", category="backend", tags=["api"], models=["haiku"], version="1.0.0", path=Path("")),
        ]
        return Catalog(metadata=metadata, skills=skills)

    def test_by_category(self, catalog):
        by_cat = catalog.by_category
        assert len(by_cat["qa"]) == 1
        assert len(by_cat["ai"]) == 1
        assert len(by_cat["backend"]) == 1

    def test_by_tag(self, catalog):
        by_tag = catalog.by_tag
        assert len(by_tag["test"]) == 1
        assert len(by_tag["ml"]) == 1

    def test_get_existing(self, catalog):
        s = catalog.get("skill1")
        assert s is not None
        assert s.name == "skill1"

    def test_get_missing(self, catalog):
        assert catalog.get("nonexistent") is None

    def test_catalog_metadata_totals(self, catalog):
        assert catalog.metadata.total_skills == 3
        assert catalog.metadata.total_ru == 1
        assert catalog.metadata.bilingual


class TestSkillSet:
    def test_empty(self):
        ss = SkillSet()
        assert ss.en_count == 0
        assert ss.ru_count == 0

    def test_counts(self):
        sf1 = SkillFile(en_path=Path("a/SKILL.md"))
        sf2 = SkillFile(en_path=Path("b/SKILL.md"), ru_path=Path("b/SKILL.ru.md"))
        ss = SkillSet(skills=[sf1, sf2])
        assert ss.en_count == 2
        assert ss.ru_count == 1


class TestSeverity:
    def test_enum_values(self):
        assert Severity.ERROR.value == "error"
        assert Severity.WARNING.value == "warning"
        assert Severity.INFO.value == "info"
