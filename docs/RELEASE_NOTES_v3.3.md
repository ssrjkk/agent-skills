# Release Notes - v3.3

## Highlights

- **47/47 skills at 100.0% quality (Grade A)** — 10 new agent-focused skills.
- **13 domains** (was 12) — new `qa` domain.
- **New skills (10):**
  - `ai`: `mcp-servers`, `llm-evals`, `function-calling`, `prompt-caching`
  - `backend`: `rest-api-design`
  - `data`: `sql-querying`
  - `database`: `vector-databases`
  - `engineering`: `git-workflow`, `claude-code-commands`
  - `qa`: `browser-automation`
- **Agent-first coverage** — skills for the hottest 2026 agent topics: Model
  Context Protocol, LLM evaluation, function/tool calling, prompt caching,
  vector retrieval, browser automation, and Claude Code workflows.
- **Cross-provider model tags** — all new skills declare `sonnet`, `opus`,
  `gpt-5`, `gemini-2.5`, and `glm-4.6`.
- Live catalog site continues to deploy from CI:
  `ssrjkk.github.io/claude-skills/`.

## Quality Report

```
47/47 skills at 100.0% (A)
Grade A:  47/47
Bilingual coverage: 47/47 (100%)
Average score: 100.0
```

## Validation

- 133 tests pass; `ruff` clean; `mypy` clean (src + tests).
- Catalog: 47 skills, 13 domains, 47 Russian translations, regenerated from
  source with anti-pattern detection and agent-interop checks passing.