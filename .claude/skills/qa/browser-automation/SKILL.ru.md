---
name: browser-automation
description: "Automate browsers with Playwright: selectors, waits, assertions, screenshots, network interception, and CI. Use for E2E tests and scraping."
category: qa
tags: [browser-automation, qa, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: browser-automation
author: ssrjkk
---
# Browser Automation (Автоматизация браузера)

> Автоматизация реальных браузеров через Playwright для E2E-тестов и скрапинга.

## Быстрый старт
```bash
npm init playwright@latest
npx playwright test
# или в Python:
pip install playwright && playwright install
```

## Когда использовать
- End-to-end тесты пользовательских сценариев
- Визуальные регрессии и скриншот-проверки
- Веб-скрапинг и сбор данных
- Мониторинг критичных пользовательских путей

## Лучшие практики

### Селекторы
- Предпочитайте role и text селекторы вместо CSS/XPath
- Используйте `getByRole`, `getByLabel`, `getByText` для надёжных запросов
- Добавляйте `data-testid` для сложных компонентов
- Избегайте хрупких CSS-селекторов, привязанных к layout

### Ожидания и тайминги
- Используйте auto-waiting действия; избегайте фиксированных sleep
- Ждите явных условий (`waitFor` network idle)
- Предпочитайте `expect().toBeVisible()` вместо sleep
- Ставьте щедрые таймауты для медленных окружений

### Ассерты
- Проверяйте видимое пользователю поведение, а не внутренности
- Используйте soft assertions, где фейл не должен прерывать
- Делайте скриншоты при фейле для отладки
- Проверяйте сетевые запросы и ответы

### Надёжность
- Запускайте в CI с retries на флаки
- Изолируйте тесты: свежее состояние на тест
- Осторожно с параллельными воркерами и общим состоянием
- Обрабатывайте popup, диалоги и multi-tab сценарии

## Зависимости
```bash
npm init playwright@latest
npx playwright install --with-deps
# или Python:
pip install pytest-playwright
```

## Примеры
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
# Тестовый файл с Playwright runner
from playwright.sync_api import Page, expect

def test_login(page: Page):
    page.goto("/login")
    page.get_by_label("Email").fill("user@example.com")
    page.get_by_role("button", name="Sign in").click()
    expect(page.get_by_text("Welcome back")).to_be_visible()
```
```js
// JavaScript E2E тест
const { test, expect } = require("@playwright/test");

test("search flow", async ({ page }) => {
  await page.goto("/");
  await page.getByPlaceholder("Search...").fill("playwright");
  await page.keyboard.press("Enter");
  await expect(page.locator("h1")).toContainText("Results");
});
```
```python
# Перехват сети и скриншот
def test_intercept(page):
    page.route("**/api/data", lambda route: route.fulfill(json={"ok": True}))
    page.goto("/")
    page.screenshot(path="home.png", full_page=True)
```

## Пошаговое руководство
1. Установите Playwright и настройте тестовый проект.
2. Определите критичные пользовательские сценарии первыми.
3. Пишите тесты с role-селекторами и auto-waiting.
4. Проверяйте видимое поведение; добавляйте скриншоты при фейле.
5. Перехватывайте внешние API для изоляции тестов.
6. Запускайте локально; чините флаки через retries и waits.
7. Добавьте тесты в CI с параллельными воркерами.
8. Расширяйте покрытие до визуальных регрессий и мониторинга.

## Валидация
1. Тесты стабильно проходят 3+ запуска
2. Селекторы переживают мелкие изменения UI
3. Скриншоты фейла фиксируют состояние
4. Внешние сети не протекают в тесты
5. CI гоняет их на каждом PR с приемлемым временем

## Устранение неполадок
- Флаки waits: заменяйте sleep явными waits и ассертами.
- Элемент не найден: используйте role/text селекторы; проверяйте iframes и shadow DOM.
- Медленный сьют: параллельте и ограничьте full-page скриншоты.