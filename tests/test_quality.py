"""Tests for the quality analyzer."""

from __future__ import annotations

import datetime
from pathlib import Path

import pytest

from claude_skills.models import QualityScore, SkillFile
from claude_skills.quality import QualityAnalyzer, QualityReport


class TestQualityAnalyzer:
    @pytest.fixture
    def analyzer(self):
        return QualityAnalyzer()

    def _make_skill_file(self, body: str, ru_body: str = "", created: str = "", models: str = "") -> SkillFile:
        sf = SkillFile(en_path=Path("test/SKILL.md"), en_body=body, en_content=f"---\n---\n{body}")
        if created:
            sf.en_frontmatter = {"created": created, "models": models}
        if ru_body:
            sf.ru_path = Path("test/SKILL.ru.md")
            sf.ru_body = ru_body
            sf.ru_content = f"---\n---\n{ru_body}"
        return sf

    def test_complete_skill_score(self, analyzer: QualityAnalyzer):
        body = "## Quick Start\nContent\n## When to Use\nContent\n## Step-by-Step\nContent\n## Examples\nContent\n## Validation\nContent"
        sf = self._make_skill_file(body=body, created="2026-06-01", ru_body="## Быстрый старт\n\n## Когда использовать\n")
        score = analyzer.analyze(sf)
        assert score.completeness > 80
        assert score.depth > 0
        assert score.bilingual > 0

    def test_empty_skill_score(self, analyzer: QualityAnalyzer):
        sf = self._make_skill_file(body="")
        score = analyzer.analyze(sf)
        assert score.completeness == 0.0
        assert score.depth == 0.0
        assert score.overall > 0  # bilingual might be > 0 from freshness

    def test_grade_a_for_complete_advanced_skill(self, analyzer: QualityAnalyzer):
        sections = ["Quick Start", "When to Use", "Best Practices", "Step-by-Step",
                    "Examples", "Validation", "Troubleshooting", "Dependencies"]
        parts = []
        for s in sections:
            parts.append("## " + s)
            parts.extend(f"Detail line {j} for {s}" for j in range(12))
        body = "\n".join(parts) + "\n" + ("```python\nx = 1\n```\n" * 4)
        sf = self._make_skill_file(body=body, created="2026-09-28",
                                   ru_body="\n".join("## " + s for s in ["Быстрый старт", "Когда использовать", "Практики", "Шаги", "Примеры", "Валидация", "Устранение", "Зависимости"]))
        score = analyzer.analyze(sf)
        assert score.overall >= 99.5
        assert score.grade == "A"

    def test_depth_calculation(self, analyzer: QualityAnalyzer):
        short = self._make_skill_file(body="Line1\nLine2\n")
        assert analyzer._score_depth(short) < 50
        long_body = "\n".join([f"Line {i}" for i in range(80)])
        long = self._make_skill_file(body=long_body)
        assert analyzer._score_depth(long) >= 80

    def test_code_quality_no_code(self, analyzer: QualityAnalyzer):
        sf = self._make_skill_file(body="Just text\nNo code blocks\n")
        assert analyzer._score_code_quality(sf) < 30

    def test_code_quality_with_fences(self, analyzer: QualityAnalyzer):
        sf = self._make_skill_file(body="Text\n```python\nx=1\n```\nMore\n```bash\nls\n```\nEnd\n")
        assert analyzer._score_code_quality(sf) >= 70

    def test_freshness_recent(self, analyzer: QualityAnalyzer):
        recent = datetime.datetime.now(tz=datetime.timezone.utc).date() - datetime.timedelta(days=10)
        sf = self._make_skill_file(body="Content", created=recent.isoformat())
        assert analyzer._score_freshness(sf) == 100.0

    def test_freshness_old(self, analyzer: QualityAnalyzer):
        old = datetime.datetime.now(tz=datetime.timezone.utc).date() - datetime.timedelta(days=400)
        sf = self._make_skill_file(body="Content", created=old.isoformat())
        assert analyzer._score_freshness(sf) < 80

    def test_freshness_no_date(self, analyzer: QualityAnalyzer):
        sf = self._make_skill_file(body="Content")
        assert analyzer._score_freshness(sf) == 30.0

    def test_freshness_pyaml_date_object_regression(self, analyzer: QualityAnalyzer):
        from datetime import date

        sf = self._make_skill_file(body="Content")
        today = datetime.datetime.now(tz=datetime.timezone.utc).date()
        sf.en_frontmatter = {"created": date(today.year, today.month, today.day)}
        assert analyzer._score_freshness(sf) == 100.0

    def test_freshness_updated_overrides_created(self, analyzer: QualityAnalyzer):
        sf = self._make_skill_file(body="Content")
        today = datetime.datetime.now(tz=datetime.timezone.utc).date()
        sf.en_frontmatter = {"created": "2025-01-01", "updated": today.isoformat()}
        assert analyzer._score_freshness(sf) >= 80

    def test_freshness_iso_with_z_suffix(self, analyzer: QualityAnalyzer):
        sf = self._make_skill_file(body="Content")
        today = datetime.datetime.now(tz=datetime.timezone.utc).date()
        iso = f"{today.isoformat()}T12:00:00Z"
        sf.en_frontmatter = {"updated": iso}
        assert analyzer._score_freshness(sf) == 100.0

    def test_freshness_datetime_object(self, analyzer: QualityAnalyzer):
        sf = self._make_skill_file(body="Content")
        today = datetime.datetime.now(tz=datetime.timezone.utc)
        sf.en_frontmatter = {"updated": today}
        assert analyzer._score_freshness(sf) == 100.0

    def test_freshness_created_fallback_two_digit_days(self, analyzer: QualityAnalyzer):
        sf = self._make_skill_file(body="Content")
        old = datetime.datetime.now(tz=datetime.timezone.utc).date() - datetime.timedelta(days=45)
        sf.en_frontmatter = {"created": old.isoformat()}
        assert analyzer._score_freshness(sf) == 80.0

    def test_bilingual_no_ru(self, analyzer: QualityAnalyzer):
        sf = self._make_skill_file(body="Content")
        assert analyzer._score_bilingual(sf) == 0.0

    def test_bilingual_with_ru(self, analyzer: QualityAnalyzer):
        sf = self._make_skill_file(body="EN content\n## Quick Start\nMore", ru_body="RU content\n## Быстрый старт\nMore")
        assert analyzer._score_bilingual(sf) > 0

    def test_bilingual_ru_path_but_empty_body(self, analyzer: QualityAnalyzer):
        sf = self._make_skill_file(body="## Quick Start\nContent", ru_body="")
        sf.ru_path = Path("test/SKILL.ru.md")
        sf.ru_content = ""
        assert analyzer._score_bilingual(sf) == 10.0

    def test_bilingual_ru_content_without_body(self, analyzer: QualityAnalyzer):
        sf = self._make_skill_file(body="## Quick Start\nContent")
        sf.ru_path = Path("test/SKILL.ru.md")
        sf.ru_content = "### body never extracted"
        sf.ru_body = ""
        assert analyzer._score_bilingual(sf) == 10.0

    def test_depth_sub_10_lines(self, analyzer: QualityAnalyzer):
        sf = self._make_skill_file(body="a\nb\nc\nd\ne")
        assert analyzer._score_depth(sf) == 25.0

    def test_depth_linear_range(self, analyzer: QualityAnalyzer):
        body = "\n".join(f"Line {i}" for i in range(30))
        sf = self._make_skill_file(body=body)
        score = analyzer._score_depth(sf)
        assert 10 < score < 100

    def test_code_quality_two_fences(self, analyzer: QualityAnalyzer):
        sf = self._make_skill_file(body="a\n```python\nx\n```\nb\n")
        assert analyzer._score_code_quality(sf) == 70.0

    def test_code_quality_inline_code(self, analyzer: QualityAnalyzer):
        sf = self._make_skill_file(body="Use `foo()` and `bar()` plus `baz()` and `qux()` with `last()`.\n")
        assert analyzer._score_code_quality(sf) == 50.0

    def test_freshness_greater_than_180_days(self, analyzer: QualityAnalyzer):
        old = datetime.datetime.now(tz=datetime.timezone.utc).date() - datetime.timedelta(days=400)
        sf = self._make_skill_file(body="Content", created=old.isoformat())
        score = analyzer._score_freshness(sf)
        assert 10.0 <= score < 60.0

    def test_freshness_invalid_value(self, analyzer: QualityAnalyzer):
        sf = self._make_skill_file(body="Content", created="not-a-date")
        assert analyzer._score_freshness(sf) == 30.0

    def test_completeness_sections(self, analyzer: QualityAnalyzer):
        sf = self._make_skill_file(body="## Quick Start\nContent\n## Validation\nContent")
        score = analyzer._score_completeness(sf)
        assert score > 30  # 2/5 sections + partial frontmatter
        assert score < 100

    def test_overall_zero_edge_case(self, analyzer: QualityAnalyzer):
        sf = self._make_skill_file(body="")
        score = analyzer.analyze(sf)
        assert score.overall >= 0


class TestQualityReport:
    @pytest.fixture
    def scores(self):
        return {
            "skill-a": QualityScore(90, 90, 90, 90, 90),
            "skill-b": QualityScore(70, 70, 70, 70, 70),
            "skill-c": QualityScore(30, 30, 30, 30, 30),
        }

    def test_average(self, scores: dict):
        report = QualityReport(scores)
        avg = report.average
        assert avg.completeness == pytest.approx(63.33, 0.1)
        assert avg.overall == pytest.approx(63.33, 0.1)

    def test_grade_distribution(self, scores: dict):
        report = QualityReport(scores)
        dist = report.grade_distribution
        assert dist["A"] == 1
        assert dist["B"] == 0
        assert dist["C"] == 1
        assert dist["F"] == 1

    def test_top_skills(self, scores: dict):
        report = QualityReport(scores)
        top = report.top_skills(2)
        assert len(top) == 2
        assert top[0][0] == "skill-a"

    def test_bottom_skills(self, scores: dict):
        report = QualityReport(scores)
        bottom = report.bottom_skills(2)
        assert len(bottom) == 2
        assert bottom[0][0] == "skill-c"

    def test_summary_contains_key_metrics(self, scores: dict):
        report = QualityReport(scores)
        summary = report.summary()
        assert "QUALITY REPORT" in summary
        assert "63" in summary
        assert "A" in summary

    def test_empty_report(self):
        report = QualityReport({})
        avg = report.average
        assert avg.overall == 0.0
        assert avg.grade == "F"
        assert report.grade_distribution["F"] == 0
