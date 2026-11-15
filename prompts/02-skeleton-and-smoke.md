# Skeleton + One-command Smoke Test

Generate a **throwaway prototype**: the smallest project that runs the slice locally with one command and proves it with a smoke script.

## When to use
- Stage 2 of any conveyor: the prototype loop
- Deciding whether an idea lives or dies before investing

## Prompt
```text
You are a pragmatic engineer. Create a THROWAWAY prototype (ugly code is fine) for the spec below.
Requirements:
- One command boots everything locally: `docker compose up` (or equivalent)
- One happy path works end-to-end
- A smoke script `scripts/smoke.sh` exits 0 when the slice works, 1 when it does not
- No auth, no polish, no extra features — the slice only
- A DECISION.md file: "continue / pivot / kill" plus the reason

Output: the full file tree with file contents, then the two commands to run.
Spec: <PASTE THE SPEC>
```

## Gate this satisfies
Stage 2 · gates 1-3: one-command local run, E2E smoke, recorded decision.
