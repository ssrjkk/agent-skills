from __future__ import annotations

import datetime
from typing import ClassVar

from claude_skills.models import QualityScore, SkillFile


class QualityAnalyzer:
    SECTION_VARIANTS: ClassVar[dict[str, list[str]]] = {
        "Quick Start": ["Quick Start"],
        "When to Use": ["When to Use"],
        "Step-by-Step": ["Step-by-Step"],
        "Examples": ["Examples"],
        "Validation": ["Validation"],
    }

    def analyze(self, skill_file: SkillFile) -> QualityScore:
        return QualityScore(
            completeness=self._score_completeness(skill_file),
            depth=self._score_depth(skill_file),
            code_quality=self._score_code_quality(skill_file),
            freshness=self._score_freshness(skill_file),
            bilingual=self._score_bilingual(skill_file),
        )

    def _score_completeness(self, skill: SkillFile) -> float:
        if not skill.en_body:
            return 0.0
        score = 0.0
        for variants in self.SECTION_VARIANTS.values():
            if any(v in skill.en_body for v in variants):
                score += 100.0 / len(self.SECTION_VARIANTS)
        has_frontmatter = bool(skill.en_frontmatter)
        if has_frontmatter:
            present = [k for k in ("name", "description", "category", "tags", "models", "version") if k in skill.en_frontmatter]
            score += 10.0 * (len(present) / 6.0)
        return min(100.0, score)

    def _score_depth(self, skill: SkillFile) -> float:
        body = skill.en_body or ""
        lines = body.strip().split("\n") if body else []
        if len(lines) < 10:
            return max(0, len(lines) * 5)
        if len(lines) >= 70:
            return 100.0
        return 10 + (len(lines) - 10) * (90.0 / 60.0)

    def _score_code_quality(self, skill: SkillFile) -> float:
        body = skill.en_body or ""
        fence_count = body.count("```")
        if fence_count >= 4:
            return 100.0
        if fence_count >= 2:
            return 70.0
        inline_code = body.count("`")
        if inline_code >= 5:
            return 50.0
        return 20.0 if inline_code > 0 else 0.0

    def _score_freshness(self, skill: SkillFile) -> float:
        last = skill.en_frontmatter.get("updated") or skill.en_frontmatter.get("created")
        if not last:
            return 30.0
        try:
            if isinstance(last, datetime.datetime):
                dt = last
            elif isinstance(last, datetime.date):
                dt = datetime.datetime.combine(last, datetime.time.min)
            else:
                iso = str(last)
                iso = iso.replace("Z", "+00:00") if iso.endswith("Z") else iso
                dt = datetime.datetime.fromisoformat(iso)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=datetime.timezone.utc)
            days_old = (datetime.datetime.now(tz=datetime.timezone.utc) - dt).days
            if days_old < 30:
                return 100.0
            if days_old < 90:
                return 80.0
            if days_old < 180:
                return 60.0
            return max(10.0, 100.0 - days_old * 0.2)
        except (ValueError, TypeError):
            return 30.0

    def _score_bilingual(self, skill: SkillFile) -> float:
        if not skill.ru_path:
            return 0.0
        if not skill.ru_content:
            return 10.0
        ru_body = (skill.ru_body or "").strip()
        en_body = (skill.en_body or "").strip()
        if not ru_body or not en_body:
            return 10.0
        en_sections = en_body.count("\n## ")
        ru_sections = ru_body.count("\n## ")
        if ru_sections >= en_sections:
            return 100.0
        return 50.0 if ru_sections > 0 else 10.0


class QualityReport:
    def __init__(self, scores: dict[str, QualityScore]):
        self.scores = scores

    @property
    def average(self) -> QualityScore:
        if not self.scores:
            return QualityScore()
        n = len(self.scores)
        return QualityScore(
            completeness=sum(s.completeness for s in self.scores.values()) / n,
            depth=sum(s.depth for s in self.scores.values()) / n,
            code_quality=sum(s.code_quality for s in self.scores.values()) / n,
            freshness=sum(s.freshness for s in self.scores.values()) / n,
            bilingual=sum(s.bilingual for s in self.scores.values()) / n,
        )

    @property
    def grade_distribution(self) -> dict[str, int]:
        dist: dict[str, int] = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
        for s in self.scores.values():
            dist[s.grade] = dist.get(s.grade, 0) + 1
        return dist

    def top_skills(self, n: int = 10) -> list[tuple[str, QualityScore]]:
        return sorted(self.scores.items(), key=lambda x: x[1].overall, reverse=True)[:n]

    def bottom_skills(self, n: int = 10) -> list[tuple[str, QualityScore]]:
        return sorted(self.scores.items(), key=lambda x: x[1].overall)[:n]

    def summary(self) -> str:
        avg = self.average
        dist = self.grade_distribution
        lines = [
            "=" * 60,
            "QUALITY REPORT",
            "=" * 60,
            f"Skills analyzed: {len(self.scores)}",
            f"Average completeness: {avg.completeness:.1f}%",
            f"Average depth:        {avg.depth:.1f}%",
            f"Average code quality: {avg.code_quality:.1f}%",
            f"Average freshness:    {avg.freshness:.1f}%",
            f"Average bilingual:    {avg.bilingual:.1f}%",
            f"Overall score:        {avg.overall:.1f}% ({avg.grade})",
            "",
            "Grade distribution:",
            *[f"  {g}: {n}" for g, n in sorted(dist.items())],
        ]
        return "\n".join(lines)
