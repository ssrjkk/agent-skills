# Release Notes - v3.5

## Highlights

- **65/65 skills at 100.0% quality (Grade A)** across 16 domains.
- **PyPI published** — `agent-skills-library` is live on PyPI:
  ```bash
  pip install agent-skills-library
  ```
- **CLI alias** — both `agent-skills` and `claude-skills` commands work.
- **Repo renamed** to `agent-skills` (old `claude-skills` URLs redirect).
- **Accuracy pass** — README, docs, badges, and the catalog now consistently
  report 65 skills / 16 domains (finance, gamedev, healthcare were present in
  the library but missing from docs).
- **Housekeeping** — removed stale v1.0 examples (`skill-XXXX` references),
  added `CODE_OF_CONDUCT.md`, rebuilt the site with SEO meta + favicon.

## Quality Report

```
65/65 skills at 100.0% (A)
Grade A:  65/65
Bilingual coverage: 65/65 (100%)
Average score: 100.0
```

## Validation

- 133 tests pass; `ruff` clean; `mypy` clean (src + tests).
- Catalog: 65 skills, 16 domains, 65 Russian translations, regenerated from
  source with anti-pattern detection and agent-interop checks passing.