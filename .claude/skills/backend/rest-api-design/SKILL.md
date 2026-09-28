---
name: rest-api-design
description: "Design consistent REST APIs: resource modeling, status codes, pagination, versioning, error contracts, and documentation. Use for any API design task."
category: backend
tags: [rest, api-design, http, resources, pagination, versioning, openapi]
models: [sonnet, opus, gpt-5, gemini-2.5, glm-4.6]
version: 1.0.0
created: 2026-09-25
updated: 2026-09-28
author: ssrjkk
---
# REST API Design

> Designing consistent, evolvable REST APIs.

## Quick Start
```text
Resources:   /users, /users/{id}, /users/{id}/orders
Methods:     GET list/detail, POST create, PUT replace, PATCH partial, DELETE
Status:      200, 201, 204, 400, 401, 403, 404, 409, 422, 429, 500
```

## When to Use
- Public or internal HTTP APIs
- Designing before implementation
- Versioning and evolving existing APIs
- SDKs and clients that consume the API

## Best Practices

### Resources
- Model nouns as resources, actions as sub-resources
- Use plural names: `/users`, not `/user`
- Nest only for genuine ownership: `/users/{id}/orders`
- Represent relations with IDs, not nested objects

### Methods & Status
- Use HTTP methods for intent (GET/POST/PUT/PATCH/DELETE)
- Return 201 with Location on create, 204 on delete
- Use 422 for validation, 409 for conflicts
- Map errors consistently: code, message, details

### Pagination & Filtering
- Paginate list endpoints: page/limit or cursor
- Use cursor-based pagination for stability
- Filter with query params, not paths
- Sort with explicit `sort` param

### Versioning & Evolution
- Version the API: URL prefix or header
- Additive changes within a version
- Deprecate with headers and clear notices
- Document everything in OpenAPI

## Dependencies
```bash
# Design/docs tooling
npm i -D @redocly/cli
# or Python
pip install openapi-spec-validator
```

## Examples
```yaml
# OpenAPI minimal user resource
openapi: 3.1.0
info:
  title: Users API
  version: v1
paths:
  /users:
    get:
      parameters:
        - name: limit
          in: query
          schema: { type: integer, maximum: 100 }
      responses:
        "200":
          description: Paginated users
    post:
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/UserInput"
      responses:
        "201":
          description: Created
```
```json
// Consistent error contract
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request body",
    "details": [{ "field": "email", "reason": "must be a valid email" }],
    "request_id": "req_abc123"
  }
}
```
```text
// Pagination response shape
GET /users?limit=25&cursor=eyJpZCI6MTAwfQ

{
  "data": [...],
  "pagination": {
    "next_cursor": "eyJpZCI6MTI1fQ",
    "has_more": true
  }
}
```
```python
# Example routing
# GET /v1/users -> list
# POST /v1/users -> create
# GET /v1/users/{id} -> detail
# PATCH /v1/users/{id} -> partial update
# DELETE /v1/users/{id} -> 204
```

## Step-by-Step
1. Identify resources and their relations from the domain.
2. Define endpoints with proper methods and paths.
3. Specify request/response schemas and status codes.
4. Add pagination, filtering, and sorting to lists.
5. Create a consistent error contract.
6. Decide versioning strategy up front.
7. Write OpenAPI spec and validate it.
8. Generate docs and SDKs from the spec.

## Validation
1. All paths follow the resource naming convention
2. Status codes match HTTP semantics
3. Error responses have a consistent shape
4. Lists are paginated with a stable cursor
5. OpenAPI spec validates and documents fully

## Troubleshooting
- Over-nested paths: flatten unless true ownership.
- Inconsistent errors: centralize the error mapping.
- Breaking changes: bump version instead of changing semantics.