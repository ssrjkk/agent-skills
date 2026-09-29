---
name: modern-css
description: "Use modern CSS: layout (grid/flex), custom properties, container queries, cascade layers, and responsive design. Use for maintainable styling."
category: frontend
tags: [css, grid, flexbox, custom-properties, container-queries, responsive]
models: [sonnet, opus, gpt-5, gemini-2.5, glm-4.6]
version: 1.0.0
created: 2026-09-29
updated: 2026-09-29
author: ssrjkk
---
# Modern CSS

> Maintainable, performant styling with modern CSS.

## Quick Start
```css
:root { --accent: #8b5cf6; }
.card { padding: 1rem; border: 1px solid color-mix(in srgb, var(--accent), white 40%); }
```

## When to Use
- Any styling without heavy frameworks
- Responsive and maintainable layouts
- Design systems with tokens
- Component libraries

## Best Practices

### Layout
- Use Grid for page/component layout
- Use Flexbox for one-dimensional alignment
- Prefer logical properties (inline/block)
- Use `auto-fit`/`minmax` for responsive grids

### Custom Properties
- Define design tokens as `--*` variables
- Use them consistently across components
- Scope overrides with `:root` or components
- Use `color-mix()` for derived colors

### Container Queries
- Use container queries for component-level responsiveness
- Define `container-type` on the container
- Combine with media queries for viewport
- Test components in isolation

### Cascade & Layers
- Organize with `@layer` (reset, tokens, base, components)
- Keep specificity low
- Avoid `!important` unless forced
- Prefer modern units (rem, ch, dvh)

## Dependencies
```bash
# No build step required — modern CSS works natively
```

## Examples
```css
/* Responsive grid layout */
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1rem;
}
```
```css
/* Design tokens */
:root {
  --color-bg: #0b0b1a;
  --color-accent: #8b5cf6;
  --space-1: 0.5rem;
  --radius: 12px;
}
.card { background: var(--color-bg); border-radius: var(--radius); padding: var(--space-1); }
```
```css
/* Container queries */
.cards { container-type: inline-size; }
@container (min-width: 500px) {
  .card { display: grid; grid-template-columns: 1fr 2fr; }
}
```
```css
/* Cascade layers */
@layer reset, tokens, base, components;
@layer tokens { :root { --accent: #8b5cf6; } }
@layer components { .btn { background: var(--accent); } }
```

## Step-by-Step
1. Define design tokens as custom properties.
2. Structure with @layer for maintainability.
3. Build layouts with Grid and Flexbox.
4. Use logical properties and modern units.
5. Add container queries for components.
6. Use color-mix and modern functions.
7. Scope styles and keep specificity low.
8. Test responsive behavior at breakpoints.

## Validation
1. Layouts adapt without media-query sprawl
2. Tokens are consistent across components
3. Container queries work in isolation
4. No specificity wars or !important
5. Performance: no layout thrash or huge stylesheets

## Troubleshooting
- Specificity issues: use @layer and low-specificity selectors.
- Responsive breakpoints piling up: use container queries.
- Old browser support: check target browsers for modern features.