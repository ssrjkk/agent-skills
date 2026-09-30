# Roadmap

## Current state

- **100 curated skills** across 16 domains, 100% bilingual (EN + RU), Grade A.
- Universal Agent Skills format, portable to Claude Code, OpenCode, Cursor,
  Windsurf, and every Agent Skills-compatible agent.
- Python SDK + CLI, GitHub Action, live catalog site, PyPI-ready packaging.
- JSON Schema validation, npm package, domain filters, quality gates.

## Planned

### v4.0 — Ecosystem
- [x] Publish `agent-skills-library` to PyPI (auto-publish on tags)
- [x] Add `skills_catalog.json` downloads and JSON Schema for the catalog
- [x] npm package for Node-based agents
- [ ] Homebrew tap for macOS installs

### v4.1 — More coverage
- [x] Add skills for more domains: gamedev, finance, healthcare, ecommerce
- [ ] Community-requested skills via GitHub Discussions
- [ ] Per-skill verified recipes (tested commands + expected output)

### v4.2 — Quality & UX
- [x] CI that validates new skills in PRs (already) + blocks below-Grade-A
- [x] `claude-skills install <skill>` targeted single-skill install
- [x] Better docs site with search, filters, and install snippets
- [ ] Benchmark suite for validation speed

### v4.3 — Community
- [ ] Contribution guides for translators
- [ ] Skill badges / certification for contributors
- [ ] Monthly release cadence with changelog

## How to help

- Open a Discussion to propose a new skill.
- Submit a PR following `AGENTS.md`.
- Translate or improve existing `SKILL.ru.md` files.
- Star the repo to help others discover it.

**Want to shape this roadmap?** Open an issue or discussion on GitHub.