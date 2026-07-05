# HosPrime Engineering Run 0076 — M1-B Controlled Filled-Packet Execution Readiness Real Problem

Date: 2026-07-06
Stage: REAL PROBLEM
Parent issue: #10
Memory epic: #8
Control issue: #94
Previous stage: NEXT GOAL (#93)
Next stage: REAL USER

## North Star outcome supported

Enable healthcare and public-health organizations to use trusted data, knowledge, organizational memory and governed AI to complete real work and make better decisions faster, with evidence, accountability and continuous learning.

This bounded REAL PROBLEM stage supports Trusted Task Completion Rate, evidence quality, user trust, decision-to-outcome traceability, knowledge reuse, cost per accepted task discipline and zero unauthorized high-impact action by defining the exact execution-readiness problem before any source-owner packet is opened, filled, reviewed, approved, ingested or activated.

## Repository evidence checked before selecting work

- `README.md` on `main` was read before work selection and confirms the North Star, ordered Loop Engineering sequence, Core Rules, memory boundaries and current controlled release target: Milestone 1 — Governed Knowledge Oracle MVP.
- Open issue #94 is the active ordered M1-B stage: REAL PROBLEM after #93 NEXT GOAL.
- Recent open issues were inspected. #94 is the current M1-B control issue; #10 remains the governed backoffice pipeline parent.
- Recent pull requests inspected: latest visible PRs include #33, #13, #12, #7 and #1; no open execution PR was selected for this bounded stage.
- CI status checked for previous commit `dd89df8f095ed3365388b35880e76c9c18dfc8a4`: no workflow runs returned; CI pass is not claimed.
- Previous NEXT GOAL evidence inspected: `engineering_runs/2026-07-06/0075-m1b-controlled-filled-packet-execution-readiness-next-goal.md`.
- Controlled workflow inspected: `docs/governance/M1_B_CONTROLLED_FILLED_PACKET_EXECUTION_WORKFLOW.md`.
- Release-boundary memory correction inspected: `docs/governance/M1_B_CONTROLLED_FILLED_PACKET_RELEASE_BOUNDARY_MEMORY_CORRECTION.md`.
- Source register inspected: `data/source_register/m1_source_register.yml` still contains five DISCOVERED placeholder records only, with no approved source and no active RAG index.

## Current loop stage

```text
CURRENT_STAGE = REAL_PROBLEM
PREVIOUS_STAGE = NEXT_GOAL
NEXT_STAGE = REAL_USER
```

## Real organizational work problem

The M1 Governed Knowledge Oracle cannot safely progress from placeholder source inventory toward trustworthy source-owner collection readiness because the five seed records still lack executable accountability facts required for later review routing:

```text
organization = pending_source_owner_confirmation
owner_person = pending_human_assignment
file_or_system_location = pending_inventory
version = pending_inventory
checksum = pending_checksum
reviewer = pending_human_reviewer
review_status = not_reviewed
approval_status = not_approved
active_rag_index = false
```

The real work problem is not that HosPrime needs more documents or agents. The problem is that a public-health organization cannot yet determine who is accountable for each priority knowledge source, where the controlled source is, which version or source period applies, whether file integrity can be verified, what access restrictions apply, and which independent reviewer can later decide whether the source is review-ready. Without that execution-readiness evidence, the Knowledge Oracle must not answer factual organizational questions from these sources.

## Why this is a real organizational problem

Milestone 1 requires approved documents, evidence retrieval, traceable citations, access control, audit and cost data. The current register has the structure for those controls, but the seed records are still only DISCOVERED placeholders. If packet execution begins without a precise problem boundary, staff may confuse collection readiness with approval, review-pending status, index readiness, active RAG or factual-answer permission.

This problem directly affects practical work such as preparing executive briefs, program reviews, EOC lessons, NCD workload analysis, TB control evidence and digital-health governance decisions. In each case, unsupported or unreviewed evidence could reduce user trust and create decision traceability risk.

## Real user and real work need carried into next stage

The next stage must identify the concrete real users and decision-rights boundaries for this problem. Candidate users remain:

- public-health executive / accountable sponsor;
- provincial program source owner;
- source inventory operator;
- data governance lead;
- knowledge reviewer / independent reviewer.

The work need is controlled filled-packet execution readiness for the five existing source IDs only:

```text
M1A-PM25-001
M1A-TB-001
M1A-NCD-001
M1A-EOC-001
M1A-DIGITAL-001
```

No invented source ID, renamed source ID or non-register source may be used.

## Baseline and target metric

Current baseline preserved:

```text
DECISION_RIGHTS_READINESS_GAP_RATE = 50.0%
FULLY_COLLECTION_READY_RECORDS = 0 / 5
FULLY_REVIEW_READY_RECORDS = 0 / 5
FULLY_APPROVED_RECORDS = 0 / 5
ACTIVE_RAG_RECORDS = 0 / 5
```

Target preserved for later filled-packet execution, not achieved in this run:

```text
TARGET_DECISION_RIGHTS_READINESS_GAP_RATE_AFTER_LATER_FILLED_PACKET <= 30%
TARGET_FULLY_COLLECTION_READY_RECORDS_AFTER_LATER_FILLED_PACKET >= 3 / 5
TARGET_FULLY_APPROVED_RECORDS = 0 unless authorized human review evidence exists
TARGET_ACTIVE_RAG_RECORDS = 0 until approved source, retrieval evaluation and activation gate exist
```

## Problem boundary

This REAL PROBLEM stage defines only the problem that must be solved by later ordered stages. It does not collect evidence or execute the packet workflow.

Required boundary assertions:

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
M1_B_REAL_PROBLEM_COMPLETED = true
REAL_PROBLEM_DEFINED_FOR_CONTROLLED_FILLED_PACKET_EXECUTION_READINESS = true
REAL_PROBLEM_LINKED_TO_SOURCE_OWNER_COLLECTION_READINESS = true
REAL_PROBLEM_DOES_NOT_BYPASS_REVIEW_OR_RAG_GATES = true
SOURCE_REGISTER_MODIFIED = false
SOURCE_APPROVAL_CLAIMED = false
RAG_ACTIVATION_CLAIMED = false
NEXT_STAGE = REAL USER
```

## Memory layer affected

Affected:

- engineering-run evidence;
- issue traceability.

Not affected:

- Personal / Staff Twin Memory;
- Person Memory;
- Role Memory;
- Organizational Memory / Governed RAG;
- Research Staging promotion;
- source-register lifecycle state;
- source-register approval status;
- source-register active-RAG status.

## Risks and blockers

```text
RISK_FILLED_PACKET_NOT_YET_EXECUTED = true
RISK_SOURCE_OWNER_ASSIGNMENT_PENDING = true
RISK_CONTROLLED_LOCATION_PENDING = true
RISK_VERSION_OR_SOURCE_PERIOD_PENDING = true
RISK_CHECKSUM_PENDING = true
RISK_REVIEWER_ASSIGNMENT_PENDING = true
RISK_COLLECTION_READINESS_COULD_BE_MISREAD_AS_APPROVAL = true
CI_WORKFLOW_RUNS_RETURNED_FOR_PREVIOUS_COMMIT = 0
```

## Single next stage

REAL USER — identify the exact real users, decision-rights boundaries, accountable owners and non-approval responsibilities for controlled filled-packet execution readiness before any packet evidence is opened or filled.
