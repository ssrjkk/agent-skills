# Карта 05 (Расширенная): Observability и DevSecOps

## 1. Мониторинг и Сбор Метрик
- [ ] **Концепции и методологии:**
  - **Four Golden Signals** (Задержка, Трафик, Ошибки, Насыщение).
  - **RED** (Rate, Errors, Duration — для микросервисов) и **USE** (Utilization, Saturation, Errors — для аппаратных ресурсов).
- [ ] **Prometheus и VictoriaMetrics:**
  - Архитектура сбора данных (Pull-модель), декларативный Service Discovery в Kubernetes через `ServiceMonitor` и `PodMonitor` (стек `kube-prometheus-stack`).
  - Типы метрик: `Counter` (счетчик), `Gauge` (текущее значение), `Histogram` (распределение по бакетам), `Summary`.
  - **PromQL на практике:** использование функций `rate()` и `irate()`, агрегации `sum by ()`, расчет перцентилей (p95, p99) через функцию `histogram_quantile()`.
  - Масштабирование хранения метрик: **VictoriaMetrics** (Single/Cluster) или **Thanos** / **Mimir** для долгосрочного хранения и федерации.
- [ ] **Визуализация и Уведомления:**
  - **Grafana:** проектирование дашбордов, использование переменных, смешанных источников данных, автоматический provisioning дашбордов через файлы конфигурации (As-Code).
  - **Alertmanager:** логика дедупликации, группировки, подавления алертов (`inhibit_rules`) и маршрутизации нотификаций в Telegram, Slack, PagerDuty. Борьба с Alert Fatigue.

## 2. Централизованные логи и Трассировка
- [ ] **Логирование:**
  - Требования к структурированным логам (формат JSON с обязательными полями `timestamp`, `level`, `trace_id`, `service`, `message`).
  - Современный легковесный стек: **Grafana Loki** + агенты **Vector** / **Fluent Bit** (индексация только метаданных-лейблов, высокая скорость и низкое потребление RAM, язык запросов **LogQL**).
  - Полнотекстовый поиск под высокую нагрузку: стек **OpenSearch** / **ELK**.
- [ ] **Распределенная трассировка (Distributed Tracing):**
  - Стандарт **OpenTelemetry (OTel):** настройка OTel Collector, автоматическая и ручная инструментация кода приложений, передача контекста трассировки через HTTP-заголовки (W3C Trace Context).
  - Бэкенды хранения и анализа трейсов: **Grafana Tempo** или **Jaeger**. Связывание метрик, логов и трейсов через сквозной `trace_id`.

## 3. DevSecOps и Управление Секретами
- [ ] **Безопасное хранение секретов:**
  - Почему хранение паролей и токенов в Git запрещено.
  - **HashiCorp Vault:** секретные движки (KV v2, PKI, Database dynamic credentials), аутентификация клиентов через Kubernetes Auth Method / OIDC.
  - Синхронизация секретов в Kubernetes: **External Secrets Operator (ESO)** или инструменты шифрования манифестов в репозитории (**SOPS** / **Sealed Secrets**).
- [ ] **Безопасность цепочки поставок (Supply Chain Security):**
  - Сканирование репозиториев на утечки паролей и ключей с помощью **Gitleaks** и `trufflehog`.
  - Анализ контейнеров, файловой системы и IaC на уязвимости с помощью **Trivy** или `Grype`.
  - Статический анализ кода (SAST) через **SonarQube**, управление зависимостями (Dependabot / Renovate), генерация **SBOM** (Software Bill of Materials) и цифровая подпись образов через **Cosign**.
- [ ] **Безопасность кластера Kubernetes:**
  - Настройка **RBAC** (Principle of Least Privilege: избегание использования `cluster-admin` для приложений).
  - Применение **Pod Security Standards** (профили `Privileged`, `Baseline`, `Restricted`).
  - Policy as Code: использование **Kyverno** или **OPA Gatekeeper** для автоматического отклонения манифестов (например, запрет образов с тегом `:latest`, проверка наличия лимитов ресурсов, запрет запуска от root).
  - Runtime-безопасность: **Falco** или **Tetragon** для детекции подозрительной активности на основе eBPF.
