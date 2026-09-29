---
name: hipaa-compliance
description: "Реализация соответствия HIPAA в программном обеспечении здравоохранения: защита PHI, контроль доступа, аудит-логирование, шифрование и уведомление о нарушениях. Для безопасности медицинских ИТ."
category: healthcare
tags: [hipaa, compliance, healthcare, security, phi, encryption, audit, access-control]
models: [sonnet, opus, gpt-5, gemini-2.5, glm-4.6]
version: 1.0.0
created: 2026-09-29
updated: 2026-09-29
author: ssrjkk
---

# Соответствие HIPAA

> Реализация соответствия HIPAA в программном обеспечении здравоохранения с защитой PHI и аудит-логированием.

## Быстрый старт

```python
import hashlib
import hmac
import json
import logging
from datetime import datetime
from functools import wraps

class HIPAACompliance:
    """Основные утилиты соответствия HIPAA для медицинских приложений."""

    def __init__(self, organization_id: str):
        self.organization_id = organization_id
        self.audit_logger = logging.getLogger('hipaa.audit')

    def hash_phi(self, value: str, salt: str = "") -> str:
        """Односторонний хеш для PHI (полезно для аналитики без раскрытия данных)."""
        return hashlib.sha256(f"{salt}{value}".encode()).hexdigest()

    def mask_phi(self, value: str, visible_chars: int = 4) -> str:
        """Маскировка PHI для отображения (например, SSN: ***-**-1234)."""
        if len(value) <= visible_chars:
            return '*' * len(value)
        return '*' * (len(value) - visible_chars) + value[-visible_chars:]
```

## Когда использовать

- Создание медицинских приложений, работающих с защищённой медицинской информацией (PHI)
- Когда нужно соответствие Privacy и Security Rules HIPAA
- Реализация контроля доступа и аудит-логирования для медицинских данных
- Подготовка к аудитам HIPAA или оценкам рисков

## Пошагово

### 1. Контроль доступа

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

### 2. Аудит-логирование

```python
class AuditLogger:
    """Аудит-логирование PHI в соответствии с HIPAA."""

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

### 3. Шифрование

```python
from cryptography.fernet import Fernet
import base64
import os

class PHIEncryption:
    """Шифрование PHI в покое и при передаче."""

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
    """Шифрование на уровне столбцов для PHI в базах данных."""

    def __init__(self, encryption_key: bytes):
        self.cipher = Fernet(encryption_key)

    def encrypt_column(self, value: str) -> str:
        encrypted = self.cipher.encrypt(value.encode())
        return base64.b64encode(encrypted).decode()

    def decrypt_column(self, encrypted_b64: str) -> str:
        encrypted = base64.b64decode(encrypted_b64)
        return self.cipher.decrypt(encrypted).decode()
```

### 4. Управление сессиями

```python
import secrets
from datetime import datetime, timedelta

class SecureSession:
    """Управление сессиями в соответствии с HIPAA с автотаймаутом."""

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
        """Чувствительные операции требуют повторной аутентификации."""
        return (datetime.utcnow() - self.last_activity) > timedelta(minutes=5)
```

### 5. Обнаружение нарушений

```python
class BreachDetector:
    """Обнаружение потенциальных нарушений PHI по паттернам доступа."""

    def __init__(self, audit_logger: AuditLogger):
        self.audit_logger = audit_logger
        self.access_counts: dict[str, int] = {}
        self.threshold = 50  # Доступов в час перед оповещением

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

## Лучшие практики

- **Минимально необходимый доступ** — предоставляйте доступ к PHI только по необходимости для роли
- **Шифруйте PHI в покое и при передаче** — используйте минимум AES-256
- **Логируйте весь доступ к PHI** — кто, что, когда, почему
- **Автотаймаут сессий** — 15 мин простоя, 8 часов максимум
- **Реализуйте break-glass** — экстренный доступ с расширенным логированием
- **Регулярные оценки рисков** — минимум ежегодно
- **Обучайте весь персонал** — обучение HIPAA в течение 30 дней после найма

## Типичные ошибки

- Хранение PHI в логах или сообщениях об ошибках
- Отсутствие шифрования резервных копий базы данных
- Передача PHI по незашифрованным каналам (email, чат)
- Отсутствие правильных таймаутов сессий
- Недокументирование политик доступа
- Отсутствие плана уведомления о нарушениях

## Примеры

### Декоратор для доступа к PHI

```python
def require_phi_access(resource_type: str):
    """Декоратор для принудительного контроля доступа HIPAA."""
    def decorator(func):
        @wraps(func)
        def wrapper(user, patient_id, *args, **kwargs):
            acl = AccessControl()
            if not acl.check_access(user.role, resource_type, patient_id):
                raise PermissionError("Доступ запрещён")

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
    # Выполняется только если доступ предоставлен и залогирован
    return fetch_record(patient_id)
```

## Валидация

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
