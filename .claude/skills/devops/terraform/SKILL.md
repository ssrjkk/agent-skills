---
name: terraform
description: "Provision infrastructure as code with Terraform: resources, modules, state, workspaces, and remote backends. Use for cloud resource management."
category: devops
tags: [terraform, iac, infrastructure, cloud, modules, state, aws]
models: [sonnet, opus, gpt-5, gemini-2.5, glm-4.6]
version: 1.0.0
created: 2026-09-26
updated: 2026-09-28
author: ssrjkk
---
# Terraform

> Provisioning cloud infrastructure as code with Terraform.

## Quick Start
```bash
terraform init
terraform plan
terraform apply
terraform destroy  # when done
```

## When to Use
- Reproducible cloud infrastructure
- Managing AWS/GCP/Azure resources as code
- Environments that must be identical
- Team-wide infrastructure changes with review

## Best Practices

### Configuration
- Organize by environment and component
- Use variables for config; locals for derived values
- Define outputs for inter-module references
- Pin provider and module versions

### Modules
- Extract reusable units into modules
- Keep modules small and focused
- Validate inputs with variables
- Document inputs/outputs

### State
- Use a remote backend (S3/OSS/Terraform Cloud)
- Enable state locking to prevent conflicts
- Never edit state by hand; use `terraform state`
- Protect state with permissions and versioning

### Workflow
- Plan before apply; review the diff
- Use workspaces or separate dirs per environment
- Run in CI with approval for production
- Clean up unused resources with destroy

## Dependencies
```bash
# Terraform CLI
terraform version
# providers configured in code
```

## Examples
```hcl
# Provider + resource
terraform {
  required_version = ">= 1.5"
  backend "s3" {
    bucket = "my-tf-state"
    key    = "prod/terraform.tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
  region = var.region
}

resource "aws_s3_bucket" "app" {
  bucket = "my-app-bucket"
  tags   = { Environment = var.environment }
}
```
```hcl
# Variable + output
variable "region" {
  type    = string
  default = "us-east-1"
}

variable "environment" {
  type        = string
  description = "Deployment environment"
}

output "bucket_id" {
  value = aws_s3_bucket.app.id
}
```
```hcl
# Simple module usage
module "vpc" {
  source = "./modules/vpc"
  cidr   = "10.0.0.0/16"
  name   = var.environment
}
```
```bash
# Standard workflow
terraform init
terraform fmt
terraform validate
terraform plan -out=plan.tfplan
terraform apply plan.tfplan
```

## Step-by-Step
1. Initialize the project and configure the provider.
2. Set up a remote backend with locking.
3. Write resources for the core infrastructure.
4. Extract repeated logic into modules.
5. Parameterize with variables; define outputs.
6. Run `fmt`, `validate`, and `plan` before apply.
7. Apply in CI with approval for prod environments.
8. Keep state secure and reviewed.

## Validation
1. `terraform validate` passes
2. `terraform plan` shows the intended changes only
3. State is consistent with real resources (`refresh`)
4. Destroy removes all created resources
5. Plan diff is reviewed before apply

## Troubleshooting
- State lock: release stale locks via the backend or force-unlock.
- Drift: run `terraform plan` to detect and reconcile.
- "Provider not found": run `terraform init` to fetch providers.