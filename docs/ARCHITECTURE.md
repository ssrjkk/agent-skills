# Skills Library - Architecture Guide

A bilingual (EN + RU) library of production-grade skills in the **universal
Agent Skills format**, consumed by Claude Code, OpenCode, Cursor, Windsurf and
every Agent Skills-compatible agent.

## Project Structure

```
claude-skills/
├── .claude/skills/          # 59 curated skills (universal SKILL.md format)
│   └── {domain}/
│       └── {skill-name}/
│           ├── SKILL.md     # English (primary)
│           └── SKILL.ru.md  # Russian (parallel)
├── src/
│   └── claude_skills/       # Python SDK
│       ├── __init__.py      # Public API exports
│       ├── models.py        # Data models + shared parse_frontmatter
│       ├── catalog.py       # Catalog builder & loader
│       ├── validator.py     # Validation pipeline
│       ├── quality.py       # Quality scoring
│       └── cli.py           # CLI entry points
├── tests/                   # Test suite (133 tests, 100% coverage)
├── scripts/                 # Tooling & CI helpers
│   ├── check_agent_interop.py    # Cross-agent portability check
│   ├── detect_anti_patterns.py   # Catalog anti-pattern detection
│   ├── build_docs.py             # Doc site builder
│   └── list-skills.py
├── docs/                    # Documentation site (built from catalog)
├── skills_catalog.json      # Generated catalog
├── setup.cfg                # Package configuration
└── .github/workflows/       # CI/CD
```

## Data Flow

```
SKILL.md files on disk
        │
        ▼
  CatalogBuilder.scan()
        │
        ├──╴CatalogBuilder.to_json() → skills_catalog.json
        │
        ├──╴ValidationPipeline.run_all() → ValidationResult[]
        │
        └──╴QualityAnalyzer.analyze() → QualityScore[]
                │
                ▼
          QualityReport → Summary + Grades
```

## Cross-Agent Portability

Each `SKILL.md` follows the universal Agent Skills format. The frontmatter
requires two portable fields:

- `name` — lowercase-kebab, must match the skill directory name
- `description` — single-line summary, ≤1024 characters

Library-specific metadata (`category`, `tags`, `models`, `version`, `created`,
`updated`) is safely ignored by other agents that implement the spec.
`scripts/check_agent_interop.py` enforces these invariants in CI.

Installing a skill into another agent means pointing the agent at the same
folder — only the root directory changes (`.opencode/skills/`, `.cursor/skills/`,
`.windsurf/skills/`).

## Quality Scoring

The quality score is a weighted composite of 5 dimensions:

| Dimension | Weight | Description |
|-----------|--------|-------------|
| Completeness | 25% | Section coverage (Quick Start, When to Use, etc.) |
| Depth | 25% | Content length and substance |
| Code Quality | 20% | Code examples, fences, inline code |
| Freshness | 15% | Recency of last update |
| Bilingual | 15% | Russian translation quality |

All 59 skills currently score 100.0% (Grade A).