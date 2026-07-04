# HosPrime Engineering Run 0033 — M1-B Source Owner Evidence Baseline

Date: 2026-07-04
Stage: BASELINE
Parent issue: #10
Control issue: #51
Previous stage: REAL USER (#50)
Next stage: RESEARCH

## North Star outcome supported

Enable healthcare and public-health organizations to use trusted data, knowledge, organizational memory and governed AI to complete real work and make better decisions faster, with evidence, accountability and continuous learning.

This bounded baseline supports:

- evidence quality;
- user trust;
- decision-to-outcome traceability;
- knowledge reuse;
- zero unauthorized high-impact action.

## Repository evidence checked before selecting work

- `README.md` on `main` confirms the North Star, ordered loop, current controlled release target and Core Rules.
- Current controlled release target remains **Milestone 1 — Governed Knowledge Oracle MVP**.
- Open issue #51 is the next ordered M1-B stage: **BASELINE**.
- Parent issue #10 requires a governed source lifecycle with ownership, classification, review evidence, restricted-source filtering, retrieval evaluation before activation, authenticated reviewer decisions and no backoffice-agent self-approval.
- `data/source_register/m1_source_register.yml` contains five seed source records, all still `lifecycle_state: DISCOVERED`, `approval_status: not_approved`, and `active_rag_index: false`.
- Prior run `engineering_runs/2026-07-04/0032-m1b-source-owner-evidence-real-user.md` defines the real users, role boundaries and decision rights for controlled source-owner evidence collection.
- Open pull request lookup returned no open pull requests for this governance baseline stage.

## Real user and real organizational work problem

Real users:

- public-health executive / accountable sponsor;
- provincial program source owner;
- source inventory operator;
- data governance lead;
- knowledge reviewer / independent reviewer.

Real work problem:

The five M1 placeholder source records cannot safely advance toward governed evidence collection unless the project first measures whether each record has enough role coverage and decision-right readiness to identify source owners, collect controlled-source evidence and route evidence to an independent reviewer without creating unauthorized source approval, ingestion or RAG activation.

## Current loop stage

Completed exactly one stage: **BASELINE**.

No research, hypothesis, plan, build, test, evaluation, review, release, observation, learning or memory-correction stage was performed in this run.

## Baseline inherited from #36 through #50

```text
TOTAL_SOURCE_RECORDS = 5
TOTAL_CONFIRMATION_CELLS = 50
PRESENT_CELLS = 15 / 50 = 30%
PENDING_CELLS = 15 / 50 = 30%
MISSING_CELLS = 20 / 50 = 40%
BASELINE_GAP_RATE = 35 / 50 pending_or_missing_cells = 70%
FULLY_CONFIRMED_RECORDS = 0 / 5
REAL_USERS_DEFINED = true
DECISION_RIGHTS_DEFINED = true
```

## New role-readiness baseline measured in this run

Role-readiness dimensions measured for each of the five placeholder records:

1. `owner_role_defined`
2. `owner_person_assigned`
3. `organization_confirmed`
4. `allowed_roles_defined`
5. `knowledge_reviewer_role_present`
6. `independent_reviewer_assigned`
7. `data_governance_decision_path_present`

Interpretation rules:

- **Present** means the current register or prior role-definition evidence explicitly supports the readiness item.
- **Missing** means the item still requires a named human, confirmed organization, reviewer assignment or decision-path record before evidence collection can be treated as controlled.
- This baseline does not collect evidence from source owners and does not update the source register.

### Record-level role-readiness results

| Source record | Owner role defined | Owner person assigned | Organization confirmed | Allowed roles defined | Knowledge reviewer role present | Independent reviewer assigned | Data-governance decision path present | Present / 7 | Missing / 7 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| M1A-PM25-001 | Present | Missing | Missing | Present | Present | Missing | Missing | 3 | 4 |
| M1A-TB-001 | Present | Missing | Missing | Present | Present | Missing | Missing | 3 | 4 |
| M1A-NCD-001 | Present | Missing | Missing | Present | Present | Missing | Missing | 3 | 4 |
| M1A-EOC-001 | Present | Missing | Missing | Present | Present | Missing | Missing | 3 | 4 |
| M1A-DIGITAL-001 | Present | Missing | Missing | Present | Present | Missing | Present | 4 | 3 |

### Aggregate role-readiness baseline

```text
TOTAL_SOURCE_RECORDS = 5
ROLE_READINESS_DIMENSIONS_PER_RECORD = 7
TOTAL_ROLE_READINESS_CELLS = 35
ROLE_READINESS_PRESENT_CELLS = 16 / 35 = 45.7%
ROLE_READINESS_MISSING_CELLS = 19 / 35 = 54.3%
ROLE_READINESS_GAP_RATE = 54.3%
RECORDS_WITH_OWNER_ROLE_DEFINED = 5 / 5
RECORDS_WITH_OWNER_PERSON_ASSIGNED = 0 / 5
RECORDS_WITH_ORGANIZATION_CONFIRMED = 0 / 5
RECORDS_WITH_ALLOWED_ROLES_DEFINED = 5 / 5
RECORDS_WITH_KNOWLEDGE_REVIEWER_ROLE_PRESENT = 5 / 5
RECORDS_WITH_INDEPENDENT_REVIEWER_ASSIGNED = 0 / 5
RECORDS_WITH_DATA_GOVERNANCE_DECISION_PATH_PRESENT = 1 / 5
FULLY_ROLE_READY_RECORDS = 0 / 5
```

## Baseline and target metric

Current baseline:

```text
CONFIRMATION_GAP_RATE = 70%
ROLE_READINESS_GAP_RATE = 54.3%
FULLY_CONFIRMED_RECORDS = 0 / 5
FULLY_ROLE_READY_RECORDS = 0 / 5
SOURCE_OWNER_EVIDENCE_COLLECTED = false
```

Target framing for later source-owner evidence collection, not claimed in this stage:

```text
TARGET_GAP_RATE_AFTER_LATER_COLLECTION_PACKET <= 30%
TARGET_FULLY_CONFIRMED_RECORDS_AFTER_LATER_COLLECTION_PACKET >= 3 / 5
TARGET_ROLE_READINESS_GAP_RATE_AFTER_LATER_COLLECTION_PACKET <= 30%
TARGET_FULLY_ROLE_READY_RECORDS_AFTER_LATER_COLLECTION_PACKET >= 3 / 5
```

## Work completed

- Completed exactly one loop stage: BASELINE.
- Measured role-coverage and decision-rights readiness across the five M1 placeholder source records.
- Preserved the inherited 70% confirmation gap baseline.
- Recorded that the strongest current readiness items are owner-role definition, allowed-role definition and knowledge-reviewer role presence.
- Recorded that the blocking readiness gaps are named owner assignment, organization confirmation, independent reviewer assignment and explicit data-governance decision path coverage for four of five records.
- Created the next executable issue for the RESEARCH stage.

## Boundary assertions

```text
M1_B_BASELINE_COMPLETED = true
BASELINE_ROLE_READINESS_MEASURED = true
ROLE_COVERAGE_GAP_DEFINED = true
ROLE_READINESS_GAP_RATE = 54.3%
FULLY_ROLE_READY_RECORDS = 0 / 5
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

## Test / CI status

No executable CI success is claimed for this governance baseline stage.

Evidence basis:

- README inspection on `main`;
- open issue #51 inspection;
- parent issue #10 inspection through open issue search;
- source-register inspection;
- prior engineering run 0032 inspection;
- open pull request lookup returned no open pull requests.

## Memory layer affected

Affected:

- engineering-run evidence;
- issue traceability;
- governance planning memory.

Not affected:

- Personal/Staff Twin Memory;
- Person Memory;
- Role Memory as active runtime memory;
- Organizational Memory / Governed RAG;
- Research Staging promotion state;
- source-register approval status;
- source-register active-RAG status.

No source was ingested, approved, indexed, retrieved from, answered from or promoted into Organizational RAG.

## Risks and blockers

- Source-owner evidence has not been collected.
- Named source owners remain unconfirmed across all five records.
- Organization confirmation remains missing across all five records.
- Independent reviewer assignment remains missing across all five records.
- Data-governance decision path is explicit only for the Digital Health/Data Governance record; the other four records need explicit data-governance routing before later packet collection can reduce the role-readiness gap.
- The confirmation gap remains 70% until accountable source owners fill the packet and reviewers verify it.

## Stage result

```text
M1_B_BASELINE_COMPLETED = true
BASELINE_ROLE_READINESS_MEASURED = true
ROLE_COVERAGE_GAP_DEFINED = true
ROLE_READINESS_GAP_RATE = 54.3%
FULLY_ROLE_READY_RECORDS = 0 / 5
SOURCE_APPROVAL_CLAIMED = false
SOURCE_INGESTION_CLAIMED = false
RAG_ACTIVATION_CLAIMED = false
```

## Single next stage

RESEARCH — identify the minimum authority, role-assignment and reviewer-routing evidence needed to reduce the role-readiness gap without collecting source-owner evidence, modifying the source register, starting ingestion planning or activating RAG.
