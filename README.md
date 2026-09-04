# REVORA AI — Merchant Growth & Agentic Commerce Platform

> **DOMAIN**: AI Growth & Agentic Commerce  
> An autonomous, bounded AI revenue intelligence system that discovers merchant opportunities, applies RAG policy guardrails, enforces human-in-the-loop approval gating, and maintains a strict audit trail.

---

## Executive Summary

Revora AI transforms passive payment gateways and e-commerce stores into proactive revenue engines. By continuously analyzing transaction, cart, and customer behavior data, Revora automatically detects high-value revenue recovery opportunities (abandoned carts, failed payment recovery, customer churn, and cross-sell potential). 

Unlike unconstrained AI agents that risk financial losses or customer dissatisfaction, Revora enforces **strict policy guardrails and approval gating**: every action recommended by the Growth Agent is evaluated against policy rules via RAG, verified for confidence and impact bounds, gated for merchant authorization, and recorded in an immutable audit trail.

---

## Core Differentiators

1. **Revenue Opportunity Detection**: Continuous real-time scanning of abandoned carts, failed gateway payments, customer dormancy, and cross-sell signals grounded in actual database ledger values.
2. **ML-Powered Customer Reactivation**: Scikit-Learn machine learning model scoring customer reactivation probabilities based on RFM features, lifetime value, and discount sensitivity.
3. **RAG-Based Policy Retrieval**: Retrieval-Augmented Generation that fetches relevant policy guardrails (`cart_recovery`, `payment_recovery`, `customer_reactivation`, `agent_safety`) for every opportunity type.
4. **Bounded Policy Engine & Guardrails**: Deterministic rules that enforce safety thresholds (e.g., minimum 40% confidence, positive monetary value, bounded discount limits) before any action is permitted.
5. **Human-in-the-Loop Approval Gating**: High-impact financial and customer-facing operations are paused in a `PENDING` approval state until authorized by the merchant.
6. **Immutable Audit Trail**: Full end-to-end traceability linking each opportunity, policy decision, agent action ID, and JSON metadata.
7. **Explainable AI Recommendations**: Concise reasoning explaining the business impact and recommended action, backed by a deterministic fallback that ensures zero downtime even if third-party LLMs fail.
8. **Fintech-Grade User Experience**: Crisp, Stripe/Razorpay-inspired interface featuring Indian currency formatting (`₹ Cr`, `₹ L`, `₹ K`), responsive navigation, live merchant switching, and clear guardrail indicators.

---

## Architecture Flow

```
                ┌───────────────────────────────────┐
                │          Merchant Data            │
                │  (Orders, Carts, Payments, Users) │
                └─────────────────┬─────────────────┘
                                  │
                                  ▼
                ┌───────────────────────────────────┐
                │       Revenue Intelligence        │
                │     (Aggregate Analytics & KPI)   │
                └─────────────────┬─────────────────┘
                                  │
                                  ▼
                ┌───────────────────────────────────┐
                │       Opportunity Detection       │
                │   (Cart, Payment, Dormant, Cross) │
                └─────────────────┬─────────────────┘
                                  │
                                  ▼
                ┌───────────────────────────────────┐
                │    ML / Business Intelligence     │
                │  (Reactivation Probability Model) │
                └─────────────────┬─────────────────┘
                                  │
                                  ▼
                ┌───────────────────────────────────┐
                │       RAG Policy Retrieval        │
                │    (Knowledge Base Guardrails)    │
                └─────────────────┬─────────────────┘
                                  │
                                  ▼
                ┌───────────────────────────────────┐
                │           Policy Engine           │
                │   (Confidence & Impact Bounds)    │
                └─────────────────┬─────────────────┘
                                  │
                                  ▼
                ┌───────────────────────────────────┐
                │           Growth Agent            │
                │     (Bounded Recommendations)     │
                └─────────────────┬─────────────────┘
                                  │
                                  ▼
                ┌───────────────────────────────────┐
                │       Approval Gate (HITL)        │
                │   (Required for Sensitive Acts)   │
                └─────────────────┬─────────────────┘
                                  │
                                  ▼
                ┌───────────────────────────────────┐
                │           Agent Action            │
                │      (Dispatched / Queued)        │
                └─────────────────┬─────────────────┘
                                  │
                                  ▼
                ┌───────────────────────────────────┐
                │            Audit Log              │
                │      (Immutable Traceability)     │
                └───────────────────────────────────┘
```

---

## Technology Stack

- **Frontend**: Next.js 16 (App Router), TypeScript, Tailwind CSS 4, React 19
- **Backend API**: FastAPI, Starlette, Pydantic v2, Uvicorn
- **Database & ORM**: SQLite (pre-seeded enterprise scale), SQLAlchemy 2.0
- **Machine Learning**: Scikit-Learn, Joblib, NumPy
- **RAG & Reasoning**: In-memory policy document knowledge base, OpenAI GPT-4.1-mini integration with deterministic fail-safe fallback
- **Testing**: Pytest, Starlette TestClient

---

## Database Scale (Pre-Seeded Synthetic Data)

- **10 Merchants**: Multi-category coverage (Jewelry, Electronics, Fashion, Grocery, Beauty, Pharmacy, Sports, Books, Pets, Home)
- **5,000 Customers**: Complete with behavioral RFM attributes, engagement scores, and discount sensitivities
- **300 Products**: Multi-tier catalog items
- **8,000 Carts & Cart Items**: Abandoned checkout states with monetary tracking
- **12,000 Orders & 12,000 Payments**: Transaction ledgers with success, timeout, and failure tracking
- **3,000+ Agent Actions**: Historical and dynamically generated policy-bounded actions
- **6,000+ Audit Logs**: Complete event trail for regulatory traceability

---

## Key Backend API Endpoints

### Health & Information
- `GET /` — API service identity & version
- `GET /health` — Service health status
- `GET /api/merchants` — List all registered merchants

### Revenue Intelligence
- `GET /api/revenue/overview?merchant_id={id}` — Current revenue, estimated opportunity, opportunity breakdown, high priority count, top opportunities
- `GET /api/revenue/opportunities?merchant_id={id}&opportunity_type={type}&priority={priority}&limit={n}` — Filtered list of bounded opportunities
- `GET /api/revenue/merchants/{merchant_id}` — Merchant-specific revenue analytics

### Growth Agent & Governance
- `POST /api/agent/analyze/{merchant_id}?limit={n}` — Triggers autonomous agent analysis, RAG policy evaluation, guardrail validation, action persistence, and explainable AI generation
- `GET /api/agent/actions/{merchant_id}?limit={n}` — List of bounded agent actions and approval states
- `GET /api/agent/audit-logs/{merchant_id}?limit={n}` — Complete audit log trail with metadata

---

## Local Setup & Execution Guide

### Prerequisites
- Python 3.11+
- Node.js 18+ & npm

### 1. Backend Setup

```bash
cd backend

# Activate virtual environment
# Windows:
.\.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# (Optional) Set OpenAI API key for live GPT-4.1 explanations
# If omitted, Revora automatically uses its deterministic fail-safe engine
export OPENAI_API_KEY="your-api-key-here"

# Start the FastAPI server
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

The backend will be live at `http://127.0.0.1:8000`.  
Interactive Swagger docs: `http://127.0.0.1:8000/docs`.

### 2. Frontend Setup

In a separate terminal:

```bash
cd frontend

# Install dependencies (if not already installed)
npm install

# Start the Next.js development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## Running Automated Tests

Revora AI includes a comprehensive test suite testing all endpoints, policy checks, and database relationships:

```bash
cd backend
.\.venv\Scripts\python -m pytest -v
```

To test the frontend production build:

```bash
cd frontend
npm run build
```

---

## Environment Variables

| Variable | Location | Default | Description |
|---|---|---|---|
| `NEXT_PUBLIC_API_URL` | `frontend/.env.local` | `http://127.0.0.1:8000` | Backend API URL accessed by frontend |
| `OPENAI_API_KEY` | `backend/.env` | Optional | OpenAI API key for LLM explanations (falls back safely if absent) |

---

## Dashboard Walkthrough & User Experience

1. **Top Header**: Live status pill (`● AI Agent Active`), dynamic merchant selector (default: `#10 Lumen Jewels`), and instant data refresh button.
2. **KPI Overview**: 4 live cards with Indian currency notation (`₹ Cr`, `₹ L`, `₹ K`): Current Revenue, Estimated Opportunity, High Priority Opportunities, and AI Actions Generated.
3. **Revenue Breakdown**: Proportional horizontal bar showing contribution across Abandoned Cart Recovery, Cross-Sell, Failed Payment Recovery, and Dormant Reactivation.
4. **Growth Agent Section**: Interactive trigger to run `POST /api/agent/analyze/10`. Shows live reasoning steps and displays recommendation cards with RAG policy tags, explainable reasoning, and approval badges (`✓ Policy Allowed`, `⚠ Approval Required`).
5. **Top Opportunities Table**: Filterable table with priority badges (`HIGH`, `MEDIUM`, `LOW`), ML confidence meters, and recommended actions.
6. **Actions & Approvals**: Dedicated view for monitoring bounded actions, execution status (`PENDING`, `EXECUTED`, `SKIPPED`), and policy compliance.
7. **Audit Log**: Transparent audit records with expandable JSON payload view.
8. **Settings**: Policy guardrails inspection showing confidence thresholds, value constraints, and active RAG policy documents.

---

## Future Enhancements

- **Direct Razorpay Webhook Ingestion**: Webhook listeners to instantly ingest checkout abandonment and payment failure events.
- **WhatsApp & SMS Channel Connectors**: Direct outbound messaging connectors for authorized cart recovery offers.
- **Dynamic Policy Editor**: In-app UI allowing merchants to author and update RAG policy documents and approval rules on the fly.
- **Multi-Merchant Comparative Benchmarking**: Cohort analysis comparing conversion benchmarks across merchants in the same category.
