---
name: owasp-web-security
description: "Harden web applications against the OWASP Top 10: injection, XSS, auth flaws, CSRF, SSRF, and insecure dependencies. Use for any web app security review."
category: security
tags: [owasp, security, web, injection, xss, csrf, ssrf, pentest]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-09-20
updated: 2026-09-28
author: ssrjkk
---
# OWASP Web Security

> Hardening web applications against the OWASP Top 10.

## Quick Start
```bash
# Scan dependencies for known vulnerabilities
pip-audit --format full
npm audit
# then review the OWASP Top 10 checklist against your app
```

## When to Use
- Before launching or major releases
- When handling auth, payments, or PII
- After dependency or framework upgrades
- Regular security hardening of existing apps

## Best Practices

### Injection
- Parameterize all SQL/query construction
- Escape output for the context (HTML, JS, URL)
- Validate and whitelist inputs server-side
- Use ORM/query builders; never string-concatenate queries

### Authentication & Authorization
- Use a proven auth library (not homegrown)
- Hash passwords with bcrypt/argon2
- Enforce MFA for sensitive actions
- Check authorization on every endpoint, not just the UI

### XSS & CSRF
- Auto-escape template output; sanitize rich content
- Set CSP headers; use strict `Trusted Types` where possible
- CSRF tokens on all state-changing requests
- Set `SameSite=Lax/Strict` on cookies

### Data & Dependencies
- Encrypt data in transit (TLS) and at rest
- Keep dependencies updated; scan regularly
- Restrict SSRF: block private ranges, pin redirects
- Limit file uploads: type, size, and execution

## Dependencies
```bash
pip install bandit pip-audit
npm install -g npm-audit-resolver
# scanners: semgrep, gitleaks, trivy
```

## Examples
```python
# SQL injection safe pattern
cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
```
```python
# Escape output in templates (Django auto-escapes)
# context = {"user_input": user_input}
# Template: {{ user_input }}   # auto-escaped
```
```python
# CSRF protection (Django middleware default)
from django.views.decorators.csrf import csrf_exempt
# never use @csrf_exempt on state-changing views
```
```python
# SSRF guard
import ipaddress, socket

def safe_fetch(url: str) -> str:
    host = urlparse(url).hostname
    ip = ipaddress.ip_address(socket.gethostbyname(host))
    if not ip.is_private:          # block local/private ranges
        return requests.get(url).text
    raise ValueError("Blocked private address")
```

## Step-by-Step
1. Run dependency scanners (pip-audit/npm audit/trivy).
2. Review authN/authZ: password storage, sessions, roles.
3. Check all inputs: validation, escaping, parameterization.
4. Audit CSRF, XSS, and CSP headers.
5. Review file uploads, SSRF vectors, and redirect handling.
6. Check secrets: gitleaks scan and env-based config.
7. Harden headers: CSP, HSTS, X-Content-Type-Options.
8. Re-scan after fixes; document residual risks.

## Validation
1. No injection points found in code scan
2. Passwords stored with a strong hash
3. Authorization enforced server-side on all endpoints
4. CSP and security headers present
5. Dependency scan reports no critical vulnerabilities

## Troubleshooting
- Broken auth flows: test with the same browser/network rules users hit.
- False positives: verify scanners' claims in a safe environment.
- Legacy code risk: prioritize by exposed attack surface.