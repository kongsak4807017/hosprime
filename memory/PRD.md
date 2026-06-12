# HosPRIME - Product Requirements Document (Memory)

## Original Problem Statement
"สร้าง ทั้งหมดนี้ ให้พร้อม upขึ้น github เป็น master product ครับ" — Build HosPRIME, an enterprise-grade web-based Hospital Management System managing all hospital data/systems, with Knowledge Graph, AI agents, AI/ML, and LLM features. Use Emergent Universal Key for LLM. User language: **Thai** (always respond in Thai).

## User Choices (confirmed 2026-06-12)
- Auth: JWT email/password + RBAC 7 roles (admin, doctor, nurse, pharmacist, lab_technician, finance, patient)
- UI language: Thai primary
- Phase 1 scope: Auth + Patient Management + Appointments

## Architecture
- Backend: FastAPI + MongoDB (motor), modular: `/app/backend/core/` (database, security, utils, seed), `/app/backend/models/schemas.py`, `/app/backend/routes/` (auth, patients, appointments, dashboard), tests at `/app/backend/tests/backend_test.py` (27 pytest, all passing)
- Frontend: React 19 + Tailwind + shadcn, design per `/app/design_guidelines.json` (Forest Green #1E3F33 / Bone White, fonts: Prompt + IBM Plex Sans Thai)
- Auth: httpOnly cookies (access 60min + refresh 7d), bcrypt, brute-force lockout (5 fails/15min), audit_logs collection, JWT has iat/jti
- IDs: uuid string `id` field (Mongo `_id` excluded from all responses); numbers via counters collection (PAT-XXXXXX, APT-XXXXXX)
- Blueprints: /app/01_PRD_HIOS.md ... 08_ROADMAP_AND_IMPLEMENTATION_PLAN.md

## Implemented (2026-06-12) — Phase 1 Foundation ✅ TESTED
- JWT Auth: login/logout/me/refresh/register(admin)/users(admin), 7-role RBAC, admin+staff seeding
- Patients: CRUD + Thai search + filters + pagination + soft delete (admin) + vitals records + allergy/chronic/medication lists
- Appointments: booking (double-booking guard 409), doctors list, filters (date/status/search), status workflow scheduled→confirmed→checked_in→in_progress→completed/cancelled/no_show
- Dashboard: KPIs, 7-day trend chart, today's queue, recent patients
- Frontend pages (Thai): Login, Dashboard, Patients list/form/detail, Appointments; role-based sidebar with "coming soon" modules
- Seed data: 8 Thai patients, 8 appointments, 7 user accounts (see /app/memory/test_credentials.md)
- Testing: testing_agent iteration_1 — backend 96%→fixed→27/27 pytest pass, frontend 100%

## Implemented (2026-06-12) — Phase 2 Clinical Modules ✅ TESTED
- **Pharmacy** (`routes/pharmacy.py`, `PharmacyPage.jsx` 3 tabs): drug inventory CRUD (DRG-XXXXXX) + batches, stock adjust (atomic guarded $inc with rollback on dispense), low-stock + 90-day expiry alerts (/api/pharmacy/alerts), prescriptions (PRE-XXXXXX, doctor creates, pharmacist dispenses → stock deducted, cancel)
- **Laboratory** (`routes/lab.py`, `LabPage.jsx`): 8-test catalog with parameters + reference ranges (CBC, FBS, Lipid, HbA1c, LFT, Kidney, UA, TSH), order (LAB-XXXXXX, doctor) → collect sample (SMP id, lab tech/nurse) → enter results (auto abnormal flagging vs ref range, unknown param = 400) → view results with red ผิดปกติ flags
- **Billing** (`routes/billing.py`, `BillingPage.jsx`): invoices (INV-XXXXXX, server-computed totals, finance/admin), payments (partial/full → status pending/partially_paid/paid, overpay 400), insurance claims (CLM-XXXXXX submit → approve/reject with approved_amount), cancel, /api/billing/stats (revenue today/month UTC, outstanding, pending count)
- RBAC enforced: prescribe=doctor/admin, dispense+drug write=pharmacist/admin, lab order=doctor/admin, collect=lab/nurse/admin, results=lab/admin, billing write=finance/admin; all staff read
- Seed: 10 drugs (Amlodipine low-stock, Amoxicillin expiring ~45d), 2 prescriptions, 3 lab tests, 3 invoices
- Testing: testing_agent iteration_2 — backend 32/32, frontend 100%; full pytest suite 59/59 at /app/backend/tests/

## Implemented (2026-06-12) — Phase 3 Intelligence Layer ✅ TESTED
- **AI Core** (`core/ai.py`): switchable provider — Emergent Universal Key (openai/anthropic/gemini via emergentintegrations, default gpt-5.2 VERIFIED; gpt-5.4/5.5 NOT available on key) OR custom OpenAI-compatible endpoint (base_url+api_key+model, supports local Ollama/LM Studio). Settings in db.settings _id=ai
- **AI Settings** (`routes/ai_settings.py`, `/ai-settings` admin): provider/model config UI, masked keys, test-connection endpoint
- **Data Connector & Governance Agent** (`routes/connector.py`, `/connector` admin): sources = internal DB + external MongoDB (conn string) + CSV/Excel upload (pandas, 20MB cap, stores first 1000 rows); One-Click Scan = schema discovery (field types, fill rates, max 30 collections, 100-doc samples) + PII/PDPA keyword detection + LLM governance analysis (mapping/PDPA/quality/KG suggestions in Thai markdown)
- **Knowledge Graph** (`routes/graph_kg.py`, `/graph` staff): build (admin/doctor) from patients/doctors/drugs/conditions/allergens/labtests/departments → kg_nodes/kg_edges (deterministic keys, weighted edges, curated DRUG_INTERACTIONS); interactive react-force-graph-2d viz with type filters + node neighbor panel; Thai NL query → subgraph context → LLM answer
- **Digital Twin Agents** (`routes/agents.py`, `/agents` staff): 6 หัวหน้างาน personas (director, cmo, head_nurse, head_pharmacy, head_lab, head_finance) each with live DB context builder injected per call; multi-turn sessions (agent_sessions/agent_messages, last-12 history window, user-scoped)
- Testing: testing_agent iteration_3 — backend 32/32, frontend 100%; pytest test_phase3.py added (~2.5 min, real LLM calls)

## Backlog / Roadmap
### P0 — Phase 4
- Bed & room management (เตียงผู้ป่วย), staff scheduling (บุคลากร), advanced reports/exports (รายงานวิเคราะห์)
- Patient portal (patient role currently placeholder)
- GitHub master product preparation (README, docker, env docs)
### P1 — Enhancements
- AI Drug interaction checker inline on prescription creation
- Auto-invoice from prescriptions + completed labs
- Lab report AI summarization, no-show prediction
- Embeddings-based KG query (current: substring match + LLM fallback), context caching for agents (30s)
- MFA, streaming (SSE) agent replies

## Known Notes
- CORS_ORIGINS="*" + credentials: fine same-origin; set explicit origin for production deploy
- Cookies secure=False (preview); set True for production HTTPS
- Patient role login shows portal placeholder (full portal = Phase 4)
