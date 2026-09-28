---
name: kubernetes
description: "Deploy and operate applications on Kubernetes: workloads, services, config, scaling, and GitOps. Use for container orchestration at scale."
category: devops
tags: [kubernetes, k8s, containers, orchestration, deployment, gitops, helm]
models: [sonnet, opus, gpt-5, gemini-2.5, glm-4.6]
version: 1.0.0
created: 2026-09-20
updated: 2026-09-28
author: ssrjkk
---
# Kubernetes

> Deploying and operating containerized applications with Kubernetes.

## Quick Start
```bash
# Local cluster (kind or minikube)
kind create cluster
kubectl apply -f deploy.yaml
kubectl get pods
```

## When to Use
- Running many services that need automated scaling
- Self-healing workloads (restarts, rescheduling)
- Rolling deployments and canaries
- Multi-environment consistency at scale

## Best Practices

### Workloads
- Prefer Deployments (stateless); StatefulSets for databases
- Define resources (requests/limits) on every container
- Add liveness and readiness probes
- Use ReplicaSets with at least 2 replicas for prod

### Configuration
- Put config in ConfigMaps; secrets in Secrets (base64, external for real secrets)
- Inject via env, mounted volumes, or external secret operators
- Use Helm for packaging; chart versioning matches app version
- Never hardcode config in images

### Networking & Security
- Expose via Services (ClusterIP/NodePort/LoadBalancer)
- Use Ingress for HTTP routing with TLS
- Apply RBAC with least privilege; use NetworkPolicies
- Set resource quotas and limits per namespace

## Dependencies
```bash
# kubectl + a cluster (kind/minikube/cloud)
kubectl version --client
# Helm (optional)
helm version
```

## Examples
```yaml
# Deployment with probes, resources, and replicas
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
spec:
  replicas: 3
  selector:
    matchLabels: { app: web }
  template:
    metadata:
      labels: { app: web }
    spec:
      containers:
        - name: web
          image: ghcr.io/org/myapp:1.0.0
          ports: [{ containerPort: 8080 }]
          resources:
            requests: { cpu: 100m, memory: 128Mi }
            limits: { cpu: 500m, memory: 512Mi }
          readinessProbe:
            httpGet: { path: /health, port: 8080 }
          livenessProbe:
            httpGet: { path: /health, port: 8080 }
```
```yaml
# Service + Ingress
apiVersion: v1
kind: Service
metadata: { name: web }
spec:
  selector: { app: web }
  ports:
    - { port: 80, targetPort: 8080 }
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata: { name: web }
spec:
  rules:
    - host: app.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service: { name: web, port: { number: 80 } }
```
```yaml
# ConfigMap + Secret
apiVersion: v1
kind: ConfigMap
metadata: { name: app-config }
data:
  LOG_LEVEL: info
---
apiVersion: v1
kind: Secret
metadata: { name: app-secret }
type: Opaque
stringData:
  API_KEY: change-me
```
```bash
# Rolling update and rollback
kubectl set image deploy/web web=ghcr.io/org/myapp:1.1.0
kubectl rollout status deploy/web
kubectl rollout undo deploy/web
```

## Step-by-Step
1. Define the Deployment with resources, probes, and replicas.
2. Add a Service and Ingress for traffic routing.
3. Externalize config into ConfigMaps and Secrets.
4. Apply to a dev cluster first; validate with `kubectl get` and logs.
5. Add autoscaling (HPA) based on CPU/memory.
6. Package with Helm for reusable charts.
7. Adopt GitOps (ArgoCD/Flux) for declarative deploys.
8. Add NetworkPolicies, RBAC, and resource quotas before prod.

## Validation
1. `kubectl apply` succeeds; pods reach Ready
2. Probes pass; rolling updates complete without downtime
3. `kubectl rollout status` shows fully available
4. Ingress routes to the service over HTTPS
5. `kubectl describe` shows no crash loops or OOMKills

## Troubleshooting
- CrashLoopBackOff: check logs and image tag.
- ImagePullBackOff: verify image name, tag, and registry credentials.
- Pending pods: insufficient resources or node pressure — check events.