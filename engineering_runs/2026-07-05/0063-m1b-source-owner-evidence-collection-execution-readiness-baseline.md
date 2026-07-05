# HosPrime Engineering Run 0063 — M1-B Source Owner Evidence Collection Execution Readiness Baseline

Date: 2026-07-05
Stage: BASELINE
Parent issue: #10
Memory epic: #8
Control issue: #81
Previous stage: REAL USER (#80)
Next stage: RESEARCH

## North Star outcome supported

Enable healthcare and public-health organizations to use trusted data, knowledge, organizational memory and governed AI to complete real work and make better decisions faster, with evidence, accountability and continuous learning.

This bounded BASELINE stage supports evidence quality, user trust, decision-to-outcome traceability, knowledge reuse and zero unauthorized high-impact action by measuring the execution-readiness starting point before any later controlled source-owner evidence collection occurs.

## Repository evidence checked before selecting work

- `README.md` on `main` was read before work selection and confirms the North Star, ordered Loop Engineering sequence, Core Rules, memory boundaries and current controlled release target: Milestone 1 — Governed Knowledge Oracle MVP.
- Open issue #81 is the active ordered M1-B stage: BASELINE after #80 REAL USER.
- Previous run inspected: `engineering_runs/2026-07-05/0062-m1b-source-owner-evidence-collection-execution-readiness-real-user.md`.
- Controlled packet inspected: `docs/governance/M1_B_SOURCE_OWNER_COLLECTION_READINESS_PACKET.md`.
- Controlled memory-boundary artifact inspected: `docs/governance/M1_B_SOURCE_CONFIRMATION_MEMORY_BOUNDARY.md`.
- Source register inspected only: `data/source_register/m1_source_register.yml`.
- Open issue inspection identified #10 as the parent governed source lifecycle workstream and #81 as the active sequenced control issue.
- Open PR inspection found no open pull request competing with this bounded stage.
- Workflow-run inspection for prior REAL USER commit `d9d8ab7aed93d490d28df1b82a3d2120f9a8712f` returned no workflow runs; therefore this run does not claim CI pass.

## Real organizational work problem

HosPrime has a released collection-readiness packet and user/decision-rights boundary, but before controlled source-owner evidence collection can proceed, the project needs an execution-readiness baseline that records what is currently known, pending and prohibited.

Without this baseline, later runs could falsely claim that packet release or user-boundary definition reduced the source-owner evidence gap, approved a source, or authorized ingestion/RAG activation.

## Real users and real work need

- Public-health executive / accountable sponsor: needs to know whether source-owner collection can safely start for real M1 knowledge packs without creating unsupported factual answers.
- Provincial program source owner: needs a controlled route to provide source facts later without being treated as final approver.
- Source inventory operator: needs a baseline for which fields remain pending before filling any packet.
- Data governance lead: needs classification, access, provenance and reviewer-routing gaps visible before any review or activation.
- Knowledge reviewer / independent reviewer: needs to distinguish collection-readiness precheck from source approval.

## Baseline measurement method

The baseline was measured by comparing the five seed records in `data/source_register/m1_source_register.yml` against the released packet's ten field groups and the real-user decision-rights boundaries from run 0062.

Scoring uses the released packet rule:

```text
total_collection_groups = source_record_count * 10
closed_collection_groups = present_groups + accepted_not_applicable_groups
gap_collection_groups = pending_groups + missing_groups
DECISION_RIGHTS_READINESS_GAP_RATE = gap_collection_groups / total_collection_groups
```

No field was counted as closed unless the current register or controlled governance artifact already records a concrete value, controlled reference, accountable owner, evidence note or accepted non-applicability rationale. Placeholder values such as `pending_source_owner_confirmation`, `pending_human_assignment`, `pending_inventory`, `pending_checksum`, `not_reviewed`, `not_approved` and `active_rag_index: false` were treated as unresolved for execution-readiness purposes.

## Execution-readiness baseline result

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

## Per-source baseline table

| Source ID | Knowledge pack | Closed groups | Gap groups | Collection-ready for precheck | Approved | Active RAG |
|---|---|---:|---:|---|---|---|
| M1A-PM25-001 | PM2.5 and Environmental Health | 5 / 10 | 5 / 10 | false | false | false |
| M1A-TB-001 | Tuberculosis and Communicable Disease Control | 5 / 10 | 5 / 10 | false | false | false |
| M1A-NCD-001 | NCD and Chronic Care Service Model | 5 / 10 | 5 / 10 | false | false | false |
| M1A-EOC-001 | Disaster, EOC and Public Health Emergency Operations | 5 / 10 | 5 / 10 | false | false | false |
| M1A-DIGITAL-001 | Digital Health, Data Governance and AI Workflow | 5 / 10 | 5 / 10 | false | false | false |

## Field-group baseline interpretation

For each of the five seed records, these groups are treated as currently closed only at placeholder/governance-boundary level, not as source approval:

1. source identity mapping to the register;
2. source title / knowledge-pack placeholder mapping;
3. owner role placeholder;
4. classification placeholder;
5. role-scoped access-policy placeholder.

For each of the five seed records, these groups remain unresolved for execution-readiness until later controlled collection supplies real evidence:

1. confirmed organization or office;
2. accountable sponsor person or office;
3. source-owner person or office assignment;
4. controlled file/system location and access route;
5. version/source period/currentness, checksum or non-file verification, reviewer routing, provenance and limitations.

Because several unresolved packet groups are cross-cutting, no record is fully collection-ready for precheck.

## Target metric for this execution-readiness cycle

```text
TARGET_DECISION_RIGHTS_READINESS_GAP_RATE_AFTER_LATER_FILLED_PACKET <= 30%
TARGET_FULLY_COLLECTION_READY_RECORDS_AFTER_LATER_FILLED_PACKET >= 3 / 5
TARGET_FULLY_APPROVED_RECORDS = 0 unless authorized human review evidence exists
TARGET_ACTIVE_RAG_RECORDS = 0 until approved source, retrieval evaluation and activation gate exist
```

This BASELINE run does not claim the target gap reduction has been achieved.

## Work completed in this run

- Measured the execution-readiness baseline against the released packet, real users and decision-rights boundary.
- Preserved the prior 50.0% decision-rights readiness gap as the current baseline.
- Confirmed all five seed records remain not fully collection-ready, not review-ready, not approved and inactive in RAG.
- Created this engineering-run evidence package only.
- Did not collect source-owner evidence.
- Did not modify `data/source_register/m1_source_register.yml`.
- Did not approve, ingest, parse, embed, index, answer from or activate any source.

## Acceptance result

```text
M1_B_BASELINE_COMPLETED = true
EXECUTION_READINESS_BASELINE_MEASURED = true
REAL_USER_DECISION_RIGHTS_BASELINE_RECORDED = true
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
NEXT_STAGE = RESEARCH
```

## Memory layer affected

Affected:

- engineering-run evidence;
- issue traceability.

Not affected:

- Personal/Staff Twin Memory;
- Person Memory;
- Role Memory;
- Organizational Memory / Governed RAG;
- Research Staging promotion state;
- source-register approval status;
- source-register active-RAG status.

## Risks and blockers

```text
RISK_UNRESOLVED_OWNER_ASSIGNMENT = true
RISK_UNRESOLVED_CONTROLLED_LOCATION = true
RISK_UNRESOLVED_VERSION_AND_CHECKSUM = true
RISK_UNRESOLVED_REVIEWER_ROUTING = true
RISK_PREMATURE_APPROVAL_OR_RAG_ACTIVATION = controlled_by_non_approval_boundary
```

## Single next stage

RESEARCH — identify current primary/official guidance needed to design a controlled filled-packet evidence collection workflow, keeping findings in Research Staging and not promoting external findings into Organizational Memory / Governed RAG without review.
