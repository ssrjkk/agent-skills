---
name: gitlab-ci
description: "Configures GitLab CI/CD pipelines with stages, jobs, and GitLab Runner. Use for Git-native automation and deployment."
category: devops
tags: [gitlab, ci-cd, pipelines, runner, devops]
models: [sonnet, opus]
version: 1.0.0
created: 2026-05-14
updated: 2026-09-29
---
# GitLab CI/CD

> Git-integrated CI/CD with powerful pipeline orchestration.

## Quick Start
```yaml
stages:
  - test
  - build
  - deploy

test:
  stage: test
  image: node:20
  script:
    - npm ci
    - npm test

build:
  stage: build
  script:
    - npm run build
  artifacts:
    paths:
      - dist/
```

## When to Use
- GitLab-hosted repositories
- Auto DevOps deployments
- Multi-project pipelines
- Container registry integration

## Step-by-Step
1. Add `.gitlab-ci.yml` to repo root
2. Configure stages and jobs
3. Set up GitLab Runner
4. Push to trigger pipeline

## Dependencies
```bash
# Local runner
gitlab-runner register
```

## Examples
```yaml
deploy:
  stage: deploy
  only:
    - main
  script:
    - kubectl apply -f k8s/
  environment: production
```

## Resources
- [GitLab CI Docs](https://docs.gitlab.com/ee/ci)

## Troubleshooting
- **Job stuck in pending** — runner has no tag match. Add `tags: [docker]`
  to the job or register the runner with matching tags.
- **Pipeline fails on `npm ci`** — cache is stale. Clear the cache from
  *CI/CD → Pipelines → Run pipeline* or bump the cache `key`.
- **Deploy stage skipped** — `only: [main]` blocks feature branches;
  use `rules: [if: '$CI_COMMIT_BRANCH == "main"']` for finer control.
- **Runner runs as `sh`, not `bash`** — set `image` per job or use
  POSIX-compatible script lines (`|| true`, no `set -o pipefail`).

## Validation
1. Pipeline starts on commit
2. All stages execute in order
3. Deployments succeed
