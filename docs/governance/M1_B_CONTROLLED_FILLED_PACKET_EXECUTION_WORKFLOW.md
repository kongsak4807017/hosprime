# M1-B Controlled Filled-Packet Execution Workflow

Status: controlled BUILD artifact / workflow guidance only / non-authoritative for source approval  
Release target: Milestone 1 — Governed Knowledge Oracle MVP  
Parent issue: #10  
Memory epic: #8  
Control issue: #85  
Previous stage: PLAN (#84)  
Current stage: BUILD  
Next stage: TEST

## Purpose

This workflow defines how a later operator may fill M1-B source-owner collection-readiness packets in a controlled, auditable way without changing source-register approval state or activating any source for Organizational RAG.

It supports the HosPrime North Star by improving evidence quality, source-owner accountability, decision-to-outcome traceability, knowledge reuse and zero unauthorized high-impact action.

## Non-approval boundary

This workflow is for collection-readiness execution only. It does not approve, ingest, parse, embed, index, retrieve, answer from or promote any source.

```text
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
```

## Real user and real work problem

Real users:

- public-health executive / accountable sponsor;
- provincial program source owner;
- source inventory operator;
- data governance lead;
- knowledge reviewer / independent reviewer.

Real work problem:

The M1 register has five seed records and a released source-owner collection-readiness packet, but the project still needs an executable controlled workflow for filling packets consistently without letting source-owner collection evidence be misread as source approval or active Organizational RAG truth.

## Baseline carried forward

```text
DECISION_RIGHTS_READINESS_GAP_RATE = 50.0%
FULLY_COLLECTION_READY_RECORDS = 0 / 5
FULLY_REVIEW_READY_RECORDS = 0 / 5
FULLY_APPROVED_RECORDS = 0 / 5
ACTIVE_RAG_RECORDS = 0 / 5
```

## Target for later filled-packet execution

```text
TARGET_DECISION_RIGHTS_READINESS_GAP_RATE_AFTER_LATER_FILLED_PACKET <= 30%
TARGET_FULLY_COLLECTION_READY_RECORDS_AFTER_LATER_FILLED_PACKET >= 3 / 5
TARGET_FULLY_APPROVED_RECORDS = 0 unless authorized human review evidence exists
TARGET_ACTIVE_RAG_RECORDS = 0 until approved source, retrieval evaluation and activation gate exist
```

This BUILD artifact does not claim that any target has been achieved.

## Source IDs allowed for packet execution

A filled packet may be opened only for a source ID already present in `data/source_register/m1_source_register.yml`:

```text
M1A-PM25-001
M1A-TB-001
M1A-NCD-001
M1A-EOC-001
M1A-DIGITAL-001
```

Fail closed if the source ID is absent, duplicated, invented, renamed or not present in the register.

## Per-source packet naming convention

Filled packets should be stored as engineering evidence before any source-register mutation is considered:

```text
engineering_runs/<YYYY-MM-DD>/m1b-filled-packet-<source_id-lowercase>-collection-readiness.md
```

Example:

```text
engineering_runs/2026-07-05/m1b-filled-packet-m1a-pm25-001-collection-readiness.md
```

The packet filename is evidence-package metadata only. It does not change lifecycle state, review status, approval status or active RAG status.

## Required workflow steps

### Step 1 — Confirm source identity from the register

Required checks:

```text
source_id_exists_in_register = true
source_register_path = data/source_register/m1_source_register.yml
source_register_record_seen = true
source_register_mutation_required = false
```

Do not create packet evidence for unknown source IDs.

### Step 2 — Open packet under collection-readiness-only status

Required packet status:

```text
packet_status = draft_collection_readiness_only
non_approval_boundary_acknowledged = true
```

Fail closed if packet status implies approval, review-pending state, index readiness, active retrieval or Organizational Memory promotion.

### Step 3 — Fill exactly ten field groups

The packet must include these ten field groups:

1. `source_identity_mapping`
2. `organization_scope_confirmation`
3. `accountable_sponsor`
4. `source_owner`
5. `controlled_location`
6. `version_or_source_period`
7. `checksum_or_pending`
8. `classification_access`
9. `reviewer_routing`
10. `provenance_limitations_non_approval`

Allowed field-group statuses only:

```text
present
pending_with_accountable_owner
missing
not_applicable_with_rationale
```

### Step 4 — Record accountable gap routing

Every `pending_with_accountable_owner` group must include both:

```text
accountable_owner_for_pending
next_action_if_pending_or_missing
```

Fail closed if either value is missing.

Every `missing` group must include:

```text
next_action_if_pending_or_missing
```

Missing must not be hidden as `present`.

### Step 5 — Preserve checksum integrity boundary

Checksum may be `pending` only when the controlled file is not yet inventoried. The packet must record one of:

```text
checksum_value + checksum_method
checksum_pending_reason
non_file_verification_method
```

Do not claim file integrity verification without controlled file access and checksum evidence.

### Step 6 — Preserve classification and access boundary

Restricted sources must remain restricted until authorized review evidence exists.

Required checks:

```text
restricted_source_handling_preserved = true
access_policy_loosened_without_review = false
allowed_roles_seen_or_pending_with_owner = true
```

### Step 7 — Route to reviewer precheck without approval

Reviewer routing must include:

```text
review_gate = collection_readiness_precheck
reviewer_role_or_office = present_or_pending_with_accountable_owner
conflict_of_interest_check = present_or_pending_with_accountable_owner
escalation_path = present_or_pending_with_accountable_owner
explicit_non_approval_decision = not_approved
active_rag_index_allowed = false
```

Reviewer precheck is not source approval. It only determines whether the packet is ready for a later source review gate.

### Step 8 — Record provenance, limitations and applicability

Each packet must state:

```text
evidence_collected_by = recorded_or_pending_with_accountable_owner
evidence_collection_date = recorded_or_pending_with_accountable_owner
evidence_collection_method = recorded_or_pending_with_accountable_owner
limitation_or_replacement_note = recorded_or_not_applicable_with_rationale
applicability_boundary = recorded_or_pending_with_accountable_owner
source_approval_claimed = false
ingestion_claimed = false
active_rag_activation_claimed = false
```

### Step 9 — Calculate collection-readiness score

For all five seed records:

```text
total_collection_groups = source_record_count * 10
closed_collection_groups = present_groups + accepted_not_applicable_groups
gap_collection_groups = pending_groups + missing_groups
DECISION_RIGHTS_READINESS_GAP_RATE = gap_collection_groups / total_collection_groups
```

Per source:

```text
collection_ready_for_precheck = true only when all 10 groups are closed
review_ready_for_precheck = true only when reviewer routing, conflict handling, provenance/limitations and non-approval assertion are closed
collection_ready_for_precheck != source_approved
collection_ready_for_precheck != review_pending
collection_ready_for_precheck != index_ready
collection_ready_for_precheck != indexed
```

### Step 10 — Store as engineering evidence only

Allowed output:

```text
engineering-run evidence package
issue comment or linked issue transition
later test fixture or validation artifact
```

Disallowed output in this stage:

```text
source-register mutation
source approval
ingestion
parsing
embedding
indexing
active RAG activation
factual answer permission
Organizational Memory promotion
```

## Fail-closed checklist

```text
FAIL_IF_SOURCE_ID_NOT_IN_REGISTER = true
FAIL_IF_PACKET_STATUS_NOT_COLLECTION_READINESS_ONLY = true
FAIL_IF_FIELD_GROUP_COUNT_NOT_10 = true
FAIL_IF_STATUS_NOT_IN_ALLOWED_SET = true
FAIL_IF_PENDING_WITHOUT_ACCOUNTABLE_OWNER = true
FAIL_IF_PENDING_WITHOUT_NEXT_ACTION = true
FAIL_IF_MISSING_MARKED_PRESENT = true
FAIL_IF_SOURCE_OWNER_ASSERTION_TREATED_AS_REVIEWER_DECISION = true
FAIL_IF_CHECKSUM_CLAIMED_WITHOUT_CONTROLLED_FILE_EVIDENCE = true
FAIL_IF_RESTRICTED_ACCESS_LOOSENED_WITHOUT_REVIEW = true
FAIL_IF_SOURCE_APPROVAL_STATUS_CHANGED = true
FAIL_IF_LIFECYCLE_STATE_ADVANCED = true
FAIL_IF_ACTIVE_RAG_INDEX_CHANGED = true
FAIL_IF_FACTUAL_ANSWER_PERMISSION_CLAIMED = true
FAIL_IF_EXTERNAL_RESEARCH_PROMOTED_WITHOUT_REVIEW = true
FAIL_IF_PERSONAL_OR_STAFF_TWIN_MEMORY_PROMOTED_WITHOUT_REVIEW = true
```

## Acceptance flags for this BUILD artifact

```text
M1_B_BUILD_COMPLETED = true
CONTROLLED_FILLED_PACKET_WORKFLOW_ARTIFACT_ADDED = true
PER_SOURCE_PACKET_NAMING_CONVENTION_ADDED = true
SCORING_RULE_IMPLEMENTATION_GUIDANCE_ADDED = true
FAIL_CLOSED_CHECKLIST_ADDED = true
REVIEW_ROUTING_BOUNDARY_ADDED = true
NON_APPROVAL_AND_NON_RAG_ASSERTIONS_ADDED = true
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
NEXT_STAGE = TEST
```

## Memory layer affected

Affected:

- engineering-run evidence;
- issue traceability;
- controlled governance documentation.

Not affected:

- Personal / Staff Twin Memory;
- Person Memory;
- Role Memory;
- Organizational Memory / Governed RAG;
- Research Staging promotion;
- source-register approval status;
- source-register lifecycle state;
- source-register active-RAG status.
