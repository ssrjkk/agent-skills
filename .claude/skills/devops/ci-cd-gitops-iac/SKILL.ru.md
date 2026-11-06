---
name: ci-cd-gitops-iac
description: "Builds secure CI/CD pipelines (GitHub Actions, GitLab CI, Dagger Go SDK, rootless BuildKit/Kaniko), OIDC tokenless cloud auth, OpenTofu/Terraform with Terragrunt, Supply Chain security (SBOM, Cosign, Kyverno), and ArgoCD GitOps with Canary rollouts. Use for end-to-end delivery automation."
category: devops
tags: [ci-cd, gitops, argocd, opentofu, terraform, dagger, oidc, devsecops]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-10-28
updated: 2026-10-28
language: ru
original: ci-cd-gitops-iac
author: ssrjkk
---
# CI/CD, GitOps & Infrastructure as Code (Пайплайны, IaC и GitOps)

> Конвейеры доставки без статических ключей (OIDC), rootless-сборка образов, пайплайны как код на Dagger, модули OpenTofu и канарки Argo Rollouts.

## Быстрый старт
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

## Когда использовать
- Переход от небезопасного Docker-in-Docker (DinD) и вечных облачных ключей к rootless BuildKit/Kaniko и временным OIDC-токенам
- Разработка переносимых пайплайнов на Go через Dagger SDK для 100% идентичности локального и CI-прогона
- Организация стейта OpenTofu/Terraform для dev/stage/prod с блокировками в S3 и обертками Terragrunt
- Защита цепочки поставки (SBOM через Syft, бесключевая подпись Cosign, проверка в Kyverno) и канареечный деплой через Argo Rollouts

## Лучшие практики
- Используйте multi-stage сборку с финальным образом gcr.io/distroless/static-debian12:nonroot (UID 65532), исключая shell и пакетные менеджеры из продакшена.
- Фиксируйте внешние GitHub Actions и базовые образы по SHA256-хэшу для защиты от подмены тегов (Supply Chain атак).
- Никогда не храните terraform.tfstate или секреты в Git; включайте блокировку стейта в S3 и проверку gitleaks на каждом PR.
- Разделяйте CI (сборка, тесты, скан Trivy, подпись Cosign, коммит тега в GitOps-репо) и CD (pull-синхронизация через ArgoCD внутри кластера).
- Автоматизируйте откат канареечных релизов в Argo Rollouts по метрикам Prometheus (доля 5xx ошибок < 1% и латентность p99 < 300 мс).
- Применяйте ArgoCD ApplicationSet с генераторами по папкам Git для автоматического подключения новых микросервисов.

## Зависимости
```bash
# Install OpenTofu, Trivy, Cosign, and Gitleaks CLI tools
brew install opentofu trivy cosign gitleaks
```

## Примеры
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

## Пошаговое руководство
1. Напишите multi-stage Dockerfile со сборкой в первом слое и копированием статики в минимальный образ distroless:nonroot.
2. Настройте доверие OIDC между GitHub Actions / GitLab CI и облачным IAM-провайдером (без сохранения статических ключей).
3. Соберите конвейер CI: линтеры, юнит-тесты, поиск секретов Gitleaks, сборка образа через BuildKit rootless и гейт уязвимостей Trivy.
4. Сгенерируйте SBOM-паспорт через syft и подпишите дайджест образа в реестре через cosign sign --yes.
5. Опишите облачную инфраструктуру в модулях OpenTofu с обертками Terragrunt и удаленным стейтом в S3.
6. Разверните ArgoCD по паттерну App-of-Apps или ApplicationSet с включенными политиками selfHeal и prune.
7. Настройте канареечный выкат Argo Rollouts с автоматической проверкой метрик Prometheus (AnalysisTemplate) на каждом шаге трафика.

## Валидация
1. Пайплайн CI авторизуется в облаке по OIDC без единого статического ключа в секретах репозитория
2. Сканирование trivy image --severity HIGH,CRITICAL --exit-code 1 проходит без критических уязвимостей
3. Проверка cosign verify подтверждает валидность криптографической подписи дайджеста образа
4. Argo Rollouts автоматически прерывает релиз и откатывает трафик при превышении порога 5xx ошибок в Prometheus

## Устранение неполадок
- Ошибка AccessDenied при OIDC-авторизации — проверьте совпадение поля sub (repo:<org>/<repo>:ref:refs/heads/main) в Trust Policy IAM-роли.
- Зависла блокировка стейта OpenTofu после обрыва CI — убедитесь в отсутствии параллельных джобов и выполните tofu force-unlock <LOCK_ID>.
- Вечный статус OutOfSync в ArgoCD при работе HPA — удалите поле spec.replicas из Deployment в Git и добавьте /spec/replicas в ignoreDifferences.
- Ошибка exec format error при старте distroless-контейнера — собирайте Go-бинарник с флагами CGO_ENABLED=0 GOOS=linux GOARCH=amd64.
