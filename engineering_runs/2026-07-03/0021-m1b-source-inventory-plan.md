# HosPrime Engineering Run 0021 — M1-B Controlled Source Inventory Plan

Date: 2026-07-03
Stage: PLAN
Parent issue: #10
Control issue: #39
Previous stage: HYPOTHESIS (#38)
Next stage: BUILD

## North Star outcome supported

Enable healthcare and public-health organizations to use trusted data, knowledge, organizational memory and governed AI to complete real work and make better decisions faster, with evidence, accountability and continuous learning.

This plan supports:

- evidence-based decisions;
- user trust;
- decision-to-outcome traceability;
- knowledge reuse;
- zero unauthorized high-impact action.

## Real user and real organizational work problem

Real users:

- public-health executive;
- provincial program owner;
- data governance lead;
- knowledge reviewer;
- future source inventory operator.

Real work problem:

The M1 source register contains five placeholder source records, but no record is fully confirmed for controlled source inventory. A bounded confirmation packet is needed so source owners and reviewers can close inventory gaps without confusing confirmation with approval, ingestion, indexing, retrieval activation or factual-answer authority.

## Baseline inherited from #36 and #38

```text
TOTAL_SOURCE_RECORDS = 5
TOTAL_CONFIRMATION_CELLS = 50
PRESENT_CELLS = 15 / 50 = 30%
PENDING_CELLS = 15 / 50 = 30%
MISSING_CELLS = 20 / 50 = 40%
BASELINE_GAP_RATE = 35 / 50 pending_or_missing_cells = 70%
FULLY_CONFIRMED_RECORDS = 0 / 5
```

## Target metric for the planned build/test path

```text
TARGET_GAP_RATE_AFTER_PACKET = <= 15 / 50 = <= 30%
TARGET_FULLY_CONFIRMED_RECORDS = >= 3 / 5
SOURCE_APPROVAL_CLAIMED = false
SOURCE_INGESTION_CLAIMED = false
RAG_ACTIVATION_CLAIMED = false
```

## Repository evidence checked before selecting work

- `README.md` on `main` confirms the North Star, current release target and Core Rules.
- Current release target remains Milestone 1 — Governed Knowledge Oracle MVP.
- Open issue #39 is the next ordered M1-B stage: PLAN.
- Parent issue #10 defines the governed backoffice source lifecycle and explicitly requires auditable source ownership, quality, review, promotion and rejection controls.
- The M1 source register remains placeholder-only:
  - five records exist;
  - all lifecycle states are `DISCOVERED`;
  - all approval statuses are `not_approved`;
  - all active RAG flags are `false`.
- Previous hypothesis run #38 / Engineering Run 0020 defined the minimum confirmation packet hypothesis and target metrics.
- Recent PR evidence: PR #33 is already merged and established the executable M1 source-register CI gate.

## Plan scope

Create a controlled confirmation-packet structure and measurement method in the next BUILD stage. The planned artifact should be documentation and/or a non-authoritative template only. It must not alter `data/source_register/m1_source_register.yml` during PLAN.

Planned build artifact:

```text
docs/governance/M1_B_CONTROLLED_SOURCE_CONFIRMATION_PACKET.md
```

Optional future machine-readable artifact, only if needed in BUILD:

```text
data/source_register/m1b_confirmation_packet_template.yml
```

## Minimum confirmation packet fields

Each placeholder source record should be confirmable against these ten cells:

1. `source_id` — existing register ID being confirmed.
2. `accountable_owner_or_office` — named owner person or accountable office.
3. `controlled_location_type` — file repository, document management system, official drive folder, approved system, physical archive or other controlled location class.
4. `controlled_location_reference` — controlled path, system identifier or archive reference; not necessarily public.
5. `version_or_effective_date` — document version, effective date, approval date or currentness statement.
6. `checksum_status` — checksum value, checksum pending with reason, or non-file evidence with documented verification method.
7. `classification_and_access_policy_confirmed` — confirmation that classification and role-scoped access policy are correct or need correction.
8. `reviewer_assignment` — reviewer role plus named reviewer or reviewing office.
9. `provenance_confirmation` — confirmation method, confirmer and confirmation date.
10. `limitation_or_replacement_note` — known limitations, superseded source relationship or replacement note.

## Measurement method

A confirmation cell counts as:

- `present` only when a specific value or accountable office/person/method is recorded;
- `pending` when the packet gives an accountable pending reason and owner for follow-up;
- `missing` when no specific value, accountable pending reason or owner exists.

A source record is `fully_confirmed_for_inventory` only when all ten cells are `present` or contain an explicitly accountable pending reason accepted for inventory readiness. This does **not** mean source approval.

Gap rate formula:

```text
pending_or_missing_confirmation_cells
-------------------------------------
total_confirmation_cells
```

Target pass condition for the later TEST stage:

```text
pending_or_missing_confirmation_cells <= 15 / 50
fully_confirmed_for_inventory_records >= 3 / 5
all_records_remain_not_approved = true
all_active_rag_index_flags_remain_false = true
```

## Build-stage work plan

The next BUILD stage should do exactly one bounded step:

1. Add the confirmation-packet documentation/template.
2. Include the field definitions, allowed statuses, measurement formula and explicit non-approval boundary.
3. Include a reviewer checklist for source owner and knowledge reviewer use.
4. Include a warning that the packet is inventory-readiness evidence only.
5. Do not modify the source register records.
6. Do not create ingestion, parsing, embedding, indexing or retrieval code.

## Test-stage plan

A later TEST stage should validate that the built packet/template contains:

```text
MINIMUM_CONFIRMATION_PACKET_FIELDS_PRESENT = true
MEASUREMENT_METHOD_DEFINED = true
NON_APPROVAL_BOUNDARY_DEFINED = true
SOURCE_REGISTER_UNCHANGED_FOR_APPROVAL_STATUS = true
SOURCE_REGISTER_UNCHANGED_FOR_ACTIVE_RAG_INDEX = true
```

Fail conditions:

- any placeholder is marked approved, review-pending, index-ready or indexed;
- any active RAG flag is changed to true;
- any language claims factual-answer permission from placeholder sources;
- Research Staging is promoted to Organizational Memory / Governed RAG without review.

## Release and observation plan

Release should only link the packet to the controlled issue path. Observation should recompute gap rate only after a later authorized human/user confirmation packet is filled. No improvement claim is allowed until evidence exists.

## Memory layer affected

Research Staging and engineering-run evidence only.

No Personal/Staff Twin Memory, Person Memory, Role Memory, Organizational Memory or Governed RAG was updated.

## Risks and blockers

- Named source owners remain missing.
- Controlled locations remain missing.
- Version/effective date evidence remains missing.
- Checksum evidence remains missing.
- Reviewer assignments remain missing.
- The packet could be misinterpreted as approval evidence unless the non-approval boundary is repeated in the BUILD artifact.

## Stage result

```text
M1_B_PLAN_DEFINED = true
CONFIRMATION_PACKET_BUILD_SCOPE_DEFINED = true
ACCEPTANCE_TESTS_DEFINED = true
SOURCE_REGISTER_MODIFIED = false
SOURCE_APPROVAL_CLAIMED = false
SOURCE_INGESTION_CLAIMED = false
RAG_ACTIVATION_CLAIMED = false
ORGANIZATIONAL_MEMORY_PROMOTION_CLAIMED = false
```

## Single next stage

BUILD — create the controlled source confirmation packet documentation/template without altering approval, ingestion, indexing or RAG activation state.
