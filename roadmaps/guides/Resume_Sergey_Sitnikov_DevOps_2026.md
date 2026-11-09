# Ситников Сергей Алексеевич
**DevOps / Platform / Infrastructure Engineer**
📍 Санкт-Петербург (Полная занятость / Гибрид / Удаленно)
📞 8 (900) 313-24-87

---

## Профиль
Инженер с выраженным аналитическим и структурным подходом к решению сложных инфраструктурных и архитектурных задач. Специализируюсь на контейнеризации, автоматизации CI/CD пайплайнов, построении надежной облачной и Kubernetes-инфраструктуры (IaC, GitOps, Observability) и обеспечении качества мультимодульных программных систем. Веду открытую инженерную экосистему с полным жизненным циклом: код → тесты → CI-гейты → деплой → наблюдаемость.

---

## Ключевые технические навыки (Hard Skills)
- **Контейнеризация и Оркестрация:** Docker (multi-stage, distroless, BuildKit, Docker Compose), containerd, Kubernetes (Deployment, StatefulSet, Probes, HPA, PDB, RBAC, NetworkPolicy, Gateway API), Helm, Kustomize.
- **CI/CD и GitOps:** GitHub Actions, GitLab CI (Kaniko, кэширование, матричные сборки), ArgoCD (App of Apps, ApplicationSet), Argo Rollouts.
- **Инфраструктура как код (IaC):** Terraform / OpenTofu (Remote State, модули), Terragrunt, Ansible (плейбуки харденинга, роли), Crossplane.
- **Наблюдаемость (Observability):** Prometheus, VictoriaMetrics (PromQL), Grafana (RED/USE дашборды), Grafana Loki, Vector, Alertmanager, OpenTelemetry.
- **Безопасность (DevSecOps):** HashiCorp Vault, External Secrets Operator, Trivy (сканирование образов и IaC), Gitleaks, Hadolint, Kyverno (Policy-as-Code).
- **Linux и Сети:** Linux Internals (cgroups v2, namespaces, systemd, sysctl тюнинг, lsof/iostat/vmstat/eBPF), стек TCP/IP, DNS, TLS/mTLS, Nginx, Envoy, балансировка нагрузки.
- **Программирование и СУБД:** Go (Golang), TypeScript/Node.js, Python, Bash (`set -euo pipefail`), PostgreSQL (Patroni/CloudNativePG, PgBouncer), Redis / Valkey.

---

## Инженерный опыт и проекты

### Мейнтейнер экосистемы agent-skills — библиотека AI-скиллов и портал обучения
*Open Source, единоличный архитектор и инженер (2026)*
- Выстроил библиотеку из **120 production-grade скиллов** в универсальном Agent Skills формате (EN + RU, 20 доменов) с автоматическими валидаторами качества и интероперабельности между агентами (Claude Code, OpenCode, Cursor, Windsurf).
- Спроектировал **CI-конвейер с тремя уровнями гейтов**: статический анализ (ruff, mypy — 0 замечаний), **318 автотестов** (юнит / property-based на Hypothesis / e2e-сборка / интеграционные), безопасность (CodeQL) — покрытие тестами **95%**, порог качества зашит в Makefile (`--cov-fail-under=90`).
- Собрал **статический портал на GitHub Pages**: вкладки-секции (каталог, роадмапы, библиотека мап), клиентский поиск, двуязычный интерфейс (EN/RU) с автоопределением языка, SEO (sitemap, JSON-LD, Open Graph) и автоматическим деплоем из main.
- Доведил до продакшена **27 полнотекстовых учебных мап** (DevOps, SRE, Platform Engineering, AI-Infra) с рендерингом markdown → HTML, кросс-ссылками трек ↔ мапа ↔ скилл и проверкой консистентности сайта в CI.

### Инженер по автоматизации сборки и тестирования — Проект «Shroud» (мультимодульная инфраструктурная и криптографическая платформа)
*2025 — 2026*
- Выстроил модульную архитектуру репозитория и автоматизировал прогон тестовых конвейеров в 4 ключевых пакетах системы, доведя общее покрытие до **320+ автотестов**:
  - `packages/contracts`: расширил и стабилизировал тестовый набор до **102 успешных тестов** (`npm test`).
  - `node`: реализовал и отладил **~165 модульных и интеграционных тестов** (`#[test]`-атрибутов) ядерного модуля.
  - `sdk` и `bot`: обеспечил покрытие клиентского SDK (**32 теста**) и сервисного бота (**22 теста**).
- Настроил воспроизводимую среду сборки и строгий контроль регрессий перед слиянием веток.

### DevOps / SRE архитектор — Production-Grade Cloud-Native & GitOps платформа (сквозной инфраструктурный стенд)
*2026*
- Разработал микросервис на **Go 1.23** со структурированным JSON-логированием (`slog`), сквозной трассировкой (`X-Trace-Id`), разделением проб `/healthz` и `/readyz` (с проверкой TCP-коннектов к PostgreSQL и Redis) и корректным **Graceful Shutdown** по `SIGTERM`.
- Упаковал сервис в защищенный multi-stage образ на базе `gcr.io/distroless/static-debian12:nonroot` (размер образа < 25 МБ, `readOnlyRootFilesystem`, сброс всех Linux capabilities).
- Реализовал конвейер CI/CD (**GitHub Actions / GitLab CI**) с автоматическим поиском утечек секретов (**Gitleaks**), линтингом (**Hadolint**) и блокировкой сборки при обнаружении CRITICAL-уязвимостей в **Trivy**.
- Спроектировал GitOps-доставку через **ArgoCD (`ApplicationSet`)** и прогрессивный Canary-деплой (**Argo Rollouts**) с автоматическим откатом по метрикам ошибок в Prometheus, а также внедрил Zero-Trust сетевые политики (`NetworkPolicy`) и правила **Kyverno**.
- Развернул полный стек наблюдаемости (**Prometheus + Grafana + Loki + Vector + Alertmanager**) и провел нагрузочное тестирование с помощью **Grafana k6** для валидации SLO (`p95 < 150ms`).

---

## Инфраструктурные лаборатории (публичные артефакты)
- **Chaos Drill** — лаборатория отказоустойчивости: `break-my-cluster.yaml` поднимает 4 сценария реальных отказов Kubernetes (OOMKilled, CrashLoopBackOff, NetworkPolicy blackhole, вытеснение подов), `verify-fixes.sh` автоматически верифицирует починку.
- **Bare-Metal Kubernetes** — кластер на Talos Linux с Cilium eBPF/BGP-пирингом, патчи control-plane, HA-конфигурация.
- **Stateful-стек** — CloudNativePG HA-кластер PostgreSQL и Kafka в режиме KRaft (Strimzi) с критериями готовности.
- **AI/GPU инфраструктура** — сервинг LLM в K8s (vLLM + NVIDIA GPU Operator), AI Gateway на Envoy + LiteLLM.

---

## Образование
**Санкт-Петербургский государственный университет аэрокосмического приборостроения (ГУАП)**, Санкт-Петербург
- Направление: **Прикладная информатика** (поступление: сентябрь 2024 г.)
