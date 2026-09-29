# Release Notes - v3.2

## Highlights

- **37/37 skills at 100.0% quality (Grade A)** — 16 new production skills added.
- **12 domains** (was 11) — new `data` domain; expanded `ai`, `backend`,
  `database`, `devops`, `engineering`, `frontend`, `security`.
- **New skills (16):**
  - `ai`: `prompt-engineering`, `rag-pipeline`, `agent-development`
  - `backend`: `fastapi`, `go-rest-api`
  - `data`: `pandas`
  - `database`: `postgresql`, `redis`
  - `devops`: `docker`, `github-actions`, `kubernetes`
  - `engineering`: `code-review`
  - `frontend`: `nextjs`, `react-19`, `typescript`
  - `security`: `owasp-web-security`
- **Cross-provider model tags** — new skills declare `sonnet`, `opus`, `gpt-5`,
  `gemini-2.5`, and `glm-4.6` for portability across Claude, OpenAI, Google, and
  Zhipu GLM ecosystems.
- **GitHub Pages live site** — the catalog site is deployed via CI
  (`ssrjkk.github.io/agent-skills/`).
- **PyPI publish workflow** — ready to publish `claude-skills-library` on tag
  (set the `PUBLISH_TO_PYPI` repo variable and `PYPI_API_TOKEN` secret).
- **Social preview banner** — new OpenGraph image for link sharing.

## Quality Report

```
37/37 skills at 100.0% (A)
Grade A:  37/37
Bilingual coverage: 37/37 (100%)
Average score: 100.0
```

## Validation

- 133 tests pass; `ruff` clean; `mypy` clean (src + tests).
- Catalog: 37 skills, 12 domains, 37 Russian translations, regenerated from
  source with anti-pattern detection and agent-interop checks passing.