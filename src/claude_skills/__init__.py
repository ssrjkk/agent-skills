"""Claude Skills SDK — validate, analyze, and manage curated bilingual skills."""

import contextlib
import sys

from claude_skills.catalog import CatalogBuilder
from claude_skills.models import (
    Catalog,
    CatalogMetadata,
    QualityScore,
    Severity,
    Skill,
    SkillFile,
    SkillSet,
    ValidationResult,
)
from claude_skills.quality import QualityAnalyzer, QualityReport
from claude_skills.validator import SkillValidator, ValidationPipeline

__version__ = "4.1.1"


def ensure_utf8_console() -> None:
    """Force UTF-8 on stdout/stderr so non-ASCII skill names, descriptions
    and paths never crash on Windows (cp1251) or C-locale containers.

    Best-effort: silently skips streams that cannot be reconfigured
    (pipes, StringIO in tests, exotic runners).
    """
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if not callable(reconfigure):
            continue
        with contextlib.suppress(OSError, ValueError):
            reconfigure(encoding="utf-8")


__all__ = [
    "Catalog",
    "CatalogBuilder",
    "CatalogMetadata",
    "QualityAnalyzer",
    "QualityReport",
    "QualityScore",
    "Severity",
    "Skill",
    "SkillFile",
    "SkillSet",
    "SkillValidator",
    "ValidationPipeline",
    "ValidationResult",
    "ensure_utf8_console",
]
