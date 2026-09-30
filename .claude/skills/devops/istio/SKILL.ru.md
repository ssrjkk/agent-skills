---
name: istio
description: "Operate a service mesh with Istio: sidecars, traffic routing, mTLS, observability, and resiliency. Use for Kubernetes service management."
category: devops
tags: [istio, devops, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: istio
author: ssrjkk
---
# Istio (Истио)

> Service mesh на Kubernetes через Istio.

## Быстрый старт
```bash
istioctl install --set profile=default
kubectl label namespace default istio-injection=enabled
```

## Когда использовать
- Mutual TLS между сервисами
- Точный роутинг трафика и canary
- Единая телеметрия (метрики, трейсы, логи)
- Политики устойчивости (таймауты, retries, circuit breakers)

## Лучшие практики

### Управление трафиком
- VirtualServices для правил роутинга
- DestinationRules для subsets и балансировки
- Canary через весовые сплиты
- Правила явные и проверяемые

### Безопасность
- mTLS по всему mesh
- PeerAuthentication для шифрования
- AuthorizationPolicy для авторизации
- SPIFFE-идентичности сервисов

### Наблюдаемость
- Prometheus-метрики через сайдкары
- Kiali для топологии
- Распределённый трейсинг (Jaeger/Tempo)
- Мониторинг объёма, задержки и ошибок

### Устойчивость
- Таймауты и retries в VirtualServices
- Circuit breakers через DestinationRules
- Тест фейлов через fault injection
- Fail-open дефолты для низкорисковых путей

## Зависимости
```bash
istioctl install --set profile=default
kubectl label namespace default istio-injection=enabled
```

## Примеры
```yaml
# VirtualService с canary-сплитом
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata: { name: web }
spec:
  hosts: [web]
  http:
    - route:
        - destination: { host: web, subset: stable }
          weight: 90
        - destination: { host: web, subset: canary }
          weight: 10
```
```yaml
# DestinationRule subsets + circuit breaker
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata: { name: web }
spec:
  host: web
  subsets:
    - name: stable
      labels: { version: v1 }
    - name: canary
      labels: { version: v2 }
  trafficPolicy:
    connectionPool:
      tcp: { maxConnections: 100 }
    outlierDetection:
      consecutive5xxErrors: 5
```
```yaml
# AuthorizationPolicy
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata: { name: require-jwt }
spec:
  action: ALLOW
  rules:
    - from:
        - source: { requestPrincipals: ["*"] }
```
```yaml
# mTLS peer authentication
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata: { name: default }
spec:
  mtls:
    mode: STRICT
```

## Пошаговое руководство
1. Установите Istio и включите sidecar-инъекцию.
2. Пометьте namespace для инъекции.
3. Добавьте DestinationRules с subsets.
4. Создайте VirtualServices для роутинга/canary.
5. Включите mTLS и AuthorizationPolicies.
6. Включите телеметрию и трейсинг.
7. Добавьте таймауты, retries и circuit breakers.
8. Мониторьте через Kiali и дашборды.

## Валидация
1. Сайдкары инжектированы и здоровы
2. mTLS шифрует трафик сервис-к-сервису
3. Canary-сплиты роутят корректные веса
4. AuthorizationPolicy блокирует неавторизованные вызовы
5. Метрики/трейсы идут для всех сервисов

## Устранение неполадок
- Сайдкар не инжектирован: проверьте label namespace и перезапуск подов.
- Неверный роутинг: просмотрите host VirtualService и labels subsets.
- Проблемы mTLS: проверьте PeerAuthentication mode и серты.