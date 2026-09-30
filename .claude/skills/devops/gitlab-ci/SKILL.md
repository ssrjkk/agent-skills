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

## Best Practices
- Name jobs clearly and keep each stage single-purpose.
- Cache dependencies and use `needs` for fast pipelines.
- Store secrets in CI/CD variables, masked and scoped.
- Use rules (not only/except) for branch-based triggers.
- Upload artifacts and reports for visibility.
- Reuse logic with `include` and templates.

## Step-by-Step
1. Add `.gitlab-ci.yml` to repo root
2. Configure stages and jobs
3. Set up GitLab Runner
4. Push to trigger pipeline
5. Add caching and rules
6. Secure variables and deploy

## Dependencies
```bash
# Local runner
gitlab-runner register
```

## Examples
```yaml
# Job with caching and rules
test:
  stage: test
  image: node:20
  cache:
    key: npm
    paths: [node_modules/]
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
  script:
    - npm ci
    - npm test
```
```yaml
# Reusable template via include
include:
  - template: Security/SAST.gitlab-ci.yml
  - local: /ci/deploy.gitlab-ci.yml

deploy:
  stage: deploy
  image: docker:24
  services: [docker:24-dind]
  only:
    - main
  script:
    - docker build -t $CI_REGISTRY_IMAGE .
    - docker push $CI_REGISTRY_IMAGE
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
