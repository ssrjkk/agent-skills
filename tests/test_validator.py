"""Tests for the validator."""

from __future__ import annotations

from pathlib import Path

import pytest

from claude_skills.models import Severity
from claude_skills.validator import SkillValidator, ValidationPipeline


class TestSkillValidator:
    @pytest.fixture
    def validator(self):
        return SkillValidator()

    def test_valid_skill(self, validator: SkillValidator, tmp_path: Path):
        path = tmp_path / "test-skill" / "SKILL.md"
        path.parent.mkdir(parents=True)
        path.write_text(
            "---\n"
            "name: test-skill\n"
            "description: A skill\n"
            "category: qa\n"
            "tags: [testing]\n"
            "models: [sonnet, opus]\n"
            "version: 1.0.0\n"
            "created: 2026-01-01\n"
            "---\n"
            "# Test Skill\n\n"
            "## Quick Start\n\nContent\n\n"
            "## Validation\n\nContent\n"
        )
        results = validator.validate_skill_file(path)
        errors = [r for r in results if r.severity == Severity.ERROR]
        assert len(errors) == 0

    def test_filler_words_are_info_only(self, validator: SkillValidator, tmp_path: Path):
        path = tmp_path / "test" / "SKILL.md"
        path.parent.mkdir(parents=True)
        path.write_text(
            "---\nname: test\ndescription: We will revolutionize your workflow\n"
            "category: qa\ntags: []\nmodels: []\nversion: 1.0.0\n---\n"
            "# Test\n\n## Quick Start\n\nContent here.\n\n## Validation\n\nContent here.\n"
        )
        results = validator.validate_skill_file(path)
        codes = [r.code for r in results]
        assert "I030" in codes
        assert not [r for r in results if r.severity == Severity.ERROR]

    def test_filler_words_in_ban_list_are_skipped(self, validator: SkillValidator, tmp_path: Path):
        path = tmp_path / "test" / "SKILL.md"
        path.parent.mkdir(parents=True)
        path.write_text(
            "---\nname: test\ndescription: Plain copy guide\n"
            "category: qa\ntags: []\nmodels: []\nversion: 1.0.0\n---\n"
            "# Test\n\n## Quick Start\n\nBan filler: revolutionize, supercharge, cutting edge.\n\n"
            "## Validation\n\nWrite plainly.\n"
        )
        results = validator.validate_skill_file(path)
        assert "I030" not in [r.code for r in results]

    def test_ru_without_cyrillic_warns(self, validator: SkillValidator, tmp_path: Path):
        d = tmp_path / "test"
        d.mkdir(parents=True)
        (d / "SKILL.md").write_text(
            "---\nname: test\ndescription: desc\ncategory: qa\ntags: []\nmodels: []\nversion: 1.0.0\n---\n"
            "# Test\n\n## Quick Start\n\nContent here.\n\n## Validation\n\nContent here.\n"
        )
        path = d / "SKILL.ru.md"
        path.write_text(
            "---\nname: test\ndescription: desc\ncategory: qa\ntags: []\nmodels: []\nversion: 1.0\n---\n"
            "# Test\n\nJust an English copy of the whole thing without translation.\n"
        )
        results = validator.validate_skill_file(path)
        assert any(r.code == "W040" for r in results)
        assert not [r for r in results if r.severity == Severity.ERROR]

    def test_ru_stub_warns_on_length(self, validator: SkillValidator, tmp_path: Path):
        d = tmp_path / "test"
        d.mkdir(parents=True)
        (d / "SKILL.md").write_text(
            "---\nname: test\ndescription: desc\ncategory: qa\ntags: []\nmodels: []\nversion: 1.0.0\n---\n"
            "# Test\n\n" + ("Full English body sentence number one. " * 100) + "\n"
        )
        path = d / "SKILL.ru.md"
        path.write_text(
            "---\nname: test\ndescription: desc\ncategory: qa\ntags: []\nmodels: []\nversion: 1.0\n---\n"
            "# Тест\n\nКороткий перевод, который явно не покрывает оригинал целиком и полностью.\n",
            encoding="utf-8",
        )
        results = validator.validate_skill_file(path)
        assert any(r.code == "W041" for r in results)
        assert not any(r.code == "W040" for r in results)

    def test_good_ru_passes_clean(self, validator: SkillValidator, tmp_path: Path):
        d = tmp_path / "test"
        d.mkdir(parents=True)
        (d / "SKILL.md").write_text(
            "---\nname: test\ndescription: desc\ncategory: qa\ntags: []\nmodels: []\nversion: 1.0.0\n---\n"
            "# Test\n\n" + ("Full English body sentence number one. " * 20) + "\n"
        )
        path = d / "SKILL.ru.md"
        path.write_text(
            "---\nname: test\ndescription: desc\ncategory: qa\ntags: []\nmodels: []\nversion: 1.0\n---\n"
            "# Тест\n\n" + ("Полноценный русский перевод каждого предложения оригинала. " * 20) + "\n",
            encoding="utf-8",
        )
        results = validator.validate_skill_file(path)
        assert not [r.code for r in results if r.code in ("W040", "W041")]

    def test_ru_code_fences_excluded_from_prose(self, validator: SkillValidator, tmp_path: Path):
        d = tmp_path / "test"
        d.mkdir(parents=True)
        (d / "SKILL.md").write_text(
            "---\nname: test\ndescription: desc\ncategory: qa\ntags: []\nmodels: []\nversion: 1.0.0\n---\n"
            "# Test\n\n" + ("Full English body sentence number one. " * 20) + "\n"
        )
        path = d / "SKILL.ru.md"
        path.write_text(
            "---\nname: test\ndescription: desc\ncategory: qa\ntags: []\nmodels: []\nversion: 1.0\n---\n"
            "# Тест\n\n"
            + ("Полноценный русский перевод каждого предложения оригинала. " * 20)
            + "\n```python\nprint('latin code stays out of prose metrics')\n```\n",
            encoding="utf-8",
        )
        results = validator.validate_skill_file(path)
        assert not [r.code for r in results if r.code in ("W040", "W041")]

    def test_ru_without_english_original_skips_length_check(self, validator: SkillValidator, tmp_path: Path):
        d = tmp_path / "test"
        d.mkdir(parents=True)
        path = d / "SKILL.ru.md"
        path.write_text(
            "---\nname: test\ndescription: desc\ncategory: qa\ntags: []\nmodels: []\nversion: 1.0\n---\n"
            "# Тест\n\n"
            + ("Полноценный русский перевод без английского оригинала рядом. " * 10)
            + "\n",
            encoding="utf-8",
        )
        results = validator.validate_skill_file(path)
        assert not [r.code for r in results if r.code in ("W040", "W041")]

    def test_missing_frontmatter(self, validator: SkillValidator, tmp_path: Path):
        path = tmp_path / "test" / "SKILL.md"
        path.parent.mkdir(parents=True)
        path.write_text("Just content without frontmatter\n")
        results = validator.validate_skill_file(path)
        errors = [r for r in results if r.severity == Severity.ERROR]
        assert any("E010" in r.code for r in errors)

    def test_missing_required_fields(self, validator: SkillValidator, tmp_path: Path):
        path = tmp_path / "test" / "SKILL.md"
        path.parent.mkdir(parents=True)
        path.write_text("---\nname: test\n---\nContent\n")
        results = validator.validate_skill_file(path)
        errors = [r for r in results if r.severity == Severity.ERROR]
        assert any("E020" in r.code for r in errors)

    def test_short_body_warning(self, validator: SkillValidator, tmp_path: Path):
        path = tmp_path / "test" / "SKILL.md"
        path.parent.mkdir(parents=True)
        path.write_text(
            "---\n"
            "name: test\ndescription: desc\ncategory: qa\ntags: []\nmodels: []\nversion: 1.0.0\n"
            "---\n"
            "Short\n"
        )
        results = validator.validate_skill_file(path)
        warnings = [r for r in results if r.severity == Severity.WARNING]
        assert any("W020" in r.code for r in warnings)

    def test_unbalanced_code_fences(self, validator: SkillValidator, tmp_path: Path):
        path = tmp_path / "test" / "SKILL.md"
        path.parent.mkdir(parents=True)
        path.write_text(
            "---\n"
            "name: test\ndescription: desc\ncategory: qa\ntags: []\nmodels: []\nversion: 1.0.0\n"
            "---\n"
            "# Test\n\n"
            "```python\nprint('hello')\n```\n"
            "```bash\necho hi\n"
        )
        results = validator.validate_skill_file(path)
        errors = [r for r in results if r.severity == Severity.ERROR]
        assert any("E040" in r.code for r in errors)

    def test_placeholder_name(self, validator: SkillValidator, tmp_path: Path):
        path = tmp_path / "skill-0001" / "SKILL.md"
        path.parent.mkdir(parents=True)
        path.write_text(
            "---\n"
            "name: skill-0001\ndescription: desc\ncategory: qa\ntags: []\nmodels: []\nversion: 1.0.0\n"
            "---\n"
            "## Quick Start\n\nContent\n\n## Validation\n\nContent\n"
        )
        results = validator.validate_skill_file(path)
        warnings = [r for r in results if r.severity == Severity.WARNING]
        assert any("W011" in r.code for r in warnings)

    def test_duplicate_tags(self, validator: SkillValidator, tmp_path: Path):
        path = tmp_path / "test" / "SKILL.md"
        path.parent.mkdir(parents=True)
        path.write_text(
            "---\n"
            "name: test\ndescription: desc\ncategory: qa\n"
            "tags: [qa, basics, qa]\nmodels: [sonnet]\nversion: 1.0.0\n"
            "---\n"
            "## Quick Start\n\nContent\n\n## Validation\n\nContent\n"
        )
        results = validator.validate_skill_file(path)
        warnings = [r for r in results if r.severity == Severity.WARNING]
        assert any("W013" in r.code for r in warnings)

    def test_default_model_detection(self, validator: SkillValidator, tmp_path: Path):
        path = tmp_path / "test" / "SKILL.md"
        path.parent.mkdir(parents=True)
        path.write_text(
            "---\n"
            "name: test\ndescription: desc\ncategory: qa\n"
            "tags: [qa]\nmodels: [gpt-4, claude-3]\nversion: 1.0.0\n"
            "---\n"
            "## Quick Start\n\nContent\n\n## Validation\n\nContent\n"
        )
        results = validator.validate_skill_file(path)
        infos = [r for r in results if r.severity == Severity.INFO]
        assert any("I010" in r.code for r in infos)

    def test_unknown_category(self, validator: SkillValidator, tmp_path: Path):
        path = tmp_path / "test" / "SKILL.md"
        path.parent.mkdir(parents=True)
        path.write_text(
            "---\n"
            "name: test\ndescription: desc\ncategory: nonexistent\n"
            "tags: []\nmodels: []\nversion: 1.0.0\n"
            "---\n"
            "## Quick Start\n\nContent\n\n## Validation\n\nContent\n"
        )
        results = validator.validate_skill_file(path)
        warnings = [r for r in results if r.severity == Severity.WARNING]
        assert any("W012" in r.code for r in warnings)

    def test_unreadable_file(self, validator: SkillValidator, tmp_path: Path):
        path = tmp_path / "test" / "SKILL.md"
        path.parent.mkdir(parents=True)
        path.write_bytes(b"\xff\xfe invalid utf8 that cannot decode \x00")
        path.write_bytes(bytes([0xff, 0xfe, 0x00, 0xff]))
        results = validator.validate_skill_file(path)
        errors = [r for r in results if r.severity == Severity.ERROR]
        assert any("E001" in r.code for r in errors)

    def test_malformed_frontmatter(self, validator: SkillValidator, tmp_path: Path):
        path = tmp_path / "test" / "SKILL.md"
        path.parent.mkdir(parents=True)
        path.write_text("---\nname: [unclosed\n---\nContent\n")
        results = validator.validate_skill_file(path)
        assert any("E011" in r.code for r in results)

    def test_empty_frontmatter(self, validator: SkillValidator, tmp_path: Path):
        path = tmp_path / "test" / "SKILL.md"
        path.parent.mkdir(parents=True)
        path.write_text("---\n# not a dict\n---\nContent\n")
        results = validator.validate_skill_file(path)
        assert any("E011" in r.code for r in results)

    def test_name_mismatch_warning(self, validator: SkillValidator, tmp_path: Path):
        path = tmp_path / "actual-name" / "SKILL.md"
        path.parent.mkdir(parents=True)
        path.write_text(
            "---\n"
            "name: other-name\ndescription: desc\ncategory: qa\n"
            "tags: []\nmodels: []\nversion: 1.0.0\n"
            "---\n"
            "## Quick Start\n\nContent\n\n## Validation\n\nContent\n"
        )
        results = validator.validate_skill_file(path)
        warnings = [r for r in results if r.severity == Severity.WARNING]
        assert any("W010" in r.code for r in warnings)

    def test_nonstandard_version(self, validator: SkillValidator, tmp_path: Path):
        path = tmp_path / "test" / "SKILL.md"
        path.parent.mkdir(parents=True)
        path.write_text(
            "---\n"
            "name: test\ndescription: desc\ncategory: qa\n"
            "tags: []\nmodels: []\nversion: 1.0-beta\n"
            "---\n"
            "## Quick Start\n\nContent\n\n## Validation\n\nContent\n"
        )
        results = validator.validate_skill_file(path)
        assert any("W014" in r.code for r in results)

    def test_critically_short_body(self, validator: SkillValidator, tmp_path: Path):
        path = tmp_path / "test" / "SKILL.md"
        path.parent.mkdir(parents=True)
        path.write_text(
            "---\n"
            "name: test\ndescription: desc\ncategory: qa\n"
            "tags: []\nmodels: []\nversion: 1.0.0\n"
            "---\n"
            "Tiny.\n"
        )
        results = validator.validate_skill_file(path)
        codes = [r.code for r in results]
        assert "W020" in codes
        assert "W030" in codes

    def test_todo_placeholder(self, validator: SkillValidator, tmp_path: Path):
        path = tmp_path / "test" / "SKILL.md"
        path.parent.mkdir(parents=True)
        path.write_text(
            "---\n"
            "name: test\ndescription: desc\ncategory: qa\n"
            "tags: []\nmodels: []\nversion: 1.0.0\n"
            "---\n"
            "## Quick Start\nTODO: write this later\n## Validation\nContent\n"
        )
        results = validator.validate_skill_file(path)
        assert any("W021" in r.code for r in results)

    def test_empty_dict_frontmatter(self, validator: SkillValidator, tmp_path: Path):
        path = tmp_path / "test" / "SKILL.md"
        path.parent.mkdir(parents=True)
        path.write_text("---\n{}\n---\nContent\n")
        results = validator.validate_skill_file(path)
        assert any(r.code in ("E011", "E012") for r in results)

    def test_missing_info_sections(self, validator: SkillValidator, tmp_path: Path):
        path = tmp_path / "test" / "SKILL.md"
        path.parent.mkdir(parents=True)
        path.write_text(
            "---\n"
            "name: test\ndescription: desc\ncategory: qa\n"
            "tags: []\nmodels: []\nversion: 1.0.0\n"
            "---\n"
            "No sections here, just prose.\n"
        )
        results = validator.validate_skill_file(path)
        infos = [r for r in results if r.severity == Severity.INFO]
        assert any("I020" in r.code for r in infos)


class TestValidationPipeline:
    @pytest.fixture
    def pipeline(self, tmp_path: Path):
        skills_dir = tmp_path / ".claude" / "skills"
        for cat, name in [("qa", "skill-a"), ("ai", "skill-b"), ("backend", "skill-c")]:
            path = skills_dir / cat / name / "SKILL.md"
            path.parent.mkdir(parents=True)
            path.write_text(
                "---\n"
                f"name: {name}\ndescription: desc\ncategory: {cat}\n"
                "tags: [test]\nmodels: [sonnet]\nversion: 1.0.0\n"
                "---\n"
                "# Test\n\n## Quick Start\n\nContent\n\n## Validation\n\nContent\n"
            )
        return ValidationPipeline(skills_dir)

    def test_run_all(self, pipeline: ValidationPipeline):
        results = pipeline.run_all()
        assert len(results) == 3
        assert "qa/skill-a" in results
        assert "ai/skill-b" in results
        assert "backend/skill-c" in results

    def test_run_all_keeps_same_named_dirs_in_different_domains(
        self, pipeline: ValidationPipeline, tmp_path: Path
    ):
        dup = tmp_path / ".claude" / "skills" / "ai" / "skill-a" / "SKILL.md"
        dup.parent.mkdir(parents=True)
        dup.write_text(
            "---\nname: skill-a\ndescription: desc\ncategory: ai\n"
            "tags: [test]\nmodels: [sonnet]\nversion: 1.0.0\n"
            "---\n# Test\n\n## Quick Start\n\nContent\n\n## Validation\n\nContent\n"
        )
        results = pipeline.run_all()
        assert "qa/skill-a" in results
        assert "ai/skill-a" in results
        assert len(results) == 4

    def test_run_all_no_errors(self, pipeline: ValidationPipeline):
        results = pipeline.run_all()
        for name, res in results.items():
            errors = [r for r in res if r.severity == Severity.ERROR]
            assert len(errors) == 0, f"{name} has errors: {errors}"

    def test_report(self, pipeline: ValidationPipeline):
        results = pipeline.run_all()
        report = pipeline.report(results)
        assert report["total"] == 3
        assert report["errors"] == 0

    def test_report_counts_info_and_warnings(self, pipeline: ValidationPipeline, tmp_path: Path):
        path = tmp_path / ".claude" / "skills" / "qa" / "skill-bad" / "SKILL.md"
        path.parent.mkdir(parents=True)
        path.write_text(
            "---\nname: skill-bad\ndescription: desc\ncategory: qa\n"
            "tags: []\nmodels: []\nversion: 1.0.0\n"
            "---\n## Quick Start\nContent\n"
        )
        results = pipeline.run_all()
        report = pipeline.report(results)
        assert report["total"] == 4
        assert report["errors"] == 0
        assert report["info"] >= 1
        assert "warning_details" in report
        assert len(report["warning_details"]) <= 50

    def test_report_counts_errors(self, pipeline: ValidationPipeline, tmp_path: Path):
        path = tmp_path / ".claude" / "skills" / "qa" / "skill-broken" / "SKILL.md"
        path.parent.mkdir(parents=True)
        path.write_text("Just content without any frontmatter at all\n")
        results = pipeline.run_all()
        report = pipeline.report(results)
        assert report["total"] == 4
        assert report["errors"] >= 1
        assert report["error_details"]

    def test_run_ru_all(self, pipeline: ValidationPipeline, tmp_path: Path):
        ru_path = tmp_path / ".claude" / "skills" / "qa" / "skill-a" / "SKILL.ru.md"
        ru_path.write_text(
            "---\nname: skill-a\ndescription: desc-ru\ncategory: qa\ntags: [test]\nmodels: [sonnet]\nversion: 1.0.0\nlanguage: ru\n---\nContent"
        )
        results = pipeline.run_ru_all()
        assert "qa/skill-a" in results
