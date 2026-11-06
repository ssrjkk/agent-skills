---
name: vibe-seo-audit
description: "Audits and fixes SEO, SSR/prerendering, meta tags, Open Graph preview cards, sitemap.xml, robots.txt, PageSpeed/LCP performance, and curated GitHub/MCP/Cursor integrations for vibe-coded websites and SPAs. Use when fixing empty React/Vite root divs and search visibility."
category: frontend
tags: [seo, ssr, nextjs, astro, pagespeed, open-graph, mcp, frontend]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-10-28
updated: 2026-10-28
language: ru
original: vibe-seo-audit
author: ssrjkk
---
# Vibe-Coded Website SEO, SSR & Performance Audit (SEO-аудит вайбкод-сайтов)

> Превращение одностраничников с пустым div#root в быстрые индексируемые сайты с мета-тегами, Open Graph, sitemap.xml и PageSpeed 90+.

## Быстрый старт
```bash
# Verify that the initial HTTP response ships semantic HTML instead of an empty <div id="root"></div>
curl -s http://localhost:3000 | grep -E "<h1|<title|og:image"
test -f public/sitemap.xml && test -f public/robots.txt && echo "SEO files present"
```

```html
<!-- Complete SEO & Open Graph head block for crawler indexing and Telegram preview cards -->
<head>
  <title>AI Coder Portal — Roadmaps, Skills & Career</title>
  <meta name="description" content="Step-by-step IT roadmaps, 120 bilingual agent skills, and hands-on DevOps/AI labs." />
  <link rel="canonical" href="https://ssrjkk.github.io/agent-skills/" />
  <meta property="og:title" content="AI Coder Portal — Roadmaps, Skills & Career" />
  <meta property="og:description" content="Step-by-step IT roadmaps and 120 bilingual agent skills." />
  <meta property="og:image" content="https://ssrjkk.github.io/agent-skills/og-preview.webp" />
  <meta property="og:type" content="website" />
  <meta name="twitter:card" content="summary_large_image" />
</head>
```

## Когда использовать
- Сгенерированный нейросетью сайт на React/Vite отдает поисковому роботу пустой <div id="root"></div> вместо контента
- При отправке ссылки в Telegram или соцсети отображается голый URL без картинки и заголовка (отсутствует Open Graph)
- Низкий балл в PageSpeed Insights (< 90) и долгая отрисовка главного экрана (LCP > 2.5 с) из-за тяжелых PNG и лишних скриптов
- Подбор проверенных баз знаний GitHub (build-your-own-x, public-apis, awesome-mcp-servers, awesome-cursorrules) для сборки проекта

## Лучшие практики
- Отдавайте готовый семантический HTML (<header>, <main>, <h1>) сразу при сборке или на сервере через Next.js, Astro или скрипт пререндера.
- Держите ровно один заголовок <h1> на странице и прописывайте уникальные <title> и <meta name="description"> под реальные поисковые запросы.
- Указывайте полный абсолютный HTTPS-адрес в <meta property="og:image">, чтобы парсер Telegram гарантированно подтягивал превью-карточку.
- Конвертируйте тяжелые фоновые картинки из PNG/JPEG в формат WebP (до 180–200 КБ) с явными атрибутами width и height.
- Размещайте корректные файлы sitemap.xml и robots.txt в корне сайта и добавляйте домен в Google Search Console и Яндекс Вебмастер.
- Пишите заголовки под реальный поисковый спрос пользователей вместо абстрактных лозунгов про «инновационную синергию».

## Зависимости
```bash
# Convert heavy PNG/JPG assets to WebP and run Lighthouse SEO/LCP checks
cwebp -q 82 public/hero.png -o public/hero.webp
```

## Примеры
```python
# Audit an HTML file for empty SPA root, single H1, meta description, and absolute og:image
import re
from pathlib import Path

def audit_html_seo(html_text: str) -> list[str]:
    issues: list[str] = []
    if re.search(r'<div\s+id=["\']root["\']>\s*</div>', html_text):
        issues.append("Empty <div id='root'></div> detected: enable SSR or prerendering")
    h1_count = len(re.findall(r"<h1[\s>]", html_text, flags=re.I))
    if h1_count != 1:
        issues.append(f"Expected exactly 1 <h1> tag, found {h1_count}")
    if 'name="description"' not in html_text:
        issues.append("Missing <meta name='description'>")
    og_img = re.search(r'property="og:image"\s+content="([^"]+)"', html_text)
    if not og_img or not og_img.group(1).startswith("https://"):
        issues.append("og:image must be present and use an absolute https:// URL")
    return issues
```

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://ssrjkk.github.io/agent-skills/</loc>
    <lastmod>2026-10-28</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://ssrjkk.github.io/agent-skills/roadmaps.html</loc>
    <lastmod>2026-10-28</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
</urlset>
```

## Пошаговое руководство
1. Проверьте исходный код ответа сервера через curl -s <URL>, чтобы убедиться в наличии готового HTML вместо пустого <div id="root"></div>.
2. Подключите SSR/SSG (Next.js, Astro) или скрипт пререндера на этапе сборки для генерации семантической разметки.
3. Пропишите уникальные <title>, <meta name="description">, canonical и ровно один заголовок <h1> на каждой странице.
4. Добавьте разметку Open Graph (og:title, og:description, og:image с полным https:// URL) для красивых карточек в Telegram.
5. Создайте в корне файлы sitemap.xml и robots.txt и отправьте карту сайта на индексацию в Google Search Console и Яндекс Вебмастер.
6. Сожмите тяжелые изображения в WebP, добавьте preload для главного баннера и сократите JS-бандл до достижения LCP < 2.5 с.
7. Подключите курируемые репозитории (build-your-own-x, public-apis, awesome-mcp-servers, awesome-cursorrules) в рабочий стек.

## Валидация
1. Запрос curl -s <URL> возвращает заполненные теги <h1>, <main>, <title> и <meta name="description"> без выполнения JS
2. Функция проверки audit_html_seo() выдает 0 замечаний по всем страницам сайта
3. Файлы sitemap.xml и robots.txt отдаются с кодом HTTP 200 и проходят проверку в панелях вебмастеров
4. Оценка в PageSpeed Insights составляет 90+ баллов при времени загрузки главного контента LCP быстрее 2.5 секунды

## Устранение неполадок
- В Telegram не обновляется превью ссылки — проверьте абсолютный https:// путь в og:image и сбросьте кэш через бота @WebpageBot.
- Яндекс Вебмастер обходит сайт, но не индексирует контент — робот получает пустой div#root; включите пререндер HTML на этапе сборки.
- Показатель LCP остается выше 3 секунд после сжатия в WebP — уберите атрибут loading="lazy" у первого экрана и добавьте fetchpriority="high".
- Предупреждения о дублях title в панели вебмастера — сформируйте уникальные заголовки и теги canonical для каждой вложенной страницы.
