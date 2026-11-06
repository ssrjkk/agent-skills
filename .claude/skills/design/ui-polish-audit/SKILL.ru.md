---
name: ui-polish-audit
description: "Audits and refines existing UI layouts for optical alignment, baseline consistency, visual hierarchy, tabular numbers, and micro-interaction polish. Use when upgrading rough prototypes into production-grade interfaces."
category: design
tags: [ui-polish, design, frontend, css, visual-hierarchy, alignment, ux]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-10-28
updated: 2026-10-28
language: ru
original: ui-polish-audit
author: ssrjkk
---
# Impeccable UI Polish & Optical Alignment Audit (Шлифовка интерфейса и иерархии)

> Выявление и устранение визуального шума, разъехавшихся базовых линий, тесных карточек и пропущенных состояний интерфейса.

## Быстрый старт
```css
/* Optical polish: tabular numbers, balanced headings, and smooth border transitions */
.metric, .price, .counter { font-variant-numeric: tabular-nums; }
h1, h2, h3 { text-wrap: balance; }
p { text-wrap: pretty; max-width: 65ch; }
.card { display: flex; flex-direction: column; justify-content: space-between; }
```

```python
# Check CSS file for common anti-patterns: transition: all, missing box-sizing, or raw z-index > 1000
import re
from pathlib import Path

def audit_css_polish(css_text: str) -> list[str]:
    warnings: list[str] = []
    if re.search(r"transition\s*:\s*all\b", css_text):
        warnings.append("Avoid 'transition: all'; animate only transform, opacity, or color")
    if "box-sizing: border-box" not in css_text and "box-sizing:border-box" not in css_text:
        warnings.append("Missing global box-sizing: border-box reset")
    return warnings
```

## Когда использовать
- Интерфейс работает функционально, но выглядит «сырым» из-за разной высоты карточек, рваных переносов и случайных отступов
- Числа в таблицах, ценах, таймерах или счетчиках дергают верстку при обновлении значений
- Элементы в шапке, тулбаре или подвале карточки не выровнены по единой оптической оси
- Финальная зачистка сдвигов макета (CLS), полос прокрутки и резких скачков состояний перед релизом

## Лучшие практики
- Держите макро-отступы (между секциями: 48–64px) заметно больше микро-отступов (внутри карточек: 16–24px) по закону близости.
- Выравнивайте подвалы карточек в одной строке Grid-сетки через display: flex; flex-direction: column и margin-top: auto у блока кнопок.
- Добавляйте text-wrap: balance заголовкам, чтобы избегать «висячих» одиночных слов на последней строке.
- Запретите свойство transition: all — анимируйте явно только transform, opacity, background-color или border-color.
- Выравнивайте числовые колонки таблиц по правому краю с tabular-nums, а текстовые названия — по левому.
- Заменяйте прыгающие индикаторы загрузки на скелетоны, точно повторяющие высоту контента.

## Зависимости
```bash
# Run CSS polish checks and verify DOM alignment
python3 --version
```

## Примеры
```css
/* Equal-height grid cards with pinned footer actions */
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1rem;
  align-items: stretch;
}
.card-item {
  display: flex;
  flex-direction: column;
  padding: 1.25rem;
}
.card-item-footer {
  margin-top: auto;
  padding-top: 1rem;
}
```

```css
/* Optical icon-to-text alignment inside badges and buttons */
.badge {
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  line-height: 1;
  padding: 0.25rem 0.625rem;
}
.badge svg {
  width: 14px;
  height: 14px;
  flex-shrink: 0;
}
```

## Пошаговое руководство
1. Проверьте вертикальные оси выравнивания: левые края заголовков секций, сеток карточек и таблиц должны лежать на одной линии.
2. Выстройте вертикальный ритм: 48–64px между секциями, 20–24px внутри карточек и 8–12px между элементами внутри карточки.
3. Прижмите кнопки действий к низу карточек в Grid-сетке с помощью flex-direction: column и margin-top: auto.
4. Добавьте правило font-variant-numeric: tabular-nums всем ценам, метрикам, бейджам количества и таблицам.
5. Включите text-wrap: balance для заголовков и ограничьте ширину текстовых абзацев до 65ch.
6. Прогоните проверку audit_css_polish() и протестируйте состояния hover, focus-visible, empty и error в обеих темах.

## Валидация
1. Все карточки в одном ряду сетки имеют одинаковую высоту и выровненные по одной линии нижние кнопки
2. Проверка audit_css_polish() не находит запрещенных конструкций transition: all
3. Обновление счетчиков и цен не вызывает горизонтального дрожания символов
4. Иконки внутри кнопок и ссылок меню строго отцентрированы по высоте текста и имеют flex-shrink: 0

## Устранение неполадок
- SVG-иконка сжимается при переносе текста кнопки на узком экране — добавьте свойство flex-shrink: 0 для всех тегов svg.
- Кнопка дергается на 2px при появлении рамки на ховере — задайте border: 1px solid transparent в базовом состоянии и меняйте только цвет.
- Текст в таблице прилипает к границам ячеек — задайте padding не менее 10px по вертикали и 14px по горизонтали.
- Центрированный контейнер прыгает при фильтрации списка — добавьте правило html { scrollbar-gutter: stable; }.
