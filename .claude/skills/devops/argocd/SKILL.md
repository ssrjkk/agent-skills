---
name: argocd
description: "Deploy applications on Kubernetes with Argo CD: GitOps, applications, sync policies, health checks, and rollbacks. Use for declarative deployments."
category: devops
tags: [argocd, gitops, kubernetes, deployments, sync, rollback]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-09-29
updated: 2026-09-29
author: ssrjkk
---
# Argo CD

> GitOps deployments on Kubernetes with Argo CD.

## Quick Start
```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

## When to Use
- Declarative GitOps deployments
- Multi-environment consistency
- Self-healing cluster state
- Auditability via git history

## Best Practices

### Git as Source of Truth
- Keep manifests in git; never apply directly
- Use Kustomize/Helm for templating
- One repo per app or a monorepo with paths
- Tag versions for traceability

### Applications
- Define an Application per service
- Use app-of-apps for large fleets
- Set sync policy (manual/automated) deliberately
- Add health checks via CRDs

### Sync & Self-Healing
- Enable automated sync with prune for CI repos
- Use `selfHeal` carefully with PR review
- Add sync waves for dependency order
- Monitor sync status and history

### Security
- Restrict who can sync (RBAC)
- Use SSO (dex/okta) for auth
- Keep repo credentials in secrets
- Approve destructive syncs

## Dependencies
```bash
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
argocd login <server>
```

## Examples
```yaml
# Application manifest
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: web
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/org/app-config
    path: overlays/prod
    targetRevision: main
  destination:
    server: https://kubernetes.default.svc
    namespace: prod
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```
```yaml
# App-of-apps pattern
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: apps
  namespace: argocd
spec:
  source:
    repoURL: https://github.com/org/apps
    path: apps
    directory:
      recurse: true
```
```bash
# CLI sync and rollback
argocd app sync web
argocd app rollback web <revision>
argocd app get web
```

## Step-by-Step
1. Install Argo CD and expose the server.
2. Connect the git repo (with credentials).
3. Create an Application per service.
4. Define sync policy and health checks.
5. Enable automated sync with pruning where safe.
6. Add RBAC and SSO for access control.
7. Monitor sync status and history.
8. Roll back via git revert or argocd rollback.

## Validation
1. Apps sync from git to the desired state
2. Sync status is Healthy/Synced
3. Self-heal corrects drift
4. Rollback restores a prior revision
5. RBAC restricts who can sync

## Troubleshooting
- OutOfSync: drift detected — review and sync.
- Sync failed: check manifests and permissions.
- Health degraded: fix the workload probes.