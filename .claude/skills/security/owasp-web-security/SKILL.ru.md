---
name: owasp-web-security
description: "Harden web applications against the OWASP Top 10: injection, XSS, auth flaws, CSRF, SSRF, and insecure dependencies. Use for any web app security review."
category: security
tags: [owasp-web-security, security, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: owasp-web-security
author: ssrjkk
---
# OWASP Web Security (ОВАСП веб-безопасность)

> Укрепление веб-приложений против OWASP Top 10.

## Быстрый старт
```bash
# Сканирование зависимостей на известные уязвимости
pip-audit --format full
npm audit
# затем пройдитесь по чек-листу OWASP Top 10 по своему приложению
```

## Когда использовать
- Перед запуском или крупными релизами
- При работе с auth, платежами или PII
- После обновления зависимостей или фреймворков
- Регулярное укрепление существующих приложений

## Лучшие практики

### Инъекции
- Параметризуйте все SQL/конструкции запросов
- Экранируйте вывод под контекст (HTML, JS, URL)
- Валидируйте и whitelist'ите входы на сервере
- Используйте ORM/query builders; никогда не склеивайте запросы строками

### Аутентификация и авторизация
- Используйте проверенную auth-библиотеку (не самописную)
- Хешируйте пароли через bcrypt/argon2
- Включайте MFA для чувствительных действий
- Проверяйте авторизацию на каждом эндпоинте, а не только в UI

### XSS и CSRF
- Авто-экранирование вывода в шаблонах; санитизируйте rich content
- Ставьте CSP headers; где можно — строгие `Trusted Types`
- CSRF-токены на все state-changing запросы
- Ставьте `SameSite=Lax/Strict` на куки

### Данные и зависимости
- Шифруйте данные в транзите (TLS) и в покое
- Держите зависимости обновлёнными; сканируйте регулярно
- Ограничивайте SSRF: блокируйте приватные диапазоны, пиньте редиректы
- Ограничивайте загрузку файлов: тип, размер и исполнение

## Зависимости
```bash
pip install bandit pip-audit
npm install -g npm-audit-resolver
# сканеры: semgrep, gitleaks, trivy
```

## Примеры
```python
# Безопасный SQL без инъекций
cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
```
```python
# Экранирование вывода в шаблонах (Django авто-экранирует)
# context = {"user_input": user_input}
# Template: {{ user_input }}   # авто-экранирован
```
```python
# CSRF защита (Django middleware по умолчанию)
from django.views.decorators.csrf import csrf_exempt
# никогда не используйте @csrf_exempt на state-changing вьюхах
```
```python
# SSRF защита
import ipaddress, socket

def safe_fetch(url: str) -> str:
    host = urlparse(url).hostname
    ip = ipaddress.ip_address(socket.gethostbyname(host))
    if not ip.is_private:          # блокировка локальных/приватных диапазонов
        return requests.get(url).text
    raise ValueError("Blocked private address")
```

## Пошаговое руководство
1. Запустите сканеры зависимостей (pip-audit/npm audit/trivy).
2. Проверьте authN/authZ: хранение паролей, сессии, роли.
3. Проверьте все входы: валидация, экранирование, параметризация.
4. Аудит CSRF, XSS и CSP headers.
5. Проверьте загрузки файлов, SSRF-векторы и редиректы.
6. Проверьте секреты: gitleaks и конфиг через env.
7. Укрепите заголовки: CSP, HSTS, X-Content-Type-Options.
8. Пересканируйте после фиксов; задокументируйте остаточные риски.

## Валидация
1. В коде нет точек инъекций по данным скана
2. Пароли хранятся с сильным хешем
3. Авторизация enforce'ится на сервере на всех эндпоинтах
4. CSP и security headers присутствуют
5. Скан зависимостей не показывает критических уязвимостей

## Устранение неполадок
- Сломанные auth-флоу: тестируйте с теми же browser/network правилами, что и пользователи.
- False positives: проверяйте утверждения сканеров в безопасном окружении.
- Риск легаси-кода: приоритизируйте по открытой поверхности атаки.