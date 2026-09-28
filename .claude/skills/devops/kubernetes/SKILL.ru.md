---
name: kubernetes
description: "Deploy and operate applications on Kubernetes: workloads, services, config, scaling, and GitOps. Use for container orchestration at scale."
category: devops
tags: [kubernetes, devops, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: kubernetes
author: ssrjkk
---
# Kubernetes (Кубернетес)

> Деплой и эксплуатация контейнерных приложений на Kubernetes.

## Быстрый старт
```bash
# Локальный кластер (kind или minikube)
kind create cluster
kubectl apply -f deploy.yaml
kubectl get pods
```

## Когда использовать
- Много сервисов, которым нужен автоматический скейлинг
- Self-healing нагрузки (рестарты, перепланирование)
- Rolling-деплои и canary
- Консистентность мульти-окружений в масштабе

## Лучшие практики

### Нагрузки
- Предпочитайте Deployments (stateless); StatefulSets — для БД
- Определяйте resources (requests/limits) на каждом контейнере
- Добавляйте liveness и readiness пробы
- В проде минимум 2 реплики

### Конфигурация
- Конфиг — в ConfigMaps; секреты — в Secrets (base64; для реальных секретов — внешние)
- Инжектируйте через env, смонтированные volumes или external secret operators
- Для упаковки используйте Helm; версия чарта совпадает с версией приложения
- Никогда не зашивайте конфиг в образы

### Сеть и безопасность
- Экспонируйте через Services (ClusterIP/NodePort/LoadBalancer)
- Для HTTP-маршрутизации используйте Ingress с TLS
- Применяйте RBAC с минимальными правами; используйте NetworkPolicies
- Ставьте quotas и limits на namespace

## Зависимости
```bash
# kubectl + кластер (kind/minikube/cloud)
kubectl version --client
# Helm (опционально)
helm version
```

## Примеры
```yaml
# Deployment с пробами, ресурсами и репликами
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
spec:
  replicas: 3
  selector:
    matchLabels: { app: web }
  template:
    metadata:
      labels: { app: web }
    spec:
      containers:
        - name: web
          image: ghcr.io/org/myapp:1.0.0
          ports: [{ containerPort: 8080 }]
          resources:
            requests: { cpu: 100m, memory: 128Mi }
            limits: { cpu: 500m, memory: 512Mi }
          readinessProbe:
            httpGet: { path: /health, port: 8080 }
          livenessProbe:
            httpGet: { path: /health, port: 8080 }
```
```yaml
# Service + Ingress
apiVersion: v1
kind: Service
metadata: { name: web }
spec:
  selector: { app: web }
  ports:
    - { port: 80, targetPort: 8080 }
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata: { name: web }
spec:
  rules:
    - host: app.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service: { name: web, port: { number: 80 } }
```
```yaml
# ConfigMap + Secret
apiVersion: v1
kind: ConfigMap
metadata: { name: app-config }
data:
  LOG_LEVEL: info
---
apiVersion: v1
kind: Secret
metadata: { name: app-secret }
type: Opaque
stringData:
  API_KEY: change-me
```
```bash
# Rolling update и откат
kubectl set image deploy/web web=ghcr.io/org/myapp:1.1.0
kubectl rollout status deploy/web
kubectl rollout undo deploy/web
```

## Пошаговое руководство
1. Определите Deployment с ресурсами, пробами и репликами.
2. Добавьте Service и Ingress для маршрутизации трафика.
3. Вынесите конфиг в ConfigMaps и Secrets.
4. Сначала применяйте в dev-кластер; валидируйте через `kubectl get` и логи.
5. Добавьте автопскейлинг (HPA) по CPU/памяти.
6. Упакуйте в Helm-чарты для переиспользования.
7. Внедрите GitOps (ArgoCD/Flux) для декларативных деплоев.
8. Добавьте NetworkPolicies, RBAC и quotas до прода.

## Валидация
1. `kubectl apply` проходит; поды достигают Ready
2. Пробы проходят; rolling-обновления без downtime
3. `kubectl rollout status` показывает fully available
4. Ingress маршрутизирует на сервис по HTTPS
5. `kubectl describe` не показывает crash loops или OOMKills

## Устранение неполадок
- CrashLoopBackOff: проверьте логи и тег образа.
- ImagePullBackOff: проверьте имя/тег образа и креды реестра.
- Pending поды: нехватка ресурсов или node pressure — проверьте события.