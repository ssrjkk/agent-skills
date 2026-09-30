---
name: jenkins
description: "Operate Jenkins CI/CD: pipelines as code, agents, shared libraries, credentials, and plugins. Use for build and release automation."
category: devops
tags: [jenkins, devops, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: jenkins
author: ssrjkk
---
# Jenkins (Дженкинс)

> CI/CD автоматизация через Jenkins.

## Быстрый старт
```bash
docker run -p 8080:8080 -p 50000:50000 -d jenkins/jenkins:lts
# http://localhost:8080, разблокировка initial admin password
```

## Когда использовать
- Build/test/deploy пайплайны
- Сложные multi-stage workflow
- Легаси или on-prem CI
- Богатая плагинами автоматизация

## Лучшие практики

### Pipelines as code
- Declarative пайплайны в Jenkinsfile
- Jenkinsfile в репо с приложением
- Стадии небольшие и именованные
- Параметры для переиспользования

### Агенты и конкурентность
- Labels для роутинга задач по агентам
- Лимиты параллельных сборок на задачу
- Эфемерные агенты/контейнеры
- Предзагруженные образы агентов

### Креды и безопасность
- Секреты в Credentials (не inline)
- Привязка через `withCredentials`
- Скоуп кредов по проектам
- RBAC и ограничение админов

### Поддержка
- Версионируйте shared libraries (pipelines)
- Пините версии плагинов и обновляйте осознанно
- Чистите workspaces и артефакты
- Мониторьте диск и время сборок

## Зависимости
```bash
docker run -p 8080:8080 -p 50000:50000 -d jenkins/jenkins:lts
```

## Примеры
```groovy
// Declarative Jenkinsfile
pipeline {
    agent { label 'linux' }
    parameters {
        string(name: 'BRANCH', defaultValue: 'main', description: 'Branch to build')
    }
    stages {
        stage('Checkout') {
            steps { git branch: "${params.BRANCH}", url: 'https://github.com/org/app.git' }
        }
        stage('Test') {
            steps { sh 'pytest tests/' }
        }
        stage('Deploy') {
            steps { sh './deploy.sh' }
        }
    }
    post {
        always { junit 'reports/**/*.xml' }
        failure { emailext subject: 'Build failed', to: 'dev@example.com' }
    }
}
```
```groovy
// Безопасное использование кредов
pipeline {
    stages {
        stage('Push') {
            steps {
                withCredentials([string(credentialsId: 'dockerhub', variable: 'TOKEN')]) {
                    sh 'docker login -u user -p "$TOKEN"'
                }
            }
        }
    }
}
```
```groovy
// Ссылка на shared library
@Library('my-lib@1.2') _
def result = myDeploy(stage: 'prod')
```

## Пошаговое руководство
1. Установите Jenkins и настройте master.
2. Добавьте агенты или cloud-агенты.
3. Создайте pipeline job со ссылкой на Jenkinsfile.
4. Напишите declarative стадии build/test/deploy.
5. Храните секреты в Credentials.
6. Добавьте post-build действия и уведомления.
7. Версионируйте shared libraries.
8. Мониторьте диск, плагины и время сборок.

## Валидация
1. Пайплайны зелёные на целевых ветках
2. Секреты не появляются в логах
3. Сборки идут на корректные агенты
4. Фейлы уведомляют и чистят за собой
5. Версии плагинов пинованы

## Устранение неполадок
- Синтаксис пайплайна: валидируйте через Snippet Generator.
- Агент offline: проверьте связь и labels.
- Утечки секретов: ротируйте и исправьте шаг, который напечатал.