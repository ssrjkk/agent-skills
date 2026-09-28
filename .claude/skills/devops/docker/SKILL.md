---
name: docker
description: "Containerize applications with Docker: Dockerfiles, images, networking, volumes, compose, and production hardening. Use for any deployable service."
category: devops
tags: [docker, containers, images, dockerfile, compose, deployment, devops]
models: [sonnet, opus, gpt-5, gemini-2.5, glm-4.6]
version: 1.0.0
created: 2026-09-20
updated: 2026-09-28
author: ssrjkk
---
# Docker

> Containerizing applications with Docker for consistent deployment.

## Quick Start
```bash
docker build -t myapp .
docker run -p 8080:8080 myapp
docker compose up -d
```

## When to Use
- Consistent environments across dev, test, and prod
- Microservices and isolated dependencies
- CI/CD artifacts that are identical everywhere
- Local development with databases and services

## Best Practices

### Dockerfiles
- Use multi-stage builds to slim images
- Prefer official and pinned base images (`alpine:3.20`)
- Run as non-root; copy only what is needed
- Layer ordering: dependencies first, code last (better caching)

### Images
- Keep images small: distroless or alpine when possible
- Tag with commit SHA and semver; avoid `latest` for prod
- Scan images with `docker scout` or Trivy
- Use `--platform` for multi-arch builds

### Runtime
- Set resource limits (`--memory`, `--cpus`)
- Use volumes for persistent data; anonymous volumes are ephemeral
- Prefer `init: true` or `tini` to reap zombies
- Add healthchecks so orchestrators can manage lifecycle

## Dependencies
```bash
# Docker Desktop or docker engine + compose plugin
docker --version
docker compose version
```

## Examples
```dockerfile
# Multi-stage Node build
FROM node:22-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:22-alpine AS runtime
ENV NODE_ENV=production
WORKDIR /app
COPY --from=build /app/dist ./dist
COPY --from=build /app/node_modules ./node_modules
USER node
EXPOSE 3000
CMD ["node", "dist/server.js"]
```
```yaml
# docker-compose.yml
services:
  web:
    build: .
    ports:
      - "8080:8080"
    depends_on:
      db:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://localhost:8080/health"]
      interval: 10s
      retries: 3
  db:
    image: postgres:17-alpine
    environment:
      POSTGRES_PASSWORD: secret
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
volumes:
  pgdata:
```
```bash
# Build and push with metadata
docker build -t ghcr.io/org/myapp:${GITHUB_SHA} .
docker push ghcr.io/org/myapp:${GITHUB_SHA}
```
```bash
# Inspect and debug
docker exec -it myapp sh
docker logs --follow myapp
docker image prune -f
```

## Step-by-Step
1. Write a multi-stage Dockerfile with pinned base images.
2. Order layers for cache efficiency (deps before code).
3. Run as non-root; add a healthcheck.
4. Build and test locally with `docker build` and `docker run`.
5. Compose services for local integration (app + db + cache).
6. Tag images with the commit SHA; push to a registry.
7. Scan for vulnerabilities before deploy.
8. Pin resource limits and set up log rotation.

## Validation
1. `docker build` succeeds with no warnings
2. `docker run` starts and responds to healthcheck
3. Image scan reports no critical vulnerabilities
4. Compose stack starts cleanly with `docker compose up`
5. Non-root container cannot write to protected paths

## Troubleshooting
- "Cannot connect to the Docker daemon": start Docker Desktop/engine.
- Image too large: switch to multi-stage and slimmer base.
- "Address already in use": change host port mapping or stop the conflicting container.