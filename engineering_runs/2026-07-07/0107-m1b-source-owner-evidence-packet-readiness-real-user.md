# HosPrime Engineering Run 0107 — M1-B Source-Owner Evidence Packet Readiness Real User

Date: 2026-07-07
Stage: REAL USER
Parent issue: #10
Memory epic: #8
Control issue: #125
Previous stage: REAL PROBLEM (#124)
Next stage: BASELINE

## North Star outcome supported

This REAL USER stage supports the HosPrime North Star by defining who needs, owns, reviews, inventories and may later technically process source-owner evidence packets before any M1 Governed Knowledge Oracle seed source can move from placeholder discovery toward reviewed approval.

Supported outcomes:

- evidence-based decisions;
- knowledge continuity;
- decision-to-outcome traceability;
- user trust;
- knowledge reuse;
- reduced rework from unclear ownership;
- zero unauthorized high-impact action.

## Repository evidence checked

- `README.md` on `main` was read first for the North Star, current controlled release target, loop sequence, Core Rules and memory boundaries.
- Open issues were inspected. The current ordered control issue is #125.
- Open pull requests were inspected; no open PR was found and no PR change or merge is claimed.
- Recent engineering-run evidence inspected: `engineering_runs/2026-07-07/0106-m1b-source-owner-evidence-packet-readiness-real-problem.md`.
- Source register inspected and not modified: `data/source_register/m1_source_register.yml`.
- CI/status evidence for commit `dcd4d249246b59799c75f34b7a74b457cd20428a` returned no combined statuses and no associated workflow runs; no CI pass is claimed.

## Current controlled release target

```text
CONTROLLED_RELEASE_TARGET = Milestone 1 — Governed Knowledge Oracle MVP
M1_MUST_INGEST_APPROVED_DOCUMENTS = true
M1_MUST_RETRIEVE_EVIDENCE = true
M1_MUST_ANSWER_ONLY_WITH_SUFFICIENT_EVIDENCE = true
M1_MUST_PROVIDE_TRACEABLE_CITATIONS = true
M1_MUST_ENFORCE_ACCESS_CONTROL = true
M1_MUST_RECORD_AUDIT_AND_COST_DATA = true
```

## Current loop stage

```text
CURRENT_STAGE = REAL USER
PREVIOUS_STAGE = REAL PROBLEM
NEXT_STAGE = BASELINE
```

## Baseline and target metric

```text
SEED_RECORDS_COUNT = 5
APPROVED_DOCUMENTS_COUNT = 0
FILLED_SOURCE_OWNER_PACKET_COUNT = 0 / 5
RECORDED_SOURCE_APPROVALS = 0 / 5
ACTIVE_RAG_READY_RECORDS = 0 / 5
SOURCE_REGISTER_RECORDS_WITH_PENDING_OWNER_PERSON = 5 / 5
SOURCE_REGISTER_RECORDS_WITH_PENDING_FILE_LOCATION = 5 / 5
SOURCE_REGISTER_RECORDS_WITH_PENDING_VERSION = 5 / 5
SOURCE_REGISTER_RECORDS_WITH_PENDING_CHECKSUM = 5 / 5
SOURCE_REGISTER_RECORDS_WITH_REVIEW_STATUS_NOT_REVIEWED = 5 / 5

TARGET_REAL_USER_COMPLETED = true
TARGET_SOURCE_OWNER_PACKET_USERS_AND_DECISION_RIGHTS_DEFINED = true
TARGET_SOURCE_REGISTER_MODIFIED = false
TARGET_SOURCE_OWNER_EVIDENCE_COLLECTED = false
TARGET_SOURCE_APPROVAL_CLAIMED = false
TARGET_RAG_ACTIVATION_CLAIMED = false
```

No improvement is claimed for source approval, ingestion, active RAG, Organizational Memory promotion or real-world execution.

## Real user and organizational work problem

### Real organizational work problem

M1 seed source records cannot safely progress toward governed evidence readiness until the project defines which real organizational users are accountable for each part of the source-owner evidence packet route. Without explicit user boundaries, a placeholder source-register row or released checklist may be misread as permission to collect, approve, ingest, index or answer from unreviewed evidence.

### Real users separated by decision right

| User / role | Real work problem | Decision right in this stage | Explicit non-right in this stage |
|---|---|---|---|
| Public-health executive sponsor | Needs confidence that M1 source readiness supports real organizational decision work without unsafe automation. | Confirms the business need for auditable source-owner packets and identifies the priority knowledge-pack route. | Does not approve sources, authorize ingestion, or claim operational completion. |
| Data governance lead | Needs a governed route separating ownership, classification, access policy, review, lifecycle state and auditability. | Defines packet governance fields, required separation of memory layers and approval prerequisites. | Does not promote Research Staging or source placeholders into Organizational Memory. |
| Provincial program source owner | Needs a way to later provide accountable evidence for PM2.5, TB, NCD, EOC or Digital Health source packs. | Identifies accountable office/role and the type of evidence that must later be inventoried. | Does not yet submit evidence, certify files, approve quality, or authorize RAG use. |
| Independent knowledge reviewer | Needs a future review path to decide whether a packet is complete, relevant, current and safe for controlled use. | Defines the reviewer role and independence requirement for later review. | Does not yet issue review approval or rejection. |
| Source inventory operator | Needs a safe way to later record file/system location, version, checksum and provenance without changing approval state. | Defines the inventory function and audit fields required for a later packet. | Does not yet collect files, compute checksum, mutate source register, or parse content. |
| Technical ingestion operator | Needs clear gating before parsing, embedding, indexing or activation. | Defines that technical work can start only after authorized review and explicit execution issue. | Does not ingest, parse, embed, index, activate RAG, or claim retrieval readiness. |

## Required separation of authority

```text
BUSINESS_NEED_CONFIRMED_BY = public_health_executive_sponsor
PACKET_GOVERNANCE_DEFINED_BY = data_governance_lead
SOURCE_ACCOUNTABILITY_HELD_BY = provincial_program_source_owner
REVIEW_DECISION_HELD_BY = independent_knowledge_reviewer
INVENTORY_EXECUTION_HELD_BY = source_inventory_operator_after_authorization
TECHNICAL_INGESTION_HELD_BY = technical_ingestion_operator_after_review_and_authorization
```

The same user should not both provide source-owner evidence and independently approve the source for Organizational RAG. The ingestion operator must not self-authorize parsing, embedding, indexing or activation.

## Knowledge-pack user mapping for the five seed records

| Seed source | Source-owner user direction | Reviewer direction | Access concern |
|---|---|---|---|
| `M1A-PM25-001` | Environmental health program lead or delegated accountable office. | Knowledge reviewer with environmental-health governance awareness. | Internal, role-scoped. |
| `M1A-TB-001` | TB / communicable disease program lead or delegated accountable office. | Knowledge reviewer independent from source preparation. | Restricted internal, role-scoped. |
| `M1A-NCD-001` | NCD program lead or delegated accountable office. | Knowledge reviewer independent from source preparation. | Internal, role-scoped. |
| `M1A-EOC-001` | EOC / emergency response lead or delegated accountable office. | Knowledge reviewer with incident-information sensitivity awareness. | Restricted internal, role-scoped. |
| `M1A-DIGITAL-001` | Digital health or data governance lead. | Knowledge reviewer independent from system owner. | Internal, role-scoped. |

This mapping is directional only. It does not name persons, collect evidence, approve sources, mutate the source register, or authorize technical ingestion.

## Boundary controls preserved

```text
SOURCE_REGISTER_MODIFIED = false
SOURCE_OWNER_EVIDENCE_COLLECTED = false
SOURCE_APPROVAL_CLAIMED = false
INGESTION_PERMISSION_CLAIMED = false
SOURCE_INGESTION_CLAIMED = false
SOURCE_PARSING_CLAIMED = false
SOURCE_EMBEDDING_CLAIMED = false
SOURCE_INDEXING_CLAIMED = false
RAG_ACTIVATION_CLAIMED = false
FACTUAL_ANSWER_PERMISSION_CLAIMED = false
ORGANIZATIONAL_MEMORY_PROMOTION_CLAIMED = false
REAL_WORLD_COMPLETION_CLAIMED = false
CI_PASS_CLAIMED = false
```

## Test and CI status

```text
MANUAL_REAL_USER_REVIEW_COMPLETED = true
AUTOMATED_TEST_ADDED = false
COMBINED_STATUS_COUNT_FOR_PREVIOUS_COMMIT = 0
WORKFLOW_RUNS_FOUND_FOR_PREVIOUS_COMMIT = 0
CI_PASS_CLAIMED = false
```

No CI pass is claimed because no successful workflow result was found for the inspected prior commit.

## Memory layer affected

Affected:

- engineering-run evidence;
- issue traceability;
- governance working memory for the M1-B loop.

Not affected:

- Personal / Staff Twin Memory;
- Person Memory;
- Role Memory;
- Organizational Memory / Governed RAG;
- Research Staging promotion state;
- source-register lifecycle state;
- source-register review status;
- source-register approval status;
- source-register active-RAG status.

## Risks or blockers

```text
RISK_GUIDANCE_CONFUSED_WITH_AUTHORIZATION = still_present
RISK_SOURCE_OWNER_PACKET_CONFUSED_WITH_SOURCE_APPROVAL = still_present
RISK_SOURCE_APPROVAL_CONFUSED_WITH_ACTIVE_RAG = still_present
RISK_ROLE_MAPPING_CONFUSED_WITH_PERSON_ASSIGNMENT = still_present
BLOCKER_TO_SOURCE_OWNER_EVIDENCE_COLLECTION = true until later authorized execution stage exists
BLOCKER_TO_SOURCE_APPROVAL = true until named reviewer and explicit human review decision exist
BLOCKER_TO_ACTIVE_RAG = true until approval, ingestion, retrieval evaluation and activation gates pass
OPEN_RELEASE_CLOSE_BLOCKER = issue #119 remains open from prior connector safety block
```

## Acceptance result

```text
M1_B_REAL_USER_COMPLETED = true
SOURCE_OWNER_PACKET_USERS_AND_DECISION_RIGHTS_DEFINED = true
SOURCE_REGISTER_MODIFIED = false
SOURCE_OWNER_EVIDENCE_COLLECTED = false
SOURCE_APPROVAL_CLAIMED = false
RAG_ACTIVATION_CLAIMED = false
CI_PASS_CLAIMED = false
```

## Single next stage

```text
NEXT_STAGE = BASELINE
NEXT_ISSUE_TITLE = M1-B Baseline: Source-owner evidence packet readiness baseline
```
