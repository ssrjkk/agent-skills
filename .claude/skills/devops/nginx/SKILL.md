---
name: nginx
description: "Configure and operate Nginx: reverse proxy, load balancing, TLS, caching, and security headers. Use for web serving and proxying."
category: devops
tags: [nginx, reverse-proxy, load-balancing, tls, caching, web-server]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-09-29
updated: 2026-09-29
author: ssrjkk
---
# Nginx

> Reverse proxying, load balancing, and TLS with Nginx.

## Quick Start
```bash
sudo apt install nginx
sudo nginx -t && sudo systemctl reload nginx
```

## When to Use
- Reverse proxy in front of app servers
- Load balancing across backends
- TLS termination and static asset serving
- Caching and rate limiting

## Best Practices

### Proxy Setup
- Use `upstream` blocks for backend groups
- Set proxy timeouts and headers explicitly
- Pass the original host/IP via `proxy_set_header`
- Enable keepalive to upstreams

### TLS
- Terminate TLS at Nginx with a current cert
- Redirect HTTP to HTTPS
- Set strong protocols and ciphers
- Auto-renew with certbot

### Performance
- Serve static assets directly with expires
- Enable gzip for compressible responses
- Cache responses with `proxy_cache`
- Tune worker_processes and connections

### Security
- Add security headers (HSTS, X-Frame-Options)
- Rate-limit sensitive endpoints
- Hide server version
- Restrict access where needed

## Dependencies
```bash
sudo apt install nginx
sudo nginx -t
```

## Examples
```nginx
# Reverse proxy to an app
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
# Load balancing across backends
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
# Static caching + gzip
location /static/ {
    alias /var/www/app/static/;
    expires 30d;
    gzip on;
}
```

## Step-by-Step
1. Install Nginx and check the default config.
2. Add an upstream for your backends.
3. Write a server block for your domain.
4. Terminate TLS (certbot) and redirect HTTP.
5. Set proxy headers and timeouts.
6. Add caching, gzip, and static serving.
7. Harden with security headers and limits.
8. Test with `nginx -t` and reload.

## Validation
1. `nginx -t` passes
2. Requests reach backends with correct headers
3. HTTPS works with a valid cert
4. Static assets cache correctly
5. Load balancer distributes across upstreams

## Troubleshooting
- 502 Bad Gateway: backend down or wrong address.
- Slow proxying: check timeouts and keepalive.
- Cert errors: renew and check permissions.