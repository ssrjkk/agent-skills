---
name: code-review
description: "Conduct effective code reviews: correctness, security, performance, style, and actionable feedback. Use for reviewing any pull request or diff."
category: engineering
tags: [code-review, quality, pull-request, best-practices, review, engineering]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-09-20
updated: 2026-09-28
author: ssrjkk
---
# Code Review

> Conducting thorough, actionable code reviews.

## Quick Start
```bash
# Review a diff systematically
git diff main...HEAD
# check correctness, security, performance, and readability
```

## When to Use
- Every pull request before merge
- Security-sensitive changes (auth, payments, data)
- Refactors and large diffs
- Onboarding and knowledge sharing

## Best Practices

### Prioritize
- Review correctness and security first, style last
- Separate blocking issues from nits
- Focus on the diff, not the whole codebase
- Read tests: do they cover the change?

### Feedback Quality
- Ask questions instead of demanding changes
- Explain the "why" behind each suggestion
- Suggest concrete fixes with examples
- Acknowledge what is done well

### Security & Performance
- Look for injection, secrets, and unsafe deserialization
- Check authz on every endpoint
- Flag N+1 queries and O(n^2) patterns
- Watch for unbounded inputs and resource leaks

### Scope
- Review the intent: does it solve the stated problem?
- Check for dead code, leftovers, and debug output
- Verify tests, docs, and migrations are included
- Respect scope: propose follow-ups for large refactors

## Dependencies
```bash
# Tools that help: ruff, mypy, eslint, golangci-lint
# Static security scanning: bandit, semgrep, gitleaks
```

## Examples
```python
# Risk: user-supplied value in SQL query
query = f"SELECT * FROM users WHERE id = {request.user_id}"  # SQL injection
# Fix: parameterize
cursor.execute("SELECT * FROM users WHERE id = %s", (request.user_id,))
```
```python
# Risk: N+1 queries in a loop
for order in user.orders:           # 1 query per order
    items += order.items.all()
# Fix: eager load
from django.db.models import Prefetch
user.orders.prefetch_related(Prefetch("items"))
```
```python
# Risk: missing authorization check
@app.route("/admin/users/<uid>")
def delete_user(uid):
    User.objects.get(id=uid).delete()   # no authz check
# Fix: verify the caller is an admin first
```
```python
# Risk: secrets in code
API_KEY = "sk-live-abc123..."   # leaked secret
# Fix: use environment variables / secret manager
```

## Step-by-Step
1. Read the PR description and understand the intent.
2. Scan the diff for obvious correctness and security issues.
3. Read tests; check they assert real behavior.
4. Review each file in order of risk (backend, auth, data).
5. Run static analysis if not already in CI.
6. Write feedback: blocking issues, questions, nits.
7. Approve only when blockers are resolved.
8. Follow up on deferred suggestions as issues.

## Validation
1. No injection, broken authz, or leaked secrets
2. Tests cover the new behavior including edge cases
3. No N+1 queries or obvious performance regressions
4. Code matches project style and conventions
5. Every blocking comment addressed or justified

## Troubleshooting
- Large PR: request splitting or review by commits.
- Missing tests: ask for tests on the changed paths.
- Style bikeshedding: defer to the project linter/config.