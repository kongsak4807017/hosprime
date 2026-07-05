# HosPrime Engineering Run 0065 — M1-B Source Owner Evidence Collection Execution Readiness Hypothesis

Date: 2026-07-05
Stage: HYPOTHESIS
Parent issue: #10
Memory epic: #8
Control issue: #83
Previous stage: RESEARCH (#82)
Next stage: PLAN

## North Star outcome supported

Enable healthcare and public-health organizations to use trusted data, knowledge, organizational memory and governed AI to complete real work and make better decisions faster, with evidence, accountability and continuous learning.

This bounded HYPOTHESIS stage supports evidence quality, user trust, decision-to-outcome traceability, knowledge reuse and zero unauthorized high-impact action by defining a falsifiable workflow hypothesis for later controlled filled-packet execution before any source-owner evidence is collected or any source is approved, ingested, indexed or activated.

## Repository evidence checked before selecting work

- `README.md` on `main` was read before work selection and confirms the North Star, ordered Loop Engineering sequence, Core Rules, memory boundaries and current controlled release target: Milestone 1 — Governed Knowledge Oracle MVP.
- Open issue #83 is the active ordered M1-B stage: HYPOTHESIS after #82 RESEARCH.
- Previous run inspected: `engineering_runs/2026-07-05/0064-m1b-source-owner-evidence-collection-execution-readiness-research.md`.
- Collection-readiness packet inspected: `docs/governance/M1_B_SOURCE_OWNER_COLLECTION_READINESS_PACKET.md`.
- Memory-boundary correction inspected: `docs/governance/M1_B_SOURCE_CONFIRMATION_MEMORY_BOUNDARY.md`.
- Maturity gate inspected: `docs/governance/MATURITY_GATES.md`.
- Source register inspected only: `data/source_register/m1_source_register.yml`.
- Open issue inspection identified #10 as the parent governed source lifecycle workstream and #83 as the active sequenced control issue.
- PR inspection found no newer open user PR superseding this bounded stage.

## Real organizational work problem

HosPrime has five M1 seed source records and a released collection-readiness packet, but the next practical work must avoid converting a filled packet into de facto source approval.

The real problem is that source owners, inventory operators and governance reviewers need a controlled workflow for filling collection packets that can reduce decision-rights readiness gaps while keeping all records outside Organizational Memory / Governed RAG until an authorized review, retrieval evaluation and activation gate exist.

## Real users and real work need

- Public-health executive / accountable sponsor: needs assurance that later collection execution improves readiness without creating unauthorized factual-answer capability.
- Provincial program source owner: needs a clear way to provide ownership, location, version and limitation facts without becoming an automatic approver.
- Source inventory operator: needs a repeatable packet-filling route with fail-closed handling for missing controlled locations, versions or checksum evidence.
- Data governance lead: needs classification, access policy and reviewer routing to be captured before any source-register mutation.
- Knowledge reviewer / independent reviewer: needs source-owner assertions separated from reviewer decisions and explicit non-approval boundaries.

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

This HYPOTHESIS run does not claim any target improvement.

## Research staging carried forward

The previous RESEARCH stage staged official guidance only as design input:

- NIST AI Risk Management Framework official page;
- NIST SP 800-53 Rev. 5 official page;
- WHO ethics and governance of AI for health;
- WHO guidance on large multi-modal models for health;
- ISO/IEC 42001:2023 official standard page.

These sources remain Research Staging only. They are not promoted into Organizational Memory / Governed RAG and are not used as authority for source approval.

## Hypothesis

```text
If HosPrime runs a controlled filled-packet workflow for the five M1 seed records that requires source identity mapping, accountable office, source owner, controlled location, version/source period, checksum or checksum-pending rationale, classification/access policy, reviewer routing, conflict-of-interest handling, provenance/limitations and explicit non-approval assertion, then at least 3 of 5 seed records can become collection-ready for a later independent review precheck while reducing DECISION_RIGHTS_READINESS_GAP_RATE from 50.0% to <= 30%, without approving, ingesting, parsing, embedding, indexing, activating or answering from any source.
```

## Testable mechanism

The later PLAN stage should define a workflow where each seed source can be evaluated across the ten packet field groups already released in `docs/governance/M1_B_SOURCE_OWNER_COLLECTION_READINESS_PACKET.md`.

A field group may count as resolved only when it is either:

1. `present` with a concrete value, controlled reference, evidence note or verification method; or
2. `pending_with_accountable_owner` with a named accountable owner and next action that a reviewer can follow.

A seed record may count as collection-ready only when all ten field groups are `present`, or any non-present field group is `not_applicable_with_rationale` and acceptable to the later reviewer.

A seed record may count as review-ready only when reviewer routing, conflict-of-interest status, provenance/limitations and non-approval assertion are explicitly recorded.

No seed record may count as approved or active-RAG in this workflow.

## Falsification criteria

The hypothesis must be considered false or not yet supported if any of the following occurs during later PLAN/BUILD/TEST/EVALUATE stages:

```text
DECISION_RIGHTS_READINESS_GAP_RATE_AFTER_LATER_FILLED_PACKET > 30%
FULLY_COLLECTION_READY_RECORDS_AFTER_LATER_FILLED_PACKET < 3 / 5
ANY_SOURCE_REGISTER_APPROVAL_STATUS_CHANGED_WITHOUT_AUTHORIZED_REVIEW = true
ANY_ACTIVE_RAG_INDEX_CHANGED = true
ANY_SOURCE_USED_FOR_FACTUAL_ANSWER = true
SOURCE_OWNER_ASSERTION_TREATED_AS_REVIEWER_DECISION = true
RESEARCH_STAGING_PROMOTED_WITHOUT_REVIEW_RECORD = true
```

## Required fail-closed controls for later plan

The next PLAN stage must include explicit fail-closed handling for:

1. missing or ambiguous source-register identity;
2. missing accountable source owner or accountable office;
3. uncontrolled public link or memory-only source claim;
4. missing version/source period/currentness statement;
5. missing checksum or checksum-pending rationale;
6. disputed classification or access policy;
7. missing reviewer route;
8. missing conflict-of-interest check or rationale;
9. missing provenance, limitation or applicability note;
10. absent non-approval assertion;
11. any attempt to approve, ingest, parse, embed, index, answer from or activate a source.

## Work completed in this run

- Read the latest README North Star, Core Rules, ordered loop, memory boundaries and controlled release target.
- Inspected open issue #83, parent source lifecycle workstream #10, maturity gates, source register, collection-readiness packet, memory-boundary correction and previous research evidence.
- Defined a bounded, testable hypothesis for controlled filled-packet execution readiness.
- Preserved Research Staging as staging only.
- Did not collect source-owner evidence.
- Did not modify `data/source_register/m1_source_register.yml`.
- Did not approve, ingest, parse, embed, index, answer from or activate any source.

## Acceptance result

```text
M1_B_HYPOTHESIS_COMPLETED = true
CONTROLLED_FILLED_PACKET_WORKFLOW_HYPOTHESIS_DEFINED = true
RESEARCH_STAGING_ONLY = true
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
NEXT_STAGE = PLAN
```

## Memory layer affected

Affected:

- Research Staging design interpretation;
- engineering-run evidence;
- issue traceability.

Not affected:

- Personal/Staff Twin Memory;
- Person Memory;
- Role Memory;
- Organizational Memory / Governed RAG;
- source-register approval status;
- source-register active-RAG status.

## Risks and blockers

```text
RISK_HYPOTHESIS_NOT_YET_TESTED = true
RISK_UNRESOLVED_OWNER_ASSIGNMENT = true
RISK_UNRESOLVED_CONTROLLED_LOCATION = true
RISK_UNRESOLVED_VERSION_AND_CHECKSUM = true
RISK_UNRESOLVED_REVIEWER_ROUTING = true
RISK_SOURCE_OWNER_ASSERTION_MISREAD_AS_APPROVAL = controlled_by_non_approval_boundary
RISK_PREMATURE_RAG_ACTIVATION = controlled_by_fail_closed_plan_requirement
```

## Single next stage

PLAN — define the controlled filled-packet execution workflow, scoring rules, fail-closed checks, review-routing boundaries and evidence outputs needed to test this hypothesis without source-register mutation, source approval, ingestion or RAG activation.
