---
name: hl7-fhir
description: "Build healthcare integrations with HL7 FHIR: resources, operations, SMART on FHIR apps, and clinical data exchange. Use for health IT interoperability."
category: healthcare
tags: [hl7, fhir, healthcare, interoperability, smart-on-fhir, clinical, api, resources]
models: [sonnet, opus, gpt-5, gemini-2.5, glm-4.6]
version: 1.0.0
created: 2026-09-29
updated: 2026-09-29
author: ssrjkk
---

# HL7 FHIR

> Building healthcare integrations with HL7 FHIR resources and SMART on FHIR apps.

## Quick Start

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
        """Read a FHIR resource by ID."""
        resp = requests.get(
            f'{self.base_url}/{resource_type}/{id}',
            headers=self.headers
        )
        resp.raise_for_status()
        return resp.json()

    def search(self, resource_type: str, params: dict = None) -> dict:
        """Search FHIR resources."""
        resp = requests.get(
            f'{self.base_url}/{resource_type}',
            params=params or {},
            headers=self.headers
        )
        resp.raise_for_status()
        return resp.json()

    def create(self, resource: dict) -> dict:
        """Create a new FHIR resource."""
        resp = requests.post(
            f'{self.base_url}/{resource["resourceType"]}',
            json=resource,
            headers=self.headers
        )
        resp.raise_for_status()
        return resp.json()

# Example: fetch a Patient
client = FHIRClient('https://fhir.example.com/fhir')
patient = client.read('Patient', '12345')
print(f"Patient: {patient['name'][0]['family']}")
```

## When to Use

- Building EHR integrations (Epic, Cerner, etc.)
- Creating SMART on FHIR apps for clinical workflows
- Exchanging clinical data between systems
- When you need healthcare data interoperability

## Step-by-Step

### 1. Understanding FHIR Resources

Common resources you'll work with:

```python
# Patient resource
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

# Observation (lab result)
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

### 2. SMART on FHIR Auth

```python
import secrets
from urllib.parse import urlencode

class SMARTAuth:
    def __init__(self, client_id: str, client_secret: str, fhir_url: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.fhir_url = fhir_url

    def get_auth_url(self, redirect_uri: str, scopes: list[str]) -> str:
        """Generate OAuth2 authorization URL."""
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
        """Exchange authorization code for access token."""
        resp = requests.post(f'{self.fhir_url}/auth/token', data={
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': redirect_uri,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        })
        return resp.json()
```

### 3. Clinical Queries

```python
def get_patient_labs(client: FHIRClient, patient_id: str) -> list[dict]:
    """Fetch all lab results for a patient."""
    bundle = client.search('Observation', {
        'subject': f'Patient/{patient_id}',
        'category': 'laboratory',
        '_sort': '-date',
    })
    return bundle.get('entry', [])

def get_patient_medications(client: FHIRClient, patient_id: str) -> list[dict]:
    """Fetch active medications for a patient."""
    bundle = client.search('MedicationRequest', {
        'subject': f'Patient/{patient_id}',
        'status': 'active',
    })
    return bundle.get('entry', [])

def get_patient_conditions(client: FHIRClient, patient_id: str) -> list[dict]:
    """Fetch active conditions (diagnoses) for a patient."""
    bundle = client.search('Condition', {
        'subject': f'Patient/{patient_id}',
        'clinical-status': 'active',
    })
    return bundle.get('entry', [])
```

### 4. FHIR Bulk Data

```python
def kick_off_bulk_export(client: FHIRClient, output_format: str = 'application/fhir+ndjson'):
    """Initiate FHIR Bulk Data export."""
    resp = requests.get(
        f'{client.base_url}/$export',
        headers={
            **client.headers,
            'Accept': output_format,
            'Prefer': 'respond-async',
        }
    )
    return resp.headers.get('Content-Location')  # Poll this URL for status

def check_bulk_status(status_url: str) -> dict:
    """Check status of bulk data export."""
    resp = requests.get(status_url)
    if resp.status_code == 200:
        return resp.json()  # Contains download URLs
    return {'status': 'in-progress'}
```

### 5. Subscriptions

```python
def create_subscription(client: FHIRClient, criteria: str, endpoint: str) -> dict:
    """Create a FHIR subscription for real-time notifications."""
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

# Example: subscribe to new Observations for a patient
create_subscription(
    client,
    "Observation?subject=Patient/12345",
    "https://myapp.example.com/fhir-webhook"
)
```

## Best Practices

- **Use official FHIR schemas** for validation
- **Handle pagination** in search results (Bundle links)
- **Cache resources** when appropriate to reduce server load
- **Use _summary and _elements** to reduce payload size
- **Implement retry logic** for transient failures
- **Validate tokens** on every request in production

## Common Pitfalls

- Not handling Bundle pagination (missing results)
- Ignoring FHIR version differences (R4 vs R5)
- Not validating resource references before use
- Forgetting to handle timezone in date/time fields
- Not implementing proper OAuth2 token refresh

## Examples

### Patient Summary

```python
def build_patient_summary(client: FHIRClient, patient_id: str) -> dict:
    """Build a comprehensive patient summary."""
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

## Validation

```python
def test_fhir_client():
    client = FHIRClient('https://hapi.fhir.org/baseR4')
    patient = client.read('Patient', 'example')
    assert patient['resourceType'] == 'Patient'

def test_resource_validation():
    patient = {"resourceType": "Patient", "name": [{"family": "Test"}]}
    assert patient['resourceType'] == 'Patient'
```
