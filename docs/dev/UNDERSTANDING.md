# UNDERSTANDING — погружение в проект

## Суть одним абзацем
**agent-skills** — двуязычная (EN/RU) библиотека из 120 production-grade «скиллов» для AI-агентов (Claude Code, OpenCode, Cursor, Windsurf и любые совместимые), решающая боль «взял сниппет из интернета → он не работает и не проверяется». Каждый скилл — папка с `SKILL.md` (EN) и `SKILL.ru.md`, валидируемая схемой, качеством и кросс-агентной переносимостью в CI. Библиотека поставляется как Python SDK + CLI (PyPI), npm-пакет и GitHub Action, а GitHub Pages-портал превращает её в обучающий продукт: 20 live-роадмапов (Junior→Principal), 25 полнотекстовых мап-энциклопедий и chaos-лаборатории с автопроверкой. Целевой пользователь — инженер/AI-кодер, которому нужен проверенный контекст для агента и структурированный путь обучения; вторая аудитория — рекрутёр, для которого портал и метрики являются верифицируемым портфолио (страница `hire.html`).

## Карта архитектуры
```
Контент (источник истины)
  .claude/skills/{domain}/{skill}/SKILL[.ru].md   ← 120 скиллов, 20 доменов
  roadmaps/<slug>.json                            ← 20 live-треков
  roadmaps/guides/*.md                            ← 25 полных мап
Генерация
  src/claude_skills/        — SDK: validator, quality, catalog, models, CLI (click)
  scripts/build_docs.py     — единый генератор сайта: index/skills/domains/
                              roadmaps/guides/hire + style.css + site.js + sitemap
  scripts/sync_readme.py    — README ← каталог (+ замер Quality-строки)
  scripts/sync_npm.py       — снапшот каталога в npm/ + сверка версий
Проверки (каждый пуш, 4 версии Python)
  validate.yml → catalog → validate → quality-gate → sync-readme --check
  → npm-snapshot --check → anti-patterns → interop → fences → pytest(332)
  → coverage → package build → docker build → docs → consistency →
  pip-audit → responsive (Chromium, 4 вьюпорта) → deploy-pages
  codeql.yml → CodeQL (python/js-ts/actions)
Публикация
  deploy-pages → GitHub Pages (ssrjkk.github.io/agent-skills)
  pypi.yml → PyPI по тегам
```

## Ключевые сценарии (вход → результат)
1. Установка SDK: `pip install agent-skills-library` → `agent-skills stats/search/validate/quality/catalog` (PyPI 430 загрузок/мес).
2. Поиск по живому registry: `agent-skills search <q> --remote` → канонический путь скилла.
3. Установка скиллов агенту: `git clone --depth 1 … ~/.claude/skills` или `npx agent-skills install <name>` (npm-CLI с fallback на shallow clone).
4. Чтение портала: index → вкладки Catalog/Roadmaps/Guides → страница скилла/трека/мапы (EN/RU-переключение).
5. Найм: hire.html → контакты + evidence grid, каждое заявление — живая ссылка.
6. Добавление нового скилла (автор): файлы → make validate/quality/catalog/sync-readme/docs → CI-гейты → main → автодеплой.
7. Добавление мапы: roadmaps/guides/*.md → build_docs рендерит + кросс-линкует с треком → consistency проверяет md↔html.
8. Ночной контроль: dependabot пушит бампы → CI полный → зелёный = merge.

## Инварианты (не ломать)
- Каждая пара `SKILL.md`/`SKILL.ru.md` валидна, секции 1:1, `name` = имени папки, без дубликатов.
- `docs/` — всегда консистентен с источниками (links, css/js пути, search-index = каталог, md↔html гайдов, roadmaps.json = tracks).
- README синхронен каталогу; строка Quality — бездатная (timezone-баг закрыт).
- Bilingual-механизм `data-slang-body` и i18n-паритет EN/RU ключей в `assets/site.js`.
- `roadmaps/*.json` проходят validate_roadmaps (live-трек: полный RU-зеркало, ≥2 item'а, без заглушек).
- Гейты CI ничего не отключают ради зелени; `--cov-fail-under=90`.

## Негласные решения автора (уважаю)
- **Hand-rolled валидаторы без внешних зависимостей** (только pyyaml/click/colorama) — портативность и нулевой supply-chain.
- **`assets/site.js` — единственный источник фронтенда**, страницы не дублируют JS; i18n — только в site.js.
- **Корневые `skills_catalog.json`/`quality-report.json` в .gitignore**, трекается только `docs/skills_catalog.json` — «generated не коммитится».
- **Вложенный `<a>` запрещён** в карточках (браузеры рвут вёрстку) — чипы в карточках это `<span>`.
- **Без-датная Quality-строка** — CI и локаль живут в разных таймзонах.
- **`labs/` не входит в CI-линт** — это боевые артефакты для копирования, не библиотечный код.
