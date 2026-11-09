#!/usr/bin/env bash
# Скрипт проверки успешного прохождения траблшутинг-лаборатории в неймспейсе chaos-drill.
# Проверяет все 4 кейса из Карты 20; код возврата: 0 — лаборатория пройдена, 1 — есть незакрытые кейсы.
set -euo pipefail

NS="chaos-drill"
FAIL_COUNT=0
echo "=== Проверка статуса восстановления кластера в неймспейсе '${NS}' ==="

# 1. Проверка broken-readonly-app
READY_1=$(kubectl get deploy broken-readonly-app -n "${NS}" -o jsonpath='{.status.readyReplicas}' || echo "0")
if [[ "${READY_1}" == "1" ]]; then
    echo "[PASS] Кейс 1 (broken-readonly-app): Под стабильно работает!"
else
    echo "[FAIL] Кейс 1 (broken-readonly-app): Под всё еще не в статусе Ready."
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# 2. Проверка oom-and-probe-trap
READY_2=$(kubectl get deploy oom-and-probe-trap -n "${NS}" -o jsonpath='{.status.readyReplicas}' || echo "0")
RESTARTS_2=$(kubectl get pods -n "${NS}" -l app=oom-trap -o jsonpath='{.items[0].status.containerStatuses[0].restartCount}' || echo "99")
if [[ "${READY_2}" == "1" ]]; then
    echo "[PASS] Кейс 2 (oom-and-probe-trap): Liveness probe исправлена (рестартов: ${RESTARTS_2})!"
else
    echo "[FAIL] Кейс 2 (oom-and-probe-trap): Под не проходит пробы."
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# 3. Проверка Endpoints у healthy-backend-svc
EP=$(kubectl get endpoints healthy-backend-svc -n "${NS}" -o jsonpath='{.subsets[0].addresses[0].ip}' 2>/dev/null || echo "")
if [[ -n "${EP}" ]]; then
    echo "[PASS] Кейс 3 (phantom-service): Endpoints найдены (${EP})!"
else
    echo "[FAIL] Кейс 3 (phantom-service): У сервиса healthy-backend-svc пустой список Endpoints."
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

# 4. Проверка сетевой связности (Кейс 4: lockdown-all NetPol).
#    Починка по Картам 20: ingress-правило, разрешающее порт 80 (или снятие блокировки).
#    Верифицируем исход трафика через Service — как в реальном инциденте.
echo "Кейс 4: проверка сетевой связности через Service (запуск тестового пода с curl, ~20 секунд)..."
NETCHECK=$(kubectl run "netcheck-$(date +%s)" --rm -i --restart=Never \
    --image=curlimages/curl:8.9.1 -n "${NS}" \
    -- -s -m 5 http://healthy-backend-svc:8080 2>/dev/null | grep -c "nginx" || true)
if [[ "${NETCHECK}" -ge 1 ]]; then
    echo "[PASS] Кейс 4 (blackhole-netpol): Трафик до healthy-backend-svc проходит (NetworkPolicy настроена)!"
else
    echo "[FAIL] Кейс 4 (blackhole-netpol): Трафик до Service не проходит — NetworkPolicy всё еще блокирует Ingress."
    FAIL_COUNT=$((FAIL_COUNT + 1))
fi

echo ""
echo "=== Итог: закрыто $((4 - FAIL_COUNT)) из 4 кейсов ==="
if [[ "${FAIL_COUNT}" -eq 0 ]]; then
    echo "[✓] Лаборатория пройдена полностью. Кластер здоров!"
    exit 0
fi
echo "[!] Остались незакрытые кейсы — вернись к разбору в Карте 20."
exit 1
