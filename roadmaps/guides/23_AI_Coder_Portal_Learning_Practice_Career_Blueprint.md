# Карта 23: Архитектура Портала «Обучение — Практика — Работа для кодеров с AI» (на базе `ssrjkk/agent-skills`)

Этот документ описывает концепцию, архитектуру и дорожную карту запуска единого портала для разработчиков, использующих ИИ-агентов, на фундаменте репозитория **[ssrjkk/agent-skills](https://github.com/ssrjkk/agent-skills)** (`agent-skills-library`).

---

## 1. Главная идея и ценность портала (Value Proposition)

Современный разработчик тонет в разрозненных промптах, гайдах и пустых вайбкод-шаблонах, которые падают в продакшене и не индексируются поисковиками. Портал соединяет **три этапа роста инженера в одном месте**:

1. **ОБУЧЕНИЕ (Learn & Roadmaps):**
   - Структурированные дорожные карты **01–23** (от Linux Internals, Go/Python, Kubernetes, Bare-Metal Talos/Cilium и AI/GPU-инфраструктуры до Вайбкодинга и SEO).
   - Интеграция с курируемыми списками ([build-your-own-x](https://github.com/codecrafters-io/build-your-own-x), [public-apis](https://github.com/public-apis/public-apis), [awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers), [awesome-cursorrules](https://github.com/PatrickJS/awesome-cursorrules)).
2. **ПРАКТИКА И ИНСТРУМЕНТЫ (Build & Agent Skills):**
   - Библиотека из **110+ двуязычных (EN + RU) скиллов уровня Grade A** (`SKILL.md` / `SKILL.ru.md`) для Claude Code, Cursor, Windsurf, OpenCode и [ssrjkk/raven](https://github.com/ssrjkk/raven).
   - Интерактивные тренажеры и полигоны: **Chaos Drill Lab** (`break-my-cluster.yaml` + `verify-fixes.sh`), **Vibe-SEO & Zero-CLS чек-лист** и готовые продакшн-манифесты (vLLM, Envoy AI Gateway + LiteLLM, CloudNativePG, Kafka KRaft, ClickHouse).
3. **РАБОТА И КАРЬЕРА (Career & Job Hub):**
   - Конструктор инженерного резюме по формуле **XYZ** (*«Достиг [X], измеряемого в [Y], за счет внедрения [Z]»*) из Карты 15.
   - Тренажер технических собеседований и System Design (10k+ RPS, Multi-Region, RTO/RPO) из Карт 08 и 11.
   - Карьерный трекер прогресса (`DevOps_Career_Tracker_2026.xlsx` + веб-трекер в `localStorage`) и витрина проверенных пет-проектов для работодателей.

---

## 2. Техническая архитектура портала

```
┌───────────────────────────────────────────────────────────────────────────┐
│        Frontend Портала (Next.js / Astro / Static Prerendered HTML)       │
│  SEO 100/100 · Open Graph · sitemap.xml · robots.txt · Zero-CLS · WebP   │
├───────────────────────┬───────────────────────────┬───────────────────────┤
│   Модуль 1: ОБУЧЕНИЕ  │  Модуль 2: СКИЛЛЫ & ЛАБЫ  │   Модуль 3: КАРЬЕРА   │
│  • Карты 01–23 (MD)   │  • 110+ SKILL.md (EN/RU)  │  • Тренажер Q&A       │
│  • Build-Your-Own-X   │  • Awesome MCP & Cursor   │  • Генератор XYZ CV   │
│  • Трекер прогресса   │  • Chaos Lab K8s & SEO    │  • Матрица грейдов    │
└───────────┬───────────┴─────────────┬─────────────┴───────────┬───────────┘
            │                         │                         │
            ▼                         ▼                         ▼
┌───────────────────────────────────────────────────────────────────────────┐
│         Ядро данных и CLI: репозиторий ssrjkk/agent-skills (PyPI)         │
│  • Пакет: pip install agent-skills-library                                │
│  • Валидация CI: Python 3.9–3.13 + проверка структуры SKILL.md            │
│  • Интеграция с автономным агентом ssrjkk/raven (raven-mcp, 66 тулов)     │
└───────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Дорожная карта запуска портала (4 спринта)

- [ ] **Спринт 1 (Контентное ядро в `ssrjkk/agent-skills`):**
  - Добавить в репозиторий новые двуязычные скиллы (`vibe-seo-audit`, `catalog-photo-mapper`, `vibe-shop-normalizer`, `linux-ebpf-troubleshooting`, `ci-cd-gitops-iac`, `k8s-baremetal-multicluster`, `ai-gpu-infra-llmops`, `observability-sre-highload`, `ai-coder-career-architect`).
  - Разместить папки `roadmaps/` (Карты 01–23) и `labs_and_manifests/` (боевые манифесты и полигон поломок).
- [ ] **Спринт 2 (Веб-витрина портала на GitHub Pages / собственной доменной зоне):**
  - Задеплоить пререндеренный лендинг-портал (`portal/index.html`, `sitemap.xml`, `robots.txt`, `portal-catalog.json`) с поиском по скиллам, фильтрацией карт по грейдам (Junior -> Middle -> Senior -> Principal) и интерактивным чек-листом прогресса.
- [ ] **Спринт 3 (Интерактивные песочницы и ИИ-ревьюер через `ssrjkk/raven`):**
  - Подключить бота `@ssrjkk_bot` / шлюз `RavenFlow` для автоматического аудита GitHub-репозиториев студентов (проверка SEO, Dockerfile, K8s-манифестов и резюме по формуле XYZ).
- [ ] **Спринт 4 (Карьерный хаб и матчинг):**
  - Запуск публичных профилей выпускников с верифицированными бейджами пройденных лаб (`Chaos Drill Passed`, `Vibe-SEO 95+`, `K8s Operator Built`) и доски вакансий для AI-Native / DevOps / Platform инженеров.
