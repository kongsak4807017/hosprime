# HosPrime Engineering Run 0062 — M1-B Source Owner Evidence Collection Execution Readiness Real User

Date: 2026-07-05
Stage: REAL USER
Parent issue: #10
Memory epic: #8
Control issue: #80
Previous stage: REAL PROBLEM (#79)
Next stage: BASELINE

## North Star outcome supported

Enable healthcare and public-health organizations to use trusted data, knowledge, organizational memory and governed AI to complete real work and make better decisions faster, with evidence, accountability and continuous learning.

This bounded REAL USER stage supports evidence quality, user trust, decision-to-outcome traceability, knowledge reuse and zero unauthorized high-impact action by defining who may participate in later controlled source-owner evidence collection execution readiness and what they may or may not decide.

## Repository evidence checked before selecting work

- `README.md` on `main` was read before work selection and confirms the North Star, ordered Loop Engineering sequence, Core Rules, memory boundaries and current controlled release target: Milestone 1 — Governed Knowledge Oracle MVP.
- Open issue #80 is the active ordered M1-B stage: REAL USER after #79 REAL PROBLEM.
- Previous run inspected: `engineering_runs/2026-07-05/0061-m1b-source-owner-evidence-collection-execution-readiness-real-problem.md`.
- Controlled packet inspected: `docs/governance/M1_B_SOURCE_OWNER_COLLECTION_READINESS_PACKET.md`.
- Controlled memory-boundary artifact inspected: `docs/governance/M1_B_SOURCE_CONFIRMATION_MEMORY_BOUNDARY.md`.
- Source register inspected only: `data/source_register/m1_source_register.yml`.
- Open issue inspection identified #10 as the parent governed source lifecycle workstream and #80 as the active sequenced control issue.
- Open PR inspection found no open pull request competing with this bounded stage.
- Combined status check for prior REAL PROBLEM commit `88746edd9020a020031978c9206f6d2f1b9741c4` returned no statuses; therefore this run does not claim CI pass.

## Real organizational work problem

The previous REAL PROBLEM stage defined that source-owner evidence collection cannot safely start until HosPrime defines the execution-readiness boundary for moving from an empty released packet to later controlled filled-packet collection, while preserving explicit non-approval, non-ingestion and non-RAG-activation status.

This REAL USER stage defines the exact users and decision-rights boundaries for that later controlled filled-packet workflow. It does not collect evidence or change source state.

## Real users and roles for controlled execution-readiness collection

### 1. Accountable sponsor / public-health executive

Real work need:

- confirm that source-owner evidence collection supports a real organizational decision need under M1;
- protect against unsupported factual answers or high-impact action.

May decide:

- whether a knowledge pack is worth sending into controlled collection-readiness workflow;
- whether a source-owner packet should be prioritized for later completion.

May not decide in this stage:

- source approval;
- ingestion, parsing, embedding, indexing or RAG activation;
- bypassing reviewer or access-control requirements.

### 2. Provincial program source owner

Real work need:

- identify the accountable program context behind one seed source record;
- later provide controlled file/system location, version/source period, currentness note and limitation context.

May decide:

- whether they are the correct source owner or whether another office must be routed;
- whether controlled source facts are present, pending, missing or not applicable with rationale.

May not decide in this stage:

- independent review result;
- final source approval;
- active RAG activation.

### 3. Source inventory operator

Real work need:

- turn source-owner statements into structured collection-readiness packet fields without inventing missing facts.

May decide:

- whether a field is captured as `present`, `pending_with_accountable_owner`, `missing` or `not_applicable_with_rationale` according to the released packet rules;
- whether a pending field has an accountable owner and next action note.

May not decide in this stage:

- authority of the source;
- reviewer acceptance;
- source-register status transition;
- ingestion or retrieval activation.

### 4. Data governance lead

Real work need:

- protect classification, role-scoped access, provenance, limitations and conflict-of-interest boundaries before any source can move toward review.

May decide:

- whether access-policy and classification fields are ready enough for later review routing;
- whether a filled packet must fail closed because of ambiguous role scope, classification, provenance or access route.

May not decide in this stage:

- that the source is approved for factual answers;
- that the source is safe for active RAG indexing without separate retrieval evaluation and activation gate.

### 5. Knowledge reviewer / independent reviewer

Real work need:

- later review filled-packet completeness and identify whether source approval review can proceed.

May decide:

- whether a later filled packet is review-ready or must be returned for correction;
- whether collection-readiness evidence is sufficient to continue to separate source approval review.

May not decide in this stage:

- final source approval without an explicit later review record;
- source ingestion or RAG activation;
- promotion into Organizational Memory / Governed RAG.

## Decision-rights boundaries

```text
PACKET_TEMPLATE_RELEASED = true
REAL_USERS_DEFINED_FOR_EXECUTION_READINESS = true
SOURCE_OWNER_EVIDENCE_COLLECTION_EXECUTION_ALLOWED_NOW = false
FILLED_PACKET_ALLOWED_IN_LATER_STAGE_ONLY = true
FILLED_PACKET_CONFERS_SOURCE_APPROVAL = false
SOURCE_APPROVAL_REQUIRES_SEPARATE_AUTHORIZED_REVIEW_RECORD = true
RAG_ACTIVATION_REQUIRES_APPROVED_SOURCE_AND_RETRIEVAL_GATE = true
```

Operational meaning:

1. A sponsor may authorize later controlled packet completion, but not source approval.
2. A source owner may provide or route facts, but not self-approve source authority.
3. An inventory operator may structure evidence, but not invent missing fields.
4. A data governance lead may fail the packet closed for governance gaps, but not activate retrieval.
5. A knowledge reviewer may determine review-readiness, but final approval and RAG activation remain separate later gates.

## Workflow boundary for later execution-readiness collection

Later controlled source-owner evidence collection may only proceed record-by-record through this boundary:

```text
select_one_seed_record
-> confirm source register identity
-> identify accountable sponsor/source owner route
-> capture field-group statuses using the released packet
-> record pending owner and next action for unresolved fields
-> preserve explicit non-approval assertion
-> route to later baseline/review-readiness measurement
```

This stage does not perform that workflow. It only defines the user and decision-rights boundary.

## Baseline preserved

```text
SEED_RECORDS_MEASURED = 5
FIELD_GROUPS_MEASURED = 10
TOTAL_FIELD_GROUP_RECORD_CHECKS = 50
RESOLVED_FIELD_GROUP_RECORD_CHECKS = 25
UNRESOLVED_FIELD_GROUP_RECORD_CHECKS = 25
DECISION_RIGHTS_READINESS_GAP_RATE = 50.0%
FULLY_COLLECTION_READY_RECORDS = 0 / 5
FULLY_REVIEW_READY_RECORDS = 0 / 5
FULLY_APPROVED_RECORDS = 0 / 5
ACTIVE_RAG_RECORDS = 0 / 5
```

The source register still records all five seed records as placeholder-only with pending owner assignment, pending inventory, pending checksum, not reviewed, not approved and inactive RAG status.

## Target metric for this execution-readiness cycle

```text
TARGET_DECISION_RIGHTS_READINESS_GAP_RATE_AFTER_LATER_FILLED_PACKET <= 30%
TARGET_FULLY_COLLECTION_READY_RECORDS_AFTER_LATER_FILLED_PACKET >= 3 / 5
TARGET_REAL_USERS_DEFINED_FOR_SOURCE_OWNER_EVIDENCE_COLLECTION_EXECUTION_READINESS = true
TARGET_DECISION_RIGHTS_BOUNDARIES_DEFINED = true
TARGET_FULLY_APPROVED_RECORDS = 0 unless authorized human review evidence exists
TARGET_ACTIVE_RAG_RECORDS = 0 until approved source, retrieval evaluation and activation gate exist
```

This REAL USER run does not claim the target gap reduction has been achieved.

## Work completed in this run

- Defined exact real users for controlled source-owner evidence collection execution readiness.
- Defined user-specific decision rights and prohibitions.
- Defined the later record-by-record workflow boundary.
- Preserved the baseline and source-register non-approval state.
- Created this engineering-run evidence package only.
- Did not collect source-owner evidence.
- Did not modify `data/source_register/m1_source_register.yml`.
- Did not approve, ingest, parse, embed, index, answer from or activate any source.

## Acceptance result

```text
M1_B_REAL_USER_COMPLETED = true
REAL_USERS_DEFINED_FOR_SOURCE_OWNER_EVIDENCE_COLLECTION_EXECUTION_READINESS = true
DECISION_RIGHTS_BOUNDARIES_DEFINED = true
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
NEXT_STAGE = BASELINE
```

## Memory layer affected

Engineering-run evidence package only.

No Personal / Staff Twin Memory, Person Memory, Role Memory, Research Staging promotion state or Organizational Memory / Governed RAG was modified or promoted.

## Risks and blockers

- Source-owner evidence collection has not started.
- No source owner, sponsor, controlled location, checksum, reviewer or currentness fact has been verified.
- No human source approval exists for any M1 seed record.
- No source has been ingested, parsed, embedded, indexed or activated in RAG.
- CI pass was not observed and is not claimed.

## Single next stage

BASELINE — measure execution-readiness baseline against the defined real-user and decision-rights boundary, without modifying the source register or claiming evidence collection, approval, ingestion or RAG activation.
