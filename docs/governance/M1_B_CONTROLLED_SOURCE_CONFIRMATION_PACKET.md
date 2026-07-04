# M1-B Controlled Source Confirmation Packet

Status: controlled release artifact / inventory-confirmation only / role-assignment evidence section added / non-authoritative for source approval  
Release target: Milestone 1 — Governed Knowledge Oracle MVP  
Parent issue: #10  
Build control issue: #40  
Test control issue: #41  
Evaluate control issue: #42  
Review control issue: #43  
Release control issue: #44  
Role-assignment plan issue: #54  
Role-assignment build issue: #55  
Previous stage: PLAN (#54)  
Current stage: BUILD  
Next stage: TEST

## Controlled release decision

This packet is released only as a controlled source-inventory and role-assignment evidence artifact.

It may be used by a source owner, accountable office, source inventory operator, data governance lead or knowledge reviewer to collect inventory-readiness and role-assignment readiness evidence for the five M1 seed source records.

It must not be used as evidence that any source is approved, authoritative, ingested, parsed, embedded, indexed, retrievable, answerable or promoted into Organizational Memory / Governed RAG.

```text
ROLE_ASSIGNMENT_PACKET_BUILD_COMPLETED = true
ROLE_ASSIGNMENT_EVIDENCE_SECTION_ADDED = true
ROLE_ASSIGNMENT_FIELD_GROUP_COUNT = 5
CONTROLLED_RELEASE_SCOPE = inventory_confirmation_and_role_assignment_evidence_only
SOURCE_OWNER_EVIDENCE_COLLECTED = false
SOURCE_REGISTER_MODIFIED = false
SOURCE_APPROVAL_CLAIMED = false
SOURCE_INGESTION_CLAIMED = false
SOURCE_PARSING_CLAIMED = false
SOURCE_EMBEDDING_CLAIMED = false
SOURCE_INDEXING_CLAIMED = false
RAG_ACTIVATION_CLAIMED = false
FACTUAL_ANSWER_PERMISSION_CLAIMED = false
ORGANIZATIONAL_MEMORY_PROMOTION_CLAIMED = false
```

## Purpose

This packet gives source owners and knowledge reviewers a controlled way to confirm whether each placeholder source record has enough inventory evidence and role-assignment evidence to proceed toward later review planning.

It supports the HosPrime North Star by improving evidence quality, user trust, decision-to-outcome traceability, knowledge reuse and zero unauthorized high-impact action.

## Non-approval boundary

This packet is **inventory-readiness and role-assignment readiness evidence only**.

Completing this packet does **not** mean that a source is approved, authoritative, ingested, parsed, embedded, indexed, retrievable, answerable or promoted into Organizational Memory / Governed RAG.

A source remains excluded from active retrieval unless a later authorized review records source approval, access decision, quality decision, indexing readiness and release evidence.

## Real user / real problem

Real users:

- public-health executive;
- provincial program owner;
- data governance lead;
- knowledge reviewer;
- source inventory operator.

Real work problem:

The M1 source register has five placeholder source records, but none is fully confirmed for controlled source inventory or role assignment. Users need a structured packet to close missing ownership, location, version, checksum, classification, reviewer, authority-basis and provenance gaps without accidentally authorizing source use.

## Baseline inherited from M1-B baseline and role-assignment plan

```text
TOTAL_SOURCE_RECORDS = 5
TOTAL_CONFIRMATION_CELLS = 50
PRESENT_CELLS = 15 / 50 = 30%
PENDING_CELLS = 15 / 50 = 30%
MISSING_CELLS = 20 / 50 = 40%
BASELINE_CONFIRMATION_GAP_RATE = 35 / 50 pending_or_missing_cells = 70%
FULLY_CONFIRMED_RECORDS = 0 / 5
ROLE_READINESS_GAP_RATE = 54.3%
FULLY_ROLE_READY_RECORDS = 0 / 5
```

## Target after a later filled packet is reviewed

```text
TARGET_CONFIRMATION_GAP_RATE_AFTER_PACKET <= 15 / 50 = <= 30%
TARGET_FULLY_CONFIRMED_RECORDS >= 3 / 5
TARGET_ROLE_READINESS_GAP_RATE_AFTER_LATER_COLLECTION_PACKET <= 30%
SOURCE_APPROVAL_CLAIMED = false
SOURCE_INGESTION_CLAIMED = false
RAG_ACTIVATION_CLAIMED = false
```

The BUILD stage publishes the role-assignment evidence section only. It does not claim the target has been achieved.

## Confirmation cell statuses

Use exactly one status for each confirmation or role-assignment cell:

```text
present
pending_with_accountable_owner
missing
not_applicable_with_rationale
```

Status rules:

- `present` means a specific value, accountable office/person, controlled reference or verification method is recorded.
- `pending_with_accountable_owner` means a reason, accountable owner and next follow-up action are recorded.
- `missing` means no specific value, accountable pending reason or follow-up owner is recorded.
- `not_applicable_with_rationale` may be used only when a reviewer records why the field does not apply for this source type.

For metric calculation, `present` and `not_applicable_with_rationale` count as closed cells. `pending_with_accountable_owner` and `missing` count as gap cells unless a later approved test rule explicitly accepts accountable pending status for inventory or role-assignment readiness.

## Minimum confirmation packet fields

Each source record must be checked against ten inventory confirmation cells.

| # | Field | Required evidence | Status | Notes |
|---|---|---|---|---|
| 1 | `source_id` | Existing source-register ID being confirmed |  | Must match `data/source_register/m1_source_register.yml` |
| 2 | `accountable_owner_or_office` | Named owner person or accountable office |  | No invented owners |
| 3 | `controlled_location_type` | File repository, document management system, official drive folder, approved system, physical archive or other controlled location class |  | Avoid public-link assumptions |
| 4 | `controlled_location_reference` | Controlled path, system identifier or archive reference |  | May be internal/non-public |
| 5 | `version_or_effective_date` | Version, effective date, approval date or currentness statement |  | Must support freshness review |
| 6 | `checksum_status` | Checksum value, checksum pending reason or non-file verification method |  | Do not fabricate checksum |
| 7 | `classification_and_access_policy_confirmed` | Confirmation that classification and role-scoped access policy are correct or need correction |  | Must preserve access-control boundary |
| 8 | `reviewer_assignment` | Reviewer role plus named reviewer or reviewing office |  | Must be human/accountable review boundary |
| 9 | `provenance_confirmation` | Confirmation method, confirmer and confirmation date |  | Records how inventory evidence was obtained |
| 10 | `limitation_or_replacement_note` | Known limitations, superseded source relationship or replacement note |  | Required even when no limitation is known |

## Role-assignment evidence section

This section is separate from the ten inventory confirmation cells. It is designed to make source-owner, reviewer and decision-scope readiness measurable before any later source review.

Role-assignment evidence does **not** confer source authority, source approval, ingestion permission, indexing permission, retrieval activation or permission to answer factual questions from the source.

Each source record should be checked against five role-assignment field groups.

### 1. Authority basis and decision scope

Purpose: prove why the named person or office can act as source owner or accountable office for inventory confirmation only.

```yaml
authority_basis:
  status: ""
  authority_type: ""
  authority_reference: ""
  decision_scope: "inventory_confirmation_only"
  approval_boundary_acknowledged: true
  evidence_note: ""
  accountable_owner_for_pending: ""
```

Required controls:

- `decision_scope` must remain `inventory_confirmation_only` unless a later reviewed governance decision explicitly changes scope.
- `approval_boundary_acknowledged` must remain `true`.
- A named role or office is not enough by itself; the evidence note must explain the authority basis or the accountable pending reason.

### 2. Named human or approved office assignment mapped to source ID

Purpose: identify a real accountable person or approved office without inventing names or authority.

```yaml
source_owner_assignment:
  status: ""
  source_id: ""
  assigned_person_or_office: ""
  assignment_method: ""
  assignment_date: ""
  assigned_by: ""
  assignment_limitations: ""
  evidence_note: ""
  accountable_owner_for_pending: ""
```

Required controls:

- `source_id` must match an existing source-register record.
- `assigned_person_or_office` must not be fabricated.
- `assignment_limitations` must record restrictions, uncertainty or gaps even when the assignment is otherwise present.

### 3. Independent reviewer routing by gate

Purpose: define who checks the role assignment before any later source review proceeds.

```yaml
independent_reviewer_routing:
  status: ""
  reviewer_person_or_office: ""
  reviewer_role: ""
  review_gate: "role_assignment_precheck"
  conflict_of_interest_check: ""
  escalation_path: ""
  evidence_note: ""
  accountable_owner_for_pending: ""
```

Required controls:

- `review_gate` must remain `role_assignment_precheck` for this packet.
- Reviewer routing does not equal source quality review or source approval.
- A conflict-of-interest check or pending owner must be recorded before later review planning.

### 4. Access/classification confirmation with restricted-source handling

Purpose: confirm that role assignment does not weaken classification or bypass restricted-source access controls.

```yaml
access_classification_role_check:
  status: ""
  classification_confirmed_or_disputed: ""
  access_policy_confirmed_or_disputed: ""
  restricted_source_handling_required: false
  permitted_roles_confirmed: []
  access_boundary_note: ""
  evidence_note: ""
  accountable_owner_for_pending: ""
```

Required controls:

- Restricted/internal sources must remain restricted unless a later authorized access review changes policy.
- `permitted_roles_confirmed` must not add roles that are absent from the approved source register without a later review record.
- Any dispute must be treated as a blocker for approval, ingestion, indexing and retrieval activation.

### 5. Provenance, version/freshness and no-execution boundary acknowledgement

Purpose: keep role assignment evidence traceable and prevent claims of source approval or real-world execution.

```yaml
role_assignment_provenance:
  status: ""
  evidence_collected_by: ""
  evidence_collection_date: ""
  evidence_collection_method: ""
  version_or_effective_date_checked: ""
  no_execution_boundary_acknowledged: true
  no_source_approval_boundary_acknowledged: true
  evidence_note: ""
  accountable_owner_for_pending: ""
```

Required controls:

- `no_execution_boundary_acknowledged` must remain `true`.
- `no_source_approval_boundary_acknowledged` must remain `true`.
- Provenance confirms how role-assignment evidence was collected; it does not confirm the source content itself is authoritative.

## Per-source packet template

Copy one block per source record.

```yaml
source_confirmation_packet:
  source_id: ""
  knowledge_pack: ""
  source_title: ""
  packet_status: draft_inventory_and_role_assignment_confirmation_only
  non_approval_boundary_acknowledged: true
  confirmation_cells:
    source_id:
      status: ""
      value: ""
      evidence_note: ""
      accountable_owner_for_pending: ""
    accountable_owner_or_office:
      status: ""
      value: ""
      evidence_note: ""
      accountable_owner_for_pending: ""
    controlled_location_type:
      status: ""
      value: ""
      evidence_note: ""
      accountable_owner_for_pending: ""
    controlled_location_reference:
      status: ""
      value: ""
      evidence_note: ""
      accountable_owner_for_pending: ""
    version_or_effective_date:
      status: ""
      value: ""
      evidence_note: ""
      accountable_owner_for_pending: ""
    checksum_status:
      status: ""
      value: ""
      evidence_note: ""
      accountable_owner_for_pending: ""
    classification_and_access_policy_confirmed:
      status: ""
      value: ""
      evidence_note: ""
      accountable_owner_for_pending: ""
    reviewer_assignment:
      status: ""
      value: ""
      evidence_note: ""
      accountable_owner_for_pending: ""
    provenance_confirmation:
      status: ""
      value: ""
      evidence_note: ""
      accountable_owner_for_pending: ""
    limitation_or_replacement_note:
      status: ""
      value: ""
      evidence_note: ""
      accountable_owner_for_pending: ""
  role_assignment_evidence:
    authority_basis:
      status: ""
      authority_type: ""
      authority_reference: ""
      decision_scope: "inventory_confirmation_only"
      approval_boundary_acknowledged: true
      evidence_note: ""
      accountable_owner_for_pending: ""
    source_owner_assignment:
      status: ""
      source_id: ""
      assigned_person_or_office: ""
      assignment_method: ""
      assignment_date: ""
      assigned_by: ""
      assignment_limitations: ""
      evidence_note: ""
      accountable_owner_for_pending: ""
    independent_reviewer_routing:
      status: ""
      reviewer_person_or_office: ""
      reviewer_role: ""
      review_gate: "role_assignment_precheck"
      conflict_of_interest_check: ""
      escalation_path: ""
      evidence_note: ""
      accountable_owner_for_pending: ""
    access_classification_role_check:
      status: ""
      classification_confirmed_or_disputed: ""
      access_policy_confirmed_or_disputed: ""
      restricted_source_handling_required: false
      permitted_roles_confirmed: []
      access_boundary_note: ""
      evidence_note: ""
      accountable_owner_for_pending: ""
    role_assignment_provenance:
      status: ""
      evidence_collected_by: ""
      evidence_collection_date: ""
      evidence_collection_method: ""
      version_or_effective_date_checked: ""
      no_execution_boundary_acknowledged: true
      no_source_approval_boundary_acknowledged: true
      evidence_note: ""
      accountable_owner_for_pending: ""
  source_owner_confirmation:
    confirmer_name_or_office: ""
    confirmation_date: ""
    confirmation_method: ""
    limitations: ""
  knowledge_reviewer_precheck:
    reviewer_name_or_office: ""
    precheck_date: ""
    inventory_readiness_comment: ""
    role_assignment_readiness_comment: ""
    explicit_non_approval_decision: "not_approved"
    active_rag_index_allowed: false
```

## Measurement method

For an inventory packet batch:

```text
total_confirmation_cells = source_record_count * 10
closed_cells = present_cells + not_applicable_with_rationale_cells
gap_cells = pending_with_accountable_owner_cells + missing_cells
gap_rate = gap_cells / total_confirmation_cells
```

For a role-assignment packet batch:

```text
total_role_assignment_field_groups = source_record_count * 5
role_assignment_ready_groups = groups_with_present_or_not_applicable_with_rationale_status
role_assignment_gap_groups = groups_with_pending_with_accountable_owner_or_missing_status
role_readiness_gap_rate = role_assignment_gap_groups / total_role_assignment_field_groups
```

A source is `fully_confirmed_for_inventory` only when all ten inventory cells are either:

- `present`, or
- `not_applicable_with_rationale` with a documented reason accepted by the reviewer.

A source is `role_assignment_ready_for_precheck` only when all five role-assignment field groups are either:

- `present`, or
- `not_applicable_with_rationale` with a documented reason accepted by the reviewer.

These statuses are still **not source approval**.

## Source owner checklist

Before submitting a filled packet, the source owner or accountable office must verify:

- the controlled source location is identifiable;
- the source version or effective date is recorded;
- any checksum gap has a documented reason;
- classification and access policy are not weakened;
- authority basis and decision scope are recorded for inventory confirmation only;
- named source-owner assignment is mapped to the source ID or has an accountable pending owner;
- independent reviewer routing is recorded before any later source review;
- role-assignment provenance and no-execution boundary are acknowledged;
- known limitations, superseded records or replacement candidates are listed;
- no statement claims approval, ingestion, indexing, retrieval activation or answer authority.

## Knowledge reviewer checklist

Before accepting the packet for later TEST/EVALUATE stages, the reviewer must verify:

- all ten inventory confirmation cells use allowed statuses;
- all five role-assignment field groups exist and use allowed statuses;
- pending cells include accountable owners and next action notes;
- missing cells are not hidden as present;
- role assignment is separated from source approval and source authority;
- personal/staff memory and external research are not promoted into Organizational RAG;
- all records remain `approval_status: not_approved`;
- all records remain `active_rag_index: false`.

## Explicit prohibited claims

Do not make any of these claims from this packet alone:

```text
SOURCE_APPROVED = true
SOURCE_INGESTED = true
SOURCE_PARSED = true
SOURCE_EMBEDDED = true
SOURCE_INDEXED = true
ACTIVE_RAG_INDEX = true
FACTUAL_ANSWER_PERMISSION = true
ORGANIZATIONAL_MEMORY_PROMOTION = true
REAL_WORLD_ACTION_EXECUTED = true
```

## Build acceptance checks

```text
ROLE_ASSIGNMENT_PACKET_BUILD_COMPLETED = true
ROLE_ASSIGNMENT_EVIDENCE_SECTION_ADDED = true
ROLE_ASSIGNMENT_FIELD_GROUP_COUNT = 5
SOURCE_REGISTER_MODIFIED = false
SOURCE_OWNER_EVIDENCE_COLLECTED = false
SOURCE_APPROVAL_CLAIMED = false
SOURCE_INGESTION_CLAIMED = false
RAG_ACTIVATION_CLAIMED = false
```
