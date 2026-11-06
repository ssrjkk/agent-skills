---
name: design-taste-direction
description: "Applies intentional art direction, anti-template visual concepts, curated typographic pairings, and domain-specific color palettes to web interfaces. Use when moving beyond generic AI-generated layouts into distinctive brand experiences."
category: design
tags: [art-direction, design, typography, color-palette, branding, ui, frontend]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-10-28
updated: 2026-10-28
author: ssrjkk
---
# Intentional Art Direction & Design Taste

> Replacing generic purple-gradient AI templates with domain-grounded palettes, purposeful typography, and focal-point composition.

## Quick Start
```markdown
# Art Direction Brief (Lock Before Writing CSS)
- Aesthetic Archetype: Precision Terminal / Swiss Editorial / Warm Craft
- Palette (max 3 hues): Canvas #0B0F0A, Surface #11170F, Primary Accent #7DFF4A, Secondary #00FFD1
- Type Pairing: Display/UI 'Inter' (600/700) + Technical/Data 'JetBrains Mono' (400/500)
- Signature Detail: 1px phosphor border glow + live terminal command preview
```

```python
# Check that a palette defines no more than 3 distinct chromatic accent hues
def validate_palette_restraint(hex_accents: list[str], max_accents: int = 3) -> bool:
    unique = {h.lower().strip() for h in hex_accents}
    return 1 <= len(unique) <= max_accents

assert validate_palette_restraint(["#7dff4a", "#00ffd1"])
```

## When to Use
- An AI-generated website looks like a generic SaaS template (default Indigo/Purple gradients, 3 identical icon cards, stock filler)
- Defining a cohesive visual language for developer tools, fintech dashboards, e-commerce storefronts, or editorial publications
- Selecting expressive, Cyrillic-compatible font pairings and semantic color hierarchies
- Designing a distinctive hero focal point (interactive terminal, live code diff, studio product stage, or data visual)

## Best Practices
- Ban default Indigo/Violet (#6366f1 / #8b5cf6) rainbow gradients unless explicitly required by an existing brand guide.
- Follow the 60-30-10 color rule: 60% neutral canvas, 30% elevated surface/cards, and 10% high-contrast semantic accent.
- Choose one of three clear archetypes per project: Technical Monospace/Terminal, Swiss High-Contrast Editorial, or Crisp Commercial Light.
- Give the hero section a concrete product artifact (interactive CLI, real data preview, or 1:1 studio render) instead of abstract floating blobs.
- Use weight, size, and muted foreground tokens to create hierarchy before reaching for extra background colors or borders.
- Verify that every chosen typeface renders Cyrillic and Latin glyphs with matching x-height and stroke weight.

## Dependencies
```bash
# Google Fonts preconnect for zero-FOUT Cyrillic + Latin typography
# Inter + JetBrains Mono or Manrope + IBM Plex Mono
python3 --version
```

## Examples
```css
/* Archetype 1: Precision Developer Terminal (Dark Phosphor) */
.theme-terminal {
  --canvas: #0b0f0a;
  --surface: #11170f;
  --ink: #d6ffd0;
  --muted: #6f8f6a;
  --accent: #7dff4a;
  --font-sans: 'Inter', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
}
```

```css
/* Archetype 2: Crisp Commercial Storefront (Light Zero-CLS) */
.theme-storefront {
  --canvas: #f4f5f7;
  --surface: #ffffff;
  --ink: #141619;
  --muted: #5a6270;
  --accent: #0e9f6e;
  --font-sans: 'Manrope', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
}
```

## Step-by-Step
1. Write a 4-line Art Direction Brief (Archetype, 60-30-10 Palette, Type Pairing, and Hero Focal Artifact) before coding.
2. Select at most 2 typefaces (one UI/display sans-serif and one technical monospace) with full Cyrillic glyph coverage.
3. Define the 60-30-10 color tokens and verify contrast with wcag_contrast().
4. Design the hero around a functional interactive preview (live search, terminal, or product configurator).
5. Introduce visual rhythm across sections by alternating dense structured grids with high-contrast focal callouts.
6. Strip decorative noise (random floating emojis, mismatched icon styles, and competing gradients).

## Validation
1. Palette uses <= 3 chromatic hues and adheres to the 60-30-10 surface distribution
2. Hero section features a concrete interactive or technical focal artifact rather than generic stock filler
3. All icons come from a single stroke-weight family (no emoji icons in navigation or feature cards)
4. Both English and Russian views maintain identical visual hierarchy and typographic balance

## Troubleshooting
- Page still feels generic — replace 3-column generic benefit icons with concrete code snippets, metrics, or product previews.
- Too many competing colors — collapse status and domain badges to subtle 10% alpha backgrounds with 1px tinted borders.
- Display font breaks on Russian text — switch to Manrope, Inter, or Golos Text which have native Cyrillic kerning tables.
- Dark background looks muddy — tint dark surfaces subtly toward the primary hue (#0b0f0a for green, #0b0d14 for blue) instead of pure #000000.
