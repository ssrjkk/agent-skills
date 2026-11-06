# Шпаргалка: Запросы PromQL и LogQL для мониторинга и разбора аварий

## PromQL (Prometheus / VictoriaMetrics)

### 1. Методология RED для HTTP-сервисов
- **RPS (Запросов в секунду по сервису):**
  ```promql
  sum(rate(http_requests_total{job="backend-api"}[5m])) by (status_code)
  ```
- **Процент 5xx ошибок от общего трафика:**
  ```promql
  sum(rate(http_requests_total{job="backend-api", status_code=~"5.."}[5m]))
  /
  sum(rate(http_requests_total{job="backend-api"}[5m])) * 100
  ```
- **99-й перцентиль задержки ответа (Latency p99):**
  ```promql
  histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket{job="backend-api"}[5m])) by (le))
  ```

### 2. Ресурсы Kubernetes (cAdvisor / kube-state-metrics)
- **Топ-5 подов по потреблению памяти:**
  ```promql
  topk(5, sum(container_memory_working_set_bytes{container!="", image!=""}) by (namespace, pod))
  ```
- **Поиск контейнеров с высоким CPU Throttling (> 25%):**
  ```promql
  sum(rate(container_cpu_cfs_throttled_periods_total{container!=""}[5m])) by (namespace, pod, container)
  /
  sum(rate(container_cpu_cfs_periods_total{container!=""}[5m])) by (namespace, pod, container) * 100 > 25
  ```
- **Поды, которые часто рестартуют за последние 15 минут:**
  ```promql
  increase(kube_pod_container_status_restarts_total[15m]) > 2
  ```

---

## LogQL (Grafana Loki)

- **Поиск ошибок в JSON-логах конкретного сервиса с фильтрацией по полю:**
  ```logql
  {namespace="production", app="backend-api"} |= "error" | json | level="error" and status >= 500
  ```
- **Подсчет количества ошибок в секунду из логов (для построения графика в Grafana):**
  ```logql
  sum by (app) (rate({namespace="production"} | json | level="error" [5m]))
  ```
- **Поиск медленных запросов в логах (> 1 секунды):**
  ```logql
  {namespace="production", app="backend-api"} | json | duration_ms > 1000 | line_format "{{.method}} {{.path}} took {{.duration_ms}}ms (trace={{.trace_id}})"
  ```
