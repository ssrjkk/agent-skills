---
name: nginx
description: "Configure and operate Nginx: reverse proxy, load balancing, TLS, caching, and security headers. Use for web serving and proxying."
category: devops
tags: [nginx, devops, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: nginx
author: ssrjkk
---
# Nginx (Энджинкс)

> Reverse proxy, балансировка и TLS через Nginx.

## Быстрый старт
```bash
sudo apt install nginx
sudo nginx -t && sudo systemctl reload nginx
```

## Когда использовать
- Reverse proxy перед app-серверами
- Балансировка нагрузки между бэкендами
- TLS termination и раздача статики
- Кэширование и rate limiting

## Лучшие практики

### Прокси
- `upstream` блоки для групп бэкендов
- Таймауты и заголовки прокси явно
- Оригинальный host/IP через `proxy_set_header`
- keepalive к апстримам

### TLS
- TLS termination с актуальным сертификатом
- Редирект HTTP на HTTPS
- Сильные протоколы и шифры
- Авто-обновление через certbot

### Производительность
- Статика напрямую с expires
- gzip для сжимаемых ответов
- `proxy_cache` для кэша ответов
- Настройка worker_processes и соединений

### Безопасность
- Security headers (HSTS, X-Frame-Options)
- Rate-limit чувствительных эндпоинтов
- Скрывайте версию сервера
- Ограничивайте доступ при необходимости

## Зависимости
```bash
sudo apt install nginx
sudo nginx -t
```

## Примеры
```nginx
# Reverse proxy к приложению
server {
    listen 80;
    server_name app.example.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```
```nginx
# Балансировка между бэкендами
upstream app {
    server 10.0.0.1:8000;
    server 10.0.0.2:8000;
    keepalive 32;
}

server {
    listen 443 ssl;
    location / {
        proxy_pass http://app;
    }
}
```
```nginx
# TLS termination
server {
    listen 443 ssl http2;
    server_name app.example.com;
    ssl_certificate /etc/letsencrypt/live/app/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/app/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    add_header Strict-Transport-Security "max-age=31536000" always;
}
```
```nginx
# Кэш статики + gzip
location /static/ {
    alias /var/www/app/static/;
    expires 30d;
    gzip on;
}
```

## Пошаговое руководство
1. Установите Nginx и проверьте дефолтный конфиг.
2. Добавьте upstream для бэкендов.
3. Напишите server block для домена.
4. TLS (certbot) и редирект HTTP.
5. Заголовки и таймауты прокси.
6. Кэш, gzip и раздача статики.
7. Укрепите security headers и лимитами.
8. Проверьте `nginx -t` и перезагрузите.

## Валидация
1. `nginx -t` проходит
2. Запросы доходят до бэкендов с корректными заголовками
3. HTTPS работает с валидным сертом
4. Статика кэшируется корректно
5. Балансировщик распределяет по апстримам

## Устранение неполадок
- 502 Bad Gateway: бэкенд упал или неверный адрес.
- Медленный прокси: проверьте таймауты и keepalive.
- Ошибки серта: обновите и проверьте права.