---
name: design-spec-md
description: "Write precise Markdown design specs: requirements, tokens, states, a11y, responsive. Use to make agents understand design exactly."
category: design
tags: [design, spec, markdown, ui-ux, tokens, a11y, responsive, frontend]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-10-24
updated: 2026-10-24
author: ssrjkk
---
# Design Spec in Markdown

> Precise Markdown specs that make agents understand design exactly.

## Quick Start
```markdown
# Feature: Checkout form
## Goal
Let users pay in under 60 seconds with zero confusion.

## Audience
Mobile-first shoppers, low patience, possible screen readers.

## Tokens
- colors: bg/surface/foreground/primary/border/ring
- spacing: 4/8/16/24 scale only
- radii: sm 6px, md 12px, lg 20px

## Out of scope
- No new brand colors, no custom fonts.
```

```bash
# validate the spec before building
python scripts/check_spec.py docs/specs/checkout.md
```

## When to Use
- Any UI task given to an AI agent
- Landing pages, dashboards, forms, mobile screens
- Retheme or redesign of existing apps
- Handoff between human and agent
- Design reviews and pre-delivery checks

## Best Practices

### Goal
- One sentence, one measurable outcome
- State the user job, not the component list
- Add a time or quality bar when possible
- No marketing fluff in the goal

### Audience
- Device, context, constraints (one-handed, sunlight, keyboard-only)
- Accessibility needs up front
- What the user already knows (skip re-explaining)
- Edge users: zoom 200%, slow network, old phones

### Tokens
- Reuse existing semantic tokens, never hard-code hex
- Map roles: background, surface, foreground, primary, border, ring
- Typography: font, sizes, line-height, weights
- Spacing and radii from the scale, no magic numbers

### Components and States
- List components with props and variants
- Every interactive element needs default/hover/focus/disabled/error/empty/loading
- Focus visible for keyboard, 44px+ touch targets
- Reduced motion respected, no bounce easing

### Responsive and A11y
- Breakpoints 375/768/1024/1440 with behavior per breakpoint
- Contrast 4.5:1 minimum for text
- Meaning never by color alone
- Chips and badges reflow, long tokens wrap safely

## Dependencies
```bash
# no runtime required, spec is plain Markdown
# optional local checks
python3 --version
```

## Examples
```markdown
# Spec: SaaS pricing section
## Goal
Visitors compare 3 plans and click CTA without scrolling confusion.

## Tokens
- primary: indigo-600, hover indigo-700
- surface: white, border slate-200
- font: Inter/ system fallback, h2 32/40 bold

## Components
- PricingCard x3: title, price, features[5 max], CTA
- States: default, highlighted (middle), focus-visible ring

## A11y
- h2 hierarchy, list semantics for features
- CTA contrast 5.1:1, keyboard reachable
```

```markdown
# Spec: Ops dashboard table
## Goal
Operators scan 500 rows and spot failures in seconds.

## Tokens
- danger: red-600 with icon + text (never color alone)
- density: comfortable/compact toggle
- font: tabular numbers for metrics

## States
- loading skeleton, empty with action, error with retry
- row hover subtle, selected with checkbox + aria-selected
```

```markdown
# Spec: Mobile onboarding (3 steps)
## Goal
80% completion, under 90 seconds.

## Constraints
- One primary action per screen
- Back + skip always visible
- No keyboard traps, safe-area respected

## Validation
- Test on 360px wide, 200% text scaling
- Screen reader order matches visual order
```

```markdown
## Anti-patterns to forbid in the spec
- "Make it beautiful" without tokens or constraints
- Emojis as icons (use SVG: Lucide/Heroicons)
- Cards nested in cards, gray text on colored bg
- Pure black (#000) or pure gray fills
```

## Step-by-Step
1. Write Goal in one measurable sentence.
2. Describe Audience, devices, and constraints.
3. Lock Tokens: colors, typography, spacing, radii.
4. List Components with all interaction states.
5. Define Responsive behavior per breakpoint.
6. Add A11y requirements: contrast, focus, semantics.
7. Declare Out of scope explicitly.
8. Run the Validation checklist before building.

## Validation
1. Goal is measurable and single-sentence
2. Tokens cover all colors and fonts used, no hard-coded hex
3. Every button and input has hover, focus, disabled, error states
4. Contrast 4.5:1 minimum, focus visible, touch targets 44px+
5. Layout works at 375/768/102vpx without clipping

## Troubleshooting
- Agent ignores spec: shorten to one page, move details to appendix.
- Vague output: replace adjectives with tokens and numbers.
- Clipped chips: require wrap or +n disclosure in the spec.
- Color-only meaning: add icon + text rule to A11y section.
- Scope creep: enforce Out of scope, new asks go to v2.
