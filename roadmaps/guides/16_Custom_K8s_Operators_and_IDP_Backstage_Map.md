# Карта 16: Разработка Kubernetes-операторов на Go (Kubebuilder) и Портал Backstage

На уровне Senior DevOps / Platform Engineer недостаточно просто писать YAML-манифесты для чужих операторов — нужно уметь расширять сам Kubernetes API под бизнес-логику компании.

---

## 1. Как работает Kubernetes Operator изнутри (`controller-runtime` / `Kubebuilder`)

Оператор состоит из двух частей:
1. **CRD (Custom Resource Definition):** схема нового объекта в Kubernetes API (например, `kind: MicroserviceApp` или `kind: PostgresDatabase`).
2. **Custom Controller:** приложение на Go, которое подписывается через Informer/Watch на события создания/изменения/удаления этого CRD и приводит реальное состояние кластера к желаемому (`Spec` -> `Status`).

### Главные правила написания контроллера (`Reconcile(ctx, req)`):
- **Идемпотентность:** функция `Reconcile` может вызываться десятки раз подряд для одного и того же объекта. Код обязан безопасно проверять: *«Существует ли уже дочерний Deployment? Если нет — создать, если его Spec отличается — обновить через Patch»*.
- **OwnerReferences (Сборка мусора):** при создании дочерних ресурсов (`Deployment`, `Service`) контроллер прописывает им в `metadata.ownerReferences` UID родительского CRD. Когда пользователь удалит CRD — Kubernetes сам каскадно удалит все дочерние объекты.
- **Finalizers (`metadata.finalizers`):** если при удалении CRD нужно сначала удалить внешний ресурс (например, бакет в S3 или БД в облаке), контроллер вешает на объект строчку-финализатор. Пока контроллер не удалит внешний ресурс и не снимет финализатор, объект в K8s не исчезнет из `etcd`.
- **Обработка ошибок и Requeue:** если произошла временная ошибка сети, `Reconcile` возвращает `ctrl.Result{}, err` — `controller-runtime` автоматически повторит попытку с экспоненциальной задержкой (Exponential Backoff).

---

## 2. Internal Developer Portal (IDP) на базе Backstage

**Backstage** (создан в Spotify, проект CNCF Incubation) решает главную боль больших команд: разработчик хочет выкатить новый сервис, но не хочет неделю ждать тикета от DevOps.

### Три главных модуля Backstage:
1. **Software Catalog (`catalog-info.yaml`):** единый реестр всех микросервисов, библиотек, баз данных и пайплайнов компании. Видно, какая команда владеет сервисом, ссылки на его дашборды в Grafana, статус в ArgoCD и алерты PagerDuty.
2. **Software Templates (Scaffolder):** мастер создания проектов («Golden Paths»). Разработчик вводит имя сервиса, выбирает язык (Go/Python) и галочку «Нужна БД PostgreSQL». Backstage сам:
   - Создает репозиторий из эталонного шаблона с настроенным `.gitlab-ci.yml` и `Dockerfile`.
   - Генерирует манифесты в GitOps-репозитории и регистрирует `Application` в ArgoCD.
   - Добавляет `PostgreSQLInstance` Claim для Crossplane.
3. **TechDocs (Docs-like-Code):** документация в Markdown лежит прямо в репозитории кода, а при пуше автоматически собирается через `mkdocs` и публикуется в красивом интерфейсе портала.
