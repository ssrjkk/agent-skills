---
name: linux-ebpf-troubleshooting
description: "Diagnoses and resolves production Linux kernel, cgroups v2, network conntrack, deleted file descriptor leaks, and Kubernetes pod incidents using USE/RED methods, eBPF tools, and chaos drill labs. Use for 5-minute incident triage and root-cause isolation."
category: devops
tags: [linux, ebpf, troubleshooting, sre, kubernetes, chaos-engineering, networking]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-10-28
updated: 2026-10-28
language: ru
original: linux-ebpf-troubleshooting
author: ssrjkk
---
# Linux Kernel, eBPF & Kubernetes Troubleshooting (Траблшутинг Linux и K8s)

> Боевая локализация первопричин аварий ядра Linux, утечек диска, сети и подов Kubernetes в первые 5 минут инцидента.

## Быстрый старт
```bash
# 10-second USE triage: load average, D-state processes, disk I/O saturation, and deleted open files
uptime && vmstat 1 3 && iostat -xz 1 2
lsof +L1 | head -n 20
ss -tulpan | head -n 20
```

```bash
# Launch the 4-scenario Kubernetes Chaos Drill lab and run automated fix verification
kubectl apply -f labs/troubleshooting_lab/break-my-cluster.yaml
bash labs/troubleshooting_lab/verify-fixes.sh
```

## Когда использовать
- Высокий Load Average при низком потреблении CPU из-за блокировки процессов в статусе D (ожидание диска или NFS)
- Диск заполнен на 100% по df -h при полупустом du -sh из-за удаленных файлов, удерживаемых открытыми дескрипторами
- Периодические ошибки 502/504 Bad Gateway, сбросы TCP-пакетов или переполнение таблицы состояний nf_conntrack
- Поды Kubernetes в статусе CrashLoopBackOff (коды 1, 126, 127, 137, 143), OOMKilled или потеря трафика из-за NetworkPolicy

## Лучшие практики
- Начинайте диагностику узла по методологии USE (Utilization, Saturation, Errors) для CPU, памяти, диска и сети.
- Очищайте удерживаемые удаленные файлы безопасно через : > /proc/<PID>/fd/<FD> без жесткого убийства рабочего процесса.
- Используйте tini в качестве PID 1 внутри контейнера для корректной обработки SIGTERM и сборки процессов-зомби (статус Z).
- Монтируйте том emptyDir в /tmp и /var/run при включении жесткой защиты readOnlyRootFilesystem: true в Kubernetes.
- Настраивайте startupProbe для долго стартующих сервисов, чтобы livenessProbe не убивал приложение до завершения инициализации.
- Всегда проверяйте наличие IP-адресов в kubectl get endpoints <svc> перед тем, как искать проблему в балансировщике или CNI.

## Зависимости
```bash
# Standard Linux triage utilities and eBPF observability tools
apt-get update && apt-get install -y sysstat lsof iproute2 dnsutils bpfcc-tools
```

## Примеры
```python
# Parse /proc/sys/net/netfilter/nf_conntrack_count vs max to detect firewall table saturation
from pathlib import Path

def check_conntrack_saturation(threshold: float = 0.85) -> dict:
    count_p = Path("/proc/sys/net/netfilter/nf_conntrack_count")
    max_p = Path("/proc/sys/net/netfilter/nf_conntrack_max")
    if not count_p.exists() or not max_p.exists():
        return {"status": "not_enabled", "ratio": 0.0}
    cur = int(count_p.read_text().strip())
    lim = int(max_p.read_text().strip())
    ratio = cur / lim if lim else 0.0
    return {"status": "critical" if ratio >= threshold else "ok", "current": cur, "max": lim, "ratio": round(ratio, 3)}
```

```yaml
# Fix readOnlyRootFilesystem crash and aggressive liveness probe in Kubernetes
apiVersion: apps/v1
kind: Deployment
metadata:
  name: resilient-api
  namespace: chaos-lab
spec:
  replicas: 2
  selector:
    matchLabels:
      app: resilient-api
  template:
    metadata:
      labels:
        app: resilient-api
    spec:
      containers:
        - name: api
          image: nginxinc/nginx-unprivileged:1.27-alpine
          resources:
            requests: { cpu: 100m, memory: 128Mi }
            limits: { cpu: 500m, memory: 256Mi }
          securityContext:
            readOnlyRootFilesystem: true
            runAsNonRoot: true
            runAsUser: 101
          volumeMounts:
            - { name: tmp-vol, mountPath: /tmp }
      volumes:
        - name: tmp-vol
          emptyDir: {}
```

## Пошаговое руководство
1. Выполните uptime, vmstat 1 3 и поиск процессов в статусе D (ps aux | awk '$8 ~ /D/'), чтобы отделить полку по CPU от зависания диска или NFS.
2. Проверьте системный журнал dmesg -T | grep -iE 'oom|killed' и счетчики cgroups v2 (memory.events) на предмет срабатывания OOM Killer.
3. Сверьте df -h и df -i с du -xhd1 /var; при утечке удаленных файлов найдите процесс через lsof +L1 и обнулите дескриптор.
4. Замерьте фазы сетевого соединения через curl -w 'dns:%{time_namelookup} tcp:%{time_connect} tls:%{time_appconnect} ttfb:%{time_starttransfer}\n' -o /dev/null -s <URL>.
5. В Kubernetes изучите kubectl describe pod <pod> (код 137 = SIGKILL/OOM, 143 = SIGTERM, 126/127 = ошибка запуска) и логи предыдущего контейнера kubectl logs <pod> --previous.
6. Проверьте список эндпоинтов kubectl get endpoints <svc> и правила NetworkPolicy (особенно разрешение egress на порт 53 для CoreDNS).
7. Подтвердите устранение всех поломок автотестом bash labs/troubleshooting_lab/verify-fixes.sh.

## Валидация
1. В выводе dmesg -T отсутствуют новые срабатывания OOM Killer после корректировки лимитов и проб
2. Команда lsof +L1 не показывает зависших удаленных лог-файлов, удерживающих место на диске
3. Эндпоинты сервиса (kubectl get endpoints) содержат IP живых подов и отвечают кодом HTTP 200
4. Все 4 сценария полигона в скрипте labs/troubleshooting_lab/verify-fixes.sh проходят со статусом [PASS]

## Устранение неполадок
- Под падает с кодом 137 при низком потреблении памяти — его убивает kubelet по провалу livenessProbe; добавьте startupProbe или увеличьте таймаут.
- Таймаут при обращении к Service при живых подах — метки в spec.selector сервиса не совпадают с метками подов.
- Внутри пода перестает резолвиться DNS после включения NetworkPolicy — добавьте в Egress-правило разрешение на порт 53 (UDP/TCP) до CoreDNS.
- Высокое потребление sys% CPU на пиках трафика — проверьте лимит nf_conntrack_max и переключите Cilium в режим eBPF kube-proxy replacement.
