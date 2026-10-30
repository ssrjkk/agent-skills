from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from claude_skills.models import Catalog, CatalogMetadata, Skill, parse_frontmatter


class CatalogBuilder:
    BASE = ".claude/skills"

    def __init__(self, root: Path | None = None, base: str | None = None):
        self.root = Path(root or os.getcwd())
        self.base = base or self.BASE
        self.skills_dir = self.root / self.base

    def scan(self) -> list[Skill]:
        skills: list[Skill] = []
        seen: set[str] = set()

        for sk_path in sorted(self.skills_dir.rglob("SKILL.md")):
            meta = self._parse_frontmatter(sk_path)
            if not meta or "name" not in meta:
                continue

            name = meta["name"]
            if name in seen:
                continue
            seen.add(name)

            ru_path = sk_path.parent / "SKILL.ru.md"
            has_ru = ru_path.exists()

            skill = Skill(
                name=name,
                description=meta.get("description", ""),
                category=meta.get("category", ""),
                tags=self._parse_list(meta.get("tags", [])),
                models=self._parse_list(meta.get("models", [])),
                version=str(meta.get("version", "1.0.0")),
                path=sk_path,
                languages=["en", "ru"] if has_ru else ["en"],
                has_ru=has_ru,
                created=str(meta.get("created", "")),
                updated=str(meta.get("updated", "")),
            )
            skills.append(skill)

        return skills

    def build_catalog(self) -> Catalog:
        skills = self.scan()
        domains = sorted({s.category for s in skills})
        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        metadata = CatalogMetadata(
            schema_version="3.0",
            generated_at=now,
            total_skills=len(skills),
            total_ru=sum(1 for s in skills if s.has_ru),
            domains=domains,
            bilingual=True,
        )
        return Catalog(metadata=metadata, skills=skills)

    def to_json(self, catalog: Catalog, path: Path | None = None) -> str:
        data = {
            "metadata": {
                "schema_version": catalog.metadata.schema_version,
                "generated_at": catalog.metadata.generated_at,
                "total_skills": catalog.metadata.total_skills,
                "total_ru": catalog.metadata.total_ru,
                "domains": catalog.metadata.domains,
                "bilingual": catalog.metadata.bilingual,
            },
            "skills": [
                {
                    "name": s.name,
                    "description": s.description,
                    "category": s.category,
                    "tags": s.tags,
                    "models": s.models,
                    "version": s.version,
                    "path": str(s.path.as_posix()),
                    "languages": s.languages,
                    "has_ru": s.has_ru,
                    "created": s.created or "",
                    "updated": s.updated or "",
                }
                for s in catalog.skills
            ],
        }
        text = json.dumps(data, indent=2, ensure_ascii=False)
        if path:
            path.write_text(text, encoding="utf-8")
        return text

    def _parse_frontmatter(self, filepath: Path) -> dict[str, Any] | None:
        try:
            content = filepath.read_text(encoding="utf-8")
            frontmatter, _, ok = parse_frontmatter(content)
            return frontmatter if ok else None
        except (OSError, UnicodeDecodeError):
            return None

    @staticmethod
    def _parse_list(value: Any) -> list[str]:
        if isinstance(value, list):
            return [str(v).strip() for v in value if v]
        if isinstance(value, str):
            cleaned = value.strip().strip("[]").strip()
            if not cleaned:
                return []
            return [v.strip().strip("\"'") for v in re.split(r"[\s,]+", cleaned) if v.strip()]
        return []

    @staticmethod
    def from_json(path: Path) -> Catalog:
        data = json.loads(path.read_text(encoding="utf-8"))
        meta = data.get("metadata", {})
        metadata = CatalogMetadata(
            schema_version=meta.get("schema_version", "3.0"),
            generated_at=meta.get("generated_at", ""),
            total_skills=meta.get("total_skills", 0),
            total_ru=meta.get("total_ru", 0),
            domains=meta.get("domains", []),
            bilingual=meta.get("bilingual", True),
        )

        skills = [
            Skill(
                name=s["name"],
                description=s.get("description", ""),
                category=s.get("category", ""),
                tags=CatalogBuilder._parse_list(s.get("tags", [])),
                models=CatalogBuilder._parse_list(s.get("models", [])),
                version=str(s.get("version", "1.0.0")),
                path=Path(s.get("path", "")),
                languages=s.get("languages", ["en"]),
                has_ru=s.get("has_ru", False),
                created=s.get("created", ""),
                updated=s.get("updated", ""),
            )
            for s in data.get("skills", [])
        ]
        return Catalog(metadata=metadata, skills=skills)
