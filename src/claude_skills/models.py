from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

import yaml  # type: ignore[import-untyped]


class Severity(Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass(frozen=True)
class ValidationResult:
    skill_path: str
    severity: Severity
    code: str
    message: str
    line: int | None = None

    def __str__(self) -> str:
        prefix = {
            Severity.ERROR: "  ERROR",
            Severity.WARNING: "WARNING",
            Severity.INFO: "   INFO",
        }[self.severity]
        loc = f":{self.line}" if self.line else ""
        return f"[{prefix}] {self.skill_path}{loc} [{self.code}] {self.message}"


@dataclass
class QualityScore:
    completeness: float = 0.0
    depth: float = 0.0
    code_quality: float = 0.0
    freshness: float = 0.0
    bilingual: float = 0.0

    @property
    def overall(self) -> float:
        weights = {"completeness": 0.25, "depth": 0.25, "code_quality": 0.2, "freshness": 0.15, "bilingual": 0.15}
        return sum(getattr(self, k) * v for k, v in weights.items())

    @property
    def grade(self) -> str:
        score = self.overall
        if score >= 90:
            return "A"
        if score >= 80:
            return "B"
        if score >= 65:
            return "C"
        if score >= 50:
            return "D"
        return "F"


@dataclass
class SkillFile:
    en_path: Path
    ru_path: Path | None = None
    en_content: str = ""
    ru_content: str = ""
    en_frontmatter: dict = field(default_factory=dict)
    ru_frontmatter: dict = field(default_factory=dict)
    en_body: str = ""
    ru_body: str = ""


@dataclass
class Skill:
    name: str
    description: str
    category: str
    tags: list[str]
    models: list[str]
    version: str
    path: Path
    languages: list[str] = field(default_factory=lambda: ["en"])
    has_ru: bool = False
    created: str | None = None
    updated: str | None = None
    quality: QualityScore | None = None
    validation_results: list[ValidationResult] = field(default_factory=list)

    NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]*[a-z0-9]$|^[a-z0-9]$")
    SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")

    @property
    def is_valid_name(self) -> bool:
        return bool(self.NAME_RE.match(self.name))

    @property
    def is_valid_semver(self) -> bool:
        return bool(self.SEMVER_RE.match(self.version))

    @property
    def dir_path(self) -> Path:
        return self.path.parent

    @property
    def category_path(self) -> str:
        return str(self.path.parent.parent.name) if self.path else ""


@dataclass
class CatalogMetadata:
    schema_version: str = "3.0"
    generated_at: str = ""
    total_skills: int = 0
    total_ru: int = 0
    domains: list[str] = field(default_factory=list)
    bilingual: bool = True


@dataclass
class Catalog:
    metadata: CatalogMetadata = field(default_factory=CatalogMetadata)
    skills: list[Skill] = field(default_factory=list)

    @property
    def by_category(self) -> dict[str, list[Skill]]:
        result: dict[str, list[Skill]] = {}
        for s in self.skills:
            result.setdefault(s.category, []).append(s)
        return result

    @property
    def by_tag(self) -> dict[str, list[Skill]]:
        result: dict[str, list[Skill]] = {}
        for s in self.skills:
            for tag in s.tags:
                result.setdefault(tag, []).append(s)
        return result

    def get(self, name: str) -> Skill | None:
        for s in self.skills:
            if s.name == name:
                return s
        return None


@dataclass
class SkillSet:
    skills: list[SkillFile] = field(default_factory=list)

    @property
    def en_count(self) -> int:
        return len(self.skills)

    @property
    def ru_count(self) -> int:
        return sum(1 for s in self.skills if s.ru_path)


def parse_frontmatter(content: str) -> tuple[dict | None, str, bool]:
    """Split a SKILL.md file into (frontmatter dict, body, ok).

    Handles both ``---`` delimiters (opening/closing) regardless of whether
    the file uses LF or CRLF line endings. Missing/empty frontmatter is not
    an error at this level - callers decide how to react.
    """
    try:
        if not content.startswith("---"):
            return None, content.strip(), False
        end = content.find("---", 3)
        if end < 0:
            return None, content.strip(), False
        front = content[3:end].strip()
        body = content[end + 3 :].lstrip("\r\n")
        parsed = yaml.safe_load(front)
        if not isinstance(parsed, dict):
            return None, body, False
        return parsed, body, True
    except yaml.YAMLError:
        return None, "", False
