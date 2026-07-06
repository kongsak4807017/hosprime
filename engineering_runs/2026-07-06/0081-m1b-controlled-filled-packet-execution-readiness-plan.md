# HosPrime Engineering Run 0081 — M1-B Controlled Filled-Packet Execution Readiness Plan

Date: 2026-07-06
Stage: PLAN
Parent issue: #10
Memory epic: #8
Control issue: #99
Previous stage: HYPOTHESIS (#98)
Next stage: BUILD

## North Star outcome supported

Enable healthcare and public-health organizations to use trusted data, knowledge, organizational memory and governed AI to complete real work and make better decisions faster, with evidence, accountability and continuous learning.

This bounded PLAN stage supports Trusted Task Completion Rate, evidence quality, user trust, decision-to-outcome traceability, knowledge reuse and zero unauthorized high-impact action by defining exactly how the next controlled filled-packet execution step may be built without claiming source approval, ingestion, indexing, Organizational RAG activation or operational execution.

## Repository evidence checked before selecting work

- `README.md` on `main` was read before work selection and confirms the North Star, ordered Loop Engineering sequence, Core Rules, memory boundaries and the current controlled release target: Milestone 1 — Governed Knowledge Oracle MVP.
- Open issue #99 is the active ordered M1-B control issue: PLAN after #98 HYPOTHESIS.
- Recent open issues were inspected. #99 is the current M1-B control issue; #10 remains the governed backoffice pipeline parent.
- Open pull requests inspected through the available connector: none returned for this repository at this run.
- CI/workflow status for prior commit `d1f477ca349e1930f8b412e521c8995edfefbc22` was checked through the available connector and returned no workflow runs. CI pass is not claimed.
- Previous hypothesis evidence inspected: `engineering_runs/2026-07-06/0080-m1b-controlled-filled-packet-execution-readiness-hypothesis.md`.
- Maturity gate evidence inspected: `docs/governance/MATURITY_GATES.md`.
- Source register inspected: `data/source_register/m1_source_register.yml` still contains five `DISCOVERED` placeholder records only, no approved source and no active RAG index.

## Current loop stage

```text
CURRENT_STAGE = PLAN
PREVIOUS_STAGE = HYPOTHESIS
NEXT_STAGE = BUILD
```

## Real user and real work problem

Real users carried forward:

```text
public-health executive / accountable sponsor
provincial program source owner
source inventory operator
data governance lead
knowledge reviewer / independent reviewer
```

Real organizational work problem:

HosPrime has five M1 seed source records and a controlled workflow, but no filled source-owner packet exists for any seed source. Without a bounded execution-readiness plan, operators could either stop at placeholders or accidentally treat incomplete packet filling as approval. The work problem is therefore to define a safe, measurable build plan for source-owner packet preparation that improves collection readiness while preserving non-approval and non-RAG boundaries.

## Baseline carried forward

```text
DECISION_RIGHTS_READINESS_GAP_RATE = 50.0%
FULLY_COLLECTION_READY_RECORDS = 0 / 5
FULLY_REVIEW_READY_RECORDS = 0 / 5
FULLY_APPROVED_RECORDS = 0 / 5
ACTIVE_RAG_RECORDS = 0 / 5
TOTAL_REQUIRED_FIELD_GROUPS = 50
FILLED_SOURCE_OWNER_PACKET_COUNT = 0
FULLY_CLOSED_PACKET_FIELD_GROUPS = 0 / 50
FIELD_GROUP_FULL_CLOSURE_GAP_RATE = 100.0%
```

## Target metric for the next bounded build

The next BUILD stage should add a controlled execution-readiness packet template and planned filled-packet skeletons, not collect or assert live owner evidence.

```text
TARGET_PACKET_TEMPLATE_EXISTS = true
TARGET_PACKET_SKELETONS_CREATED = 5 / 5
TARGET_SOURCE_IDS_MATCH_REGISTER = 5 / 5
TARGET_REQUIRED_FIELD_GROUPS_PER_PACKET = 10
TARGET_PENDING_GROUPS_HAVE_ACCOUNTABLE_OWNER_AND_NEXT_ACTION = 100%
TARGET_COLLECTION_READY_RECORDS_AFTER_BUILD = 0 / 5 unless real source-owner evidence is supplied separately
TARGET_APPROVED_RECORDS_AFTER_BUILD = 0 / 5
TARGET_ACTIVE_RAG_RECORDS_AFTER_BUILD = 0 / 5
```

## Planned build artifact

Create one documentation artifact only:

```text
docs/governance/M1_B_CONTROLLED_FILLED_PACKET_EXECUTION_READINESS_PACKETS.md
```

The artifact should include:

1. a reusable packet template;
2. one skeleton section for each source ID already present in `data/source_register/m1_source_register.yml`;
3. ten required field groups for each skeleton;
4. explicit pending-owner routing and next executable action for every unfilled field group;
5. non-approval and non-RAG assertions for every skeleton;
6. reviewer precheck routing;
7. scoring method and failure conditions;
8. a statement that the source register is not modified by skeleton creation.

## Allowed source IDs for the next build

The next BUILD must use exactly these source IDs and must not invent additional records:

```text
M1A-PM25-001
M1A-TB-001
M1A-NCD-001
M1A-EOC-001
M1A-DIGITAL-001
```

## Required ten field groups per packet

Each packet skeleton must contain exactly these ten field groups:

```text
1. source_identity
2. organization_scope
3. accountable_sponsor
4. source_owner
5. controlled_location
6. version_or_source_period
7. checksum_or_checksum_pending_reason
8. classification_and_access
9. reviewer_precheck_routing
10. provenance_and_limitations
```

## Allowed field-group statuses

```text
present
pending_owner_confirmation
pending_inventory
pending_checksum
pending_reviewer_assignment
not_applicable_with_reason
```

Rules:

- `present` must not be used unless the artifact records the evidence value, provenance and limitation.
- Any pending status must name an accountable role and the next executable action.
- `pending_checksum` must include the checksum-pending reason and must not imply file control.
- `not_applicable_with_reason` must include a reason that a reviewer can accept or reject.

## Scoring method for later evaluation

Per source record:

```text
TOTAL_FIELD_GROUPS = 10
CLOSED_FIELD_GROUP = status is present OR not_applicable_with_reason accepted_for_precheck
PENDING_FIELD_GROUP = any pending status with accountable role and next action
UNCONTROLLED_FIELD_GROUP = pending status without accountable role OR without next action
COLLECTION_READY = all 10 field groups closed or controlled-pending, and no uncontrolled field group
REVIEW_READY = collection-ready plus named reviewer and evidence packet complete
APPROVED = only after authorized human review record exists
ACTIVE_RAG = only after approved source, retrieval evaluation and activation gate exist
```

Decision-rights readiness gap for later evaluation:

```text
DECISION_RIGHTS_READINESS_GAP_RATE =
records missing accountable owner or reviewer routing
---------------------------------------------------
total source records
```

## Build acceptance criteria

The next BUILD stage may be accepted only if:

```text
PACKET_TEMPLATE_CREATED = true
PACKET_SKELETON_COUNT = 5
ALL_SOURCE_IDS_EXIST_IN_REGISTER = true
ALL_PACKET_SKELETONS_HAVE_10_FIELD_GROUPS = true
ALL_PENDING_GROUPS_HAVE_ACCOUNTABLE_ROLE_AND_NEXT_ACTION = true
SOURCE_REGISTER_MODIFIED = false
SOURCE_OWNER_EVIDENCE_COLLECTED = false unless separately evidenced
SOURCE_APPROVAL_CLAIMED = false
SOURCE_INGESTION_CLAIMED = false
SOURCE_INDEXING_CLAIMED = false
RAG_ACTIVATION_CLAIMED = false
CI_PASS_CLAIMED = false unless workflow evidence exists
```

## Test plan for the later TEST stage

The later TEST stage should verify:

```text
SOURCE_ID_SET_EQUALS_REGISTER_SEED_IDS = true
PACKET_SKELETON_COUNT_EQUALS_5 = true
FIELD_GROUP_COUNT_EQUALS_10_FOR_EACH_PACKET = true
NO_APPROVED_STATUS_IN_PACKET_SKELETONS = true
NO_ACTIVE_RAG_STATUS_IN_PACKET_SKELETONS = true
NO_SOURCE_REGISTER_MUTATION = true
PENDING_FIELDS_HAVE_ACCOUNTABLE_OWNER = true
PENDING_FIELDS_HAVE_NEXT_ACTION = true
RESTRICTED_ACCESS_IS_NOT_LOOSENED = true
```

## Boundaries preserved in this PLAN stage

```text
RESEARCH_STAGING_ONLY_UNTIL_REVIEWED = true
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
```

## Acceptance result

```text
M1_B_PLAN_COMPLETED = true
CONTROLLED_PACKET_EXECUTION_READINESS_BUILD_PLAN_DEFINED = true
MEASURABLE_BUILD_ACCEPTANCE_CRITERIA_DEFINED = true
NON_APPROVAL_BOUNDARY_PRESERVED = true
SOURCE_REGISTER_MODIFIED = false
SOURCE_APPROVAL_CLAIMED = false
RAG_ACTIVATION_CLAIMED = false
NEXT_STAGE = BUILD
```

## Memory layer affected

Affected:

- engineering-run evidence;
- issue traceability;
- plan record for controlled packet execution readiness.

Not affected:

- Personal / Staff Twin Memory;
- Person Memory;
- Role Memory as durable operational truth;
- Organizational Memory / Governed RAG;
- source-register lifecycle state;
- source-register approval status;
- source-register active-RAG status.

## Risks and blockers

```text
RISK_PLAN_NOT_YET_BUILT = true
RISK_NAMED_SOURCE_OWNER_ASSIGNMENT_PENDING = true
RISK_CONTROLLED_LOCATION_PENDING = true
RISK_VERSION_OR_SOURCE_PERIOD_PENDING = true
RISK_CHECKSUM_PENDING = true
RISK_REVIEWER_ASSIGNMENT_PENDING = true
RISK_PACKET_SKELETON_COULD_BE_MISREAD_AS_SOURCE_OWNER_EVIDENCE = true
RISK_EXTERNAL_GUIDANCE_NOT_YET_REVIEWED_FOR_LOCAL_APPLICABILITY = true
CI_STATUS_PASS_NOT_VERIFIED = true
```

## Single next stage

BUILD — create the controlled filled-packet execution-readiness packet template and five source-ID-matched packet skeletons, preserving skeleton-only status and explicit non-approval/RAG boundaries.
