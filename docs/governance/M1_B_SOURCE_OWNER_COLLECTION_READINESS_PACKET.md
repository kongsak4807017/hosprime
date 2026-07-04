# M1-B Source Owner Evidence Collection Readiness Packet

Status: controlled BUILD artifact / collection-readiness template only / non-authoritative for source approval  
Release target: Milestone 1 — Governed Knowledge Oracle MVP  
Parent issue: #10  
Memory epic: #8  
Control issue: #70  
Previous stage: PLAN (#69)  
Current stage: BUILD  
Next stage: TEST

## Purpose

This packet gives source owners, source inventory operators, data governance leads and knowledge reviewers a bounded template for collecting source-owner evidence readiness for the five M1 seed records.

It supports the HosPrime North Star by improving evidence quality, decision-to-outcome traceability, knowledge reuse, user trust and zero unauthorized high-impact action.

## Non-approval boundary

This packet is **collection-readiness evidence only**.

Completing this packet does **not** mean that any source is approved, authoritative, ingested, parsed, embedded, indexed, active in RAG, retrievable, answerable or promoted into Organizational Memory / Governed RAG.

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

## Real user / real problem

Real users:

- public-health executive / accountable sponsor;
- provincial program source owner;
- source inventory operator;
- data governance lead;
- knowledge reviewer / independent reviewer.

Real work problem:

The M1 source register has five placeholder records, but collection readiness is still not operationally actionable. Source owners need a precise packet that records ownership, controlled location, version, checksum status, classification, reviewer routing and provenance without modifying the source register or accidentally implying source approval.

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

## Target for later filled-packet work

```text
TARGET_DECISION_RIGHTS_READINESS_GAP_RATE_AFTER_LATER_COLLECTION_PACKET <= 30%
TARGET_FULLY_COLLECTION_READY_RECORDS_AFTER_LATER_COLLECTION_PACKET >= 3 / 5
TARGET_FULLY_APPROVED_RECORDS = 0 unless authorized human review evidence exists
TARGET_ACTIVE_RAG_RECORDS = 0 until approved source, retrieval evaluation and activation gate exist
```

This BUILD stage does not claim that the target has been achieved.

## Covered seed source records

The packet template is intended to be copied once per seed source record from `data/source_register/m1_source_register.yml`:

```text
M1A-PM25-001
M1A-TB-001
M1A-NCD-001
M1A-EOC-001
M1A-DIGITAL-001
```

## Allowed field-group statuses

Use exactly one status for each of the ten field groups:

```text
present
pending_with_accountable_owner
missing
not_applicable_with_rationale
```

Status rules:

- `present` means a concrete value, controlled reference, accountable owner, evidence note or verification method is recorded.
- `pending_with_accountable_owner` means the gap has a named accountable owner and next action note.
- `missing` means no concrete value, accountable pending owner or next action exists.
- `not_applicable_with_rationale` may be used only with a reviewer-acceptable rationale.

## Ten source-owner collection readiness field groups

Each source record must include all ten groups below.

### 1. Source ID and knowledge-pack mapping

Purpose: prevent collection evidence from drifting away from the governed source register.

```yaml
source_identity_mapping:
  status: ""
  source_id: ""
  knowledge_pack: ""
  source_title: ""
  source_register_path: "data/source_register/m1_source_register.yml"
  source_register_record_seen: false
  evidence_note: ""
  accountable_owner_for_pending: ""
  next_action_if_pending_or_missing: ""
```

### 2. Organization scope confirmation

Purpose: identify which organization, office or controlled domain owns the source context.

```yaml
organization_scope_confirmation:
  status: ""
  organization_or_office: ""
  scope_boundary: ""
  confirmation_method: ""
  evidence_note: ""
  accountable_owner_for_pending: ""
  next_action_if_pending_or_missing: ""
```

### 3. Accountable sponsor role or person

Purpose: identify the accountable sponsor for collection readiness without inventing authority.

```yaml
accountable_sponsor:
  status: ""
  sponsor_role: ""
  sponsor_person_or_office: ""
  authority_basis: ""
  decision_scope: "collection_readiness_only"
  evidence_note: ""
  accountable_owner_for_pending: ""
  next_action_if_pending_or_missing: ""
```

### 4. Source owner role or person

Purpose: assign who can confirm the source inventory facts.

```yaml
source_owner:
  status: ""
  owner_role: ""
  owner_person_or_office: ""
  assignment_method: ""
  assignment_limitations: ""
  evidence_note: ""
  accountable_owner_for_pending: ""
  next_action_if_pending_or_missing: ""
```

### 5. Controlled file or system location

Purpose: avoid public-link or memory-only source claims.

```yaml
controlled_location:
  status: ""
  location_type: ""
  controlled_reference: ""
  access_route: ""
  non_public_reference_allowed: true
  evidence_note: ""
  accountable_owner_for_pending: ""
  next_action_if_pending_or_missing: ""
```

### 6. Version or source date/period evidence

Purpose: support freshness and supersession review.

```yaml
version_or_source_period:
  status: ""
  version: ""
  effective_date_or_period: ""
  currentness_statement: ""
  supersedes_or_replaces: ""
  evidence_note: ""
  accountable_owner_for_pending: ""
  next_action_if_pending_or_missing: ""
```

### 7. Checksum or checksum-pending reason

Purpose: avoid pretending file integrity is verified before controlled file access exists.

```yaml
checksum_or_pending:
  status: ""
  checksum_value: ""
  checksum_method: ""
  checksum_pending_reason: ""
  non_file_verification_method: ""
  evidence_note: ""
  accountable_owner_for_pending: ""
  next_action_if_pending_or_missing: ""
```

### 8. Classification and access policy confirmation

Purpose: keep restricted sources inactive and role-scoped.

```yaml
classification_access:
  status: ""
  classification_confirmed_or_disputed: ""
  access_policy_confirmed_or_disputed: ""
  permitted_roles_seen: []
  restricted_source_handling_required: false
  dispute_or_escalation_note: ""
  evidence_note: ""
  accountable_owner_for_pending: ""
  next_action_if_pending_or_missing: ""
```

### 9. Reviewer routing and review expectation

Purpose: route collection readiness to a human reviewer before any later source review.

```yaml
reviewer_routing:
  status: ""
  reviewer_role: ""
  reviewer_person_or_office: ""
  review_gate: "collection_readiness_precheck"
  conflict_of_interest_check: ""
  escalation_path: ""
  evidence_note: ""
  accountable_owner_for_pending: ""
  next_action_if_pending_or_missing: ""
```

### 10. Provenance, limitations, applicability and non-approval assertion

Purpose: make collected evidence auditable while preventing source approval or RAG activation claims.

```yaml
provenance_limitations_non_approval:
  status: ""
  evidence_collected_by: ""
  evidence_collection_date: ""
  evidence_collection_method: ""
  limitation_or_replacement_note: ""
  applicability_boundary: ""
  source_approval_claimed: false
  ingestion_claimed: false
  active_rag_activation_claimed: false
  evidence_note: ""
  accountable_owner_for_pending: ""
  next_action_if_pending_or_missing: ""
```

## Per-source packet template

Copy one block per source record. Do not fill values from memory unless there is controlled evidence.

```yaml
source_owner_collection_readiness_packet:
  source_id: ""
  knowledge_pack: ""
  source_title: ""
  packet_status: "draft_collection_readiness_only"
  non_approval_boundary_acknowledged: true
  source_identity_mapping: {}
  organization_scope_confirmation: {}
  accountable_sponsor: {}
  source_owner: {}
  controlled_location: {}
  version_or_source_period: {}
  checksum_or_pending: {}
  classification_access: {}
  reviewer_routing: {}
  provenance_limitations_non_approval: {}
  source_owner_confirmation:
    confirmer_name_or_office: ""
    confirmation_date: ""
    confirmation_method: ""
    limitations: ""
  knowledge_reviewer_precheck:
    reviewer_name_or_office: ""
    precheck_date: ""
    collection_readiness_comment: ""
    explicit_non_approval_decision: "not_approved"
    active_rag_index_allowed: false
```

## Scoring rule

```text
total_collection_groups = source_record_count * 10
closed_collection_groups = present_groups + accepted_not_applicable_groups
gap_collection_groups = pending_groups + missing_groups
DECISION_RIGHTS_READINESS_GAP_RATE = gap_collection_groups / total_collection_groups
```

Per-record collection readiness:

```text
collection_ready_for_precheck = true only when all 10 groups are closed
collection_ready_for_precheck != source_approved
collection_ready_for_precheck != review_pending
collection_ready_for_precheck != index_ready
collection_ready_for_precheck != indexed
```

## TEST scope for next stage

The next TEST stage should verify this packet without modifying `data/source_register/m1_source_register.yml`:

```text
FIELD_GROUP_COUNT = 10
ALLOWED_STATUS_SET_ENFORCED = true
ALL_FIVE_SEED_SOURCE_IDS_COVERED = true
SOURCE_ID_MATCHES_REGISTER_REQUIRED = true
PENDING_GROUPS_REQUIRE_ACCOUNTABLE_OWNER = true
PENDING_GROUPS_REQUIRE_NEXT_ACTION = true
CHECKSUM_PENDING_ALLOWED_WITH_REASON = true
RESTRICTED_SOURCE_HANDLING_PRESERVED = true
NON_APPROVAL_ASSERTION_REQUIRED = true
SOURCE_REGISTER_MODIFIED = false
SOURCE_APPROVAL_CLAIMED = false
SOURCE_INGESTION_CLAIMED = false
RAG_ACTIVATION_CLAIMED = false
```

## Fail-closed safety gates

This packet must fail closed if any of these occur:

1. Any source is marked approved from collection evidence alone.
2. Any source is marked ingested, parsed, embedded, indexed or active in RAG.
3. Any restricted source loosens access roles without review evidence.
4. Any person, office, source location, checksum or reviewer is invented.
5. Any `pending_with_accountable_owner` group lacks accountable owner and next action note.
6. Any missing field is hidden as `present`.
7. Any Personal / Staff Twin Memory or external research is promoted into Organizational Memory / Governed RAG without review.

## Build acceptance checks

```text
M1_B_BUILD_COMPLETED = true
COLLECTION_PACKET_TEMPLATE_ADDED = true
COLLECTION_PACKET_FIELD_GROUP_COUNT = 10
COLLECTION_PACKET_SCORING_RULE_ADDED = true
COLLECTION_PACKET_TEST_SCOPE_ADDED = true
NEXT_STAGE = TEST
SOURCE_REGISTER_MODIFIED = false
SOURCE_OWNER_EVIDENCE_COLLECTED = false
SOURCE_APPROVAL_CLAIMED = false
SOURCE_INGESTION_CLAIMED = false
RAG_ACTIVATION_CLAIMED = false
```
