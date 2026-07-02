# HOSPRIME — Progression Note for Senior Developer
**Date:** 2026-06-16  
**From:** AI Agentic Architect / Backend AI Lead  
**To:** Senior Developer Team  
**Subject:** Current State Assessment → Enterprise AI Agent Office Roadmap  
**Version:** 1.0  
**Classification:** Internal Engineering Roadmap

---

## 1. Executive Summary

ระบบ HosPrime ปัจจุบันอยู่ในระดับ **Milestone 1: Knowledge Oracle MVP (~75% Complete)** มีโครงสร้างพื้นฐานที่ใช้งานได้ (FastAPI + React + SQLite + Gemini API) แต่ยังไม่สามารถใช้งานในระดับ Enterprise (220-300 users, Multi-Agent Orchestration, Real-time Digital Twin, Production Security) ได้  

เอกสารนี้ประกอบด้วย:
- สถานะระบบปัจจุบันในมุมมองเทคนิคลึก
- ช่องโหว่ (Gaps) ที่ต้องแก้ไขก่อนขึ้น Production
- Enterprise Architecture Blueprint 8-Layer
- แผนการพัฒนา 4 Phase พร้อม Deliverables ชัดเจน
- Immediate Action Items 30 วันข้างหน้า
- Technical Decision Records (TDR)

---

## 2. Current State — Technical Assessment

### 2.1 Repository Structure

```
HODTprime/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI entry point (CORS, Routers)
│   │   ├── auth.py                 # JWT + bcrypt (Basic)
│   │   ├── config.py               # Settings via pydantic
│   │   ├── db/
│   │   │   ├── session.py          # SQLAlchemy engine (SQLite)
│   │   │   ├── models.py           # Core models (Document, Chunk, QueryLog, User, Meeting, WorkflowRun)
│   │   │   └── bootstrap.py        # Seed data for twins
│   │   ├── models/
│   │   │   └── twin_models.py      # Digital Twin schema (Organization, Role, Person, Agent, Knowledge, etc.)
│   │   ├── schemas/
│   │   │   ├── schemas.py          # Pydantic schemas (Document, etc.)
│   │   │   ├── twin_schemas.py     # Twin CRUD schemas
│   │   │   └── auth_schemas.py     # Login/Register schemas
│   │   ├── api/
│   │   │   ├── router.py           # API router aggregator
│   │   │   └── endpoints/
│   │   │       ├── auth.py         # Login, register, me
│   │   │       ├── documents.py    # Upload, list, delete docs
│   │   │       ├── oracle.py       # /ask (RAG endpoint)
│   │   │       ├── twins.py        # CRUD twins + consult agent (~42KB — largest file)
│   │   │       ├── workflows.py    # Workflow trigger/status
│   │   │       ├── meetings.py     # Meeting upload, summary, action items
│   │   │       ├── admin.py        # Admin dashboard data (~19KB)
│   │   │       ├── graph.py        # Graph DB proxy endpoints
│   │   │       └── twins_full.py   # Extended twin API (~8KB)
│   │   ├── agents/
│   │   │   ├── agents.py           # 10 Knowledge Agents pipeline (~19KB)
│   │   │   ├── executive_twin_agent.py  # Executive consultation (~3KB)
│   │   │   ├── meeting_memory_agent.py  # Meeting processing (~4KB)
│   │   │   ├── workflow_agent.py        # Workflow definitions (~5KB)
│   │   │   └── graph_rag_agent.py       # Graph RAG prototype (~4KB)
│   │   └── services/
│   │       ├── gemini_service.py   # Gemini API wrapper (~23KB) — CRITICAL PATH
│   │       ├── orchestrator.py     # MasterOrchestrator (~9KB)
│   │       ├── twin_service.py     # Twin business logic (~6KB)
│   │       ├── workflow_service.py # Workflow runner (~0.7KB)
│   │       ├── document_parser.py  # PDF/DOCX/TXT parser (~3KB)
│   │       ├── graph_db_service.py # Neo4j wrapper + mock fallback (~5KB)
│   │       └── speech_to_text.py # Audio transcription (~3KB)
│   ├── requirements.txt            # FastAPI, SQLAlchemy, google-generativeai, numpy, python-docx, PyPDF2
│   └── .env                      # GEMINI_API_KEY, SECRET_KEY, etc.
├── frontend/
│   ├── src/
│   │   ├── App.tsx                 # Main app router (~14KB)
│   │   ├── main.tsx                # Entry point
│   │   ├── index.css               # Tailwind base
│   │   ├── lib/api.ts              # Axios client + API wrappers (~16KB)
│   │   ├── components/
│   │   │   ├── Login.tsx           # Auth UI (~8KB)
│   │   │   ├── ThemeSwitcher.tsx   # Dark/light mode
│   │   │   └── tabs/
│   │   │       ├── HomeTab.tsx         # Dashboard home (~6KB)
│   │   │       ├── AskTab.tsx          # Oracle Q&A (~38KB)
│   │   │       ├── CatalogTab.tsx      # Document catalog (~9KB)
│   │   │       ├── UploadTab.tsx       # File upload (~7KB)
│   │   │       ├── AdminTab.tsx        # Admin panel (~62KB)
│   │   │       ├── ExecutiveTwinTab.tsx # Executive workspace (~161KB — largest component)
│   │   │       ├── GraphBrainTab.tsx     # Graph visualization (~10KB)
│   │   │       ├── MeetingMemoryTab.tsx  # Meeting tools (~31KB)
│   │   │       ├── AIWorkflowsTab.tsx    # Workflow UI (~7KB)
│   │   │       └── LogsTab.tsx           # Query/Agent logs (~35KB)
│   │   └── pages/                  # (empty directories)
│   ├── package.json                # React, Vite, Tailwind, shadcn deps
│   ├── vite.config.ts
│   └── tsconfig.json
├── hosprime_vibe_coding_seed/      # Reference docs (prompts, architecture, milestones)
├── docs/                           # (empty)
├── storage/                        # Uploaded files storage
├── demo_data/                      # Demo datasets
├── alembic/                        # DB migration (exists but needs verification)
├── alembic.ini                     # Alembic config
├── hosprime.db                     # Main SQLite DB (~1.7MB)
├── run.bat                         # Windows startup script
└── README.md                       # Project overview
```

### 2.2 What Works Right Now

| Feature | Status | Notes |
|---------|--------|-------|
| Document Upload (PDF/DOCX/TXT/MD) | ✅ Stable | `DocumentParser.parse_document()` uses `PyPDF2` + `python-docx` + plain text |
| Text Chunking | ✅ Stable | 800 chars chunk, 150 overlap, naive sentence boundary |
| Gemini Embedding | ✅ Stable | `gemini-embedding-001`, 3072-dim, fallback to pseudo-embedding if API down |
| Vector Search (Cosine Similarity) | ⚠️ MVP | In-memory scan over all chunks in SQLite. **O(n) complexity — will crash at >5K docs** |
| RAG Answer Generation | ✅ Stable | Strict prompt: grounded only, citation required, 6-section format in Thai |
| Document Classification | ✅ Stable | LLM-based classification into Policy/SOP/Meeting/Report |
| Metadata Extraction | ✅ Stable | Department, Program, Year, Owner, Entity Relations extracted via Gemini |
| Meeting Transcription | ✅ Basic | Speech-to-text via Gemini API, summary extraction, action item extraction |
| Agent Registry | ✅ Basic | 10 seeded agents with token quotas (mock financial model) |
| Basic Auth (JWT) | ✅ Stable | bcrypt + JWT, role-based access (admin/user/guest) |
| Admin Dashboard | ✅ Functional | Document mgmt, query logs, feedback review, agent settings |
| Executive Twin UI | ✅ Functional | UI-heavy but backend logic is thin (mostly prompt wrappers) |
| CORS | ✅ Configured | Allows localhost:5173, 3000, 8000 |

### 2.3 Critical Technical Debt

#### 2.3.1 Database Layer — SQLite is a Blocker

**ปัญหา:**
- `hosprime.db` เป็น SQLite ไฟล์เดี่ยว ขนาด ~1.7MB
- Write lock ทำให้ concurrent writes จากหลาย Agent จะพังทันที
- `DocumentChunk.embedding_data` เก็บ JSON string ของ embedding vector (3072 floats) ใน SQLite Text column — ไม่มี index, scan ทั้งหมดทุกครั้ง
- `EntityRelation` เก็บ relation แบบ flat table ไม่ใช่ graph structure จริง

**ผลกระทบ:**
- ด้วย 100 เอกสาร × 20 chunks = 2,000 rows. Scan 2,000 vectors × 3072 dims = 6M float operations/ query. ยังพอไหว.
- แต่ถึง 1,000 เอกสาร = 20,000 rows × 3072 = 61M operations/query. API จะ timeout.
- ไม่รองรับ 300 concurrent users.

#### 2.3.2 Vector Store — No ANN Index

**ปัญหา:**
```python
# backend/app/agents/agents.py — RetrievalAgent
chunks = db.query(DocumentChunk).join(Document).filter(Document.status == "processed").all()
# ... ดึงมาทั้งหมดแล้วคำนวณ cosine similarity ใน Python loop
```

ไม่มี Approximate Nearest Neighbor (ANN) index เช่น HNSW, IVFFlat, หรือแม้แต่ `pgvector` indexing.

#### 2.3.3 AI Runtime — Single Provider, No Fallback

**ปัญหา:**
- `GeminiService` ผูกติด `google.generativeai` ตัวเดียว
- Model ใช้ `gemini-2.5-flash` ทั้งหมด (ไม่แยก task)
- Fallback เป็น `pseudo-embedding` (hash-based) ไม่มี semantic meaning — ถ้า API down ระบบ RAG จะคืนผลลัพธ์ garbage
- ไม่มี **Circuit Breaker** — ถ้า Gemini quota exceeded ระบบจะ retry ซ้ำๆ จน crash

#### 2.3.4 Agent Architecture — Flat, Not Orchestrated

**ปัญหา:**
- `MasterOrchestrator` ใช้ Prompt-based decomposition โดยให้ Gemini แตกงานเป็น 3 steps แล้ว run ทีละ step ใน Python loop
- ไม่มี **State Machine** — ถ้า step 2 ล้ม ไม่มี retry mechanism, ไม่มี checkpoint
- ไม่มี **HITL Gateway** — ไม่สามารถ Pause workflow รอผู้ใช้อนุมัติได้
- Agent ทั้งหมดเป็น **Static Classes** ไม่มี lifecycle (spawn, health check, restart, scale)

#### 2.3.5 Security & Governance — Pre-Production

**ปัญหา:**
- `SECRET_KEY` อยู่ใน `.env` แต่ไม่มี rotation mechanism
- JWT token ไม่มี expiry / refresh token pattern
- Password hash ใช้ bcrypt แต่ไม่มี rate limiting → brute force ได้
- ไม่มี **Audit Trail Immutable** — `AgentLog` เก็บใน SQLite ปกติ แก้ไข/ลบได้
- ไม่มี **RBAC ระดับ Agent** — Agent ทุกตัวมีสิทธิ์เท่ากัน
- ไม่มี **PDPA Compliance Layer** — เอกสารราชการที่ upload ไม่มี data classification, retention policy, encryption at rest

#### 2.3.6 Frontend — Not Enterprise-Ready

**ปัญหา:**
- ไม่มี WebSocket — ทุกอย่างเป็น polling หรือ one-shot HTTP
- `ExecutiveTwinTab.tsx` 161KB — ใหญ่มาก ไม่มี lazy loading / code splitting ที่มีประสิทธิภาพ
- ไม่มี **Connection Pooling** — ถ้า 300 users เปิดพร้อมกัน จะเปิด 300 HTTP connections แยก
- ไม่มี **Progressive Loading** — โหลดทุกอย่างทีเดียว

---

## 3. Gap Analysis — Enterprise Readiness Matrix

| # | Dimension | Current (MVP) | Target (Enterprise) | Severity | Effort |
|---|-----------|---------------|---------------------|----------|--------|
| 1 | **Database** | SQLite | PostgreSQL + Read Replica + pgvector | 🔴 Critical | Medium |
| 2 | **Vector Search** | In-memory cosine scan | pgvector HNSW index / Qdrant ANN | 🔴 Critical | Medium |
| 3 | **Cache** | None | Redis (Session, Cache, Pub/Sub) | 🔴 Critical | Low |
| 4 | **Message Queue** | None | Kafka / RabbitMQ (Async tasks) | 🔴 Critical | Medium |
| 5 | **AI Gateway** | Gemini only | Multi-provider + Circuit Breaker + Fallback | 🔴 Critical | Medium |
| 6 | **Orchestrator** | Prompt-based loop | LangGraph State Machine + HITL | 🔴 Critical | High |
| 7 | **Agent Protocol** | None | A2A (Agent-to-Agent) + MCP (Model Context Protocol) | 🔴 Critical | High |
| 8 | **Knowledge Graph** | Neo4j mock | Neo4j / Neptune + Ontology + Reasoning | 🟡 High | High |
| 9 | **Graph RAG** | Prototype file only | Hybrid Vector+Graph RAG integrated | 🟡 High | Medium |
| 10 | **Data Platform** | None | Bronze-Silver-Gold + dbt + Airflow | 🟡 High | High |
| 11 | **HL7 FHIR** | None | FHIR Gateway (HAPI FHIR) | 🟡 High | High |
| 12 | **Digital Twin** | Schema only | 5-Twin Layer + Simulation + Forecast | 🟡 High | Very High |
| 13 | **Auth** | Basic JWT | ThaiD/SSO/LDAP + Keycloak | 🟡 High | Medium |
| 14 | **RBAC** | User-level | User + Agent-level RBAC/ABAC | 🟡 High | Medium |
| 15 | **Audit Trail** | SQLite table | Immutable WORM store (7 years) | 🟡 High | Medium |
| 16 | **PDPA** | None | Consent, Classification, Retention, Erasure | 🟡 High | Medium |
| 17 | **Real-time UI** | HTTP polling | WebSocket + Connection Pooling | 🟡 High | Medium |
| 18 | **Observability** | Python logging | OpenTelemetry + Centralized Logs | 🟡 High | Medium |
| 19 | **Eval Framework** | None | MLflow + Regression Tests + Eval Datasets | 🟡 High | Medium |
| 20 | **Prompt Versioning** | None | Prompt Registry + A/B Testing | 🟡 High | Low |
| 21 | **CI/CD** | None | GitHub Actions / GitLab CI + K8s | 🟡 High | Medium |
| 22 | **Containerization** | None | Docker + docker-compose + K8s manifests | 🟡 High | Low |
| 23 | **Cost Control** | Token quota table | Token Budget + Rate Limit + Hierarchical Summary | 🟡 High | Medium |
| 24 | **Mobile/PWA** | Desktop only | Responsive + PWA | 🟢 Medium | Medium |
| 25 | **Multi-modal** | Text only | Voice + Image + Video + GIS | 🟢 Medium | High |
| 26 | **Cross-Agency** | Single org | Federated Intelligence + HIE | 🟢 Medium | Very High |

---

## 4. Enterprise Architecture Blueprint (8-Layer)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ LAYER 8: EXPERIENCE LAYER                                                   │
│ ───────────────────────────────────────────────────────────────────────── │
│ • React 18 + TypeScript + Vite + TailwindCSS + shadcn/ui                  │
│ • WebSocket Client (real-time agent activity, live feed)                  │
│ • Role-Based Dashboard (นพ.สสจ. vs หัวหน้ากลุ่ม vs CIO)                    │
│ • PWA (Service Worker, offline cache for static assets)                    │
│ • Connection Pooling: 1 WS connection per user → Central Hub               │
│ • Lazy Loading + Code Splitting (React.lazy + Suspense)                    │
│ • Data Aggregation: 100ms debounce window for real-time updates            │
├─────────────────────────────────────────────────────────────────────────────┤
│ LAYER 7: AGENT ORCHESTRATION LAYER                                          │
│ ───────────────────────────────────────────────────────────────────────── │
│ • LangGraph (State Machine + Checkpoint + Pause/Resume)                    │
│   - Workflows: Idea→Brief→Plan→Build→Review→Report                        │
│   - Alert→Triage→Investigate→Decide→Act→Audit                            │
│   - Meeting→Extract→Assign→Track→Escalate→Close                          │
│ • A2A Protocol (Agent-to-Agent)                                            │
│   - Agent Cards: `/.well-known/agent.json`                                  │
│   - Capability Discovery + Peer-to-Peer messaging                          │
│ • MCP (Model Context Protocol)                                             │
│   - Schema-driven Tool Calling                                             │
│   - Audit every tool call at Protocol Layer                                │
│ • HITL Gateway                                                             │
│   - Interrupt → Human Review → Modify State → Resume                      │
│   - Approval Tokens for external actions (send memo, publish alert)        │
│ • Agent Registry + AIOC (AI Operations Center)                             │
│   - Agent Health Check, Restart, Scale, Versioning                         │
│   - Agent Lifecycle: Sandbox → Pilot → Production Assistive → Auto         │
├─────────────────────────────────────────────────────────────────────────────┤
│ LAYER 6: AI INTELLIGENCE LAYER                                              │
│ ───────────────────────────────────────────────────────────────────────── │
│ • AI Gateway ( abstraction layer )                                           │
│   - Providers: Gemini, OpenAI (GPT-4.5), Anthropic (Claude Sonnet/Opus)   │
│   - Local Models: vLLM / KServe / NIM (Llama 4 / Mistral Large)            │
│   - Routing: Task-based (simple→flash, complex→opus, sensitive→local)      │
│   - Circuit Breaker (fail-fast after 3 errors, fallback to next provider)  │
│   - Retry with Exponential Backoff                                         │
│   - Prompt Caching (reuse context for policy/KPI docs)                     │
│   - Hierarchical Summarization (reduce token usage)                         │
│ • Cost Control                                                             │
│   - Token Budget per Agent per Day                                         │
│   - Cost-per-request tracking in DB                                        │
│   - Rate Limiting (Redis-based sliding window)                             │
│ • Eval Framework                                                           │
│   - MLflow / PromptLayer for Prompt Versioning                             │
│   - Regression Test Suite (20 standard questions)                          │
│   - Metrics: Grounded Answer Rate, Citation Coverage, Latency, Cost       │
├─────────────────────────────────────────────────────────────────────────────┤
│ LAYER 5: DIGITAL TWIN LAYER                                                 │
│ ───────────────────────────────────────────────────────────────────────── │
│ • 5-Twin Hierarchy:                                                         │
│   1. Entity Twin    (Person, Bed, Staff, Equipment, Vehicle)               │
│   2. Process Twin   (OPD flow, OR schedule, Discharge, Claim)             │
│   3. Department Twin (OPD, IPD, ER, Finance, HR, TB, NCD)                  │
│   4. Organization Twin (Hospital / Provincial Health Office)               │
│   5. Ecosystem Twin  (Province, Health Region, Referral Network)          │
│ • Forecast Engine                                                           │
│   - Time-series models (Prophet / ARIMA / LSTM) for disease prediction     │
│   - Budget forecast (linear regression on historical spend)                  │
│   - Workforce forecast (retirement + training pipeline)                    │
│ • Simulation Engine                                                         │
│   - What-if: "If move 5 staff from dept A to B, what happens?"             │
│   - Bottleneck detection (Process Mining)                                  │
│   - Resource Optimizer (Linear Programming / OR-Tools)                     │
│ • Feedback Loop                                                             │
│   - Twin → Real System → Sensor Data → Twin Update (closed loop)           │
├─────────────────────────────────────────────────────────────────────────────┤
│ LAYER 4: KNOWLEDGE LAYER                                                    │
│ ───────────────────────────────────────────────────────────────────────── │
│ • Knowledge Graph (Neo4j / Amazon Neptune)                                  │
│   - Ontology Nodes: Person, Role, Department, KPI, Project, Budget,      │
│     Policy, Meeting, Incident, Decision, Document, Program                 │
│   - Relations: reports_to, owns, approved, responsible_for, affects,          │
│     related_to, supports, collaborated_with, decided_at                   │
│   - Graph Reasoning: Multi-hop queries ("Who approved PM2.5 budget?")        │
│ • RAG Pipeline (Hybrid)                                                     │
│   - Vector Store: pgvector HNSW index (MVP) → Qdrant/Milvus (Scale)        │
│   - Retrieval: Dense (vector) + Sparse (BM25) + Graph (entity)             │
│   - Reranking: Cross-encoder or ColBERT (later)                            │
│   - Citation: Source ID, Page, Line, Confidence Score                      │
│ • Organizational Memory                                                       │
│   - Meeting Memory (transcript, decision, action, owner)                   │
│   - Decision Graph (decision → policy → outcome → lesson learned)          │
│   - Lessons Learned (incident → RCA → prevention)                          │
│   - Best Practice Repository                                               │
├─────────────────────────────────────────────────────────────────────────────┤
│ LAYER 3: DATA PLATFORM LAYER                                                │
│ ───────────────────────────────────────────────────────────────────────── │
│ • Data Lakehouse (Bronze → Silver → Gold)                                   │
│   - Bronze: Raw data from source systems (FHIR, HIS, ERP)                  │
│   - Silver: Cleaned, normalized, deduplicated, master data                   │
│   - Gold: Curated Data Marts (KPI marts, Executive marts, Department marts)  │
│ • ETL/ELT Orchestration                                                     │
│   - Apache Airflow (batch pipelines)                                       │
│   - dbt (data transformation + documentation + tests)                      │
│   - Streaming: Kafka / Redpanda (near real-time)                           │
│ • Metadata & Lineage                                                        │
│   - DataHub (data catalog)                                                 │
│   - OpenLineage (pipeline lineage tracking)                                │
│   - KPI Dictionary (YAML/JSON — single source of truth)                    │
│   - Data Contracts (input/output schemas between systems)                  │
│ • Master Data Management                                                    │
│   - Patient Master Index (PMI)                                             │
│   - Provider Master Index                                                  │
│   - Organization Master (โครงสร้าง สสจ.)                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│ LAYER 2: INTEGRATION LAYER                                                  │
│ ───────────────────────────────────────────────────────────────────────── │
│ • FHIR Gateway (HAPI FHIR / IBM FHIR Server)                                │
│   - FHIR R4 Resources: Patient, Encounter, Observation, Condition,        │
│     Procedure, Medication, Organization, Practitioner, Location            │
│   - SMART on FHIR (OAuth2 for app auth)                                    │
│   - Subscription API (real-time clinical events)                           │
│ • API Wrapper Layer                                                         │
│   - HIS/EMR Adapter (REST/SOAP/HL7 v2)                                    │
│   - ERP Adapter (SAP/Oracle REST API)                                     │
│   - HR Adapter (ระบบบุคลากร ราชการ)                                         │
│   - Finance Adapter (งบประมาณ, GFMIS)                                     │
│ • Event-Driven Integration                                                  │
│   - Kafka Connect (CDC from source DBs)                                    │
│   - Message Schema: Avro / JSON Schema (registry)                          │
│   - Dead Letter Queue (DLQ) for failed events                              │
│ • GIS Integration                                                           │
│   - GeoServer / PostGIS (spatial queries)                                  │
│   - Heatmap, Disease Cluster, Service Gap layers                           │
│ • External APIs                                                             │
│   - Thai Meteorological Department (weather)                               │
│   - Department of Disease Control (surveillance)                             │
│   - HISO / ThaiHealthStat (health indicators)                              │
├─────────────────────────────────────────────────────────────────────────────┤
│ LAYER 1: ENTERPRISE SYSTEMS LAYER                                         │
│ ───────────────────────────────────────────────────────────────────────── │
│ • Source Systems (do NOT replace, only integrate):                          │
│   - HIS / EMR (Hospital Information System)                                │
│   - LIS (Laboratory)                                                        │
│   - RIS / PACS (Imaging)                                                    │
│   - ERP / Finance (SAP, Oracle, หรือ ราชการ)                               │
│   - HR System (บุคลากร, ตำแหน่ง, สิทธิ)                                    │
│   - Document Management (เอกสารราชการ)                                     │
│   - Email / Calendar (Outlook / Google Workspace)                          │
│   - Telemedicine Platform                                                   │
│   - HIE / FHIR Gateway (MOPH)                                              │
│   - Surveillance System (e.g., 506, e-Report)                              │
│   - IoT / Medical Devices (FHIR Observation)                                 │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Phase-by-Phase Implementation Plan

### Phase 1: Foundation Hardening (Month 1-3)
**Goal:** ยกระดับ MVP ให้เป็น Production-Grade Foundation รองรับ 50-100 users pilot

#### Month 1: Database & Infrastructure

**Deliverables:**
1. **PostgreSQL Migration**
   - Schema migration จาก SQLite → PostgreSQL 15+
   - ติดตั้ง `pgvector` extension
   - สร้าง Read Replica (ถ้า deploy บน Cloud)
   - Alembic migrations สำหรับทุก schema change ต่อจากนี้
   - **Schema Changes:**
     ```sql
     -- pgvector extension
     CREATE EXTENSION IF NOT EXISTS vector;
     
     -- DocumentChunk with vector type
     ALTER TABLE document_chunks 
     ADD COLUMN embedding vector(3072);
     
     -- HNSW index for ANN search
     CREATE INDEX ON document_chunks 
     USING hnsw (embedding vector_cosine_ops);
     ```

2. **Redis Setup**
   - Redis 7+ สำหรับ: Session Store, Cache Org Structure, Rate Limiting, Pub/Sub
   - Backend: `redis-py` + `fastapi-cache`
   - Frontend: WebSocket ผ่าน Redis Pub/Sub (ใช้ `socket.io` หรือ `fastapi-websocket`)

3. **Docker + Compose**
   ```yaml
   # docker-compose.yml
   services:
     postgres:
       image: pgvector/pgvector:pg15
       volumes:
         - postgres_data:/var/lib/postgresql/data
     redis:
       image: redis:7-alpine
     backend:
       build: ./backend
       depends_on: [postgres, redis]
     frontend:
       build: ./frontend
       ports: ["80:80"]
   ```

4. **Environment Management**
   - แยก `.env` เป็น `env/.dev`, `env/.staging`, `env/.production`
   - ใช้ `pydantic-settings` แทน `pydantic.BaseSettings` ถ้ายังไม่ได้ migrate
   - Vault integration (HashiCorp Vault หรือ AWS Secrets Manager) สำหรับ Production

**Success Criteria:**
- `docker-compose up` รันระบบทั้งหมดได้ในครั้งเดียว
- Load test: 100 concurrent users, 1000 docs, API latency < 2s สำหรับ /ask
- Zero data loss migration จาก SQLite

#### Month 2: AI Gateway + Security + Auth

**Deliverables:**
1. **AI Gateway Layer** (`backend/app/services/ai_gateway.py`)
   ```python
   class AIGateway:
       providers: Dict[str, LLMProvider]
       circuit_breakers: Dict[str, CircuitBreaker]
       
       def generate(self, prompt, task_type="simple"):
           # Route: simple→gemini-flash, complex→claude-opus, sensitive→local-vllm
           provider = self.route(task_type)
           try:
               return provider.generate(prompt)
           except QuotaExceeded:
               self.circuit_breakers[provider].record_failure()
               return self.fallback_provider.generate(prompt)
   ```
   - รองรับ: Gemini, OpenAI, Anthropic, Local (vLLM)
   - Circuit Breaker pattern (3 failures → open for 60s)
   - Prompt Caching: เก็บ context ที่ใช้ซ้ำ (KPI dict, policy pack) ใน Redis
   - Cost tracking: บันทึก cost/request ลง DB

2. **Authentication Upgrade**
   - ThaiD / SSO Integration (OAuth 2.1 / SAML 2.0)
   - ใช้ **Keycloak** เป็น Identity Broker (รองรับ ThaiD, LDAP, AD)
   - JWT Refresh Token pattern (access token 15min, refresh token 7 days)
   - MFA (TOTP) สำหรับ Admin และ Agent Operator

3. **RBAC ระดับ Agent**
   - ตารางใหม่: `agent_permissions` (agent_id, tool_name, action, allowed: bool)
   - ทุก Tool Call ตรวจสอบที่ Protocol Layer ก่อน execute
   - Forbidden Actions: `submit_claim`, `alter_financial_records`, `publish_alert_without_approval`

4. **Audit Trail Immutable**
   - แยกตาราง `audit_logs` ไปยัง database แยก (append-only, WORM)
   - หรือใช้ **Write-Ahead Log** + **S3/MinIO** สำหรับ long-term storage
   - ฟิลด์บังคับ: `agent_id`, `workflow_id`, `user_id`, `timestamp`, `input`, `output`, `tools_used`, `decisions`, `approval_token`
   - เก็บอย่างน้อย 7 ปี (ตามมาตรฐานราชการ)

**Success Criteria:**
- AI Gateway สลับ provider ได้ใน < 100ms
- Auth ผ่าน ThaiD mock server ได้
- Audit log ไม่สามารถแก้ไข/ลบได้ (append-only)

#### Month 3: Multi-Agent + LangGraph PoC

**Deliverables:**
1. **LangGraph Integration**
   - ติดตั้ง `langgraph` + `langchain` + `langsmith`
   - สร้าง State Graph แรก: `Executive Briefing Workflow`
     ```
     START → Decompose → [analyst, knowledge, cfo] → Synthesize → HITL(Review) → Generate → END
     ```
   - Checkpoint: บันทึก state ทุก step ลง PostgreSQL (via `langgraph-checkpoint-postgres`)
   - HITL: `interrupt` node ที่หยุดรออนุมัติ

2. **Agent Taxonomy Refactor**
   - แยกจาก 10 flat agents → 6 ประเภท Hierarchical:
     - **Executive Agent** (สรุป, ตัดสินใจ)
     - **Planner Agent** (แตกงาน, สร้าง brief)
     - **Analyst Agent** (SQL, วิเคราะห์, insight)
     - **Knowledge Agent** (RAG, citation, SOP)
     - **Action Agent** (draft memo, report, PPT)
     - **Department Agents** (NCD, TB, Finance, HR, etc.)
   - แต่ละ agent มี Job Description Template:
     ```yaml
     name: Finance Claim Agent
     mission: ตรวจจับ claim ตกหล่น
     inputs: [claim_queue, billing_logs]
     outputs: [exception_list, root_cause_summary]
     allowed_tools: [sql_readonly, claims_api_readonly]
     forbidden_actions: [submit_claim, alter_records]
     escalation_rule: confidence < 0.8 → CFO Agent + Human Reviewer
     ```

3. **MCP Protocol (Model Context Protocol)**
   - สร้าง `mcp_server` สำหรับ tools ที่ Agent เรียกใช้
   - JSON-RPC 2.0 สำหรับ tool definition
   - Schema validation ทุก request/response
   - Audit log ทุก tool call

4. **A2A Protocol (Agent-to-Agent)**
   - Agent Cards: แต่ละ agent ประกาศ capability ที่ `/.well-known/agent.json`
   - Handoff message schema (JSON) ตามที่ deep-research report กำหนด:
     ```json
     {
       "task_id": "TASK-2026-06-OPD-0012",
       "from_agent": "PlannerAgent",
       "to_agent": "AnalystAgent",
       "task_type": "analysis",
       "priority": "high",
       "objective": "Assess OPD waiting time root causes",
       "inputs": { "kpi_definitions_ref": "...", "data_sources": [...] },
       "constraints": { "must_cite_sources": true, "read_only": true },
       "expected_output": { "format": "analysis_memo", "confidence_required": 0.8 },
       "escalation": { "on_failure_to": "HumanReviewer" }
     }
     ```

**Success Criteria:**
- LangGraph workflow รัน end-to-end ได้
- HITL pause/resume ทำงาน
- Agent handoff ส่ง message ผ่าน API ได้

---

### Phase 2: Knowledge & Data Platform (Month 3-6)
**Goal:** สร้าง Knowledge Graph จริง + Data Platform สำหรับ Analytics

#### Month 4: Knowledge Graph + Graph RAG

**Deliverables:**
1. **Neo4j Production Setup**
   - Neo4j 5.x Enterprise (หรือ Community ถ้า budget จำกัด)
   - Ontology Schema:
     ```cypher
     CREATE CONSTRAINT person_id FOR (p:Person) REQUIRE p.id IS UNIQUE;
     CREATE CONSTRAINT role_id FOR (r:Role) REQUIRE r.id IS UNIQUE;
     CREATE CONSTRAINT dept_id FOR (d:Department) REQUIRE d.id IS UNIQUE;
     CREATE CONSTRAINT kpi_id FOR (k:KPI) REQUIRE k.id IS UNIQUE;
     CREATE CONSTRAINT policy_id FOR (p:Policy) REQUIRE p.id IS UNIQUE;
     ```
   - Node Labels: `Person`, `Role`, `Department`, `KPI`, `Project`, `Budget`, `Policy`, `Meeting`, `Incident`, `Decision`, `Document`, `Program`
   - Relationship Types: `REPORTS_TO`, `OWNS`, `APPROVED`, `RESPONSIBLE_FOR`, `AFFECTS`, `RELATED_TO`, `SUPPORTS`, `DECIDED_AT`, `MENTIONS`

2. **Graph RAG Integration**
   - Hybrid Retrieval Pipeline:
     1. Vector Search (pgvector) →  candidate chunks
     2. Entity Extraction from query →  Cypher query →  graph subgraph
     3. Merge: chunks + graph context →  LLM prompt
   - Graph Reasoning: Multi-hop queries เช่น "ใครเป็นคนอนุมัติงบ PM2.5 ปี 2568?"
     ```cypher
     MATCH (p:Person)-[:APPROVED]->(b:Budget {program: "PM2.5", year: "2568"})
     RETURN p.name, b.amount
     ```

3. **KnowledgeOps Agents**
   - **Knowledge Ingestion Agent** (existing) →  enhance ให้เขียนลง Neo4j ด้วย
   - **Entity Resolution Agent** (ใหม่): จับ entity ที่ชื่อคล้ายกัน (Dr. Somchai vs นพ.สมชาย) ให้เป็น node เดียวกัน
   - **Graph Maintenance Agent** (ใหม่): ตรวจสอบ orphaned nodes, แก้ inconsistent relationships

**Success Criteria:**
- Neo4j มี nodes > 1,000, relationships > 5,000
- Graph RAG query ตอบได้ใน < 3s
- Multi-hop reasoning ทำงานได้

#### Month 5: Data Platform (Bronze-Silver-Gold)

**Deliverables:**
1. **Airflow Setup**
   - DAGs สำหรับ:
     - `ingest_his_fhir`: ดึง FHIR Encounter จาก HIS → Bronze
     - `ingest_erp`: ดึงงบประมาณจาก ERP → Bronze
     - `transform_silver`: Clean, normalize, deduplicate → Silver
     - `build_kpi_mart`: คำนวณ KPI ต่างๆ → Gold
     - `sync_to_vector`: อัปเดต vector index เมื่อเอกสารใหม่เข้า

2. **dbt Project** (`dbt_hosprime/`)
   - Models:
     - `stg_encounters.sql` (Silver)
     - `stg_budgets.sql` (Silver)
     - `fct_kpi_monthly.sql` (Gold)
     - `dim_department.sql` (Gold)
     - `dim_person.sql` (Gold)
   - Tests: `not_null`, `unique`, `relationships`
   - Docs: auto-generated documentation

3. **KPI Dictionary** (`data_contracts/kpi_dictionary.yaml`)
   ```yaml
   kpi:
     waiting_time_opd:
       definition: "ระยะเวลารอคอยเฉลี่ยใน OPD (นาที)"
       formula: "AVG(encounter.wait_time_minutes)"
       source: "fct_encounters"
       owner: "กลุ่มงานบริหาร"
       refresh_frequency: "daily"
       target: "< 60 minutes"
       alert_threshold: "> 90 minutes"
   ```

4. **DataHub + OpenLineage**
   - Data Catalog: แสดงทุก dataset, owner, schema, freshness
   - Lineage: แสดงว่าตัวเลข KPI มาจาก pipeline ไหน, ผ่าน transformation อะไร
   - สำคัญมากสำหรับ Agent: ถ้า Agent ตอบคำถามผู้บริหาร ต้องบอกได้ว่า "ตัวเลขมาจากไหน"

**Success Criteria:**
- Airflow DAGs รันได้ไม่มี error
- dbt docs แสดง lineage ได้
- Agent ตอบคำถามพร้อม cite แหล่งที่มาของตัวเลข (pipeline + table)

#### Month 6: Integration Layer

**Deliverables:**
1. **FHIR Gateway PoC**
   - HAPI FHIR Server หรือ ใช้ `fhir.resources` Python library
   - Resources แรกที่ต้องเชื่อม: `Patient`, `Encounter`, `Observation`, `Practitioner`, `Organization`
   - FHIR Subscription: รับ event จาก HIS เมื่อมี encounter ใหม่
   - สร้าง `FHIRAdapter` class ใน backend:
     ```python
     class FHIRAdapter:
         def get_encounters(self, start_date, end_date, department=None):
             # Query HIS FHIR API → return FHIR Bundle
             pass
     ```

2. **API Wrapper Layer**
   - สร้าง `integration_catalog/` ใน backend:
     - `his_adapter.py` — HIS REST API wrapper
     - `erp_adapter.py` — ERP/งบประมาณ wrapper
     - `hr_adapter.py` — ระบบบุคลากร wrapper
     - `gis_adapter.py` — PostGIS/GeoServer wrapper
   - แต่ละ adapter มี: `owner`, `auth_method`, `data_contract`, `sync_mode`, `latency_expectation`, `allowed_agent_classes`

3. **Event Streaming (Kafka)**
   - Kafka topics:
     - `document.ingested` — เมื่อเอกสารใหม่เข้า
     - `kpi.updated` — เมื่อ KPI เปลี่ยน
     - `agent.task.completed` — เมื่อ Agent ทำงานเสร็จ
     - `alert.triggered` — เมื่อเกิด alert
   - Consumer: อัปเดต Digital Twin, ส่ง WebSocket ไป Frontend, บันทึก Audit Log

**Success Criteria:**
- FHIR Gateway ดึงข้อมูลจาก HIS mock server ได้
- Kafka topics รับ-ส่ง event ได้
- Integration catalog มี adapters ครบ 4 ตัว (HIS, ERP, HR, GIS)

---

### Phase 3: Digital Twin & Command Center (Month 6-9)
**Goal:** สร้าง Digital Twin ระดับองค์กร + All Activity Dashboard

#### Month 7: Digital Twin 5-Layer

**Deliverables:**
1. **Entity Twin**
   - Sync จาก HIS/HR: `Person`, `Bed`, `Equipment`, `Vehicle`
   - Real-time update: เมื่อ HIS มีการ admit/discharge → อัปเดต twin ทันที

2. **Process Twin**
   - OPD Flow: ลงทะเบียน → ตรวจ → จ่ายยา → จ่ายเงิน → ออก
   - OR Schedule: ห้องผ่าตัด, แพทย์, พยาบาล, เวลา
   - Discharge Flow: ใบสั่งจ่าย, นัดหมาย, ส่งต่อ
   - Claim Flow: ยื่นเบิก, ตรวจสอบ, อนุมัติ, โอนเงิน

3. **Department Twin**
   - Dashboard แต่ละแผนก: OPD, IPD, ER, Finance, HR, TB, NCD, PM2.5
   - KPIs: ตาม `kpi_dictionary.yaml`
   - Alerts: เมื่อ KPI เกิน threshold

4. **Organization Twin**
   - Org Chart แบบ interactive (ใช้ D3.js / Cytoscape.js)
   - แสดง workload แต่ละแผนก (heat map)
   - แสดง flow ของงาน/เอกสารระหว่างแผนก

5. **Ecosystem Twin**
   - แผนที่จังหวัด: 18 อำเภอ, 18 รพ., 20 โปรแกรม
   - แสดง KPI รวม, ความเสี่ยง, ทรัพยากร

#### Month 8: Forecast & Simulation Engine

**Deliverables:**
1. **Forecast Engine**
   - Disease Forecast: Prophet หรือ ARIMA บน historical data (Dengue, TB, PM2.5)
   - Budget Forecast: คาดการณ์การใช้จ่ายงบประมาณ
   - Workforce Forecast: คาดการณ์การขาดแคลนบุคลากร (retirement + training)
   - APIs: `/api/forecast/disease`, `/api/forecast/budget`, `/api/forecast/workforce`

2. **Simulation Engine**
   - What-if: "ถ้าย้ายบุคลากร 5 คนจากแผนก A ไป B จะเกิดอะไรขึ้น?"
   - Resource Optimizer: ใช้ `ortools` (Google OR-Tools) สำหรับ linear programming
   - APIs: `/api/simulate/scenario`, `/api/simulate/optimize`

#### Month 9: All Activity Command Center

**Deliverables:**
1. **6-Panel Dashboard** (ตาม `ai_agent_office_digital_twin_report.md`):
   - **Panel 1 — Agent Activity Monitor:** Progress bar แต่ละ agent, สถานะ real-time
   - **Panel 2 — Live Activity Feed:** Feed แบบ Twitter/X, filter ตาม agent/department
   - **Panel 3 — Department Activity Map:** Heat map ภาระงานแต่ละแผนก
   - **Panel 4 — Agent Command Center:** Pause/Restart/Emergency Stop/Assign Task
   - **Panel 5 — Organizational Digital Twin:** Graph viz แบบ interactive + animation
   - **Panel 6 — Performance Metrics:** Task Completion Rate, Avg Response Time, Agent Uptime, Cost Savings

2. **WebSocket Infrastructure**
   - Backend: `fastapi-websocket` + Redis Pub/Sub
   - Frontend: `socket.io-client` หรือ native WebSocket
   - Event types: `agent.status`, `task.progress`, `alert.new`, `kpi.update`

3. **Role-Based UI**
   - นพ.สสจ.: Executive Brief, KPI, Risk Radar, AI Recommendation
   - หัวหน้ากลุ่ม NCD: DM Coverage, HT Coverage, CKD, Forecast
   - CIO: Infrastructure, Cybersecurity, Data Quality, API Health, AI Health, Twin Health
   - หัวหน้ากลุ่มควบคุมโรค: Disease surveillance, Outbreak alert, Intervention status

**Success Criteria:**
- Dashboard แสดงข้อมูล real-time (latency < 500ms)
- สามารถ Pause/Restart Agent จาก UI ได้
- 300 concurrent users ใช้พร้อมกันได้ไม่ crash

---

### Phase 4: Scale & Intelligence (Month 9-12+)
**Goal:** ขยายระดับจังหวัด/เครือข่าย + ระบบเรียนรู้ต่อเนื่อง

#### Month 10-11: Provincial Health Brain

**Deliverables:**
1. **Federated Intelligence**
   - แต่ละโรงพยาบาลมี Local Brain ของตัวเอง
   - Query Federation: ผู้บริหารจังหวัดสามารถ query ข้อมูลรวมจากหลายโรงพยาบาล โดยไม่ต้อง centralize ข้อมูลทั้งหมด
   - ใช้ **Federated Learning** หรือ **Data Mesh** pattern

2. **Multi-Modal**
   - Voice: ถอดเสียงประชุม (Whisper API / Gemini multimodal), Voice command
   - Image: OCR เอกสารราชการ (ถ่ายรูป → สกัดข้อความ), วิเคราะห์รูปภาพสาธารณสุข
   - Video: วิเคราะห์ video surveillance (เช่น ความแออัดใน ER)

3. **GIS Advanced**
   - Heatmap โรคระดับตำบล/หมู่บ้าน
   - Disease Cluster Detection (SaTScan / R-INLA)
   - Service Gap Analysis (เขตไหนขาดบริการ)

#### Month 12+: Adaptive Learning & Cross-Agency

**Deliverables:**
1. **RLHF (Reinforcement Learning from Human Feedback)**
   - เก็บ feedback ทุก interaction (thumbs up/down, edit, correction)
   - ปรับ prompt / retrieval strategy / threshold อัตโนมัติ
   - A/B Testing: Prompt v1 vs v2, retrieval vector vs hybrid

2. **Cross-Agency Integration**
   - เชื่อม สธ. (MOPH HIE), สปสช. (NHSO), กรมควบคุมโรค (DDC)
   - สร้าง **National Health Brain** ระดับประเทศ
   - Policy alignment: ระบบรู้ว่านโยบายระดับชาติส่งผลกระทบต่อระดับจังหวัดอย่างไร

---

## 6. Immediate Action Items — Next 30 Days

### Week 1 (17-23 June 2026)

| # | Task | Owner | Deliverable | Priority |
|---|------|-------|-------------|----------|
| 1.1 | Create `docker-compose.yml` with PostgreSQL + pgvector + Redis + Backend + Frontend | DevOps | `docker-compose.yml` running | 🔴 Critical |
| 1.2 | Write SQLite → PostgreSQL migration script | Backend | Alembic migration + data migration script | 🔴 Critical |
| 1.3 | Add `pgvector` extension to `DocumentChunk` model + HNSW index | Backend | PR with schema change + vector search refactor | 🔴 Critical |
| 1.4 | Refactor `RetrievalAgent` to use `pgvector` cosine similarity query instead of in-memory scan | Backend | `RetrievalAgent.retrieve()` ใช้ SQL `ORDER BY embedding <=> query_embedding LIMIT 5` | 🔴 Critical |
| 1.5 | Create `AIGateway` abstraction class | Backend | `backend/app/services/ai_gateway.py` | 🔴 Critical |
| 1.6 | Add Circuit Breaker pattern to `GeminiService` | Backend | 3 failures → open 60s → fallback to next provider | 🔴 Critical |

### Week 2 (24-30 June 2026)

| # | Task | Owner | Deliverable | Priority |
|---|------|-------|-------------|----------|
| 2.1 | Implement Redis session store + cache | Backend | `redis-py` integration, `fastapi-cache` decorator | 🔴 Critical |
| 2.2 | Add rate limiting (Redis-based sliding window) | Backend | 100 requests/min per user, 1000 requests/min per agent | 🔴 Critical |
| 2.3 | Create `AgentPermission` model + middleware | Backend | `agent_permissions` table, check before every tool call | 🔴 Critical |
| 2.4 | Add immutable audit log table (separate schema or append-only) | Backend | `audit_logs` table with write-only policy | 🔴 Critical |
| 2.5 | Implement JWT refresh token pattern | Backend | Access token 15min, refresh token 7 days, `/auth/refresh` endpoint | 🔴 Critical |
| 2.6 | Add environment separation (dev/staging/prod) | DevOps | `env/` directory + `pydantic-settings` config | 🟡 High |

### Week 3 (1-7 July 2026)

| # | Task | Owner | Deliverable | Priority |
|---|------|-------|-------------|----------|
| 3.1 | Install LangGraph + create first State Graph | Backend | `ExecutiveBriefingGraph` ง่ายๆ | 🔴 Critical |
| 3.2 | Refactor `MasterOrchestrator` ใช้ LangGraph แทน prompt loop | Backend | `orchestrator_v2.py` | 🔴 Critical |
| 3.3 | Create `hitl_gateway.py` with pause/resume endpoints | Backend | `/api/hitl/interrupt`, `/api/hitl/resume` | 🔴 Critical |
| 3.4 | Add `agent_registry` table with versioning | Backend | `agent_registry` (name, version, owner, risk_tier, allowed_tools) | 🟡 High |
| 3.5 | Implement `task_handoff.schema.json` | Backend | JSON Schema สำหรับ agent-to-agent message | 🟡 High |
| 3.6 | Create `data_contracts/` directory with `kpi_dictionary.yaml` | Data | 10 KPI definitions แรก | 🟡 High |

### Week 4 (8-14 July 2026)

| # | Task | Owner | Deliverable | Priority |
|---|------|-------|-------------|----------|
| 4.1 | Install Neo4j (Docker) + create basic ontology | Backend | `docker-compose.yml` with neo4j, Cypher schema | 🟡 High |
| 4.2 | Create `GraphIngestionAgent` — write extracted entities to Neo4j | Backend | `graph_db_service.py` 不再 mock | 🟡 High |
| 4.3 | Add WebSocket endpoint to backend | Backend | `/ws/activity` ส่ง agent status real-time | 🟡 High |
| 4.4 | Implement frontend WebSocket client | Frontend | `useWebSocket` hook, `ActivityFeed` component | 🟡 High |
| 4.5 | Load testing (k6 / locust) | QA | Report: 100 concurrent users, 1000 docs, latency < 2s | 🟡 High |
| 4.6 | Create `AGENTS.md` + `SOP.md` + `GOVERNANCE.md` | Architect | Project governance docs | 🟡 High |

---

## 7. Technical Decision Records (TDR)

### TDR-001: Database — SQLite → PostgreSQL + pgvector
**Status:** APPROVED  
**Context:** SQLite ไม่รองรับ concurrency, ไม่มี vector index, ไม่รองรับ 300 users  
**Decision:** ย้ายไป PostgreSQL 15 + pgvector extension สำหรับ vector storage  
**Consequences:** ต้อง migrate ข้อมูล, ต้อง rewrite `RetrievalAgent`, ได้ ANN search, ได้ Read Replica

### TDR-002: Vector Store — pgvector vs Qdrant vs Milvus
**Status:** PENDING  
**Context:** ต้องเลือก vector database สำหรับ scale  
**Decision:** เริ่มด้วย pgvector (อยู่ใน PostgreSQL แล้ว, ไม่ต้อง maintain อีกระบบ)  
**Migration trigger:** ถึง 100,000 chunks (ประมาณ 5,000 เอกสาร) จะย้ายไป Qdrant หรือ Milvus  
**Consequences:** ลด complexity ตอนเริ่ม แต่ pgvector อาจช้ากว่า dedicated vector DB ที่ scale สูง

### TDR-003: AI Gateway — Multi-Provider vs Single Provider
**Status:** APPROVED  
**Context:** ผูกติด Gemini มี risk (quota, downtime, policy change)  
**Decision:** สร้าง AIGateway abstraction รองรับ Gemini, OpenAI, Anthropic, Local (vLLM)  
**Routing logic:** simple→gemini-flash, complex→claude-opus, sensitive→local-vllm  
**Consequences:** เพิ่ม complexity แต่ลด risk, ได้ failover, ได้ cost optimization

### TDR-004: Orchestrator — LangGraph vs Custom State Machine
**Status:** APPROVED  
**Context:** ต้องมี stateful workflow, checkpoint, HITL  
**Decision:** ใช้ LangGraph (เพราะมี ecosystem รองรับ, checkpoint, visualization, LangSmith observability)  
**Alternative:** Temporal (งาน background ยาว) อาจใช้เสริมภายหลัง  
**Consequences:** ต้องเรียนรู้ LangGraph API, แต่ได้ community support, ได้ HITL first-class

### TDR-005: Auth — Keycloak vs Custom vs ThaiD Direct
**Status:** APPROVED  
**Context:** ต้องเชื่อม ThaiD, LDAP, AD, SSO  
**Decision:** ใช้ Keycloak เป็น Identity Broker (รองรับ ThaiD, LDAP, AD, SAML, OAuth2.1)  
**Consequences:** ต้อง deploy Keycloak (Docker/K8s), แต่ได้ feature ครบ (MFA, session management, RBAC)

### TDR-006: Knowledge Graph — Neo4j vs Amazon Neptune vs RDF
**Status:** PENDING  
**Context:** ต้องเลือก graph database  
**Decision:** เริ่มด้วย Neo4j Community Edition (หรือ AuraDB ถ้า cloud)  
**Reason:** Cypher ง่าย, ecosystem ใหญ่, มี Python driver ดี, มี Graph Data Science library  
**Migration trigger:** ถ้า deploy บน AWS อย่างเดียว อาจพิจารณา Neptune ภายหลัง  
**Consequences:** Neo4j มี license แตกต่าง (Community vs Enterprise), ต้องวางแผน backup

### TDR-007: FHIR — HAPI FHIR Server vs Custom Adapter
**Status:** PENDING  
**Context:** ต้องเชื่อม HIS/EMR ผ่าน FHIR  
**Decision:** เริ่มด้วย Custom FHIR Adapter (Python `fhir.resources` + `requests`) สำหรับ HIS ที่มี FHIR API อยู่แล้ว  
**ถ้า HIS ไม่มี FHIR:** สร้าง HAPI FHIR Server เป็น translation layer แปลง HL7 v2 / custom API → FHIR  
**Consequences:** ลด infrastructure ตอนเริ่ม แต่ถ้า HIS หลายตัว อาจต้องมี HAPI FHIR Server จริง

---

## 8. Risk Assessment & Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| **Gemini API quota exceeded / rate limited** | High | High | AIGateway multi-provider, circuit breaker, local model fallback |
| **SQLite corruption under concurrent load** | High | Critical | Migrate to PostgreSQL ทันที (Week 1) |
| **Data migration failure** | Medium | Critical | สร้าง migration script + backup + rollback plan + test บน staging |
| **LangGraph learning curve** | Medium | Medium | ส่งทีมไปอบรม / ทำ PoC 1-2 weeks ก่อน refactor จริง |
| **HIS integration complexity** | High | High | เริ่มจาก HIS ที่มี API ดีที่สุด 1 ตัว, ใช้ API Wrapper pattern |
| **PDPA compliance gap** | Medium | High | ปรึกษา legal team, สร้าง data classification + consent flow ตั้งแต่ Phase 1 |
| **ThaiD integration delay** | Medium | High | มี fallback basic auth ที่ secure รอไว้, ThaiD ใช้ Keycloak broker |
| **Frontend performance at 300 users** | Medium | High | WebSocket connection pooling, Redis pub/sub, lazy loading, code splitting |
| **Team bandwidth** | High | Medium | จ้าง contractor สำหรับ DevOps/Security, ใช้ managed services ให้มากที่สุด |
| **Model hallucination in production** | Medium | High | Strict grounding prompt, citation required, confidence threshold, HITL for critical decisions |

---

## 9. Resource Requirements

### 9.1 Infrastructure (Production Estimate for 300 users)

| Component | Spec | Qty | Monthly Cost (Cloud) |
|-----------|------|-----|-------------------|
| App Server | 8 vCPU, 32GB RAM | 4-6 | ~$800-1200 |
| PostgreSQL Primary | 16 vCPU, 64GB RAM | 1 | ~$400-600 |
| PostgreSQL Read Replica | 8 vCPU, 32GB RAM | 1 | ~$200-400 |
| Redis Cluster | 4 vCPU, 16GB RAM | 3 | ~$300-500 |
| Neo4j | 8 vCPU, 32GB RAM | 1 | ~$300-500 (or AuraDB) |
| Kafka / Redpanda | 4 vCPU, 16GB RAM | 3 | ~$400-600 |
| Load Balancer | - | 2 | ~$100-200 |
| Object Storage (MinIO/S3) | 5-10TB | 1 | ~$100-300 |
| AI API Costs | - | - | ~$1500-3000 |
| **Total** | | | **~$4000-7000/month** |

### 9.2 Team Composition

| Role | FTE | Phase |
|------|-----|-------|
| Backend AI Engineer (Python/FastAPI/LangGraph) | 2 | All |
| Frontend Engineer (React/TypeScript/WebSocket) | 1-2 | All |
| Data Engineer (Airflow/dbt/PostgreSQL) | 1 | Phase 2+ |
| DevOps / Platform Engineer | 1 | Phase 1+ |
| Security / Compliance Engineer (part-time) | 0.5 | Phase 1+ |
| QA / Test Engineer | 1 | Phase 2+ |
| Product Owner / AI Architect | 1 | All |
| Domain Expert (Public Health) | 0.5 | Phase 2+ |

### 9.3 Development Tools & Licenses

| Tool | Purpose | Cost |
|------|---------|------|
| LangSmith | LLM tracing & observability | ~$39-399/mo |
| MLflow / PromptLayer | Prompt versioning & eval | Open source / ~$50/mo |
| DataHub | Data catalog | Open source |
| Neo4j Enterprise | Graph database (optional) | License-based |
| Keycloak | Identity broker | Open source |
| HAPI FHIR | FHIR server (optional) | Open source |
| GitHub Actions / GitLab CI | CI/CD | Free tier / ~$50/mo |
| Sentry / Datadog | Error tracking / APM | ~$50-200/mo |

---

## 10. Definition of Done (DoD) per Phase

### Phase 1 DoD
- [ ] `docker-compose up` รันได้ครบทุก service
- [ ] PostgreSQL + pgvector มีข้อมูลจาก migration สมบูรณ์
- [ ] Load test: 100 users, 1000 docs, latency < 2s
- [ ] AIGateway สลับ provider ได้
- [ ] Refresh token pattern ทำงาน
- [ ] Audit log แก้ไขไม่ได้
- [ ] Code review ผ่าน + Unit tests > 70% coverage

### Phase 2 DoD
- [ ] LangGraph workflow รัน end-to-end ได้ (Executive Briefing)
- [ ] HITL pause/resume ทำงาน
- [ ] Neo4j มี nodes > 1000, relationships > 5000
- [ ] Graph RAG ตอบคำถาม multi-hop ได้
- [ ] Airflow DAGs รัน daily ไม่มี error
- [ ] dbt docs + lineage แสดงได้
- [ ] KPI Dictionary มี 50+ definitions
- [ ] FHIR Gateway ดึงข้อมูลจาก HIS mock ได้

### Phase 3 DoD
- [ ] Digital Twin 5 layers มีข้อมูลจริงจาก HIS/HR
- [ ] Forecast engine ทำนาย Dengue/TB/PM2.5 ได้
- [ ] Simulation engine รัน what-if scenario ได้
- [ ] All Activity Dashboard 6 panels แสดง real-time
- [ ] WebSocket รองรับ 300 concurrent connections
- [ ] Role-based UI แยกตามระดับผู้ใช้
- [ ] ThaiD/SSO login ทำงาน
- [ ] Penetration test ผ่าน (no critical vulnerabilities)

### Phase 4 DoD
- [ ] Provincial Health Brain รวมข้อมูล 18 อำเภอ
- [ ] Federated query รวมจากหลายโรงพยาบาลได้
- [ ] RLHF: system ปรับ prompt จาก feedback ได้
- [ ] Multi-modal: voice, image, video ใช้งานได้
- [ ] Cross-agency: เชื่อม MOPH / NHSO / DDC ได้
- [ ] 99.9% uptime (SRE monitoring)
- [ ] Disaster recovery plan tested (RTO < 4h, RPO < 1h)

---

## 11. Appendix A: API Contract Changes (Phase 1)

### New Endpoints

```
POST   /api/v2/auth/refresh              # Refresh token
POST   /api/v2/hitl/interrupt            # Pause workflow for human review
POST   /api/v2/hitl/resume               # Resume workflow after approval
GET    /api/v2/agents/registry           # Agent registry with capabilities
POST   /api/v2/agents/handoff            # Agent-to-agent task handoff
GET    /api/v2/audit/logs                # Immutable audit trail (read-only)
WS     /ws/v2/activity                   # WebSocket for real-time updates
```

### Modified Endpoints

```
GET    /api/oracle/ask                   # Add: citation provenance, confidence score, source pipeline
POST   /api/documents/upload             # Add: data classification, retention policy, PDPA consent check
GET    /api/twins/agents                 # Add: agent health status, version, allowed tools
POST   /api/workflows/trigger            # Change: accept LangGraph workflow name, not just static workflow
```

---

## 12. Appendix B: Database Schema Changes (Phase 1)

### New Tables

```sql
-- Agent Registry
CREATE TABLE agent_registry (
    id SERIAL PRIMARY KEY,
    agent_id VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    version VARCHAR(50) NOT NULL,
    owner VARCHAR(100) NOT NULL,
    risk_tier VARCHAR(50) NOT NULL, -- low, medium, high, critical
    allowed_tools JSONB NOT NULL DEFAULT '[]',
    forbidden_actions JSONB NOT NULL DEFAULT '[]',
    model_provider VARCHAR(50),
    model_name VARCHAR(100),
    approval_level VARCHAR(50), -- none, manager, executive, council
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Agent Permissions
CREATE TABLE agent_permissions (
    id SERIAL PRIMARY KEY,
    agent_id VARCHAR(100) REFERENCES agent_registry(agent_id),
    tool_name VARCHAR(100) NOT NULL,
    action VARCHAR(50) NOT NULL, -- read, write, execute
    allowed BOOLEAN NOT NULL DEFAULT FALSE,
    conditions JSONB -- e.g., {"read_only": true, "max_rows": 1000}
);

-- Audit Logs (Immutable, append-only, separate schema or partition)
CREATE TABLE audit_logs (
    id BIGSERIAL PRIMARY KEY,
    timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
    agent_id VARCHAR(100),
    workflow_id VARCHAR(100),
    user_id VARCHAR(100),
    action_type VARCHAR(100) NOT NULL,
    input_data JSONB,
    output_data JSONB,
    tools_used JSONB,
    decisions JSONB,
    approval_token VARCHAR(100),
    ip_address INET,
    user_agent TEXT,
    -- Ensure append-only via trigger or RLS policy
    CONSTRAINT no_update_audit CHECK (false) NO INHERIT
);

-- Cost Tracking
CREATE TABLE cost_logs (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT NOW(),
    agent_id VARCHAR(100),
    provider VARCHAR(50),
    model VARCHAR(100),
    input_tokens INT,
    output_tokens INT,
    cost_usd DECIMAL(10,6),
    request_id VARCHAR(100)
);

-- HITL Queue
CREATE TABLE hitl_queue (
    id SERIAL PRIMARY KEY,
    workflow_id VARCHAR(100) NOT NULL,
    task_id VARCHAR(100) NOT NULL,
    agent_id VARCHAR(100),
    status VARCHAR(50) NOT NULL DEFAULT 'pending', -- pending, approved, rejected, expired
    requested_at TIMESTAMP DEFAULT NOW(),
    approved_at TIMESTAMP,
    approved_by VARCHAR(100),
    approval_token VARCHAR(100),
    payload JSONB,
    context JSONB
);
```

### Modified Tables

```sql
-- DocumentChunk: add vector column (pgvector)
ALTER TABLE document_chunks ADD COLUMN embedding vector(3072);
CREATE INDEX idx_document_chunks_embedding ON document_chunks USING hnsw (embedding vector_cosine_ops);

-- Documents: add data classification and PDPA fields
ALTER TABLE documents ADD COLUMN data_classification VARCHAR(50) DEFAULT 'Internal'; -- Public, Internal, Confidential, Restricted
ALTER TABLE documents ADD COLUMN retention_years INT DEFAULT 7;
ALTER TABLE documents ADD COLUMN pdpa_consent BOOLEAN DEFAULT FALSE;
ALTER TABLE documents ADD COLUMN encryption_at_rest BOOLEAN DEFAULT FALSE;

-- Users: add SSO fields
ALTER TABLE users ADD COLUMN sso_provider VARCHAR(50); -- thaid, ldap, keycloak
ALTER TABLE users ADD COLUMN sso_subject VARCHAR(255);
ALTER TABLE users ADD COLUMN mfa_enabled BOOLEAN DEFAULT FALSE;
ALTER TABLE users ADD COLUMN last_login TIMESTAMP;
```

---

## 13. Appendix C: Technology Stack Summary

| Layer | Current | Phase 1 | Phase 2 | Phase 3 |
|-------|---------|---------|---------|---------|
| **Frontend** | React 18 + Vite + Tailwind | + WebSocket + PWA + Lazy Loading | + Role-Based Dashboard | + Multi-modal (Voice, Image) |
| **Backend** | FastAPI + SQLite | FastAPI + PostgreSQL + Redis + Docker | + LangGraph + A2A + MCP | + K8s + Microservices |
| **AI Runtime** | Gemini 2.5 Flash | AIGateway (Multi-provider) | + Local Models (vLLM) | + Model Serving (KServe) |
| **Vector DB** | SQLite JSON | pgvector | pgvector + HNSW | Qdrant/Milvus (if scale) |
| **Graph DB** | Mock (log only) | Neo4j Community | Neo4j + GDS | Neo4j Enterprise (if needed) |
| **Orchestrator** | Prompt loop | LangGraph PoC | LangGraph Production | Temporal (background jobs) |
| **Data Platform** | None | PostgreSQL + Airflow (basic) | Bronze-Silver-Gold + dbt | + DataHub + OpenLineage |
| **Message Queue** | None | Redis Pub/Sub | Kafka / Redpanda | Kafka Cluster |
| **Auth** | Basic JWT | Keycloak + ThaiD/LDAP | RBAC + ABAC | MFA + Biometric |
| **Observability** | Python logging | + Sentry + Prometheus | + OpenTelemetry + LangSmith | + Datadog / Grafana |
| **CI/CD** | None | GitHub Actions + Docker | + K8s manifests | + ArgoCD |

---

## 14. Sign-off

| Role | Name | Signature | Date |
|------|------|-----------|------|
| AI Architect / Backend Lead | | | |
| Senior Developer | | | |
| Product Owner | | | |
| Security Lead | | | |
| DevOps Lead | | | |

---

**Next Review Date:** 2026-07-16  
**Document Owner:** AI Agentic Architect  
**Distribution:** Senior Developer Team, Product Owner, DevOps Lead, Security Lead

---
*End of Progression Note*
