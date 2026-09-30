# Project Guidelines for AI Agents

This file helps AI coding agents (Claude Code, OpenCode, Cursor, Windsurf,
Gemini CLI, GLM Coding, Codex, etc.) work correctly in this repository.

## Repository structure

- `.claude/skills/{domain}/{skill}/SKILL.md` — skills (English, primary)
- `.claude/skills/{domain}/{skill}/SKILL.ru.md` — parallel Russian translation
- `src/claude_skills/` — Python SDK (validator, quality, catalog, CLI)
- `scripts/` — CI helper scripts
- `docs/` — architecture, release notes, catalog site

## Skill file requirements

Every `SKILL.md` must:

- Have YAML frontmatter with: `name`, `description`, `category`, `tags`,
  `models`, `version`, `created`, `updated`, `author`.
- `name` must be lowercase kebab-case and match its directory name.
- `description` must be a single line <= 1024 chars.
- Include sections `Quick Start`, `When to Use`, `Step-by-Step`, `Examples`,
  and `Validation`.
- Include >= 4 code fences and >= 70 lines for 100% quality score.
- A `SKILL.ru.md` translation with the same number of `## ` sections.

Valid categories are in `src/claude_skills/validator.py` (`VALID_CATEGORIES`).

## Commands

```bash
make lint          # ruff
make typecheck     # mypy
make test          # pytest
make validate      # validate all skills (EN + RU)
make quality       # quality analysis
make catalog       # rebuild skills_catalog.json
make interop       # cross-agent portability check
make docs          # rebuild docs site
```

Or use the CLI:

```bash
python -m claude_skills.cli validate --dir .claude/skills
python -m claude_skills.cli quality --dir .claude/skills
```

## Testing a new skill

1. Add the skill files under `.claude/skills/{domain}/{name}/`.
2. Run `make validate` and `make quality` — expect 0 errors, 100% score.
3. Run `python scripts/check_agent_interop.py`.
4. Run `make test`.
5. Rebuild catalog and docs: `make catalog && make docs`.

## Commit conventions

Use conventional commits: `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`.
Never commit secrets. Keep skills EN + RU in the same change.