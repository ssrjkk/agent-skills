---
name: jest
description: "Write reliable JavaScript tests with Jest: unit tests, mocking, snapshots, coverage, and CI integration. Use for JS/TS testing."
category: qa
tags: [jest, javascript, testing, mocking, coverage, typescript, unit-tests]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-09-29
updated: 2026-09-29
author: ssrjkk
---
# Jest

> Testing JavaScript and TypeScript with Jest.

## Quick Start
```bash
npm i -D jest @types/jest ts-jest
npx jest
```

## When to Use
- Unit tests for JS/TS code
- React/Node component logic
- API and utility function testing
- Coverage and regression suites

## Best Practices

### Test Structure
- Name tests by behavior: `test('adds numbers')`
- Arrange, act, assert per test
- One behavior per test
- Colocate or use `__tests__`

### Matchers & Assertions
- Use natural matchers (`toBe`, `toEqual`, `toContain`)
- Use `expect` with descriptive messages
- Test edge cases and errors
- Prefer `toEqual` for objects

### Mocking
- Mock external modules and side effects
- Use `jest.fn()` and `jest.spyOn()`
- Reset mocks between tests (`clearMocks`)
- Avoid over-mocking your own code

### Coverage & CI
- Set coverage thresholds
- Run in CI on every PR
- Use `--ci` and `--coverage`
- Keep tests fast and isolated

## Dependencies
```bash
npm i -D jest @types/jest ts-jest
# React: @testing-library/react
```

## Examples
```ts
// Basic test
function add(a: number, b: number) {
  return a + b;
}

test("adds two numbers", () => {
  expect(add(2, 3)).toBe(5);
});
```
```ts
// Mocking a module
import { fetchUsers } from "./api";
jest.mock("./api");

test("renders users", async () => {
  fetchUsers.mockResolvedValue([{ id: 1, name: "Alice" }]);
  const users = await loadUsers();
  expect(users).toHaveLength(1);
});
```
```ts
// Parameterized tests
test.each([
  [1, 1, 2],
  [2, 3, 5],
  [-1, 1, 0],
])("adds %i + %i = %i", (a, b, expected) => {
  expect(add(a, b)).toBe(expected);
});
```
```ts
// Spy and error test
const spy = jest.spyOn(console, "error").mockImplementation(() => {});
expect(() => risky()).toThrow();
spy.mockRestore();
```

## Step-by-Step
1. Install Jest and configure for your stack.
2. Add the test script and coverage thresholds.
3. Write focused unit tests.
4. Mock external dependencies.
5. Add edge case and error tests.
6. Run with `--coverage` and review gaps.
7. Wire Jest into CI.
8. Keep tests deterministic and fast.

## Validation
1. All tests pass locally and in CI
2. Coverage meets the threshold
3. Mocks are reset between tests
4. No tests depend on network or timers
5. Failures pinpoint the behavior

## Troubleshooting
- Flaky tests: remove shared state and timing.
- Over-mocked: mock only boundaries, not internals.
- Slow suite: use `--maxWorkers` and isolate heavy tests.