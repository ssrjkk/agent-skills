# GitOps Delivery + Canary + SLO

Turn "hosted" into "operated": declarative delivery, progressive rollout, an SLO with an error budget, and a 3 AM runbook.

## When to use
- Stage 5 of any conveyor, when the MVP is stable under load

## Prompt
```text
You are a platform engineer. Make this MVP operable:
1. GitOps: repo structure (ApplicationSet) driving the cluster; cluster state == repo state
2. Canary: progressive rollout with automatic rollback on error-metric regression; include a rollback drill
3. SLO: one user-facing SLI, target, error budget, and the burn-rate alert
4. Runbook: a 3 AM checklist (symptom -> diagnosis command -> action -> verification), tested once
Output: repo tree, rollout manifest, SLO definition, runbook.
Stack: <PASTE THE STACK AND CLUSTER>
```

## Gate this satisfies
Stage 5 · gates 1-4: GitOps state, canary drill, SLO + budget, tested runbook.
