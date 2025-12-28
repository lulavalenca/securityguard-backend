# SecurityGuard API Documentation

## Overview

RESTful API for security monitoring, threat detection, and compliance management.

**Base URL**: `https://api.secureapps.com/api/v1`
**Version**: 1.0.0

## Authentication

All endpoints (except `/register`) require JWT authentication.

### Login

```bash
POST /token
Content-Type: application/x-www-form-urlencoded

username=admin&password=admin123
```

**Response** (200 OK):
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

### Using Token

Include in all requests:
```bash
Authorization: Bearer eyJhbGc...
```

## Endpoints

### Authentication

#### Register User
```
POST /register
```

**Request**:
```json
{
  "username": "newuser",
  "email": "user@example.com",
  "password": "SecurePass123!",
  "full_name": "New User"
}
```

**Response** (200 OK):
```json
{
  "id": 3,
  "username": "newuser",
  "email": "user@example.com",
  "full_name": "New User",
  "role": "viewer",
  "is_active": true,
  "created_at": "2024-12-28T20:30:00Z",
  "updated_at": "2024-12-28T20:30:00Z"
}
```

### Threats

#### List Threats
```
GET /threats?skip=0&limit=10&status_filter=active
```

**Query Parameters**:
- `skip`: Number of results to skip (default: 0)
- `limit`: Max results (default: 10, max: 100)
- `status_filter`: Filter by status (active, mitigated, false_positive)

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "threat_type": "malware",
    "severity": "critical",
    "source_ip": "203.0.113.45",
    "destination_ip": "192.168.1.10",
    "description": "Malware detection",
    "status": "active",
    "detection_timestamp": "2024-12-28T20:00:00Z",
    "created_at": "2024-12-28T20:00:00Z"
  }
]
```

#### Create Threat
```
POST /threats
```

**Request**:
```json
{
  "threat_type": "malware",
  "severity": "critical",
  "source_ip": "203.0.113.45",
  "destination_ip": "192.168.1.10",
  "description": "Malware detected in network traffic",
  "signature_id": "SIG-12345"
}
```

#### Update Threat
```
PATCH /threats/{threat_id}
```

**Request**:
```json
{
  "status": "mitigated",
  "severity": "high"
}
```

### Network Monitoring

#### Record Traffic
```
POST /network/traffic
```

**Request**:
```json
{
  "source_ip": "192.168.1.50",
  "destination_ip": "8.8.8.8",
  "source_port": 54321,
  "destination_port": 443,
  "protocol": "TCP",
  "packet_count": 450,
  "bytes_sent": 125000,
  "bytes_received": 89500,
  "status": "normal"
}
```

### Security Dashboard

#### Get Dashboard Metrics
```
GET /security/dashboard
```

**Response** (200 OK):
```json
{
  "system_health": 98.5,
  "threats_detected": 47,
  "critical_threats": 5,
  "access_attempts": 2341,
  "blocked_attempts": 156,
  "data_protected_tb": 2.4,
  "threats_last_24h": 12,
  "total_threats": 156
}
```

### Scanning

#### Scan Single Port
```
POST /scanning/port
```

**Request**:
```json
{
  "target": "192.168.1.1",
  "port": 80,
  "scan_type": "tcp"
}
```

**Response** (200 OK):
```json
{
  "target": "192.168.1.1",
  "port": 80,
  "status": "open",
  "service": "HTTP",
  "protocol": "TCP",
  "timestamp": "2024-12-28T20:30:00Z"
}
```

#### Scan Vulnerabilities
```
POST /scanning/vulnerabilities
```

**Request**:
```json
{
  "target": "192.168.1.1",
  "scan_depth": "deep"
}
```

### Cryptography

#### Generate Hash
```
POST /crypto/hash
```

**Request**:
```json
{
  "text": "password123",
  "algorithms": ["sha256", "sha512", "md5"]
}
```

**Response** (200 OK):
```json
{
  "sha256": "ef92b778bafe771e89245d171bafed6f56bc1f65c1000",
  "sha512": "d404559f602eab6fd602ac7680dacbfaadd13630335e951f097af3900e9de176",
  "md5": "5f4dcc3b5aa765d61d8327deb882cf99"
}
```

#### Encrypt (AES)
```
POST /crypto/aes/encrypt
```

**Request**:
```json
{
  "mode": "CBC",
  "key_hex": "0123456789abcdef0123456789abcdef",
  "plaintext": "Secret message"
}
```

### Reports

#### Generate Report
```
POST /reports/generate
```

**Request**:
```json
{
  "report_type": "executive",
  "period": "30",
  "include_charts": true,
  "include_recommendations": true
}
```

### Compliance

#### Get Compliance Score
```
GET /compliance/score
```

**Response** (200 OK):
```json
{
  "LGPD": {
    "score": 94.0,
    "status": "Very Good"
  },
  "NIST_CSF": {
    "functions": {
      "GOVERN": 85.0,
      "IDENTIFY": 90.0,
      "PROTECT": 88.0,
      "DETECT": 87.0,
      "RESPOND": 82.0,
      "RECOVER": 80.0
    },
    "average": 85.3
  },
  "ISO_27001": {
    "score": 91.0,
    "status": "Excellent"
  }
}
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid input data"
}
```

### 401 Unauthorized
```json
{
  "detail": "Token invalid or expired"
}
```

### 403 Forbidden
```json
{
  "detail": "User is deactivated"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

## Rate Limiting

- Default: 100 requests per minute
- Headers returned:
  - `X-RateLimit-Limit`: Total requests allowed
  - `X-RateLimit-Remaining`: Requests remaining
  - `X-RateLimit-Reset`: Time when limit resets

## Examples

### Login and Get Threats

```bash
#!/bin/bash

# Get token
TOKEN=$(curl -X POST http://localhost:8000/api/v1/token \
  -d "username=admin&password=admin123" | jq -r '.access_token')

# Get threats
curl -X GET http://localhost:8000/api/v1/threats \
  -H "Authorization: Bearer $TOKEN" | jq
```

### Create and Mitigate Threat

```bash
# Create threat
THREAT=$(curl -X POST http://localhost:8000/api/v1/threats \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "threat_type": "malware",
    "severity": "critical",
    "source_ip": "203.0.113.45",
    "destination_ip": "192.168.1.10",
    "description": "Detected malware"
  }' | jq -r '.id')

# Update threat to mitigated
curl -X PATCH http://localhost:8000/api/v1/threats/$THREAT \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status": "mitigated"}'
```

## WebSocket (Real-time)

For real-time threat updates (future implementation):

```javascript
const ws = new WebSocket('wss://api.secureapps.com/ws/threats');
ws.onmessage = (event) => {
  console.log('New threat:', event.data);
};
```

## Webhooks

Register webhooks to receive notifications:

```bash
curl -X POST http://localhost:8000/api/v1/webhooks \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "threat_detected",
    "url": "https://myserver.com/webhook"
  }'
```
