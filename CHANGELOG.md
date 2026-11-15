# Changelog

Формат: [Keep a Changelog](https://keepachangelog.com/). Версионирование: SemVer.

## [Unreleased]

### Added
- Career mode: открытая для рекрутёров страница `hire.html` (Person JSON-LD, evidence grid «каждое заявление — живая ссылка», три карьерных трека) + запись в sitemap (priority 1.0)
- Гейт уязвимостей зависимостей: `make audit` / CI-шаг `pip-audit -r requirements.txt` (на внедрении — чисто)
- `scripts/sync_npm.py`: синхронизация снапшота каталога в npm/ + семантическая проверка дрейфа + сверка версий pyproject ↔ npm/package.json
- Chaos Drill (Карты 20): автоматическая проверка Кейса 4 (NetworkPolicy) и итоговый exit-код лаборатории
- `docs/dev/`: UNDERSTANDING, AUDIT, PLAN, PROGRESS, REPORT — процессная документация

### Changed
- Библиотека: поле `models` нормализовано к единому набору (21 скилл; llm-finetuning имел только `[opus]`)
- gitlab-ci: пример privileged DinD заменён на rootless Kaniko (соответствие стандарту Карты 03)
- kubernetes / cloud-native-ai: пометки Gateway API (HTTPRoute) как преемника Ingress
- README: строка Quality синхронизируется замером из quality-report.json (97.5 avg / min 97, без даты — timezone-proof); Test coverage указан честно — 93% с гейтом ≥90%
- ROADMAP.md: актуализирован (120 skills / 20 domains / 97.5), история Shipped, план v4.3
- Резюме-мапа: синхронизирована с полным профилем (amoCRM SDET 2г9м, 23 репо, 9 пакетов); каждый названный проект ссылается на публичный GitHub
- npm-пакет: `install` падает назад на shallow clone репо, если в тарболе нет `skills/`

### Removed
- Дословные артефакты чата из публичной библиотеки мап (`00_CURRENT_CHAT…`, `00_DEVOPS_CHAT_CHRONICLE…`)
- Несуществующий проект из резюме (Wake Up — нет публичного репо) и фантомное заявление про тег `v1.0-legacy`

### Fixed
- npm-пакет: версия 3.4.0 → 4.1.1, манифест `files`, `install` с fallback, smoke-тест node:test, каталог-снапшот под CI-гейтом
- README: «Test coverage 100%» → измеренные 93%
- Мобильный overflow hire-страницы (120px на 360px) — поймано собственным Chromium-гейтом
- `.gitignore` без слэша молча исключал `npm/skills_catalog.json` — un-ignore
