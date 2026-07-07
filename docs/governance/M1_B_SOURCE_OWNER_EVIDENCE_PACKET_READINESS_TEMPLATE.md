# M1-B Source-Owner Evidence Packet Readiness Template

Status: RELEASED CONTROLLED GUIDANCE ONLY
Release target: Milestone 1 — Governed Knowledge Oracle MVP
Register linkage: `data/source_register/m1_source_register.yml`
Controlling issue: #134
Build evidence: `engineering_runs/2026-07-07/0112-m1b-source-owner-evidence-packet-readiness-build.md`
Test evidence: `engineering_runs/2026-07-07/0113-m1b-source-owner-evidence-packet-readiness-test.md`
Evaluate evidence: `engineering_runs/2026-07-07/0114-m1b-source-owner-evidence-packet-readiness-evaluate.md`
Review evidence: `engineering_runs/2026-07-07/0115-m1b-source-owner-evidence-packet-readiness-review.md`
Release scope: controlled readiness guidance only

## 1. Purpose

This template gives source inventory and governance operators one consistent way to prepare a source-owner evidence packet for each M1 seed source record.

It exists to reduce ambiguity before any later source-owner evidence collection, human review, approval decision, ingestion, parsing, embedding, indexing, active RAG activation or Organizational Memory promotion.

## 2. Non-authorization boundary

Completing or releasing this template does **not** authorize any of the following:

```text
source_approved = false
source_ingested = false
source_parsed = false
source_embedded = false
source_indexed = false
active_rag_enabled = false
organizational_memory_promoted = false
factual_answer_allowed = false
real_world_action_completed = false
ci_passed = false
```

This is a readiness template only. It is not a review record, approval record, access-control grant, ingestion job, retrieval activation record, factual-answer permission, or execution receipt.

## 3. Intended real users

- Public-health executive sponsor: confirms that later evidence collection supports a real governance need.
- Data governance lead: confirms routing, classification, access policy and review boundary.
- Provincial program source owner: later confirms custody, version, source period and limitations through an authorized evidence process.
- Source inventory operator: prepares packet fields and records pending reasons.
- Independent knowledge reviewer: later reviews evidence and limitations before promotion decisions.
- Technical ingestion operator: uses only reviewed/approved records in a later stage; this template does not authorize ingestion.

## 4. Applicable seed records

This template is applicable to the five current M1 seed records without modifying the source register:

```text
M1A-PM25-001
M1A-TB-001
M1A-NCD-001
M1A-EOC-001
M1A-DIGITAL-001
```

Current observed register baseline:

```text
SEED_RECORDS_COUNT = 5
FILLED_SOURCE_OWNER_PACKET_COUNT = 0 / 5
SOURCE_OWNER_PACKET_READINESS_RATE = 0%
LIFECYCLE_STATE = DISCOVERED
REVIEW_STATUS = not_reviewed
APPROVAL_STATUS = not_approved
ACTIVE_RAG_INDEX = false
```

## 5. Source-register linkage rules

For each packet:

1. Link to exactly one `source_id` in `data/source_register/m1_source_register.yml`.
2. Do not edit the source register while completing this template.
3. Use pending reasons instead of invented evidence.
4. Keep owner role separate from named owner-person evidence.
5. Keep packet readiness separate from source approval.
6. Keep reviewer precheck routing separate from review completion.
7. Keep checksum-pending reason separate from checksum verification.
8. Keep limitations visible until reviewed.

## 6. Packet template

Copy this block once per source record when a later authorized packet-preparation stage exists.

```yaml
packet_id: pending_packet_id
packet_status: readiness_draft_only
linked_register_path: data/source_register/m1_source_register.yml
linked_source_id: pending_source_id
control_issue: pending_issue_number
prepared_by_role: pending_role
prepared_date: pending_date

source_identity:
  source_id: pending_source_id
  knowledge_pack: pending_from_register
  source_title: pending_from_register
  source_type: pending_from_register
  linked_register_path: data/source_register/m1_source_register.yml
  safe_fail_condition: missing_source_identity

organization_scope:
  organization_name_or_pending_reason: pending_source_owner_confirmation
  organization_scope_type: pending_scope_type
  jurisdiction_or_service_scope: pending_scope
  safe_fail_condition: missing_organization_scope

accountable_sponsor:
  accountable_sponsor_role: pending_role
  sponsor_evidence_status: pending_or_not_collected
  sponsor_pending_reason_if_any: pending_reason
  safe_fail_condition: missing_accountable_sponsor_role_or_pending_reason

source_owner:
  source_owner_role: pending_role_from_register
  source_owner_person_status: pending_human_assignment
  owner_person_evidence_reference_or_pending_reason: pending_reason
  safe_fail_condition: missing_source_owner_role_or_pending_reason

controlled_location:
  controlled_file_or_system_location: pending_inventory
  location_status: pending_or_not_collected
  location_pending_reason_if_any: pending_reason
  safe_fail_condition: missing_controlled_location_or_pending_reason

version_or_source_period:
  version_label_or_source_period: pending_inventory
  source_date_or_period: pending_source_period
  version_pending_reason_if_any: pending_reason
  safe_fail_condition: missing_version_or_source_period_or_pending_reason

checksum_or_checksum_pending_reason:
  checksum_status: pending_checksum
  checksum_value_if_available: null
  checksum_pending_reason_if_any: original_controlled_file_not_yet_inventoried
  safe_fail_condition: missing_checksum_or_checksum_pending_reason

classification_and_access:
  classification: pending_from_register
  access_policy: pending_from_register
  allowed_roles: []
  sensitive_context_notes: pending_notes
  safe_fail_condition: missing_classification_and_access_policy

reviewer_precheck_routing:
  reviewer_role_required: pending_role
  reviewer_assignment_status: pending_human_reviewer
  review_route_notes: pending_notes
  safe_fail_condition: missing_reviewer_precheck_routing

provenance_and_limitations:
  provenance_summary: pending_summary
  known_limitations: pending_limitations
  conflict_or_supersession_notes: pending_notes
  not_for_factual_answer_until_reviewed_acknowledgement: true
  safe_fail_condition: missing_provenance_or_limitation_note

boundary_acknowledgements:
  source_identity_not_source_custody: true
  owner_role_not_named_owner_person_evidence: true
  packet_completion_not_source_approval: true
  source_approval_not_ingestion_permission: true
  ingestion_readiness_not_active_rag_activation: true
  active_rag_activation_not_organizational_memory_promotion: true
  pending_evidence_not_reviewed_evidence: true
  source_limitations_not_factual_answer_permission: true

memory_layer_boundary:
  current_layer: Research Staging
  organizational_memory_promotion: false
  active_rag_promotion: false
  personal_memory_affected: false
  role_memory_affected: false

prohibited_claims:
  source_approved: false
  source_ingested: false
  source_parsed: false
  source_embedded: false
  source_indexed: false
  active_rag_enabled: false
  organizational_memory_promoted: false
  factual_answer_allowed: false
  real_world_action_completed: false
  ci_passed: false
```

## 7. Ten minimum field groups

The packet is incomplete unless all ten field groups exist.

```text
FIELD_GROUP_01 = source_identity
FIELD_GROUP_02 = organization_scope
FIELD_GROUP_03 = accountable_sponsor
FIELD_GROUP_04 = source_owner
FIELD_GROUP_05 = controlled_location
FIELD_GROUP_06 = version_or_source_period
FIELD_GROUP_07 = checksum_or_checksum_pending_reason
FIELD_GROUP_08 = classification_and_access
FIELD_GROUP_09 = reviewer_precheck_routing
FIELD_GROUP_10 = provenance_and_limitations
```

## 8. Eight ambiguity boundary acknowledgements

The packet is unsafe if any acknowledgement is missing or false.

```text
BOUNDARY_01 = source_identity != source_custody
BOUNDARY_02 = owner_role != named_owner_person_evidence
BOUNDARY_03 = packet_completion != source_approval
BOUNDARY_04 = source_approval != ingestion_permission
BOUNDARY_05 = ingestion_readiness != active_rag_activation
BOUNDARY_06 = active_rag_activation != organizational_memory_promotion
BOUNDARY_07 = pending_evidence != reviewed_evidence
BOUNDARY_08 = source_limitations != factual_answer_permission
```

## 9. Safe-fail checklist

A packet must fail readiness if any of these conditions are present:

```text
missing_source_identity
missing_organization_scope
missing_accountable_sponsor_role_or_pending_reason
missing_source_owner_role_or_pending_reason
missing_controlled_location_or_pending_reason
missing_version_or_source_period_or_pending_reason
missing_checksum_or_checksum_pending_reason
missing_classification_and_access_policy
missing_reviewer_precheck_routing
missing_provenance_or_limitation_note
missing_non_approval_boundary_acknowledgement
missing_memory_layer_boundary
```

A packet must also fail if it asserts any prohibited claim as true:

```text
source_approved
source_ingested
source_parsed
source_embedded
source_indexed
active_rag_enabled
organizational_memory_promoted
factual_answer_allowed
real_world_action_completed
ci_passed
```

## 10. Memory-layer separation

```text
CURRENT_LAYER = Research Staging
ORGANIZATIONAL_MEMORY_PROMOTION = false
ACTIVE_RAG_PROMOTION = false
PERSONAL_MEMORY_AFFECTED = false
ROLE_MEMORY_AFFECTED = false
```

External findings, packet drafts and pending owner information remain in Research Staging or issue evidence until reviewed. They must not be treated as approved Organizational Memory, Role Memory, Personal Memory, or active Governed RAG content.

## 11. Release acceptance outputs

```text
M1_B_RELEASE_COMPLETED = true
TEMPLATE_STATUS = RELEASED CONTROLLED GUIDANCE ONLY
RELEASE_SCOPE = controlled_readiness_guidance_only
SOURCE_REGISTER_MODIFIED = false
SOURCE_OWNER_EVIDENCE_COLLECTED = false
SOURCE_OWNER_PERSON_NAMED = false
SOURCE_APPROVAL_CLAIMED = false
SOURCE_INGESTION_CLAIMED = false
SOURCE_PARSING_CLAIMED = false
SOURCE_EMBEDDING_CLAIMED = false
SOURCE_INDEXING_CLAIMED = false
RAG_ACTIVATION_CLAIMED = false
ORGANIZATIONAL_MEMORY_PROMOTION_CLAIMED = false
FACTUAL_ANSWER_PERMISSION_CLAIMED = false
CI_PASS_CLAIMED = false
REAL_WORLD_EXECUTION_CLAIMED = false
```

## 12. Explicit limitations

- This template does not collect real source-owner evidence.
- This template does not identify named owner persons.
- This template does not approve source records.
- This template does not grant ingestion, parsing, embedding, indexing or retrieval activation permission.
- This template does not permit factual answers from the five seed records.
- This template does not claim CI success.
- This template does not claim real-world execution.
