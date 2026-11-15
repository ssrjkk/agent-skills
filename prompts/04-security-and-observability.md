# Hardening: Security + Observability + Backups

Assume the MVP is now worth attacking and worth losing. Produce the hardening plan.

## When to use
- Stage 4 of any conveyor, right after the MVP is public

## Prompt
```text
You are an SRE/security engineer. Harden this MVP:
1. OWASP top-10 checklist against the actual stack; top 5 risks with fixes
2. Input validation and auth hardening (rate limits, session policy)
3. Observability: exactly 4 golden metrics, structured logs, one alert per error class
4. Backups: schedule + a restore drill plan that starts from zero
5. A load test against the SLO target (name the tool and the target)
Output: checklist ordered by risk, each item < 1h of work.
MVP stack: <PASTE THE STACK>
```

## Gate this satisfies
Stage 4 · gates 1-4: OWASP reviewed, metrics/logs/alerts, restore drill, load test vs SLO.
