---
name: hipaa-compliance
description: "Implement HIPAA compliance in healthcare software: PHI protection, access controls, audit logging, encryption, and breach notification. Use for health IT security."
category: healthcare
tags: [hipaa, compliance, healthcare, security, phi, encryption, audit, access-control]
models: [sonnet, opus, gpt-5, gemini-2.5, glm-4.6]
version: 1.0.0
created: 2026-09-29
updated: 2026-09-29
author: ssrjkk
---

# HIPAA Compliance

> Implementing HIPAA compliance in healthcare software with PHI protection and audit logging.

## Quick Start

```python
import hashlib
import hmac
import json
import logging
from datetime import datetime
from functools import wraps

class HIPAACompliance:
    """Core HIPAA compliance utilities for healthcare applications."""

    def __init__(self, organization_id: str):
        self.organization_id = organization_id
        self.audit_logger = logging.getLogger('hipaa.audit')

    def hash_phi(self, value: str, salt: str = "") -> str:
        """One-way hash for PHI (useful for analytics without exposing data)."""
        return hashlib.sha256(f"{salt}{value}".encode()).hexdigest()

    def mask_phi(self, value: str, visible_chars: int = 4) -> str:
        """Mask PHI for display (e.g., SSN: ***-**-1234)."""
        if len(value) <= visible_chars:
            return '*' * len(value)
        return '*' * (len(value) - visible_chars) + value[-visible_chars:]
```

## When to Use

- Building healthcare applications that handle Protected Health Information (PHI)
- When you need to comply with HIPAA Privacy and Security Rules
- Implementing access controls and audit logging for health data
- Preparing for HIPAA audits or risk assessments

## Step-by-Step

### 1. Access Control

```python
from enum import Enum
from dataclasses import dataclass

class Role(Enum):
    PHYSICIAN = "physician"
    NURSE = "nurse"
    ADMIN = "admin"
    BILLING = "billing"
    PATIENT = "patient"

@dataclass
class AccessPolicy:
    allowed_roles: set[Role]
    requires_break_glass: bool = False
    max_access_duration_minutes: int = 480

class AccessControl:
    def __init__(self):
        self.policies: dict[str, AccessPolicy] = {}

    def define_policy(self, resource_type: str, policy: AccessPolicy):
        self.policies[resource_type] = policy

    def check_access(self, user_role: Role, resource_type: str, patient_id: str) -> bool:
        policy = self.policies.get(resource_type)
        if not policy:
            return False

        if user_role not in policy.allowed_roles:
            self._log_access_denied(user_role, resource_type, patient_id)
            return False

        return True

    def _log_access_denied(self, role: Role, resource: str, patient_id: str):
        self.audit_logger.warning(
            f"ACCESS_DENIED: role={role.value} resource={resource} patient={patient_id}"
        )
```

### 2. Audit Logging

```python
class AuditLogger:
    """HIPAA-compliant audit logging for PHI access."""

    def __init__(self, log_path: str = "audit.log"):
        self.logger = logging.getLogger('hipaa.audit')
        handler = logging.FileHandler(log_path)
        handler.setFormatter(logging.Formatter(
            '%(asctime)s | %(message)s'
        ))
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def log_access(self, user_id: str, action: str, resource_type: str,
                   resource_id: str, patient_id: str, reason: str = ""):
        entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'user_id': user_id,
            'action': action,
            'resource_type': resource_type,
            'resource_id': resource_id,
            'patient_id': patient_id,
            'reason': reason,
        }
        self.logger.info(json.dumps(entry))

    def log_modification(self, user_id: str, resource_type: str,
                         resource_id: str, changes: dict):
        entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'user_id': user_id,
            'action': 'MODIFY',
            'resource_type': resource_type,
            'resource_id': resource_id,
            'changes': list(changes.keys()),
        }
        self.logger.info(json.dumps(entry))
```

### 3. Encryption

```python
from cryptography.fernet import Fernet
import base64
import os

class PHIEncryption:
    """Encrypt PHI at rest and in transit."""

    def __init__(self, key: bytes = None):
        if key is None:
            key = Fernet.generate_key()
        self.cipher = Fernet(key)

    def encrypt(self, data: str) -> bytes:
        return self.cipher.encrypt(data.encode())

    def decrypt(self, encrypted: bytes) -> str:
        return self.cipher.decrypt(encrypted).decode()

    @staticmethod
    def generate_key() -> bytes:
        return Fernet.generate_key()

class DatabaseEncryption:
    """Column-level encryption for PHI in databases."""

    def __init__(self, encryption_key: bytes):
        self.cipher = Fernet(encryption_key)

    def encrypt_column(self, value: str) -> str:
        encrypted = self.cipher.encrypt(value.encode())
        return base64.b64encode(encrypted).decode()

    def decrypt_column(self, encrypted_b64: str) -> str:
        encrypted = base64.b64decode(encrypted_b64)
        return self.cipher.decrypt(encrypted).decode()
```

### 4. Session Management

```python
import secrets
from datetime import datetime, timedelta

class SecureSession:
    """HIPAA-compliant session management with auto-timeout."""

    MAX_SESSION_DURATION = timedelta(hours=8)
    IDLE_TIMEOUT = timedelta(minutes=15)

    def __init__(self, user_id: str):
        self.user_id = user_id
        self.session_id = secrets.token_urlsafe(32)
        self.created_at = datetime.utcnow()
        self.last_activity = datetime.utcnow()

    def is_valid(self) -> bool:
        now = datetime.utcnow()
        if now - self.created_at > self.MAX_SESSION_DURATION:
            return False
        if now - self.last_activity > self.IDLE_TIMEOUT:
            return False
        return True

    def touch(self):
        self.last_activity = datetime.utcnow()

    def require_reauth(self) -> bool:
        """Sensitive operations require re-authentication."""
        return (datetime.utcnow() - self.last_activity) > timedelta(minutes=5)
```

### 5. Breach Detection

```python
class BreachDetector:
    """Detect potential PHI breaches from access patterns."""

    def __init__(self, audit_logger: AuditLogger):
        self.audit_logger = audit_logger
        self.access_counts: dict[str, int] = {}
        self.threshold = 50  # Accesses per hour before alert

    def record_access(self, user_id: str):
        self.access_counts[user_id] = self.access_counts.get(user_id, 0) + 1

    def check_for_breach(self, user_id: str) -> bool:
        if self.access_counts.get(user_id, 0) > self.threshold:
            self.audit_logger.logger.error(
                f"POTENTIAL_BREACH: user={user_id} "
                f"access_count={self.access_counts[user_id]}"
            )
            return True
        return False
```

## Best Practices

- **Minimum necessary access** — only grant access to PHI needed for the role
- **Encrypt PHI at rest and in transit** — use AES-256 minimum
- **Log all PHI access** — who, what, when, why
- **Auto-timeout sessions** — 15 min idle, 8 hour max
- **Implement break-glass** — emergency access with enhanced logging
- **Regular risk assessments** — at least annually
- **Train all staff** — HIPAA training within 30 days of hire

## Common Pitfalls

- Storing PHI in logs or error messages
- Not encrypting database backups
- Sharing PHI over unencrypted channels (email, chat)
- Not implementing proper session timeouts
- Failing to document access policies
- Not having a breach notification plan

## Examples

### Decorator for PHI Access

```python
def require_phi_access(resource_type: str):
    """Decorator to enforce HIPAA access controls."""
    def decorator(func):
        @wraps(func)
        def wrapper(user, patient_id, *args, **kwargs):
            acl = AccessControl()
            if not acl.check_access(user.role, resource_type, patient_id):
                raise PermissionError("Access denied")

            audit = AuditLogger()
            audit.log_access(
                user_id=user.id,
                action='READ',
                resource_type=resource_type,
                resource_id=patient_id,
                patient_id=patient_id,
            )

            return func(user, patient_id, *args, **kwargs)
        return wrapper
    return decorator

@require_phi_access('PatientRecord')
def get_patient_record(user, patient_id):
    # Only runs if access is granted and logged
    return fetch_record(patient_id)
```

## Validation

```python
def test_phi_masking():
    compliance = HIPAACompliance("test-org")
    assert compliance.mask_phi("123-45-6789") == "*****6789"
    assert compliance.mask_phi("John") == "****"

def test_session_timeout():
    session = SecureSession("user123")
    assert session.is_valid()
    session.last_activity = datetime.utcnow() - timedelta(hours=9)
    assert not session.is_valid()
```
