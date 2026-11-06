---
name: linux-ebpf-troubleshooting
description: "Diagnoses and resolves production Linux kernel, cgroups v2, network conntrack, deleted file descriptor leaks, and Kubernetes pod incidents using USE/RED methods, eBPF tools, and chaos drill labs. Use for 5-minute incident triage and root-cause isolation."
category: devops
tags: [linux, ebpf, troubleshooting, sre, kubernetes, chaos-engineering, networking]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-10-28
updated: 2026-10-28
author: ssrjkk
---
# Linux Kernel, eBPF & Kubernetes Troubleshooting

> Five-minute production incident triage across Linux kernel states, file descriptors, network sockets, and Kubernetes pods.

## Quick Start
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

## When to Use
- High Load Average with low CPU utilization caused by uninterruptible disk or NFS sleep (process state D)
- Disk reports 100% full in df -h while du -sh shows plenty of free space due to unlinked open file descriptors
- Intermittent 502/504 Bad Gateway spikes, TCP SYN backlog drops, or nf_conntrack table exhaustion
- Kubernetes pods stuck in CrashLoopBackOff (Exit Codes 1, 126, 127, 137, 143), OOMKilled, or blackholed by NetworkPolicy

## Best Practices
- Start every host triage with the USE method (Utilization, Saturation, Errors) across CPU, memory, disk I/O, and network interfaces.
- Truncate leaked file descriptors safely via : > /proc/<PID>/fd/<FD> instead of killing stateful database or proxy daemons mid-traffic.
- Use tini or dumb-init as PID 1 in containers so SIGTERM signals propagate cleanly and zombie processes (state Z) are reaped.
- Mount an emptyDir volume at /tmp and /var/run whenever enforcing readOnlyRootFilesystem: true in Kubernetes securityContext.
- Set startupProbe with a generous failureThreshold for slow-starting JVM/ML workloads so livenessProbe never triggers a premature restart loop.
- Verify Service selector labels against Pod labels with kubectl get endpoints <svc> before debugging CNI or ingress controllers.

## Dependencies
```bash
# Standard Linux triage utilities and eBPF observability tools
apt-get update && apt-get install -y sysstat lsof iproute2 dnsutils bpfcc-tools
```

## Examples
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

## Step-by-Step
1. Run uptime, vmstat 1 3, and ps aux | awk '$8 ~ /D/' to separate CPU saturation from disk/NFS I/O wait.
2. Check dmesg -T | grep -iE 'oom|killed' and /sys/fs/cgroup/memory.events to confirm kernel OOM kills.
3. Compare df -h and df -i against du -xhd1 /var; if deleted files hold blocks, find the PID via lsof +L1 and truncate the descriptor.
4. Measure network handshake latency with curl -w 'dns:%{time_namelookup} tcp:%{time_connect} tls:%{time_appconnect} ttfb:%{time_starttransfer}\n' -o /dev/null -s <URL>.
5. In Kubernetes, inspect kubectl describe pod <pod> for Last State Exit Code (137=SIGKILL/OOM, 143=SIGTERM, 126=Permission, 127=Not Found) and read kubectl logs <pod> --previous.
6. Check kubectl get endpoints <svc> and kubectl get networkpolicy -A to isolate selector mismatches or egress DNS (UDP/TCP 53) blocks.
7. Verify every fix with automated readiness checks (bash labs/troubleshooting_lab/verify-fixes.sh).

## Validation
1. dmesg -T shows zero new Out of Memory killer events after memory limit and probe tuning
2. lsof +L1 shows zero unlinked multi-gigabyte log files holding disk space
3. kubectl get endpoints <service> lists active pod IPs and curl succeeds with HTTP 200
4. All 4 scenarios in labs/troubleshooting_lab/verify-fixes.sh pass with [PASS] status

## Troubleshooting
- Pod killed with Exit Code 137 but memory usage is low — a failing livenessProbe triggers SIGKILL after terminationGracePeriodSeconds; increase initialDelaySeconds or add a startupProbe.
- Service ClusterIP times out despite Running pods — selector labels on the Service do not match template.metadata.labels on the Deployment.
- Pods cannot resolve internal or external DNS after applying NetworkPolicy — add an explicit egress rule allowing UDP and TCP port 53 to kube-dns/CoreDNS.
-  High sys% CPU time during traffic spikes — check conntrack table limits and enable eBPF kube-proxy replacement in Cilium.
