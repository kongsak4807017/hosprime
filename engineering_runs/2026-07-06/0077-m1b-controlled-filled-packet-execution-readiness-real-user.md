# HosPrime Engineering Run 0077 — M1-B Controlled Filled-Packet Execution Readiness Real User

Date: 2026-07-06
Stage: REAL USER
Parent issue: #10
Memory epic: #8
Control issue: #95
Previous stage: REAL PROBLEM (#94)
Next stage: BASELINE

## North Star outcome supported

Enable healthcare and public-health organizations to use trusted data, knowledge, organizational memory and governed AI to complete real work and make better decisions faster, with evidence, accountability and continuous learning.

This bounded REAL USER stage supports Trusted Task Completion Rate, evidence quality, user trust, decision-to-outcome traceability, knowledge reuse, cost per accepted task discipline and zero unauthorized high-impact action by identifying who the controlled filled-packet execution-readiness workflow serves and what each role may or may not decide.

## Repository evidence checked before selecting work

- `README.md` on `main` was read before work selection and confirms the North Star, ordered Loop Engineering sequence, Core Rules, memory boundaries and current controlled release target: Milestone 1 — Governed Knowledge Oracle MVP.
- Open issue #95 is the active ordered M1-B stage: REAL USER after #94 REAL PROBLEM.
- Recent open issues were inspected. #95 is the current M1-B control issue; #10 remains the governed backoffice pipeline parent.
- Recent pull requests inspected: latest visible PRs include #33, #13, #12, #7 and #1; no open execution PR was selected for this bounded stage.
- CI status checked for previous commit `e6947db6a1009d2ca998c3169706f50824308aa8`: combined status returned no statuses; CI pass is not claimed.
- Previous REAL PROBLEM evidence inspected: `engineering_runs/2026-07-06/0076-m1b-controlled-filled-packet-execution-readiness-real-problem.md`.
- Controlled workflow inspected: `docs/governance/M1_B_CONTROLLED_FILLED_PACKET_EXECUTION_WORKFLOW.md`.
- Source register inspected: `data/source_register/m1_source_register.yml` still contains five DISCOVERED placeholder records only, with no approved source and no active RAG index.

## Current loop stage

```text
CURRENT_STAGE = REAL_USER
PREVIOUS_STAGE = REAL_PROBLEM
NEXT_STAGE = BASELINE
```

## Real user set for controlled filled-packet execution readiness

This stage identifies the exact role users served by the next controlled source-owner evidence-collection readiness cycle. These are role-level users only; this run does not assign named people, collect source evidence, approve sources, or modify the source register.

| Real user | Real organizational work problem | Decision-rights boundary | Non-approval responsibility |
|---|---|---|---|
| Public-health executive / accountable sponsor | Needs to know whether priority knowledge packs can safely move toward governed evidence review without unapproved factual-answer use. | May authorize the need for collection-readiness work and accept readiness metrics. May not approve source content, bypass reviewer routing, activate RAG, or claim organizational truth. | Confirms organizational priority and sponsor accountability for later packet execution. |
| Provincial program source owner | Owns program context for PM2.5, TB, NCD, EOC or Digital Health evidence but the register still lacks owner-person assignment and controlled source facts. | May confirm source ownership, controlled source location, source period/version and classification intent. May not self-approve the source for Organizational RAG. | Provides or routes accountable facts required for the ten packet field groups. |
| Source inventory operator | Needs a controlled method to locate files/systems, record version/source period and support checksum or pending-checksum status. | May record inventory facts and technical metadata as collection-readiness evidence. May not change lifecycle state, review status, approval status or active RAG state in this stage. | Preserves file identity, location, checksum boundary and provenance limitations. |
| Data governance lead | Needs access, classification, retention and role-scope boundaries before evidence can move toward review. | May verify or route classification and access-policy questions. May not loosen restricted access without authorized review evidence. | Maintains separation of restricted/internal sources and prevents unauthorized high-impact use. |
| Knowledge reviewer / independent reviewer | Needs a reviewer route and conflict-of-interest boundary before later source review can occur. | May perform or route a later collection-readiness precheck. In this stage, no review decision is executed and no source approval is claimed. | Defines review gate readiness, escalation path and non-approval decision boundary. |

## Source-specific real-user mapping

The five source-register seed records remain DISCOVERED placeholders. The real users for later collection-readiness execution are mapped by role, not by named person:

```text
M1A-PM25-001 -> environmental_health_lead + executive + knowledge_reviewer + data_governance_lead + source_inventory_operator
M1A-TB-001 -> communicable_disease_lead + executive + knowledge_reviewer + data_governance_lead + source_inventory_operator
M1A-NCD-001 -> ncd_program_lead + executive + knowledge_reviewer + data_governance_lead + source_inventory_operator
M1A-EOC-001 -> eoc_lead + executive + knowledge_reviewer + data_governance_lead + source_inventory_operator
M1A-DIGITAL-001 -> digital_health_lead / data_governance_lead + executive + knowledge_reviewer + source_inventory_operator
```

No source ID outside the register is in scope.

## Decision-rights boundaries

```text
CAN_DEFINE_COLLECTION_READINESS_USER_ROLES = true
CAN_DEFINE_NON_APPROVAL_RESPONSIBILITIES = true
CAN_DEFINE_NEXT_BASELINE_MEASUREMENT_NEED = true
CAN_ASSIGN_NAMED_SOURCE_OWNER_WITHOUT HUMAN RECORD = false
CAN_COLLECT_SOURCE_OWNER_EVIDENCE_IN_THIS_STAGE = false
CAN_MODIFY_SOURCE_REGISTER_IN_THIS_STAGE = false
CAN_CLAIM_SOURCE_APPROVAL = false
CAN_CLAIM_REVIEW_PENDING_STATE = false
CAN_CLAIM_INDEX_READY_OR_INDEXED_STATE = false
CAN_CLAIM_ACTIVE_RAG_OR_FACTUAL_ANSWER_PERMISSION = false
CAN_PROMOTE_TO_ORGANIZATIONAL_MEMORY = false
```

## Baseline and target metric carried forward

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

The next BASELINE stage must measure the current role/user decision-rights gaps against the ten controlled packet field groups before any packet evidence is opened or filled.

## Acceptance result

```text
M1_B_REAL_USER_COMPLETED = true
REAL_USERS_DEFINED_FOR_CONTROLLED_FILLED_PACKET_EXECUTION_READINESS = true
DECISION_RIGHTS_BOUNDARIES_DEFINED = true
NON_APPROVAL_RESPONSIBILITIES_DEFINED = true
SOURCE_REGISTER_MODIFIED = false
SOURCE_OWNER_EVIDENCE_COLLECTED = false
SOURCE_APPROVAL_CLAIMED = false
RAG_ACTIVATION_CLAIMED = false
FACTUAL_ANSWER_PERMISSION_CLAIMED = false
ORGANIZATIONAL_MEMORY_PROMOTION_CLAIMED = false
CI_PASS_CLAIMED = false
NEXT_STAGE = BASELINE
```

## Memory layer affected

Affected:

- engineering-run evidence;
- issue traceability.

Not affected:

- Personal / Staff Twin Memory;
- Person Memory;
- Role Memory as durable operational truth;
- Organizational Memory / Governed RAG;
- Research Staging promotion;
- source-register lifecycle state;
- source-register approval status;
- source-register active-RAG status.

## Risks and blockers

```text
RISK_NAMED_SOURCE_OWNER_ASSIGNMENT_PENDING = true
RISK_CONTROLLED_LOCATION_PENDING = true
RISK_VERSION_OR_SOURCE_PERIOD_PENDING = true
RISK_CHECKSUM_PENDING = true
RISK_REVIEWER_ASSIGNMENT_PENDING = true
RISK_ROLE_MAPPING_COULD_BE_MISREAD_AS_APPROVAL = true
CI_STATUS_COUNT_FOR_PREVIOUS_COMMIT = 0
```

## Single next stage

BASELINE — measure the current decision-rights and field-group readiness gaps for the defined real-user roles and five seed records before any source-owner evidence is opened, filled, reviewed, approved, ingested, indexed or activated.
