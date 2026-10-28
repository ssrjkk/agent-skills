# Release Notes - v4.1

## Highlights

- **103/103 skills at 98.9% quality** across 17 domains, 103 Russian
  translations. New skill: `design/landing-page-pro` (conversion-first
  landing process, EN+RU, adapted from elayadesign/ai-design-skills, MIT).
- **Bilingual site**: full EN/RU language switcher, RU tabs on every skill
  page, bilingual search index, relevance-ranked results.
- **One shared `assets/site.js`** instead of duplicated inline scripts on
  142 pages (-12k lines), with Node syntax checks on every page in CI.
- **Honest quality signals**: RU translation checks (W040/W041), filler-word
  notes (I030), and a new `agent-skills stale` review queue. Gates unchanged:
  0 errors, 0 warnings on the full corpus.
- **Dependency refresh**: click 8.5, build 1.6.1, hypothesis 6.168.5,
  setuptools 84.2.1, twine 7.0, pypi-publish action 1.14.3 (supersedes
  Dependabot PRs #17-#22, verified in an isolated venv).

## Quality Report

```
103/103 skills at 98.89
Bilingual coverage: 103/103 (100%)
Average score: 98.89
```

## Validation

- 184 tests pass; `ruff` clean; `mypy` clean (src + tests).
- Catalog: 103 skills, 17 domains, 103 Russian translations, regenerated from
  source with anti-pattern detection and agent-interop checks passing.
- Package builds cleanly (`python -m build`, `twine check` pass).
