<p align="center">
  <img src="assets/logo.svg" width="88" alt="Agent Skills logo">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/skills-103-blue?style=for-the-badge" alt="Skills">
  <img src="https://img.shields.io/badge/languages-EN%20%7C%20RU-green?style=for-the-badge" alt="Languages">
  <img src="https://img.shields.io/badge/domains-17-orange?style=for-the-badge" alt="Domains">
  <img src="https://img.shields.io/badge/quality-97.1%25-brightgreen?style=for-the-badge" alt="Quality">
  <img src="https://img.shields.io/badge/coverage-100%25-brightgreen?style=for-the-badge" alt="Coverage">
  <img src="https://img.shields.io/badge/agents-universal-purple?style=for-the-badge" alt="Agent-agnostic">
  <img src="https://img.shields.io/badge/license-MIT-blue?style=for-the-badge" alt="MIT">
  <img src="https://img.shields.io/github/stars/ssrjkk/agent-skills?style=for-the-badge&color=gold" alt="Stars">
  <img src="https://img.shields.io/github/actions/workflow/status/ssrjkk/agent-skills/validate.yml?branch=main&style=for-the-badge&label=CI&color=green" alt="CI">
  <img src="https://img.shields.io/github/release/ssrjkk/agent-skills?style=for-the-badge&color=blue" alt="Release">
  <img src="https://img.shields.io/github/last-commit/ssrjkk/agent-skills?style=for-the-badge&color=lightgrey" alt="Last commit">
  <img src="https://img.shields.io/pypi/v/agent-skills-library?style=for-the-badge&color=3775A9&logo=pypi&logoColor=white" alt="PyPI">
  <img src="https://img.shields.io/pypi/pyversions/agent-skills-library?style=for-the-badge&color=3775A9" alt="Python versions">
</p>

<h1 align="center">Skills Library</h1>
<p align="center"><strong>Curated bilingual (EN + RU) skills in the universal Agent Skills format</strong></p>
<p align="center">Works with Claude Code, OpenCode, Cursor, Windsurf and every Agent Skills-compatible tool</p>
<p align="center">
  <a href="https://ssrjkk.github.io/agent-skills/">Live Catalog Site</a> ·
  <a href="https://github.com/ssrjkk/agent-skills/releases">Releases</a> ·
  <a href="https://github.com/ssrjkk/agent-skills/issues">Issues</a> ·
  <a href="https://github.com/ssrjkk/agent-skills/discussions">Discussions</a> ·
  <a href="https://t.me/ssrjkk_bot">Telegram</a>
</p>

<p align="center">
  <a href="https://ssrjkk.github.io/agent-skills/">
    <img src="https://raw.githubusercontent.com/ssrjkk/agent-skills/main/.github/site-preview.png" alt="Agent Skills Library — live catalog site" width="800">
  </a>
</p>
<p align="center"><em>Live catalog: <a href="https://ssrjkk.github.io/agent-skills/">ssrjkk.github.io/agent-skills</a></em></p>

---

## Install in one line

```bash
curl -fsSL https://raw.githubusercontent.com/ssrjkk/agent-skills/main/scripts/install.sh | bash
```

Or clone directly into your agent's skills directory:

| Agent      | Command |
|------------|---------|
| Claude Code | `git clone --depth 1 https://github.com/ssrjkk/agent-skills.git ~/.claude/skills` |
| OpenCode   | `git clone --depth 1 https://github.com/ssrjkk/agent-skills.git ~/.opencode/skills` |
| Cursor     | `git clone --depth 1 https://github.com/ssrjkk/agent-skills.git ~/.cursor/skills` |
| Windsurf   | `git clone --depth 1 https://github.com/ssrjkk/agent-skills.git ~/.windsurf/skills` |

## What is this?

103 production-grade, bilingual (English + Russian) skills following the
**universal Agent Skills format** — the `SKILL.md` convention shared by Claude
Code, OpenCode, Cursor, Windsurf and other agents. Each skill is a folder with
a `SKILL.md` (primary, English) and an optional `SKILL.ru.md` (parallel
Russian translation). Any agent that implements the Agent Skills spec can
consume them directly.

The library ships with a Python SDK + CLI for validation, quality scoring,
cataloging and search, all enforced in CI.

## Quick Start

```bash
# Install the SDK + CLI from PyPI
pip install agent-skills-library

# Explore the library (both `agent-skills` and `claude-skills` work)
agent-skills stats          # Library statistics
agent-skills search <query> # Search skills
agent-skills validate       # Validate all skills (EN + RU)
agent-skills quality        # Quality analysis
agent-skills catalog        # Rebuild skills_catalog.json
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
| Total skills | **103** |
| Russian translations | **103 (100%)** |
| Domains | **17** |
| Quality score | **97.1% avg (min 97.0, measured 2026-10-30)** |
| Test coverage | **100%** |
| License | MIT |

Only skills that pass validation with zero errors and zero warnings are
kept in `main`. Everything else is archived under the `v1.0-legacy` tag.

## Skills by domain

| Domain | Skill | Description |
|--------|-------|-------------|
| `ai` | `agent-development` | Build reliable LLM agents and agentic workflows: tool use, memory, loops, guardrails, and evaluation. Use for autonomous AI systems. |
| `ai` | `context-engineering` | Curate LLM context windows for quality and cost: system prompts, compaction, just-in-time retrieval, progressive disclosure, and token budgets. Use for effective agent context. |
| `ai` | `embeddings` | Work with text embeddings: model selection, vectorization, similarity, clustering, and caching for search and retrieval. Use for semantic representation of text. |
| `ai` | `few-shot-learning` | Designs and curates few-shot examples to guide LLM behavior, including example selection, formatting, and ordering. Use for task specification without fine-tuning. |
| `ai` | `function-calling` | Implement robust LLM function/tool calling: schemas, multi-call handling, validation, error recovery, and structured execution. Use for agent tool use. |
| `ai` | `llm-evals` | Build evaluation suites for LLM applications: golden datasets, metrics, LLM-as-judge, regression gates, and CI integration. Use for trustworthy model behavior. |
| `ai` | `llm-finetuning` | Fine-tunes open-source LLMs (Llama, Mistral, Qwen) using LoRA/QLoRA with HuggingFace and Unsloth. Use for domain-specific model adaptation. |
| `ai` | `llm-guardrails` | Add safety guardrails to LLM apps: prompt injection defense, content filtering, PII protection, policy enforcement, and red-teaming. Use for safe production AI. |
| `ai` | `mcp-servers` | Build Model Context Protocol servers and clients: tools, resources, prompts, transport, and secure agent integration. Use for connecting agents to external systems. |
| `ai` | `mlops` | Operate machine learning in production: experiment tracking, pipelines, model registry, serving, monitoring, and CI/CD for ML. Use for ML lifecycle. |
| `ai` | `multi-agent-orchestration` | Design and run multi-agent systems: orchestrator-worker, routing, handoffs, shared state, and coordination patterns. Use for complex agent teams. |
| `ai` | `prompt-caching` | Optimize LLM cost and latency with prompt caching: cacheable prefixes, cache-control headers, context layout, and cache-aware prompting. Use for high-volume apps. |
| `ai` | `prompt-engineering` | Design effective prompts for LLMs: role framing, structured output, chain-of-thought, few-shot, and evaluation. Use to get reliable model behavior. |
| `ai` | `rag-pipeline` | Build retrieval-augmented generation pipelines: chunking, embeddings, vector search, hybrid retrieval, and citation. Use for grounded LLM answers over your data. |
| `ai` | `structured-output` | Force LLMs to emit valid, schema-constrained structured output: JSON modes, function calling, JSON Schema validation, and error recovery. Use for reliable data extraction. |
| `backend` | `deno-runtime` | Build secure TypeScript apps with Deno: least-privilege permissions, web-standard APIs, zero-config tooling, and standalone binaries via deno compile. Use for server-side JS without Node. |
| `backend` | `django` | Build secure web applications with Django: models, views, ORM, admin, auth, REST APIs, and deployment. Use for Python web backends. |
| `backend` | `dotnet` | Build .NET backends with ASP.NET Core: minimal APIs, EF Core, dependency injection, middleware, and testing. Use for C# services. |
| `backend` | `express` | Build Node.js web APIs with Express: routing, middleware, error handling, validation, and production hardening. Use for Node backends. |
| `backend` | `fastapi` | Build high-performance Python APIs with FastAPI: routing, Pydantic validation, async, dependency injection, OpenAPI, and testing. Use for any Python backend. |
| `backend` | `go-rest-api` | Build production REST APIs in Go with the standard library or Gin, including routing, middleware, JSON handling, and testing. Use for performant backends. |
| `backend` | `graphql` | Design and implement GraphQL APIs: schemas, resolvers, queries, mutations, subscriptions, and N+1 avoidance. Use for flexible client-driven APIs. |
| `backend` | `grpc` | Build high-performance services with gRPC: protobuf schemas, unary/streaming RPCs, interceptors, and error handling. Use for inter-service communication. |
| `backend` | `laravel` | Build PHP web applications with Laravel: routing, Eloquent ORM, Blade, migrations, validation, and deployment. Use for PHP backends. |
| `backend` | `nestjs` | Creates Node.js server-side applications with NestJS, modules, dependency injection, and decorators. Use for enterprise-grade Node.js APIs. |
| `backend` | `rest-api-design` | Design consistent REST APIs: resource modeling, status codes, pagination, versioning, error contracts, and documentation. Use for any API design task. |
| `backend` | `rust-tokio` | Build async Rust services with Tokio: high-throughput networking, tasks, channels, timers, and testing. Use for chat, proxies, streaming, and data pipelines. |
| `backend` | `spring-boot` | Build production Java/Kotlin backends with Spring Boot: REST controllers, dependency injection, data access, security, and testing. Use for JVM services. |
| `backend` | `websockets` | Build real-time features with WebSockets: connection lifecycle, protocols, backpressure, scaling, and reconnection. Use for live updates and chat. |
| `blockchain` | `zk-proofs` | Develop zero-knowledge proofs: private voting and identity, zk-rollups, verifiable computation, and compliance without exposing data. Use for privacy-preserving apps. |
| `data` | `airflow` | Orchestrate data pipelines with Apache Airflow: DAGs, tasks, dependencies, sensors, and retries. Use for scheduled workflows. |
| `data` | `apache-spark` | Process large-scale data with Apache Spark: DataFrames, SQL, joins, partitioning, and optimization. Use for big data and ETL. |
| `data` | `data-visualization` | Create clear data visualizations with Matplotlib, Plotly, and Altair: chart selection, design, interactivity, and dashboards. Use for communicating data. |
| `data` | `dbt` | Build analytics engineering workflows with dbt: models, tests, sources, macros, and documentation. Use for transform-layer data pipelines. |
| `data` | `elasticsearch` | Design and operate Elasticsearch: mappings, indexing, queries, aggregations, and cluster tuning. Use for search and log analytics. |
| `data` | `pandas` | Analyze and transform tabular data with pandas: dataframes, cleaning, aggregation, joins, and time series. Use for any data analysis or ETL task. |
| `data` | `sql-querying` | Write correct and efficient SQL: joins, aggregations, window functions, CTEs, and query optimization. Use for any relational data access. |
| `database` | `clickhouse` | Design and operate ClickHouse for OLAP analytics: columnar tables, engines, aggregations, partitioning, and performance. Use for analytics workloads. |
| `database` | `mongodb` | Design and operate MongoDB: document modeling, queries, indexes, aggregation, replication, and sharding. Use for flexible NoSQL data. |
| `database` | `mysql` | Design and operate MySQL: schema, InnoDB tuning, indexing, transactions, replication, and query optimization. Use for relational workloads. |
| `database` | `postgresql` | Design and operate PostgreSQL databases: schema design, indexing, query optimization, transactions, and migrations. Use for any relational data layer. |
| `database` | `prisma-orm` | Models databases and writes type-safe queries with Prisma ORM. Use for modern Node.js/TypeScript database access. |
| `database` | `redis` | Use Redis for caching, sessions, queues, rate limiting, and pub/sub: data structures, persistence, eviction, and clustering. Use for any high-performance data layer. |
| `database` | `sqlite` | Use SQLite for embedded relational storage: schema, WAL mode, transactions, indexing, and performance. Use for local and mobile data layers. |
| `database` | `vector-databases` | Design and operate vector databases for semantic search and RAG: embeddings, indexes (HNSW), filtering, hybrid search, and scaling. Use for AI retrieval. |
| `design` | `design-spec-md` | Write precise Markdown design specs: requirements, tokens, states, a11y, responsive. Use to make agents understand design exactly. |
| `design` | `diagram-as-code` | Visualize workflows, architecture and business processes as Mermaid/C4/PlantUML with validation. Use for any diagram. |
| `design` | `landing-page-pro` | Design high-converting landing pages end to end: batched intake, page structure, layout choice, conversion copywriting, SEO/AEO, plus a strict visual token system for type, spacing, radius, motion and states. Use for any marketing page, hero, or product section. |
| `desktop` | `electron` | Builds cross-platform desktop applications with Electron, React, and IPC communication. Use for native desktop apps with web tech. |
| `devops` | `ansible` | Automate infrastructure with Ansible: playbooks, roles, inventory, modules, and idempotency. Use for config management and provisioning. |
| `devops` | `argocd` | Deploy applications on Kubernetes with Argo CD: GitOps, applications, sync policies, health checks, and rollbacks. Use for declarative deployments. |
| `devops` | `aws-lambda` | Builds and deploys serverless functions with AWS Lambda, API Gateway, and SAM/CDK. Use for event-driven architectures. |
| `devops` | `cloud-native-ai` | Run production AI on cloud-native stacks: HA serving, multi-model infrastructure, ML canary deploys, and GPU scheduling. Use for ML platforms. |
| `devops` | `docker` | Containerize applications with Docker: Dockerfiles, images, networking, volumes, compose, and production hardening. Use for any deployable service. |
| `devops` | `github-actions` | Automate CI/CD with GitHub Actions: workflows, jobs, matrices, caching, artifacts, and reusable workflows. Use for build, test, and deploy pipelines. |
| `devops` | `gitlab-ci` | Configures GitLab CI/CD pipelines with stages, jobs, and GitLab Runner. Use for Git-native automation and deployment. |
| `devops` | `istio` | Operate a service mesh with Istio: sidecars, traffic routing, mTLS, observability, and resiliency. Use for Kubernetes service management. |
| `devops` | `jenkins` | Operate Jenkins CI/CD: pipelines as code, agents, shared libraries, credentials, and plugins. Use for build and release automation. |
| `devops` | `kafka` | Design and operate Kafka event streaming: topics, producers, consumers, consumer groups, partitioning, and exactly-once. Use for event-driven systems. |
| `devops` | `kubernetes` | Deploy and operate applications on Kubernetes: workloads, services, config, scaling, and GitOps. Use for container orchestration at scale. |
| `devops` | `loki` | Operate log aggregation with Grafana Loki: agents, labels, queries (LogQL), retention, and dashboards. Use for log observability. |
| `devops` | `nginx` | Configure and operate Nginx: reverse proxy, load balancing, TLS, caching, and security headers. Use for web serving and proxying. |
| `devops` | `observability-llm` | LLM observability with Langfuse/LangSmith |
| `devops` | `platform-engineering` | Platform engineering with Backstage/Port |
| `devops` | `prometheus-grafana` | Set up monitoring with Prometheus and Grafana: metrics, exporters, alerting rules, dashboards, and SLO tracking. Use for observability. |
| `devops` | `serverless-ai` | Serverless AI inference (Cloudflare Workers, Lambda) |
| `devops` | `sre-slos` | Define reliability with SRE practices: SLIs, SLOs, error budgets, and data-driven deploy decisions. Use for balancing features with reliability. |
| `devops` | `terraform` | Provision infrastructure as code with Terraform: resources, modules, state, workspaces, and remote backends. Use for cloud resource management. |
| `embedded` | `rust-embedded` | Write embedded firmware in Rust: ARM Cortex-M and RISC-V, no-std, HALs, and memory safety over C/C++. Use for IoT and safety-critical devices. |
| `engineering` | `ai-testing` | AI-powered test generation and validation |
| `engineering` | `claude-code-commands` | Use Claude Code effectively: slash commands, context management, hooks, MCP, permissions, and workflows. Use for agentic coding with Claude Code. |
| `engineering` | `clean-architecture` | Structure codebases with clean architecture: layers, dependency rule, use cases, ports and adapters. Use for maintainable large codebases. |
| `engineering` | `code-review` | Conduct effective code reviews: correctness, security, performance, style, and actionable feedback. Use for reviewing any pull request or diff. |
| `engineering` | `git-workflow` | Use Git effectively: branching, commits, rebase vs merge, history hygiene, conflict resolution, and collaboration workflows. Use for any git-based project. |
| `engineering` | `system-design` | Design scalable systems: requirements, architecture, data models, trade-offs, and scaling strategies. Use for architecture and interviews. |
| `engineering` | `test-driven-development` | Practice test-driven development: red-green-refactor, test design, refactoring safely, and coverage discipline. Use for reliable code evolution. |
| `finance` | `algorithmic-trading` | Build algorithmic trading systems: backtesting, strategy design, order execution, risk management, and market data pipelines. Use for quantitative finance. |
| `finance` | `risk-modeling` | Build financial risk models: VaR, CVaR, Monte Carlo simulation, stress testing, and portfolio risk decomposition. Use for quantitative risk management. |
| `frontend` | `angular` | Build enterprise web apps with Angular: components, signals, services, dependency injection, and testing. Use for scalable structured frontends. |
| `frontend` | `astro` | Build content-focused websites with Astro: islands architecture, content collections, static generation, and integrations. Use for fast content sites. |
| `frontend` | `bun-runtime` | Run JavaScript/TypeScript with Bun: fast installs and builds, hot reload, built-in SQLite, fetch, and WebSocket. Use for all-in-one JS tooling. |
| `frontend` | `modern-css` | Use modern CSS: layout (grid/flex), custom properties, container queries, cascade layers, and responsive design. Use for maintainable styling. |
| `frontend` | `nextjs` | Build full-stack React applications with Next.js App Router, Server Components, API routes, middleware, and deployment. Use for production web apps. |
| `frontend` | `react-19` | Build modern user interfaces with React 19, including Server Components, Actions, hooks, and the new compiler. Use for any interactive UI work. |
| `frontend` | `svelte` | Build reactive UIs with Svelte 5: runes, stores, components, and transitions. Use for efficient interactive frontends. |
| `frontend` | `tailwind-v4` | Style with Tailwind CSS v4: smaller config, container queries, 3D transforms, and the v3 upgrade path. Use for utility-first responsive UIs. |
| `frontend` | `typescript` | Apply TypeScript for type-safe JavaScript: type design, generics, utility types, strict mode, and integration with modern tooling. Use for any JS codebase. |
| `frontend` | `vue` | Build reactive user interfaces with Vue 3: Composition API, reactivity, components, state, and tooling. Use for any Vue-based UI work. |
| `gamedev` | `game-physics` | Implement 2D/3D game physics: rigid bodies, collisions, constraints, raycasting, and performance optimization. Use for realistic game mechanics. |
| `gamedev` | `unity-ecs` | Build scalable Unity games with Entity Component System (ECS): systems, queries, jobs, burst compilation, and DOTS patterns. Use for high-performance Unity. |
| `healthcare` | `hipaa-compliance` | Implement HIPAA compliance in healthcare software: PHI protection, access controls, audit logging, encryption, and breach notification. Use for health IT security. |
| `healthcare` | `hl7-fhir` | Build healthcare integrations with HL7 FHIR: resources, operations, SMART on FHIR apps, and clinical data exchange. Use for health IT interoperability. |
| `mobile` | `expo-rn` | Ship iOS and Android from one codebase with Expo: native features, OTA updates, EAS build, and no native tooling setup. Use for cross-platform MVPs. |
| `mobile` | `flutter` | Build cross-platform mobile apps with Flutter: widgets, state management, navigation, platform channels, and release builds. Use for iOS/Android/desktop. |
| `mobile` | `kotlin-android` | Build Android apps with Kotlin: Compose UI, coroutines, architecture components, and Gradle. Use for modern native Android development. |
| `mobile` | `swift-ios` | Build iOS apps with Swift and SwiftUI: views, state, navigation, concurrency, and Combine. Use for native Apple platforms. |
| `qa` | `browser-automation` | Automate browsers with Playwright: selectors, waits, assertions, screenshots, network interception, and CI. Use for E2E tests and scraping. |
| `qa` | `jest` | Write reliable JavaScript tests with Jest: unit tests, mocking, snapshots, coverage, and CI integration. Use for JS/TS testing. |
| `qa` | `pytest` | Write reliable Python tests with pytest: fixtures, parametrize, mocking, async tests, and CI integration. Use for any Python testing. |
| `security` | `api-security` | Secure web APIs: authentication, authorization, rate limiting, input validation, and abuse protection. Use for hardening any API. |
| `security` | `oauth2-jwt` | Implements OAuth 2.0 authentication and JWT-based authorization with refresh tokens. Use for secure API access. |
| `security` | `owasp-web-security` | Harden web applications against the OWASP Top 10: injection, XSS, auth flaws, CSRF, SSRF, and insecure dependencies. Use for any web app security review. |
| `security` | `secrets-management` | Manage secrets safely: vaults, rotation, environment variables, scanning, and least privilege. Use for protecting credentials and keys. |

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
agent-skills search <query>      # Search by name, description, tags
agent-skills validate --json out.json
agent-skills quality --json out.json
agent-skills catalog             # Rebuild catalog JSON
agent-skills stats               # Library statistics
```

### GitHub Action

Validate, score, and catalog skills in your own repo with the
[Claude Skills Action](action.yml):

```yaml
name: Validate skills
on:
  pull_request:

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ssrjkk/agent-skills@v4.1.1
        with:
          command: validate      # validate | quality | catalog | stats
          target: .claude/skills # path to skills directory
          output: skills_catalog.json
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

## Domains (17)
`ai` · `backend` · `blockchain` · `data` · `database` · `design` · `desktop` ·
`devops` · `embedded` · `engineering` · `finance` · `frontend` · `gamedev` ·
`healthcare` · `mobile` · `qa` · `security`

## Author

**ssrjkk** — creator & maintainer

<p align="center">
  <a href="https://github.com/ssrjkk"><img src="https://img.shields.io/badge/GitHub-ssrjkk-181717?style=for-the-badge&logo=github" alt="GitHub"></a>
  <a href="https://t.me/ssrjkk_bot"><img src="https://img.shields.io/badge/Telegram-@ssrjkk_bot-26A5E4?style=for-the-badge&logo=telegram" alt="Telegram bot"></a>
  <a href="https://t.me/ssrjkk"><img src="https://img.shields.io/badge/Telegram-@ssrjkk-26A5E4?style=for-the-badge&logo=telegram" alt="Telegram"></a>
  <a href="mailto:ray013lefe@gmail.com"><img src="https://img.shields.io/badge/Email-ray013lefe%40gmail.com-D14836?style=for-the-badge&logo=gmail" alt="Email"></a>
</p>

## For Contributors

See [CONTRIBUTING.md](CONTRIBUTING.md). Quick checklist:
- [ ] `SKILL.md` has frontmatter with name, description, category, tags, models, version
- [ ] `SKILL.ru.md` is a **real translation** (not auto-generated)
- [ ] Code examples compile and run
- [ ] `SKILL.md` passes `scripts/check_agent_interop.py` (portable to all agents)
- [ ] `make test` passes
- [ ] `make lint` passes

## Development

```bash
pip install -e ".[dev]"   # ruff, mypy, pytest
make all                  # lint → typecheck → test → validate → catalog → docs
```

Optional, recommended for contributors:

```bash
pip install pre-commit && pre-commit install   # ruff + mypy + validate on every commit
```

Layout: `.claude/skills/{domain}/{skill}/SKILL.md` (skills) · `roadmaps/<slug>.json`
(standalone IT maps, schema: `roadmaps.schema.json`) · `src/claude_skills/` (SDK +
CLI) · `scripts/` (CI helpers) · `docs/` (generated site, do not hand-edit).

## Links

- [Live Catalog Site](https://ssrjkk.github.io/agent-skills/)
- [Telegram Bot](https://t.me/ssrjkk_bot)
- [Architecture Guide](docs/ARCHITECTURE.md)
- [Release Notes](docs/RELEASE_NOTES_v4.0.md)
- [Roadmap](ROADMAP.md)
- [Issue Tracker](https://github.com/ssrjkk/agent-skills/issues)
- [IT Roadmaps](https://ssrjkk.github.io/agent-skills/roadmaps.html) (every direction, soon)

## Why this library

- **Curated, not generated** — 103 hand-reviewed skills that pass a 5-dimension
  quality pipeline (completeness, depth, code quality, freshness, bilingual).
- **Universal Agent Skills format** — the same `SKILL.md` convention native to
  Claude Code and supported by OpenCode, Cursor, Windsurf, and others. No
  lock-in: install once, use anywhere.
- **Bilingual (EN + RU)** — every skill ships a real Russian translation, not
  a machine one.
- **Works across every LLM/GLM ecosystem** — skills are written to work with
  Claude (Sonnet/Opus), OpenAI (GPT), Google (Gemini), and Zhipu GLM models.
- **Quality enforced in CI** — validation, quality scoring, anti-pattern
  detection, cross-agent interop checks, 100% test coverage. What you see in
  `main` is what passes the bar.
- **SDK + CLI + GitHub Action** — validate, score, catalog and search any
  skills library programmatically.

## Supported agents & models

The `SKILL.md` format is universal — every skill works with any agent that
implements the Agent Skills spec, across model providers:

<p align="center">
  <img src="https://img.shields.io/badge/Claude%20Code-Claude%20Sonnet%2FOpus-8B5CF6?style=flat-square&logo=anthropic" alt="Claude">
  <img src="https://img.shields.io/badge/OpenAI-GPT%20Series-10A37F?style=flat-square&logo=openai" alt="OpenAI">
  <img src="https://img.shields.io/badge/Google-Gemini-4285F4?style=flat-square&logo=google" alt="Gemini">
  <img src="https://img.shields.io/badge/Zhipu-GLM%20Series-3859FF?style=flat-square" alt="GLM">
  <img src="https://img.shields.io/badge/OpenCode-%E2%9C%93-00C9A7?style=flat-square" alt="OpenCode">
  <img src="https://img.shields.io/badge/Cursor-%E2%9C%93-6C5CE7?style=flat-square" alt="Cursor">
  <img src="https://img.shields.io/badge/Windsurf-%E2%9C%93-00B3FF?style=flat-square" alt="Windsurf">
</p>

## Legacy Version

The original v1.0 library (10,000+ auto-generated skills) is archived under
the `v1.0-legacy` tag — v3.1 is a complete rewrite focused on quality:

```bash
git checkout v1.0-legacy
```

## License

MIT.