# Roadmap

## Current state (2026-11-09)

- **120 curated skills** across **20 domains**, 100% bilingual (EN + RU), avg quality **97.5** (min 97, measured 2026-11-09).
- Universal Agent Skills format, portable to Claude Code, OpenCode, Cursor,
  Windsurf, and every Agent Skills-compatible agent.
- Python SDK + CLI (with remote registry search `search --remote`), GitHub
  Action, PyPI + npm packages, JSON Schema validation, quality gates.
- Tabbed portal site: skills catalog, **20/20 live roadmap tracks**, **27
  full-text maps library**, bilingual UI (EN/RU), search, honest live-status
  badges, sitemap + JSON-LD.
- Test suite: **326 tests** (unit / property-based / e2e site builds), **93%
  coverage** across `src/` + `scripts/` with a hard `--cov-fail-under=90` gate.

## Shipped

### v4.0 — Ecosystem
- [x] Publish `agent-skills-library` to PyPI (auto-publish on tags)
- [x] `skills_catalog.json` downloads + JSON Schema for the catalog
- [x] npm package for Node-based agents
- [x] Announcement on GitHub Discussions + PRs to awesome-lists

### v4.1 — More coverage
- [x] Skills for more domains: gamedev, finance, healthcare and 15 more
- [x] 100 → 120 skills milestone across 17 → 20 domains

### v4.2 — Quality & UX
- [x] CI that validates new skills in PRs + blocks below 90% quality
- [x] `agent-skills install <skill>` targeted single-skill install
- [x] Docs site: search, filters, install snippets, tabs, live roadmap
      explorer and the full-text maps library
- [x] Roadmaps portal: 20 live bilingual tracks + 27 full-text maps
- [x] In-process test coverage of every CI gate script (67% → 93%)

## Planned

### v4.3 — Portal & ecosystem
- [ ] Command palette (⌘K) with cross-entity search: skills, maps, tracks
- [ ] Full-text search across the 27 maps (server-side index)
- [ ] Tailored resume maps per hh.ru track (AI/ML, Senior Fullstack,
      Backend/SDET)
- [ ] RSS/Atom feed for new skills and maps
- [ ] Homebrew tap for macOS installs

## Backlog
- [ ] Community-requested skills via GitHub Discussions
- [ ] Per-skill verified recipes (tested commands + expected output)
- [ ] Benchmark suite for validation speed
- [ ] RU-first i18n for domain and skill pages (server-rendered mirrors)
