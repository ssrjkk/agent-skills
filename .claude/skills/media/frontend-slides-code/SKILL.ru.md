---
name: frontend-slides-code
description: "Creates interactive, keyboard-navigable HTML/CSS/JS slide decks and technical presentations as code with zero external dependencies, live code blocks, SVG architecture diagrams, and PDF print export. Use for engineering talks, pitch decks, and interactive workshops."
category: media
tags: [slides, presentations, media, frontend, html, css, svg]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-10-28
updated: 2026-10-28
language: ru
original: frontend-slides-code
author: ssrjkk
---
# Frontend Slides as Code (Интерактивные презентации кодом на HTML/CSS/JS)

> Автономные интерактивные презентации 16:9 в одном HTML-файле с управлением с клавиатуры, живым кодом и экспортом в PDF.

## Быстрый старт
```html
<!-- Minimal 16:9 Slide Deck Container with Keyboard Navigation -->
<main class="deck" id="deck">
  <section class="slide active" data-slide="0">
    <span class="kicker">01 / Architecture</span>
    <h1>Cilium eBPF Cuts Service Routing Latency by 38% vs iptables</h1>
    <p>Direct socket bypass eliminates per-rule linear chain traversal at 500+ Services.</p>
  </section>
</main>
```

```javascript
// Keyboard navigation (ArrowRight/Space/ArrowLeft) and URL hash sync (#slide-1)
let cur = 0;
const slides = Array.from(document.querySelectorAll('.slide'));
function go(idx) {
  cur = Math.max(0, Math.min(slides.length - 1, idx));
  slides.forEach((s, i) => s.classList.toggle('active', i === cur));
  history.replaceState(null, '', `#slide-${cur + 1}`);
}
window.addEventListener('keydown', (e) => {
  if (e.key === 'ArrowRight' || e.key === ' ') go(cur + 1);
  if (e.key === 'ArrowLeft') go(cur - 1);
});
```

## Когда использовать
- Создание технических докладов, защиты архитектуры или питч-деков в виде одного автономного HTML-файла
- Встраивание живых интерактивных демо, копируемых блоков кода и векторных SVG-схем прямо внутрь слайдов
- Хранение презентаций в Git рядом с кодом проекта с чистыми текстовыми диффами без тяжелых бинарных файлов
- Экспорт презентации в широкоформатный PDF (16:9) напрямую из браузера через правила @media print

## Лучшие практики
- Пишите заголовки слайдов по модели Assertion-Evidence: каждый <h1> должен быть законченным тезисом с выводом («Karpenter снизил косты на 42%»), а не ярлыком («Обзор расходов»).
- Жестко ограничивайте плотность: не более 1 главного визуального блока (схема, график или код) и 3 коротких пунктов на один слайд.
- Фиксируйте пропорции холста 16:9 и масштабируйте шрифты через clamp(), чтобы контент никогда не вылезал за границы экрана.
- Добавляйте блок стилей @media print (@page { size: 16in 9in; margin: 0; }) для чистой выгрузки всех слайдов в PDF через Ctrl+P.
- Встраивайте индикатор прогресса, счетчик слайдов (03 / 12), горячие клавиши (стрелки, пробел, F для полного экрана) и поддержку свайпов.
- Держите повышенный контраст текста (>= 7:1 для заголовков), чтобы слайды отлично читались на проекторе в освещенном зале.

## Зависимости
```bash
# Validate HTML slide deck structure and div balance with Python
python3 --version
```

## Примеры
```css
/* 16:9 responsive slide stage and print-to-PDF support */
.slide {
  display: none;
  width: min(94vw, 1280px);
  aspect-ratio: 16 / 9;
  padding: clamp(2rem, 5vw, 4.5rem);
  flex-direction: column;
  justify-content: space-between;
}
.slide.active { display: flex; }
@media print {
  @page { size: 16in 9in; margin: 0; }
  .slide { display: flex !important; width: 100vw; height: 100vh; page-break-after: always; }
}
```

```python
# Audit an HTML slide deck for assertion headlines and balanced tags
import re

def audit_slide_deck(html: str) -> dict:
    slides = re.findall(r'<section[^>]*class="[^"]*slide[^"]*"[^>]*>(.*?)</section>', html, flags=re.S)
    h1s = [re.search(r"<h1[^>]*>(.*?)</h1>", s, flags=re.S) for s in slides]
    titles = [re.sub(r"<[^>]+>", "", m.group(1)).strip() for m in h1s if m]
    return {"slide_count": len(slides), "titles": titles, "balanced_divs": html.count("<div") == html.count("</div>")}
```

## Пошаговое руководство
1. Сначала составьте скелет из заголовков (Action Title Scan): чтение одних только заголовков 8–12 слайдов должно складываться в связный рассказ.
2. Сверстайте однофайловый HTML-каркас из тегов <section class="slide"> с пропорциями 16:9 и модульной сеткой.
3. Подключите навигацию со стрелок клавиатуры, пробела, кликов и свайпов с сохранением номера слайда в хэше URL (#slide-N).
4. Встройте векторные SVG-схемы архитектуры, карточки ключевых метрик и блоки кода с кнопкой копирования.
5. Добавьте правила @media print для постраничного экспорта презентации в PDF без обрезания фонов.
6. Прогоните проверку audit_slide_deck() для контроля числа слайдов, заголовков и парности HTML-тегов.

## Валидация
1. Функция audit_slide_deck() подтверждает баланс тегов <div> и наличие тезисного заголовка <h1> на каждом слайде
2. Клавиши стрелок, пробел, Home и End плавно переключают слайды и синхронизируют хэш адреса (#slide-N)
3. Внутри контейнеров 16:9 отсутствует переполнение или обрезка текста на разрешениях 1280x720 и 1920x1080
4. Печать страницы в PDF из браузера (@media print) формирует ровно по одной альбомной странице на каждый слайд

## Устранение неполадок
- Блок кода вылезает за нижний край слайда — оставляйте на слайде не более 12–14 ключевых строк кода крупным кеглем.
- При экспорте в PDF пропадает темный фон слайдов — добавьте свойство print-color-adjust: exact; -webkit-print-color-adjust: exact;.
- Нажатие пробела прокручивает окно браузера вместо смены слайда — вызывайте e.preventDefault() в обработчике keydown.
- Текст мигает при первом открытии — подключите preconnect для шрифтов в <head> и задайте системный моноширинный фоллбэк.
