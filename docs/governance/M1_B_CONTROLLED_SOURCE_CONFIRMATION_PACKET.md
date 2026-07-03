# M1-B Controlled Source Confirmation Packet

Status: build artifact / non-authoritative template  
Release target: Milestone 1 — Governed Knowledge Oracle MVP  
Parent issue: #10  
Build control issue: #40  
Previous stage: PLAN (#39)  
Next stage: TEST

## Purpose

This packet gives source owners and knowledge reviewers a controlled way to confirm whether each placeholder source record has enough inventory evidence to proceed toward later review planning.

It supports the HosPrime North Star by improving evidence quality, user trust, decision-to-outcome traceability, knowledge reuse and zero unauthorized high-impact action.

## Non-approval boundary

This packet is **inventory-readiness evidence only**.

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

The M1 source register has five placeholder source records, but none is fully confirmed for controlled source inventory. Users need a structured packet to close missing ownership, location, version, checksum, classification, reviewer and provenance gaps without accidentally authorizing source use.

## Baseline inherited from M1-B baseline and plan

```text
TOTAL_SOURCE_RECORDS = 5
TOTAL_CONFIRMATION_CELLS = 50
PRESENT_CELLS = 15 / 50 = 30%
PENDING_CELLS = 15 / 50 = 30%
MISSING_CELLS = 20 / 50 = 40%
BASELINE_GAP_RATE = 35 / 50 pending_or_missing_cells = 70%
FULLY_CONFIRMED_RECORDS = 0 / 5
```

## Target after a later filled packet is reviewed

```text
TARGET_GAP_RATE_AFTER_PACKET <= 15 / 50 = <= 30%
TARGET_FULLY_CONFIRMED_RECORDS >= 3 / 5
SOURCE_APPROVAL_CLAIMED = false
SOURCE_INGESTION_CLAIMED = false
RAG_ACTIVATION_CLAIMED = false
```

The BUILD stage creates this template only. It does not claim the target has been achieved.

## Confirmation cell statuses

Use exactly one status for each confirmation cell:

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

For metric calculation, `present` and `not_applicable_with_rationale` count as closed cells. `pending_with_accountable_owner` and `missing` count as gap cells unless a later approved test rule explicitly accepts accountable pending status for inventory readiness.

## Minimum confirmation packet fields

Each source record must be checked against ten confirmation cells.

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

## Per-source packet template

Copy one block per source record.

```yaml
source_confirmation_packet:
  source_id: ""
  knowledge_pack: ""
  source_title: ""
  packet_status: draft_inventory_confirmation_only
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
  source_owner_confirmation:
    confirmer_name_or_office: ""
    confirmation_date: ""
    confirmation_method: ""
    limitations: ""
  knowledge_reviewer_precheck:
    reviewer_name_or_office: ""
    precheck_date: ""
    inventory_readiness_comment: ""
    explicit_non_approval_decision: "not_approved"
    active_rag_index_allowed: false
```

## Measurement method

For a packet batch:

```text
total_confirmation_cells = source_record_count * 10
closed_cells = present_cells + not_applicable_with_rationale_cells
gap_cells = pending_with_accountable_owner_cells + missing_cells
gap_rate = gap_cells / total_confirmation_cells
```

A source is `fully_confirmed_for_inventory` only when all ten cells are either:

- `present`, or
- `not_applicable_with_rationale` with a documented reason accepted by the reviewer.

This status is still **not source approval**.

## Source owner checklist

Before submitting a filled packet, the source owner or accountable office must verify:

- the controlled source location is identifiable;
- the source version or effective date is recorded;
- any checksum gap has a documented reason;
- classification and access policy are not weakened;
- known limitations, superseded records or replacement candidates are listed;
- no statement claims approval, ingestion, indexing, retrieval activation or answer authority.

## Knowledge reviewer checklist

Before accepting the packet for later TEST/EVALUATE stages, the reviewer must verify:

- all ten confirmation cells use allowed statuses;
- pending cells include accountable owners and next action notes;
- missing cells are not hidden as present;
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
```

## Next stage acceptance tests

The next TEST stage should validate:

```text
CONFIRMATION_PACKET_TEMPLATE_CREATED = true
MINIMUM_CONFIRMATION_PACKET_FIELDS_PRESENT = true
MEASUREMENT_METHOD_DEFINED = true
NON_APPROVAL_BOUNDARY_DEFINED = true
SOURCE_REGISTER_APPROVAL_STATUS_UNCHANGED = true
SOURCE_REGISTER_ACTIVE_RAG_INDEX_UNCHANGED = true
```

## Memory layer affected

This file is governance documentation and engineering-run evidence only.

It does not update Personal/Staff Twin Memory, Person Memory, Role Memory, Organizational Memory or Governed RAG.
