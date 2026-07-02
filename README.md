# HosPrime — Health Organization Operating System

HosPrime is an institutional intelligence platform for healthcare and public-health organizations.

## Current release target

The repository contains prototypes for Knowledge Oracle, Meeting Memory, Digital Twins, Graph, AI Workflows and HITL. These components are not all production-ready.

The current controlled release target is:

**Milestone 1 — Governed Knowledge Oracle MVP**

A successful Milestone 1 must ingest approved documents, retrieve evidence, answer only when evidence is sufficient, provide traceable citations, enforce access control, and record audit and cost data.

## Core rules

```text
No Evidence -> No Factual Answer
No Identity -> No Access
No Human Approval -> No High-impact Action
No Execution Record -> Never Claim Completion
No Quality Gate -> No Release
```

## Secure local setup

### Backend

```bash
cd backend
python -m venv .venv
pip install -r requirements.txt
cp .env.example .env
```

Configure the local `.env` file with your own newly issued credentials:

```env
ENVIRONMENT=development
GEMINI_API_KEY=replace-with-a-new-provider-key
JWT_SECRET=replace-with-a-long-random-secret
DATABASE_URL=sqlite:///./hosprime.db
ALLOW_DEMO_FALLBACKS=false
ALLOW_PSEUDO_EMBEDDINGS=false
```

Run from the repository root:

```bash
python -m backend.app.db.bootstrap
uvicorn backend.app.main:app --reload
```

API documentation: `http://localhost:8000/docs`

Health endpoints:

```text
GET /health/live
GET /health/ready
```

### Frontend

```bash
cd frontend
npm ci
npm run dev
```

Open `http://localhost:5173`.

## Security notice

A provider credential was previously committed to repository history. The repository owner must revoke or rotate it and review provider usage. Removing it from the current file does not remove it from Git history.

Never commit real credentials, passwords, tokens or connection strings.

## Workflow boundary

The current workflow module creates a plan and sends it to the HITL queue. It does not contain a configured external executor.

An approved plan is recorded as:

```text
APPROVED_NOT_EXECUTED
```

It must not be reported as a completed real-world action.

## Project control documents

See the controlled plans under:

- `docs/architecture/`
- `docs/governance/`
- `docs/roadmap/`

## Milestone sequence

```text
M1 Governed Knowledge Oracle
M2 Organization Memory
M3 Executive Office and Role Twin
M4 Backoffice AI Workforce and AIOC
M5 Forecast, Scenario and Provincial Health Brain
```
