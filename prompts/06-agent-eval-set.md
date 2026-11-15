# Golden Eval Set Before Any Prompting

Write the agent's golden eval set BEFORE tuning a single prompt. No eval set = no objective quality, only vibes.

## When to use
- Stage 1 of the AI conveyor, before writing the first prompt
- Every time the agent's job changes scope

## Prompt
```text
You are an AI QA engineer. Build a golden eval set for the agent below:
- >= 20 cases across 5 categories: happy paths (8), edge inputs (4),
  refusal cases (4), adversarial/injection (2), regression anchors (2+)
- Each case: input, expected behaviour (observable, not vibes), severity
- 3 cases MUST be ones the current design will fail (they define the next work)
- A runner spec: how to execute the set and compute a pass rate
Output: the eval set as a table + the runner spec.
Agent job: <ONE SENTENCE + TOOLS>
```

## Gate this satisfies
Stage 1 · gates 2-3: eval set written before prompting, refusal policy explicit.
