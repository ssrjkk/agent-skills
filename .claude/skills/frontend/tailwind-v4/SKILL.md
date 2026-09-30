---
name: tailwind-v4
description: "Tailwind CSS v4 features"
category: frontend
tags: [tailwind, css, v4, design, styling]
models: [sonnet, opus]
version: 1.0.0
created: 2026-05-14
updated: 2026-09-29
---
# Tailwind CSS v4

> Harness Tailwind CSS v4's CSS-first configuration, new utilities, and performance improvements.

## Quick Start
```css
/* app.css — Tailwind v4 CSS-first configuration */
@import "tailwindcss";

/* Native CSS custom properties for theme */
@theme {
  --color-brand: #6c5ce7;
  --color-brand-light: #a29bfe;
  --font-display: "Inter", sans-serif;
  --breakpoint-3xl: 120rem;
  --animate-fade-in: fade-in 0.5s ease-in-out;
}

@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* @apply with modern CSS features */
.btn-primary {
  @apply bg-brand text-white px-4 py-2 rounded-lg 
         hover:bg-brand-light transition-colors
         focus-visible:outline-2 focus-visible:outline-brand;
}

/* Container queries with @cq-* */
.card-grid {
  @apply grid grid-cols-1 gap-4;
  @container (min-width: 30rem) {
    @apply grid-cols-2;
  }
  @container (min-width: 50rem) {
    @apply grid-cols-3;
  }
}
```

```html
<!-- v4 new features -->
<div class="
  /* 3D transforms */
  perspective-1000 rotate-x-45 rotate-y-30
  
  /* Scroll-driven animations */
  scroll-mt-20 scroll-snap-align-start
  
  /* New color functions */
  bg-linear-to-r from-red-500 to-blue-500
  
  /* Field sizing */
  field-sizing-content

  /* Text balancing */
  text-balance
  
  /* Inset shadows */
  shadow-inner-sm

  /* Container queries */  
  @max-md:flex-col @min-lg:flex-row
">
```

## Key Concepts
Tailwind v4 is CSS-first (no tailwind.config.js). New features: `@theme` directive, container queries, 3D transforms, scroll-driven animations, CSS `@layer` support, `text-balance`, and `field-sizing`.

## When to Use
- New projects starting with Tailwind v4
- Upgrading from v3 for smaller config and new features
- Projects needing container queries or 3D transforms

## Step-by-Step
1. Install v4: `npm install tailwindcss @tailwindcss/vite` and add the Vite plugin (or the PostCSS equivalent).
2. Create CSS entry: `@import "tailwindcss";` in your main CSS file — no `tailwind.config.js` needed.
3. Theme via `@theme`: define design tokens (colors, fonts, breakpoints, animations) as CSS custom properties.
4. Use v4 utilities: container queries (`@container`, `@min-*`/`@max-*`), 3D transforms, `text-balance`, `field-sizing`.
5. Compose with `@apply` inside modern CSS (`@layer`, nesting) and reference `@theme` tokens.
6. Build and verify: run the dev server, then compare production CSS size vs a v3 baseline; no v3 migration warnings.

## Examples
```css
/* app.css — custom variant + data attribute styling */
@import "tailwindcss";

@theme {
  --color-brand: #6c5ce7;
  --font-display: "Inter", sans-serif;
}

@custom-variant data-active (&[data-active="true"]);

.card[data-active="true"] {
  @apply border-brand text-brand bg-brand/10;
}
```
```html
<!-- v4 responsive + container query combo -->
<div class="@container">
  <div class="
    grid grid-cols-1
    @min-lg:grid-cols-3
    max-md:flex-col
    space-y-4
  ">
    <section class="text-balance shadow-inner-sm">Card A</section>
    <section class="bg-linear-to-r from-violet-500 to-fuchsia-500">Card B</section>
  </div>
</div>
```

## Best Practices
- Configure the theme via CSS `@theme` tokens, not config files.
- Use utility-first classes; extract components only when repeated.
- Leverage responsive and state variants (`hover:`, `md:`).
- Use `@apply` sparingly; prefer utilities in markup.
- Add custom utilities with `@utility` for repeated patterns.
- Enable content scanning for your template paths.

## Troubleshooting
- Classes not generated: check the content globs.
- Build too slow: narrow the content paths.
- Override issues: use variant ordering or `!` for important.
- v4 vs v3 config: migrate `tailwind.config` to CSS `@theme`.

## Validation
1. `@theme` custom properties are available in all utility classes
2. Container queries respond at correct breakpoints
3. Build output is smaller than equivalent v3 configuration
4. No v3 migration warnings during build
