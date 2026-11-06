---
name: vibe-shop-normalizer
description: "Normalizes messy vibe-coded e-commerce HTML/CSS/JS storefronts into clean, light-themed, responsive Zero-CLS production sites with verified catalog imagery and passing DOM tests. Use when cleaning up multi-iteration storefront code and fixing layout shifts."
category: frontend
tags: [frontend, ecommerce, css, responsive, performance, testing, tailwind]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-10-28
updated: 2026-10-28
language: ru
original: vibe-shop-normalizer
author: ssrjkk
---
# Vibe-Coded Storefront & Zero-CLS Normalizer (Нормализация вайбкод-витрин)

> Очистка навайбкоженных витрин интернет-магазинов от визуальной каши, прыжков верстки (CLS) и поломанных DOM-контрактов.

## Быстрый старт
```bash
# Synchronize storefront HTML/assets and execute the full Node.js test suite
npm run vibe:clean
node --test
```

```css
/* Strict Zero-CLS light storefront geometry */
html { scrollbar-gutter: stable; overflow-x: hidden; }
body { background-color: #F4F5F7; color: #141619; overflow-x: hidden; }
.watch-stage { aspect-ratio: 1 / 1; background: #F8FAFC; }
.card-title { min-height: 38px; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
```

## Когда использовать
- После десятка итераций вайбкодинга в HTML/CSS/JS появились дубли шапок, конфликты тем и сырые шаблонные строки ${...}
- Карточки товаров прыгают по высоте или вызывают горизонтальный скролл на экранах 320px, 768px и 1024px+
- Перевод пестрой черновой верстки в чистую коммерческую светлую тему (#F4F5F7 фон, #FFFFFF карточки, #141619 кнопки)
- Синхронизация витрины (index.html и public/index.html) с сохранением 100% прохождения контрактных автотестов

## Лучшие практики
- Начинайте рефакторинг с чтения автотестов (tests/*.test.js), чтобы сохранить все обязательные ID, роуты (#/catalog, #/p/:id) и классы скидок.
- Вычищайте случайно попавшие в статический HTML конструкции ${...} и удаляйте дублирующиеся блоки <nav> и модальных окон.
- Фиксируйте геометрию карточки: квадратный контейнер фото (aspect-ratio: 1 / 1), высоты заголовка (38px), характеристик (32px) и кнопок (h-10).
- Включайте табличные цифры (tabular-nums) для всех цен, таймеров и счетчиков корзины, чтобы смена цифр не двигала соседние блоки.
- Вызывайте .unref() у фоновых таймеров setInterval, чтобы тестовый раннер node --test завершался мгновенно без зависания.
- Синхронизируйте корневой index.html и public/index.html единым скриптом сборки для защиты от рассинхрона статики.

## Зависимости
```bash
# Run Node.js built-in test runner and storefront normalizer
node --version
node --test
```

## Примеры
```python
# Scan static HTML outside <script> blocks for leaked JS template literals (${...}) and duplicate IDs
import re
from collections import Counter

def audit_storefront_dom(html: str) -> dict:
    no_scripts = re.sub(r"<script\b[^>]*>.*?</script>", "", html, flags=re.S | re.I)
    leaked_tpl = re.findall(r"\$\{[^}]+\}", no_scripts)
    ids = re.findall(r'\bid=["\']([^"\']+)["\']', no_scripts)
    dupe_ids = [k for k, v in Counter(ids).items() if v > 1]
    return {"leaked_templates": leaked_tpl, "duplicate_ids": dupe_ids}
```

```javascript
// Safe background stock ticker that never hangs Node.js test runners
const ticker = setInterval(() => {
  updateLiveOrderToast();
}, 15000);
if (typeof ticker.unref === 'function') {
  ticker.unref();
}
```

## Пошаговое руководство
1. Изучите все тесты в папке tests/ и выпишите проверяемые селекторы DOM, мета-теги, хэш-роуты и глобальные функции.
2. Прогоните проверку audit_storefront_dom() для поиска утекших шаблонов ${...}, дублирующихся ID и лишних тегов <nav>.
3. Удалите деструктивные переопределения !important, перекрашивающие светлые классы .bg-white и .bg-gray-50 в темные цвета.
4. Примените чистую светлую палитру (#F4F5F7 общий фон, #FFFFFF карточки и модалки, #141619 основные кнопки, #0E9F6E акцент).
5. Зафиксируйте Zero-CLS геометрию карточек: aspect-ratio: 1 / 1 для фото, явные width/height у <img> и tabular-nums для цен.
6. Синхронизируйте index.html с public/index.html и обновите метрики размера бандла в документации при наличии проверок.
7. Запустите node --test и убедитесь в отсутствии горизонтального скролла на ширине 320px, 768px и 1280px.

## Валидация
1. Проверка audit_storefront_dom() подтверждает отсутствие утекших шаблонов ${...} и дублей ID в HTML
2. Набор автотестов node --test проходит на 100% и завершается без зависания процесса
3. На разрешениях 320px, 768px и 1280px отсутствует горизонтальная прокрутка (scrollWidth <= clientWidth)
4. Переключение фильтров, избранного и кнопки корзины не вызывает сдвига соседних карточек товаров (CLS = 0)

## Устранение неполадок
- Все тесты в node --test зеленые, но процесс висит — найдите запущенный setInterval и добавьте вызов timer.unref().
- Падает тест на размер файла в README после правок HTML — запустите скрипт синхронизации (vibe-clean.js) для пересчета метрик.
- Карточки в сетке разной высоты — задайте фиксированный min-height: 38px для заголовка в 2 строки и min-height: 32px для подзаголовка.
- Страница дергается по горизонтали при открытии модального окна — пропишите html { scrollbar-gutter: stable; } в базовых стилях.
