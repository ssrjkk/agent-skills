---
name: typescript
description: "Apply TypeScript for type-safe JavaScript: type design, generics, utility types, strict mode, and integration with modern tooling. Use for any JS codebase."
category: frontend
tags: [typescript, javascript, typing, generics, static-analysis, tooling]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
author: ssrjkk
created: 2026-09-20
updated: 2026-09-28
---
# TypeScript

> Type-safe JavaScript with strong typing, generics, and strict tooling.

## Quick Start
```bash
npm create vite@latest my-app -- --template vanilla-ts
cd my-app
npm i
npm run build
# tsconfig.json enables strict mode
```

## When to Use
- Any JavaScript project that grows beyond a few files
- Libraries and shared packages where API contracts matter
- Teams that want compile-time safety before runtime
- Refactoring large legacy JS codebases

## Best Practices

### Type Design
- Model the domain with unions, discriminated unions, and literals
- Derive types from data, not the other way around
- Prefer `type` aliases over `interface` for unions and mapped types
- Export shared types from a central `types.ts`

### Strictness
- Enable `strict: true` from the start
- Avoid `any`; use `unknown` and narrow with type guards
- Use `satisfies` to validate objects against a type without widening
- Enable `noUncheckedIndexedAccess` for array safety

### Generics
- Write generic functions with sensible constraints
- Use utility types: `Pick`, `Omit`, `Partial`, `Record`, `ReturnType`
- Prefer `infer` in conditional types for advanced extraction

## Dependencies
```bash
npm i -D typescript @types/node tsx
npx tsc --init
# set: strict true, noUncheckedIndexedAccess true
```

## Examples
```ts
// Discriminated union models a state machine safely
type Result<T> =
  | { status: "success"; data: T }
  | { status: "error"; message: string };

function handle(r: Result<number>): number {
  if (r.status === "success") return r.data;
  console.error(r.message);
  return 0;
}
```
```ts
// Generic function with constraint
function pluck<T, K extends keyof T>(items: T[], key: K): T[K][] {
  return items.map((item) => item[key]);
}

const names = pluck([{ name: "a", id: 1 }], "name"); // string[]
```
```ts
// satisfies keeps narrow types while checking shape
const config = {
  port: 3000,
  host: "0.0.0.0",
} satisfies Record<string, string | number>;

config.port; // number, not string | number
```
```ts
// Type guard narrows unknown
function isError(x: unknown): x is { message: string } {
  return typeof x === "object" && x !== null && "message" in x;
}
```

## Step-by-Step
1. Enable `strict: true` and `noUncheckedIndexedAccess` in `tsconfig.json`.
2. Model domain types first (unions, entities) before writing functions.
3. Write functions with explicit return types; avoid implicit `any`.
4. Use `unknown` for external input; narrow with guards and validation.
5. Prefer `satisfies` for config objects; use `as const` for literals.
6. Extract complex logic into generics only when reused twice or more.
7. Add `tsc --noEmit` to CI; enforce on every PR.
8. Run `tsc` in watch mode during development for fast feedback.

## Validation
1. `tsc --noEmit` passes with zero errors
2. No `any` in new code (lint rule `@typescript-eslint/no-explicit-any`)
3. Public APIs of shared modules have explicit types
4. Runtime behavior matches types (no unsafe casts to work around errors)
5. Build (`tsup`/`vite build`) completes cleanly

## Troubleshooting
- "Property does not exist": the type is narrower than you think — narrow with guards.
- "Not assignable": mismatch between declared and actual shape — fix the data contract, not the cast.
- Weird `any` leaks: check `ts-ignore` and third-party typings.