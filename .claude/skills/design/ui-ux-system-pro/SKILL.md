---
name: ui-ux-system-pro
description: "Designs token-driven UI/UX systems with fluid typographic scales, 8px spatial grids, WCAG AA/AAA perceptual contrast, and complete interactive component states. Use for building cohesive design systems, dashboards, and web applications."
category: design
tags: [design-system, ui, ux, typography, accessibility, tokens, css, frontend]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-10-28
updated: 2026-10-28
author: ssrjkk
---
# UI/UX Design System Pro

> Mathematical type scales, strict 8px spacing tokens, WCAG AA/AAA contrast, and complete state matrices for every UI component.

## Quick Start
```css
:root {
  --space-1: 0.25rem; --space-2: 0.5rem; --space-3: 0.75rem; --space-4: 1rem;
  --space-6: 1.5rem;  --space-8: 2rem;   --space-12: 3rem;  --space-16: 4rem;
  --radius-sm: 6px;   --radius-md: 10px; --radius-lg: 16px;
  --text-xs: 0.75rem; --text-sm: 0.875rem; --text-base: 1rem; --text-lg: 1.125rem;
  --text-xl: 1.25rem; --text-2xl: 1.5rem;  --text-3xl: clamp(1.875rem, 3vw, 2.5rem);
}
```

```python
# Verify WCAG 2.1 relative luminance and contrast ratio (>= 4.5 for normal text, >= 3.0 for large text)
def wcag_contrast(hex_fg: str, hex_bg: str) -> float:
    def lum(h: str) -> float:
        h = h.lstrip("#")
        rgb = [int(h[i:i+2], 16) / 255.0 for i in (0, 2, 4)]
        c = [v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4 for v in rgb]
        return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
    l1, l2 = sorted([lum(hex_fg), lum(hex_bg)], reverse=True)
    return round((l1 + 0.05) / (l2 + 0.05), 2)

assert wcag_contrast("#141619", "#F4F5F7") >= 12.0
```

## When to Use
- Creating a semantic CSS custom-property token architecture for a new web app, SaaS dashboard, or documentation portal
- Fixing inconsistent spacing, arbitrary font sizes, and unreadable low-contrast text across dark and light themes
- Defining complete interactive states (default, hover, focus-visible, active, disabled, loading, empty, error) for UI components
- Auditing layouts for keyboard accessibility, touch-target sizing (>= 44x44px), and responsive breakpoint behavior

## Best Practices
- Separate primitive tokens (raw hex colors, pixel steps) from semantic tokens (--bg-canvas, --bg-surface, --text-primary, --border-subtle).
- Restrict all padding, margin, and gap values to the 4px/8px spatial scale (4, 8, 12, 16, 24, 32, 48, 64px).
- Enforce WCAG AA contrast minimums: >= 4.5:1 for body copy, >= 3.0:1 for large headings and interactive borders.
- Cap line length for reading comfort at 60-75 characters (max-width: 65ch) and pair tight heading line-height (1.15) with relaxed body line-height (1.6).
- Compute nested border-radius mathematically: R_inner = max(2px, R_outer - padding) so concentric corners never look pinched.
- Always provide visible :focus-visible outlines (2px solid var(--accent) with 2px offset) for keyboard navigation.

## Dependencies
```bash
# Verify contrast ratios and CSS token consistency with Python
python3 --version
```

## Examples
```css
/* Semantic dark and light theme surface hierarchy */
:root, [data-theme="dark"] {
  --bg-canvas: #0b0f0a;
  --bg-surface: #11170f;
  --bg-elevated: #172114;
  --text-primary: #e6ffe2;
  --text-muted: #88a883;
  --accent: #7dff4a;
  --border: rgba(125, 255, 74, 0.16);
}
[data-theme="light"] {
  --bg-canvas: #f4f6f1;
  --bg-surface: #ffffff;
  --bg-elevated: #eef2ea;
  --text-primary: #14321f;
  --text-muted: #4a6a52;
  --accent: #1a7f37;
  --border: rgba(20, 80, 40, 0.16);
}
```

```css
/* Accessible interactive button with complete state matrix */
.btn {
  display: inline-flex; align-items: center; justify-content: center; gap: var(--space-2);
  min-height: 40px; padding: var(--space-2) var(--space-4);
  font-weight: 600; font-size: var(--text-sm); border-radius: var(--radius-sm);
  transition: transform 150ms ease, background-color 150ms ease, border-color 150ms ease;
}
.btn:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
.btn:active:not(:disabled) { transform: translateY(1px); }
.btn:disabled { opacity: 0.45; cursor: not-allowed; }
```

## Step-by-Step
1. Define semantic surface, text, border, and accent tokens for both dark and light themes in :root.
2. Establish a modular typographic scale (xs through 3xl) with fluid clamp() sizing on hero and section headings.
3. Lock spacing tokens to the 4px/8px grid and replace all arbitrary pixel margins/paddings across stylesheets.
4. Run wcag_contrast() across every foreground/background token pair to verify >= 4.5:1 body contrast.
5. Implement all 8 component states (default, hover, focus-visible, active, disabled, loading, empty, error) for buttons, inputs, and cards.
6. Verify responsive layout behavior at 320px, 768px, 1024px, and 1440px with prefers-reduced-motion support.

## Validation
1. All text/background token pairs pass WCAG AA contrast (>= 4.5:1 for normal text, >= 3.0:1 for large headings)
2. Zero hard-coded hex colors or off-grid spacing values exist in component CSS rules
3. Keyboard Tab navigation highlights every interactive control with a clear :focus-visible ring
4. All interactive controls meet minimum 40x40px / 44x44px touch target dimensions on mobile viewports

## Troubleshooting
- Dark theme cards blend into the background — increase elevation using a subtle 1px border (rgba(255,255,255,0.08)) and a lighter surface token.
- Light theme accent green looks washed out on white — switch from neon lime (#7dff4a) to deep forest green (#1a7f37) in [data-theme="light"].
- Nested card corners look uneven — set inner border-radius to outer radius minus container padding.
- Cyrillic headings look cramped compared to English — add 0.01em letter-spacing and use a Cyrillic-native font (Inter, Manrope, JetBrains Mono).
