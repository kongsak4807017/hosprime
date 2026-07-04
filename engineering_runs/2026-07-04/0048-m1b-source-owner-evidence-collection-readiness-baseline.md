# HosPrime Engineering Run 0048 — M1-B Source Owner Evidence Collection Readiness Baseline

Date: 2026-07-04
Stage: BASELINE
Parent issue: #10
Memory epic: #8
Control issue: #66
Previous stage: REAL USER (#65)
Next stage: RESEARCH

## North Star outcome supported

Enable healthcare and public-health organizations to use trusted data, knowledge, organizational memory and governed AI to complete real work and make better decisions faster, with evidence, accountability and continuous learning.

This bounded BASELINE stage supports:

- evidence quality;
- user trust;
- decision-to-outcome traceability;
- knowledge reuse;
- zero unauthorized high-impact action.

## Repository evidence checked before selecting work

- `README.md` on `main` confirms the North Star, ordered Loop Engineering sequence, Core Rules, memory boundaries and current controlled release target: **Milestone 1 — Governed Knowledge Oracle MVP**.
- Open issue #66 is the next ordered M1-B stage: **BASELINE** for source-owner evidence collection readiness decision-rights baseline.
- Previous run `engineering_runs/2026-07-04/0047-m1b-source-owner-evidence-collection-readiness-real-user.md` completed the REAL USER stage and selected BASELINE as the next single stage.
- Parent issue #10 requires a governed backoffice pipeline that does not allow backoffice agents to self-approve high-impact sources.
- `docs/governance/MATURITY_GATES.md` requires named owners, source/version/classification/review-date capture, access control and review gates before M1 progression.
- `data/source_register/m1_source_register.yml` was inspected only. It was not modified.
- Recent open PR inspection found no open PR superseding this bounded stage.
- Workflow check for commit `c9036f5438948ab548cd7c8eedd586216df27e5c` returned no workflow runs; no CI pass is claimed.

## Real organizational work problem

The organization needs a measurable baseline for source-owner evidence collection readiness before later collection work can claim progress. Without a clear denominator, later source-owner packets could confuse role readiness, evidence collection, source approval, ingestion and RAG activation.

This stage therefore measures the current gaps across the five placeholder source records against the decision-rights model from run 0047 while keeping every source out of Organizational Memory / Governed RAG.

## Real users

- Public-health executive / accountable sponsor
- Provincial program source owner
- Source inventory operator
- Data governance lead
- Knowledge reviewer / independent reviewer

## Measurement basis

The current register contains five seed records:

1. `M1A-PM25-001` — PM2.5 and Environmental Health
2. `M1A-TB-001` — Tuberculosis and Communicable Disease Control
3. `M1A-NCD-001` — NCD and Chronic Care Service Model
4. `M1A-EOC-001` — Disaster, EOC and Public Health Emergency Operations
5. `M1A-DIGITAL-001` — Digital Health, Data Governance and AI Workflow

All five records remain placeholder records with:

```text
lifecycle_state = DISCOVERED
approval_status = not_approved
review_status = not_reviewed
active_rag_index = false
parsing_status = not_started
quality_status = not_started
organization = pending_source_owner_confirmation
owner_person = pending_human_assignment
file_or_system_location = pending_inventory
version = pending_inventory
checksum = pending_checksum
reviewer = pending_human_reviewer
review_date = null
decision_date = null
```

## Decision-rights readiness field groups measured

Measured across five records. These are baseline readiness fields only; they are not approval fields.

| Field group | Required readiness evidence | Current resolved count | Current unresolved count | Gap rate |
| --- | --- | ---: | ---: | ---: |
| Sponsor / organization confirmation | `organization` not pending | 0 / 5 | 5 / 5 | 100% |
| Source-owner assignment | `owner_person` not pending | 0 / 5 | 5 / 5 | 100% |
| Inventory location | `file_or_system_location` not pending | 0 / 5 | 5 / 5 | 100% |
| Version evidence | `version` not pending | 0 / 5 | 5 / 5 | 100% |
| Checksum or controlled checksum-pending justification | `checksum` not pending, or accepted checksum-pending reason | 5 / 5 | 0 / 5 | 0% |
| Classification | `classification` present | 5 / 5 | 0 / 5 | 0% |
| Access policy | `access_policy` and `allowed_roles` present | 5 / 5 | 0 / 5 | 0% |
| Reviewer assignment | `reviewer` not pending | 0 / 5 | 5 / 5 | 100% |
| Review evidence | `review_status`, `review_date`, `decision_date` complete | 0 / 5 | 5 / 5 | 100% |
| RAG activation boundary | `active_rag_index = false` until approval | 5 / 5 | 0 / 5 | 0% |

## Baseline metrics

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
SOURCE_REGISTER_MODIFIED = false
SOURCE_OWNER_EVIDENCE_COLLECTED = false
SOURCE_APPROVAL_CLAIMED = false
SOURCE_INGESTION_CLAIMED = false
RAG_ACTIVATION_CLAIMED = false
```

Inherited reference metrics are preserved for continuity:

```text
ROLE_READINESS_GAP_RATE = 54.3%
CONFIRMATION_GAP_RATE = 70%
FULLY_ROLE_READY_RECORDS = 0 / 5
FULLY_CONFIRMED_RECORDS = 0 / 5
```

## Baseline interpretation

The register has adequate placeholder controls for classification, role-scoped access policy, checksum-pending rationale and RAG non-activation. However, it is not ready for source-owner evidence collection completion because every seed record still lacks:

- confirmed organization scope;
- named owner person;
- controlled file or system location;
- source version evidence;
- named reviewer;
- completed review and decision dates.

Therefore, the correct next stage is RESEARCH, focused on how the collection packet should reduce this measured readiness gap without bypassing review or approval gates.

## Target metric for later collection work

Not achieved in this stage:

```text
TARGET_DECISION_RIGHTS_READINESS_GAP_RATE_AFTER_LATER_COLLECTION_PACKET <= 30%
TARGET_FULLY_COLLECTION_READY_RECORDS_AFTER_LATER_COLLECTION_PACKET >= 3 / 5
TARGET_FULLY_APPROVED_RECORDS_AFTER_LATER_REVIEW = 0 unless authorized review evidence exists
TARGET_ACTIVE_RAG_RECORDS = 0 until approved source, retrieval evaluation and activation gate exist
```

## Boundary assertions

```text
M1_B_BASELINE_COMPLETED = true
DECISION_RIGHTS_BASELINE_MEASURED = true
ROLE_BOUNDARY_GAPS_MEASURED = true
SOURCE_OWNER_EVIDENCE_COLLECTION_READINESS_BASELINE_RECORDED = true
NEXT_STAGE = RESEARCH
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

## Test / CI status

No executable CI success is claimed for this governance BASELINE stage.

Evidence basis:

- README inspection on `main`;
- open issue #66 inspection;
- previous run 0047 inspection;
- `data/source_register/m1_source_register.yml` inspection only;
- `docs/governance/MATURITY_GATES.md` inspection;
- open PR inspection;
- workflow run check for the previous commit.

## Memory layer affected

Research Staging / Governance evidence only.

No Personal/Staff Twin Memory, Person Memory, Role Memory or Organizational Memory / Governed RAG was modified. No external research was promoted into organizational truth.

## Risks and blockers

- No real source-owner packet has been collected yet.
- No named owner person or reviewer is assigned in the source register.
- No authoritative file, system location or version evidence is recorded.
- No approval, ingestion, parsing, embedding, indexing or retrieval activation is permitted from the current baseline.

## Next single stage

RESEARCH — identify authoritative source-owner evidence collection requirements and packet controls that can reduce the measured readiness gap without treating collection as source approval.
