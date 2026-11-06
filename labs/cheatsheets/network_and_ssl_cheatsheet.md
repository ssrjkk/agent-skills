# Шпаргалка: Сеть, SSL/TLS и Туннелирование

## Диагностика времени ответа HTTP через `curl`
Вывод полной раскладки задержек (DNS, TCP, TLS, TTFB):
```bash
curl -o /dev/null -s -w "DNS: %{time_namelookup}s | Connect: %{time_connect}s | TLS: %{time_appconnect}s | TTFB: %{time_starttransfer}s | Total: %{time_total}s | Code: %{http_code}\n" https://example.com
```
Проверка запроса в обход DNS (напрямую на нужный IP балансировщика с сохранением SNI):
```bash
curl -v --resolve example.com:443:10.0.0.50 https://example.com
```

## Работа с сертификатами (OpenSSL)
- **Проверить срок действия и цепочку сертификата на удаленном сервере:**
  ```bash
  echo | openssl s_client -servername example.com -connect example.com:443 2>/dev/null | openssl x509 -noout -dates -issuer -subject
  ```
- **Прочитать локальный файл сертификата (`crt`/`pem`):**
  ```bash
  openssl x509 -in cert.pem -text -noout
  ```
- **Проверить, что приватный ключ соответствует сертификату (хэши должны совпасть):**
  ```bash
  openssl x509 -noout -modulus -in cert.pem | openssl md5
  openssl rsa -noout -modulus -in privkey.pem | openssl md5
  ```

## SSH-туннелирование и проброс портов
- **Local Port Forwarding** (пробросить закрытую БД `10.0.1.15:5432` через бастион-хост на свой `localhost:5432`):
  ```bash
  ssh -L 5432:10.0.1.15:5432 user@bastion-host -N
  ```
- **Подключение к приватному серверу прозрачно через Jump Host:**
  ```bash
  ssh -J user@bastion-host user@10.0.1.20
  ```
- **SOCKS5 прокси через SSH** (весь трафик браузера через удаленный сервер):
  ```bash
  ssh -D 1080 -q -C -N user@remote-server
  ```
