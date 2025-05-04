# 🛠️ AI Agent T-Shirt Fulfillment System – Project README

Welcome to the official documentation for the AI Agent-powered on-demand T-shirt fulfillment platform. This system leverages LLM planning, modular backend services, and cloud storage to automate order processing end-to-end.

---

## 📂 Project Structure Overview

### Core Services

| Group | Purpose | Related Files |
|------|---------|---------------|
| **Frontend** | Web Interface for customers and operators | `frontend_service_spec.md` |
| **Agent Layer** | LLM-driven planner & orchestrator | `ai_agent_layer_spec.md`, `prompt_template.md`, `tool_registry.md` |
| **Backend Services** | Execute real-world tasks (design generation, excel, drive upload) | `ai_agent_backend_spec.md`, `tool_testing_guidelines.md` |
| **Security** | System-wide security protection and hardening | `security_guidelines.md` |
| **Data & Storage** | Schema definitions and memory snapshots | `data_schema_spec.md` |
| **Simulation & Testing** | Logs, testing, simulated agent behavior | `agent_simulation_log.md`, `tool_testing_guidelines.md` |
| **Architecture** | Overall system and deployment structure | `architecture_overview.md` |

---

## 🚀 Quick Start

1. Set up your Python environment:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Configure `.env`:

```python
OPENAI_API_KEY=your-key
GOOGLE_DRIVE_CREDENTIALS_JSON=...
POSTGRES_URL=...
REDIS_URL=...
```

3. Launch Backend Services:

```bash
cd backend
uvicorn main:app --reload
celery -A app.celery_worker worker --loglevel=info
```

4. Start Frontend:

```bash
cd frontend
npm install
npm run dev
```

---

## 🔒 Deployment Guide (Production)

- Use Gunicorn/Uvicorn + Nginx to serve backend APIs
- Enable HTTPS with Let's Encrypt certificates
- Dockerize services (backend, worker, Redis)
- Use Cloud Run (GCP) or EC2 (AWS) for auto-scaling
- Separate environment variables per environment (dev/stage/prod)
- Protect database and queue services with VPC/private networking
- Rotate secrets regularly (at least every 90 days)

Example docker-compose.yml (backend stack):

```yaml
version: '3'
services:
  api:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - ENV=production
      - POSTGRES_URL=...
  celery_worker:
    build: ./backend
    command: celery -A app.celery_worker worker --loglevel=info
    depends_on:
      - api
      - redis
  redis:
    image: redis:alpine
```

---

## 📚 Related Files by Category

### Frontend

- `frontend_service_spec.md`

### Agent Planning Layer

- `ai_agent_layer_spec.md`
- `prompt_template.md`
- `tool_registry.md`

### Backend Execution

- `ai_agent_backend_spec.md`
- `tool_testing_guidelines.md`

### Data & State

- `data_schema_spec.md`

### Security

- `security_guidelines.md`

### Simulation & Testing

- `agent_simulation_log.md`
- `tool_testing_guidelines.md`

### System Architecture

- `architecture_overview.md`

---

## ✨ Notes

- This project is fully modular. Each service can be scaled independently.
- The AI Agent is goal-driven, not task-driven. It reasons dynamically per order.
- Best practices for security, scaling, and reliability are embedded across all layers.

Let's automate, intelligently! 🚀
