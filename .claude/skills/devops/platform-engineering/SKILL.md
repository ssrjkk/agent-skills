---
name: platform-engineering
description: "Platform engineering with Backstage/Port"
category: devops
tags: [platform-engineering, backstage, port, developer-portal, internal-developer-platform]
models: [sonnet, opus]
version: 1.0.0
created: 2026-05-14
updated: 2026-09-29
---
# Platform Engineering

> Build internal developer platforms with Backstage and Port for streamlined developer workflows.

## Quick Start
```yaml
# app-config.yaml — Backstage configuration
app:
  title: Internal Developer Platform
  baseUrl: https://developer.example.com

backend:
  baseUrl: https://developer.example.com
  listen:
    port: 7007

organization:
  name: My Company

integrations:
  github:
    - host: github.com
      token: ${GITHUB_TOKEN}

techdocs:
  builder: 'local'
  generators:
    techdocs: 'docker'

catalog:
  rules:
    - allow: [Component, API, Resource, System, Domain]
  locations:
    - type: url
      target: https://github.com/org/service-catalog/blob/main/catalog-info.yaml
      rules:
        - allow: [Component, API]
```

```yaml
# catalog-info.yaml — Service entity definition
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: payment-service
  description: Payment processing service
  annotations:
    github.com/project-slug: org/payment-service
    backstage.io/techdocs-ref: dir:.
    jenkins.io/github-folder: org/payment-service
spec:
  type: service
  lifecycle: production
  owner: platform-team
  system: payment-platform
  dependsOn:
    - resource:default/postgres-main
    - api:default/payment-api
  providesApis:
    - payment-api
  consumedApis:
    - fraud-detection-api
```

## Key Concepts
Platform engineering treats the developer platform as a product. Backstage/Port provide service catalogs, software templates, tech docs, and scorecards. Golden paths reduce cognitive load on developers.

## When to Use
- Organizations with 10+ microservices needing standardized management
- Teams spending too much time on infrastructure configuration
- Standardizing deployment workflows and environments
- Improving developer experience and reducing onboarding time

## Step-by-Step
1. Bootstrap a developer portal: scaffold Backstage (`npx @backstage/create-app`) or create a Port blueprint with service metadata fields.
2. Model the golden path: define service templates for standard components (API, service, worker) using software templates / Port self-service actions.
3. Register the catalog: commit `catalog-info.yaml` for each service with owner, system, dependencies, and API boundaries.
4. Wire CI/CD: connect the SCM integration, add repository-backend events so new repos auto-register.
5. Publish docs: enable TechDocs from repo markdown with cookstyle/plugins to render living documentation.
6. Add governance: create scorecards with maturity checks (SLO covered, dependency updates, cost tags) and report in the portal.

## Examples
```yaml
# catalog-info.yaml — full entity with relations
apiVersion: backstage.io/v1alpha1
kind: System
metadata:
  name: payment-platform
  description: Core payments system
spec:
  owner: platform-team
---
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: payment-service
  annotations:
    github.com/project-slug: org/payment-service
    backstage.io/techdocs-ref: dir:.
spec:
  type: service
  lifecycle: production
  owner: platform-team
  system: payment-platform
  dependsOn:
    - resource:default/postgres-main
  providesApis: [payment-api]
  consumedApis: [fraud-detection-api]
```
```bash
# Add the entity to catalog locations, then push to trigger sync
kubectl port-forward svc/backstage-backend 7007:7007
curl http://localhost:7007/api/catalog/entities?filter=kind=component
```

## Validation
1. Backstage/Port starts and renders the service catalog
2. Software templates create repositories with correct scaffolding
3. TechDocs renders documentation from code repositories
4. Scorecards track service maturity metrics
