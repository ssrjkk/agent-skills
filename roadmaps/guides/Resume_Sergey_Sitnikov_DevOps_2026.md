# Ситников Сергей Алексеевич
**Senior Fullstack & Systems Engineer · AI/ML & Autonomous Agents · DevOps/SRE**
📍 Санкт-Петербург · Полная занятость / Гибрид / Удалённо · Релокация: Москва, Кипр, Сербия, Беларусь, Латвия
📞 8 (900) 313-24-87 · ✉️ ray013lefe@gmail.com · 💬 Telegram: @ssrjkk · 🐙 github.com/ssrjkk · 🌐 ssrjkk.github.io
**Оформление:** ТК РФ или B2B (действующее ИП с октября 2026)

---

## Профиль
5,5 года в разработке и автоматизации. **23 open-source и коммерческих репозитория**, **9 опубликованных пакетов** (PyPI / GHCR / NPM), **1 600+ автотестов** в своих проектах, **1 800+ контрибуций** за год. Последние 2 года 9 месяцев — Senior QA Automation / SDET в amoCRM параллельно с собственной инженерной практикой: 23 системы, доведённые до продакшена, на Python, Go, C++20, Rust и TypeScript — с жёстким CI, санитайзерами памяти и покрытием до 98–100%.

---

## Коммерческий опыт

### amoCRM — Senior QA Automation / SDET (инженерная инфраструктура качества)
*январь 2024 — сентябрь 2026 (2 года 9 месяцев)*
- Ускорил полный регресс **в 8 раз** (с 4 часов до 30 минут).
- Повысил покрытие на **30%**: **100+ API-тестов** (pytest) и **170+ UI-тестов** (Playwright, Selenium, Page Object).
- Тестировал **DDD/BDD и CQRS-инварианты**, асинхронные пайплайны **Apache Kafka** (Eventual Consistency) в Kubernetes.
- Настроил инженерную инфраструктуру: **GitHub Actions, Docker, Kubernetes, Locust, Kibana, Grafana**.

---

## Инженерная практика (параллельно, с апреля 2021)
Как фулстек и системный инженер создал и вывел в продакшн **23 системы**. Избранные проекты по кластерам:

### Криптография, Web3 & Confidential ML
- **Shroud** — FHE-Appchain для приватного обучения ML-моделей: Rust-ноды, клиентское шифрование **FHEWasm**, контракты **Solidity (fhEVM)**, доказательства целостности **ZK-STARK**, пороговое дешифрование, VRF-комитет разрешения споров, полная Threat Model.
- **Tippy on Base** — некастодиальная ончейн-экономика: **ERC-4337** Account Abstraction, Paymaster (gasless USDC), ончейн-аттестация действий ИИ через **EAS**, протокол **x402** для M2M-платежей, MCP, **782 автотеста**.
- **Wake** — торговый терминал для zk-perp DEX Lighter: FastAPI + React + Telegram Mini App, LMSR-рынки предсказаний, копи-трейдинг, funding-арбитраж, **270+ автотестов**; реальный опыт с Hyperliquid (топ-32k глобального лидерборда).
- **Harvest v2.3.0** — асинхронный движок параллельного исполнения в EVM-сетях: кастомный workpool на aiohttp, анти-сибил поведенческая симуляция, sliding-window ротация RPC-нод без просадок RPS.

### AI / ML, Агентные системы & Formal Verification
- **Wake Up** — десктопный real-time AI-суфлёр: C++/Win32 лаунчер (MinGW, windres), стеклянный оверлей на Electron/Node 24 с честной альфа-прозрачностью и `WDA_EXCLUDEFROMCAPTURE`, двухрежимный захват звука (микрофонный VAD + перехват через VB-Cable), STT **OpenAI Whisper / Groq**, стриминг **Llama-3.3-70B** по SSE; **184 теста** node:test (≥98% line coverage) + **57 тестов** pytest (100% branch coverage).
- **agent-skills** — этот портал: **120 двуязычных (EN/RU) скиллов**, 20 доменов, **318+ тестов** (юнит / property-based / e2e), **95% покрытия**, CI-гейты (ruff, mypy, CodeQL), Python SDK + CLI в PyPI, GitHub Action, статический сайт с 27 полнотекстовыми мапами.
- **raven** — высоконагруженные RAG-микросервисы, MCP-сервер и мониторинг на Go, Python 3.12 и PostgreSQL.
- **noema** — автономный AI-агент с **формальной верификацией** решений через SMT-решатель **Z3**.
- **drafter** — Zero-Backend браузерный AI QA-комбайн (SQLite в WASM, роутинг 9+ LLM-провайдеров).

### Системное программирование & QA/SRE-платформы
- **Volley / cppload-pro** — движки нагрузочного тестирования на **C++20** (Boost.Beast/ASIO, двусторонний mTLS, Python SDK через pybind11, ASan/TSan, clang-tidy).
- **bothive** — оркестрация AI-воркеров и ботов (Telegram, Twitch, YouTube, X) на Node.js: RBAC, Circuit Breaker, SLO, Trivy, **Chaos Engineering в CI**.
- **Qualix / QA-Arsenal / QA-Helper / AmoCRM-Tests / Mobius** — платформы API/UI/Mobile-тестирования (Playwright, Locust, Appium, Allure, Quality Gates, Nightly Builds).

### Корпоративные SaaS & E-Commerce
- **Verso / Corvid CMS / Corvid CRM** — модульная Headless CMS на TypeScript, **Prisma 7** и **tRPC**: визуальный конструктор блоков, ревизии, API-ключи, SEO-инспектор, вебхук-синхронизация с CRM.
- **Shopwatch / Our-Jamon** — коммерческие E-Commerce платформы: Zero-CLS витрины, маппинг каталогов без коллизий, весовой/штучный расчёт, Telegram-боты, интеграция с **1С:УНФ 3.0**.

---

## Ключевые технические навыки
- **Языки:** Python 3.12, Go, C++20, Rust, TypeScript/JavaScript (Node.js 24, Electron), Solidity, SQL.
- **Backend & Архитектура:** FastAPI, aiohttp, Go-микросервисы, tRPC, Prisma 7, REST/gRPC/WebSockets/SSE, PostgreSQL, Redis, Kafka, SQLite (включая WASM), DDD/BDD/CQRS, интеграция **1С:УНФ 3.0**.
- **AI / ML & Audio DSP:** мультиагентные пайплайны, RAG (Go/Python), MCP, роутинг 9+ LLM (DeepSeek, GLM, Claude, GPT, Gemini, Groq/Llama-3.3-70B), vLLM, потоковый STT Whisper (VAD, VB-Cable, 16kHz PCM), формальная верификация через **Z3**.
- **Web3 & Криптография:** fhEVM/FHEWasm (гомоморфное шифрование), **ZK-STARK**, VRF-контракты, ERC-4337, Paymaster, EAS, x402, перп-DEX и L2 (Base, Lighter, Hyperliquid).
- **Инфраструктура, SRE & QA:** Docker, Kubernetes, Cilium (eBPF), Talos Linux, GitHub Actions, GitLab CI, ArgoCD, Chaos Engineering, Locust, Playwright, Pytest, Appium, node:test, Allure, Grafana, Kibana, ASan/TSan, clang-tidy, Ruff, mypy, CodeQL, Trivy, gitleaks.

---

## Образование
**ГУАП** (Санкт-Петербург) — Прикладная информатика, гр. 4411з, заочное отделение (ИНДО), выпуск 2028 — график полностью совместим с full-time занятостью.
**SHIFT Project** — курс Machine Learning (2026).
Расчётные работы (2026): системный анализ и теория надёжности — деревья неисправностей (FTA), графы Герца, матрицы инцидентности/контуров в NetworkX, схемы резервирования вычислителей.
**Английский:** B2 (160+ дней ежедневной практики).
