---
name: svelte
description: "Build reactive UIs with Svelte 5: runes, stores, components, and transitions. Use for efficient interactive frontends."
category: frontend
tags: [svelte, sveltekit, javascript, runes, components, reactive]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-09-29
updated: 2026-09-29
author: ssrjkk
---
# Svelte

> Compiler-driven reactive UIs with Svelte.

## Quick Start
```bash
npm create svelte@latest my-app
cd my-app && npm install && npm run dev
```

## When to Use
- Highly interactive frontends
- Small bundle sizes (compiled, no runtime)
- Teams wanting simple reactivity
- SvelteKit full-stack apps

## Best Practices

### Runes (Svelte 5)
- Use `$state` for reactive state
- Use `$derived` for computed values
- Use `$props` for component inputs
- Avoid direct mutation of `$state` from outside

### Components
- Compose small focused components
- Pass data with props; emit with callbacks
- Use snippets for reusable markup
- Keep stores for shared state

### Stores
- Use writable/readable for shared state
- Derive with `derived`
- Subscribe minimally; unsubscribe
- Prefer runes for local state

### Performance
- Compiler removes unused code automatically
- Use `{#key}` to recreate blocks
- Lazy-load routes and heavy components
- Virtualize long lists

## Dependencies
```bash
npm create svelte@latest my-app -- --template demo
npm i svelte
```

## Examples
```svelte
<script lang="ts">
  let count = $state(0);
  const doubled = $derived(count * 2);
</script>

<button onclick={() => count++}>Count: {count}</button>
<p>Doubled: {doubled}</p>
```
```svelte
<script>
  let { title, done = false } = $props();
</script>

<h2>{title}</h2>
{#if done}<span>done</span>{/if}
```
```svelte
<script>
  import { writable } from "svelte/store";

  const cart = writable<string[]>([]);
  function add(item: string) {
    cart.update(items => [...items, item]);
  }
</script>

{#each $cart as item}<p>{item}</p>{/each}
```
```svelte
<!-- Transitions and keyed blocks -->
<script>
  import { fade } from "svelte/transition";
  let items = $state([1, 2, 3]);
</script>

{#each items as item, i (item)}
  <p transition:fade>{item}</p>
{/each}
```

## Step-by-Step
1. Scaffold with SvelteKit.
2. Set up routing and a global layout.
3. Build pages with runes and components.
4. Extract shared logic into stores.
5. Add transitions and animations.
6. Load data with SvelteKit load functions.
7. Optimize with lazy loading.
8. Write tests with Vitest + Testing Library.

## Validation
1. `npm run build` passes
2. State updates reflect in the DOM
3. Stores update subscribers correctly
4. No memory leaks from subscriptions
5. Bundle size stays small

## Troubleshooting
- State not reactive: use `$state`, not plain `let`.
- Store leaks: unsubscribe in `onDestroy`.
- SSR mismatch: avoid browser-only APIs in load.