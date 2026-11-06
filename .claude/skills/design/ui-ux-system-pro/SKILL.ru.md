---
name: ui-ux-system-pro
description: "Designs token-driven UI/UX systems with fluid typographic scales, 8px spatial grids, WCAG AA/AAA perceptual contrast, and complete interactive component states. Use for building cohesive design systems, dashboards, and web applications."
category: design
tags: [design-system, ui, ux, typography, accessibility, tokens, css, frontend]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-10-28
updated: 2026-10-28
language: ru
original: ui-ux-system-pro
author: ssrjkk
---
# UI/UX Design System Pro (Токенизированные дизайн-системы)

> Математическая шкала типографики, строгая модульная сетка 8px, контрастность WCAG AA/AAA и полная матрица состояний компонентов.

## Быстрый старт
```css
:root {
  --space-1: 0.25rem; --space-2: 0.5rem; --space-3: 0.75rem; --space-4: 1rem;
  --space-6: 1.5rem;  --space-8: 2rem;   --space-12: 3rem;  --space-16: 4rem;
  --radius-sm: 6px;   --radius-md: 10px; --radius-lg: 16px;
  --text-xs: 0.75rem; --text-sm: 0.875rem; --text-base: 1rem; --text-lg: 1.125rem;
  --text-xl: 1.25rem; --text-2xl: 1.5rem;  --text-3xl: clamp(1.875rem, 3vw, 2.5rem);
}
```

```python
# Verify WCAG 2.1 relative luminance and contrast ratio (>= 4.5 for normal text, >= 3.0 for large text)
def wcag_contrast(hex_fg: str, hex_bg: str) -> float:
    def lum(h: str) -> float:
        h = h.lstrip("#")
        rgb = [int(h[i:i+2], 16) / 255.0 for i in (0, 2, 4)]
        c = [v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4 for v in rgb]
        return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
    l1, l2 = sorted([lum(hex_fg), lum(hex_bg)], reverse=True)
    return round((l1 + 0.05) / (l2 + 0.05), 2)

assert wcag_contrast("#141619", "#F4F5F7") >= 12.0
```

## Когда использовать
- Проектирование архитектуры семантических CSS-токенов для нового веб-приложения, дашборда или портала документации
- Устранение разнобоя в отступах, случайных размеров шрифта и слепого низкоконтрастного текста в темной и светлой темах
- Определение полной матрицы состояний (default, hover, focus-visible, active, disabled, loading, empty, error) для компонентов
- Аудит интерфейса на доступность с клавиатуры, размер областей нажатия (>= 44x44px) и адаптивность сетки

## Лучшие практики
- Разделяйте примитивные токены (палитра цветов, шаги в пикселях) и семантические токены (--bg-canvas, --bg-surface, --text-primary).
- Выравнивайте все отступы и зазоры строго по модульной шкале 4px/8px (4, 8, 12, 16, 24, 32, 48, 64px).
- Соблюдайте стандарт контрастности WCAG AA: не менее 4.5:1 для основного текста и не менее 3.0:1 для крупных заголовков и рамок.
- Ограничивайте длину строки текста на уровне 60–75 символов (max-width: 65ch) при межстрочном интервале 1.15 для заголовков и 1.6 для текста.
- Рассчитывайте скругление вложенных элементов по формуле R_inner = max(2px, R_outer - padding) для визуальной концентричности углов.
- Обязательно задавайте заметное кольцо фокуса :focus-visible (2px solid var(--accent)) для навигации с клавиатуры.

## Зависимости
```bash
# Verify contrast ratios and CSS token consistency with Python
python3 --version
```

## Примеры
```css
/* Semantic dark and light theme surface hierarchy */
:root, [data-theme="dark"] {
  --bg-canvas: #0b0f0a;
  --bg-surface: #11170f;
  --bg-elevated: #172114;
  --text-primary: #e6ffe2;
  --text-muted: #88a883;
  --accent: #7dff4a;
  --border: rgba(125, 255, 74, 0.16);
}
[data-theme="light"] {
  --bg-canvas: #f4f6f1;
  --bg-surface: #ffffff;
  --bg-elevated: #eef2ea;
  --text-primary: #14321f;
  --text-muted: #4a6a52;
  --accent: #1a7f37;
  --border: rgba(20, 80, 40, 0.16);
}
```

```css
/* Accessible interactive button with complete state matrix */
.btn {
  display: inline-flex; align-items: center; justify-content: center; gap: var(--space-2);
  min-height: 40px; padding: var(--space-2) var(--space-4);
  font-weight: 600; font-size: var(--text-sm); border-radius: var(--radius-sm);
  transition: transform 150ms ease, background-color 150ms ease, border-color 150ms ease;
}
.btn:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
.btn:active:not(:disabled) { transform: translateY(1px); }
.btn:disabled { opacity: 0.45; cursor: not-allowed; }
```

## Пошаговое руководство
1. Определите семантические токены фонов, текста, рамок и акцентов для темной и светлой темы в корневом блоке :root.
2. Задайте модульную типографическую шкалу (от xs до 3xl) с плавным масштабированием clamp() для крупных заголовков.
3. Привяжите все внутренние и внешние отступы к сетке 4px/8px, удалив случайные дробные значения из таблиц стилей.
4. Прогоните проверку wcag_contrast() для всех пар текст/фон и убедитесь в соблюдении порога >= 4.5:1.
5. Реализуйте все 8 состояний (default, hover, focus-visible, active, disabled, loading, empty, error) для кнопок, полей ввода и карточек.
6. Проверьте адаптивное поведение макета на ширинах 320px, 768px, 1024px и 1440px с учетом prefers-reduced-motion.

## Валидация
1. Все пары семантических токенов текст/фон проходят проверку контрастности WCAG AA (>= 4.5:1 для текста, >= 3.0:1 для заголовков)
2. В стилях компонентов отсутствуют захардкоженные hex-цвета и отступы вне модульной сетки 4px/8px
3. При навигации клавишей Tab каждый интерактивный элемент получает четкую обводку :focus-visible
4. Все кнопки и переключатели имеют область нажатия не менее 40x40px на мобильных экранах

## Устранение неполадок
- Карточки в темной теме сливаются с фоном — добавьте тонкую полупрозрачную рамку 1px и используйте более светлый токен поверхности.
- Неоновый акцент не читается на белом фоне в светлой теме — переключайте токен --accent на глубокий оттенок (#1a7f37) для [data-theme="light"].
- Внутренние углы вложенного блока выглядят криво — вычитайте величину padding родителя из внешнего border-radius.
- Кириллические заголовки кажутся слипшимися — используйте шрифты с качественной кириллицей (Inter, Manrope, JetBrains Mono).
