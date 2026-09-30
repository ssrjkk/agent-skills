---
name: secrets-management
description: "Manage secrets safely: vaults, rotation, environment variables, scanning, and least privilege. Use for protecting credentials and keys."
category: security
tags: [secrets, vault, env-vars, rotation, scanning, credentials]
models: [sonnet, opus, gpt-5, gemini-2.5, glm-4.6]
version: 1.0.0
created: 2026-09-29
updated: 2026-09-29
author: ssrjkk
---
# Secrets Management

> Storing and rotating secrets safely.

## Quick Start
```bash
# Never commit secrets to git
# Use a vault or environment variables
export API_KEY="..."
```

## When to Use
- Any app with credentials or keys
- CI/CD that needs secrets
- Multi-service environments
- Compliance (PCI, HIPAA)

## Best Practices

### Storage
- Use a vault (HashiCorp Vault, cloud KMS)
- Prefer managed secret managers in the cloud
- Keep secrets out of config files and images
- Use environment variables at minimum

### Rotation
- Rotate secrets on a schedule or on incident
- Automate rotation where possible
- Support zero-downtime rotation
- Revoke compromised secrets immediately

### Scanning
- Scan repos and images for leaked secrets
- Block secrets in git pre-commit (gitleaks)
- Monitor for exposure alerts
- Rotate anything found in scans

### Least Privilege
- Grant minimal access per service
- Scope keys to resources
- Use short-lived credentials
- Audit access to secrets

## Dependencies
```bash
# gitleaks for git scanning
go install github.com/gitleaks/gitleaks@latest
# or: pip install detect-secrets
```

## Examples
```bash
# Run gitleaks to scan for secrets
gitleaks detect --source . -v
```
```python
# Load secrets from env (never hardcode)
import os

API_KEY = os.environ.get("API_KEY")
if not API_KEY:
    raise RuntimeError("API_KEY not set")
```
```yaml
# GitHub Actions secrets usage
name: Deploy
on: [push]
jobs:
  deploy:
    steps:
      - run: ./deploy.sh
        env:
          API_KEY: ${{ secrets.API_KEY }}
```
```bash
# Vault-based fetch (pseudo)
vault read secret/api_key
# or cloud: gcloud secrets versions access latest --secret=api-key
```

## Step-by-Step
1. Audit current secrets and their storage.
2. Move secrets to a vault or env vars.
3. Remove secrets from configs and history.
4. Set up pre-commit scanning (gitleaks).
5. Rotate secrets and revoke exposed ones.
6. Grant least-privilege access per service.
7. Automate rotation where possible.
8. Monitor and audit access.

## Validation
1. No secrets in git history or repos
2. Secrets come from the vault/env only
3. Rotation works with zero downtime
4. Scanning is part of CI
5. Access is scoped and audited

## Troubleshooting
- Leaked secret: revoke and rotate immediately.
- Rotation downtime: implement overlapping keys.
- Scan false positives: use allowlists carefully.