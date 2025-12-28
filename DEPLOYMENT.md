# Deployment Guide

## Production Deployment

### AWS EC2 Deployment

```bash
# SSH into instance
ssh -i key.pem ubuntu@your-instance-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3.11 python3.11-venv postgresql redis-server nginx

# Clone repository
git clone https://github.com/yourusername/securityguard-backend.git
cd securityguard-backend

# Setup Python environment
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with production values

# Initialize database
python scripts/init_db.py

# Start Gunicorn
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Docker Swarm Deployment

```bash
# Initialize swarm
docker swarm init

# Create stack
docker stack deploy -c docker/docker-compose.yml secureapps

# Check services
docker service ls
docker service logs secureapps_api
```

### Kubernetes Deployment

Create `k8s-deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: secureapps-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: secureapps-api
  template:
    metadata:
      labels:
        app: secureapps-api
    spec:
      containers:
      - name: api
        image: your-registry/secureapps-api:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
        - name: SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: app-secret
              key: key
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

```bash
# Deploy to Kubernetes
kubectl apply -f k8s-deployment.yaml

# Check deployment
kubectl get pods
kubectl logs -f deployment/secureapps-api
```

## Reverse Proxy (Nginx)

```nginx
upstream api {
    server localhost:8000;
}

server {
    listen 80;
    server_name api.secureapps.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name api.secureapps.com;

    ssl_certificate /etc/letsencrypt/live/api.secureapps.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.secureapps.com/privkey.pem;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    client_max_body_size 10M;

    location / {
        proxy_pass http://api;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Compression
        gzip on;
        gzip_types application/json text/css application/javascript;
    }

    # Cache static responses
    location ~* \.(json)$ {
        proxy_pass http://api;
        proxy_cache_valid 200 10m;
        expires 10m;
    }
}
```

## CI/CD Pipeline (GitHub Actions)

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy

on:
  push:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    - name: Run tests
      run: |
        pytest app/tests -v --cov=app
    - name: Build Docker image
      run: |
        docker build -f docker/Dockerfile -t secureapps-api:${{ github.sha }} .
    - name: Push to registry
      run: |
        docker tag secureapps-api:${{ github.sha }} your-registry/secureapps-api:latest
        docker push your-registry/secureapps-api:latest
    - name: Deploy
      run: |
        # Your deployment command
```

## Backup & Recovery

### Database Backup

```bash
# Full backup
pg_dump secureapps > backup.sql

# Compressed backup
pg_dump secureapps | gzip > backup.sql.gz

# Restore
psql secureapps < backup.sql
```

### Automated Backups

```bash
# Create backup script
cat > /usr/local/bin/backup-db.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/backups/database"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR
pg_dump secureapps | gzip > $BACKUP_DIR/backup_$DATE.sql.gz
# Keep only last 30 days
find $BACKUP_DIR -name "backup_*.sql.gz" -mtime +30 -delete
EOF

# Make executable
sudo chmod +x /usr/local/bin/backup-db.sh

# Add to crontab
sudo crontab -e
# Add: 0 2 * * * /usr/local/bin/backup-db.sh
```

## Monitoring & Logging

### Application Metrics

Setup Prometheus scraping:

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'secureapps-api'
    static_configs:
      - targets: ['localhost:8001']
```

### Log Aggregation

With Elasticsearch and Kibana:

```bash
docker-compose up elasticsearch kibana
```

Access Kibana at: http://localhost:5601

## Health Checks

```bash
# Check application health
curl http://localhost:8000/health

# Automated health monitoring
watch -n 5 'curl -s http://localhost:8000/health | jq'
```

## Scaling

### Horizontal Scaling

```bash
# Run multiple API instances
for i in {1..4}; do
  PORT=$((8000 + i)) gunicorn app.main:app --workers 4 --bind 0.0.0.0:$PORT &
done
```

### Load Balancing with HAProxy

```
global
    maxconn 4096

frontend api_frontend
    bind *:80
    default_backend api_backend

backend api_backend
    balance roundrobin
    server api1 localhost:8001 check
    server api2 localhost:8002 check
    server api3 localhost:8003 check
    server api4 localhost:8004 check
```
