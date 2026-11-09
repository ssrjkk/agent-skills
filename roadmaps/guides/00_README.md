# Полный сборник DevOps / SRE / Platform Engineering (v9 — 2026–2027 Ultimate Principal Edition)

Этот архив — полная энциклопедия, кодовая база, лаборатория траблшутинга и набор продакшн-манифестов уровня **Junior -> Middle -> Senior -> Staff / Principal Platform Engineer (2026–2027)**.

## Полная структура архива (Карты 01–20)

1. **`01_Linux_and_Networking_Map.md`** — Ядро Linux (cgroups v2, namespaces), траблшутинг (USE/RED, eBPF), сетевой стек и прокси (Nginx, Envoy).
2. **`02_Coding_and_Containers_Map.md`** — Автоматизация на Python (`uv`) и Go, архитектура OCI-рантаймов (`containerd`, `runc`), OverlayFS, оптимизация и безопасность Dockerfile.
3. **`03_CI_CD_and_IaC_Map.md`** — Пайплайны (GitLab CI, GitHub Actions), OpenTofu/Terraform, Terragrunt, Ansible и GitOps (ArgoCD, Argo Rollouts).
4. **`04_Kubernetes_and_Cloud_Map.md`** — Control Plane K8s, CNI Cilium (eBPF), Gateway API, шедулинг, автомасштабирование (Karpenter, KEDA) и облака.
5. **`05_Observability_and_DevSecOps_Map.md`** — Prometheus/VictoriaMetrics, PromQL, Grafana, Loki/Vector, OpenTelemetry, HashiCorp Vault / OpenBao, Trivy и Kyverno.
6. **`06_SRE_and_Platform_Engineering_Map.md`** — SLI/SLO, Error Budgets, Chaos Engineering, Platform Engineering (Crossplane, Backstage), Highload БД (CloudNativePG, Patroni, Valkey, Kafka) и FinOps.
7. **`07_Pet_Project_Blueprint.md`** — Пошаговое техническое задание для сквозного продакшн пет-проекта.
8. **`08_Interview_Prep_Q_and_A.md`** — Разбор главных технических вопросов на собеседованиях (Junior / Middle / Senior).
9. **`09_Incident_Troubleshooting_Playbooks.md`** — Алгоритмы действий при авариях (`CrashLoopBackOff`, `OOMKilled`, `502/504`, `nf_conntrack`).
10. **`10_Database_and_Stateful_Runbooks.md`** — Практическая эксплуатация PostgreSQL, Valkey/Redis и Kafka в продакшене.
11. **`11_System_Design_for_DevOps_SRE.md`** — Проектирование отказоустойчивых архитектур (10k+ RPS, Multi-Region, RTO/RPO).
12. **`12_Postmortem_and_SLO_Templates.md`** — Шаблон Blameless Postmortem и калькулятор SLO / Error Budget.
13. **`13_Cloud_Security_IAM_and_FinOps_Map.md`** — OIDC, IRSA/Pod Identity, Supply Chain (SBOM, Cosign) и FinOps (OpenCost, Goldilocks).
14. **`14_2026_2027_Trends_AI_eBPF_Wasm_Map.md`** — Главные тренды 2026–2027: GPU/LLM-инфраструктура в K8s, Continuous Profiling (Pyroscope), Sidecarless Ambient Mesh, OpenTelemetry Auto-Instrumentation (Beyla), Dagger и WebAssembly.
15. **`15_DevOps_Resume_and_Portfolio_Guide.md`** — Готовый шаблон резюме DevOps/SRE (ATS-friendly) с оцифрованными достижениями и чек-лист оформления инженерного GitHub-профиля.
16. **`16_Custom_K8s_Operators_and_IDP_Backstage_Map.md`** — Разработка собственных Kubernetes-операторов на Go (`Kubebuilder` / `controller-runtime`), устройство Reconciliation Loop, Finalizers и создание шаблонов самообслуживания в **Backstage**.
17. **`17_BareMetal_K8s_Talos_and_Cilium_BGP_Map.md`** — Современный Bare-Metal и On-Premise Kubernetes: неизменяемая ОС **Talos Linux**, анонсы IP-адресов по **BGP в Cilium**, распределенные хранилища **Rook-Ceph / Longhorn / TopoLVM**.
18. **`18_MultiCluster_Federation_and_Global_Traffic_Map.md`** *(Новое в v9!)* — Мульти-кластерная архитектура: **Cilium Cluster Mesh**, **vCluster** (виртуальные кластеры для PR-окружений), **Cluster API (CAPI)** и глобальная балансировка трафика (**GSLB / ExternalDNS**).
19. **`19_Data_Streaming_Kafka_ClickHouse_and_Lakehouse_Map.md`** *(Новое в v9!)* — Эксплуатация аналитических и стриминговых платформ в K8s: **ClickHouse** (Altinity Operator, шардирование, ClickHouse Keeper), **Apache Kafka в режиме KRaft** (без ZooKeeper, Strimzi) и **MinIO / Ceph RGW**.
20. **`20_HandsOn_Troubleshooting_Simulator_Guide.md`** *(Новое в v9!)* — Практический тренажер инженера: 4 сценария намеренно сломанной инфраструктуры с пошаговой методикой расследования и автопроверкой.

### Новые боевые комплекты манифестов в v9:
- **`baremetal_and_ha_db_pack/`** — Полный комплект манифестов для Bare-Metal и отказоустойчивых баз:
  - `talos-controlplane-patch.yaml` — Конфигурация узла **Talos Linux** (отключение kube-proxy для работы Cilium eBPF, шифрование диска, тюнинг sysctl).
  - `cilium-bgp-peering.yaml` — Анонс сервисов `LoadBalancer` по протоколу **BGP** на физические роутеры (`CiliumBGPPeeringPolicy` + `CiliumLoadBalancerIPPool`).
  - `cloudnativepg-ha-cluster.yaml` — Отказоустойчивый кластер **PostgreSQL 16 (CloudNativePG)**: 3 ноды, синхронная репликация, пулер **PgBouncer** и непрерывный бэкап WAL в S3.
  - `kafka-kraft-strimzi.yaml` — Современный кластер **Apache Kafka (KRaft mode без ZooKeeper)** под управлением оператора **Strimzi**.
- **`troubleshooting_lab/`** — Интерактивный полигон поломок:
  - `break-my-cluster.yaml` — Манифест, создающий неймспейс `chaos-drill` с 4 реальными продакшн-багами (сломанный сетевой полиси, OOM/Liveness ловушка, ошибка прав в ReadOnlyRootFS, фантомный Service selector).
  - `verify-fixes.sh` — Скрипт автопроверки, который тестирует, все ли 4 поломки ты успешно нашел и починил.
