---
name: ansible
description: "Automate infrastructure with Ansible: playbooks, roles, inventory, modules, and idempotency. Use for config management and provisioning."
category: devops
tags: [ansible, automation, playbooks, roles, inventory, idempotency]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-09-29
updated: 2026-09-29
author: ssrjkk
---
# Ansible

> Automating servers with Ansible playbooks and roles.

## Quick Start
```bash
pip install ansible
ansible -i hosts all -m ping
```

## When to Use
- Configuration management across servers
- Repeatable provisioning and deploys
- Orchestrating multi-host tasks
- Idempotent server setup

## Best Practices

### Playbooks & Roles
- Structure with roles (tasks, handlers, vars, templates)
- Keep playbooks thin; logic in roles
- Use handlers for service reloads
- Name every task for readable output

### Idempotency
- Write tasks that converge to the desired state
- Avoid commands with side effects; prefer modules
- Use `creates`/`when` guards where needed
- Re-running playbooks should be safe

### Inventory & Variables
- Use group_vars and host_vars for config
- Encrypt secrets with ansible-vault
- Use inventory plugins for dynamic hosts
- Prefer variables over hardcoding

### Safety
- Run `--check` before applying
- Limit blast radius with `--limit` and serial
- Use become carefully and scoped
- Version control playbooks and roles

## Dependencies
```bash
pip install ansible
ansible --version
```

## Examples
```yaml
# Playbook with a role
- hosts: webservers
  become: true
  roles:
    - nginx
```
```yaml
# Simple playbook
- hosts: all
  tasks:
    - name: Ensure nginx installed
      apt:
        name: nginx
        state: present
    - name: Start nginx
      service:
        name: nginx
        state: started
        enabled: true
```
```yaml
# Role structure
# roles/nginx/tasks/main.yml
- name: Install nginx
  apt: { name: nginx, state: present }
  notify: reload nginx

# roles/nginx/handlers/main.yml
- name: reload nginx
  service: { name: nginx, state: reloaded }
```
```bash
# Check mode + apply
ansible-playbook site.yml --check
ansible-playbook site.yml --limit web-01
```

## Step-by-Step
1. Define the inventory and group_vars.
2. Structure logic into roles.
3. Write idempotent tasks using modules.
4. Add handlers for reloads.
5. Encrypt secrets with ansible-vault.
6. Run `--check` then apply with limits.
7. Version control playbooks and roles.
8. Schedule with AWX/Ansible Tower or CI.

## Validation
1. Playbooks are idempotent (re-run changes nothing)
2. `--check` reports expected changes
3. Secrets are encrypted in vault
4. Handlers fire on changes only
5. Deploys succeed across the inventory

## Troubleshooting
- Changed on every run: find non-idempotent task.
- Become errors: check sudo rules and become_method.
- Unreachable: verify SSH keys and inventory addresses.