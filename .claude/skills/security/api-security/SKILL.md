---
name: api-security
description: "Secure web APIs: authentication, authorization, rate limiting, input validation, and abuse protection. Use for hardening any API."
category: security
tags: [api-security, authentication, authorization, rate-limiting, validation]
models: [sonnet, opus, gpt-5, gemini-2.5, glm-4.6]
version: 1.0.0
created: 2026-09-29
updated: 2026-09-29
author: ssrjkk
---
# API Security

> Hardening APIs against common threats.

## Quick Start
```text
1. Authenticate every request
2. Authorize every action
3. Validate all input
4. Rate-limit abuse
```

## When to Use
- Public and internal APIs
- Auth, payments, and data endpoints
- Any API exposed to untrusted clients
- Security reviews before release

## Best Practices

### Authentication
- Use a proven auth scheme (OAuth2, API keys, JWT)
- Never roll your own crypto
- Store tokens hashed, with expiry
- Support key rotation

### Authorization
- Check permissions on every endpoint
- Use least privilege scopes
- Never trust the client's claims alone
- Enforce ownership checks

### Input Validation
- Validate types, lengths, and ranges
- Parameterize all queries
- Reject unexpected fields
- Limit payload sizes

### Abuse Protection
- Rate limit per user/IP/key
- Set per-endpoint quotas
- Detect and block anomalies
- Return consistent error responses

## Dependencies
```bash
# language-agnostic; use the framework's security middleware
```

## Examples
```python
# Rate limiting (pseudo)
def rate_limit(key: str, limit: int, window: int) -> bool:
    count = redis.incr(f"rl:{key}")
    if count == 1:
        redis.expire(f"rl:{key}", window)
    return count <= limit

@app.route("/api/login", methods=["POST"])
def login():
    if not rate_limit(request.remote_addr, limit=10, window=60):
        return jsonify({"error": "rate_limited"}), 429
    ...
```
```python
# Input validation
from pydantic import BaseModel, EmailStr

class SignupRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

    @field_validator("password")
    def _strong(cls, v):
        if not re.search(r"[A-Za-z]", v) or not re.search(r"\d", v):
            raise ValueError("password needs letters and digits")
        return v
```
```python
# Ownership check
def get_order(user_id: int, order_id: int):
    order = db.get_order(order_id)
    if order is None or order.user_id != user_id:
        raise NotFound("order")  # no info leak
    return order
```
```python
# Consistent errors
def error(code: str, status: int):
    return jsonify({"error": {"code": code, "status": status}}), status
```

## Step-by-Step
1. Authenticate all endpoints (except public health).
2. Enforce authorization per resource and action.
3. Validate every input with schemas.
4. Parameterize queries; reject extra fields.
5. Rate-limit per user/IP and endpoint.
6. Set payload and response limits.
7. Return consistent, minimal error responses.
8. Run a security review before release.

## Validation
1. Unauthenticated requests are rejected
2. Unauthorized actions are denied
3. Invalid input returns 400/422
4. Rate limits trigger under abuse
5. Errors don't leak internals

## Troubleshooting
- Auth bypass: verify checks run on every endpoint.
- Enumeration: return generic errors for not-found vs forbidden.
- Abuse: tune rate limits and add anomaly detection.