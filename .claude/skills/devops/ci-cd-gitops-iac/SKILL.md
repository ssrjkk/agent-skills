---
name: ci-cd-gitops-iac
description: "Builds secure CI/CD pipelines (GitHub Actions, GitLab CI, Dagger Go SDK, rootless BuildKit/Kaniko), OIDC tokenless cloud auth, OpenTofu/Terraform with Terragrunt, Supply Chain security (SBOM, Cosign, Kyverno), and ArgoCD GitOps with Canary rollouts. Use for end-to-end delivery automation."
category: devops
tags: [ci-cd, gitops, argocd, opentofu, terraform, dagger, oidc, devsecops]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-10-28
updated: 2026-10-28
author: ssrjkk
---
# CI/CD, GitOps & Infrastructure as Code

> Zero static secrets, rootless container builds, programmable Dagger pipelines, OpenTofu state isolation, and progressive Argo Rollouts.

## Quick Start
```bash
# Format, validate, and security-scan OpenTofu/Terraform modules before commit
tofu fmt -check && tofu validate
trivy config . --severity HIGH,CRITICAL
```

```yaml
# GitHub Actions OIDC tokenless role assumption (no static AWS keys in secrets)
permissions:
  id-token: write
  contents: read
steps:
  - uses: aws-actions/configure-aws-credentials@v4
    with:
      role-to-assume: arn:aws:iam::123456789012:role/github-ci-oidc
      aws-region: eu-central-1
```

## When to Use
- Replacing insecure Docker-in-Docker (DinD) and static cloud keys with rootless BuildKit/Kaniko and short-lived OIDC tokens
- Writing portable CI/CD pipelines in Go with the Dagger SDK so local runs match CI execution bit-for-bit
- Structuring multi-environment OpenTofu/Terraform state with S3 locking and DRY Terragrunt hierarchies
- Enforcing container supply-chain integrity with Syft SBOMs, keyless Sigstore Cosign signatures, Kyverno policies, and Argo Rollouts Canary

## Best Practices
- Build multi-stage Dockerfiles targeting gcr.io/distroless/static-debian12:nonroot (UID 65532) to strip shells and package managers from production images.
- Pin GitHub Actions and container base images by immutable SHA256 digest in critical workflows to prevent tag-mutation supply chain attacks.
- Never commit terraform.tfstate or .env files; enforce S3 native state locking (use_lockfile = true) and run gitleaks in pre-commit.
- Separate CI (build, test, scan, sign, push image, update GitOps manifest repo) from CD (ArgoCD pull-based synchronization inside the cluster).
- Gate progressive Canary rollouts in Argo Rollouts on real Prometheus RED metrics (HTTP 5xx rate < 1% and p99 latency < 300ms).
- Use ArgoCD ApplicationSet with Git directory or matrix generators to onboard new microservices without duplicating YAML.

## Dependencies
```bash
# Install OpenTofu, Trivy, Cosign, and Gitleaks CLI tools
brew install opentofu trivy cosign gitleaks
```

## Examples
```python
# Verify that all container images in a Kubernetes manifest pin an immutable @sha256 digest or semantic tag
import re
from pathlib import Path

def audit_k8s_images(manifest_path: str) -> list[str]:
    text = Path(manifest_path).read_text(encoding="utf-8")
    images = re.findall(r"image:\s*([^\s#]+)", text)
    bad = [img for img in images if img.endswith(":latest") or (":" not in img and "@sha256:" not in img)]
    return bad
```

```yaml
# Kyverno ClusterPolicy blocking :latest tags and requiring runAsNonRoot
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: enforce-supply-chain-baseline
spec:
  validationFailureAction: Enforce
  rules:
    - name: disallow-latest-tag
      match:
        any:
          - resources:
              kinds: [Pod]
      validate:
        message: "Mutable :latest tag is forbidden; use a semantic version or @sha256 digest."
        pattern:
          spec:
            containers:
              - image: "!*:latest"
```

## Step-by-Step
1. Create a multi-stage Dockerfile that compiles the binary in stage 1 and copies only the static artifact and CA certs into a nonroot distroless image.
2. Configure OIDC trust between GitHub Actions / GitLab CI and your cloud IAM provider (AssumeRoleWithWebIdentity).
3. Add CI stages for linting, unit tests, Gitleaks secret detection, rootless BuildKit image build, and Trivy vulnerability gating.
4. Generate a CycloneDX or SPDX SBOM using syft and sign the pushed image digest with cosign sign --yes.
5. Provision cloud infrastructure via modular OpenTofu and Terragrunt with remote S3 state and encryption.
6. Deploy ArgoCD using the App-of-Apps or ApplicationSet pattern with automated selfHeal and prune policies.
7. Configure an Argo Rollouts Canary resource with an AnalysisTemplate querying Prometheus 5xx error rates during traffic shifting.

## Validation
1. CI pipeline authenticates via OIDC JWT with zero static cloud credentials stored in repository secrets
2. trivy image --severity HIGH,CRITICAL --exit-code 1 passes on the final distroless image
3. cosign verify confirms valid keyless signature on the container image digest
4. Argo Rollouts automatically aborts and rolls back the Canary release if synthetic 5xx errors exceed 1%

## Troubleshooting
- OIDC AssumeRoleWithWebIdentity AccessDenied — verify the IAM role trust policy sub claim matches repo:<org>/<repo>:ref:refs/heads/main.
- OpenTofu state lock stuck after aborted CI job — verify no concurrent run is active, then run tofu force-unlock <LOCK_ID>.
- ArgoCD OutOfSync loop on HPA replicas — omit spec.replicas from the Git Deployment manifest and add /spec/replicas to ignoreDifferences.
- Distroless container fails with exec format error — compile Go binaries with CGO_ENABLED=0 GOOS=linux GOARCH=amd64.
