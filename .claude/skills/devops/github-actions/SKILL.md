---
name: github-actions
description: "Automate CI/CD with GitHub Actions: workflows, jobs, matrices, caching, artifacts, and reusable workflows. Use for build, test, and deploy pipelines."
category: devops
tags: [github-actions, ci, cd, workflows, automation, pipelines, github]
models: [sonnet, opus, gpt-5, gemini-2.5, glm-4.6]
version: 1.0.0
created: 2026-09-20
updated: 2026-09-28
author: ssrjkk
---
# GitHub Actions

> Automating build, test, and deploy pipelines with GitHub Actions.

## Quick Start
```bash
# Add .github/workflows/ci.yml and push
# Workflow runs on push/PR automatically
```

## When to Use
- Running tests and linting on every PR
- Building and publishing artifacts
- Deploying to cloud, registries, and Pages
- Scheduled jobs and dependency updates

## Best Practices

### Workflow Design
- Split CI/CD into separate workflows or jobs
- Use job `needs` for ordering; `matrix` for version combos
- Cache dependencies (`actions/cache`) for speed
- Keep secrets in repo/org secrets; never in YAML

### Security
- Pin action versions (`@v4`) or commit SHAs
- Use `permissions:` minimal scope per job
- Sanitize untrusted inputs (PRs from forks)
- Avoid `pull_request_target` unless you handle secrets carefully

### Efficiency
- Trigger only on relevant paths (`on: push: paths:`)
- Use concurrency to cancel stale runs
- Reuse workflows via `workflow_call`
- Upload artifacts only when needed

## Dependencies
```bash
# None required — GitHub-hosted runners have common tools.
# Pin versions:
#   actions/checkout@v4, actions/setup-python@v5, actions/cache@v4
```

## Examples
```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: pip
      - run: pip install -e ".[dev]"
      - run: ruff check .
      - run: pytest tests/ -q
```
```yaml
# Deploy on tag with permissions
name: Deploy

on:
  push:
    tags: ["v*"]

permissions:
  contents: write

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: echo "deploying ${{ github.ref_name }}"
        env:
          TOKEN: ${{ secrets.DEPLOY_TOKEN }}
```
```yaml
# Reusable workflow
name: Quality
on:
  workflow_call:

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci && npm run lint
```
```yaml
# Scheduled + caching
name: Nightly

on:
  schedule:
    - cron: "0 2 * * *"

jobs:
  nightly:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: pip-${{ hashFiles('requirements.txt') }}
      - run: pip install -r requirements.txt
```

## Step-by-Step
1. Define the trigger (`on`) and job breakdown.
2. Checkout code and set up the language runtime.
3. Cache dependencies for speed.
4. Run lint, typecheck, and tests in parallel jobs where possible.
5. Add a build/publish step gated on success.
6. Add deployment job with `needs` and environment protection.
7. Set `permissions` minimal; store secrets in repo settings.
8. Review Actions logs; add status badges to the README.

## Validation
1. Workflow runs green on push and PR
2. Matrix covers the supported versions
3. Artifacts/secrets used correctly (no leaks in logs)
4. Caching measurably speeds up runs
5. Cancelled stale runs via concurrency

## Troubleshooting
- "Permission denied" on push/deploy: check `permissions` and token scope.
- Secrets missing: define them in repo/org settings.
- Flaky runs: pin action versions and runner images.