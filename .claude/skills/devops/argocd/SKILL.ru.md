---
name: argocd
description: "Deploy applications on Kubernetes with Argo CD: GitOps, applications, sync policies, health checks, and rollbacks. Use for declarative deployments."
category: devops
tags: [argocd, devops, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: argocd
author: ssrjkk
---
# Argo CD (АргоСэДи)

> GitOps-деплои на Kubernetes через Argo CD.

## Быстрый старт
```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

## Когда использовать
- Декларативные GitOps-деплои
- Консистентность мульти-окружений
- Self-healing состояние кластера
- Аудируемость через git-историю

## Лучшие практики

### Git как источник правды
- Манифесты в git; никогда не применяйте напрямую
- Kustomize/Helm для темплейтов
- Один репо на приложение или monorepo с путями
- Теги версий для трассируемости

### Приложения
- Application на сервис
- App-of-apps для больших флотов
- Sync policy (manual/automated) осознанно
- Health checks через CRD

### Sync и self-healing
- Автоматический sync с prune для CI-репо
- `selfHeal` аккуратно с PR-ревью
- Sync waves для порядка зависимостей
- Мониторинг статуса и истории

### Безопасность
- Ограничьте, кто может синкать (RBAC)
- SSO (dex/okta) для auth
- Креды репо в secrets
- Апрув разрушительных синков

## Зависимости
```bash
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
argocd login <server>
```

## Примеры
```yaml
# Манифест Application
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: web
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/org/app-config
    path: overlays/prod
    targetRevision: main
  destination:
    server: https://kubernetes.default.svc
    namespace: prod
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```
```yaml
# Паттерн app-of-apps
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: apps
  namespace: argocd
spec:
  source:
    repoURL: https://github.com/org/apps
    path: apps
    directory:
      recurse: true
```
```bash
# CLI sync и rollback
argocd app sync web
argocd app rollback web <revision>
argocd app get web
```

## Пошаговое руководство
1. Установите Argo CD и откройте сервер.
2. Подключите git-репо (с кредами).
3. Создайте Application на сервис.
4. Определите sync policy и health checks.
5. Включите автоматический sync с prune, где безопасно.
6. Добавьте RBAC и SSO для контроля доступа.
7. Мониторьте статус sync и историю.
8. Откат через git revert или argocd rollback.

## Валидация
1. Apps синкаются из git в желаемое состояние
2. Статус sync Healthy/Synced
3. Self-heal исправляет дрейф
4. Rollback возвращает прошлую ревизию
5. RBAC ограничивает, кто может синкать

## Устранение неполадок
- OutOfSync: обнаружен дрейф — просмотрите и синкните.
- Sync failed: проверьте манифесты и права.
- Health degraded: исправьте пробы ворклоада.