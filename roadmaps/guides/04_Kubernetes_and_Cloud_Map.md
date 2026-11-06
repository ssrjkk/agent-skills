# Карта 04 (Расширенная): Kubernetes и Облачная Архитектура

## 1. Архитектура Kubernetes (Под капотом)
- [ ] **Control Plane компоненты:**
  - `kube-apiserver`: центральная точка входа, аутентификация, авторизация (RBAC), обработка запросов через Mutating и Validating Admission Webhooks.
  - `etcd`: распределенное KV-хранилище на базе алгоритма Raft. Процедура снятия снапшотов (`etcdctl snapshot save`), восстановление кластера (`snapshot restore`) и мониторинг задержек записи (`fsync`).
  - `kube-scheduler`: алгоритмы фильтрации (Filtering) и взвешивания/оценки (Scoring) нод для размещения подов.
  - `kube-controller-manager`: набор контроллеров (Node Controller, ReplicaSet Controller, Endpoint Controller), реализующих цикл реконсиляции (Reconciliation Loop).
- [ ] **Worker Node компоненты:**
  - `kubelet`: агент ноды, общающийся с Container Runtime через CRI, управление жизненным циклом подов, запуск статических подов (Static Pods).
  - `kube-proxy`: поддержка сетевой абстракции сервисов (iptables, IPVS режимы, либо полное отключение при использовании eBPF CNI).

## 2. Рабочие нагрузки и управление размещением
- [ ] Жизненный цикл `Pod`, использование `initContainers` для подготовки окружения, `ephemeralContainers` для отладки работающих подов без перезапуска (`kubectl debug`).
- [ ] Контроллеры: `Deployment`, `StatefulSet` (гарантии стабильных сетевых имен через Headless Service и постоянных дисков для БД), `DaemonSet` (деплой агентов мониторинга/логирования на каждую ноду), `Job` / `CronJob`.
- [ ] **Надежность и отказоустойчивость:**
  - Пробы состояния: `startupProbe` (для тяжелых приложений), `livenessProbe` (перезапуск зависшего контейнера), `readinessProbe` (исключение не готового принимать трафик пода из Endpoints).
  - Ресурсы и изоляция: настройка `resources.requests` (используется шедулером для выделения места) и `resources.limits` (жесткое ограничение cgroups: троттлинг CPU и OOM Kill по памяти). Классы QoS: `Guaranteed`, `Burstable`, `BestEffort`.
- [ ] **Продвинутый шедулинг:**
  - Размещение подов: `nodeSelector`, `Node Affinity`, `Pod Affinity` и `Pod Anti-Affinity` (разнос критических реплик по разным стойкам/нодам).
  - Ограничения и вытеснение: `Taints & Tolerations`, `Topology Spread Constraints`.
  - Обеспечение плавных обновлений: **`PodDisruptionBudget` (PDB)** для гарантии минимального количества доступных подов при обслуживании нод, хук `preStop` и `terminationGracePeriodSeconds` для корректного завершения активных соединений.

## 3. Сеть и Хранение в Kubernetes
- [ ] **Сетевые плагины (CNI):**
  - **Cilium**: высокая производительность на базе eBPF, замена `kube-proxy`, L7 сетевые политики, прозрачное шифрование трафика между нодами через WireGuard, инструмент визуализации Hubble.
  - **Calico**: работа в режимах BGP routing или инкапсуляции IPIP/VXLAN, сетевые политики.
- [ ] **Сетевые абстракции:**
  - Типы сервисов: `ClusterIP`, `Headless Service`, `NodePort`, `LoadBalancer`.
  - Входящий трафик: классический `Ingress` (контроллеры вроде `ingress-nginx`) и современный стандарт **Gateway API** (`GatewayClass`, `Gateway`, `HTTPRoute` с поддержкой разделения трафика и фильтрации).
  - Изоляция: `NetworkPolicy` (создание политики по умолчанию `Default Deny` и открытие разрешенных направлений).
  - `CoreDNS`: тюнинг и кэширование запросов (`NodeLocal DNSCache`), борьба с проблемой `ndots:5`.
- [ ] **Хранение данных (Storage):**
  - Абстракции `PersistentVolume` (PV), `PersistentVolumeClaim` (PVC), `StorageClass`. Динамический провижининг дисков через интерфейс **CSI** (Container Storage Interface), снятие снапшотов томов.

## 4. Шаблонизация и Автомасштабирование
- [ ] **Helm и Kustomize:**
  - Создание собственных Helm-чартов: структура `Chart.yaml`, `values.yaml`, шаблонизатор Go templates, использование вспомогательных шаблонов (`helpers.tpl`), хуки и управление зависимостями.
  - Управление конфигурациями без шаблонизации через **Kustomize** (пакеты `base` и окружения `overlays`, патчи манифестов).
- [ ] **Автомасштабирование:**
  - Горизонтальное масштабирование подов: `HPA` (на базе метрик CPU/Memory или кастомных метрик Prometheus).
  - Масштабирование по внешней очереди: **KEDA** (Kubernetes Event-driven Autoscaling — масштабирование по количеству сообщений в Kafka, RabbitMQ или RPS в HTTP-сервере).
  - Масштабирование узлов кластера: **Karpenter** (быстрый провижининг инстансов под требования подов) или стандартный `Cluster Autoscaler`.

## 5. Облачные провайдеры (AWS / GCP / Yandex Cloud)
- [ ] Управление доступом (IAM): принцип наименьших привилегий, интеграция ролей облака с сервисными аккаунтами Kubernetes (AWS IRSA / Pod Identity, GCP Workload Identity).
- [ ] Проектирование сети в облаке: топология VPC (публичные/приватные подсети), NAT Gateway, VPC Peering, Transit Gateway, настройка балансировщиков (ALB/NLB).
- [ ] Управляемые сервисы: объектное хранилище S3 (политики доступа, правила жизненного цикла), управляемые базы данных (Managed PostgreSQL), службы управления ключами шифрования (KMS).
