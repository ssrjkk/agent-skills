# Шпаргалка: Команды kubectl

## Общие команды и отладка
- `kubectl get pods -A -o wide` — список всех подов во всех неймспейсах с указанием нод.
- `kubectl describe pod <pod_name>` — детальная информация, события и ошибки пода.
- `kubectl logs -f <pod_name> -c <container_name>` — просмотр логов конкретного контейнера в поде.
- `kubectl exec -it <pod_name> -- /bin/sh` — интерактивная оболочка внутри пода.
- `kubectl debug <pod_name> -it --image=busybox --target=<container_name>` — создание временного отладочного контейнера для диагностики.

## Диагностика и управление ресурсами
- `kubectl top nodes` / `kubectl top pods -A` — текущее потребление CPU и RAM нодами и подами.
- `kubectl rollout status deployment/backend-api` — проверка статуса развертывания деплоя.
- `kubectl rollout undo deployment/backend-api` — откат деплоя к предыдущей версии.
- `kubectl get events --sort-by='.metadata.creationTimestamp'` — хронологический вывод системных событий кластера.
