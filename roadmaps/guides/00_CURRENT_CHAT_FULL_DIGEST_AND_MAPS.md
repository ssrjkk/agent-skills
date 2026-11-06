# Полная сводка текущего чата: Вайбкодинг, SEO, Скиллы и Карты 01–23 для `ssrjkk/agent-skills`

Этот файл объединяет **всю информацию из нашего текущего диалога** в структурированном виде, чтобы вы могли легко переносить блоки, таблицы, промпты, дорожные карты и скиллы в свой существующий сайт и репозиторий [**ssrjkk/agent-skills**](https://github.com/ssrjkk/agent-skills).

## Блок 1. Разбор Видео №1 — 4 главных репозитория-списка на GitHub для вайбкодера

В этих репозиториях нет готовых программ (0 строк кода), но собраны курируемые списки ссылок, API, MCP-интеграций и правил для ИИ-редакторов (суммарно **более 1,18 млн звёзд**):

| № | Репозиторий | Звёзды | Назначение и ключевые разделы | 
| ----- | ----- | ----- | ----- | 
| **1** | [**codecrafters-io/build-your-own-x**](https://github.com/codecrafters-io/build-your-own-x) | \~556.6k | **Пошаговые гайды по сборке технологий с нуля** (*«What I cannot create, I do not understand — Richard Feynman»*). Разделы: `3D Renderer`, `AI Model`, `Augmented Reality`, `BitTorrent Client`, `Blockchain`, `Database`, `Docker`, `Emulator / Virtual Machine`, `Front-end Framework`, `Game`, `Git`, `Memory Allocator`, `Network Stack`, `Neural Network`, `Operating System`, `Text Editor`, `Visual Recognition`, `Voxel Engine`, `Web Browser`, `Web Server`. | 
| **2** | [**public-apis/public-apis**](https://github.com/public-apis/public-apis) | \~492.6k | **Коллективный список сотен бесплатных публичных API** — готовое топливо для пет-проектов. Категории: `Currency Exchange` (курсы валют), `Weather` (погода), `Movies` (`Open Movie Database`, `OpenSubtitles`), `Space` (космос), `Animals`, `Anime`, `Anti-Malware`, `Art & Design`, `Authentication`, `Blockchain`, `Books`, `Business`, `Calendar`, `Cloud Storage`. | 
| **3** | [**punkpeye/awesome-mcp-servers**](https://github.com/punkpeye/awesome-mcp-servers) | \~96.9k | **Каталог серверов Model Context Protocol (MCP)** — открытого протокола для безопасного подключения ИИ-моделей к локальным и удалённым ресурсам. Примеры из разбора: работа с почтой (`Albretsen/MCPEmails`, `alexneamtu/gmail-mcp`), таблицами (`freema/mcp-gsheets` для Google Sheets), базами данных (`FreePeak/db-mcp-server` для MySQL/PostgreSQL) и браузером. | 
| **4** | [**PatrickJS/awesome-cursorrules**](https://github.com/PatrickJS/awesome-cursorrules) | \~41.0k | **Готовые конфигурационные файлы `.cursor/rules` (`.mdc`) для AI-редактора Cursor**. Категории: `Frontend Frameworks and Libraries` (React, Next.js 14 App Router, Vue, Tailwind), `Backend and Full-Stack`, `Mobile Development`, `Games and Graphics`, `CSS and Styling`, `State Management`, `Database and API`. | 

## Блок 2. Разбор Видео №2 — Технический SEO-чек-лист для навайбкоженных сайтов

### В чём корневая проблема вайбкод-сайтов

Большинство сайтов, сгенерированных нейросетями — это одностраничники (SPA) на React/Vite. Человек в браузере видит красивую страницу, а поисковый робот открывает исходный HTML-код и видит пустой контейнер:

```
<!doctype html>
<html lang="ru">
  <head>
    <script src="/assets/index-4f2a.js"></script>
  </head>
  <body>
    <div id="root"></div> <!-- ПУСТО для поискового робота -->
  </body>
</html>

```

Робот Google иногда дожидается выполнения скриптов, а **Яндекс и ИИ-поисковики часто уходят ни с чем**.

### 5 шагов исправления (SEO-чек-лист)

1. **Серверный рендеринг (SSR) или пререндер:**

   * Использовать [**Next.js**](https://nextjs.org/) или [**Astro**](https://astro.build/), которые сразу отдают роботу готовый HTML с тегами `<header>`, `<h1>`, `<p>`, `<img alt="...">`, `<a href="...">`.

   * Если не хочется переписывать существующий проект — подключить **пререндер** (генерацию статического HTML при сборке).

2. **Мета-теги, заголовки и Open Graph:**

   * У каждой страницы должен быть свой уникальный `<title>` и `<meta name="description" content="...">`.

   * Ровно **один** заголовок `<h1>` на страницу.

   * Разметка **Open Graph** (`<meta property="og:title">`, `<meta property="og:image" content="https://.../og.jpg">`), чтобы при отправке ссылки в Telegram или соцсети отображалась карточка с картинкой, а не голый адрес.

3. **Файлы индексации и панели вебмастеров:**

   * Положить в корень сайта файлы **`sitemap.xml`** и **`robots.txt`**.

   * Добавить сайт в [**Google Search Console**](https://search.google.com/search-console/about) и [**Яндекс Вебмастер**](https://webmaster.yandex.com/site/optimization/seo-guide/?section=QUICK_START), чтобы видеть, сколько страниц реально попало в индекс.

4. **Скорость загрузки и PageSpeed Insights:**

   * Проверить сайт через [**PageSpeed Insights**](https://pagespeed.web.dev/).

   * Картинки по 5 МБ (`hero.png`) сжать в формат **WebP** (`hero.webp` \~ 180 КБ).

   * Выкинуть лишние скрипты (уменьшить `bundle.js`).

   * Главный блок (**LCP — Largest Contentful Paint**) должен загружаться **быстрее 2,5 секунды** (целевая зона — зелёная `90–96+`, LCP \~ `1,9 с`).

5. **Контент под поисковый спрос и внешние ссылки:**

   * Писать заголовки и тексты под то, что люди реально ищут в поиске (*«йога для начинающих дома»*, *«йога для начинающих утром»*, *«йога для начинающих рядом»*), а не абстрактные *«Инновационные решения для вашего бизнеса. Синергия. Масштаб. Будущее»*.

   * Собирать внешние ссылки на сайт: **каталоги**, **соцсети**, **статьи**.

### Готовый промпт для ИИ-агента (из видео)

```
Проверь сайт на SEO: рендер, мета-теги, sitemap, robots и скорость — и всё исправь.

```

## Блок 3. Полный реестр 23 Дорожных Карт (Maps 01–23)

Ниже перечислены все 20 карт из вашего архива DevOps/SRE (2026–2027) и 3 новые карты (`21`–`23`), созданные в этом чате:

| Код | Файл карты | Уровень / Блок | Ключевые темы внутри карты | 
| ----- | ----- | ----- | ----- | 
| **01** | `01_Linux_and_Networking_Map.md` | Junior / Base | Linux Internals (CFS, статусы `R`/`D`/`Z`, `tini`), `namespaces`, `cgroups v2`, LVM/RAID, харденинг systemd, диагностика USE/RED, `lsof +L1`, eBPF, TCP/TLS, Nginx/Envoy. | 
| **02** | `02_Coding_and_Containers_Map.md` | Junior / Base | Python (`uv`, `httpx`, `boto3`, `kubernetes`, `pytest`, `ruff`) и Go (горутины, `context`, `Cobra`), устройство `containerd`/`runc`, слои `OverlayFS`, multi-stage `distroless` Dockerfile. | 
| **03** | `03_CI_CD_and_IaC_Map.md` | Junior / Base | GitHub Actions / GitLab CI, сборка без DinD (`Kaniko`, `BuildKit rootless`), бестокенный OIDC, OpenTofu/Terraform + Terragrunt, блокировки S3 стейта, Ansible роли, ArgoCD + Argo Rollouts. | 
| **04** | `04_Kubernetes_and_Cloud_Map.md` | Junior / Base | Control Plane (`apiserver`, `etcd` Raft снапшоты, `scheduler`), пробы `startup`/`liveness`/`readiness`, классы QoS, PDB, `TopologySpreadConstraints`, Cilium eBPF, Gateway API, Karpenter, KEDA. | 
| **05** | `05_Observability_and_DevSecOps_Map.md` | Junior / Base | Four Golden Signals, Prometheus/VictoriaMetrics (`PromQL`), Grafana, Alertmanager, структурированные JSON-логи в Loki + Vector (`LogQL`), OpenTelemetry + Tempo, Vault/OpenBao, Trivy, Kyverno. | 
| **06** | `06_SRE_and_Platform_Engineering_Map.md` | Middle / Senior | SLI/SLO/SLA, Error Budgets, Blameless Postmortems, Chaos Mesh, IDP (Crossplane XRD, Backstage), Highload БД (CloudNativePG/Patroni, PgBouncer, WAL-G, Valkey, Kafka Strimzi), FinOps. | 
| **07** | `07_Pet_Project_Blueprint.md` | Middle / Senior | Пошаговое ТЗ сквозного продакшн пет-проекта: Go/Python API + воркер + PostgreSQL + Redis в K8s, модули Terraform, CI/CD с Trivy, GitOps ArgoCD, стек мониторинга и тест k6. | 
| **08** | `08_Interview_Prep_Q_and_A.md` | Middle / Senior | Разбор вопросов собеседований: полный цикл `curl https://...`, почему `df -h` 100% при `du -sh` 20% (`lsof +L1`), Load Average и статус `D`, Docker vs `containerd`, `CrashLoopBackOff`, Terraform state. | 
| **09** | `09_Incident_Troubleshooting_Playbooks.md` | Middle / Senior | Боевые плейбуки первых 5 минут аварии: `CrashLoopBackOff` (`Exit Code 137/143/126/127`), `OOMKilled`, шторм `502/504 Bad Gateway`, переполнение таблицы `nf_conntrack`. | 
| **10** | `10_Database_and_Stateful_Runbooks.md` | Middle / Senior | SQL-шпаргалка дежурного: `pg_stat_activity`, поиск блокировок `ALTER TABLE`, лаг репликации и `autovacuum` (Dead Tuples), режимы PgBouncer, диагностика Redis/Valkey и Kafka Consumer Lag. | 
| **11** | `11_System_Design_for_DevOps_SRE.md` | Middle / Senior | Проектирование систем на 10 000+ RPS: Edge-to-Core (GeoDNS, CDN/WAF, L4/L7 LB, Stateless K8s в 3 AZ, Redis Cache-Aside, буферизация пиков в Kafka, HA PostgreSQL), расчет RTO/RPO, паттерн Outbox. | 
| **12** | `12_Postmortem_and_SLO_Templates.md` | Middle / Senior | Таблица доступности SLO (от `99.0%` до `99.99%`), формула расчета Error Budget в числе ошибок 5xx и шаблон Blameless Postmortem методом «5 почему». | 
| **13** | `13_Cloud_Security_IAM_and_FinOps_Map.md` | Middle / Senior | Концепция Zero Static Secrets (OIDC `AssumeRoleWithWebIdentity`, IRSA / Pod Identity), Supply Chain (SBOM через `syft`, подпись `cosign`, проверка в `Kyverno`) и FinOps (`OpenCost`, `Karpenter`). | 
| **14** | `14_2026_2027_Trends_AI_eBPF_Wasm_Map.md` | Principal / AI | Тренды 2026–2027: оркестрация GPU в K8s (NVIDIA GPU Operator, DRA, MIG), сервинг LLM (`vLLM`, `LiteLLM` / `Envoy AI Gateway`), Continuous Profiling (`Pyroscope`), eBPF `Beyla`, Sidecarless Mesh, `Dagger`. | 
| **15** | `15_DevOps_Resume_and_Portfolio_Guide.md` | Principal / AI | Эталонное резюме по формуле **XYZ** (*«Достиг \[X\], измеряемого в \[Y\], за счет внедрения \[Z\]»*) и чек-лист оформления инженерного GitHub-профиля. | 
| **16** | `16_Custom_K8s_Operators_and_IDP_Backstage_Map.md` | Principal / AI | Разработка операторов K8s на Go (`Kubebuilder` / `controller-runtime`, идемпотентный `Reconcile`, `OwnerReferences`, `Finalizers`) и портал самообслуживания **Backstage IDP**. | 
| **17** | `17_BareMetal_K8s_Talos_and_Cilium_BGP_Map.md` | Principal / AI | Bare-Metal Kubernetes нового поколения: неизменяемая ОС **Talos Linux** (`talosctl` gRPC API), анонсы `LoadBalancer` по **BGP в Cilium** (ECMP) и выбор CSI (`Rook-Ceph` vs `TopoLVM`). | 
| **18** | `18_MultiCluster_Federation_and_Global_Traffic_Map.md` | Principal / AI | Управление флотом кластеров: **Cluster API (CAPI)**, виртуальные кластеры **vCluster** за 5 секунд для PR-окружений, сквозная сеть **Cilium Cluster Mesh** и глобальная балансировка **GSLB**. | 
| **19** | `19_Data_Streaming_Kafka_ClickHouse_and_Lakehouse_Map.md` | Principal / AI | Highload Data в K8s: **Apache Kafka в режиме KRaft** без ZooKeeper (оператор `Strimzi`, `Tiered Storage` в S3), кластеры **ClickHouse** (`Altinity Operator`, `ClickHouse Keeper`) и S3 Lakehouse. | 
| **20** | `20_HandsOn_Troubleshooting_Simulator_Guide.md` | Principal / AI | Практический полигон поломок **Chaos Drill Lab** (`break-my-cluster.yaml` + `verify-fixes.sh`): 4 сценария с разбором (`broken-readonly-app`, `oom-and-probe-trap`, `phantom-service`, `blackhole-netpol`). | 
| **21** | `21_VibeCoding_GitHub_Ecosystem_and_MCP_Map.md` | Vibe-Coding & AI | Карта 4 главных списков GitHub (`build-your-own-x`, `public-apis`, `awesome-mcp-servers`, `awesome-cursorrules`) и пошаговый пайплайн сборки проектов с ИИ-агентами. | 
| **22** | `22_VibeCoding_SEO_SSR_and_Performance_Map.md` | Vibe-Coding & AI | Полный технический SEO-стандарт для вайбкод-сайтов и интернет-магазинов: SSR/пререндер, мета-теги, Open Graph, `sitemap.xml`/`robots.txt`, PageSpeed `90+`, Zero-CLS и маппинг фото каталога без коллизий. | 
| **23** | `23_AI_Coder_Portal_Learning_Practice_Career_Blueprint.md` | Vibe-Coding & AI | Архитектура и план запуска образовательно-карьерного портала **«Обучение — Практика — Работа для кодеров с AI»** на базе `ssrjkk/agent-skills` и `ssrjkk/raven`. | 

## Блок 4. Десять скиллов для вашей библиотеки и репозитория `ssrjkk/agent-skills`

В вашу личную библиотеку скиллов здесь в ассистенте уже добавлены и активны 4 комплексных скилла (`vibe-seo-audit`, `catalog-photo-mapper`, `devops-sre-portal-architect` и ваш `vibe-shop-normalizer`), а в архиве для GitHub лежат все двуязычные папки (`SKILL.md` + `SKILL.ru.md`):

 1. **`vibe-seo-audit`** — SEO-рефакторинг вайбкод-сайтов (SSR/пререндер, мета-теги, Open Graph, `sitemap.xml`, `robots.txt`, PageSpeed `90+`, `LCP < 2.5s`) + 4 списка GitHub.

 2. **`catalog-photo-mapper`** — аудит и привязка студийных фотографий товаров (`800x800`) по брендам, сериям и категориям без коллизий, синхронизация SQLite и автотесты.

 3. **`vibe-shop-normalizer`** — очистка вайбкод-витрин от артефактов и приведение к чистой светлой геометрии Zero-CLS.

 4. **`devops-sre-portal-architect`** — проектирование дорожных карт `01`–`23`, полигонов траблшутинга и модулей портала для AI-кодеров.

 5. **`linux-ebpf-troubleshooting`** — диагностика ядра Linux (`cgroups v2`, статус `D`, `lsof +L1`), сети, eBPF и разбор падений подов в Kubernetes.

 6. **`ci-cd-gitops-iac`** — конвейеры CI/CD с rootless `BuildKit`/`Kaniko`, бестокенным OIDC, `Dagger` на Go, `OpenTofu` + `Terragrunt`, `Cosign` и `ArgoCD` GitOps.

 7. **`k8s-baremetal-multicluster`** — Bare-Metal K8s на `Talos Linux`, анонсы `LoadBalancer` по BGP в `Cilium`, Go-операторы `Kubebuilder`, `Backstage IDP` и `vCluster`.

 8. **`ai-gpu-infra-llmops`** — сервинг LLM на GPU в K8s (`NVIDIA GPU Operator`, `DRA`/`MIG`, `vLLM`), масштабирование `KEDA`/`Karpenter` и шлюз `LiteLLM` / `Envoy AI Gateway`.

 9. **`observability-sre-highload`** — стек `VictoriaMetrics`, `Loki`, `Vector`, `OpenTelemetry`, `Beyla` eBPF, `Pyroscope`, контроль `SLO`/`Error Budget` и кластеры `CloudNativePG`, `Kafka KRaft`, `ClickHouse`.

10. **`ai-coder-career-architect`** — составление резюме по формуле XYZ, упаковка эталонных пет-проектов на GitHub и подготовка к System Design (`10k+ RPS`).