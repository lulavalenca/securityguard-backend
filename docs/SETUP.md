# Setup Guide

## Installation Steps

### 1. Prerequisites

- Python 3.11+
- PostgreSQL 14+
- Redis 7+
- Docker & Docker Compose (optional)

### 2. Local Development Setup

#### Clone Repository
```bash
git clone https://github.com/lulavalenca/securityguard-backend.git
cd securityguard-backend
```

#### Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

#### Install Dependencies
```bash
pip install -r requirements.txt
```

#### Configure Environment
```bash
cp .env.example .env
# Edit .env with your credentials
```

#### Create Database
```bash
# Using PostgreSQL
psql -U postgres -c "CREATE DATABASE secureapps;"
psql -U postgres -c "ALTER DATABASE secureapps OWNER TO user;"

# Run migrations
alembic upgrade head

# Or create tables directly
python -c "from app.database import Base, engine; import app.models; Base.metadata.create_all(bind=engine)"
```

#### Initialize Database
```bash
python scripts/init_db.py
```

#### Run Application
```bash
uvicorn app.main:app --reload --port 8000
```

Access at: http://localhost:8000
- Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 3. Docker Setup

#### Build and Run
```bash
docker-compose -f docker/docker-compose.yml up -d
```

#### Check Status
```bash
docker-compose -f docker/docker-compose.yml ps
```

#### View Logs
```bash
docker-compose -f docker/docker-compose.yml logs -f api
```

#### Stop Services
```bash
docker-compose -f docker/docker-compose.yml down
```

### 4. Database Migrations

#### Create Migration
```bash
alembic revision --autogenerate -m "Add new column"
```

#### Apply Migrations
```bash
alembic upgrade head
```

#### Rollback Migration
```bash
alembic downgrade -1
```

## Configuration

### Environment Variables

See `.env.example` for all options:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/secureapps
SQLALCHEMY_ECHO=false

# JWT
SECRET_KEY=your-super-secret-key-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application
DEBUG=false
ENVIRONMENT=production
ALLOWED_ORIGINS=["http://localhost:3000","https://yourdomain.com"]

# Services
REDIS_URL=redis://localhost:6379
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SLACK_WEBHOOK_URL=https://hooks.slack.com/...
```

### Docker Compose Environment

Create `.env` for docker-compose:

```env
POSTGRES_USER=user
POSTGRES_PASSWORD=secure_password
POSTGRES_DB=secureapps
SECRET_KEY=your-secret-key
DEBUG=False
ENVIRONMENT=production
```

## Running Tests

```bash
# All tests
pytest app/tests -v

# With coverage
pytest app/tests -v --cov=app --cov-report=html

# Specific test file
pytest app/tests/test_auth.py -v

# Specific test
pytest app/tests/test_auth.py::TestAuthentication::test_login_success -v
```

## Code Quality

```bash
# Format code
black app/

# Lint
flake8 app/ --max-line-length=100

# Sort imports
isort app/

# Type checking
mypy app/ --ignore-missing-imports

# Run all checks
bash scripts/lint.sh
```

## Monitoring

### Logs

Logs are saved to `logs/app.log` and output to console.

For Docker:
```bash
docker-compose logs -f api
```

### Metrics (Prometheus)

Access metrics at: http://localhost:8001/metrics

### Elasticsearch (optional)

Access at: http://localhost:9200

### Kibana (optional)

Access at: http://localhost:5601

## Troubleshooting

### Database Connection Failed

```bash
# Check PostgreSQL is running
psql -U postgres -c "SELECT 1"

# Verify DATABASE_URL in .env
# Format: postgresql://user:password@host:port/database
```

### Port Already in Use

```bash
# Change port
uvicorn app.main:app --port 8001

# Or kill process
kill -9 $(lsof -t -i:8000)
```

### Module Not Found

```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Docker Issues

```bash
# Remove all containers and volumes
docker-compose -f docker/docker-compose.yml down -v

# Rebuild images
docker-compose -f docker/docker-compose.yml build --no-cache

# Start fresh
docker-compose -f docker/docker-compose.yml up -d
```

## Performance Tuning

### Database

- Add indexes on frequently filtered columns
- Use connection pooling (SQLAlchemy already enabled)
- Monitor query performance with EXPLAIN

### Redis

- Use for session caching
- Cache API responses (10-60 min TTL)
- Rate limiting storage

### Application

- Enable uvicorn workers: `--workers 4`
- Use connection pool: `pool_size=20`
- Enable gzip compression in nginx

## Security Hardening

1. Change default credentials
2. Use strong SECRET_KEY (min 32 chars)
3. Enable HTTPS/SSL
4. Set secure CORS origins
5. Use environment variables for secrets
6. Enable rate limiting
7. Regular security updates: `pip install --upgrade -r requirements.txt`
