---
name: jenkins
description: "Operate Jenkins CI/CD: pipelines as code, agents, shared libraries, credentials, and plugins. Use for build and release automation."
category: devops
tags: [jenkins, ci, cd, pipelines, declarative, agents, credentials]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-09-29
updated: 2026-09-29
author: ssrjkk
---
# Jenkins

> CI/CD automation with Jenkins.

## Quick Start
```bash
docker run -p 8080:8080 -p 50000:50000 -d jenkins/jenkins:lts
# http://localhost:8080, unlock with initial admin password
```

## When to Use
- Build/test/deploy pipelines
- Complex multi-stage workflows
- Legacy or on-prem CI needs
- Plugin-rich automation

## Best Practices

### Pipelines as Code
- Use Declarative pipelines in a Jenkinsfile
- Store Jenkinsfiles in the repo with the app
- Keep stages small and named
- Use parameters for reusability

### Agents & Concurrency
- Use labels to route jobs to agents
- Limit concurrent builds per job
- Use ephemeral agents/containers
- Keep agent images preloaded

### Credentials & Security
- Store secrets in Credentials (never inline)
- Bind with `withCredentials`
- Scope credentials to projects
- Enable RBAC and restrict admin

### Maintenance
- Version shared libraries (pipelines)
- Pin plugin versions and update deliberately
- Clean workspaces and artifacts
- Monitor disk and build times

## Dependencies
```bash
docker run -p 8080:8080 -p 50000:50000 -d jenkins/jenkins:lts
```

## Examples
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
// Using credentials safely
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
// Shared library reference
@Library('my-lib@1.2') _
def result = myDeploy(stage: 'prod')
```

## Step-by-Step
1. Install Jenkins and configure the master.
2. Add agents or use cloud agents.
3. Create a pipeline job referencing the Jenkinsfile.
4. Write declarative stages for build/test/deploy.
5. Store secrets in Credentials.
6. Add post-build actions and notifications.
7. Version shared libraries.
8. Monitor disk, plugins, and build times.

## Validation
1. Pipelines run green on the target branches
2. Secrets never appear in logs
3. Builds route to correct agents
4. Failures notify and clean up
5. Plugin versions are pinned

## Troubleshooting
- Pipeline syntax errors: validate via the Snippet Generator.
- Agent offline: check agent connectivity and labels.
- Secret leaks: rotate and fix the step that printed it.