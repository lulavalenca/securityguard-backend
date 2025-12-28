# 🔧 Guia de Instalação Completo

## 🚀 Começar em 5 Minutos

### Opção 1: Docker (Recomendado)

```bash
# 1. Clone
git clone https://github.com/lulavalenca/securityguard-backend.git
cd securityguard-backend

# 2. Execute
docker-compose -f docker/docker-compose.yml up -d

# 3. Aguarde 10 segundos
sleep 10

# 4. Inicialize DB
docker exec secureapps-api python scripts/init_db.py

# 5. Acesse
echo "API: http://localhost:8000/docs"
echo "Elasticsearch: http://localhost:9200"
echo "Kibana: http://localhost:5601"
```

### Opção 2: Local Python

```bash
# 1. Clone
git clone https://github.com/lulavalenca/securityguard-backend.git
cd securityguard-backend

# 2. Virtual Environment
python3.11 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Instale
pip install -r requirements.txt

# 4. Configure
cp .env.example .env
# Edite .env com suas credenciais PostgreSQL

# 5. Banco de Dados (tenha PostgreSQL rodando)
python scripts/init_db.py

# 6. Execute
uvicorn app.main:app --reload
```

---

## 👀 Verificar Instalação

```bash
# Teste a API
curl http://localhost:8000/health

# Resposta esperada:
# {"status":"ok","app":"SecureGuard...","version":"1.0.0"}
```

---

## 🔐 Login Padrão

| Usuário | Senha | Permissão |
|---------|-------|----------|
| admin | admin123 | Acesso Total |
| analyst | analyst123 | Analista |
| viewer | viewer123 | Apenas Visualização |

---

## 🗘 Troubleshooting

### Docker não funciona?

```bash
# Limpar tudo
docker-compose -f docker/docker-compose.yml down -v

# Reconstruir
docker-compose -f docker/docker-compose.yml build --no-cache

# Tentar novamente
docker-compose -f docker/docker-compose.yml up -d
```

### PostgreSQL connection error?

```bash
# Verificar conexão
psql -U user -h localhost -d secureapps -c "SELECT 1"

# Verificar .env
cat .env | grep DATABASE_URL
```

### Porta em uso?

```bash
# Mudar porta em .env ou command
uvicorn app.main:app --port 8001
```

---

Próximo passo: Leia [QUICKSTART.md](QUICKSTART.md)
