# HosPrime Engineering Run 0092 — M1-B Controlled Authorized Packet Execution Real User

Date: 2026-07-06
Stage: REAL USER
Parent issue: #10
Memory epic: #8
Control issue: #110
Previous stage: REAL PROBLEM (#109)
Next stage: BASELINE

## North Star outcome supported

Enable healthcare and public-health organizations to use trusted data, knowledge, organizational memory and governed AI to complete real work and make better decisions faster, with evidence, accountability and continuous learning.

This bounded REAL USER stage supports Trusted Task Completion Rate, evidence quality, user trust, decision-to-outcome traceability, knowledge reuse, cost control and zero unauthorized high-impact action by defining who may participate in controlled authorized source-owner packet execution and who may not treat packet preparation as approval, ingestion, indexing, active RAG or Organizational Memory promotion.

## Repository evidence checked before selecting work

- `README.md` on `main` was read first and confirms the North Star, ordered loop, Core Rules, memory boundaries and current controlled release target: Milestone 1 — Governed Knowledge Oracle MVP.
- Open issues were inspected. #110 is the current ordered M1-B control issue for REAL USER after #109 REAL PROBLEM.
- Recent PR inspection did not identify an open pull request that this run should review, merge or release.
- Prior REAL PROBLEM evidence was inspected: `engineering_runs/2026-07-06/0091-m1b-controlled-authorized-packet-execution-real-problem.md`.
- Source register was inspected in `data/source_register/m1_source_register.yml`; all five seed records remain `DISCOVERED`, `not_reviewed`, `not_approved` and `active_rag_index: false`.
- Maturity gates were inspected in `docs/governance/MATURITY_GATES.md`; M1-A still requires named owners, captured review metadata, approved documents and restricted-document access control before retrieval readiness can proceed.

## Current loop stage

```text
CURRENT_STAGE = REAL USER
PREVIOUS_STAGE = REAL PROBLEM
NEXT_STAGE = BASELINE
```

## Real organizational work problem carried forward

Placeholder source-register records cannot become trusted Governed Knowledge Oracle evidence until source-owner packet execution is authorized, auditable and separated from source approval, ingestion, indexing, active retrieval and Organizational Memory promotion.

## Real users and decision-right boundaries

### 1. Public-health executive / accountable sponsor

Real work problem:

- needs the organization to move source packs toward governed evidence without bypassing approval, access control or auditability.

Permitted decision rights in this stage:

```text
MAY_REQUEST_PACKET_PREPARATION = true
MAY_DEFINE_BUSINESS_PRIORITY = true
MAY_CONFIRM_ORGANIZATIONAL_NEED = true
MAY_APPROVE_SOURCE_STATUS = false in this stage unless separately named as authorized release/review authority with explicit review record
MAY_ACTIVATE_RAG = false
MAY_TREAT_PACKET_AS_EXECUTED_WORK = false
```

Accountability boundary:

- may sponsor the work and confirm organizational priority;
- may not convert packet skeletons or readiness language into evidence approval or operational truth.

### 2. Provincial program source owner

Real work problem:

- owns or stewards the PM2.5, TB, NCD, EOC or Digital Health source material and must provide accountable provenance before the Knowledge Oracle can use it.

Permitted decision rights in this stage:

```text
MAY_PROVIDE_SOURCE_OWNER_EVIDENCE = future stage only, not performed in this run
MAY_CONFIRM_SOURCE_OWNERSHIP = future stage only, not performed in this run
MAY_IDENTIFY_SOURCE_LOCATION = future stage only, not performed in this run
MAY_APPROVE_INDEXING = false
MAY_APPROVE_RAG_ACTIVATION = false
MAY_SELF_APPROVE_RESTRICTED_SOURCE_FOR_RETRIEVAL = false
```

Accountability boundary:

- can be the accountable source owner for future packet completion;
- cannot self-promote source material into approved Organizational RAG without independent governance review and recorded approval.

### 3. Source inventory operator

Real work problem:

- needs a controlled way to prepare source-owner packet fields without modifying the source register into a misleading state.

Permitted decision rights in this stage:

```text
MAY_PREPARE_PACKET_DRAFT = future PLAN/BUILD execution only, not performed in this run
MAY_RECORD_PENDING_FIELD_STATUS = future bounded execution only
MAY_MUTATE_SOURCE_REGISTER_APPROVAL_STATUS = false
MAY_CHANGE_LIFECYCLE_TO_APPROVED_OR_INDEX_READY = false
MAY_INGEST_OR_PARSE_SOURCE = false
MAY_EMBED_OR_INDEX_SOURCE = false
```

Accountability boundary:

- may prepare auditable packet drafts when a later plan authorizes the action;
- must preserve fail-closed defaults until reviewer and approver evidence exists.

### 4. Data governance lead

Real work problem:

- must ensure classification, access policy, retention, privacy and source lifecycle are not bypassed in pursuit of speed.

Permitted decision rights in this stage:

```text
MAY_DEFINE_GOVERNANCE_REQUIREMENTS = true
MAY_REVIEW_CLASSIFICATION_AND_ACCESS_POLICY = future review stage only
MAY_AUTHORIZE_RESTRICTED_SOURCE_ACCESS_POLICY = future review/approval record only
MAY_APPROVE_FACTUAL_ANSWER_PERMISSION = false
MAY_ALLOW_UNAUTHORIZED_HIGH_IMPACT_ACTION = false
```

Accountability boundary:

- owns governance criteria and fail-closed interpretation;
- cannot replace source-owner attestation or independent knowledge review.

### 5. Knowledge reviewer / independent reviewer

Real work problem:

- must determine whether source material is sufficient, current, relevant, internally consistent and safe for later retrieval use.

Permitted decision rights in this stage:

```text
MAY_REVIEW_PACKET_EVIDENCE = future REVIEW stage only
MAY_RECORD_ACCEPT_REJECT_OR_NEEDS_REVISION = future REVIEW stage only
MAY_APPROVE_SOURCE_FOR_RAG_ALONE = false unless named approval authority and gate evidence exists
MAY_IGNORE_CONFLICT_OR_STALENESS = false
MAY_PROMOTE_EXTERNAL_OR_PERSONAL_MEMORY_TO_ORGANIZATIONAL_TRUTH = false
```

Accountability boundary:

- can provide independent review and evidence-quality judgment in a later stage;
- cannot bypass source ownership, data governance or maturity gates.

### 6. Technical ingestion / indexing operator

Real work problem:

- may later ingest, parse, embed or index only approved, access-controlled source versions.

Permitted decision rights in this stage:

```text
MAY_INGEST_SOURCE = false
MAY_PARSE_SOURCE = false
MAY_EMBED_SOURCE = false
MAY_INDEX_SOURCE = false
MAY_ACTIVATE_ACTIVE_RAG = false
MAY_RUN_RETRIEVAL_EVALUATION = false
```

Accountability boundary:

- remains blocked until approved source status and later technical execution plan exist.

## Decision-right matrix

```text
ROLE                                      REQUEST_PACKET  PROVIDE_EVIDENCE  REVIEW_EVIDENCE  APPROVE_SOURCE  INGEST_INDEX  ACTIVATE_RAG
public_health_executive_sponsor           yes             no                no               no              no            no
provincial_program_source_owner           no              future_only       no               no              no            no
source_inventory_operator                 future_only      no                no               no              no            no
data_governance_lead                      no              no                future_only      no              no            no
knowledge_reviewer_independent_reviewer   no              no                future_only      no              no            no
technical_ingestion_indexing_operator     no              no                no               no              no            no
```

## Blocked work explicitly preserved

```text
SOURCE_REGISTER_MODIFICATION = blocked
SOURCE_OWNER_EVIDENCE_COLLECTION = blocked in this run
SOURCE_APPROVAL = blocked
SOURCE_INGESTION = blocked
SOURCE_PARSING = blocked
SOURCE_EMBEDDING = blocked
SOURCE_INDEXING = blocked
ACTIVE_RAG_ACTIVATION = blocked
FACTUAL_ANSWER_PERMISSION = blocked
ORGANIZATIONAL_MEMORY_PROMOTION = blocked
PERSONAL_MEMORY_PROMOTION_TO_ORGANIZATIONAL_TRUTH = blocked
EXTERNAL_RESEARCH_PROMOTION_TO_ORGANIZATIONAL_TRUTH = blocked
```

## Baseline gap carried forward

```text
SEED_RECORDS_COUNT = 5
REQUIRED_RECORDS_TARGET = 100
LIFECYCLE_STATE_FOR_ALL_SEED_RECORDS = DISCOVERED
REVIEW_STATUS_FOR_ALL_SEED_RECORDS = not_reviewed
APPROVAL_STATUS_FOR_ALL_SEED_RECORDS = not_approved
ACTIVE_RAG_RECORDS = 0 / 5
FILLED_SOURCE_OWNER_PACKET_COUNT = 0
FULLY_CLOSED_PACKET_FIELD_GROUPS = 0 / 50
FULLY_COLLECTION_READY_RECORDS = 0 / 5
FULLY_REVIEW_READY_RECORDS = 0 / 5
FULLY_APPROVED_RECORDS = 0 / 5
```

## Target metric for this bounded REAL USER stage

```text
TARGET_M1_B_REAL_USER_COMPLETED = true
TARGET_REAL_USERS_AND_DECISION_RIGHTS_DEFINED = true
TARGET_SOURCE_REGISTER_MODIFIED = false
TARGET_SOURCE_OWNER_EVIDENCE_COLLECTED = false
TARGET_SOURCE_APPROVAL_CLAIMED = false
TARGET_RAG_ACTIVATION_CLAIMED = false
TARGET_CI_PASS_CLAIMED = false unless workflow evidence exists
```

No improvement in source readiness, retrieval readiness, answer quality, user acceptance or time saved is claimed in this stage.

## Work completed

Defined the real users, decision rights and accountability boundaries for controlled authorized packet execution readiness.

Opened the next bounded control issue for the ordered loop stage BASELINE.

## Evidence and GitHub links

- Control issue: #110
- Parent issue: #10
- Memory epic: #8
- Previous evidence: `engineering_runs/2026-07-06/0091-m1b-controlled-authorized-packet-execution-real-problem.md`
- Source register inspected but not modified: `data/source_register/m1_source_register.yml`
- Maturity gates inspected: `docs/governance/MATURITY_GATES.md`
- README inspected: `README.md`

## Test / CI status

```text
AUTOMATED_TEST_ADDED = false
CI_PASS_CLAIMED = false
```

No automated CI pass is claimed. This run is a governance evidence and issue-traceability stage only.

## Memory layer affected

Affected:

- engineering-run evidence;
- issue traceability;
- controlled governance planning memory.

Not affected:

- Personal / Staff Twin Memory;
- Person Memory;
- Role Memory as durable operational truth;
- Organizational Memory / Governed RAG;
- Research Staging promotion;
- source-register lifecycle state;
- source-register review status;
- source-register approval status;
- source-register active-RAG status.

## Risks or blockers

```text
BLOCKER_TO_SOURCE_OWNER_EVIDENCE_COLLECTION = true until BASELINE, RESEARCH, HYPOTHESIS and PLAN stages define measurable gaps, evidence basis, testable expectation and bounded execution plan
BLOCKER_TO_SOURCE_APPROVAL = true until named authorized reviewer and explicit human review decision exist
BLOCKER_TO_ACTIVE_RAG = true until source approval, retrieval evaluation and activation gate exist
RISK_PACKET_GUIDANCE_MISUSED_AS_AUTHORIZATION = true unless next stages preserve fail-closed boundaries
```

## Acceptance result

```text
M1_B_REAL_USER_COMPLETED = true
REAL_USERS_AND_DECISION_RIGHTS_DEFINED = true
SOURCE_REGISTER_MODIFIED = false
SOURCE_OWNER_EVIDENCE_COLLECTED = false
SOURCE_APPROVAL_CLAIMED = false
SOURCE_INGESTION_CLAIMED = false
SOURCE_PARSING_CLAIMED = false
SOURCE_EMBEDDING_CLAIMED = false
SOURCE_INDEXING_CLAIMED = false
RAG_ACTIVATION_CLAIMED = false
FACTUAL_ANSWER_PERMISSION_CLAIMED = false
ORGANIZATIONAL_MEMORY_PROMOTION_CLAIMED = false
CI_PASS_CLAIMED = false
```

## Single next stage

```text
NEXT_STAGE = BASELINE
NEXT_CONTROL_ISSUE = #111
```
