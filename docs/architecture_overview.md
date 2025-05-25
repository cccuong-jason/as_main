# 🏗️ System Architecture Overview – AI Agent for Print-on-Demand

## 🎯 Goal

This document describes the full architecture for a custom T-shirt order automation system powered by an LLM-based AI Agent. It supports full pipeline automation from customer request to order finalization.

---

## 🧱 Layered System Architecture

```plaintext
┌────────────────────────────────────────────────────────┐
│                    🌐 Frontend (UI)                    │
│ - Customer form (React + Tailwind)                     │
│ - Order preview, status dashboard                      │
│ - Sends API calls to backend                           │
└──────────────┬─────────────────────────────────────────┘
               │
               ▼
┌────────────────────────────────────────────────────────┐
│               🔄 API Gateway / Controller              │
│ - FastAPI endpoints                                    │
│ - Validates inputs                                     │
│ - Triggers AgentSession (via AgentRouter)              │
└──────────────┬─────────────────────────────────────────┘
               │
               ▼
┌────────────────────────────────────────────────────────┐
│             🧠 AI Agent Orchestration Layer             │
│ - Powered by LangChain Agent / OpenAI GPT-4            │
│ - Plans steps, chooses tools, loops with memory        │
│ - Maintains short/long-term state                      │
│ - Uses prompt template + tool registry                 │
└──────────────┬─────────────────────────────────────────┘
               │
               ▼
┌────────────────────────────────────────────────────────┐
│               ⚙️ Tool Execution Services               │
│ - generate_design (Diffusion, Pillow)                  │
│ - create_excel_file (openpyxl, pandas)                 │
│ - upload_to_drive (Google API)                         │
│ - notify_customer (Email/FB API)                       │
└──────────────┬─────────────────────────────────────────┘
               │
               ▼
┌────────────────────────────────────────────────────────┐
│                   🛢️ Infrastructure Layer             │
│ - PostgreSQL / MongoDB (orders, agent state)           │
│ - Redis + Celery (task queue)                          │
│ - GCP / AWS / Docker deployment                        │
│ - Logging & Monitoring                                 │
└────────────────────────────────────────────────────────┘
```

---

## 🔐 Security Boundaries

- JWT-based auth at API layer
- Tool access only through registry-controlled Agent
- LLM output validated with `PlanValidator`
- Google/Facebook API scoped via OAuth tokens

## 🔁 Data Flow

```
Customer → Frontend → FastAPI → AgentSession → [Tool Calls] → State Updated → Notify Customer
```

## 🔄 Example Sequence

1. Customer submits order form → `POST /orders`
2. FastAPI validates, starts `AgentSession(order_id)`
3. Agent sees goal: "process this order"
4. Agent selects tool: `generate_design(prompt)`
5. Receives result → `upload_to_drive()` → `create_excel()`
6. Agent updates DB, triggers `notify_customer()`
7. Frontend polls `/orders/:id` → shows progress

---

This architecture supports flexible, intelligent order fulfillment, and can be extended with voice input, multi-agent planning, or analytics in the future.
