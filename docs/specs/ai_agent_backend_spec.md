# 🤖 AI Agent + Backend Service Specification

## 🔧 Technical Design

### Purpose

This service handles all automation logic for:

- Order intake and processing
- AI-generated design creation
- Google Drive & Excel automation
- Customer notification & system status updates
- Admin command processing and execution

### Architecture Overview

- **API Layer**: FastAPI or Flask (FastAPI preferred)
- **Task Queue**: Celery + Redis (for background task processing)
- **AI Engine**: HuggingFace Diffusers (Stable Diffusion), OpenAI (fallback)
- **Storage**: Google Drive API, local fallback
- **Excel Handling**: openpyxl
- **Database**: PostgreSQL or MongoDB

### Folder Structure (Suggested)

```
app/
├── api/
│   ├── routes/
│   │   ├── orders.py
│   │   ├── admin.py
│   │   └── auth.py
│   └── schemas/
├── core/
├── services/
│   ├── design_generator.py
│   ├── gdrive_manager.py
│   ├── excel_handler.py
│   ├── notifier.py
│   └── sheet_manager.py
├── tasks/  # Celery async jobs
├── models/  # DB Models
├── config.py
└── main.py
```

### Main Endpoints

#### Customer Flow Endpoints

- `POST /orders`: Accept new order, trigger pipeline
- `GET /orders/:id`: Fetch order metadata & progress
- `POST /orders/:id/approve`: Trigger approval logic
- `POST /orders/:id/retry`: Retry failed task in pipeline

#### Admin Flow Endpoints

- `POST /admin/commands`: Process admin natural language commands
- `GET /admin/sheets`: List Google Sheets matching criteria
- `POST /admin/sheets`: Create new Google Sheet from template
- `GET /admin/files`: List files in Google Drive folder
- `POST /admin/summary`: Generate summary sheet from data sources

### Task Pipeline

#### Customer Order Pipeline

1. Receive order data (text + image)
2. Create Google Drive folder
3. Generate design using AI model (Stable Diffusion)
4. Create & populate Excel file
5. Upload files to folder
6. Notify customer/operator (email or webhook)

#### Admin Command Pipeline

1. Receive admin command (natural language)
2. Parse command intent and parameters
3. Execute appropriate Google Drive/Sheets operation
4. Return results to admin user

## 🧠 AI Agent Integration

### Agent Session Management

- Each order or admin command creates a new `AgentSession`
- Session maintains state, history, and context
- Agent determines next steps based on goal and available tools

### Tool Registry

- Backend exposes functionality as tools for the agent
- Each tool has clear input/output schema
- Tools are registered in a central registry
- Admin-specific tools are only available to authenticated admins

## 🔒 Security & Authentication

### Authentication Methods

- JWT-based auth for all API endpoints
- Role-based access control (RBAC) for admin endpoints
- API keys for service-to-service communication

### Data Protection

- All sensitive data encrypted at rest
- HTTPS for all API communication
- Audit logging for all admin operations

## 📊 Monitoring & Logging

### Logging Strategy

- Structured JSON logs
- Log levels: DEBUG, INFO, WARNING, ERROR
- Request ID tracking across services

### Metrics

- Request latency
- Error rates
- Task completion rates
- Resource utilization

## 🧪 Testing Strategy

### Unit Tests

- Test each tool function in isolation
- Mock external dependencies

### Integration Tests

- Test complete pipelines
- Use test fixtures for consistent data

### End-to-End Tests

- Simulate real user flows
- Test both customer and admin scenarios

## 📝 API Documentation

### OpenAPI/Swagger

- Auto-generated from code
- Interactive documentation
- Example requests/responses

---

This specification defines the backend services that power the AI Agent system, handling both customer order processing and admin command execution.
