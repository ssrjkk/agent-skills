---
name: terraform
description: "Provision infrastructure as code with Terraform: resources, modules, state, workspaces, and remote backends. Use for cloud resource management."
category: devops
tags: [terraform, devops, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: terraform
author: ssrjkk
---
# Terraform (Терраформ)

> Провижининг облачной инфраструктуры как кода через Terraform.

## Быстрый старт
```bash
terraform init
terraform plan
terraform apply
terraform destroy  # когда закончили
```

## Когда использовать
- Воспроизводимая облачная инфраструктура
- Управление AWS/GCP/Azure ресурсами как кодом
- Окружения, которые должны быть идентичны
- Командные изменения инфраструктуры с ревью

## Лучшие практики

### Конфигурация
- Организуйте по окружению и компоненту
- Переменные — для конфига; locals — для производных значений
- Outputs — для ссылок между модулями
- Пините версии провайдеров и модулей

### Модули
- Переиспользуемые блоки выносите в модули
- Держите модули небольшими и сфокусированными
- Валидируйте входы через variables
- Документируйте входы/выходы

### State
- Используйте remote backend (S3/OSS/Terraform Cloud)
- Включайте state locking против конфликтов
- Никогда не редактируйте state руками; используйте `terraform state`
- Защищайте state правами и версионированием

### Workflow
- Plan перед apply; ревью диффа
- Workspaces или отдельные папки на окружение
- В CI с апрувом для продакшена
- Убирайте неиспользуемые ресурсы через destroy

## Зависимости
```bash
# Terraform CLI
terraform version
# провайдеры настраиваются в коде
```

## Примеры
```hcl
# Провайдер + ресурс
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
# Простое использование модуля
module "vpc" {
  source = "./modules/vpc"
  cidr   = "10.0.0.0/16"
  name   = var.environment
}
```
```bash
# Стандартный workflow
terraform init
terraform fmt
terraform validate
terraform plan -out=plan.tfplan
terraform apply plan.tfplan
```

## Пошаговое руководство
1. Инициализируйте проект и настройте провайдера.
2. Настройте remote backend с locking.
3. Напишите ресурсы для базовой инфраструктуры.
4. Повторяющуюся логику вынесите в модули.
5. Параметризуйте через variables; задайте outputs.
6. Перед apply — `fmt`, `validate` и `plan`.
7. В CI apply с апрувом для прод-окружений.
8. Держите state защищённым и проверяемым.

## Валидация
1. `terraform validate` проходит
2. `terraform plan` показывает только намеренные изменения
3. State согласован с реальными ресурсами (`refresh`)
4. Destroy удаляет все созданные ресурсы
5. Plan diff просмотрен до apply

## Устранение неполадок
- State lock: снимите устаревшие блокировки через backend или force-unlock.
- Drift: запустите `terraform plan` для детекции и сверки.
- "Provider not found": запустите `terraform init` для загрузки провайдеров.