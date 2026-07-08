# M1-B Source-Owner Evidence Packet Completion Workflow

Status: released controlled non-authorizing guidance

Release target: Milestone 1 — Governed Knowledge Oracle MVP

Controlling issues: #145 BUILD, #148 REVIEW, #149 RELEASE

Release evidence:

- `engineering_runs/2026-07-08/0130-m1b-source-owner-evidence-packet-completion-review.md`
- `engineering_runs/2026-07-08/0131-m1b-source-owner-evidence-packet-completion-release.md`

Previous loop evidence:

- `engineering_runs/2026-07-08/0126-m1b-source-owner-evidence-packet-completion-plan.md`
- `engineering_runs/2026-07-08/0125-m1b-source-owner-evidence-packet-completion-hypothesis.md`
- `data/source_register/m1_source_register.yml`
- `README.md`

## 1. Purpose

This workflow converts the M1-B plan into a controlled, role-based, receipt-driven packet completion artifact for the five Milestone 1 seed records.

It is designed to help healthcare and public-health organizations prepare source-owner evidence packets before any later human review, approval, ingestion, indexing, active RAG use, Organizational Memory promotion, factual-answer permission, or real-world execution claim.

This released guidance is non-authorizing. It may be used only to structure later packet-completion work that has its own authorized collection route, receipt evidence, review gate, and audit record.

## 2. Non-authorization boundary

This artifact is guidance and workflow control only.

It does not authorize:

- mutation of `data/source_register/m1_source_register.yml`;
- collection of source-owner evidence;
- naming real source-owner persons;
- source approval;
- ingestion, parsing, embedding, indexing, or active RAG activation;
- promotion from Research Staging into Organizational Memory or Governed RAG;
- factual-answer permission;
- CI pass claims;
- real-world execution or organizational action completion claims.

Default-false control flags:

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

## 3. Real users

This workflow is for role-based handoff among:

- public-health executive sponsor;
- data governance lead;
- provincial program source owner;
- source inventory operator;
- independent knowledge reviewer;
- technical ingestion operator.

The workflow records role responsibility only. It must not introduce real person names unless a later authorized human assignment receipt exists.

## 4. Baseline retained

```text
SEED_RECORDS_COUNT = 5
FILLED_SOURCE_OWNER_PACKET_COUNT = 0 / 5
SOURCE_OWNER_PACKET_READINESS_RATE = 0%
AUTHORIZED_COLLECTION_ROUTE_COMPLETENESS_RATE = 0%
SOURCE_RECORDS_WITH_APPROVAL_STATUS_APPROVED = 0 / 5
SOURCE_RECORDS_WITH_ACTIVE_RAG_INDEX = 0 / 5
```

## 5. Target enabled by this workflow

Later packet-completion work can target:

```text
AUTHORIZED_COLLECTION_ROUTE_COMPLETENESS_RATE_TARGET = 100% for 5/5 seed records
SOURCE_OWNER_PACKET_READINESS_RATE_TARGET = 100% for 5/5 seed records only after authorized packet completion and review-ready receipt evidence
SOURCE_RECORDS_WITH_APPROVAL_STATUS_APPROVED_TARGET = 0/5 until a separate review and approval stage
SOURCE_RECORDS_WITH_ACTIVE_RAG_INDEX_TARGET = 0/5 until a separate ingestion/indexing/release path
```

This released workflow does not achieve those later targets. It only creates the workflow controls needed to attempt them safely in later stages.

## 6. Packet completion workflow

| Packet field group | Authorized collection route requirement | Required receipt artifact | Responsible role | Reviewer handoff condition | Fail-closed rule |
|---|---|---|---|---|---|
| 1. Source identity and title | Use a controlled source inventory request linked to one seed `source_id`. | Inventory request receipt with source title and source type. | Source inventory operator | Source identity matches one seed record and duplicate risk is checked. | Stop if source identity is ambiguous, duplicated, or not linked to a seed record. |
| 2. Knowledge pack and work purpose | Use the Milestone 1 governance intake route. | Purpose statement receipt linking the source to a real organizational work problem. | Data governance lead | Purpose maps to Milestone 1 and a North Star outcome. | Stop if the source is added only for volume or unclear future use. |
| 3. Owner office and owner role | Use official program or governance owner nomination route. | Role-based owner nomination receipt without owner-person evidence. | Provincial program source owner or data governance lead | Owner office and owner role are present and role-scoped. | Stop if only a personal name is provided without accountable role or office context. |
| 4. Owner-person evidence boundary | Use a separate human assignment and consent/authorization route; do not use the packet-planning route. | Pending-human-assignment acknowledgement or later signed assignment receipt. | Data governance lead | Named person evidence is absent by design or explicitly authorized in a later stage. | Stop if a named person is introduced without authorized assignment evidence. |
| 5. Controlled file or system location | Use an approved inventory channel for controlled files or systems. | Controlled-location receipt or pending-location reason. | Source inventory operator | Location is traceable or a pending reason is documented. | Stop if location is informal, personal-only, inaccessible to reviewers, or unverifiable. |
| 6. Version, source period, and freshness | Use source-owner confirmation route for version and source period. | Version/source-period receipt or pending-version reason. | Provincial program source owner | Version or source-period status is explicit before reviewer handoff. | Stop if freshness, version, or source period is unknown and no pending reason is recorded. |
| 7. Checksum and integrity evidence | Use technical inventory route only after controlled file access is authorized. | Checksum receipt, checksum method, or checksum-pending reason. | Technical ingestion operator | Integrity evidence or pending reason is available before quality review. | Stop if checksum is claimed without file access, method, or receipt. |
| 8. Classification and access policy | Use data governance classification route. | Classification/access-policy receipt. | Data governance lead | Classification, access policy, and allowed roles are reviewable before ingestion. | Stop if access scope is missing, overbroad, or inconsistent with source sensitivity. |
| 9. Limitation, conflict, and sensitivity notes | Use source-owner plus reviewer pre-review route. | Limitation/conflict/sensitivity note receipt. | Independent knowledge reviewer with source-owner input | Known limitations and conflicts are documented before Knowledge Oracle use. | Stop if limitations are blank, minimized, or treated as approval evidence. |
| 10. Review and approval readiness status | Use reviewer handoff route after all readiness receipts are present. | Review-ready handoff receipt, not approval receipt. | Independent knowledge reviewer | Packet can enter review queue while source remains not approved. | Stop if readiness is represented as approval, ingestion permission, active RAG, or factual-answer permission. |

## 7. Reviewer handoff minimum

A packet may be handed to an independent knowledge reviewer only when all of the following are true:

```text
SOURCE_ID_LINKED_TO_SEED_RECORD = true
SOURCE_PURPOSE_LINKED_TO_REAL_WORK_PROBLEM = true
OWNER_OFFICE_OR_OWNER_ROLE_PRESENT = true
CONTROLLED_LOCATION_OR_PENDING_REASON_PRESENT = true
VERSION_OR_SOURCE_PERIOD_OR_PENDING_REASON_PRESENT = true
CHECKSUM_OR_CHECKSUM_PENDING_REASON_PRESENT = true
CLASSIFICATION_AND_ACCESS_POLICY_PRESENT = true
LIMITATION_CONFLICT_SENSITIVITY_NOTES_PRESENT = true
READINESS_RECEIPTS_PRESENT = true
APPROVAL_CLAIMED = false
RAG_ACTIVATION_CLAIMED = false
ORGANIZATIONAL_MEMORY_PROMOTION_CLAIMED = false
```

## 8. Approval boundary

Readiness is not approval.

A review-ready packet may enter a later review stage, but source approval requires a separate authenticated human review record, approval decision, decision date, and audit evidence. This workflow must not convert packet readiness into `APPROVED` lifecycle state or `approval_status: approved`.

## 9. RAG boundary

Packet completion is not ingestion or active retrieval permission.

No source may be parsed, embedded, indexed, or activated in RAG from this workflow alone. Active RAG use requires a later approved source lifecycle state and a separate ingestion/indexing/release control path.

## 10. Memory boundary

Packet workflow artifacts remain engineering-run evidence and governance documentation.

They do not promote personal evidence, named person assignments, or external findings into Organizational Memory or Governed RAG. Research Staging and Organizational Memory remain separated until a reviewed promotion record exists.

## 11. Safe failure handling

If any required route, receipt, role, handoff condition, or boundary is missing, the packet remains blocked and the accountable role records:

```text
BLOCKED = true
BLOCKER_TYPE = missing_authorized_route | missing_receipt | missing_role | missing_handoff_condition | boundary_violation_risk
ACCOUNTABLE_ROLE = <role only, no person name>
NEXT_EXECUTABLE_STEP = <single bounded step>
SOURCE_REGISTER_MODIFIED = false
SOURCE_APPROVAL_CLAIMED = false
RAG_ACTIVATION_CLAIMED = false
```

## 12. RELEASE acceptance status

```text
M1_B_RELEASE_COMPLETED = true
SOURCE_OWNER_PACKET_COMPLETION_WORKFLOW_RELEASED = true
RELEASE_SCOPE = controlled_non_authorizing_guidance_only
GUIDANCE_DISCOVERABLE_IN_DOC = true
REVIEW_EVIDENCE_LINKED = true
RELEASE_EVIDENCE_LINKED = true
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
NEXT_STAGE = OBSERVE
```

## 13. Single next stage

OBSERVE — observe whether the released guidance is discoverable and unambiguous for later authorized packet-completion planning, without executing packet completion, mutating the source register, collecting source-owner evidence, approving sources, activating RAG, promoting Organizational Memory, claiming CI success, or claiming real-world execution completion.
