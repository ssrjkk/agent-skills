# Карта 20: Практический Тренажер Траблшутинга (Chaos Drill Lab)

Теория без практики быстро забывается. В папке `troubleshooting_lab/` этого архива лежит боевой манифест **`break-my-cluster.yaml`**, который разворачивает в твоем локальном кластере (Minikube / Kind / k3s) неймспейс `chaos-drill` с **4 реалистичными поломками**, которые постоянно встречаются на продакшене и технических собеседованиях.

---

## Как запустить полигон:
```bash
kubectl apply -f troubleshooting_lab/break-my-cluster.yaml
kubectl get pods,svc,netpol -n chaos-drill
```

---

## Задания лабы (Попробуй найти и починить сам, прежде чем читать разбор ниже!)

1. **Кейс 1 (`broken-readonly-app`):** Под постоянно падает в `CrashLoopBackOff`. Приложение пытается записать PID-файл при старте, но что-то ему мешает.
2. **Кейс 2 (`oom-and-probe-trap`):** Под запускается, но каждые 15 секунд убивается с `Exit Code: 137`. Тут сразу две закладки — одна по памяти, вторая в пробе!
3. **Кейс 3 (`phantom-service`):** Под `healthy-backend` зеленый (`Running`, `1/1 Ready`), но при попытке обратиться к его `Service` (`curl http://healthy-backend-svc.chaos-drill.svc:8080`) соединение мгновенно сбрасывается.
4. **Кейс 4 (`blackhole-netpol`):** Даже после починки `Service` из Кейса 3 трафик от тестового пода не проходит из-за сетевой изоляции.

---

## Спойлер: Разбор и ключи к починке (Инженерные ответы)

<details>
<summary>Нажми, чтобы открыть разбор всех 4 поломок</summary>

### Разбор Кейса 1 (`broken-readonly-app`):
- **Диагностика:** `kubectl logs -n chaos-drill deploy/broken-readonly-app` покажет `can't create /var/run/app.pid: Read-only file system`.
- **Причина:** В контейнере включен харденинг `readOnlyRootFilesystem: true`, но не примонтирован `emptyDir` том для временной директории `/var/run`.
- **Починка:** Добавить `volumes: [{name: run-tmp, emptyDir: {}}]` и `volumeMounts: [{name: run-tmp, mountPath: /var/run}]`.

### Разбор Кейса 2 (`oom-and-probe-trap`):
- **Диагностика:** `kubectl describe pod -n chaos-drill -l app=oom-trap` покажет `Liveness probe failed: HTTP probe failed with statuscode: 404` или `OOMKilled`.
- **Причина:** Во-первых, `livenessProbe` стучится на несуществующий порт `9999` вместо `80`. Во-вторых, лимит памяти стоит нереалистично низкий (`8Mi`).
- **Починка:** Повысить `resources.limits.memory` до `64Mi` и исправить порт в `livenessProbe` на `80`.

### Разбор Кейса 3 (`phantom-service`):
- **Диагностика:** `kubectl get endpoints healthy-backend-svc -n chaos-drill` покажет `<none>`.
- **Причина:** В деплойменте у подов стоит лейбл `app: healthy-backend`, а в `Service` в поле `selector` написано `app: healthy-backEnd-typo` (опечатка в регистре), а `targetPort` указан `8080` вместо `80`.
- **Починка:** Выровнять `selector: app: healthy-backend` и `targetPort: 80`.

### Разбор Кейса 4 (`blackhole-netpol`):
- **Диагностика:** В неймспейсе висит `NetworkPolicy` `lockdown-all`, которая блокирует весь Ingress-трафик, но не добавляет разрешающего правила для `healthy-backend`.
- **Починка:** Добавить правило `ingress` в `NetworkPolicy`, разрешающее порт `80`.

</details>
