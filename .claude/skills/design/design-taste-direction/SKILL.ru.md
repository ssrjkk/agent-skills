---
name: design-taste-direction
description: "Applies intentional art direction, anti-template visual concepts, curated typographic pairings, and domain-specific color palettes to web interfaces. Use when moving beyond generic AI-generated layouts into distinctive brand experiences."
category: design
tags: [art-direction, design, typography, color-palette, branding, ui, frontend]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-10-28
updated: 2026-10-28
language: ru
original: design-taste-direction
author: ssrjkk
---
# Intentional Art Direction & Design Taste (Арт-дирекшн и визуальный вкус)

> Отказ от шаблонных фиолетовых ИИ-градиентов в пользу осмысленной композиции, предметных палитр и выразительной типографики.

## Быстрый старт
```markdown
# Art Direction Brief (Lock Before Writing CSS)
- Aesthetic Archetype: Precision Terminal / Swiss Editorial / Warm Craft
- Palette (max 3 hues): Canvas #0B0F0A, Surface #11170F, Primary Accent #7DFF4A, Secondary #00FFD1
- Type Pairing: Display/UI 'Inter' (600/700) + Technical/Data 'JetBrains Mono' (400/500)
- Signature Detail: 1px phosphor border glow + live terminal command preview
```

```python
# Check that a palette defines no more than 3 distinct chromatic accent hues
def validate_palette_restraint(hex_accents: list[str], max_accents: int = 3) -> bool:
    unique = {h.lower().strip() for h in hex_accents}
    return 1 <= len(unique) <= max_accents

assert validate_palette_restraint(["#7dff4a", "#00ffd1"])
```

## Когда использовать
- Сгенерированный сайт выглядит как клон тысячи шаблонных лендингов (фиолетово-синие градиенты, три скучные иконки в ряд)
- Формирование узнаваемого визуального языка для dev-тулинга, финтех-сервисов, витрин магазинов или образовательных порталов
- Подбор шрифтовых пар с поддержкой кириллицы и сбалансированной цветовой палитры по правилу 60-30-10
- Создание сильного визуального якоря на первом экране (живой терминал, интерактивное превью продукта или граф архитектуры)

## Лучшие практики
- Откажитесь от дефолтных фиолетово-розовых градиентов (#6366f1 / #8b5cf6), которые мгновенно выдают шаблонную генерацию.
- Применяйте пропорцию цвета 60–30–10: 60% спокойный фон холста, 30% плашки и карточки, 10% акцентный цвет для главных действий.
- Выбирайте один четкий архетип до написания кода: Инженерный Терминал, Швейцарская Типографика или Чистая Светлая Коммерция.
- Ставьте в центр первого экрана реальный артефакт продукта (живой терминал, интерактивный фильтр или студийный рендер товара).
- Стройте визуальную иерархию за счет контраста кегля, насыщенности и воздуха, а не нагромождения рамок и цветных плашек.
- Проверяйте выбранную шрифтовую пару на гармоничное отображение кириллицы и латиницы в одной строке.

## Зависимости
```bash
# Google Fonts preconnect for zero-FOUT Cyrillic + Latin typography
# Inter + JetBrains Mono or Manrope + IBM Plex Mono
python3 --version
```

## Примеры
```css
/* Archetype 1: Precision Developer Terminal (Dark Phosphor) */
.theme-terminal {
  --canvas: #0b0f0a;
  --surface: #11170f;
  --ink: #d6ffd0;
  --muted: #6f8f6a;
  --accent: #7dff4a;
  --font-sans: 'Inter', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
}
```

```css
/* Archetype 2: Crisp Commercial Storefront (Light Zero-CLS) */
.theme-storefront {
  --canvas: #f4f5f7;
  --surface: #ffffff;
  --ink: #141619;
  --muted: #5a6270;
  --accent: #0e9f6e;
  --font-sans: 'Manrope', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
}
```

## Пошаговое руководство
1. Составьте краткий арт-бриф из 4 пунктов (Архетип, Палитра 60–30–10, Шрифтовая пара и Главный артефакт хиро) до верстки.
2. Выберите не более двух гарнитур (основной гротеск и технический моноширинный шрифт) с полноценной кириллицей.
3. Зафиксируйте цветовые токены по правилу 60–30–10 и проверьте читаемость текста по WCAG.
4. Постройте первый экран вокруг живого демонстрационного блока (интерактивный терминал, поиск по базе или витрина).
5. Чередуйте плотные информационные секции (сетки карточек, таблицы) с лаконичными акцентными врезками.
6. Удалите визуальный мусор: разношерстные эмодзи вместо SVG-иконок, лишние тени и конкурирующие градиенты.

## Валидация
1. Палитра содержит не более 3 цветовых акцентов и выдерживает баланс площадей 60–30–10
2. На первом экране размещен осмысленный интерактивный или предметный блок продукта, а не абстрактная заглушка
3. Все иконки выполнены в единой толщине штриха SVG без использования случайных эмодзи в навигации
4. Английская и русская версии страницы сохраняют одинаковую визуальную плотность и баланс заголовков

## Устранение неполадок
- Страница все еще выглядит шаблонно — замените абстрактные иконки преимуществ на реальные фрагменты кода, цифры или скриншоты.
- Слишком пестрые бейджи категорий — переведите фон плашек в 10% прозрачности от основного цвета с тонкой рамкой 1px.
- Декоративный шрифт разваливается на русском языке — замените его на Manrope, Inter или Golos Text с родной кириллицей.
- Темный фон кажется грязно-серым — добавьте в цвет фона легкий оттенок основного акцента (#0b0f0a) вместо плоского #111111.
