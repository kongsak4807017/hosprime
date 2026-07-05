# HosPrime Engineering Run 0066 — M1-B Source Owner Evidence Collection Execution Readiness Plan

Date: 2026-07-05
Stage: PLAN
Parent issue: #10
Memory epic: #8
Control issue: #84
Previous stage: HYPOTHESIS (#83)
Next stage: BUILD

## North Star outcome supported

Enable healthcare and public-health organizations to use trusted data, knowledge, organizational memory and governed AI to complete real work and make better decisions faster, with evidence, accountability and continuous learning.

This bounded PLAN stage supports evidence quality, user trust, decision-to-outcome traceability, knowledge reuse and zero unauthorized high-impact action by defining how a later controlled filled-packet workflow can be built and tested without approving, ingesting, indexing, activating or answering from any source.

## Repository evidence checked before selecting work

- `README.md` on `main` was read before work selection and confirms the North Star, ordered Loop Engineering sequence, Core Rules, memory boundaries and current controlled release target: Milestone 1 — Governed Knowledge Oracle MVP.
- Open issue #84 is the active ordered M1-B stage: PLAN after #83 HYPOTHESIS.
- Previous run inspected: `engineering_runs/2026-07-05/0065-m1b-source-owner-evidence-collection-execution-readiness-hypothesis.md`.
- Collection-readiness packet inspected: `docs/governance/M1_B_SOURCE_OWNER_COLLECTION_READINESS_PACKET.md`.
- Source register inspected only: `data/source_register/m1_source_register.yml`.
- Open issue inspection identified #10 as the parent governed source lifecycle workstream.
- PR inspection found no open PR superseding this bounded stage.
- Latest relevant commit status inspection found no combined status checks; CI pass is not claimed.

## Real organizational work problem

HosPrime has a released collection-readiness packet and five M1 seed source records, but there is not yet a controlled execution plan for filling packet evidence in a way that reduces readiness gaps while preventing source-owner assertions from being mistaken for reviewer approval or active Organizational RAG truth.

## Real users and real work need

- Public-health executive / accountable sponsor: needs assurance that source readiness work improves evidence discipline without unauthorized factual-answer capability.
- Provincial program source owner: needs clear instructions for what can be confirmed and what remains outside approval authority.
- Source inventory operator: needs a stepwise route to record controlled location, version/source period and checksum status without mutating the source register.
- Data governance lead: needs classification, access policy, reviewer routing and conflict handling before any source review.
- Knowledge reviewer / independent reviewer: needs a precheck-ready packet that separates collection evidence from approval decisions.

## Baseline and target carried forward

```text
DECISION_RIGHTS_READINESS_GAP_RATE = 50.0%
FULLY_COLLECTION_READY_RECORDS = 0 / 5
FULLY_REVIEW_READY_RECORDS = 0 / 5
FULLY_APPROVED_RECORDS = 0 / 5
ACTIVE_RAG_RECORDS = 0 / 5

TARGET_DECISION_RIGHTS_READINESS_GAP_RATE_AFTER_LATER_FILLED_PACKET <= 30%
TARGET_FULLY_COLLECTION_READY_RECORDS_AFTER_LATER_FILLED_PACKET >= 3 / 5
TARGET_FULLY_APPROVED_RECORDS = 0 unless authorized human review evidence exists
TARGET_ACTIVE_RAG_RECORDS = 0 until approved source, retrieval evaluation and activation gate exist
```

This PLAN run does not claim target achievement.

## Controlled filled-packet workflow plan

### Step 1 — Open packet under non-approval boundary

For each seed source record, create or update only a collection-readiness evidence packet using the released ten field groups.

Required assertion:

```text
PACKET_STATUS = draft_collection_readiness_only
SOURCE_APPROVAL_CLAIMED = false
SOURCE_INGESTION_CLAIMED = false
SOURCE_PARSING_CLAIMED = false
SOURCE_EMBEDDING_CLAIMED = false
SOURCE_INDEXING_CLAIMED = false
RAG_ACTIVATION_CLAIMED = false
FACTUAL_ANSWER_PERMISSION_CLAIMED = false
ORGANIZATIONAL_MEMORY_PROMOTION_CLAIMED = false
```

### Step 2 — Map packet to source register identity

Allowed source IDs only:

```text
M1A-PM25-001
M1A-TB-001
M1A-NCD-001
M1A-EOC-001
M1A-DIGITAL-001
```

Fail closed if the source ID is absent, duplicated, invented or not present in `data/source_register/m1_source_register.yml`.

### Step 3 — Fill ten field groups without inventing evidence

Each field group must use exactly one status:

```text
present
pending_with_accountable_owner
missing
not_applicable_with_rationale
```

Status interpretation for the later build/test:

```text
present = concrete value, controlled reference, evidence note or verification method exists
pending_with_accountable_owner = accountable owner plus next action exists
missing = no concrete value, no accountable owner or no next action exists
not_applicable_with_rationale = reviewer-acceptable rationale is recorded
```

### Step 4 — Preserve review routing and source-owner limits

Source-owner confirmation may confirm inventory facts only. It must not set approval status, reviewer decision, active RAG status, source authority or factual-answer permission.

Reviewer routing must include:

```text
review_gate = collection_readiness_precheck
reviewer_role_or_office = required
conflict_of_interest_check = required_or_pending_with_owner
escalation_path = required_or_pending_with_owner
explicit_non_approval_decision = not_approved
active_rag_index_allowed = false
```

### Step 5 — Score collection readiness

For the later build/test, calculate:

```text
total_collection_groups = source_record_count * 10
closed_collection_groups = present_groups + accepted_not_applicable_groups
gap_collection_groups = pending_groups + missing_groups
DECISION_RIGHTS_READINESS_GAP_RATE = gap_collection_groups / total_collection_groups
```

Per-record readiness:

```text
collection_ready_for_precheck = true only when all 10 groups are closed
review_ready_for_precheck = true only when reviewer routing, conflict handling, provenance/limitations and non-approval assertion are closed
collection_ready_for_precheck != source_approved
collection_ready_for_precheck != review_pending
collection_ready_for_precheck != index_ready
collection_ready_for_precheck != indexed
```

### Step 6 — Route unresolved gaps

Every `pending_with_accountable_owner` group must include both:

```text
accountable_owner_for_pending
next_action_if_pending_or_missing
```

Fail closed if pending fields lack either value.

### Step 7 — Store as engineering-run evidence only

The later BUILD stage may add a controlled filled-packet execution workflow artifact or example blank execution structure. It must not modify `data/source_register/m1_source_register.yml`, approve sources, ingest files, parse, embed, index, activate RAG or answer factual questions from the seed records.

## Fail-closed checks required for later BUILD/TEST

```text
FAIL_IF_SOURCE_ID_NOT_IN_REGISTER = true
FAIL_IF_PACKET_STATUS_NOT_COLLECTION_READINESS_ONLY = true
FAIL_IF_PENDING_WITHOUT_ACCOUNTABLE_OWNER = true
FAIL_IF_PENDING_WITHOUT_NEXT_ACTION = true
FAIL_IF_MISSING_MARKED_PRESENT = true
FAIL_IF_SOURCE_OWNER_ASSERTION_TREATED_AS_REVIEWER_DECISION = true
FAIL_IF_SOURCE_APPROVAL_STATUS_CHANGED = true
FAIL_IF_LIFECYCLE_STATE_ADVANCED = true
FAIL_IF_ACTIVE_RAG_INDEX_CHANGED = true
FAIL_IF_FACTUAL_ANSWER_PERMISSION_CLAIMED = true
FAIL_IF_EXTERNAL_RESEARCH_PROMOTED_WITHOUT_REVIEW = true
```

## Evidence outputs for later build

The next BUILD stage should create one bounded controlled workflow artifact, preferably under `docs/governance/`, that includes:

1. workflow steps;
2. per-source packet naming convention;
3. scoring formula;
4. fail-closed checklist;
5. reviewer routing boundary;
6. non-approval and non-RAG assertions;
7. required acceptance flags;
8. explicit statement that source register mutation remains prohibited in this stage.

## Work completed in this run

- Read the latest README North Star, Core Rules, ordered loop, memory boundaries and controlled release target.
- Inspected open issue #84, parent issue #10, previous hypothesis run, collection-readiness packet and source register.
- Confirmed no open PR supersedes this step.
- Confirmed no CI pass is claimed because combined status checks were not present for the latest relevant commit.
- Defined the controlled filled-packet execution readiness plan.
- Did not collect source-owner evidence.
- Did not modify `data/source_register/m1_source_register.yml`.
- Did not approve, ingest, parse, embed, index, answer from or activate any source.

## Acceptance result

```text
M1_B_PLAN_COMPLETED = true
CONTROLLED_FILLED_PACKET_WORKFLOW_PLAN_DEFINED = true
SCORING_RULE_DEFINED = true
FAIL_CLOSED_CHECKS_DEFINED = true
REVIEW_ROUTING_BOUNDARY_DEFINED = true
EVIDENCE_OUTPUTS_DEFINED = true
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
NEXT_STAGE = BUILD
```

## Memory layer affected

Affected:

- engineering-run evidence;
- issue traceability;
- Research Staging design interpretation only.

Not affected:

- Personal/Staff Twin Memory;
- Person Memory;
- Role Memory;
- Organizational Memory / Governed RAG;
- source-register approval status;
- source-register lifecycle state;
- source-register active-RAG status.

## Risks and blockers

```text
RISK_PLAN_NOT_YET_BUILT = true
RISK_FILLED_PACKET_NOT_YET_EXECUTED = true
RISK_UNRESOLVED_OWNER_ASSIGNMENT = true
RISK_UNRESOLVED_CONTROLLED_LOCATION = true
RISK_UNRESOLVED_VERSION_AND_CHECKSUM = true
RISK_UNRESOLVED_REVIEWER_ROUTING = true
RISK_SOURCE_OWNER_ASSERTION_MISREAD_AS_APPROVAL = controlled_by_non_approval_boundary
RISK_PREMATURE_RAG_ACTIVATION = controlled_by_fail_closed_checks
```

## Single next stage

BUILD — create the controlled filled-packet execution workflow artifact with scoring, fail-closed checks, reviewer-routing boundaries and evidence outputs, without source-register mutation, source approval, ingestion or RAG activation.
