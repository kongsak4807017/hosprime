# HosPrime Engineering Run 0051 — M1-B Source Owner Evidence Collection Readiness Plan

Date: 2026-07-05
Stage: PLAN
Parent issue: #10
Memory epic: #8
Control issue: #69
Previous stage: HYPOTHESIS (#68)
Next stage: BUILD

## North Star outcome supported

Enable healthcare and public-health organizations to use trusted data, knowledge, organizational memory and governed AI to complete real work and make better decisions faster, with evidence, accountability and continuous learning.

This bounded PLAN stage supports:

- evidence quality;
- user trust;
- decision-to-outcome traceability;
- knowledge reuse;
- zero unauthorized high-impact action.

## Repository evidence checked before selecting work

- `README.md` on `main` confirms the North Star, ordered Loop Engineering sequence, Core Rules, memory boundaries and current controlled release target: **Milestone 1 — Governed Knowledge Oracle MVP**.
- Open issue #69 is the next ordered M1-B stage: **PLAN** after #68 HYPOTHESIS.
- Previous run `engineering_runs/2026-07-05/0050-m1b-source-owner-evidence-collection-readiness-hypothesis.md` completed HYPOTHESIS and selected PLAN as the next stage.
- Parent issue #10 requires a governed backoffice source lifecycle and states that backoffice agents cannot self-approve high-impact sources.
- `docs/governance/MATURITY_GATES.md` requires named owners, source/version/classification/review-date capture, restricted access protection, review gates and no gate bypass.
- `data/source_register/m1_source_register.yml` was inspected only. It remains placeholder-only, with five DISCOVERED seed records, no approval, no active RAG activation and pending owner/location/version/checksum fields.
- `docs/governance/M1_B_CONTROLLED_SOURCE_CONFIRMATION_PACKET.md` was inspected as the existing controlled packet artifact. It already separates inventory/role-assignment readiness from source approval and active retrieval.
- Recent PR / issue inspection found no open PR that supersedes this bounded PLAN stage.
- Combined commit status and workflow run lookup for previous run commit `f8d76b7cd5e4814652f09fbe2a07a50cfe5b4b6e` returned no CI statuses or workflow runs; no CI pass is claimed.

## Real organizational work problem

The organization has five placeholder source-register records for M1, but collection readiness is still not operationally actionable. Source owners and reviewers need a precise build plan for a source-owner collection packet that reduces decision-rights readiness gaps without modifying the source register, approving sources, ingesting files, indexing documents or enabling factual answers.

Without this plan, a later BUILD step could create extra form text without proving how it reduces the baseline gap, how the packet should be scored, or which safety gates must fail closed.

## Real users

- Public-health executive / accountable sponsor who needs trusted answers with visible ownership and accountability.
- Provincial program source owner who must identify and attest to controlled evidence before review.
- Source inventory operator who collects file/system/version/checksum evidence.
- Data governance lead who checks classification, access boundary and review route.
- Knowledge reviewer / independent reviewer who later accepts or rejects collection readiness before any source review planning.

## Baseline preserved from #66, #67 and #68

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

## Target metric for later collection packet work

```text
TARGET_DECISION_RIGHTS_READINESS_GAP_RATE_AFTER_LATER_COLLECTION_PACKET <= 30%
TARGET_FULLY_COLLECTION_READY_RECORDS_AFTER_LATER_COLLECTION_PACKET >= 3 / 5
TARGET_FULLY_APPROVED_RECORDS = 0 unless authorized human review evidence exists
TARGET_ACTIVE_RAG_RECORDS = 0 until approved source, retrieval evaluation and activation gate exist
```

This PLAN stage does not claim the target has been achieved.

## Collection packet build plan

The later BUILD stage should create a controlled source-owner collection packet template or packet appendix that can be filled for each of the five seed source records.

The build artifact should define one packet block per source record and require ten decision-rights field groups:

```text
1. source_id and knowledge_pack mapping
2. organization_scope_confirmation
3. accountable_sponsor_role_or_person
4. source_owner_role_or_person
5. controlled_file_or_system_location
6. version_or_source_date_period_evidence
7. checksum_or_checksum_pending_reason
8. classification_and_access_policy_confirmation
9. reviewer_routing_and_review_expectation
10. provenance_limitations_applicability_and_non_approval_assertion
```

The packet must retain the existing separation between:

```text
collection_status
review_status
approval_status
ingestion_status
active_rag_index
```

## Required field group detail for BUILD

### 1. Source ID and knowledge-pack mapping

Purpose: prevent evidence collection from drifting away from the governed source register.

Required fields:

```yaml
source_id: ""
knowledge_pack: ""
source_title: ""
source_register_path: "data/source_register/m1_source_register.yml"
source_register_record_seen: false
status: ""
evidence_note: ""
accountable_owner_for_pending: ""
```

### 2. Organization scope confirmation

Purpose: identify which organization, office or controlled domain owns the source context.

Required fields:

```yaml
organization_scope_confirmation:
  status: ""
  organization_or_office: ""
  scope_boundary: ""
  confirmation_method: ""
  evidence_note: ""
  accountable_owner_for_pending: ""
```

### 3. Accountable sponsor role or person

Purpose: identify the accountable sponsor for collection readiness without inventing authority.

Required fields:

```yaml
accountable_sponsor:
  status: ""
  sponsor_role: ""
  sponsor_person_or_office: ""
  authority_basis: ""
  decision_scope: "collection_readiness_only"
  evidence_note: ""
  accountable_owner_for_pending: ""
```

### 4. Source owner role or person

Purpose: assign who can confirm the source inventory facts.

Required fields:

```yaml
source_owner:
  status: ""
  owner_role: ""
  owner_person_or_office: ""
  assignment_method: ""
  assignment_limitations: ""
  evidence_note: ""
  accountable_owner_for_pending: ""
```

### 5. Controlled file or system location

Purpose: avoid public-link or memory-only source claims.

Required fields:

```yaml
controlled_location:
  status: ""
  location_type: ""
  controlled_reference: ""
  access_route: ""
  non_public_reference_allowed: true
  evidence_note: ""
  accountable_owner_for_pending: ""
```

### 6. Version or source date/period evidence

Purpose: support freshness and supersession review.

Required fields:

```yaml
version_or_source_period:
  status: ""
  version: ""
  effective_date_or_period: ""
  currentness_statement: ""
  supersedes_or_replaces: ""
  evidence_note: ""
  accountable_owner_for_pending: ""
```

### 7. Checksum or checksum-pending reason

Purpose: avoid pretending file integrity is verified before controlled file access exists.

Required fields:

```yaml
checksum_or_pending:
  status: ""
  checksum_value: ""
  checksum_method: ""
  checksum_pending_reason: ""
  non_file_verification_method: ""
  evidence_note: ""
  accountable_owner_for_pending: ""
```

### 8. Classification and access policy confirmation

Purpose: keep restricted sources inactive and role-scoped.

Required fields:

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
```

### 9. Reviewer routing and review expectation

Purpose: route collection readiness to a human reviewer before any later source review.

Required fields:

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
```

### 10. Provenance, limitations, applicability and non-approval assertion

Purpose: make collected evidence auditable while preventing source approval or RAG activation claims.

Required fields:

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
```

## Allowed statuses and scoring method

Allowed status values for each field group:

```text
present
pending_with_accountable_owner
missing
not_applicable_with_rationale
```

Closed group rule:

```text
closed_group = present OR not_applicable_with_rationale_with_reason
```

Gap group rule:

```text
gap_group = pending_with_accountable_owner OR missing
```

Collection readiness scoring:

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

## Acceptance checks for later TEST stage

Later TEST should verify that the BUILD artifact satisfies all of the following without modifying the source register:

```text
FIELD_GROUP_COUNT = 10
ALLOWED_STATUS_SET_ENFORCED = true
ALL_FIVE_SEED_SOURCE_IDS_COVERED = true
SOURCE_ID_MATCHES_REGISTER_REQUIRED = true
PENDING_GROUPS_REQUIRE_ACCOUNTABLE_OWNER = true
CHECKSUM_PENDING_ALLOWED_WITH_REASON = true
RESTRICTED_SOURCE_HANDLING_PRESERVED = true
NON_APPROVAL_ASSERTION_REQUIRED = true
SOURCE_REGISTER_MODIFIED = false
SOURCE_APPROVAL_CLAIMED = false
SOURCE_INGESTION_CLAIMED = false
RAG_ACTIVATION_CLAIMED = false
```

## Safety gates for later BUILD and TEST

The packet must fail closed if any of these occur:

1. Any source is marked approved from collection evidence alone.
2. Any source is marked ingested, parsed, embedded, indexed or active in RAG.
3. Any restricted source loosens access roles without review evidence.
4. Any person, office, source location, checksum or reviewer is invented.
5. Any `pending_with_accountable_owner` field lacks accountable owner and next action note.
6. Any missing field is hidden as `present`.
7. Any personal/staff memory or external research is promoted into Organizational Memory / Governed RAG without review.

## Build output expected in next stage

The next BUILD stage should update or add a controlled packet artifact that includes:

```text
COLLECTION_PACKET_TEMPLATE_ADDED = true
COLLECTION_PACKET_FIELD_GROUP_COUNT = 10
COLLECTION_PACKET_SCORING_RULE_ADDED = true
COLLECTION_PACKET_TEST_SCOPE_ADDED = true
SOURCE_REGISTER_MODIFIED = false
SOURCE_OWNER_EVIDENCE_COLLECTED = false
SOURCE_APPROVAL_CLAIMED = false
SOURCE_INGESTION_CLAIMED = false
RAG_ACTIVATION_CLAIMED = false
```

## Explicit non-actions in this run

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
CI_PASS_CLAIMED = false
```

## Acceptance result

```text
M1_B_PLAN_COMPLETED = true
COLLECTION_PACKET_PLAN_DEFINED = true
FIELD_GROUPS_AND_SCORING_DEFINED = true
TARGET_DECISION_RIGHTS_READINESS_GAP_RATE_AFTER_LATER_COLLECTION_PACKET <= 30%
NEXT_STAGE = BUILD
SOURCE_REGISTER_MODIFIED = false
SOURCE_APPROVAL_CLAIMED = false
SOURCE_INGESTION_CLAIMED = false
RAG_ACTIVATION_CLAIMED = false
```

## Test / CI status

No executable CI success is claimed for this governance PLAN stage.

Evidence basis:

- README inspection on `main`;
- open issue #69 inspection;
- previous run 0050 inspection;
- `data/source_register/m1_source_register.yml` inspection only;
- `docs/governance/M1_B_CONTROLLED_SOURCE_CONFIRMATION_PACKET.md` inspection;
- `docs/governance/MATURITY_GATES.md` inspection;
- recent PR / issue inspection;
- combined commit status and workflow-run check for previous run commit.

## Memory layer affected

Research Staging / Governance evidence only.

No Personal/Staff Twin Memory, Person Memory, Role Memory or Organizational Memory / Governed RAG was modified. No external research was promoted into organizational truth.

## Risks and blockers

- The collection packet has been planned, but no packet template was built in this run.
- No real source-owner evidence has been collected.
- No human reviewer has approved any source.
- No ingestion, parsing, embedding, indexing or retrieval activation is permitted from this run.
- CI has not run or has no visible status for the prior governance-only commit; no CI pass is claimed.

## Next single stage

BUILD — create the bounded collection packet artifact/template with the ten field groups, scoring rule and test scope, without modifying the source register or claiming approval.
