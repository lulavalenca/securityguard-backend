# 🚀 Quick Start Guide

## 5-Minute Setup

### Option 1: Local Development (Fastest)

```bash
# Clone
git clone https://github.com/lulavalenca/securityguard-backend.git
cd securityguard-backend

# Setup
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env: change DATABASE_URL to your PostgreSQL

# Initialize
python scripts/init_db.py

# Run
uvicorn app.main:app --reload
```

**Access**: http://localhost:8000/docs

**Default Users**:
- Admin: `admin` / `admin123`
- Analyst: `analyst` / `analyst123`
- Viewer: `viewer` / `viewer123`

---

### Option 2: Docker (Recommended for Production)

```bash
# Clone
git clone https://github.com/lulavalenca/securityguard-backend.git
cd securityguard-backend

# Run
docker-compose -f docker/docker-compose.yml up -d

# Initialize (after containers are ready)
sleep 10
docker exec secureapps-api python scripts/init_db.py
```

**Access**:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- Elasticsearch: http://localhost:9200
- Kibana: http://localhost:5601
- Redis: localhost:6379
- PostgreSQL: localhost:5432

---

## 📝 First Steps

### 1. Get Authentication Token

```bash
curl -X POST http://localhost:8000/api/v1/token \
  -d "username=admin&password=admin123"

# Response:
# {
#   "access_token": "eyJhbGc...",
#   "token_type": "bearer",
#   "expires_in": 86400
# }
```

### 2. Save Token

```bash
export TOKEN="your-access-token-here"
```

### 3. Create Your First Threat

```bash
curl -X POST http://localhost:8000/api/v1/threats \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "threat_type": "malware",
    "severity": "critical",
    "source_ip": "203.0.113.45",
    "destination_ip": "192.168.1.10",
    "description": "Malware detected in network"
  }'
```

### 4. List Threats

```bash
curl -X GET http://localhost:8000/api/v1/threats \
  -H "Authorization: Bearer $TOKEN" | jq
```

### 5. Get Dashboard

```bash
curl -X GET http://localhost:8000/api/v1/security/dashboard \
  -H "Authorization: Bearer $TOKEN" | jq
```

---

## 🧪 Test Everything

```bash
# Run tests
pytest app/tests -v

# With coverage
pytest app/tests -v --cov=app

# Specific test
pytest app/tests/test_auth.py::TestAuthentication::test_login_success -v
```

---

## 📊 Common Operations

### Create User

```bash
curl -X POST http://localhost:8000/api/v1/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "email": "user@example.com",
    "password": "SecurePass123!",
    "full_name": "New User"
  }'
```

### Scan Port

```bash
curl -X POST http://localhost:8000/api/v1/scanning/port \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "target": "192.168.1.1",
    "port": 80,
    "scan_type": "tcp"
  }'
```

### Generate Hash

```bash
curl -X POST http://localhost:8000/api/v1/crypto/hash \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "password123",
    "algorithms": ["sha256", "sha512"]
  }'
```

### Get Compliance Score

```bash
curl -X GET http://localhost:8000/api/v1/compliance/score \
  -H "Authorization: Bearer $TOKEN" | jq
```

### Generate Report

```bash
curl -X POST http://localhost:8000/api/v1/reports/generate \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "report_type": "executive",
    "period": "30"
  }'
```

---

## 🔗 Interactive API Documentation

Once running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

You can test all endpoints directly from the browser!

---

## 🐛 Troubleshooting

### Can't connect to database?

```bash
# Check PostgreSQL is running
psql -U postgres -c "SELECT 1"

# Verify connection string in .env
# Should be: postgresql://user:password@localhost:5432/secureapps
```

### Port already in use?

```bash
# Use different port
uvicorn app.main:app --reload --port 8001
```

### Module not found?

```bash
# Activate venv and reinstall
source venv/bin/activate
pip install -r requirements.txt --force-reinstall
```

### Docker issues?

```bash
# Clean everything and start fresh
docker-compose -f docker/docker-compose.yml down -v
docker-compose -f docker/docker-compose.yml build --no-cache
docker-compose -f docker/docker-compose.yml up -d
```

---

## 📚 Next Steps

1. **Read Documentation**
   - API Guide: [docs/API.md](docs/API.md)
   - Setup Guide: [docs/SETUP.md](docs/SETUP.md)
   - Deployment: [DEPLOYMENT.md](DEPLOYMENT.md)

2. **Integrate with Frontend**
   - Frontend: https://github.com/lulavalenca/securityguard-frontend

3. **Configure Integrations**
   - Slack notifications
   - Email alerts
   - Elasticsearch logging

4. **Set Up Monitoring**
   - Prometheus metrics
   - Grafana dashboards
   - Health checks

5. **Deploy to Production**
   - AWS/GCP/Azure
   - Kubernetes
   - Docker Swarm

---

## 💡 Pro Tips

✅ Use `jq` for pretty JSON output
```bash
curl ... | jq
```

✅ Save token in script
```bash
TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/token \
  -d "username=admin&password=admin123" | jq -r '.access_token')
echo "Token: $TOKEN"
```

✅ Monitor logs in real-time
```bash
docker-compose logs -f api  # Docker
tail -f logs/app.log        # Local
```

✅ Reload hot changes
```bash
# In a separate terminal while running with --reload
# Just save your files, app reloads automatically
```

---

## 🆘 Need Help?

- 📖 Check [README.md](README.md)
- 📚 Read API docs at http://localhost:8000/docs
- 🐛 Open an issue on GitHub
- 💬 Check discussions

---

**Happy coding! 🎉**
