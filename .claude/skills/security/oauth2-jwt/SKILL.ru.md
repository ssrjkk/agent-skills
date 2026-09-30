---
name: oauth2-jwt
description: "Implements OAuth 2.0 authentication and JWT-based authorization with refresh tokens. Use for secure API access."
category: security
tags: [oauth2-jwt, security, russian]
models: [sonnet, opus]
version: "1.0"
language: ru
original: oauth2-jwt
---
# OAuth2 & JWT

> Безопасная аутентификация API с OAuth 2.0 и JSON Web Tokens.

## Быстрый старт
```typescript
import jwt from 'jsonwebtoken';
import bcrypt from 'bcrypt';

// Логин
const user = await db.user.findUnique({ where: { email } });
const valid = await bcrypt.compare(password, user.password);
if (!valid) throw new Error('Invalid credentials');

// Генерация токенов
const accessToken = jwt.sign(
  { userId: user.id, role: user.role },
  process.env.JWT_SECRET!,
  { expiresIn: '15m' }
);
const refreshToken = jwt.sign(
  { userId: user.id },
  process.env.JWT_REFRESH_SECRET!,
  { expiresIn: '7d' }
);

// Middleware
function authMiddleware(req, res, next) {
  const token = req.headers.authorization?.split(' ')[1];
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET!);
    req.user = decoded;
    next();
  } catch {
    res.status(401).json({ error: 'Invalid token' });
  }
}
```

## Когда использовать
- Аутентификация и авторизация API
- Single sign-on (SSO) c OAuth-провайдерами
- Не для server-to-server с API-ключами

## Лучшие практики
- Пароли хэшированы (bcrypt/argon2), никогда в открытом виде.
- Короткоживущие access-токены (15m) и ротация refresh.
- Refresh-токены на сервере или в httpOnly cookies.
- Проверяйте сигнатуру, expiry, issuer и audience на каждом токене.
- Для браузерных клиентов — Authorization Code + PKCE.
- Ротация подписывающих ключей с JWKS и кэшированием.

## Пошаговые инструкции
1. Установите пакеты: `npm install jsonwebtoken bcrypt`
2. Настройте модель пользователя с хэшированными паролями
3. Создайте login-эндпоинт с access + refresh токенами
4. Добавьте auth middleware на защищённые маршруты
5. Реализуйте refresh с ротацией
6. Добавьте scopes и проверку audience

## Зависимости
```bash
npm install jsonwebtoken bcrypt
# Для OAuth-провайдеров: passport, passport-google-oauth20 и др.
```

## Примеры
Вход: логин email/password → Выход: `{ accessToken, refreshToken, expiresIn }`

```typescript
// Refresh с ротацией
router.post("/refresh", async (req, res) => {
  const old = req.body.refreshToken;
  const decoded = jwt.verify(old, process.env.JWT_REFRESH_SECRET!);
  if (!isStored(old)) return res.status(401).json({ error: "revoked" });
  revoke(old);
  const accessToken = jwt.sign(
    { userId: decoded.userId },
    process.env.JWT_SECRET!,
    { expiresIn: "15m" }
  );
  const refreshToken = jwt.sign({ userId: decoded.userId }, process.env.JWT_REFRESH_SECRET!, { expiresIn: "7d" });
  res.json({ accessToken, refreshToken });
});
```
```typescript
// Проверка авторизации со scopes
function requireScope(scope: string) {
  return (req, res, next) => {
    if (!req.user?.scopes?.includes(scope)) {
      return res.status(403).json({ error: "insufficient_scope" });
    }
    next();
  };
}
```

## Ресурсы
- [JWT.io](https://jwt.io/)
- [OAuth 2.0 Spec](https://oauth.net/2/)
- [Examples](./examples/)

## Устранение неполадок
- **Не совпадает `kid` в JWT** — ротация ключей подписи, а клиент кэшировал
  старый JWKS. Обновите набор ключей и уважайте `cache-control` на JWKS.
- **Ревью `exp` после рассинхрона часов** — дайте допуск (~30s) при
  верификации и сравнивайте с `nbf`/`iat` эмитента, а не с локальным временем.
- **Audience утекает между приложениями** — токены одного клиента
  валидируются в другом. Привяжите `aud` на клиента и отклоняйте без него.
- **Refresh-токен украден из localStorage** — не храните его в браузере.
  Используйте httpOnly/SameSite-cookie или серверную сессию.

## Валидация
1. Токены подписываются и верифицируются корректно
2. Истёкшие токены отклоняются
3. Refresh-токены выдают новые access-токены
