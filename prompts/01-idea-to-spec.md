# Idea → One-page Spec

Turn the idea below into a **one-page spec** a single engineer can start tomorrow.

## When to use
- Stage 1 of any conveyor, before writing a single line of code
- Any time the scope of an ongoing project quietly grows

## Prompt
```text
You are a product engineer. Convert the idea below into a one-page spec.
Rules:
- Cut scope aggressively: exactly ONE runnable vertical slice.
- No feature without a measurable success metric. Unmeasurable wishes go to Non-goals.
- The slice must have a Definition of Done checkable in one working day.
- Output exactly these sections, nothing else:
  1. Problem (2 sentences, who hurts and why)
  2. Target user (one persona)
  3. Success metric (one number with a deadline)
  4. The one slice (steps a user takes, first to last)
  5. Non-goals (at least 3 explicit rejections)
  6. Definition of done (checkbox list)

Idea: <PASTE YOUR IDEA>
```

## Gate this satisfies
Stage 1 · gates 1-4: spec exists, scope cut to one slice, non-goals written, DoD checkable.
