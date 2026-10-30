"""Property-based tests using Hypothesis."""

from __future__ import annotations

from pathlib import Path

from hypothesis import assume, given
from hypothesis import strategies as st

from claude_skills.models import QualityScore, Severity, Skill, ValidationResult
from claude_skills.quality import QualityAnalyzer, QualityReport


@given(st.text(alphabet="abcdefghijklmnopqrstuvwxyz-", min_size=1, max_size=50))
def test_skill_name_validation(name):
    assume(name)
    skill = Skill(
        name=name,
        description="desc",
        category="qa",
        tags=[],
        models=[],
        version="1.0.0",
        path=Path(name),
    )
    if name.startswith("-") or name.endswith("-"):
        assert not skill.is_valid_name
    else:
        assert skill.is_valid_name


@given(
    st.floats(min_value=0, max_value=100),
    st.floats(min_value=0, max_value=100),
    st.floats(min_value=0, max_value=100),
    st.floats(min_value=0, max_value=100),
    st.floats(min_value=0, max_value=100),
)
def test_quality_score_bounds(c, d, cq, f, b):
    score = QualityScore(completeness=c, depth=d, code_quality=cq, freshness=f, bilingual=b)
    assert 0 <= score.overall <= 100
    assert score.grade in ("A", "B", "C", "D", "F")


@given(st.sampled_from([Severity.ERROR, Severity.WARNING, Severity.INFO]))
def test_validation_result_severity(severity):
    vr = ValidationResult("path", severity, "C001", "Message")
    assert vr.severity == severity


@given(st.text(max_size=200))
def test_validation_result_always_has_code(body):
    vr = ValidationResult("path", Severity.INFO, "C001", body)
    assert "C001" in str(vr)


@given(
    st.lists(st.text(min_size=1, max_size=20), min_size=0, max_size=10, unique=True),
)
def test_quality_report_distribution(skill_names):
    assume(len(skill_names) <= 10)
    scores = {n: QualityScore(80, 80, 80, 80, 80) for n in skill_names}
    report = QualityReport(scores)
    assert sum(report.grade_distribution.values()) == len(skill_names)
    if len(skill_names) > 0:
        assert report.average.overall > 0


def test_analyzer_empty_body():
    from claude_skills.models import SkillFile

    sf = SkillFile(en_path=Path("dummy"), en_body="")
    analyzer = QualityAnalyzer()
    score = analyzer.analyze(sf)
    assert score.completeness == 0
    assert score.depth == 0


@given(st.integers(min_value=0, max_value=200))
def test_depth_never_exceeds_100(line_count):
    from pathlib import Path

    from claude_skills.models import SkillFile

    body = "\n".join([f"Line {i}" for i in range(line_count)])
    sf = SkillFile(en_path=Path("test"), en_body=body)
    analyzer = QualityAnalyzer()
    depth = analyzer._score_depth(sf)
    assert 0 <= depth <= 100
