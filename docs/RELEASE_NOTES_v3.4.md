# Release Notes - v3.4

## Highlights

- **59/59 skills at 100.0% quality (Grade A)** — 12 new skills.
- **Modern packaging** — moved to `pyproject.toml` (PEP 621), ready for PyPI
  publication as `claude-skills-library`.
- **New skills (12):**
  - `ai`: `mlops`
  - `backend`: `django`, `grpc`, `express`
  - `data`: `elasticsearch`
  - `database`: `mongodb`
  - `devops`: `terraform`, `kafka`, `prometheus-grafana`
  - `frontend`: `vue`
  - `mobile`: `flutter`
  - `qa`: `pytest`
- **Community infrastructure** — added `FUNDING.yml`, `AGENTS.md`,
  `SECURITY.md`, and `ROADMAP.md`.
- **Docs site** — improved search (name/domain/tags) and shows supported models.

## Quality Report

```
59/59 skills at 100.0% (A)
Grade A:  59/59
Bilingual coverage: 59/59 (100%)
Average score: 100.0
```

## Validation

- 133 tests pass; `ruff` clean; `mypy` clean (src + tests).
- Catalog: 59 skills, 13 domains, 59 Russian translations, regenerated from
  source with anti-pattern detection and agent-interop checks passing.