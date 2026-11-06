---
name: k8s-baremetal-multicluster
description: "Architects bare-metal and multi-cluster Kubernetes platforms using immutable Talos Linux, Cilium eBPF and BGP Control Plane, Rook-Ceph vs TopoLVM storage, Kubebuilder Go Operators, Backstage IDP, Cluster API, and vCluster. Use for platform engineering at scale."
category: devops
tags: [kubernetes, bare-metal, talos, cilium, bgp, kubebuilder, backstage, vcluster]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-10-28
updated: 2026-10-28
language: ru
original: k8s-baremetal-multicluster
author: ssrjkk
---
# Bare-Metal Kubernetes, Go Operators & Multi-Cluster (Talos, Cilium BGP и Операторы)

> Неизменяемая ОС Talos Linux, сетевой стек Cilium eBPF с BGP-анонсами на голом железе, разработка операторов на Go и мульти-кластерные платформы.

## Быстрый старт
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

## Когда использовать
- Построение bare-metal кластеров Kubernetes на неизменяемой ОС Talos Linux без SSH, bash и пакетных менеджеров
- Замена kube-proxy и MetalLB на прямую маршрутизацию Cilium eBPF и анонсы LoadBalancer по BGP (ECMP) на коммутаторы стойки
- Разработка собственных операторов Kubernetes на Go (Kubebuilder / controller-runtime) с идемпотентным циклом Reconcile
- Внедрение внутреннего портала разработчика Backstage IDP, Crossplane XRD, Cluster API (CAPI) и изолированных PR-окружений на vCluster

## Лучшие практики
- Отключайте kube-proxy в конфигурации Talos (cluster.proxy.disabled: true) и направляйте Cilium на локальный балансировщик KubePrism (127.0.0.1:7445).
- Используйте BGP-пиринг (ECMP) со стоечными коммутаторами ToR вместо L2 ARP для равномерного распределения входящего трафика.
- Для кластерных БД с собственной репликацией (CloudNativePG, Kafka, ClickHouse) выбирайте локальные NVMe через TopoLVM, чтобы не платить тройным I/O в Ceph.
- Проектируйте функцию Reconcile в Go-операторах строго идемпотентной, используя OwnerReferences для ресурсов K8s и Finalizers для внешних API.
- Поднимайте временные стенды под каждый Pull Request через vCluster за 5 секунд вместо создания отдельных дорогих облачных кластеров.
- Объединяйте кластеры разных площадок через Cilium Cluster Mesh с непересекающимися сетями PodCIDR и глобальными сервисами.

## Зависимости
```bash
# Install Talos CLI, Cilium CLI, Kubebuilder, and vCluster CLI
brew install siderolabs/tap/talosctl cilium-cli kubebuilder vcluster
```

## Примеры
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

## Пошаговое руководство
1. Сгенерируйте и примените декларативную конфигурацию узлов Talos Linux через talosctl gen config и talosctl apply-config.
2. Установите Cilium с параметрами kubeProxyReplacement=true, k8sServiceHost=127.0.0.1, k8sServicePort=7445 и bgpControlPlane.enabled=true.
3. Опишите CiliumBGPPeeringPolicy и CiliumLoadBalancerIPPool для анонса внешних VIP-адресов на BGP-маршрутизаторы стойки.
4. Разверните Rook-Ceph для общих томов и S3-бакетов, а TopoLVM — для быстрых локальных NVMe-дисков под базы данных.
5. Инициализируйте каркас оператора через kubebuilder init и реализуйте идемпотентный контроллер Reconcile на Go.
6. Подключите шаблоны Golden Path в портале Backstage IDP и инфраструктурные композиции Crossplane XRD.
7. Настройте автоматическое создание изолированных PR-кластеров через vcluster create pr-<ID> в пайплайне CI.

## Валидация
1. Команды talosctl health и cilium status подтверждают готовность всех узлов и активный режим KubeProxyReplacement: True
2. В выводе cilium bgp peers сессии с маршрутизаторами находятся в статусе Established и анонсируют /32 префиксы
3. Оператор на Go проходит интеграционные тесты envtest и каскадно удаляет дочерние ресурсы через OwnerReferences
4. Временный кластер vCluster поднимается менее чем за 10 секунд и полностью очищается при закрытии Pull Request

## Устранение неполадок
- Поды Cilium не видят API-сервер после отключения kube-proxy — укажите адрес локального балансировщика KubePrism (127.0.0.1:7445).
- BGP-сессия висит в статусе Active/Connect — проверьте номера AS, доступность IP соседа и открытие порта TCP 179 на коммутаторе.
- Удаление кастомного ресурса CRD зависает навсегда — под оператора остановлен или не снимает свой Finalizer после очистки внешних объектов.
- Высокая задержка записи в PostgreSQL поверх Ceph — перенесите тома БД с сетевого Ceph RBD на локальные NVMe-диски под управлением TopoLVM.
