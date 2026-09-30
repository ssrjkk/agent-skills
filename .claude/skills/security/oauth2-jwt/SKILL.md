---
name: oauth2-jwt
description: "Implements OAuth 2.0 authentication and JWT-based authorization with refresh tokens. Use for secure API access."
category: security
tags: [oauth2, jwt, auth, security, authentication]
models: [sonnet, opus]
version: 1.0.0
created: 2026-05-14
updated: 2026-09-29
---
# OAuth2 & JWT

> Secure API authentication with OAuth 2.0 and JSON Web Tokens.

## Quick Start
```typescript
import jwt from 'jsonwebtoken';
import bcrypt from 'bcrypt';

// Login
const user = await db.user.findUnique({ where: { email } });
const valid = await bcrypt.compare(password, user.password);
if (!valid) throw new Error('Invalid credentials');

// Generate tokens
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

## When to Use
- API authentication and authorization
- Single sign-on (SSO) with OAuth providers
- Not for server-to-server with API keys

## Best Practices
- Store passwords hashed (bcrypt/argon2), never plaintext.
- Use short-lived access tokens (15m) and rotating refresh tokens.
- Store refresh tokens server-side or in httpOnly cookies.
- Verify signature, expiry, issuer, and audience on every token.
- Use the Authorization Code + PKCE flow for browser clients.
- Rotate signing keys and support JWKS with caching.

## Step-by-Step Instructions
1. Install packages: `npm install jsonwebtoken bcrypt`
2. Set up user model with hashed passwords
3. Create login endpoint returning access + refresh tokens
4. Add auth middleware to protected routes
5. Implement token refresh with rotation
6. Add scopes and audience checks

## Dependencies
```bash
npm install jsonwebtoken bcrypt
# For OAuth providers: passport, passport-google-oauth20, etc.
```

## Examples
Input: Login with email/password → Output: `{ accessToken, refreshToken, expiresIn }`

```typescript
// Refresh with rotation
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
// Authorization check with scopes
function requireScope(scope: string) {
  return (req, res, next) => {
    if (!req.user?.scopes?.includes(scope)) {
      return res.status(403).json({ error: "insufficient_scope" });
    }
    next();
  };
}
```

## Resources
- [JWT.io](https://jwt.io/)
- [OAuth 2.0 Spec](https://oauth.net/2/)
- [Examples](./examples/)

## Troubleshooting
- **JWT `kid` mismatch** — the signing key rotated but the client cached
  the old JWKS. Refresh the key set and honor `cache-control` on the JWKS.
- **`exp` claims rejected after a clock skew** — allow leeway (~30s) on
  verification and compare with the issuer's `nbf`/`iat`, not wall time.
- **Audience leaks cross-app** — tokens minted for one audience validate
  elsewhere. Pin `aud` per client and reject tokens without an `aud` claim.
- **Refresh tokens stolen in localStorage** — never store them in the
  browser. Use httpOnly, SameSite cookies or a backend session.

## Validation
1. Tokens sign and verify correctly
2. Expired tokens are rejected
3. Refresh tokens issue new access tokens
