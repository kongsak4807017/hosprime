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

## Backlog / Roadmap
### P0 — Phase 2: Clinical Modules
- Pharmacy management (drug inventory, prescriptions, dispensing, expiry alerts)
- Laboratory management (test orders, samples, results, reference ranges)
- Billing & finance (invoices, payments, insurance claims)
### P1 — Phase 3: Intelligence Layer (use Emergent LLM Key: available in env)
- AI Medical Assistant chatbot (LLM, with session ids)
- Knowledge graph (medical knowledge queries)
- Predictive analytics (no-show prediction, risk stratification)
- Lab report summarization, drug interaction checker
### P2 — Phase 4
- Bed & room management, staff scheduling, advanced reports/exports, patient portal (patient role currently placeholder), MFA, GitHub master product preparation

## Known Notes
- CORS_ORIGINS="*" + credentials: fine same-origin; set explicit origin for production deploy
- Cookies secure=False (preview); set True for production HTTPS
- Patient role login shows portal placeholder (full portal = Phase 4)
