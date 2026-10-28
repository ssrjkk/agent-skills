---
name: landing-page-pro
description: "Design high-converting landing pages end to end: batched intake, page structure, layout choice, conversion copywriting, SEO/AEO, plus a strict visual token system for type, spacing, radius, motion and states. Use for any marketing page, hero, or product section."
category: design
tags: [landing-page, conversion, copywriting, typography, tailwind, frontend, design, ux]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-10-28
updated: 2026-10-28
author: ssrjkk
---
# Landing Page Pro

> Strategy first, tokens second, checklist last. One offer, one audience, one action.

## Quick Start
```markdown
# Intake (one batch, no drip questions)
- Action: trial signup. Offer: 14-day team trial, no card.
- ICP: backend teams drowning in flaky E2E. Objections: price, migration cost.
- Proof: 3 logos, 2 testimonials, 99.98% uptime stat.
- Traffic: search. Voice: professional. Mobile: yes.
```

```bash
# scaffold, then build section by section (never rewrite whole page per iteration)
mkdir -p landing/{sections,assets}
```

## When to Use
- New marketing or landing pages from scratch
- Heroes, pricing sections, FAQ blocks, final CTAs
- Conversion copy reviews and redesign audits
- Any UI where every visual value must resolve through tokens, not taste

## Best Practices

### Strategy before visuals
- Decide the page argument (Part A below) before any color, font, or animation.
- One primary CTA. Never place competing CTAs above the fold.
- Match message to traffic source: mirror the ad headline in the hero.
- Benefits first, features second. Specific numbers beat vague verbs.

### Intake in one batch
- Ask only for what is missing, all questions in a single message.
- If the user cannot answer, state one assumption per gap and continue. Never stall.
- Required: action, offer, ICP, top-3 objections, traffic source, proof assets, voice.

### Layout choice
- Pick exactly one layout and state why:
  - Classic hero plus sections: product is graspable from a screenshot.
  - Long form story: education needed, skepticism high.
  - Minimal conversion page: high-intent traffic or short offer.
  - Comparison page: search intent includes alternatives.
- Build order: hero, benefits, how it works, proof, FAQ, final CTA.

### Copywriting
- Headline formulas: "{Outcome} without {pain}", "The {category} for {audience}".
- CTA is verb plus payoff. Never "Learn more" or "Submit".
- Benefit bullets: bold benefit, then proof. Ban filler: revolutionize, supercharge,
  cutting edge, effortless, world class. Say what the product does plainly.
- Sentence case for headings and buttons.

### Visual tokens
- One typeface per site. Cap weight at bold, never italic in UI.
- Snap every font size to the framework scale. Snap down, never up.
- Spacing only from the token table. Buttons: 8px vertical, 12px horizontal.
- Nested radius: inner = outer minus gap, only when gap is under 32px and result above 2.
- Borders go all around a card or not at all. Flat backgrounds, no gradients
  except a text-only hero gradient.
- Motion on one base curve, 500ms for layout, 300ms for hover. Animate only
  transform and opacity. Respect prefers-reduced-motion.
- Icons from one set (for example Phosphor or Lucide). Never emojis as icons.

### Bilingual pages
- Typeface must support Cyrillic (Manrope and Poppins do, Geist does not).
- Translate meaning, not words. Keep numbers, brands, and code strings identical.
- Russian headings keep sentence case. Test line breaks in both languages.

## Dependencies
```bash
# no runtime required; a landing is plain HTML/CSS/JS
python3 --version  # optional, for local checks only
```

## Examples
```markdown
# Page outline (classic hero plus sections, type A)
1. Hero: headline, sub, CTA, proof strip, product mock
2. Benefits x4, outcome driven
3. How it works, 3 steps
4. Tagline reveal, 2+ lines, words light up on scroll
5. Metrics strip beside the claims it supports
6. FAQ x6, objections as a section
7. Final CTA, identical to the top
```

```markdown
# Hero copy (benefit first, specific)
Headline: "Cut weekly reporting from 4 hours to 15 minutes"
Subheadline: "Acme Reports pulls your data into one dashboard your team reads."
CTA: "Start free trial" / Proof: "4.9/5 from 2,300 teams"
```

```html
<!-- Nested radius: outer 16px, 8px padding, inner 8px -->
<div class="rounded-2xl border border-white/10 bg-[#181818] p-2">
  <div class="rounded-lg bg-black p-6">...</div>
</div>
```

```css
/* Motion: one base curve, transform and opacity only */
.reveal { opacity: 0; transform: translateY(32px); }
.reveal.in {
  opacity: 1; transform: none;
  transition: opacity 700ms cubic-bezier(0.22,1,0.36,1),
              transform 700ms cubic-bezier(0.22,1,0.36,1);
}
@media (prefers-reduced-motion: reduce) {
  .reveal { opacity: 1; transform: none; transition: opacity 200ms; }
}
```

## Step-by-Step
1. Run batched intake. State assumptions, do not stall.
2. Write the page outline and hero copy before any code.
3. Choose one layout type and record why.
4. Draft conversion copy: headline, sub, CTA, benefits, FAQ.
5. Lock tokens: typeface, scale steps, spacing table, radii, motion curve.
6. Build section by section in build order. Review diffs per section.
7. Add states to every interactive element: hover, active, focus, loading, empty, error.
8. Run the Validation checklist, fix, then ship.

## Validation
1. One offer, one audience, one primary action; no competing CTAs above the fold
2. Every font size on a scale step; every spacing value from the token table
3. Every interactive element has hover, active, focus, loading, empty, error states
4. Contrast 4.5:1 minimum, focus visible, no dead links, skip link present
5. Title, meta description, og tags, favicon, alt texts, semantic landmarks

## Troubleshooting
- Generic look: enforce the token tables strictly, ban ad-hoc values.
- Weak copy: replace adjectives with numbers and proofs beside claims.
- Cluttered hero: one CTA, one proof signal, cap heading width near 680px.
- Scroll jank: IntersectionObserver once per section, never raw scroll listeners.
- Scope creep: new asks go to v2, never into the current build pass.

## Credits
Process structure (batched intake, token tables, tagline reveal, ship checklist)
adapted from `landing-page-design` by elayadesign
(https://github.com/elayadesign/ai-design-skills), MIT licensed, rewritten
for the universal Agent Skills format with bilingual and validation additions.
