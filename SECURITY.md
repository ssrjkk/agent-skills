# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please report it
privately before disclosure.

**Contact:** open a private vulnerability report on GitHub:
https://github.com/ssrjkk/agent-skills/security/advisories

Please include:
- The affected file/feature
- A minimal reproduction
- Expected vs actual behavior

## Scope

- The Python SDK (`src/claude_skills/`)
- Skill content and examples that execute code
- CI workflows and release tooling

## Policy

- Do not open public issues for security bugs.
- We aim to respond within 48 hours.
- Valid reports are acknowledged and fixed in a security release.

## Security considerations for skills

- Skill examples may contain code — review before running in privileged
  environments.
- Never store secrets or credentials in `SKILL.md` files.
- Report any skill that encourages insecure practices.