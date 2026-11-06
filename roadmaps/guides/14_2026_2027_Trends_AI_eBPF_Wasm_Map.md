# Карта 14: Главные тренды DevOps / SRE / Platform Engineering на 2026–2027 годы

Индустрия в 2026–2027 годах сместилась от ручной сборки YAML-пайплайнов к **eBPF-телеметрии без изменения кода**, **оркестрации AI/GPU-нагрузок**, **Sidecarless Service Mesh** и **отказу от проприетарного вендор-лока (OpenTofu, Valkey, OpenBao)**.

---

## 1. AI-Native Infrastructure & GPU Orchestration (AI Infrastructure / LLMOps)
Сегодня почти каждая компания внедряет локальные LLM, RAG-пайплайны или векторные БД, и эксплуатировать их в Kubernetes приходится DevOps/Platform-инженерам.

- [ ] **Оркестрация GPU в Kubernetes:**
  - **NVIDIA GPU Operator** и **DRA (Dynamic Resource Allocation)** в Kubernetes 1.31–1.32+: гибкое распределение GPU между подами.
  - Разделение одной физической видеокарты между несколькими подами: **MIG (Multi-Instance GPU)** для аппаратной изоляции и **Time-Slicing** / **MPS** для тестовых контуров.
- [ ] **Сервинг моделей и AI Gateway:**
  - Запуск высокопроизводительных инференс-движков: **vLLM**, **Triton Inference Server**, **KServe** или **Ollama**.
  - Масштабирование до нуля (Scale-to-Zero) через **KEDA** или **Knative** (чтобы дорогие GPU-ноды не простаивали без трафика) и быстрый старт узлов через **Karpenter**.
  - **AI Gateways (Envoy AI Gateway, LiteLLM, Kong AI):** единый шлюз перед LLM для подсчета токенов, Rate Limiting по расходу токенов, кэширования промптов (Semantic Caching) и фоллбэка между моделями.
- [ ] **Векторные хранилища в продакшене:**
  - Эксплуатация **Qdrant**, **Milvus** или расширений **pgvector** в PostgreSQL (индексы HNSW, требования к RAM и IOPS).

---

## 2. Четвертый столп Observability: Continuous Profiling и eBPF Zero-Code
Помимо классических **Метрик**, **Логов** и **Трейсов**, в 2026–2027 году стандартом стал четвертый сигнал — **Непрерывное профилирование (Continuous Profiling)**.

- [ ] **Continuous Profiling (Grafana Pyroscope / Parca):**
  - Снятие **FlameGraphs** (профилей потребления CPU и аллокаций памяти) со всех подов в продакшене непрерывно через eBPF с накладными расходами < 1–2%.
  - Позволяет найти конкретную строчку кода и функцию, вызвавшую спайк CPU или утечку памяти, даже если под уже перезапустился.
- [ ] **Zero-Code Auto-Instrumentation (Grafana Beyla / OTel eBPF):**
  - Сбор RED-метрик и распределенных трейсов OpenTelemetry напрямую из ядра Linux через eBPF (перехват системных вызовов сокетов и TLS-хендшейков) **вообще без подключения SDK и изменения исходного кода** на Go, Rust, C++ или Python.

---

## 3. Смерть сайдкаров: Sidecarless Service Mesh (Cilium & Istio Ambient)
Классический Service Mesh со вставкой Envoy-контейнера в каждый под (Sidecar pattern) уходит в прошлое из-за огромного оверхеда по памяти и задержкам.

- [ ] **Cilium Service Mesh / Istio Ambient Mode:**
  - Шифрование межсервисного трафика (**mTLS / WireGuard**) и L4-политики работают прямо в ядре на уровне ноды через **eBPF**, а L7-проксирование запускается как общий ресурс на узле (Per-Node Proxy / ztunnel), экономя до 50% RAM кластера.
- [ ] **Gateway API v1.1+ как единый стандарт:**
  - Полный переход с устаревшего `Ingress` на `Gateway`, `HTTPRoute`, `GRPCRoute` и `TLSRoute` (единый API и для входящего трафика North-South, и для межсервисного трафика East-West — паттерн **GAMMA**).

---

## 4. Великая Open-Source Миграция (Post-BSL Era)
После изменения лицензий HashiCorp и Redis стандартный стек инструментов в 2026–2027 году обновился:

| Старый стандарт | Новый Open-Source стандарт (Linux Foundation / CNCF) | Что изменилось на практике |
| :--- | :--- | :--- |
| **Terraform** | **OpenTofu** | Полная совместимость + встроенное шифрование стейта на клиенте (Client-side State Encryption) и `for_each` для провайдеров. |
| **Redis** | **Valkey** | Форк под эгидой Linux Foundation (поддержан AWS, GCP, Oracle), улучшенная многопоточность и работа с памятью. |
| **HashiCorp Vault** | **OpenBao** (или облачный KMS + ESO) | Полностью открытый форк Vault без лицензионных ограничений BSL. |

---

## 5. Программируемый CI/CD (Dagger) и WebAssembly (Wasm)
- [ ] **Dagger (CI/CD как код вместо YAML):**
  - Отказ от тысяч строк нетестируемого YAML-кода в пользу пайплайнов, написанных на **Go, Python или TypeScript**, которые выполняются в контейнерах BuildKit одинаково на ноутбуке разработчика и в любом CI-раннере.
- [ ] **WebAssembly (Wasm) на сервере (SpinKube / Wasmtime / containerd-shim-spin):**
  - Запуск легковесных бессерверных функций в Kubernetes в виде Wasm-модулей: холодный старт за **1–2 миллисекунды** (вместо секунд у контейнеров) и размер артефакта в пару мегабайт.
