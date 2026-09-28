<p align="center">
  <img src="https://img.shields.io/badge/skills-59-blue?style=for-the-badge" alt="Skills">
  <img src="https://img.shields.io/badge/languages-EN%20%7C%20RU-green?style=for-the-badge" alt="Languages">
  <img src="https://img.shields.io/badge/domains-13-orange?style=for-the-badge" alt="Domains">
  <img src="https://img.shields.io/badge/quality-A%20(100%25)-brightgreen?style=for-the-badge" alt="Quality">
  <img src="https://img.shields.io/badge/coverage-100%25-brightgreen?style=for-the-badge" alt="Coverage">
  <img src="https://img.shields.io/badge/agents-universal-purple?style=for-the-badge" alt="Agent-agnostic">
  <img src="https://img.shields.io/badge/license-MIT-blue?style=for-the-badge" alt="MIT">
  <img src="https://img.shields.io/github/stars/ssrjkk/claude-skills?style=for-the-badge&color=gold" alt="Stars">
  <img src="https://img.shields.io/github/actions/workflow/status/ssrjkk/claude-skills/validate.yml?branch=main&style=for-the-badge&label=CI&color=green" alt="CI">
</p>

<h1 align="center">Skills Library</h1>
<p align="center"><strong>Curated bilingual (EN + RU) skills in the universal Agent Skills format</strong></p>
<p align="center">Works with Claude Code, OpenCode, Cursor, Windsurf and every Agent Skills-compatible tool</p>
<p align="center">
  <a href="https://ssrjkk.github.io/claude-skills/">Live Catalog Site</a> ·
  <a href="https://github.com/ssrjkk/claude-skills/releases">Releases</a> ·
  <a href="https://github.com/ssrjkk/claude-skills/issues">Issues</a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/ssrjkk/claude-skills/main/.github/social-preview.svg" alt="Skills Library banner" width="640">
</p>

---

## Install in one line

```bash
curl -fsSL https://raw.githubusercontent.com/ssrjkk/claude-skills/main/install.sh | bash
```

Or clone directly into your agent's skills directory:

| Agent      | Command |
|------------|---------|
| Claude Code | `git clone --depth 1 https://github.com/ssrjkk/claude-skills.git ~/.claude/skills` |
| OpenCode   | `git clone --depth 1 https://github.com/ssrjkk/claude-skills.git ~/.opencode/skills` |
| Cursor     | `git clone --depth 1 https://github.com/ssrjkk/claude-skills.git ~/.cursor/skills` |
| Windsurf   | `git clone --depth 1 https://github.com/ssrjkk/claude-skills.git ~/.windsurf/skills` |

## What is this?

59 production-grade, bilingual (English + Russian) skills following the
**universal Agent Skills format** — the `SKILL.md` convention shared by Claude
Code, OpenCode, Cursor, Windsurf and other agents. Each skill is a folder with
a `SKILL.md` (primary, English) and an optional `SKILL.ru.md` (parallel
Russian translation). Any agent that implements the Agent Skills spec can
consume them directly.

The library ships with a Python SDK + CLI for validation, quality scoring,
cataloging and search, all enforced in CI.

## Quick Start

```bash
# Install (editable)
pip install -e .

# Explore the library
claude-skills stats          # Library statistics
claude-skills search <query> # Search skills
claude-skills validate       # Validate all skills (EN + RU)
claude-skills quality        # Quality analysis
claude-skills catalog        # Rebuild skills_catalog.json
```

## Using the skills with your agent

Every skill is a standard Agent Skills directory:

```
.claude/skills/
  {domain}/
    {skill-name}/
      SKILL.md        <- English (primary)
      SKILL.ru.md     <- Russian (parallel)
```

To install a skill into another agent, point it at the same folder — the file
format is identical, only the root directory changes:

| Agent      | Default skills root     | Notes |
|------------|-------------------------|-------|
| Claude Code | `.claude/skills/`       | Native |
| OpenCode   | `.opencode/skills/`     | Same `SKILL.md` format |
| Cursor     | `.cursor/skills/`       | Same `SKILL.md` format |
| Windsurf   | `.windsurf/skills/`     | Same `SKILL.md` format |

Frontmatter is strictly validated for cross-agent portability in CI
(`scripts/check_agent_interop.py`): portable `name`, single-line
`description`, no duplicate names.

## Stats

| Metric | Value |
|--------|-------|
| Total skills | **59** |
| Russian translations | **59 (100%)** |
| Domains | **13** |
| Quality score | **100% (Grade A)** |
| Test coverage | **100%** |
| License | MIT |

Only skills meeting the quality bar (Grade A, no validation errors) are kept
in `main`. Everything else is archived under the `v1.0-legacy` tag.

## Skills by domain

| Domain | Skill | Description |
|--------|-------|-------------|
| `ai` | `few-shot-learning` | Few-shot prompt design with example selection |
| `ai` | `llm-finetuning` | Fine-tuning LLMs end-to-end |
| `ai` | `prompt-engineering` | Reliable prompt design for LLMs |
| `ai` | `rag-pipeline` | Retrieval-augmented generation |
| `ai` | `agent-development` | Reliable LLM agents with tools |
| `ai` | `mcp-servers` | Model Context Protocol servers |
| `ai` | `llm-evals` | Evaluation suites for LLMs |
| `ai` | `function-calling` | Robust LLM tool calling |
| `ai` | `prompt-caching` | LLM cost & latency optimization |
| `ai` | `mlops` | ML in production lifecycle |
| `backend` | `deno-runtime` | Deno realtime apps & Workers |
| `backend` | `nestjs` | NestJS modular backends |
| `backend` | `rust-tokio` | Async Rust with Tokio |
| `backend` | `fastapi` | High-performance Python APIs |
| `backend` | `go-rest-api` | REST APIs in Go |
| `backend` | `rest-api-design` | Consistent REST API design |
| `backend` | `django` | Secure Django web apps |
| `backend` | `grpc` | High-performance gRPC services |
| `backend` | `express` | Node.js APIs with Express |
| `blockchain` | `zk-proofs` | Zero-knowledge proofs |
| `data` | `pandas` | Tabular data analysis & ETL |
| `data` | `sql-querying` | Correct & efficient SQL |
| `data` | `elasticsearch` | Search & log analytics |
| `database` | `postgresql` | PostgreSQL schema & queries |
| `database` | `prisma-orm` | Prisma ORM data layer |
| `database` | `redis` | Caching, queues, rate limiting |
| `database` | `vector-databases` | Semantic search & RAG retrieval |
| `database` | `mongodb` | Flexible NoSQL documents |
| `desktop` | `electron` | Electron cross-platform apps |
| `devops` | `aws-lambda` | Serverless on AWS Lambda |
| `devops` | `cloud-native-ai` | Cloud-native AI platforms |
| `devops` | `docker` | Containers & deployment |
| `devops` | `github-actions` | CI/CD pipelines on GitHub |
| `devops` | `gitlab-ci` | GitLab CI/CD pipelines |
| `devops` | `kubernetes` | Container orchestration |
| `devops` | `observability-llm` | LLM observability |
| `devops` | `platform-engineering` | Internal developer platforms |
| `devops` | `serverless-ai` | Serverless AI workloads |
| `devops` | `sre-slos` | SLOs & reliability |
| `devops` | `terraform` | Infrastructure as code |
| `devops` | `kafka` | Event streaming platform |
| `devops` | `prometheus-grafana` | Metrics & dashboards |
| `embedded` | `rust-embedded` | Embedded Rust |
| `engineering` | `ai-testing` | AI/LLM testing |
| `engineering` | `code-review` | Effective code reviews |
| `engineering` | `git-workflow` | Git branching & history hygiene |
| `engineering` | `claude-code-commands` | Claude Code commands & hooks |
| `frontend` | `bun-runtime` | Bun runtime & tooling |
| `frontend` | `nextjs` | Next.js full-stack React |
| `frontend` | `react-19` | Modern React UIs |
| `frontend` | `tailwind-v4` | Tailwind CSS v4 |
| `frontend` | `typescript` | Type-safe JavaScript |
| `frontend` | `vue` | Vue 3 reactive UIs |
| `mobile` | `expo-rn` | Expo & React Native |
| `mobile` | `flutter` | Cross-platform Flutter apps |
| `qa` | `browser-automation` | Playwright E2E & scraping |
| `qa` | `pytest` | Reliable Python testing |
| `security` | `oauth2-jwt` | OAuth 2.0 & JWT |
| `security` | `owasp-web-security` | OWASP Top 10 hardening |

## SDK

### Python

```python
from claude_skills.catalog import CatalogBuilder
from claude_skills.validator import ValidationPipeline
from claude_skills.quality import QualityAnalyzer

catalog = CatalogBuilder().build_catalog()
print(f"{catalog.metadata.total_skills} skills, {catalog.metadata.total_ru} RU")

pipeline = ValidationPipeline(Path(".claude/skills"))
report = pipeline.report(pipeline.run_all())
print(f"Errors: {report['errors']}, Warnings: {report['warnings']}")
```

### CLI

Commands: `stats`, `search`, `validate`, `quality`, `catalog`.

```bash
claude-skills search <query>      # Search by name, description, tags
claude-skills validate --json out.json
claude-skills quality --json out.json
claude-skills catalog             # Rebuild catalog JSON
claude-skills stats               # Library statistics
```

## Quality Pipeline

Every skill is scored on 5 dimensions:

| Dimension | Weight | What it measures |
|-----------|--------|-----------------|
| Completeness | 25% | Section coverage (Quick Start, Validation, etc.) |
| Depth | 25% | Content length & substance |
| Code Quality | 20% | Working code examples |
| Freshness | 15% | Recency of last update |
| Bilingual | 15% | Russian translation quality |

## Domains (13)

`ai` · `backend` · `blockchain` · `data` · `database` · `desktop` · `devops` ·
`embedded` · `engineering` · `frontend` · `mobile` · `qa` · `security`

## Author

**ssrjkk**

- Telegram: [@ssrjkk](https://t.me/ssrjkk)
- Email: [ray013lefe@gmail.com](mailto:ray013lefe@gmail.com)
- Twitter/X: [ssrjkk](https://twitter.com/ssrjkk)

## For Contributors

See [CONTRIBUTING.md](CONTRIBUTING.md). Quick checklist:
- [ ] `SKILL.md` has frontmatter with name, description, category, tags, models, version
- [ ] `SKILL.ru.md` is a **real translation** (not auto-generated)
- [ ] Code examples compile and run
- [ ] `SKILL.md` passes `scripts/check_agent_interop.py` (portable to all agents)
- [ ] `make test` passes
- [ ] `make lint` passes

## Links

- [Architecture Guide](docs/ARCHITECTURE.md)
- [Release Notes](docs/RELEASE_NOTES_v3.4.md)
- [Roadmap](ROADMAP.md)
- [Issue Tracker](https://github.com/ssrjkk/claude-skills/issues)

## Why this library

- **Curated, not generated** — 59 hand-reviewed skills that pass a 5-dimension
  quality pipeline (completeness, depth, code quality, freshness, bilingual).
- **Universal Agent Skills format** — the same `SKILL.md` convention native to
  Claude Code and supported by OpenCode, Cursor, Windsurf, and others. No
  lock-in: install once, use anywhere.
- **Bilingual (EN + RU)** — every skill ships a real Russian translation, not
  a machine one.
- **Quality enforced in CI** — validation, quality scoring, anti-pattern
  detection, cross-agent interop checks, 100% test coverage. What you see in
  `main` is what passes the bar.
- **SDK + CLI + GitHub Action** — validate, score, catalog and search any
  skills library programmatically.

## Legacy Version

The original v1.0 library (10,000+ auto-generated skills) is archived under
the `v1.0-legacy` tag — v3.1 is a complete rewrite focused on quality:

```bash
git checkout v1.0-legacy
```

## License

MIT.