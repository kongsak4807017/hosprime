# HosPrime Current-State Reassessment

**Assessment date:** 2026-07-02  
**Baseline:** latest `main` after repository restructuring  
**Assessment branch:** `governance-project-control-v1`

## 1. Executive conclusion

The repository has advanced significantly. It now contains prototypes for all five strategic milestones, including Knowledge Oracle, Meeting Memory, Twin models, Graph integration, workflow planning, HITL, agent registry, audit and cost logging.

The primary problem is no longer missing screens or missing classes. The primary problem is **maturity ambiguity**:

- prototype code is mixed with production claims;
- later-milestone modules are exposed before Milestone 1 is validated;
- several fallback paths can create misleading confidence;
- security and access boundaries are inconsistent;
- success criteria and release evidence were not encoded into the repository.

The correct strategy is to preserve the useful code, classify every component by maturity, and release only through measurable gates.

## 2. Current capability inventory

| Capability | Current evidence | Maturity 0–5 | Assessment |
|---|---|---:|---|
| Document ingestion | PDF, DOCX, TXT and MD parser pipeline | 2.5 | Functional prototype; requires malware scanning, async jobs and access policy |
| Metadata extraction | LLM classification and entity extraction | 2.0 | Exists; requires schema validation and human review |
| Embeddings and retrieval | Gemini embeddings, pgvector path and SQLite fallback | 2.5 | Technical path exists; needs evaluation and calibrated thresholds |
| Answer generation | Grounded prompt and citation response | 2.0 | Structure exists; claim-to-source alignment not yet proven |
| Knowledge governance | Pending review and admin review screens | 1.5 | Roles and audit coverage incomplete |
| Meeting Memory | Audio/document ingestion and meeting Q&A | 1.5 | Model is too thin; Decision, Outcome and Lesson Learned are missing |
| Twin Runtime | Organization, Role, Person, Knowledge and specialist classes | 1.0 | Data models exist; runtime context, memory policy and succession are absent |
| Graph Intelligence | SQLite relations and Neo4j service | 1.5 | Integration exists; ontology and provenance controls are incomplete |
| Workflow planning | AI-generated workflow steps | 1.5 | Planning exists; real executor is not implemented |
| HITL | Queue, approve and reject records | 2.0 | Exists; identity binding and execution semantics required hardening |
| Agent governance | Registry, permissions and token balances | 1.5 | Duplicate agent representations and weak lifecycle governance |
| Security | JWT, roles and CORS | 1.0 | Inconsistent endpoint protection and insecure defaults were present |
| Observability | Agent logs and cost logs | 1.5 | No metrics service, traces, SLOs or alerting |
| Delivery engineering | Vite and FastAPI runnable structure | 1.5 | CI, automated tests, migrations and release gates are missing |
| User experience | Integrated navigation across five milestones | 2.0 | Strong demo breadth; insufficient role-based product focus |

## 3. Strengths to preserve

1. **Knowledge-first foundation** — the code includes document chunks, embeddings, query logs and citations.
2. **Local-first development** — SQLite enables rapid testing while PostgreSQL and pgvector are anticipated.
3. **AI Gateway concept** — centralized model, budget and cost control is the correct architectural direction.
4. **HITL intent** — high-impact work is designed to pass through human review.
5. **Graph readiness** — entity relationships and Neo4j integration provide a path toward Organization and Decision Graphs.
6. **Integrated product shell** — frontend navigation makes end-to-end demonstrations possible.
7. **Audit and cost entities** — the data model anticipates governance instead of treating it as an afterthought.

## 4. Critical findings

### P0 — Credential exposure

A real-looking provider credential was committed in source and README history. Current files must be cleaned, but the credential must also be revoked or rotated because Git history remains accessible.

### P0 — Fabricated fallback evidence

The previous offline fallback returned detailed public-health claims, metrics and citations even when the provider was unavailable. This directly violated the rule `No Evidence -> No Answer`.

### P0 — Unauthenticated or weakly protected operations

Several document, administrative, workflow and HITL routes previously lacked consistent authentication or accepted approver identity from query parameters.

### P0 — False execution semantics

The workflow layer previously used a mock Temporal identifier and could label AI-proposed steps as completed. The current repository does not contain an external action executor or Temporal worker.

### P1 — Milestone scope collapse

Milestones 1–5 are exposed simultaneously, but none has a repository-enforced exit gate. This creates a false sense of completion and makes debugging, governance and investment reporting difficult.

### P1 — RAG confidence is not calibrated

Average vector similarity is recorded as confidence. It is not yet a validated probability of correctness. The threshold must be calibrated using a controlled evaluation set.

### P1 — Citations are context references, not proven claim citations

The current Citation Agent returns all selected chunks. It does not verify that every material claim in the final answer is entailed by a cited chunk.

### P1 — Organization Memory model is incomplete

Meeting and Action Item exist, but canonical Decision, Decision Rationale, Alternative, Outcome, Lesson Learned and Evidence links are missing.

### P1 — Twin models are structural, not operational

Current Twin classes represent records. A working Twin Runtime still requires:

- effective role and authority;
- scoped knowledge and memory;
- role history;
- person versus role memory separation;
- permitted tools;
- learning and memory-promotion workflow;
- version and retirement policy.

### P1 — Agent model duplication

`Agent`, `AgentRegistry`, specialist Twin subclasses and code-level agent classes overlap. A single canonical agent specification and lifecycle must replace duplicated identities.

### P2 — Production data architecture

SQLite and `create_all` are suitable for a prototype but not controlled production deployment. Alembic migrations, PostgreSQL, backup, recovery and tenant boundaries are required.

### P2 — Operational visibility

AgentLog and CostLog exist, but SLOs, traces, failure alerts, queue health, evidence coverage and model drift metrics are not yet exposed.

## 5. Changes applied in the governance branch

- Removed embedded provider credentials from current files.
- Replaced insecure JWT defaults with environment-controlled configuration.
- Added production configuration checks and health endpoints.
- Disabled fabricated factual fallbacks and fake citations.
- Disabled pseudo-embeddings by default.
- Prevented the AI Gateway from labeling Gemini output as another provider.
- Changed budget-control failures to fail closed in production.
- Added router-level authentication and role boundaries.
- Hardened document upload filename and size handling.
- Converted workflow behavior to plan-only semantics.
- Bound HITL decisions to authenticated user identities.
- Changed workflow approval to `APPROVED_NOT_EXECUTED`.

## 6. Target bounded contexts

The repository should converge toward these bounded contexts:

1. Identity and Access
2. Organization and Role
3. Knowledge and Evidence
4. Organization Memory
5. Twin Runtime
6. Agent and Capability Registry
7. Workflow Planning and Execution
8. HITL and Decision Authority
9. Data Governance
10. Forecast and Scenario
11. Audit, Cost and Observability
12. User Experience

Each bounded context owns its data, rules, APIs, events and acceptance tests.

## 7. Immediate architectural decisions

1. Milestone 1 remains the only release candidate until all M1 gates pass.
2. Later-milestone modules remain feature-flagged prototypes.
3. AI may propose workflow steps but cannot mark them completed.
4. Approved plans are not equivalent to executed actions.
5. Retrieval confidence and answer confidence are separate metrics.
6. Every sensitive object must carry organization, owner, classification and retention metadata.
7. Every material answer must be traceable to approved evidence.
8. Every release must produce an evidence pack, not only a demo.

## 8. Recommended next build slice

The next vertical slice should prove one complete, governed path:

```text
Approved document
  -> secure ingestion
  -> metadata review
  -> embedding and retrieval
  -> grounded answer
  -> claim-level citations
  -> user feedback
  -> evaluation score
  -> audit and cost record
```

Use five controlled knowledge packs: PM2.5, TB, NCD, Disaster and Digital Health. Do not expand the number of agents until this slice passes the M1 acceptance gates.
