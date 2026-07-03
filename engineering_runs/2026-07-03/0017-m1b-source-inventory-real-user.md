# Engineering Run 0017 — M1-B Source Inventory Real User

## Loop stage

REAL USER

## North Star outcome supported

Evidence-based decisions, knowledge continuity, reduced repetitive workload, decision-to-outcome traceability and zero unauthorized high-impact action.

This run supports the North Star by defining the accountable human roles that must confirm whether candidate organizational sources are safe enough to enter a controlled inventory workflow before any ingestion, indexing or factual answering can occur.

## Controlled release target

Milestone 1 — Governed Knowledge Oracle MVP.

## Evidence inspected at start of run

- `README.md` on `main`: North Star, loop sequence, current release target, Core Rules and Memory Boundaries.
- Open issue #35: `M1-B Real User: Define accountable source inventory decision roles`.
- Parent issue #10: `M1/M4: Build Organizational Memory Backoffice Pipeline`.
- Parent epic #8: `Epic: Loop Engineering and Two-Layer Memory Runtime`.
- Source register: `data/source_register/m1_source_register.yml`.
- Recent engineering run `engineering_runs/2026-07-03/0016-m1b-controlled-source-inventory-real-problem.md`.
- Recent pull requests were inspected; PR #33 is the latest relevant merged test-gate PR and no newer open PR superseded #35.

No external research was required for this stage because the work is an internal governance responsibility definition, not a material external fact claim.

## Real organizational problem carried forward

HosPrime cannot safely begin controlled ingestion planning while the five M1 source-register records remain placeholders without accountable source inventory evidence.

The source register confirms that all five seed records still have:

```text
organization = pending_source_owner_confirmation
owner_person = pending_human_assignment
file_or_system_location = pending_inventory
version = pending_inventory
checksum = pending_checksum
review_status = not_reviewed
approval_status = not_approved
active_rag_index = false
```

## Real users defined

The accountable source-inventory workflow has five real user roles.

### 1. Executive Sponsor

Primary organizational user who authorizes the controlled source-inventory effort as a legitimate organizational workstream.

Decision rights:

- Confirms the inventory purpose supports Milestone 1 and a real executive/public-health work problem.
- Confirms the organizational unit or program scope.
- Resolves conflicts between program owners when ownership is disputed.
- Cannot self-approve source content for Organizational RAG unless also formally recorded as the correct source owner/reviewer under the review boundary.

Non-delegable boundary:

- Must not treat inventory authorization as source approval.
- Must not authorize high-impact factual answering from placeholder records.

### 2. Data Governance Lead

Accountable user for classification, access scope, retention and controlled evidence handling.

Decision rights:

- Confirms classification category for candidate sources.
- Confirms role-scoped access policy and whether restricted handling is required.
- Confirms whether checksum-pending status is acceptable before checksum capture.
- Blocks inventory movement when source handling would violate governance boundaries.

Non-delegable boundary:

- Cannot approve factual authority of source content unless also acting through the documented human review role.
- Cannot move a source to active RAG without review record, approval record and retrieval evaluation gate.

### 3. Knowledge Reviewer

Accountable user for deciding whether inventoried source metadata is sufficient for later review and whether the source may proceed to a future review-pending state.

Decision rights:

- Confirms that source title, version/date, owner, location, limitation note and provenance are sufficient for review.
- Records accept/reject/defer decision for inventory readiness.
- Records conflicts, uncertainty, superseded versions or missing evidence.

Non-delegable boundary:

- Review readiness is not source approval.
- A source remains non-approved until an authorized review decision explicitly approves it under the review boundary.

### 4. Program / Source Owner

Accountable user who owns the actual organizational source set.

Decision rights:

- Confirms source owner role and named accountable owner.
- Confirms controlled file or system location.
- Confirms source version, date range or latest authoritative copy.
- Confirms whether the source contains sensitive operational, personal, restricted or draft content.
- Confirms whether the source is current, obsolete, superseded or disputed.

Non-delegable boundary:

- Source ownership confirmation is not approval for active retrieval or factual answering.
- Program owner confirmation cannot bypass data governance classification or knowledge review.

### 5. Future Knowledge Oracle Implementer

Technical user responsible for implementing the later inventory, parsing, retrieval and evaluation workflow without bypassing governance.

Decision rights:

- Confirms technical feasibility of recording location, checksum, parsing status and future test hooks.
- Identifies required technical evidence for later baseline, build and test stages.
- Flags implementation blockers such as missing file access, unsupported format or unsafe storage.

Non-delegable boundary:

- Cannot self-approve sources.
- Cannot ingest, embed, index, retrieve from or answer from placeholder records before authorized gates pass.

## Minimum role-to-confirmation matrix

| Inventory confirmation item | Accountable role | Required before baseline? | Boundary |
|---|---|---:|---|
| Inventory purpose and organizational scope | Executive Sponsor | Yes | Not source approval |
| Source owner role and named owner | Program / Source Owner | Yes | Not RAG activation |
| Controlled file or system location | Program / Source Owner | Yes | No parsing yet |
| Version/date or latest authoritative copy | Program / Source Owner | Yes | No factual answer yet |
| Classification and restricted handling | Data Governance Lead | Yes | No access bypass |
| Access policy scope | Data Governance Lead | Yes | No retrieval activation |
| Review sufficiency decision path | Knowledge Reviewer | Yes | Readiness only, not approval |
| Technical feasibility and evidence hooks | Future Knowledge Oracle Implementer | Yes | No ingestion/indexing yet |

## Work decision clarified

The real users are responsible for answering this bounded decision:

```text
Which candidate organizational sources are safe enough to enter a controlled inventory workflow for later review, without yet approving, ingesting, indexing or using them for answers?
```

A candidate source may proceed to the next BASELINE stage only when the repository can measure whether these confirmations are present or missing.

## Baseline inherited from #34 and #35

```text
SOURCE_REGISTER_EXISTS = true
SEED_RECORDS_PRESENT = 5
APPROVED_PLACEHOLDER_SOURCES = 0 / 5
ACTIVE_RAG_INDEXED_RECORDS = 0 / 5
SOURCE_OWNER_CONFIRMATION_MISSING = true
CONTROLLED_FILE_LOCATION_MISSING = true
CHECKSUM_EVIDENCE_MISSING = true
CLASSIFICATION_CONFIRMATION_MISSING = true
ACCESS_POLICY_CONFIRMATION_MISSING = true
HUMAN_REVIEW_RECORD_MISSING = true
ACTIVE_RAG_INDEXING_ALLOWED = false
```

## Target metric for this stage

```text
M1_B_REAL_USER_DEFINED = true
ACCOUNTABLE_SOURCE_INVENTORY_ROLES_DEFINED = true
DECISION_RIGHTS_DEFINED = true
INGESTION_PLANNING_ALLOWED = false
SOURCE_APPROVAL_CLAIMED = false
RAG_ACTIVATION_CLAIMED = false
NEXT_STAGE = BASELINE
```

## Stage result

```text
M1_B_REAL_USER_DEFINED = true
ACCOUNTABLE_SOURCE_INVENTORY_ROLES_DEFINED = true
DECISION_RIGHTS_DEFINED = true
NON_DELEGABLE_HUMAN_BOUNDARIES_DEFINED = true
BASELINE_STAGE_READY = true
INGESTION_PLANNING_ALLOWED = false
SOURCE_APPROVAL_CLAIMED = false
RAG_ACTIVATION_CLAIMED = false
```

## Work completed

- Defined the accountable real users for M1-B source inventory confirmation.
- Defined decision rights and non-delegable boundaries for each role.
- Defined the minimum role-to-confirmation matrix required before measurement.
- Preserved the boundary that placeholders are not approved evidence.
- Prepared the next ordered stage as BASELINE.

## Test / CI status

```text
DOC_AND_ISSUE_ONLY_CHANGE = true
PYTEST_REQUIRED_FOR_THIS_STAGE = false
CI_PASS_CLAIMED_FOR_THIS_STAGE = false
PR_REQUIRED_FOR_THIS_STAGE = false
PRIOR_M1_SOURCE_REGISTER_CI_GATE = passed in earlier TEST stage
```

This run does not claim new executable test success because the bounded work was a governance role-definition stage.

## Memory layer affected

```text
Personal / Staff Twin Memory = not modified
Person Memory = not modified
Role Memory = not modified
Research Staging = not modified
Organizational Memory / Governed RAG = not modified; no source promoted
Repository engineering evidence = updated
Repository issue control path = updated
```

## Safety boundary

No source was ingested, parsed, embedded, approved, indexed, retrieved from, answered from or promoted into Organizational RAG.

No external findings were promoted into organizational truth.

No real-world execution was claimed.

## Risks and blockers

```text
NAMED_HUMAN_ASSIGNMENTS_MISSING = true
SOURCE_OWNER_CONFIRMATION_MISSING = true
CONTROLLED_FILE_LOCATION_MISSING = true
CHECKSUM_EVIDENCE_MISSING = true
CLASSIFICATION_CONFIRMATION_MISSING = true
ACCESS_POLICY_CONFIRMATION_MISSING = true
HUMAN_REVIEW_RECORD_MISSING = true
RETRIEVAL_EVALUATION_MISSING = true
ACTIVE_RAG_INDEXING_ALLOWED = false
```

## Completion criteria

```text
M1_B_REAL_USER_DEFINED = true
ACCOUNTABLE_SOURCE_INVENTORY_ROLES_DEFINED = true
DECISION_RIGHTS_DEFINED = true
ISSUE_35_CAN_CLOSE_AS_COMPLETED = true
INGESTION_PLANNING_ALLOWED = false
SOURCE_APPROVAL_CLAIMED = false
RAG_ACTIVATION_CLAIMED = false
```

## Next single stage

BASELINE — measure which source-inventory confirmations are present or missing for each of the five placeholder source-register records before any research, hypothesis, plan, build or ingestion work begins.
