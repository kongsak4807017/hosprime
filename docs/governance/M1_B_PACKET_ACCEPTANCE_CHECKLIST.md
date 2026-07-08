# M1-B Packet Acceptance Checklist

Status: controlled non-authorizing BUILD artifact

Release target: Milestone 1 — Governed Knowledge Oracle MVP

Controlling issue: #154

Build evidence:

- `engineering_runs/2026-07-08/0142-m1b-source-owner-evidence-packet-completion-build.md`

Planning evidence:

- `engineering_runs/2026-07-08/0141-m1b-source-owner-evidence-packet-completion-plan.md`
- `engineering_runs/2026-07-08/0140-m1b-source-owner-evidence-packet-completion-hypothesis.md`
- `docs/governance/M1_B_SOURCE_OWNER_PACKET_COMPLETION_WORKFLOW.md`
- `data/source_register/m1_source_register.yml`
- `README.md`

## 1. Purpose

This checklist gives future authorized operators a review-ready packet acceptance template for the five Milestone 1 seed source records.

It helps a data governance lead, source inventory operator, provincial program source owner, independent knowledge reviewer, and technical ingestion operator determine whether a source-owner evidence packet is structurally ready for later human review.

## 2. Non-authorization boundary

This checklist is not a source-owner evidence collection authorization, source approval form, ingestion ticket, active RAG permission, factual-answer permission, Organizational Memory promotion, user acceptance record, CI result, or real-world execution record.

Default-false controls:

```text
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
REAL_USER_ACCEPTANCE_CLAIMED = false
REAL_WORLD_EXECUTION_CLAIMED = false
```

Any future packet that conflicts with these controls must be marked blocked and must not be represented as review-ready.

## 3. Baseline retained

```text
SEED_RECORDS_COUNT = 5
FILLED_SOURCE_OWNER_PACKET_COUNT = 0 / 5
SOURCE_OWNER_PACKET_READINESS_RATE = 0%
AUTHORIZED_COLLECTION_ROUTE_COMPLETENESS_RATE = 0%
SOURCE_RECORDS_WITH_APPROVAL_STATUS_APPROVED = 0 / 5
SOURCE_RECORDS_WITH_ACTIVE_RAG_INDEX = 0 / 5
```

This checklist does not change the baseline. It creates a bounded structure for a later authorized packet-completion path.

## 4. Seed source linkage

A packet must link to exactly one seed `source_id` from `data/source_register/m1_source_register.yml`:

| Seed source_id | Knowledge pack | Owner role from register | Packet can become review-ready in this checklist? |
|---|---|---|---|
| `M1A-PM25-001` | PM2.5 and Environmental Health | Provincial public health environmental health lead | Only after all required receipts or pending reasons are present in a later authorized path |
| `M1A-TB-001` | Tuberculosis and Communicable Disease Control | Provincial TB program lead | Only after all required receipts or pending reasons are present in a later authorized path |
| `M1A-NCD-001` | NCD and Chronic Care Service Model | Provincial NCD program lead | Only after all required receipts or pending reasons are present in a later authorized path |
| `M1A-EOC-001` | Disaster, EOC and Public Health Emergency Operations | Provincial EOC or emergency response lead | Only after all required receipts or pending reasons are present in a later authorized path |
| `M1A-DIGITAL-001` | Digital Health, Data Governance and AI Workflow | Digital health or data governance lead | Only after all required receipts or pending reasons are present in a later authorized path |

## 5. Allowed packet field status values

Each packet field must use one of these status values:

```text
PRESENT_WITH_RECEIPT
PENDING_WITH_REASON
BLOCKED_WITH_REASON
BOUNDARY_VIOLATION
```

Definitions:

| Status | Meaning | Allowed next action |
|---|---|---|
| `PRESENT_WITH_RECEIPT` | The field has a traceable receipt generated through an authorized route. | Continue to the next field. |
| `PENDING_WITH_REASON` | The field is not available, but a reason is explicit and reviewable. | Continue only if the workflow allows pending evidence for that field. |
| `BLOCKED_WITH_REASON` | The packet cannot proceed because a required route, receipt, role, or handoff condition is missing. | Stop and record the accountable role and next executable step. |
| `BOUNDARY_VIOLATION` | The packet implies unauthorized evidence collection, named-person use, approval, ingestion, RAG activation, Organizational Memory promotion, CI success, user acceptance, factual-answer permission, or real-world execution. | Stop and correct before any reviewer handoff. |

## 6. Packet checklist

| Check | Required field | Acceptable evidence pattern | Responsible role | Pass condition | Fail-closed condition |
|---|---|---|---|---|---|
| 1 | Seed source linkage | `source_id` matches exactly one of the five seed records. | Source inventory operator | `SOURCE_ID_LINKED_TO_SEED_RECORD = true` | Source is ambiguous, duplicated, or outside the seed register. |
| 2 | Real work purpose | Purpose statement links the source to a real organizational work problem and M1 outcome. | Data governance lead | `SOURCE_PURPOSE_LINKED_TO_REAL_WORK_PROBLEM = true` | Purpose is generic, speculative, or added only for document volume. |
| 3 | Owner office or role | Owner office or owner role is present; person name is not required. | Provincial program source owner or data governance lead | `OWNER_OFFICE_OR_OWNER_ROLE_PRESENT = true` | Only an informal personal name is supplied without accountable role context. |
| 4 | Owner-person boundary | Named owner-person evidence is absent or has separate authorized assignment receipt. | Data governance lead | `OWNER_PERSON_BOUNDARY_RESPECTED = true` | Named person evidence appears without authorized assignment evidence. |
| 5 | Controlled location | Controlled file/system location receipt or pending-location reason. | Source inventory operator | `CONTROLLED_LOCATION_OR_PENDING_REASON_PRESENT = true` | Location is informal, personal-only, inaccessible, or unverifiable. |
| 6 | Version or source period | Version, source period, freshness receipt, or pending-version reason. | Provincial program source owner | `VERSION_OR_SOURCE_PERIOD_OR_PENDING_REASON_PRESENT = true` | Freshness/version is unknown with no pending reason. |
| 7 | Checksum/integrity | Checksum receipt with method, or checksum-pending reason where controlled access is not yet authorized. | Technical ingestion operator | `CHECKSUM_OR_CHECKSUM_PENDING_REASON_PRESENT = true` | Checksum is claimed without method, file access, or receipt. |
| 8 | Classification and access | Classification, access policy, and allowed roles are explicit. | Data governance lead | `CLASSIFICATION_AND_ACCESS_POLICY_PRESENT = true` | Access is missing, overbroad, or inconsistent with sensitivity. |
| 9 | Limitations/conflicts/sensitivity | Limitation, conflict, and sensitivity note receipt or explicit pending reason. | Independent knowledge reviewer with source-owner input | `LIMITATION_CONFLICT_SENSITIVITY_NOTES_PRESENT = true` | Notes are blank, minimized, or treated as approval evidence. |
| 10 | Review-ready handoff | Handoff receipt states packet is ready for independent review only. | Independent knowledge reviewer | `REVIEW_READY_HANDOFF_RECEIPT_PRESENT = true` | Review-ready status is represented as approval, ingestion permission, active RAG, or factual-answer permission. |

## 7. Reviewer handoff minimum

A future packet may be handed to an independent knowledge reviewer only when all of the following are true:

```text
SOURCE_ID_LINKED_TO_SEED_RECORD = true
SOURCE_PURPOSE_LINKED_TO_REAL_WORK_PROBLEM = true
OWNER_OFFICE_OR_OWNER_ROLE_PRESENT = true
OWNER_PERSON_BOUNDARY_RESPECTED = true
CONTROLLED_LOCATION_OR_PENDING_REASON_PRESENT = true
VERSION_OR_SOURCE_PERIOD_OR_PENDING_REASON_PRESENT = true
CHECKSUM_OR_CHECKSUM_PENDING_REASON_PRESENT = true
CLASSIFICATION_AND_ACCESS_POLICY_PRESENT = true
LIMITATION_CONFLICT_SENSITIVITY_NOTES_PRESENT = true
REVIEW_READY_HANDOFF_RECEIPT_PRESENT = true
APPROVAL_CLAIMED = false
RAG_ACTIVATION_CLAIMED = false
ORGANIZATIONAL_MEMORY_PROMOTION_CLAIMED = false
FACTUAL_ANSWER_PERMISSION_CLAIMED = false
REAL_WORLD_EXECUTION_CLAIMED = false
```

## 8. Blank packet row template

This example is intentionally blank and uses placeholders only. It must not be treated as collected evidence.

| Field | Value | Status | Receipt or pending/blocker reason | Accountable role | Reviewer note |
|---|---|---|---|---|---|
| `source_id` | `<one seed source_id>` | `<PRESENT_WITH_RECEIPT | BLOCKED_WITH_REASON>` | `<receipt id or blocker reason>` | `source_inventory_operator_role_only` | `<note>` |
| `real_work_purpose` | `<purpose linked to M1 work problem>` | `<PRESENT_WITH_RECEIPT | BLOCKED_WITH_REASON>` | `<receipt id or blocker reason>` | `data_governance_lead_role_only` | `<note>` |
| `owner_office_or_role` | `<office or role only>` | `<PRESENT_WITH_RECEIPT | BLOCKED_WITH_REASON>` | `<receipt id or blocker reason>` | `provincial_program_source_owner_role_only` | `<note>` |
| `owner_person_assignment` | `<absent by default or authorized assignment receipt>` | `<PENDING_WITH_REASON | PRESENT_WITH_RECEIPT | BOUNDARY_VIOLATION>` | `<pending reason, receipt id, or violation reason>` | `data_governance_lead_role_only` | `<note>` |
| `controlled_location` | `<controlled path/system or pending>` | `<PRESENT_WITH_RECEIPT | PENDING_WITH_REASON | BLOCKED_WITH_REASON>` | `<receipt id, pending reason, or blocker reason>` | `source_inventory_operator_role_only` | `<note>` |
| `version_or_source_period` | `<version/source period or pending>` | `<PRESENT_WITH_RECEIPT | PENDING_WITH_REASON | BLOCKED_WITH_REASON>` | `<receipt id, pending reason, or blocker reason>` | `provincial_program_source_owner_role_only` | `<note>` |
| `checksum_or_integrity` | `<checksum/method or pending>` | `<PRESENT_WITH_RECEIPT | PENDING_WITH_REASON | BLOCKED_WITH_REASON>` | `<receipt id, pending reason, or blocker reason>` | `technical_ingestion_operator_role_only` | `<note>` |
| `classification_access_policy` | `<classification + access roles>` | `<PRESENT_WITH_RECEIPT | BLOCKED_WITH_REASON>` | `<receipt id or blocker reason>` | `data_governance_lead_role_only` | `<note>` |
| `limitations_conflicts_sensitivity` | `<notes or pending reason>` | `<PRESENT_WITH_RECEIPT | PENDING_WITH_REASON | BLOCKED_WITH_REASON>` | `<receipt id, pending reason, or blocker reason>` | `independent_knowledge_reviewer_role_only` | `<note>` |
| `review_ready_handoff` | `<review-ready only, not approval>` | `<PRESENT_WITH_RECEIPT | BLOCKED_WITH_REASON | BOUNDARY_VIOLATION>` | `<receipt id, blocker reason, or violation reason>` | `independent_knowledge_reviewer_role_only` | `<note>` |

## 9. False-claim guardrails

A future packet fails this checklist if it states or implies any of the following without separate authorized records:

```text
approved source
approved Organizational Memory
active RAG source
factual answer source
executed organizational action
accepted user output
passed CI
completed real-world task
```

The only allowed positive result from this checklist is:

```text
PACKET_STRUCTURALLY_REVIEW_READY = true
```

Even then, approval, ingestion, indexing, activation, factual use, and Organizational Memory promotion remain separate stages.

## 10. Memory-layer boundary

Checklist artifacts, blank templates, and later unreviewed packet drafts remain engineering-run evidence or packet working files. They do not become Organizational Memory or Governed RAG evidence unless a later reviewed promotion record exists.

```text
Personal / Staff Twin Memory = not affected
Person Memory = not affected
Role Memory = not affected
Research Staging = not promoted
Organizational Memory / Governed RAG = not affected
```

## 11. TEST-stage acceptance criteria

The next TEST stage should verify this checklist against the planned BUILD criteria:

```text
M1_B_PACKET_ACCEPTANCE_CHECKLIST_CREATED = true
CHECKLIST_IS_NON_AUTHORIZING = true
CHECKLIST_HAS_SEED_SOURCE_ID_LINKAGE = true
CHECKLIST_HAS_RECEIPT_OR_PENDING_REASON_FIELDS = true
CHECKLIST_HAS_FAIL_CLOSED_RULES = true
CHECKLIST_HAS_FALSE_CLAIM_GUARDRAILS = true
CHECKLIST_HAS_TEST_STAGE_ACCEPTANCE_CRITERIA = true
SOURCE_REGISTER_MODIFIED = false
SOURCE_OWNER_EVIDENCE_COLLECTED = false
SOURCE_APPROVAL_CLAIMED = false
RAG_ACTIVATION_CLAIMED = false
ORGANIZATIONAL_MEMORY_PROMOTION_CLAIMED = false
```

## 12. BUILD acceptance status

```text
CURRENT_STAGE = BUILD
M1_B_PACKET_ACCEPTANCE_CHECKLIST_CREATED = true
CHECKLIST_IS_NON_AUTHORIZING = true
CHECKLIST_HAS_SEED_SOURCE_ID_LINKAGE = true
CHECKLIST_HAS_RECEIPT_OR_PENDING_REASON_FIELDS = true
CHECKLIST_HAS_FAIL_CLOSED_RULES = true
CHECKLIST_HAS_FALSE_CLAIM_GUARDRAILS = true
CHECKLIST_HAS_TEST_STAGE_ACCEPTANCE_CRITERIA = true
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
REAL_USER_ACCEPTANCE_CLAIMED = false
REAL_WORLD_EXECUTION_CLAIMED = false
NEXT_STAGE = TEST
```
