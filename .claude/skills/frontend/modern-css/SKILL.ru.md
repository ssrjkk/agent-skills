---
name: modern-css
description: "Use modern CSS: layout (grid/flex), custom properties, container queries, cascade layers, and responsive design. Use for maintainable styling."
category: frontend
tags: [modern-css, frontend, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: modern-css
author: ssrjkk
---
# Modern CSS (Современный CSS)

> Поддерживаемые и производительные стили на современном CSS.

## Быстрый старт
```css
:root { --accent: #8b5cf6; }
.card { padding: 1rem; border: 1px solid color-mix(in srgb, var(--accent), white 40%); }
```

## Когда использовать
- Стилизация без тяжёлых фреймворков
- Адаптивные и поддерживаемые макеты
- Дизайн-системы с токенами
- Библиотеки компонентов

## Лучшие практики

### Layout
- Grid для макета страницы/компонента
- Flexbox для одномерного выравнивания
- Логические свойства (inline/block)
- `auto-fit`/`minmax` для адаптивных гридов

### Custom properties
- Токены дизайна как `--*` переменные
- Консистентное использование
- Переопределения через `:root` или компоненты
- `color-mix()` для производных цветов

### Container queries
- Компонентная адаптивность
- `container-type` на контейнере
- Комбинируйте с media queries
- Тестируйте компоненты изолированно

### Cascade и слои
- Организация через `@layer` (reset, tokens, base, components)
- Низкая специфичность
- Избегайте `!important` без крайней нужды
- Современные единицы (rem, ch, dvh)

## Зависимости
```bash
# Сборка не нужна — современный CSS работает нативно
```

## Примеры
```css
/* Адаптивный grid */
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1rem;
}
```
```css
/* Токены дизайна */
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

## Пошаговое руководство
1. Определите токены дизайна как custom properties.
2. Структурируйте через @layer.
3. Макеты на Grid и Flexbox.
4. Логические свойства и современные единицы.
5. Container queries для компонентов.
6. color-mix и современные функции.
7. Скоуп стилей и низкая специфичность.
8. Тестируйте адаптивность на брейкпоинтах.

## Валидация
1. Макеты адаптируются без разрастания media queries
2. Токены консистентны между компонентами
3. Container queries работают изолированно
4. Нет войн специфичности или !important
5. Производительность: без layout thrash и гигантских таблиц стилей

## Устранение неполадок
- Проблемы специфичности: используйте @layer и низкоспецифичные селекторы.
- Много брейкпоинтов: применяйте container queries.
- Поддержка старых браузеров: проверьте целевые браузеры для новых фич.