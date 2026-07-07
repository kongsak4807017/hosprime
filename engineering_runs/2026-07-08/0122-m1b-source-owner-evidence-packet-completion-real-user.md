# HosPrime Engineering Run 0122 — M1-B Authorized Source-Owner Evidence Packet Completion Real User

Date: 2026-07-08
Stage: REAL USER
Parent issue: #10
Memory epic: #8
Control issue: #140
Previous stage: REAL PROBLEM (#139)
Next stage: BASELINE

## North Star outcome supported

This REAL USER stage supports the HosPrime North Star by defining who must participate in authorized source-owner evidence packet completion before any M1 seed source can move toward review readiness. It strengthens evidence quality, user trust, decision-to-outcome traceability, knowledge reuse and zero unauthorized high-impact action.

## Repository evidence checked

- `README.md` on `main` was read first for the North Star, Core Rules, memory boundaries and current controlled release target.
- Active control issue inspected: #140, `M1-B Real User: Authorized source-owner evidence packet completion roles`.
- Recent commits inspected; latest observed commit: `4bb456ee75a5e5b3c1783cc26b8b00796689b8a2`.
- Open pull requests inspected; no open PR was found or acted on.
- CI status for latest observed commit was checked through combined status; no status contexts were returned, so CI pass is not claimed.
- Previous run inspected: `engineering_runs/2026-07-08/0121-m1b-source-owner-evidence-packet-completion-real-problem.md`.
- Source register inspected and not modified: `data/source_register/m1_source_register.yml`.
- Maturity gate evidence inspected: `docs/governance/MATURITY_GATES.md`.

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

## Real users and accountable roles

This stage defines accountable roles only. It does not name real persons, collect source-owner evidence, approve sources, mutate the source register, ingest, parse, embed, index, activate RAG or promote Organizational Memory.

### 1. Executive sponsor / accountable decision owner

Real work problem: needs evidence-grounded executive answers from M1 knowledge packs but must prevent unreviewed placeholders from being treated as organizational truth.

Decision rights at this stage:

- may confirm that source-owner evidence packet completion is an approved governance workstream;
- may assign accountability for packet completion workflow design;
- may not approve individual sources in this stage;
- may not authorize factual-answer use from placeholder sources in this stage.

### 2. Source-owner role for each knowledge pack

Mapped from the discovered seed records:

```text
M1A-PM25-001      -> Provincial public health environmental health lead
M1A-TB-001        -> Provincial TB program lead
M1A-NCD-001       -> Provincial NCD program lead
M1A-EOC-001       -> Provincial EOC or emergency response lead
M1A-DIGITAL-001   -> Digital health or data governance lead
```

Real work problem: the source-owner role must later verify whether the controlled source exists, is current, is appropriately classified and can be reviewed.

Decision rights at this stage:

- may be identified as the accountable role category for later packet completion;
- may later provide owner-role confirmation, controlled location, version/provenance, checksum or checksum-pending justification and classification/access context;
- may not be treated as a named person in this stage;
- may not approve the source alone unless a later review workflow explicitly grants that right.

### 3. Knowledge reviewer

Real work problem: must accept or reject review-ready packets before any source moves toward approved evidence status.

Decision rights at this stage:

- may later review packet completeness, provenance, classification, access-policy fit, conflicts, freshness and limitations;
- may recommend accept, reject, quarantine or request correction;
- may not approve a source in this stage because no completed packet exists yet.

### 4. Data governance / access-control lead

Real work problem: must prevent restricted or sensitive operational material from becoming accessible to unauthorized roles.

Decision rights at this stage:

- may later verify classification, role-scoped access policy, restricted/internal boundary and least-privilege access;
- may require quarantine or restriction before ingestion;
- may not activate access-control enforcement for these placeholder sources in this stage.

### 5. Ingestion operator / technical custodian

Real work problem: must know when a source is authorized for technical ingestion and when it must remain untouched.

Decision rights at this stage:

- may later parse, checksum, validate and prepare source files only after an authorized packet and review gate exist;
- may report parsing failure, duplicate detection and recoverability evidence;
- may not ingest, parse, embed, index or activate RAG from the current placeholder records.

### 6. Audit / evidence steward

Real work problem: must preserve traceability from source discovery through review, decision, ingestion and later answer use.

Decision rights at this stage:

- may later verify that packet completion has an audit trail, receipt, timestamp, accountable actor and review record;
- may flag missing execution records;
- may not claim real-world execution or completion from this stage.

## Handoff boundary

```text
SOURCE_OWNER_ROLE_IDENTIFIED = allowed
REAL_OWNER_PERSON_NAMED = not_allowed_this_stage
SOURCE_OWNER_EVIDENCE_COLLECTION = not_allowed_this_stage
SOURCE_APPROVAL = not_allowed_this_stage
SOURCE_REGISTER_MUTATION = not_allowed_this_stage
INGEST_PARSE_EMBED_INDEX = not_allowed_this_stage
RAG_ACTIVATION = not_allowed_this_stage
ORGANIZATIONAL_MEMORY_PROMOTION = not_allowed_this_stage
FACTUAL_ANSWER_PERMISSION = not_allowed_this_stage
```

The next BASELINE stage should measure the current role/decision-rights completeness and packet-completion readiness without changing source records.

## Baseline and target metric

Baseline preserved from prior run and `data/source_register/m1_source_register.yml`:

```text
SEED_RECORDS_COUNT = 5
FILLED_SOURCE_OWNER_PACKET_COUNT = 0 / 5
SOURCE_OWNER_PACKET_READINESS_RATE = 0%
SOURCE_RECORDS_WITH_APPROVAL_STATUS_APPROVED = 0 / 5
SOURCE_RECORDS_WITH_ACTIVE_RAG_INDEX = 0 / 5
```

Target for this REAL USER stage:

```text
M1_B_REAL_USER_COMPLETED = true
AUTHORIZED_SOURCE_OWNER_PACKET_COMPLETION_USERS_DEFINED = true
DECISION_RIGHTS_AND_HANDOFF_BOUNDARY_DEFINED = true
SOURCE_REGISTER_MODIFIED = false
SOURCE_OWNER_EVIDENCE_COLLECTED = false
SOURCE_OWNER_PERSON_NAMED = false
SOURCE_APPROVAL_CLAIMED = false
RAG_ACTIVATION_CLAIMED = false
CI_PASS_CLAIMED = false
REAL_WORLD_EXECUTION_CLAIMED = false
```

## Test / CI status

```text
LOCAL_TEST_EXECUTED = false
CI_STATUS_CHECKED = true
CI_STATUS_CONTEXTS_RETURNED = 0
CI_PASS_CLAIMED = false
```

No CI success is claimed. This run only adds a governance evidence document and closes the corresponding REAL USER issue.

## Memory layer affected

```text
PERSONAL_STAFF_TWIN_MEMORY_MODIFIED = false
PERSON_MEMORY_MODIFIED = false
ROLE_MEMORY_MODIFIED = false
ORGANIZATIONAL_MEMORY_PROMOTED = false
RESEARCH_STAGING_MODIFIED = false
GOVERNANCE_RUN_EVIDENCE_ADDED = true
```

## Risks and blockers

- The five source-owner packets remain unfilled.
- No real source-owner person was named.
- No source-owner evidence was collected or claimed.
- No source was approved.
- The source register remains unchanged.
- No ingestion, parsing, embedding, indexing or RAG activation occurred.
- CI status returned no contexts; CI pass is not claimed.
- A later authorized review workflow is still required before any source can become approved or retrievable.

## Completion result

```text
M1_B_REAL_USER_COMPLETED = true
AUTHORIZED_SOURCE_OWNER_PACKET_COMPLETION_USERS_DEFINED = true
DECISION_RIGHTS_AND_HANDOFF_BOUNDARY_DEFINED = true
SOURCE_REGISTER_MODIFIED = false
SOURCE_OWNER_EVIDENCE_COLLECTED = false
SOURCE_OWNER_PERSON_NAMED = false
SOURCE_APPROVAL_CLAIMED = false
SOURCE_INGESTION_CLAIMED = false
SOURCE_PARSING_CLAIMED = false
SOURCE_EMBEDDING_CLAIMED = false
SOURCE_INDEXING_CLAIMED = false
RAG_ACTIVATION_CLAIMED = false
FACTUAL_ANSWER_PERMISSION_CLAIMED = false
ORGANIZATIONAL_MEMORY_PROMOTION_CLAIMED = false
CI_PASS_CLAIMED = false
REAL_WORLD_EXECUTION_CLAIMED = false
```

## Single next stage

BASELINE — measure the current role/decision-rights completeness and packet-completion readiness for the five seed records without changing source records or collecting evidence.
