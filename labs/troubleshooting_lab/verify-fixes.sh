#!/usr/bin/env bash
# Скрипт проверки успешного прохождения траблшутинг-лаборатории в неймспейсе chaos-drill
set -euo pipefail

NS="chaos-drill"
echo "=== Проверка статуса восстановления кластера в неймспейсе '${NS}' ==="

# 1. Проверка broken-readonly-app
READY_1=$(kubectl get deploy broken-readonly-app -n "${NS}" -o jsonpath='{.status.readyReplicas}' || echo "0")
if [[ "${READY_1}" == "1" ]]; then
    echo "[PASS] Кейс 1 (broken-readonly-app): Под стабильно работает!"
else
    echo "[FAIL] Кейс 1 (broken-readonly-app): Под всё еще не в статусе Ready."
fi

# 2. Проверка oom-and-probe-trap
READY_2=$(kubectl get deploy oom-and-probe-trap -n "${NS}" -o jsonpath='{.status.readyReplicas}' || echo "0")
RESTARTS_2=$(kubectl get pods -n "${NS}" -l app=oom-trap -o jsonpath='{.items[0].status.containerStatuses[0].restartCount}' || echo "99")
if [[ "${READY_2}" == "1" ]]; then
    echo "[PASS] Кейс 2 (oom-and-probe-trap): Liveness probe исправлена (рестартов: ${RESTARTS_2})!"
else
    echo "[FAIL] Кейс 2 (oom-and-probe-trap): Под не проходит пробы."
fi

# 3. Проверка Endpoints у healthy-backend-svc
EP=$(kubectl get endpoints healthy-backend-svc -n "${NS}" -o jsonpath='{.subsets[0].addresses[0].ip}' 2>/dev/null || echo "")
if [[ -n "${EP}" ]]; then
    echo "[PASS] Кейс 3 (phantom-service): Endpoints найдены (${EP})!"
else
    echo "[FAIL] Кейс 3 (phantom-service): У сервиса healthy-backend-svc пустой список Endpoints."
fi
