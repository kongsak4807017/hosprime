# HosPrime Master Implementation Plan

## Objective

Deliver a secure and measurable Governed Knowledge Oracle MVP within 90 days. Later-milestone modules remain experimental until their own gates pass.

## Ninety-day outcome

- secure authenticated platform;
- five governed knowledge packs;
- at least 100 approved documents;
- traceable retrieval and citations;
- calibrated no-answer behavior;
- automated quality and security checks;
- pilot users and benefit evidence;
- audit and cost reporting;
- release and rollback process;
- approved recommendation for Milestone 2.

## Workstreams

1. Product and user value
2. Knowledge and data governance
3. RAG and AI quality
4. Security and privacy
5. Platform and operations
6. Project governance and evidence

## Week 0 — Containment and baseline

### Work

- rotate the exposed provider credential;
- review provider usage and billing;
- clean current source files;
- enable secret scanning;
- classify modules by maturity;
- establish risk register and project controls;
- freeze unsupported production claims;
- capture baseline build and quality status.

### Exit

- no active credential in current files;
- P0 risks have accountable owners;
- current release scope is limited to M1.

## Sprint 1, Weeks 1–2 — Secure engineering foundation

### Build

- backend and frontend CI;
- protected-route tests;
- production configuration guard;
- health and readiness checks;
- safe file upload controls;
- structured audit IDs;
- dependency and secret scanning;
- initial migration framework;
- feature flags for experimental modules.

### Governance

- approve role matrix;
- approve classification levels;
- approve logging and retention policy;
- identify pilot users and organization.

### Exit

- no unresolved P0;
- CI passes;
- protected routes tested;
- Global Gate 0 evidence substantially complete.

## Sprint 2, Weeks 3–4 — Governed ingestion

### Build

- document identity and version;
- owner, department, program and classification;
- effective and review dates;
- parser quality result;
- ingestion state and retry;
- duplicate detection;
- quarantine and rejection;
- page and section anchors;
- storage abstraction.

### Knowledge packs

- PM2.5
- TB
- NCD
- Disaster
- Digital Health

For every source, assign owner, version, classification, effective date and review date.

### Exit

- at least 100 approved documents;
- metadata completeness at least 95 percent;
- parsing success at least 95 percent;
- access tests pass.

## Sprint 3, Weeks 5–6 — Retrieval and citation

### Build

- PostgreSQL and pgvector integration;
- hybrid lexical and vector retrieval;
- metadata and access filters;
- reranker interface;
- duplicate chunk suppression;
- source preview;
- retrieval debug view.

### Evaluate

- versioned gold question set;
- Recall@5 and Recall@10;
- Mean Reciprocal Rank;
- Precision@5;
- latency and access correctness;
- failure analysis by parser, chunking, metadata and retrieval.

### Exit

- Recall@5 at least 0.85;
- MRR at least 0.70;
- zero access-boundary violation;
- p95 retrieval latency below 2 seconds.

## Sprint 4, Weeks 7–8 — Trusted answer layer

### Build

- structured answer contract;
- fact, analysis, recommendation and uncertainty separation;
- claim-to-source mapping;
- conflicting-source disclosure;
- no-answer policy;
- freshness warning;
- model, prompt and evidence version logging;
- reviewer correction workflow.

### Evaluate

- answerable and unanswerable questions;
- ambiguous and conflicting-source questions;
- groundedness;
- citation precision and completeness;
- fabricated-source detection;
- prompt-injection resistance;
- cost and latency.

### Exit

- groundedness at least 0.90;
- citation precision at least 0.90;
- false answer rate below 2 percent;
- fabricated source rate zero;
- correct no-answer behavior at least 98 percent.

## Sprint 5, Weeks 9–10 — Pilot experience

### Build

- role-specific landing page;
- Ask Oracle workflow;
- evidence preview;
- feedback and correction;
- knowledge steward queue;
- quality and cost dashboard;
- onboarding and help.

### Prepare pilot

- enroll 15–25 users;
- select 20–30 real tasks;
- measure the current baseline;
- train users on evidence and limitations;
- establish support and incident channels.

### Exit

- UAT scenarios approved;
- task analytics active;
- privacy and security review complete;
- pilot support ready.

## Sprint 6, Weeks 11–12 — Controlled pilot

### Operate

- review failures daily;
- review quality and cost weekly;
- collect task acceptance and time saved;
- conduct security testing;
- rehearse rollback;
- close or accept residual P1 risks.

### Deliverables

- M1 evaluation report;
- adoption report;
- benefit report;
- security and privacy report;
- cost and capacity model;
- production architecture proposal;
- investment case;
- M2 entry recommendation.

### Exit

- target task completion at least 80 percent;
- usefulness and trust at least 4 of 5;
- median time reduction at least 30 percent;
- no P0 incident;
- executive go, hold or stop decision.

## Later milestones

### M2 — Organization Memory

Build Meeting, Decision, Rationale, Alternative, Action, Outcome and Lesson Learned with review and traceability.

### M3 — Executive Office and Role Twin

Build the five Core Office roles, capability registry, role context, Person and Role Memory separation, Executive Brief and governed AI Council.

### M4 — Backoffice AI Workforce

Build DataOps, KnowledgeOps, GovernanceOps, AgentOps and AIOC with monitored, reversible and governed work.

### M5 — Forecast and Scenario

Build governed models, scenario assumptions, uncertainty, drift monitoring, strategic analysis and learning from actual outcomes.

## Minimum accountable roles

- Executive Sponsor
- Product Owner
- Delivery Lead
- Technical Lead
- Backend Engineer
- Frontend Engineer
- AI and RAG Engineer
- Data or Knowledge Steward
- Security and Privacy Reviewer
- QA and Evaluation Lead
- Domain reviewers

One person may hold more than one role, but accountability must remain explicit.

## Weekly control dashboard

Track:

- maturity gate completion;
- sprint goal confidence;
- open P0 and P1 risks;
- build and test status;
- document coverage;
- retrieval and answer metrics;
- pilot adoption;
- cost;
- decisions required.

## Scope protection

During the first 90 days, do not expand agent count or external automation unless required to pass M1. Prioritize a trustworthy end-to-end evidence path over feature breadth.
