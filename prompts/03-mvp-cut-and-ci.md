# MVP Scope + CI Pipeline

Upgrade the prototype into a **deployed MVP**: real data model, auth, CI gates, public URL.

## When to use
- Stage 3 of any conveyor, when the prototype decision was "continue"
- Any project that runs manually but should run in CI

## Prompt
```text
You are a senior engineer. Upgrade this prototype into an MVP with these gates:
1. Real data model with migrations (no hand-edited databases)
2. Auth: working session or token flow; secrets in a manager, never in code
3. CI pipeline on every push: lint -> tests -> build -> deploy; red blocks merge
4. A public HTTPS URL serving the MVP, plus a documented ROLLBACK command
Keep the prototype's scope. Add NOTHING that is not in the spec.
Output: a numbered task list (each task < 2h), the CI file, and the deploy config.
Prototype: <PASTE THE REPO TREE>
```

## Gate this satisfies
Stage 3 · gates 1-4: CI blocks red, migrations, auth + managed secrets, public URL.
