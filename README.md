# SecureGuard Backend - Sistema de Detecção de Ameaças

Backend FastAPI completo para monitoramento de segurança, detecção de ameaças e conformidade regulatória (LGPD, NIST, ISO 27001).

## 🚀 Recursos

- **Autenticação JWT** - Segurança baseada em tokens
- **Detecção de Ameaças** - Em tempo real (IDS/IPS)
- **Monitoramento de Rede** - Análise de tráfego e padrões
- **Scanning de Portas** - Integração com NMAP
- **Análise de Vulnerabilidades** - Detecção e rastreamento
- **Validação SSL/TLS** - Verificação de certificados
- **Geração de Relatórios** - PDF, HTML, compliance
- **Conformidade** - LGPD, NIST CSF, ISO 27001
- **Criptografia** - AES, RSA, Hash (SHA256/512, MD5, BLAKE2)
- **Testes de Penetração** - Laboratório de pentest simulado
- **Dashboard** - Métricas em tempo real

## 📋 Pré-requisitos

- Python 3.11+
- PostgreSQL 14+
- Redis 7+
- Docker & Docker Compose (opcional)

## ⚙️ Instalação

### Local

```bash
# Clone o repositório
git clone https://github.com/lulavalenca/securityguard-backend.git
cd securityguard-backend

# Crie ambiente virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instale dependências
pip install -r requirements.txt

# Configure variáveis de ambiente
cp .env.example .env
# Edite .env com suas credenciais

# Crie banco de dados
psql -U postgres -c "CREATE DATABASE secureapps;"

# Crie as tabelas
python -c "from app.database import Base, engine; import app.models; Base.metadata.create_all(bind=engine)"

# Inicie a aplicação
uvicorn app.main:app --reload --port 8000
```

### Docker

```bash
# Build e inicie containers
docker-compose -f docker/docker-compose.yml up -d

# Logs
docker-compose logs -f api

# Parar
docker-compose down
```

## 📚 API Documentation

Acesse a documentação interativa:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔑 Endpoints Principais

### Autenticação
```
POST   /api/v1/register           - Criar usuário
POST   /api/v1/token              - Login (obter token)
GET    /api/v1/me                 - Dados do usuário atual
```

### Ameaças
```
GET    /api/v1/threats            - Listar ameaças
POST   /api/v1/threats            - Criar ameaça
GET    /api/v1/threats/{id}       - Detalhes da ameaça
PATCH  /api/v1/threats/{id}       - Atualizar ameaça
```

### Segurança
```
GET    /api/v1/security/dashboard         - Dashboard
GET    /api/v1/security/threats/by-type   - Ameaças por tipo
GET    /api/v1/security/network-activity  - Atividade de rede
```

### Rede
```
POST   /api/v1/network/traffic    - Registrar tráfego
GET    /api/v1/network/traffic    - Listar tráfego
```

### Scanning
```
POST   /api/v1/scanning/port      - Escanear porta
POST   /api/v1/scanning/port-range- Escanear intervalo
POST   /api/v1/scanning/vulnerabilities - Escanear vulnerabilidades
```

### Criptografia
```
POST   /api/v1/crypto/aes/encrypt - Encriptar AES
POST   /api/v1/crypto/aes/decrypt - Descriptografar AES
POST   /api/v1/crypto/hash        - Gerar hash
```

### Pentest
```
GET    /api/v1/pentest/environments           - Listar ambientes
POST   /api/v1/pentest/payload/decode         - Decodificar payload
POST   /api/v1/pentest/shellcode/analyze      - Analisar shellcode
POST   /api/v1/pentest/password/test          - Testar força de senha
POST   /api/v1/pentest/wordlist/generate      - Gerar wordlist
```

### Relatórios
```
POST   /api/v1/reports/generate   - Gerar relatório
GET    /api/v1/reports/list       - Listar relatórios
GET    /api/v1/reports/trends     - Tendências de segurança
```

### Conformidade
```
GET    /api/v1/compliance/score                  - Scores de compliance
GET    /api/v1/compliance/lgpd/requirements      - Requisitos LGPD
GET    /api/v1/compliance/nist/functions        - Funções NIST
```

## 🗄️ Estrutura do Banco de Dados

```
users                - Usuários e autenticação
threats              - Ameaças detectadas
logs                 - Eventos de sistema
network_traffic      - Tráfego monitorado
vulnerabilities      - Vulnerabilidades
ssl_certificates     - Certificados SSL/TLS
security_policies    - Políticas de segurança
reports              - Relatórios gerados
audit_log            - Trilha de auditoria
```

## 🔐 Segurança

- **JWT**: Tokens com expiração configurável
- **Password Hashing**: bcrypt com salt
- **Rate Limiting**: Limite de requisições
- **CORS**: Configuração por origem
- **Input Validation**: Pydantic schemas
- **Encryption**: Fernet para dados sensíveis

## 📊 Monitoramento

- **Prometheus**: Métricas expostas em `/metrics`
- **Elasticsearch**: Log centralization (opcional)
- **Kibana**: Visualização de logs (opcional)

## 🧪 Testes

```bash
# Rodar testes
pytest app/tests -v --cov=app

# Teste específico
pytest app/tests/test_auth.py::test_register_user -v
```

## 📝 Variáveis de Ambiente

Veja `.env.example` para todas as opções:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/secureapps
SECRET_KEY=sua-chave-super-secreta
REDIS_URL=redis://localhost:6379
SMTP_HOST=smtp.gmail.com
SMTP_USER=seu-email@gmail.com
SMTP_PASSWORD=sua-senha-app
```

## 🤝 Contribuindo

1. Fork o repositório
2. Crie uma branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

MIT - veja LICENSE para detalhes

## 👨‍💼 Suporte

Para suporte, abra uma issue no GitHub ou entre em contato através de security@secureapps.com
