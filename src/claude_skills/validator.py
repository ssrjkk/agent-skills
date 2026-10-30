from __future__ import annotations

import re
from pathlib import Path
from typing import Any, ClassVar

from claude_skills.models import Severity, ValidationResult, parse_frontmatter


class SkillValidator:
    REQUIRED_FIELDS: ClassVar[set[str]] = {"name", "description", "category", "tags", "models", "version"}
    VALID_CATEGORIES: ClassVar[set[str]] = {
        "ai", "ar-vr", "backend", "block", "blockchain", "ci-cd-setup", "cloud",
        "communications", "data", "database", "database-migration", "design", "desktop",
        "devops", "ecommerce", "education", "embedded", "energy", "engineering",
        "finance", "frontend", "gamedev", "geospatial", "healthcare", "hr", "iot",
        "media", "mobile", "networking", "os-admin", "payments", "product", "qa",
        "scientific", "security", "supply-chain", "sustainability", "test-reporting",
        "api-testing",
    }
    PLACEHOLDER_NAMES: ClassVar[re.Pattern[str]] = re.compile(r"^(skill-\d+|.*-skill-\d+)$")
    BAD_PATTERNS: ClassVar[re.Pattern[str]] = re.compile(r"\b(TODO|FIXME|HACK|XXX|UNDONE)\b")
    FILLER_WORDS: ClassVar[tuple[str, ...]] = (
        "revolutionize", "supercharge", "cutting edge", "effortless",
        "world class", "take it to the next level", "harness the power",
    )

    def validate_skill_file(self, filepath: Path) -> list[ValidationResult]:
        results: list[ValidationResult] = []
        name = filepath.parent.name
        try:
            content = filepath.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as e:
            results.append(ValidationResult(str(filepath), Severity.ERROR, "E001", f"Cannot read file: {e}"))
            return results

        if not content.startswith("---"):
            results.append(ValidationResult(str(filepath), Severity.ERROR, "E010", "Missing opening frontmatter ---"))
            return results

        frontmatter, body, parse_ok = parse_frontmatter(content)
        if not parse_ok:
            results.append(ValidationResult(str(filepath), Severity.ERROR, "E011", "Malformed frontmatter"))
            return results

        if not frontmatter:
            results.append(ValidationResult(str(filepath), Severity.ERROR, "E012", "Empty frontmatter"))
            return results

        results.extend(self._validate_frontmatter(filepath, frontmatter, name))
        results.extend(self._validate_body(filepath, body))
        results.extend(self._validate_copy(filepath, frontmatter, body))
        if filepath.name == "SKILL.ru.md":
            results.extend(self._validate_ru(filepath, body))

        return results

    def _validate_frontmatter(self, filepath: Path, fm: dict[str, Any], expected_name: str) -> list[ValidationResult]:
        results: list[ValidationResult] = []
        missing = self.REQUIRED_FIELDS - set(fm.keys())
        if missing:
            results.append(ValidationResult(str(filepath), Severity.ERROR, "E020", f"Missing required fields: {sorted(missing)}"))

        name = fm.get("name", "")
        if name != expected_name:
            results.append(ValidationResult(str(filepath), Severity.WARNING, "W010", f'Directory name "{expected_name}" != frontmatter name "{name}"'))

        if self.PLACEHOLDER_NAMES.match(name):
            results.append(ValidationResult(str(filepath), Severity.WARNING, "W011", f"Placeholder-style name: {name}"))

        category = fm.get("category", "")
        if category and category not in self.VALID_CATEGORIES:
            results.append(ValidationResult(str(filepath), Severity.WARNING, "W012", f'Unknown category "{category}"'))

        tags = fm.get("tags", [])
        if isinstance(tags, list):
            dupes = self._find_duplicates(tags)
            if dupes:
                results.append(ValidationResult(str(filepath), Severity.WARNING, "W013", f"Duplicate tags: {dupes}"))

        version = str(fm.get("version", ""))
        if version and not re.match(r"^\d+\.\d+(\.\d+)?$", version):
            results.append(ValidationResult(str(filepath), Severity.WARNING, "W014", f"Non-standard version format: {version}"))

        models = fm.get("models", [])
        if isinstance(models, list) and len(models) == 2 and "gpt-4" in models and "claude-3" in models:
            results.append(ValidationResult(str(filepath), Severity.INFO, "I010", "Default model set [gpt-4, claude-3] - may need updating"))

        return results

    def _validate_body(self, filepath: Path, body: str) -> list[ValidationResult]:
        results: list[ValidationResult] = []
        body_stripped = body.strip()

        if len(body_stripped) < 80:
            results.append(ValidationResult(str(filepath), Severity.WARNING, "W020", f"Body too short ({len(body_stripped)} chars)"))

        if len(body_stripped) < 50:
            results.append(ValidationResult(str(filepath), Severity.WARNING, "W030", f"Body critically short ({len(body_stripped)} chars)"))

        if self.BAD_PATTERNS.search(body):
            results.append(ValidationResult(str(filepath), Severity.WARNING, "W021", "Contains TODO/FIXME placeholder"))

        required_sections = ["Quick Start", "Validation"]
        if filepath.name == "SKILL.ru.md":
            # RU files carry translated headers; checking English names here
            # produced 100+ bogus I020 infos. Both RU headers below are
            # present in every shipped translation (verified 103/103).
            required_sections = ["Быстрый старт", "Валидация"]
        for section in required_sections:
            if section not in body:
                results.append(ValidationResult(str(filepath), Severity.INFO, "I020", f'Missing section "{section}"'))

        fence_count = body.count("```")
        if fence_count > 0 and fence_count % 2 != 0:
            results.append(ValidationResult(str(filepath), Severity.ERROR, "E040", f"Unbalanced code fences ({fence_count} fences)"))

        return results

    def _validate_copy(self, filepath: Path, frontmatter: dict[str, Any], body: str) -> list[ValidationResult]:
        """INFO-level copy signals. Never blocks: flags marketing filler so a
        human can verify each hit is intentional (e.g. a ban-list example)."""
        results: list[ValidationResult] = []
        hits: list[str] = []
        for line in f"{frontmatter.get('description', '')}\n{body}".splitlines():
            low = line.lower()
            if "ban" in low:
                continue  # ban-list examples name the filler to forbid it
            hits.extend(w for w in self.FILLER_WORDS if w in low)
        hits = sorted(set(hits))
        if hits:
            results.append(ValidationResult(str(filepath), Severity.INFO, "I030", f"Mentions filler words, verify intentional: {hits}"))
        return results

    @staticmethod
    def _prose_text(body: str) -> str:
        """Body without fenced code blocks: code is never translated, so only
        prose counts when judging a translation."""
        out = []
        in_fence = False
        for line in body.splitlines():
            if line.strip().startswith("```"):
                in_fence = not in_fence
                continue
            if not in_fence:
                out.append(line)
        return "\n".join(out)

    def _validate_ru(self, filepath: Path, body: str) -> list[ValidationResult]:
        """Catch machine-copy 'translations': near-zero Cyrillic or a stub
        body next to a full English original. Warnings only."""
        results: list[ValidationResult] = []
        prose = self._prose_text(body)
        letters = [c for c in prose if c.isalpha()]
        cyrillic = sum(1 for c in letters if "Ѐ" <= c <= "џ")
        if letters and cyrillic / len(letters) < 0.05:
            results.append(ValidationResult(str(filepath), Severity.WARNING, "W040", f"Almost no Cyrillic ({cyrillic}/{len(letters)} letters) - machine translation?"))
        try:
            en_text = (filepath.parent / "SKILL.md").read_text(encoding="utf-8")
            en_parts = en_text.split("---", 2)
            en_body = en_parts[2].strip() if len(en_parts) >= 3 else ""
        except (OSError, UnicodeDecodeError):
            en_body = ""
        en_prose = self._prose_text(en_body).strip()
        if en_prose and len(prose.strip()) < 0.3 * len(en_prose):
            results.append(ValidationResult(str(filepath), Severity.WARNING, "W041", "Suspiciously short vs English original - incomplete translation?"))
        return results

    def _find_duplicates(self, items: list[Any]) -> list[str]:
        seen: dict[str, bool] = {}
        dupes: list[str] = []
        for item in items:
            key = str(item).strip().lower()
            if key in seen:
                dupes.append(str(item))
            else:
                seen[key] = True
        return list(set(dupes))


class ValidationPipeline:
    def __init__(self, skills_dir: Path):
        self.skills_dir = skills_dir
        self.validator = SkillValidator()

    def _result_key(self, sk_path: Path) -> str:
        """Collision-safe key: two domains may host same-named directories."""
        try:
            return sk_path.parent.relative_to(self.skills_dir).as_posix()
        except ValueError:  # pragma: no cover - rglob always stays under skills_dir
            return sk_path.parent.name

    def run_all(self) -> dict[str, list[ValidationResult]]:
        results: dict[str, list[ValidationResult]] = {}
        for sk_path in sorted(self.skills_dir.rglob("SKILL.md")):
            results[self._result_key(sk_path)] = self.validator.validate_skill_file(sk_path)
        return results

    def run_ru_all(self) -> dict[str, list[ValidationResult]]:
        results: dict[str, list[ValidationResult]] = {}
        for sk_path in sorted(self.skills_dir.rglob("SKILL.ru.md")):
            results[self._result_key(sk_path)] = self.validator.validate_skill_file(sk_path)
        return results

    def report(self, results: dict[str, list[ValidationResult]]) -> dict[str, Any]:
        stats = {"total": len(results), "errors": 0, "warnings": 0, "info": 0}
        all_errors: list[str] = []
        all_warnings: list[str] = []
        for skill_results in results.values():
            for r in skill_results:
                if r.severity == Severity.ERROR:
                    stats["errors"] += 1
                    all_errors.append(str(r))
                elif r.severity == Severity.WARNING:
                    stats["warnings"] += 1
                    all_warnings.append(str(r))
                elif r.severity == Severity.INFO:
                    stats["info"] += 1
        return {**stats, "error_details": all_errors[:50], "warning_details": all_warnings[:50]}
