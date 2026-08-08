# Swarn RAG Chatbot

A production-ready **Retrieval-Augmented Generation (RAG) chatbot** system featuring multi-agent orchestration, advanced observability, and enterprise-grade deployment patterns.

## 🚀 Quick Start

```bash
# 1. Clone & setup
cp .env.example .env

# 2. Start all services
cd infra
docker-compose up -d

# 3. Access
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- Grafana: http://localhost:3000 (admin/admin)
- LangFuse: http://localhost:3001
```

## 📋 Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | React 18 + Vite + Axios | SPA user interface |
| **Backend** | FastAPI + Uvicorn | REST API & RAG orchestration |
| **LLM** | Ollama + LangChain + LangGraph | Local inference & agent graph |
| **Vector DB** | Qdrant | Semantic search & embeddings |
| **Relational DB** | PostgreSQL | Users, documents, conversations |
| **Message Bus** | Kafka (optional) | Async task processing |
| **Observability** | Prometheus + Grafana + Loki | Metrics, logs, dashboards |
| **LLM Tracing** | LangFuse | Prompt versioning, evaluation |
| **Reverse Proxy** | Nginx | Request routing, static files |
| **Deployment** | Docker Compose + Kubernetes | Local & production |

## 📁 Project Structure

```
├── frontend/              # React SPA (Vite)
├── backend/               # FastAPI application
│   ├── app/
│   │   ├── api/          # Route handlers
│   │   ├── services/     # Business logic (RAG, users)
│   │   ├── agents/       # LangGraph workflows
│   │   └── utils/        # Telemetry, exceptions
│   └── tests/
├── data/                  # Raw & processed data (not in git)
├── infra/
│   ├── docker-compose.yaml
│   ├── docker-compose.kafka.yml  # Optional
│   ├── scripts/           # DB init, health checks
│   ├── nginx/
│   ├── prometheus/
│   ├── grafana/
│   ├── loki/
│   └── k8s/              # Kubernetes manifests
├── config/               # Application configuration
├── docs/                 # Architecture documentation
└── .env.example
```

## 🎯 Key Features

✅ **Production-Ready RAG**
- Document ingestion pipeline (PDF, DOCX, TXT)
- Semantic search via Qdrant
- LLM-powered generation with Ollama
- Multi-agent orchestration with LangGraph

✅ **Enterprise Observability**
- Prometheus metrics + Grafana dashboards
- Centralized logging (Loki)
- LLM observability (LangFuse)
- OpenTelemetry instrumentation

✅ **Scalable Architecture**
- Horizontal scaling (backend replicas)
- Event-driven design (Kafka-ready, commented)
- Load balancing (Nginx)
- Container-native (Docker + K8s)

✅ **Security & Auth**
- JWT authentication
- FastAPI-Users integration
- CORS configured
- Database encryption ready

## 🐳 Docker Compose (Local Development)

### Start Stack
```bash
cd infra
docker-compose up -d
```

### Services
- **PostgreSQL**: User & document metadata
- **Qdrant**: Vector embeddings
- **Ollama**: Local LLM (pull model first!)
- **FastAPI**: Backend API
- **React**: Frontend (Vite dev server)
- **Nginx**: Reverse proxy
- **Prometheus/Grafana**: Metrics & dashboards
- **Loki**: Log aggregation
- **LangFuse**: LLM tracing

### Pull LLM Model
```bash
docker-compose exec ollama ollama pull mistral
# or any model from https://ollama.ai/library
```

### Database Setup
```bash
docker-compose exec postgres psql -U postgres -d swarn_db -f /docker-entrypoint-initdb.d/init.sql
```

## ☸️ Kubernetes Deployment

### Prerequisites
- K8s cluster (1.28+)
- Container registry (Docker Hub, ECR, etc.)

### Deploy
```bash
cd infra/k8s
kubectl apply -k .
```

### Verify
```bash
kubectl get pods -n swarn-ai
kubectl get svc -n swarn-ai
```

### Port Forward
```bash
kubectl port-forward -n swarn-ai svc/backend 8000:8000
kubectl port-forward -n swarn-ai svc/grafana 3000:3000
```

## 🧪 Development

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Testing
```bash
# Unit tests
pytest backend/tests/ -v

# With coverage
pytest backend/tests/ --cov=backend/app
```

## 📊 Observability

### Grafana
- **URL**: http://localhost:3000
- **Credentials**: admin/admin
- **Datasources**: Prometheus, Loki (pre-configured)

### LangFuse
- **URL**: http://localhost:3001
- **Features**: Prompt versioning, latency tracking, evaluation

### Prometheus
- **URL**: http://localhost:9090
- **Metrics**: Request count, latency, backend health

### Loki
- **Access via**: Grafana → Explore → Loki
- **Labels**: service, level, timestamp

## 🔄 Optional: Kafka for Async Processing

Enable message-driven async tasks:

```bash
# Local
docker-compose -f docker-compose.yaml -f docker-compose.kafka.yml up

# K8s: Uncomment in infra/k8s/kustomization.yaml
```

**Topics**:
- `document-ingestion`: Process uploaded documents
- `rag-evaluation`: Ragas evaluation results

## 📝 Configuration

Copy `.env.example` → `.env` and customize:

```env
# Database
DATABASE_URL=postgresql://postgres:password@postgres:5432/swarn_db

# JWT
JWT_SECRET=your-secret-key-here

# LLM
OLLAMA_MODEL=mistral

# Observability
LANGFUSE_PUBLIC_KEY=your-key
LANGFUSE_SECRET_KEY=your-secret

# Frontend
VITE_API_BASE_URL=http://localhost:8000
```

## 🚦 API Endpoints

### Health
```
GET /health
```

### Authentication (TODO)
```
POST /api/users/register
POST /api/users/login
GET /api/users/me
```

### Chat (TODO)
```
POST /api/chat/message          # Send message & get RAG response
GET /api/chat/conversation/{id} # Conversation history
```

### Documents (TODO)
```
POST /api/documents/upload      # Upload & ingest document
GET /api/documents/list         # List documents
DELETE /api/documents/{id}      # Delete document
```

## 📖 Documentation

- [Architecture Deep Dive](./docs/architecture.md) - System design, data flow, scalability patterns
- [API Documentation](http://localhost:8000/docs) - Interactive Swagger UI

## 🐛 Troubleshooting

```bash
# Check service logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Database connection test
docker-compose exec postgres psql -U postgres -d swarn_db -c "SELECT 1"

# Verify Qdrant
curl http://localhost:6333/health

# Verify Ollama
curl http://localhost:11434/api/tags
```

## 🤝 Contributing

1. Create feature branch: `git checkout -b feature/your-feature`
2. Make changes & test
3. Submit PR

## 📄 License

TBD

## 👤 Author

**Nicolas-FTM** - nicolasfelipetm@gmail.com

---

**Note**: This is a technical assessment project showcasing production-grade RAG implementation with enterprise observability patterns.
