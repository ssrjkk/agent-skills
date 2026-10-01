---
name: istio
description: "Operate a service mesh with Istio: sidecars, traffic routing, mTLS, observability, and resiliency. Use for Kubernetes service management."
category: devops
tags: [istio, service-mesh, kubernetes, mTLS, traffic-routing, observability]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-09-29
updated: 2026-09-29
author: ssrjkk
---
# Istio

> Running a service mesh on Kubernetes with Istio.

## Quick Start
```bash
istioctl install --set profile=default
kubectl label namespace default istio-injection=enabled
```

## When to Use
- Mutual TLS across services
- Fine-grained traffic routing and canaries
- Uniform telemetry (metrics, traces, logs)
- Resilience policies (timeouts, retries, circuit breakers)

## Best Practices

### Traffic Management
- Define VirtualServices for routing rules
- Use DestinationRules for subsets and load balancing
- Prefer canary via weight splits
- Keep rules explicit and reviewable

### Security
- Enable mTLS across the mesh
- Use PeerAuthentication for encryption
- Authorize with AuthorizationPolicy
- Use SPIFFE identities for services

### Observability
- Enable Prometheus metrics via sidecars
- Use Kiali for topology
- Add distributed tracing (Jaeger/Tempo)
- Monitor request volume, latency, and errors

### Resiliency
- Set timeouts and retries in VirtualServices
- Add circuit breakers via DestinationRules
- Test failure with fault injection
- Keep fail-open defaults for low-risk paths

## Dependencies
```bash
istioctl install --set profile=default
kubectl label namespace default istio-injection=enabled
```

## Examples
```yaml
# VirtualService with canary split
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

## Step-by-Step
1. Install Istio and enable sidecar injection.
2. Label namespaces for injection.
3. Add DestinationRules with subsets.
4. Create VirtualServices for routing/canaries.
5. Enable mTLS and AuthorizationPolicies.
6. Turn on telemetry and tracing.
7. Add timeouts, retries, and circuit breakers.
8. Monitor with Kiali and dashboards.

## Validation
1. Sidecars are injected and healthy
2. mTLS encrypts service-to-service traffic
3. Canary splits route the correct weight
4. AuthorizationPolicy blocks unauthorized calls
5. Metrics/traces flow for all services

## Troubleshooting
- Sidecar not injected: check namespace label and restart pods.
- Routing wrong: review VirtualService host and subset labels.
- mTLS issues: check PeerAuthentication mode and certs.