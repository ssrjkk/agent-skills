---
name: hl7-fhir
description: "Создание интеграций в здравоохранении с HL7 FHIR: ресурсы, операции, SMART on FHIR приложения и обмен клиническими данными. Для интероперабельности медицинских ИТ."
category: healthcare
tags: [hl7, fhir, healthcare, interoperability, smart-on-fhir, clinical, api, resources]
models: [sonnet, opus, gpt-6, gemini-3, glm-5]
version: 1.0.0
created: 2026-09-29
updated: 2026-09-29
author: ssrjkk
---

# HL7 FHIR

> Создание интеграций в здравоохранении с ресурсами HL7 FHIR и приложениями SMART on FHIR.

## Быстрый старт

```python
import requests

class FHIRClient:
    def __init__(self, base_url: str, access_token: str = None):
        self.base_url = base_url.rstrip('/')
        self.headers = {
            'Content-Type': 'application/fhir+json',
            'Accept': 'application/fhir+json',
        }
        if access_token:
            self.headers['Authorization'] = f'Bearer {access_token}'

    def read(self, resource_type: str, id: str) -> dict:
        """Чтение ресурса FHIR по ID."""
        resp = requests.get(
            f'{self.base_url}/{resource_type}/{id}',
            headers=self.headers
        )
        resp.raise_for_status()
        return resp.json()

    def search(self, resource_type: str, params: dict = None) -> dict:
        """Поиск ресурсов FHIR."""
        resp = requests.get(
            f'{self.base_url}/{resource_type}',
            params=params or {},
            headers=self.headers
        )
        resp.raise_for_status()
        return resp.json()

    def create(self, resource: dict) -> dict:
        """Создание нового ресурса FHIR."""
        resp = requests.post(
            f'{self.base_url}/{resource["resourceType"]}',
            json=resource,
            headers=self.headers
        )
        resp.raise_for_status()
        return resp.json()

# Пример: получение Patient
client = FHIRClient('https://fhir.example.com/fhir')
patient = client.read('Patient', '12345')
print(f"Пациент: {patient['name'][0]['family']}")
```

## Когда использовать

- Создание интеграций с EHR (Epic, Cerner и др.)
- Создание приложений SMART on FHIR для клинических рабочих процессов
- Обмен клиническими данными между системами
- Когда нужна интероперабельность медицинских данных

## Пошагово

### 1. Понимание ресурсов FHIR

Основные ресурсы, с которыми вы будете работать:

```python
# Ресурс Patient
patient = {
    "resourceType": "Patient",
    "id": "12345",
    "name": [{
        "family": "Smith",
        "given": ["John"]
    }],
    "gender": "male",
    "birthDate": "1990-01-15"
}

# Observation (лабораторный результат)
observation = {
    "resourceType": "Observation",
    "status": "final",
    "code": {
        "coding": [{
            "system": "http://loinc.org",
            "code": "2339-0",
            "display": "Glucose [Mass/volume] in Blood"
        }]
    },
    "subject": {"reference": "Patient/12345"},
    "valueQuantity": {
        "value": 95,
        "unit": "mg/dL"
    }
}
```

### 2. Авторизация SMART on FHIR

```python
import secrets
from urllib.parse import urlencode

class SMARTAuth:
    def __init__(self, client_id: str, client_secret: str, fhir_url: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.fhir_url = fhir_url

    def get_auth_url(self, redirect_uri: str, scopes: list[str]) -> str:
        """Генерация URL авторизации OAuth2."""
        params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': redirect_uri,
            'scope': ' '.join(scopes),
            'state': secrets.token_urlsafe(32),
            'aud': self.fhir_url,
        }
        return f'{self.fhir_url}/auth/authorize?{urlencode(params)}'

    def exchange_code(self, code: str, redirect_uri: str) -> dict:
        """Обмен кода авторизации на токен доступа."""
        resp = requests.post(f'{self.fhir_url}/auth/token', data={
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': redirect_uri,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        })
        return resp.json()
```

### 3. Клинические запросы

```python
def get_patient_labs(client: FHIRClient, patient_id: str) -> list[dict]:
    """Получение всех лабораторных результатов пациента."""
    bundle = client.search('Observation', {
        'subject': f'Patient/{patient_id}',
        'category': 'laboratory',
        '_sort': '-date',
    })
    return bundle.get('entry', [])

def get_patient_medications(client: FHIRClient, patient_id: str) -> list[dict]:
    """Получение активных назначений пациента."""
    bundle = client.search('MedicationRequest', {
        'subject': f'Patient/{patient_id}',
        'status': 'active',
    })
    return bundle.get('entry', [])

def get_patient_conditions(client: FHIRClient, patient_id: str) -> list[dict]:
    """Получение активных состояний (диагнозов) пациента."""
    bundle = client.search('Condition', {
        'subject': f'Patient/{patient_id}',
        'clinical-status': 'active',
    })
    return bundle.get('entry', [])
```

### 4. Массовые данные FHIR

```python
def kick_off_bulk_export(client: FHIRClient, output_format: str = 'application/fhir+ndjson'):
    """Инициация массового экспорта FHIR Bulk Data."""
    resp = requests.get(
        f'{client.base_url}/$export',
        headers={
            **client.headers,
            'Accept': output_format,
            'Prefer': 'respond-async',
        }
    )
    return resp.headers.get('Content-Location')  # Опрос этого URL для статуса

def check_bulk_status(status_url: str) -> dict:
    """Проверка статуса массового экспорта данных."""
    resp = requests.get(status_url)
    if resp.status_code == 200:
        return resp.json()  # Содержит URL для скачивания
    return {'status': 'in-progress'}
```

### 5. Подписки

```python
def create_subscription(client: FHIRClient, criteria: str, endpoint: str) -> dict:
    """Создание подписки FHIR для уведомлений в реальном времени."""
    subscription = {
        "resourceType": "Subscription",
        "status": "requested",
        "criteria": criteria,
        "channel": {
            "type": "rest-hook",
            "endpoint": endpoint,
            "payload": "application/fhir+json",
        }
    }
    return client.create(subscription)

# Пример: подписка на новые Observation для пациента
create_subscription(
    client,
    "Observation?subject=Patient/12345",
    "https://myapp.example.com/fhir-webhook"
)
```

## Лучшие практики

- **Используйте официальные схемы FHIR** для валидации
- **Обрабатывайте пагинацию** в результатах поиска (Bundle links)
- **Кэшируйте ресурсы** при необходимости для снижения нагрузки на сервер
- **Используйте _summary и _elements** для уменьшения размера payload
- **Реализуйте логику повторов** для временных сбоев
- **Валидируйте токены** при каждом запросе в production

## Типичные ошибки

- Отсутствие обработки пагинации Bundle (пропущенные результаты)
- Игнорирование различий версий FHIR (R4 vs R5)
- Отсутствие валидации ссылок на ресурсы перед использованием
- Забывают учитывать часовой пояс в полях даты/времени
- Отсутствие правильной реализации обновления токенов OAuth2

## Примеры

### Сводка по пациенту

```python
def build_patient_summary(client: FHIRClient, patient_id: str) -> dict:
    """Создание комплексной сводки по пациенту."""
    patient = client.read('Patient', patient_id)
    labs = get_patient_labs(client, patient_id)
    meds = get_patient_medications(client, patient_id)
    conditions = get_patient_conditions(client, patient_id)

    return {
        'patient': patient['name'][0],
        'recent_labs': [e['resource'] for e in labs[:10]],
        'active_medications': [e['resource'] for e in meds],
        'active_conditions': [e['resource'] for e in conditions],
    }
```

## Валидация

```python
def test_fhir_client():
    client = FHIRClient('https://hapi.fhir.org/baseR4')
    patient = client.read('Patient', 'example')
    assert patient['resourceType'] == 'Patient'

def test_resource_validation():
    patient = {"resourceType": "Patient", "name": [{"family": "Test"}]}
    assert patient['resourceType'] == 'Patient'
```
