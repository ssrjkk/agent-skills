# Карта 15: Эталонное Резюме DevOps / SRE и Оформление Инженерного Портфолио (2026–2027)

На современном рынке труда HR-фильтры (ATS) и тимлиды отсеивают резюме со списками обязанностей («настраивал CI/CD, писал Dockerfile»). В резюме должны быть **инженерные результаты в цифрах** по формуле **XYZ**: *«Достиг [X], измеряемого в [Y], за счет внедрения [Z]»*.

---

## 1. Примеры сильных формулировок для резюме (Бери и адаптируй)

### CI/CD и Контейнеризация:
- *Слабо:* «Писал Dockerfile и настраивал пайплайны в GitHub Actions / GitLab CI».
- **Сильно (Middle/Senior):** «Оптимизировал CI/CD пайплайны для 15+ микросервисов (переход на multi-stage `distroless` образы, кэширование слоев BuildKit и параллельные матрицы тестов), сократив время сборки и доставки релиза **с 24 до 5 минут** и уменьшив размер продакшн-образов **на 75% (с 420 МБ до 35 МБ)**».

### Kubernetes, GitOps и Надежность:
- *Слабо:* «Администрировал кластер Kubernetes и деплоил через ArgoCD».
- **Сильно (Middle/Senior):** «Внедрил декларативную доставку по модели GitOps (**ArgoCD ApplicationSet + Argo Rollouts Canary**) с автоматическим откатом по метрикам Prometheus, что позволило увеличить частоту релизов **в 3 раза** и снизить число инцидентов при выкатке **до нуля (SLO доступности 99.95%)**».

### Наблюдаемость и Траблшутинг:
- *Слабо:* «Настраивал мониторинг в Prometheus и Grafana».
- **Сильно (Middle/Senior):** «Спроектировал единый стек наблюдаемости (**VictoriaMetrics + Grafana + Loki + Vector + OpenTelemetry**) с алертингом по методу RED и скоростью сжигания Error Budget, сократив среднее время обнаружения инцидентов (**MTTD**) **с 25 до 2 минут**».

### Инфраструктура как код и FinOps:
- *Слабо:* «Поднимал инфраструктуру через Terraform и Ansible».
- **Сильно (Middle/Senior):** «Перевел облачную инфраструктуру на модульный **Terraform/OpenTofu + Terragrunt** и внедрил автомасштабирование узлов кластера через **Karpenter (Spot + Consolidation)**, сократив ежемесячный счет за облако **на 42% без потери производительности**».

---

## 2. Готовый каркас резюме (Markdown-шаблон)

```markdown
# Имя Фамилия
**DevOps / SRE / Platform Engineer**
📍 Санкт-Петербург (Гибрид / Удаленно) | 📞 +7 (900) 000-00-00 | ✉️ email@example.com | 🔗 GitHub / Telegram

## Технический стек (Core Skills)
- **Orchestration & Cloud-Native:** Kubernetes, Helm, Kustomize, Cilium (eBPF), Gateway API, Karpenter, KEDA, Docker, containerd.
- **CI/CD & GitOps:** GitLab CI, GitHub Actions, ArgoCD, Argo Rollouts, Kaniko, BuildKit.
- **IaC & Configuration:** Terraform / OpenTofu, Terragrunt, Ansible, Packer, Crossplane.
- **Observability:** Prometheus, VictoriaMetrics, Grafana, Loki, Vector, OpenTelemetry, Pyroscope, Alertmanager.
- **DevSecOps & Networking:** HashiCorp Vault / ESO, Trivy, Kyverno, Gitleaks, Linux Internals (cgroups v2, namespaces, sysctl), TCP/IP, Nginx, Envoy, TLS/mTLS.
- **Scripting & Databases:** Go (Golang), Python, Bash, PostgreSQL (Patroni/CloudNativePG, PgBouncer), Redis/Valkey, Kafka.

## Опыт работы / Инженерные проекты
**[Название Компании / Проекта]** — *DevOps Engineer* (Период)
- Спроектировал и автоматизировал отказоустойчивую инфраструктуру в Kubernetes с использованием **Terraform** и **ArgoCD (App of Apps)**.
- Внедрил конвейер DevSecOps (**Gitleaks, Hadolint, Trivy, Kyverno Policy-as-Code**), заблокировав попадание критических уязвимостей и контейнеров с правами `root` в продакшн.
- Настроил изоляцию трафика по стандарту Zero-Trust (`NetworkPolicy`) и безопасную доставку секретов из **Vault** через **External Secrets Operator**.
- Разработал и покрыл тестами сервисные модули и инфраструктурные компоненты (100+ автотестов в пайплайне), обеспечив предсказуемость релизов.
```
