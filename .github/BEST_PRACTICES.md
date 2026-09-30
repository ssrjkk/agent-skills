# Best Practices for Using Agent Skills

## Overview

This guide covers how to get the most value from the curated skills in this
library. Every skill lives under `.claude/skills/{domain}/{skill}/` and is
portable to Claude Code, OpenCode, Cursor, Windsurf, and other agents.

## How to reference a skill

The universal Agent Skills format is `domain/skill-name`. Reference the exact
name so the agent loads the right file:

```
Use skill backend/fastapi to build a REST API with JWT auth
```

## Skill selection by task

| Task | Skill |
|------|-------|
| Build a REST API (Python) | `backend/fastapi` |
| Build a REST API (Go) | `backend/go-rest-api` |
| Design an API contract | `backend/rest-api-design` |
| React UI | `frontend/react-19` |
| Full-stack React | `frontend/nextjs` |
| Type-safe JavaScript | `frontend/typescript` |
| PostgreSQL schema & queries | `database/postgresql` |
| SQL queries & analysis | `data/sql-querying` |
| Cache / queues / rate limiting | `database/redis` |
| Semantic search / RAG | `database/vector-databases` |
| RAG pipeline | `ai/rag-pipeline` |
| LLM agents with tools | `ai/agent-development` |
| MCP servers | `ai/mcp-servers` |
| Prompt design | `ai/prompt-engineering` |
| Function calling | `ai/function-calling` |
| LLM evaluation | `ai/llm-evals` |
| Dockerize a service | `devops/docker` |
| Kubernetes | `devops/kubernetes` |
| CI/CD (GitHub) | `devops/github-actions` |
| Infrastructure as code | `devops/terraform` |
| Event streaming | `devops/kafka` |
| Metrics & dashboards | `devops/prometheus-grafana` |
| E2E tests (Playwright) | `qa/browser-automation` |
| Python tests | `qa/pytest` |
| Code review | `engineering/code-review` |
| Git workflows | `engineering/git-workflow` |
| Auth (OAuth2/JWT) | `security/oauth2-jwt` |
| Web security (OWASP) | `security/owasp-web-security` |

## Combining skills

Combine skills to cover a full feature:

```
Use skills:
1. backend/fastapi          (API layer)
2. database/postgresql      (data)
3. security/oauth2-jwt      (auth)
4. qa/pytest                (tests)
5. devops/docker            (container)
```

## Golden rules

1. Reference the exact skill name — don't paraphrase.
2. Ask for tests alongside the feature (`qa/pytest` or `qa/browser-automation`).
3. Ask for error handling and validation explicitly.
4. Ask for security review on auth/payment/data code (`security/owasp-web-security`).
5. Keep prompts focused: one skill per concern, combine when needed.

## Validation

- Run `make validate` and `make quality` — expect 0 errors, 100% score.
- Run `python scripts/check_agent_interop.py` for cross-agent portability.
- Run `make test` before pushing changes.