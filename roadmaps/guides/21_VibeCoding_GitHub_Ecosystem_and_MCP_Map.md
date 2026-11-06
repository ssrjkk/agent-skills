# Карта 21: Экосистема Вайбкодинга — 4 Главных Списка GitHub, MCP-серверы и Cursor Rules (2026–2027)

Эта карта объединяет ключевые курируемые репозитории GitHub (более 1,1 млн звёзд суммарно), которые заменяют десятки разрозненных туториалов и дают готовую инфраструктуру для разработки с ИИ-агентами.

---

## 1. Четыре базовых репозитория-списка для AI-кодера

| Репозиторий | Звёзды | Назначение в экосистеме `ssrjkk/agent-skills` и портала |
| :--- | :--- | :--- |
| **[codecrafters-io/build-your-own-x](https://github.com/codecrafters-io/build-your-own-x)** | ~556k+ | Пошаговые руководства по воссозданию технологий с нуля (свой браузер, БД, Docker, Git, нейросеть, компилятор, веб-сервер). База для модуля **«Обучение через сборку»** на портале. |
| **[public-apis/public-apis](https://github.com/public-apis/public-apis)** | ~492k+ | Коллективный каталог 1400+ бесплатных публичных API (погода, курсы валют, финансы, геоданные, фильмы, космос, книги). Готовое «топливо» для пет-проектов без долгой разработки бэкенда. |
| **[punkpeye/awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers)** | ~97k+ | Каталог серверов протокола **Model Context Protocol (MCP)**, через которые ИИ-агенты (Claude Code, Cursor, OpenCode, Raven) безопасно работают с почтой, Google Sheets, PostgreSQL/MySQL, Git и браузером. |
| **[PatrickJS/awesome-cursorrules](https://github.com/PatrickJS/awesome-cursorrules)** | ~41k+ | Библиотека готовых файлов правил `.cursor/rules` (`.mdc`) под конкретные фреймворки (Next.js, React 19, Astro, FastAPI, Go, Rust, Solidity, Tailwind). |

---

## 2. Как использовать эти списки на практике (Workflow вайбкодера)

- [ ] **Шаг 1. Выбор архитектуры и прототипа (`build-your-own-x`):**
  - Вместо пассивного чтения документации выбери технологию из [build-your-own-x](https://github.com/codecrafters-io/build-your-own-x) на нужном языке (Python, Go, Rust, TypeScript) и собери минимальное ядро за уикенд.
- [ ] **Шаг 2. Подключение реальных данных (`public-apis`):**
  - Подключи 1–2 бесплатных API из [public-apis](https://github.com/public-apis/public-apis) (проверь колонки `Auth`, `HTTPS` и `CORS`), чтобы пет-проект работал с живыми котировками, погодой или медиа-данными.
- [ ] **Шаг 3. Интеграция инструментов агента (`awesome-mcp-servers`):**
  - Подключи MCP-серверы для базы данных (`db-mcp-server`), таблиц (`mcp-gsheets`), почты (`MCPEmails`) или собственного шлюза (`raven-mcp`), чтобы агент сам проверял схему БД и прогонял запросы.
- [ ] **Шаг 4. Фиксация стандартов кода (`awesome-cursorrules` + `ssrjkk/agent-skills`):**
  - Положи правила `.cursor/rules/*.mdc` и двуязычные скиллы `SKILL.md` / `SKILL.ru.md` в корень проекта, чтобы ИИ-агент с первого промпта писал типобезопасный код без техдолга.
