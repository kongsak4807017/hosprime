# HosPrime Test and Validation Strategy

## 1. Objective

HosPrime must prove correctness, safety, usefulness and operability. A passing software build is necessary but insufficient because AI behavior depends on data, retrieval, model output, policy and human workflow.

Testing is divided into six evidence layers:

1. code correctness;
2. integration correctness;
3. data and knowledge quality;
4. AI and RAG quality;
5. security, privacy and governance;
6. user and operational acceptance.

## 2. Test environments

### Local development

- SQLite permitted;
- synthetic or approved non-sensitive data only;
- demo flags allowed only when explicitly enabled;
- no production credential or data.

### Continuous integration

- clean dependency installation;
- isolated temporary database;
- no external AI call required for deterministic tests;
- frontend production build;
- static and security checks.

### Integration

- PostgreSQL and pgvector;
- object storage equivalent to production;
- Neo4j where graph use is tested;
- test identity provider;
- approved model sandbox;
- representative but de-identified documents.

### Pilot / pre-production

- production-like topology;
- strict access control;
- production monitoring and backup;
- controlled pilot users;
- no autonomous high-impact execution.

## 3. Test pyramid

### Unit tests

Cover:

- configuration validation;
- authentication and role checks;
- metadata validators;
- safe filename and file-size controls;
- chunking boundaries;
- embedding dimension checks;
- similarity and ranking functions;
- source filtering;
- confidence calculation;
- workflow state transitions;
- HITL identity binding;
- audit-event serialization;
- cost calculation and attribution.

Target: at least 80 percent coverage of critical domain and security code. Coverage percentage alone does not override missing risk-based tests.

### Component tests

Cover each bounded context with real persistence:

- document ingestion;
- Oracle query;
- admin review;
- meeting memory;
- Twin context;
- graph operations;
- workflow planning;
- HITL approval;
- audit and cost records.

### Contract tests

Verify:

- request and response schemas;
- error status and message contracts;
- role and access behavior;
- event and audit payloads;
- frontend API assumptions;
- backward compatibility for published endpoints.

### End-to-end tests

Required flows:

1. login -> upload -> review -> approve -> query -> citation -> feedback;
2. restricted document -> unauthorized user denied;
3. meeting upload -> transcript -> decision review -> action tracking;
4. workflow plan -> HITL queue -> approval -> approved-not-executed state;
5. provider unavailable -> explicit failure with no fabricated answer;
6. expired source -> excluded or visibly warned;
7. account or role change -> access updated immediately.

## 4. Knowledge and data test pack

Milestone 1 uses five controlled knowledge packs:

- PM2.5;
- TB;
- NCD;
- Disaster;
- Digital Health.

Each pack must contain:

- current authoritative sources;
- superseded source examples;
- conflicting statements;
- tables and page-specific facts;
- Thai terminology and abbreviations;
- sensitive and non-sensitive examples;
- documents with poor formatting;
- known unanswerable questions.

Every source receives a stable source ID, owner, version, effective date, classification and review date.

## 5. RAG evaluation dataset

Minimum M1 set:

- 100 answerable questions;
- 30 unanswerable questions;
- 20 ambiguous questions;
- 20 conflicting-source questions;
- 20 access-control questions;
- 20 adversarial or prompt-injection questions.

Each test item contains:

- question;
- expected relevant source IDs;
- expected answer facts;
- prohibited claims;
- expected no-answer behavior;
- authorized roles;
- reviewer and approval date.

The test set is versioned and separated from prompt development examples to reduce overfitting.

## 6. Retrieval evaluation

Measure:

- Recall@1, @5 and @10;
- Precision@5;
- Mean Reciprocal Rank;
- normalized discounted cumulative gain where multiple sources are relevant;
- access-filter correctness;
- retrieval latency;
- stale-source and duplicate-source behavior.

Failure analysis categories:

- parser failure;
- chunking failure;
- embedding mismatch;
- vocabulary or abbreviation mismatch;
- metadata filter error;
- obsolete source;
- wrong access filter;
- missing document;
- reranker failure.

## 7. Answer evaluation

Every material claim is evaluated against cited evidence.

### Required metrics

- groundedness;
- factual correctness;
- citation precision;
- citation completeness;
- source-title and page correctness;
- uncertainty quality;
- conflict disclosure;
- no-answer correctness;
- harmful overstatement;
- usefulness and clarity.

### Reviewer scale

- 0: unsafe or materially false;
- 1: major correction required;
- 2: partially useful with material gaps;
- 3: acceptable with minor edits;
- 4: fully acceptable and traceable.

M1 release target: at least 85 percent of evaluated answers score 3 or 4, with zero fabricated source identifier.

## 8. Confidence validation

Do not equate embedding similarity with answer confidence.

Confidence should be derived from separate signals:

- retrieval strength;
- source agreement;
- evidence coverage;
- source authority and freshness;
- claim verification;
- model uncertainty;
- reviewer history.

Calibration evaluation compares predicted confidence bands with actual reviewer acceptance. Until calibrated, display component signals rather than a single percentage.

## 9. Security testing

Required before pilot:

- secret scanning;
- dependency vulnerability scan;
- static analysis;
- authentication bypass tests;
- role escalation tests;
- IDOR tests;
- file upload abuse and path traversal tests;
- oversized and malformed document tests;
- prompt-injection tests;
- cross-document data exfiltration tests;
- cross-tenant access tests;
- audit tampering tests;
- rate-limit and denial-of-service tests;
- CORS and token expiry tests.

No unresolved P0 is permitted.

## 10. Privacy validation

Verify:

- minimum necessary data;
- purpose and lawful basis;
- classification and retention;
- sensitive log redaction;
- deletion and correction workflow;
- consent where required;
- access review;
- export and incident traceability;
- person-memory versus role-memory separation.

## 11. Agent and workflow testing

Each agent requires:

- identity and version test;
- allowed capability test;
- denied-tool test;
- authority-level test;
- citation requirement test;
- low-confidence escalation test;
- budget exhaustion test;
- provider failure test;
- prompt-injection resistance;
- rollback test.

Workflow tests must prove:

- LLM-proposed steps remain `planned`;
- approval identity comes from authentication;
- approval does not imply execution;
- no action is marked complete without tool receipt;
- duplicate approval is rejected;
- rejected plans cannot execute;
- audit records contain user, workflow, decision and time.

## 12. Performance and reliability

Pilot workload profiles must include:

- concurrent queries;
- large document ingestion;
- graph query;
- long meeting transcript;
- provider latency and outage;
- database degradation;
- object storage failure.

Measure p50, p95 and p99 latency, throughput, error rate, resource use and recovery time.

## 13. User acceptance testing

User groups:

- executives;
- program managers;
- knowledge stewards;
- data and IT administrators;
- governance reviewers.

UAT uses real tasks, not feature tours. Each scenario records:

- task objective;
- baseline method and time;
- completion success;
- output acceptance;
- evidence quality;
- time and effort;
- user confidence;
- defect or improvement request.

## 14. Release evidence pack

A release candidate must provide:

- commit and build IDs;
- dependency inventory;
- test summary;
- RAG evaluation report;
- security and privacy report;
- open defects and residual risks;
- performance report;
- user acceptance sign-off;
- database migration plan;
- deployment and rollback plan;
- monitoring dashboard links;
- release decision.

## 15. Defect severity

### P0

Credential exposure, unauthorized sensitive access, fabricated evidence used for decision, unauthorized action, data corruption or unrecoverable outage.

### P1

Milestone-blocking correctness, access, reliability or trust failure.

### P2

Material defect with a viable workaround.

### P3

Minor usability or cosmetic defect.

## 16. Exit rule

A feature is not done until:

- acceptance criteria are tested;
- tests run automatically where feasible;
- evidence is linked to the work item;
- security and data impacts are reviewed;
- documentation and operations are updated;
- Product Owner accepts the result.
