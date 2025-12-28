# System Architecture

## Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend (React)                      │
│                    http://localhost:3000                     │
└─────────────────────┬───────────────────────────────────────┘
                      │ HTTPS/REST
                      ↓
┌─────────────────────────────────────────────────────────────┐
│                    NGINX Reverse Proxy                       │
│                   Port: 80, 443 (HTTPS)                      │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ↓
┌─────────────────────────────────────────────────────────────┐
│                   FastAPI Application                        │
│                   Port: 8000 (Uvicorn)                       │
│  ┌───────────────────────────────────────────────────────┐  │
│  │           API Routers (v1)                            │  │
│  │  - auth.py          → Autenticação JWT               │  │
│  │  - security.py      → Dashboard & métricas           │  │
│  │  - threats.py       → CRUD de ameaças                │  │
│  │  - network.py       → Monitoramento de rede          │  │
│  │  - logs.py          → Agregação de logs              │  │
│  │  - scanning.py      → Port scanning & vulnerabilities│  │
│  │  - crypto.py        → Operações criptográficas      │  │
│  │  - pentest.py       → Pentest labs & payloads       │  │
│  │  - reports.py       → Geração de relatórios         │  │
│  │  - compliance.py    → Conformidade (LGPD/NIST/ISO)  │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                               │
│  ┌───────────────────────────────────────────────────────┐  │
│  │        Services Layer (Business Logic)                │  │
│  │  - auth_service.py          → JWT & Autenticação     │  │
│  │  - threat_detection.py      → Detecção de ameaças    │  │
│  │  - port_scanner.py          → Scan de portas         │  │
│  │  - ssl_validator.py         → Validação SSL/TLS      │  │
│  │  - vulnerability_scanner.py → Análise de vulns       │  │
│  │  - crypto_service.py        → Criptografia (AES/RSA) │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                               │
│  ┌───────────────────────────────────────────────────────┐  │
│  │        Security Layer                                 │  │
│  │  - jwt_handler.py      → Gestão de tokens            │  │
│  │  - password_hasher.py  → Hash bcrypt                 │  │
│  │  - encryption.py       → Fernet encryption           │  │
│  │  - rate_limiter.py     → Rate limiting               │  │
│  │  - validators.py       → Validação de entrada        │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                               │
│  ┌───────────────────────────────────────────────────────┐  │
│  │       Utilities & Integrations                        │  │
│  │  - logger.py           → JSON logging                 │  │
│  │  - email_sender.py     → Notificações via email      │  │
│  │  - slack.py            → Integração Slack            │  │
│  │  - webhook_handler.py  → Gestão de webhooks          │  │
│  └───────────────────────────────────────────────────────┘  │
└──────┬───────────────────────┬──────────────┬────────────────┘
       │                       │              │
       ↓                       ↓              ↓
┌──────────────┐     ┌──────────────┐  ┌──────────────┐
│ PostgreSQL   │     │    Redis     │  │Elasticsearch │
│   Database   │     │    Cache     │  │  Log Storage │
│              │     │              │  │              │
│ - users      │     │ - Sessions   │  │ - Event logs │
│ - threats    │     │ - Rate limit │  │ - Alerts     │
│ - logs       │     │ - Webhooks   │  │ - Metrics    │
│ - vulns      │     │              │  │              │
│ - reports    │     │              │  │              │
└──────────────┘     └──────────────┘  └──────────────┘
       ↓                                       ↓
    Backup                                  Kibana
    (pg_dump)                        Visualization
                                    (localhost:5601)

     ┌──────────────────────────────────────┐
     │      Monitoring & Observability       │
     │  ┌──────────────────────────────────┐ │
     │  │  Prometheus (localhost:8001)     │ │
     │  │  - Request metrics               │ │
     │  │  - Response times                │ │
     │  │  - Error rates                   │ │
     │  └──────────────────────────────────┘ │
     │  ┌──────────────────────────────────┐ │
     │  │  Grafana (optional)              │ │
     │  │  - Custom dashboards             │ │
     │  │  - Alerts                        │ │
     │  └──────────────────────────────────┘ │
     └──────────────────────────────────────┘
```

## Data Flow

### Authentication Flow

```
Client
   │
   ├─→ POST /api/v1/token
   │   (username, password)
   │
   ↓
FastAPI
   │
   ├─→ auth_service.authenticate_user()
   │
   ├─→ verify_password()
   │
   ├─→ jwt_handler.create_access_token()
   │
   ↓
Client receives token
   │
   └─→ Store in localStorage
       Use in Authorization header
```

### Threat Detection Flow

```
Network Traffic
   │
   ├─→ IDS/IPS System
   │
   ├─→ POST /api/v1/threats
   │   (threat data)
   │
   ↓
FastAPI
   │
   ├─→ threat_detection.analyze()
   │
   ├─→ threat_detection.create_threat_record()
   │
   ├─→ Save to PostgreSQL
   │
   ├─→ Cache in Redis
   │
   ├─→ Send to Elasticsearch
   │
   ├─→ Trigger webhooks
   │
   ├─→ Send Slack notification
   │
   ↓
Dashboard Updated (real-time)
```

### Report Generation Flow

```
User Request
   │
   ├─→ POST /api/v1/reports/generate
   │   (type, period, options)
   │
   ↓
FastAPI
   │
   ├─→ Query threats from PostgreSQL
   │
   ├─→ Query vulnerabilities
   │
   ├─→ Calculate metrics
   │
   ├─→ Generate charts
   │
   ├─→ Create HTML/PDF
   │
   ├─→ Save to database
   │
   ↓
Return download link
   │
   └─→ User downloads PDF
```

## Database Schema (Simplified)

```
users (1) ─→ (N) logs
       │
       └─→ (N) audit_log
       └─→ (N) security_policies
       └─→ (N) reports

threats (1) ─→ (N) logs
       │
       └─→ (N) audit_log

network_traffic (1) ─→ (N) logs

vulnerabilities (1) ─→ (N) logs

ssl_certificates (standalone)

security_policies (1) ─→ (N) audit_log
```

## API Response Flow

```
Client Request
   ↓
[CORS Middleware]
   ↓
[Rate Limiter]
   ↓
[JWT Authentication]
   ↓
[Authorization Check]
   ↓
[Input Validation (Pydantic)]
   ↓
[Route Handler]
   ↓
[Service Logic]
   ↓
[Database Query]
   ↓
[Cache Check/Update]
   ↓
[Logging]
   ↓
[Response Serialization]
   ↓
[Status Code]
   ↓
Client receives JSON
```

## Scalability Architecture

```
                    Load Balancer (Nginx/HAProxy)
                              │
              ┌───────────────┼───────────────┐
              ↓               ↓               ↓
         API Server 1    API Server 2    API Server 3
         (8001)          (8002)          (8003)
              │               │               │
              └───────────────┼───────────────┘
                              │
            ┌─────────────────┼─────────────────┐
            ↓                 ↓                 ↓
      PostgreSQL         Redis Cluster    Elasticsearch
      (with replication) (with failover)  (with shards)

For Heavy Load:
- Add more API servers
- Use database replication
- Implement Redis clustering
- Scale Elasticsearch with shards
```

## Security Layers

```
┌──────────────────────────────────────┐
│         HTTPS/TLS Encryption         │
├──────────────────────────────────────┤
│         CORS Policy Validation       │
├──────────────────────────────────────┤
│         Rate Limiting                │
├──────────────────────────────────────┤
│         JWT Authentication           │
├──────────────────────────────────────┤
│         Role-Based Authorization     │
├──────────────────────────────────────┤
│         Input Validation (Pydantic)  │
├──────────────────────────────────────┤
│         SQL Injection Prevention      │
│         (SQLAlchemy ORM)             │
├──────────────────────────────────────┤
│         Password Hashing (bcrypt)    │
├──────────────────────────────────────┤
│         Data Encryption (Fernet)     │
├──────────────────────────────────────┤
│         Audit Logging                │
├──────────────────────────────────────┤
│         Database Row-Level Security  │
└──────────────────────────────────────┘
```

## Performance Optimization

```
┌─ Frontend Caching ─────────────────┐
│ Browser cache (30 min)             │
└────────────────────────────────────┘
              │
              ↓
┌─ Application Cache ────────────────┐
│ Redis (10-60 min TTL)              │
│ - User sessions                    │
│ - Dashboard metrics                │
│ - API responses                    │
└────────────────────────────────────┘
              │
              ↓
┌─ Database Optimization ────────────┐
│ - Indexed columns                  │
│ - Connection pooling               │
│ - Query optimization               │
│ - Materialized views               │
└────────────────────────────────────┘
              │
              ↓
┌─ Compression ──────────────────────┐
│ - GZIP (API responses)             │
│ - BROTLI (static files)            │
│ - Minified frontend                │
└────────────────────────────────────┘
```

## Deployment Environments

### Development
- Single container or local machine
- SQLite or local PostgreSQL
- Hot reload enabled
- Debug logging

### Staging
- Docker containers
- PostgreSQL with backups
- Redis for caching
- SSL/TLS enabled
- Email/Slack configured

### Production
- Kubernetes cluster or Docker Swarm
- PostgreSQL with replication
- Redis cluster
- Elasticsearch cluster
- CDN for static files
- Monitoring & alerts
- Automated backups
- Load balancing
