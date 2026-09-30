<p align="center">
  <img src="https://img.shields.io/badge/skills-100-blue?style=for-the-badge" alt="Skills">
  <img src="https://img.shields.io/badge/languages-EN%20%7C%20RU-green?style=for-the-badge" alt="Languages">
  <img src="https://img.shields.io/badge/domains-16-orange?style=for-the-badge" alt="Domains">
  <img src="https://img.shields.io/badge/quality-SSS%20(100%25)-brightgreen?style=for-the-badge" alt="Quality">
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
  <a href="https://github.com/ssrjkk/agent-skills/discussions">Discussions</a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/ssrjkk/agent-skills/main/.github/social-preview.svg" alt="Skills Library banner" width="640">
</p>

---

## Install in one line

```bash
curl -fsSL https://raw.githubusercontent.com/ssrjkk/agent-skills/main/install.sh | bash
```

Or clone directly into your agent's skills directory:

| Agent      | Command |
|------------|---------|
| Claude Code | `git clone --depth 1 https://github.com/ssrjkk/agent-skills.git ~/.claude/skills` |
| OpenCode   | `git clone --depth 1 https://github.com/ssrjkk/agent-skills.git ~/.opencode/skills` |
| Cursor     | `git clone --depth 1 https://github.com/ssrjkk/agent-skills.git ~/.cursor/skills` |
| Windsurf   | `git clone --depth 1 https://github.com/ssrjkk/agent-skills.git ~/.windsurf/skills` |

## What is this?

100 production-grade, bilingual (English + Russian) skills following the
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
| Total skills | **100** |
| Russian translations | **100 (100%)** |
| Domains | **16** |
| Quality score | **100% (SSS rank)** |
| Test coverage | **100%** |
| License | MIT |

Only skills meeting the quality bar (Grade A, no validation errors) are kept
in `main`. Everything else is archived under the `v1.0-legacy` tag.

## Skills by domain

| Domain | Skill | Description |
|--------|-------|-------------|
| `ai` | `agent-development` | Build reliable LLM agents and agentic workflows: tool use, memory, loops, guardrails, and evaluation |
| `ai` | `context-engineering` | Curate LLM context windows for quality and cost: system prompts, compaction, just-in-time retrieval, progressive disclosure, and token budgets |
| `ai` | `embeddings` | Work with text embeddings: model selection, vectorization, similarity, clustering, and caching for search and retrieval |
| `ai` | `few-shot-learning` | Designs and curates few-shot examples to guide LLM behavior, including example selection, formatting, and ordering |
| `ai` | `function-calling` | Implement robust LLM function/tool calling: schemas, multi-call handling, validation, error recovery, and structured execution |
| `ai` | `llm-evals` | Build evaluation suites for LLM applications: golden datasets, metrics, LLM-as-judge, regression gates, and CI integration |
| `ai` | `llm-finetuning` | Fine-tunes open-source LLMs (Llama, Mistral, Qwen) using LoRA/QLoRA with HuggingFace and Unsloth |
| `ai` | `llm-guardrails` | Add safety guardrails to LLM apps: prompt injection defense, content filtering, PII protection, policy enforcement, and red-teaming |
| `ai` | `mcp-servers` | Build Model Context Protocol servers and clients: tools, resources, prompts, transport, and secure agent integration |
| `ai` | `mlops` | Operate machine learning in production: experiment tracking, pipelines, model registry, serving, monitoring, and CI/CD for ML |
| `ai` | `multi-agent-orchestration` | Design and run multi-agent systems: orchestrator-worker, routing, handoffs, shared state, and coordination patterns |
| `ai` | `prompt-caching` | Optimize LLM cost and latency with prompt caching: cacheable prefixes, cache-control headers, context layout, and cache-aware prompting |
| `ai` | `prompt-engineering` | Design effective prompts for LLMs: role framing, structured output, chain-of-thought, few-shot, and evaluation |
| `ai` | `rag-pipeline` | Build retrieval-augmented generation pipelines: chunking, embeddings, vector search, hybrid retrieval, and citation |
| `ai` | `structured-output` | Force LLMs to emit valid, schema-constrained structured output: JSON modes, function calling, JSON Schema validation, and error recovery |
| `backend` | `deno-runtime` | Deno runtime and standard library |
| `backend` | `django` | Build secure web applications with Django: models, views, ORM, admin, auth, REST APIs, and deployment |
| `backend` | `dotnet` | Build  |
| `backend` | `express` | Build Node |
| `backend` | `fastapi` | Build high-performance Python APIs with FastAPI: routing, Pydantic validation, async, dependency injection, OpenAPI, and testing |
| `backend` | `go-rest-api` | Build production REST APIs in Go with the standard library or Gin, including routing, middleware, JSON handling, and testing |
| `backend` | `graphql` | Design and implement GraphQL APIs: schemas, resolvers, queries, mutations, subscriptions, and N+1 avoidance |
| `backend` | `grpc` | Build high-performance services with gRPC: protobuf schemas, unary/streaming RPCs, interceptors, and error handling |
| `backend` | `laravel` | Build PHP web applications with Laravel: routing, Eloquent ORM, Blade, migrations, validation, and deployment |
| `backend` | `nestjs` | Creates Node |
| `backend` | `rest-api-design` | Design consistent REST APIs: resource modeling, status codes, pagination, versioning, error contracts, and documentation |
| `backend` | `rust-tokio` | Async Rust with Tokio runtime |
| `backend` | `spring-boot` | Build production Java/Kotlin backends with Spring Boot: REST controllers, dependency injection, data access, security, and testing |
| `backend` | `websockets` | Build real-time features with WebSockets: connection lifecycle, protocols, backpressure, scaling, and reconnection |
| `blockchain` | `zk-proofs` | Zero-knowledge proof development |
| `data` | `airflow` | Orchestrate data pipelines with Apache Airflow: DAGs, tasks, dependencies, sensors, and retries |
| `data` | `apache-spark` | Process large-scale data with Apache Spark: DataFrames, SQL, joins, partitioning, and optimization |
| `data` | `data-visualization` | Create clear data visualizations with Matplotlib, Plotly, and Altair: chart selection, design, interactivity, and dashboards |
| `data` | `dbt` | Build analytics engineering workflows with dbt: models, tests, sources, macros, and documentation |
| `data` | `elasticsearch` | Design and operate Elasticsearch: mappings, indexing, queries, aggregations, and cluster tuning |
| `data` | `pandas` | Analyze and transform tabular data with pandas: dataframes, cleaning, aggregation, joins, and time series |
| `data` | `sql-querying` | Write correct and efficient SQL: joins, aggregations, window functions, CTEs, and query optimization |
| `database` | `clickhouse` | Design and operate ClickHouse for OLAP analytics: columnar tables, engines, aggregations, partitioning, and performance |
| `database` | `mongodb` | Design and operate MongoDB: document modeling, queries, indexes, aggregation, replication, and sharding |
| `database` | `mysql` | Design and operate MySQL: schema, InnoDB tuning, indexing, transactions, replication, and query optimization |
| `database` | `postgresql` | Design and operate PostgreSQL databases: schema design, indexing, query optimization, transactions, and migrations |
| `database` | `prisma-orm` | Models databases and writes type-safe queries with Prisma ORM |
| `database` | `redis` | Use Redis for caching, sessions, queues, rate limiting, and pub/sub: data structures, persistence, eviction, and clustering |
| `database` | `sqlite` | Use SQLite for embedded relational storage: schema, WAL mode, transactions, indexing, and performance |
| `database` | `vector-databases` | Design and operate vector databases for semantic search and RAG: embeddings, indexes (HNSW), filtering, hybrid search, and scaling |
| `desktop` | `electron` | Builds cross-platform desktop applications with Electron, React, and IPC communication |
| `devops` | `ansible` | Automate infrastructure with Ansible: playbooks, roles, inventory, modules, and idempotency |
| `devops` | `argocd` | Deploy applications on Kubernetes with Argo CD: GitOps, applications, sync policies, health checks, and rollbacks |
| `devops` | `aws-lambda` | Builds and deploys serverless functions with AWS Lambda, API Gateway, and SAM/CDK |
| `devops` | `cloud-native-ai` | Cloud-native AI deployment patterns |
| `devops` | `docker` | Containerize applications with Docker: Dockerfiles, images, networking, volumes, compose, and production hardening |
| `devops` | `github-actions` | Automate CI/CD with GitHub Actions: workflows, jobs, matrices, caching, artifacts, and reusable workflows |
| `devops` | `gitlab-ci` | Configures GitLab CI/CD pipelines with stages, jobs, and GitLab Runner |
| `devops` | `istio` | Operate a service mesh with Istio: sidecars, traffic routing, mTLS, observability, and resiliency |
| `devops` | `jenkins` | Operate Jenkins CI/CD: pipelines as code, agents, shared libraries, credentials, and plugins |
| `devops` | `kafka` | Design and operate Kafka event streaming: topics, producers, consumers, consumer groups, partitioning, and exactly-once |
| `devops` | `kubernetes` | Deploy and operate applications on Kubernetes: workloads, services, config, scaling, and GitOps |
| `devops` | `loki` | Operate log aggregation with Grafana Loki: agents, labels, queries (LogQL), retention, and dashboards |
| `devops` | `nginx` | Configure and operate Nginx: reverse proxy, load balancing, TLS, caching, and security headers |
| `devops` | `observability-llm` | LLM observability with Langfuse/LangSmith |
| `devops` | `platform-engineering` | Platform engineering with Backstage/Port |
| `devops` | `prometheus-grafana` | Set up monitoring with Prometheus and Grafana: metrics, exporters, alerting rules, dashboards, and SLO tracking |
| `devops` | `serverless-ai` | Serverless AI inference (Cloudflare Workers, Lambda) |
| `devops` | `sre-slos` | SRE SLI/SLO/SLA implementation |
| `devops` | `terraform` | Provision infrastructure as code with Terraform: resources, modules, state, workspaces, and remote backends |
| `embedded` | `rust-embedded` | Rust for embedded systems |
| `engineering` | `ai-testing` | AI-powered test generation and validation |
| `engineering` | `claude-code-commands` | Use Claude Code effectively: slash commands, context management, hooks, MCP, permissions, and workflows |
| `engineering` | `clean-architecture` | Structure codebases with clean architecture: layers, dependency rule, use cases, ports and adapters |
| `engineering` | `code-review` | Conduct effective code reviews: correctness, security, performance, style, and actionable feedback |
| `engineering` | `git-workflow` | Use Git effectively: branching, commits, rebase vs merge, history hygiene, conflict resolution, and collaboration workflows |
| `engineering` | `system-design` | Design scalable systems: requirements, architecture, data models, trade-offs, and scaling strategies |
| `engineering` | `test-driven-development` | Practice test-driven development: red-green-refactor, test design, refactoring safely, and coverage discipline |
| `finance` | `algorithmic-trading` | Build algorithmic trading systems: backtesting, strategy design, order execution, risk management, and market data pipelines |
| `finance` | `risk-modeling` | Build financial risk models: VaR, CVaR, Monte Carlo simulation, stress testing, and portfolio risk decomposition |
| `frontend` | `angular` | Build enterprise web apps with Angular: components, signals, services, dependency injection, and testing |
| `frontend` | `astro` | Build content-focused websites with Astro: islands architecture, content collections, static generation, and integrations |
| `frontend` | `bun-runtime` | Bun runtime for JavaScript/TypeScript |
| `frontend` | `modern-css` | Use modern CSS: layout (grid/flex), custom properties, container queries, cascade layers, and responsive design |
| `frontend` | `nextjs` | Build full-stack React applications with Next |
| `frontend` | `react-19` | Build modern user interfaces with React 19, including Server Components, Actions, hooks, and the new compiler |
| `frontend` | `svelte` | Build reactive UIs with Svelte 5: runes, stores, components, and transitions |
| `frontend` | `tailwind-v4` | Tailwind CSS v4 features |
| `frontend` | `typescript` | Apply TypeScript for type-safe JavaScript: type design, generics, utility types, strict mode, and integration with modern tooling |
| `frontend` | `vue` | Build reactive user interfaces with Vue 3: Composition API, reactivity, components, state, and tooling |
| `gamedev` | `game-physics` | Implement 2D/3D game physics: rigid bodies, collisions, constraints, raycasting, and performance optimization |
| `gamedev` | `unity-ecs` | Build scalable Unity games with Entity Component System (ECS): systems, queries, jobs, burst compilation, and DOTS patterns |
| `healthcare` | `hipaa-compliance` | Implement HIPAA compliance in healthcare software: PHI protection, access controls, audit logging, encryption, and breach notification |
| `healthcare` | `hl7-fhir` | Build healthcare integrations with HL7 FHIR: resources, operations, SMART on FHIR apps, and clinical data exchange |
| `mobile` | `expo-rn` | Expo SDK for React Native development |
| `mobile` | `flutter` | Build cross-platform mobile apps with Flutter: widgets, state management, navigation, platform channels, and release builds |
| `mobile` | `kotlin-android` | Build Android apps with Kotlin: Compose UI, coroutines, architecture components, and Gradle |
| `mobile` | `swift-ios` | Build iOS apps with Swift and SwiftUI: views, state, navigation, concurrency, and Combine |
| `qa` | `browser-automation` | Automate browsers with Playwright: selectors, waits, assertions, screenshots, network interception, and CI |
| `qa` | `jest` | Write reliable JavaScript tests with Jest: unit tests, mocking, snapshots, coverage, and CI integration |
| `qa` | `pytest` | Write reliable Python tests with pytest: fixtures, parametrize, mocking, async tests, and CI integration |
| `security` | `api-security` | Secure web APIs: authentication, authorization, rate limiting, input validation, and abuse protection |
| `security` | `oauth2-jwt` | Implements OAuth 2 |
| `security` | `owasp-web-security` | Harden web applications against the OWASP Top 10: injection, XSS, auth flaws, CSRF, SSRF, and insecure dependencies |
| `security` | `secrets-management` | Manage secrets safely: vaults, rotation, environment variables, scanning, and least privilege |

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
      - uses: ssrjkk/agent-skills@v3.5.0
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

**SSS rank** is the top tier: a skill must score 100% on all five dimensions
**and** be structurally advanced — at least 4 code blocks and 90+ lines of body
content. All 100 skills in this library hold the SSS rank.

## Domains (16)

`ai` · `backend` · `blockchain` · `data` · `database` · `desktop` · `devops` ·
`embedded` · `engineering` · `finance` · `frontend` · `gamedev` · `healthcare` ·
`mobile` · `qa` · `security`

## Author

**ssrjkk** — creator & maintainer

<p align="center">
  <a href="https://github.com/ssrjkk"><img src="https://img.shields.io/badge/GitHub-ssrjkk-181717?style=for-the-badge&logo=github" alt="GitHub"></a>
  <a href="https://t.me/ssrjkk"><img src="https://img.shields.io/badge/Telegram-@ssrjkk-26A5E4?style=for-the-badge&logo=telegram" alt="Telegram"></a>
  <a href="https://twitter.com/ssrjkk"><img src="https://img.shields.io/badge/Twitter/X-@ssrjkk-000000?style=for-the-badge&logo=x" alt="Twitter/X"></a>
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

## Links

- [Live Catalog Site](https://ssrjkk.github.io/agent-skills/)
- [Architecture Guide](docs/ARCHITECTURE.md)
- [Release Notes](docs/RELEASE_NOTES_v4.0.md)
- [Roadmap](ROADMAP.md)
- [Issue Tracker](https://github.com/ssrjkk/agent-skills/issues)

## Why this library

- **Curated, not generated** — 100 hand-reviewed skills that pass a 5-dimension
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