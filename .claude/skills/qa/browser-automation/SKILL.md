---
name: browser-automation
description: "Automate browsers with Playwright: selectors, waits, assertions, screenshots, network interception, and CI. Use for E2E tests and scraping."
category: qa
tags: [playwright, browser, e2e, testing, automation, scraping, selectors]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-09-25
updated: 2026-09-28
author: ssrjkk
---
# Browser Automation

> Automating real browsers with Playwright for E2E tests and scraping.

## Quick Start
```bash
npm init playwright@latest
npx playwright test
# or in Python:
pip install playwright && playwright install
```

## When to Use
- End-to-end tests of user flows
- Visual regression and screenshot checks
- Web scraping and data collection
- Monitoring critical user journeys

## Best Practices

### Selectors
- Prefer role and text selectors over CSS/XPath
- Use `getByRole`, `getByLabel`, `getByText` for robust queries
- Add `data-testid` for complex components
- Avoid brittle CSS selectors tied to layout

### Waits & Timing
- Use auto-waiting actions; avoid fixed sleeps
- Wait for explicit conditions (`waitFor` network idle)
- Prefer `expect().toBeVisible()` over sleep
- Set generous timeouts for slow environments

### Assertions
- Assert user-visible behavior, not internals
- Use soft assertions where failure shouldn't abort
- Take screenshots on failure for debugging
- Verify network requests and responses

### Reliability
- Run tests in CI with retries on flakiness
- Isolate tests: fresh state per test
- Use parallel workers carefully with shared state
- Handle popups, dialogs, and multi-tab flows

## Dependencies
```bash
npm init playwright@latest
npx playwright install --with-deps
# or Python:
pip install pytest-playwright
```

## Examples
```python
from playwright.sync_api import sync_playwright, expect

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://example.com/login")
    page.get_by_label("Email").fill("user@example.com")
    page.get_by_label("Password").fill("secret")
    page.get_by_role("button", name="Sign in").click()
    expect(page).to_have_url("https://example.com/dashboard")
    browser.close()
```
```python
# Test file with Playwright test runner
from playwright.sync_api import Page, expect

def test_login(page: Page):
    page.goto("/login")
    page.get_by_label("Email").fill("user@example.com")
    page.get_by_role("button", name="Sign in").click()
    expect(page.get_by_text("Welcome back")).to_be_visible()
```
```js
// JavaScript E2E test
const { test, expect } = require("@playwright/test");

test("search flow", async ({ page }) => {
  await page.goto("/");
  await page.getByPlaceholder("Search...").fill("playwright");
  await page.keyboard.press("Enter");
  await expect(page.locator("h1")).toContainText("Results");
});
```
```python
# Network interception and screenshot
def test_intercept(page):
    page.route("**/api/data", lambda route: route.fulfill(json={"ok": True}))
    page.goto("/")
    page.screenshot(path="home.png", full_page=True)
```

## Step-by-Step
1. Install Playwright and set up the test project.
2. Identify the critical user flows to cover first.
3. Write tests with role-based selectors and auto-waiting.
4. Assert user-visible behavior; add screenshots on failure.
5. Intercept external APIs to isolate tests.
6. Run locally; fix flakiness with retries and waits.
7. Add tests to CI with parallel workers.
8. Extend coverage to visual regression and monitoring.

## Validation
1. Tests pass consistently across 3+ runs
2. Selectors survive minor UI changes
3. Failure screenshots capture the failing state
4. No network dependency leaks into tests
5. CI runs them on every PR with acceptable runtime

## Troubleshooting
- Flaky waits: replace sleeps with explicit waits and assertions.
- Element not found: use role/text selectors; check iframes and shadow DOM.
- Slow suite: parallelize and limit full-page screenshots.