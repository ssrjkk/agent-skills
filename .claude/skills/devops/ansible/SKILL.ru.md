---
name: ansible
description: "Automate infrastructure with Ansible: playbooks, roles, inventory, modules, and idempotency. Use for config management and provisioning."
category: devops
tags: [ansible, devops, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: ansible
author: ssrjkk
---
# Ansible (Ансибл)

> Автоматизация серверов через playbooks и роли Ansible.

## Быстрый старт
```bash
pip install ansible
ansible -i hosts all -m ping
```

## Когда использовать
- Управление конфигурацией на многих серверах
- Повторяемый провижининг и деплой
- Оркестрация multi-host задач
- Идемпотентная настройка серверов

## Лучшие практики

### Playbooks и роли
- Структура через роли (tasks, handlers, vars, templates)
- Playbooks тонкие; логика в ролях
- Handlers для перезагрузки сервисов
- Именуйте каждую задачу для читаемого вывода

### Идемпотентность
- Задачи сходятся к желаемому состоянию
- Избегайте команд с сайд-эффектами; используйте модули
- Guard-условия `creates`/`when` где нужно
- Повторный прогон безопасен

### Инвентарь и переменные
- group_vars и host_vars для конфига
- Секреты через ansible-vault
- Inventory plugins для динамических хостов
- Переменные вместо хардкода

### Безопасность
- `--check` перед применением
- Ограничьте blast radius через `--limit` и serial
- become аккуратно и с областью
- Playbooks и роли в git

## Зависимости
```bash
pip install ansible
ansible --version
```

## Примеры
```yaml
# Playbook с ролью
- hosts: webservers
  become: true
  roles:
    - nginx
```
```yaml
# Простой playbook
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
# Структура роли
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

## Пошаговое руководство
1. Определите инвентарь и group_vars.
2. Структурируйте логику в роли.
3. Пишите идемпотентные задачи через модули.
4. Добавьте handlers для перезагрузок.
5. Шифруйте секреты через ansible-vault.
6. Сначала `--check`, затем apply с лимитами.
7. Playbooks и роли в git.
8. Планируйте через AWX/Tower или CI.

## Валидация
1. Playbooks идемпотентны (повторный прогон ничего не меняет)
2. `--check` показывает ожидаемые изменения
3. Секреты зашифрованы в vault
4. Handlers срабатывают только при изменениях
5. Деплои проходят по всему инвентарю

## Устранение неполадок
- Изменения при каждом прогоне: найдите неидемпотентную задачу.
- Ошибки become: проверьте sudo-правила и become_method.
- Unreachable: проверьте SSH-ключи и адреса инвентаря.