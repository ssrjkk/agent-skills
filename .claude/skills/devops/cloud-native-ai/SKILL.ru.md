---
name: cloud-native-ai
description: "Cloud-native AI deployment patterns"
category: devops
tags: [cloud-native-ai, devops, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: cloud-native-ai
---
# Cloud-Native AI

> Разворачивайте и масштабируйте AI-нагрузки по cloud-native паттернам: Kubernetes и контейнеризация.

## Быстрый старт
```yaml
# model-serving.yaml — inference-сервер на vLLM
apiVersion: apps/v1
kind: Deployment
metadata:
  name: vllm-server
spec:
  replicas: 1
  selector:
    matchLabels: { app: vllm }
  template:
    metadata:
      labels: { app: vllm }
    spec:
      containers:
      - name: vllm
        image: vllm/vllm-openai:latest
        args: ["--model", "mistralai/Mistral-7B-v0.1"]
        env:
        - name: HUGGING_FACE_HUB_TOKEN
          valueFrom:
            secretKeyRef: { name: hf-token, key: token }
        ports:
        - containerPort: 8000
        resources:
          limits:
            nvidia.com/gpu: 1
            memory: "32Gi"
            cpu: "8"
        readinessProbe:
          httpGet: { path: /health, port: 8000 }
          initialDelaySeconds: 60
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: vllm-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: vllm-server
  minReplicas: 1
  maxReplicas: 10
  metrics:
  - type: Pods
    pods:
      metric: { name: vllm:gpu_cache_usage_perc }
      target: { type: AverageValue, averageValue: 80 }
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
```

```bash
# Инференс с батчингом
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"mistralai/Mistral-7B-v0.1","messages":[{"role":"user","content":"Hello"}],"max_tokens":100}'
```

## Ключевые концепции
Cloud-native AI использует контейнеры, оркестрацию, service mesh и GitOps для ML-деплоя. Ключевые паттерны: serving моделей на vLLM/TGI, batch-инференс на Kueue/Volcano, модельные реестры и A/B-тестирование с разделением трафика.

## Когда использовать
- Продакшн-AI-сервисы с высоким SLA
- Мультимодельная serving-инфраструктура
- CI/CD для ML-моделей с canary-деплоем
- Управление и планирование GPU-кластеров

## Пошаговое руководство
1. Контейнеризуйте модель: соберите образ с inference-движком (vLLM/TGI) и зафиксированными весами.
2. Разверните в Kubernetes: `Deployment` с GPU-лимитами, секретами и readiness-probe на `/health`.
3. Откройте API: `Service` (ClusterIP) плюс `Ingress`/Gateway с TLS и роутингом на `/v1`.
4. Масштабируйте горизонтально: HPA по метрике GPU-кэша (`vllm:gpu_cache_usage_perc`) с окном стабилизации.
5. Откатывайте безопасно: rolling update с readiness для новых версий; canary-трафик по весу.
6. Запускайте batch-задачи: `Queue` + `Job` в Kueue/Volcano для оффлайн-инференса с PVC-артефактами.

## Примеры
```yaml
# Gateway + Service, открывающие API модели
apiVersion: v1
kind: Service
metadata:
  name: vllm-server
spec:
  selector: { app: vllm }
  ports:
    - port: 8000
      targetPort: 8000
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: model-ingress
spec:
  rules:
    - host: models.example.com
      http:
        paths:
          - path: /v1
            pathType: Prefix
            backend:
              service: { name: vllm-server, port: { number: 8000 } }
```
```bash
kubectl apply -f model-serving.yaml -f hpa.yaml -f svc-ingress.yaml
kubectl rollout status deployment/vllm-server
kubectl get hpa vllm-hpa
curl https://models.example.com/v1/chat/completions -d '{"model":"mistralai/Mistral-7B-v0.1","messages":[{"role":"user","content":"hi"}],"max_tokens":50}'
```

## Лучшие практики
- AI-нагрузки в контейнерах с закреплёнными базовыми образами.
- GPU requests/limits на Kubernetes для инференса.
- Кэшируйте модели и эмбеддинги против cold-start.
- Масштабируйте инференс горизонтально за балансировщиком.
- Мониторьте GPU, задержку и error rates.
- Service mesh или gateway для контроля трафика.

## Устранение неполадок
- GPU не выделен: проверьте nodeSelector, resources и драйвер.
- Медленный cold start: предзагрузите модели в shared memory или кэш.
- OOM на инференсе: батчите запросы или увеличьте контейнер.
- Спайки задержки: масштабируйте реплики и грейте кэш моделей.

## Валидация
1. Деплой модели завершается, health check проходит
2. HPA масштабируется по загрузке GPU
3. Rolling update разворачивает новую версию без даунтайма
4. Batch-задачи инференса завершаются с корректными результатами
