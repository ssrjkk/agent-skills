---
name: k8s-baremetal-multicluster
description: "Architects bare-metal and multi-cluster Kubernetes platforms using immutable Talos Linux, Cilium eBPF and BGP Control Plane, Rook-Ceph vs TopoLVM storage, Kubebuilder Go Operators, Backstage IDP, Cluster API, and vCluster. Use for platform engineering at scale."
category: devops
tags: [kubernetes, bare-metal, talos, cilium, bgp, kubebuilder, backstage, vcluster]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-10-28
updated: 2026-10-28
author: ssrjkk
---
# Bare-Metal Kubernetes, Go Operators & Multi-Cluster

> Immutable API-driven Talos Linux nodes, kube-proxy-free Cilium eBPF/BGP networking, custom Go controllers, and ephemeral vClusters.

## Quick Start
```bash
# Apply kube-proxy-free Talos control-plane patch and configure Cilium BGP peering
talosctl apply-config --nodes 10.10.0.11 --file labs/baremetal_and_ha_db_pack/talos-controlplane-patch.yaml
kubectl apply -f labs/baremetal_and_ha_db_pack/cilium-bgp-peering.yaml
```

```yaml
# CiliumLoadBalancerIPPool + BGP announcement for bare-metal Service: LoadBalancer
apiVersion: cilium.io/v2alpha1
kind: CiliumLoadBalancerIPPool
metadata:
  name: baremetal-vip-pool
spec:
  blocks:
    - cidr: "198.51.100.64/27"
```

## When to Use
- Building bare-metal Kubernetes clusters on immutable Talos Linux without SSH, systemd, or package managers
- Replacing kube-proxy and MetalLB with Cilium eBPF native routing and Cilium BGP Control Plane (ECMP) to Top-of-Rack routers
- Writing custom Kubernetes Operators in Go with Kubebuilder (controller-runtime), OwnerReferences, and Finalizers
- Scaling developer self-service with Backstage IDP, Crossplane XRDs, Cluster API (CAPI), and 5-second ephemeral PR vClusters

## Best Practices
- Disable kube-proxy in Talos machine config (cluster.proxy.disabled: true) and forward KubePrism localhost:7445 to Cilium k8sServiceHost.
- Use ECMP BGP peering with Top-of-Rack switches in Cilium so external traffic load-balances across nodes without L2 ARP bottlenecks.
- Choose TopoLVM or OpenEBS LocalPV on NVMe drives for replicated databases (CloudNativePG, Kafka, ClickHouse) to avoid double network replication in Ceph.
- Make every Kubebuilder Reconcile loop strictly idempotent: use OwnerReferences for in-cluster children and Finalizers for external cloud resources.
- Provision ephemeral per-PR environments with vCluster inside shared host nodes instead of spinning up dedicated cloud control planes.
- Connect multi-region Kubernetes clusters via Cilium Cluster Mesh with non-overlapping PodCIDRs and Global Services.

## Dependencies
```bash
# Install Talos CLI, Cilium CLI, Kubebuilder, and vCluster CLI
brew install siderolabs/tap/talosctl cilium-cli kubebuilder vcluster
```

## Examples
```python
# Check non-overlapping PodCIDR allocations before enabling Cilium Cluster Mesh
import ipaddress

def verify_non_overlapping_cidrs(cidrs: list[str]) -> bool:
    nets = [ipaddress.ip_network(c) for c in cidrs]
    for i, a in enumerate(nets):
        for b in nets[i + 1:]:
            if a.overlaps(b):
                return False
    return True

assert verify_non_overlapping_cidrs(["10.244.0.0/16", "10.245.0.0/16"])
```

```yaml
# Talos Linux Control Plane patch disabling kube-proxy and enabling host DNS
machine:
  features:
    kubePrism:
      enabled: true
      port: 7445
    hostDNS:
      enabled: true
      forwardKubeDNSToHost: true
cluster:
  proxy:
    disabled: true
```

## Step-by-Step
1. Generate and apply Talos Linux machine configurations via talosctl gen config and talosctl apply-config.
2. Install Cilium with kubeProxyReplacement=true, k8sServiceHost=127.0.0.1, k8sServicePort=7445, and bgpControlPlane.enabled=true.
3. Configure CiliumBGPPeeringPolicy and CiliumLoadBalancerIPPool to announce LoadBalancer VIPs to Top-of-Rack BGP neighbors.
4. Deploy Rook-Ceph for shared RWO/RWX/S3 storage and TopoLVM for low-latency local NVMe database volumes.
5. Scaffold custom Kubernetes controllers with kubebuilder init and implement idempotent Reconcile logic in Go.
6. Register Golden Path software templates in Backstage IDP backed by Crossplane CompositeResourceDefinitions (XRDs).
7. Automate ephemeral PR environments with vcluster create pr-<ID> inside GitHub Actions / GitLab CI.

## Validation
1. talosctl health and cilium status report all nodes Ready and KubeProxyReplacement: True
2. cilium bgp peers shows Established session state with Top-of-Rack routers and advertised /32 VIP prefixes
3. Custom Go Operator passes envtest reconciliation suites and cleans up child Deployments via OwnerReferences
4. vcluster create spins up an isolated control plane in under 10 seconds and tears down cleanly on PR merge

## Troubleshooting
- Cilium pods fail to reach API server when kube-proxy is disabled — point k8sServiceHost to Talos KubePrism (127.0.0.1:7445).
- BGP session stuck in Active or Connect — verify ASN numbers, peer IP reachability, and TCP port 179 firewall rules on the ToR switch.
- CRD deletion hangs indefinitely — the custom operator pod is down or failing to remove its Finalizer string from metadata.finalizers.
- High storage write latency on PostgreSQL inside Ceph — migrate database PVCs from network-replicated Ceph RBD to local NVMe TopoLVM.
