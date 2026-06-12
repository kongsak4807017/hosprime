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

## Backlog / Roadmap
### P0 — Phase 3: Intelligence Layer (use Emergent LLM Key: available in env)
- AI Medical Assistant chatbot (LLM, with session ids)
- AI Drug interaction checker on prescriptions
- Knowledge graph (medical knowledge queries)
- Predictive analytics (no-show prediction, risk stratification)
- Lab report summarization
### P1 — Phase 4
- Bed & room management, staff scheduling, advanced reports/exports, patient portal (patient role currently placeholder), MFA, GitHub master product preparation

## Known Notes
- CORS_ORIGINS="*" + credentials: fine same-origin; set explicit origin for production deploy
- Cookies secure=False (preview); set True for production HTTPS
- Patient role login shows portal placeholder (full portal = Phase 4)
