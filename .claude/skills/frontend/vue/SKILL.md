---
name: vue
description: "Build reactive user interfaces with Vue 3: Composition API, reactivity, components, state, and tooling. Use for any Vue-based UI work."
category: frontend
tags: [vue, vue3, javascript, typescript, frontend, reactivity, components]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-09-26
updated: 2026-09-28
author: ssrjkk
---
# Vue

> Building reactive UIs with Vue 3 and the Composition API.

## Quick Start
```bash
npm create vue@latest my-app
cd my-app
npm install
npm run dev
```

## When to Use
- Progressive enhancement on existing pages
- Single-file-component SPAs
- Teams wanting a gentle learning curve
- Reusable component libraries

## Best Practices

### Composition API
- Use `<script setup>` for concise components
- Compose logic into reusable `composables`
- Keep reactive state minimal and explicit
- Use `ref` for primitives, `reactive` for objects

### Components
- Split UI into small focused components
- Define props with types and defaults
- Emit typed events instead of mutating props
- Use slots for flexible composition

### Performance
- Use `computed` for derived state
- Virtualize long lists
- Lazy-load routes and heavy components
- Use `v-memo` and `shallowRef` where appropriate

### State
- Local state with `ref`/`reactive` first
- Add Pinia for shared app state
- Keep stores focused and typed
- Avoid over-engineering with global state

## Dependencies
```bash
npm create vue@latest my-app -- --typescript --router --pinia
npm i vue
```

## Examples
```vue
<script setup lang="ts">
import { ref, computed } from "vue";

const count = ref(0);
const doubled = computed(() => count.value * 2);

function increment() {
  count.value += 1;
}
</script>

<template>
  <button @click="increment">Count: {{ count }}</button>
  <p>Doubled: {{ doubled }}</p>
</template>
```
```ts
// Reusable composable
import { ref } from "vue";

export function useCounter(start = 0) {
  const count = ref(start);
  const increment = () => count.value++;
  const decrement = () => count.value--;
  return { count, increment, decrement };
}
```
```vue
<script setup lang="ts">
// Props with types and events
interface Props {
  title: string;
  done?: boolean;
}
const props = withDefaults(defineProps<Props>(), { done: false });
const emit = defineEmits<{ (e: "toggle", id: number): void }>();
</script>
```
```ts
// Pinia store
import { defineStore } from "pinia";
import { ref } from "vue";

export const useCartStore = defineStore("cart", () => {
  const items = ref<string[]>([]);
  const total = ref(0);
  const add = (item: string, price: number) => {
    items.value.push(item);
    total.value += price;
  };
  return { items, total, add };
});
```

## Step-by-Step
1. Scaffold with `create-vue` (TypeScript, Router, Pinia).
2. Set up a global layout with navigation.
3. Build pages as route components.
4. Extract shared logic into composables.
5. Add Pinia stores for shared state.
6. Create reusable components with typed props.
7. Optimize: lazy routes, computed, virtualization.
8. Write tests with Vitest + Vue Test Utils.

## Validation
1. `npm run build` passes with type checking
2. `npm run lint` is clean
3. Components render and update reactively
4. No unnecessary re-renders (Vue DevTools)
5. Tests pass for core logic and components

## Troubleshooting
- Reactive loss: unwrap refs in templates; use `reactive` for objects.
- "Cannot find module": check path aliases and `tsconfig`.
- Devtools missing state: check Pinia installation and plugin order.