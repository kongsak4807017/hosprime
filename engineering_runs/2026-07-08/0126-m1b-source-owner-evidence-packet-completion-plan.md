# HosPrime Loop Engineering Run 0126 — M1-B Source-Owner Evidence Packet Completion Plan

Date: 2026-07-08

Stage: PLAN

Controlling issue: #144

Previous stage: HYPOTHESIS (#143)

Next stage candidate: BUILD

Release target: Milestone 1 — Governed Knowledge Oracle MVP

## 1. North Star outcome supported

This run supports the HosPrime North Star by planning a controlled, role-based, receipt-driven path for completing source-owner evidence packets before any source can be approved, ingested, indexed, activated in RAG, or promoted into Organizational Memory.

Supported outcomes:

- Evidence-based decisions
- Knowledge continuity
- Closed execution loop
- Continuous organizational learning

Primary metric linkage: Trusted Task Completion Rate.

## 2. Real user and real organizational work problem

Real users retained from the prior stages:

- Public-health executive sponsor
- Data governance lead
- Provincial program source owner
- Source inventory operator
- Independent knowledge reviewer
- Technical ingestion operator

Real organizational work problem:

The five M1 seed source-register records are discovered placeholders only. The organization needs a bounded plan for moving from placeholder records toward review-ready source-owner packets while preserving governance separation among packet readiness, human approval, ingestion/indexing, active RAG use, Organizational Memory promotion, and real-world execution claims.

## 3. Baseline and target metric

Baseline retained from #141, #142, and #143:

```text
SEED_RECORDS_COUNT = 5
FILLED_SOURCE_OWNER_PACKET_COUNT = 0 / 5
SOURCE_OWNER_PACKET_READINESS_RATE = 0%
AUTHORIZED_COLLECTION_ROUTE_COMPLETENESS_RATE = 0%
SOURCE_RECORDS_WITH_APPROVAL_STATUS_APPROVED = 0 / 5
SOURCE_RECORDS_WITH_ACTIVE_RAG_INDEX = 0 / 5
```

Target for this PLAN stage only:

```text
TEN_PACKET_FIELD_GROUPS_MAPPED_TO_WORKFLOW = true
AUTHORIZED_COLLECTION_ROUTE_REQUIREMENTS_DEFINED = true
RECEIPT_ARTIFACT_REQUIREMENTS_DEFINED = true
RESPONSIBLE_ROLE_REQUIREMENTS_DEFINED = true
REVIEWER_HANDOFF_CONDITIONS_DEFINED = true
FAIL_CLOSED_RULES_DEFINED = true
SOURCE_REGISTER_MODIFIED = false
SOURCE_OWNER_EVIDENCE_COLLECTED = false
SOURCE_OWNER_PERSON_NAMED = false
SOURCE_APPROVAL_CLAIMED = false
RAG_ACTIVATION_CLAIMED = false
REAL_WORLD_EXECUTION_CLAIMED = false
```

Later measurable target enabled by this plan, not achieved in this run:

```text
AUTHORIZED_COLLECTION_ROUTE_COMPLETENESS_RATE_TARGET = 100% for 5/5 seed records
SOURCE_OWNER_PACKET_READINESS_RATE_TARGET = 100% for 5/5 seed records only after authorized packet completion and review-ready receipt evidence
SOURCE_RECORDS_WITH_APPROVAL_STATUS_APPROVED_TARGET = 0/5 until a separate review and approval stage
SOURCE_RECORDS_WITH_ACTIVE_RAG_INDEX_TARGET = 0/5 until a separate ingestion/indexing/release path
```

## 4. Repository evidence inspected

- `README.md` confirms the North Star, current Milestone 1 release target, ordered loop, core rules, and memory boundaries.
- `data/source_register/m1_source_register.yml` confirms five seed records and their discovered-only state.
- `engineering_runs/2026-07-08/0125-m1b-source-owner-evidence-packet-completion-hypothesis.md` defines the testable hypothesis for this plan.
- Issue #144 defines the bounded PLAN scope.
- Open PR inspection found no open pull requests during this run.
- Workflow-run inspection for commit `5e574bf0e1dace8ab9729087cd827d9f991a60d4` returned no workflow runs; therefore this run does not claim CI pass.

## 5. Bounded plan

The next BUILD stage should create a controlled workflow artifact for M1-B source-owner packet completion. The artifact should be a non-authorizing operational plan or template under governance documentation. It must not mutate `data/source_register/m1_source_register.yml` and must not contain real owner-person names, actual source files, or approval claims.

The workflow must map each minimum packet field group to:

1. authorized collection route;
2. required receipt artifact;
3. responsible role;
4. reviewer handoff condition;
5. fail-closed rule.

## 6. Ten packet field groups mapped to workflow controls

| Packet field group | Authorized collection route | Required receipt artifact | Responsible role | Reviewer handoff condition | Fail-closed rule |
|---|---|---|---|---|---|
| 1. Source identity and title | Controlled source inventory request linked to the seed `source_id` | Inventory request receipt with source title and source type | Source inventory operator | Source identity matches one seed record and duplicate risk is checked | Stop if source identity is ambiguous, duplicated, or not linked to a seed record |
| 2. Knowledge pack and work purpose | Milestone 1 governance intake route | Purpose statement receipt linking source to a real organizational work problem | Data governance lead | Purpose maps to Milestone 1 and North Star outcome | Stop if the source is added only for volume or unclear future use |
| 3. Owner office and owner role | Official program or governance owner nomination route | Role-based owner nomination receipt without naming owner-person evidence | Provincial program source owner or data governance lead | Owner office and owner role are present and role-scoped | Stop if only a personal name is provided without accountable role/office context |
| 4. Owner-person evidence boundary | Separate human assignment and consent/authorization route, not the packet-planning route | Pending-human-assignment acknowledgement or later signed assignment receipt | Data governance lead | Named person evidence is either absent by design or explicitly authorized in a later stage | Stop if a named person is introduced without authorized assignment evidence |
| 5. Controlled file or system location | Approved inventory channel for controlled files/systems | Controlled-location receipt or pending-location reason | Source inventory operator | Location is traceable or pending reason is documented | Stop if the location is informal, personal-only, inaccessible to reviewers, or unverifiable |
| 6. Version, source period, and freshness | Source-owner confirmation route for version/date range | Version/source-period receipt or pending-version reason | Provincial program source owner | Version or source-period status is explicit before reviewer handoff | Stop if freshness, version, or source period is unknown and no pending reason is recorded |
| 7. Checksum and integrity evidence | Technical inventory route after controlled file access is authorized | Checksum receipt, checksum method, or checksum-pending reason | Technical ingestion operator | Integrity evidence or pending reason is available before quality review | Stop if checksum is claimed without file access, method, or receipt |
| 8. Classification and access policy | Data governance classification route | Classification/access-policy receipt | Data governance lead | Classification, access policy, and allowed roles are reviewable before ingestion | Stop if access scope is missing, overbroad, or inconsistent with source sensitivity |
| 9. Limitation, conflict, and sensitivity notes | Source-owner plus reviewer pre-review route | Limitation/conflict/sensitivity note receipt | Independent knowledge reviewer with source owner input | Known limitations and conflicts are documented before Knowledge Oracle use | Stop if limitations are blank, minimized, or treated as approval evidence |
| 10. Review and approval readiness status | Reviewer handoff route after all readiness receipts are present | Review-ready handoff receipt, not approval receipt | Independent knowledge reviewer | Packet can enter review queue but source remains not approved | Stop if readiness is represented as approval, ingestion permission, active RAG, or factual-answer permission |

## 7. Required build artifact behavior

The next BUILD artifact should include explicit default-false flags:

```text
SOURCE_REGISTER_MODIFIED = false
SOURCE_OWNER_EVIDENCE_COLLECTED = false
SOURCE_OWNER_PERSON_NAMED = false
SOURCE_APPROVAL_CLAIMED = false
SOURCE_INGESTION_CLAIMED = false
SOURCE_PARSING_CLAIMED = false
SOURCE_EMBEDDING_CLAIMED = false
SOURCE_INDEXING_CLAIMED = false
RAG_ACTIVATION_CLAIMED = false
ORGANIZATIONAL_MEMORY_PROMOTION_CLAIMED = false
FACTUAL_ANSWER_PERMISSION_CLAIMED = false
CI_PASS_CLAIMED = false
REAL_WORLD_EXECUTION_CLAIMED = false
```

## 8. Acceptance checks for next BUILD stage

The BUILD stage should be considered acceptable only if it creates a controlled artifact that satisfies all checks below without violating boundaries:

```text
BUILD_ARTIFACT_CREATED = true
TEN_PACKET_FIELD_GROUPS_INCLUDED = true
AUTHORIZED_COLLECTION_ROUTE_REQUIREMENTS_INCLUDED = true
RECEIPT_ARTIFACT_REQUIREMENTS_INCLUDED = true
RESPONSIBLE_ROLE_REQUIREMENTS_INCLUDED = true
REVIEWER_HANDOFF_CONDITIONS_INCLUDED = true
FAIL_CLOSED_RULES_INCLUDED = true
APPROVAL_BOUNDARY_EXPLICIT = true
RAG_BOUNDARY_EXPLICIT = true
MEMORY_BOUNDARY_EXPLICIT = true
SOURCE_REGISTER_MODIFIED = false
```

## 9. Limitations

- This plan does not collect source-owner evidence.
- This plan does not name real source-owner persons.
- This plan does not approve any source.
- This plan does not change the source register.
- This plan does not ingest, parse, embed, index, or activate RAG.
- This plan does not promote Research Staging into Organizational Memory.
- This plan does not grant factual-answer permission.
- This plan does not claim CI pass.
- This plan does not claim real-world execution or completed organizational action.

## 10. Memory layer affected

Affected:

- Research Staging
- Engineering-run evidence
- Issue traceability

Not affected:

- Personal / Staff Twin Memory
- Person Memory
- Role Memory
- Organizational Memory / Governed RAG
- Source-register lifecycle state
- Source-register review status
- Source-register approval status
- Source-register active-RAG state

## 11. Result

```text
M1_B_PLAN_COMPLETED = true
TEN_PACKET_FIELD_GROUPS_MAPPED_TO_WORKFLOW = true
AUTHORIZED_COLLECTION_ROUTE_REQUIREMENTS_DEFINED = true
RECEIPT_ARTIFACT_REQUIREMENTS_DEFINED = true
RESPONSIBLE_ROLE_REQUIREMENTS_DEFINED = true
REVIEWER_HANDOFF_CONDITIONS_DEFINED = true
FAIL_CLOSED_RULES_DEFINED = true
BUILD_ACCEPTANCE_CHECKS_DEFINED = true
SOURCE_REGISTER_MODIFIED = false
SOURCE_OWNER_EVIDENCE_COLLECTED = false
SOURCE_OWNER_PERSON_NAMED = false
SOURCE_APPROVAL_CLAIMED = false
SOURCE_INGESTION_CLAIMED = false
SOURCE_PARSING_CLAIMED = false
SOURCE_EMBEDDING_CLAIMED = false
SOURCE_INDEXING_CLAIMED = false
RAG_ACTIVATION_CLAIMED = false
ORGANIZATIONAL_MEMORY_PROMOTION_CLAIMED = false
FACTUAL_ANSWER_PERMISSION_CLAIMED = false
CI_PASS_CLAIMED = false
REAL_WORLD_EXECUTION_CLAIMED = false
```

## 12. Single next stage

BUILD — create the controlled non-authorizing workflow artifact for role-based, receipt-driven source-owner packet completion, using the ten field-group mappings and fail-closed rules defined in this PLAN stage.
