# HosPrime Engineering Run 0109 — M1-B Source-Owner Evidence Packet Readiness Research

Date: 2026-07-07
Stage: RESEARCH
Parent issue: #10
Memory epic: #8
Control issue: #127
Previous stage: BASELINE (#126)
Next stage: HYPOTHESIS

## North Star outcome supported

This RESEARCH stage supports the HosPrime North Star by staging a minimum safe source-owner evidence packet structure before any later authorized source-owner evidence collection, source approval, ingestion, indexing, active RAG, factual-answer permission or Organizational Memory promotion.

Supported outcomes:

- evidence-based decisions;
- knowledge continuity;
- decision-to-outcome traceability;
- evidence quality;
- user trust;
- knowledge reuse;
- zero unauthorized high-impact action.

## Repository evidence checked

- `README.md` on `main` was read first for the North Star, current controlled release target, loop sequence, Core Rules and memory boundaries.
- Open issues were inspected. The current ordered control issue is #127: `M1-B Research: Source-owner evidence packet minimum safe structure`.
- Open pull requests were inspected; no open pull request was found and no PR change or merge is claimed.
- Recent engineering-run baseline inspected: `engineering_runs/2026-07-07/0108-m1b-source-owner-evidence-packet-readiness-baseline.md`.
- Source register inspected and not modified: `data/source_register/m1_source_register.yml`.
- Controlled guidance inspected: `docs/governance/M1_B_CONTROLLED_AUTHORIZED_PACKET_EXECUTION_PLAN.md`.
- Controlled memory correction inspected: `docs/governance/M1_B_GUIDANCE_NOT_AUTHORIZATION_MEMORY_RULE.md`.
- CI pass is not claimed because no successful workflow evidence was produced or inspected for this commit.

## Current controlled release target

```text
CONTROLLED_RELEASE_TARGET = Milestone 1 — Governed Knowledge Oracle MVP
M1_MUST_INGEST_APPROVED_DOCUMENTS = true
M1_MUST_RETRIEVE_EVIDENCE = true
M1_MUST_ANSWER_ONLY_WITH_SUFFICIENT_EVIDENCE = true
M1_MUST_PROVIDE_TRACEABLE_CITATIONS = true
M1_MUST_ENFORCE_ACCESS_CONTROL = true
M1_MUST_RECORD_AUDIT_AND_COST_DATA = true
```

## Current loop stage

```text
CURRENT_STAGE = RESEARCH
PREVIOUS_STAGE = BASELINE
NEXT_STAGE = HYPOTHESIS
```

## Real user and organizational work problem

### Real users

- public-health executive sponsor;
- data governance lead;
- provincial program source owner;
- source inventory operator;
- independent knowledge reviewer;
- technical ingestion operator.

### Real organizational work problem

The five M1 seed knowledge-pack records still have 0/5 filled source-owner evidence packets. Before HosPrime can later collect source-owner evidence safely, the team needs a minimum packet structure that separates custody evidence, provenance, classification, review routing, limitations and non-authorization boundaries.

This run does not collect any real source-owner evidence. It researches and stages the structure only.

## Baseline and target metric

Baseline from run 0108:

```text
SEED_RECORDS_COUNT = 5
FILLED_SOURCE_OWNER_PACKET_COUNT = 0 / 5
SOURCE_OWNER_PACKET_READINESS_RATE = 0%
SOURCE_RECORDS_WITH_CONFIRMED_ORGANIZATION = 0 / 5
SOURCE_RECORDS_WITH_NAMED_OWNER_PERSON = 0 / 5
SOURCE_RECORDS_WITH_CONFIRMED_FILE_OR_SYSTEM_LOCATION = 0 / 5
SOURCE_RECORDS_WITH_CONFIRMED_VERSION = 0 / 5
SOURCE_RECORDS_WITH_CONFIRMED_CHECKSUM = 0 / 5
SOURCE_RECORDS_WITH_HUMAN_REVIEWER_ASSIGNED = 0 / 5
SOURCE_RECORDS_WITH_APPROVAL_STATUS_APPROVED = 0 / 5
SOURCE_RECORDS_WITH_ACTIVE_RAG_INDEX = 0 / 5
```

Target for this RESEARCH stage:

```text
TARGET_SOURCE_OWNER_PACKET_MINIMUM_SAFE_STRUCTURE_STAGED = true
TARGET_RESEARCH_STAGING_ONLY = true
TARGET_SOURCE_REGISTER_MODIFIED = false
TARGET_SOURCE_OWNER_EVIDENCE_COLLECTED = false
TARGET_SOURCE_APPROVAL_CLAIMED = false
TARGET_RAG_ACTIVATION_CLAIMED = false
```

## Research method

Primary method:

1. Use repository-controlled governance first.
2. Use current official external sources only where they clarify governance, traceability, transparency, accountability, risk management or documented information requirements.
3. Keep all external findings in Research Staging.
4. Do not promote external findings into Organizational Memory or active RAG.
5. Do not mutate the source register.

## Internal research findings from repository-controlled evidence

### Finding I1 — Source packets must remain non-authorizing

The released M1-B checklist states that a completed packet-execution checklist is not source approval and that source approval requires a separate explicit human review decision with accountable reviewer identity, review record, limitations and gate evidence.

Research implication:

```text
PACKET_COMPLETION != SOURCE_APPROVAL
PACKET_COMPLETION != INGESTION_PERMISSION
PACKET_COMPLETION != ACTIVE_RAG
```

### Finding I2 — Ten field groups already define the minimum safe packet frame

The controlled checklist defines ten field groups:

```text
source_identity
organization_scope
accountable_sponsor
source_owner
controlled_location
version_or_source_period
checksum_or_checksum_pending_reason
classification_and_access
reviewer_precheck_routing
provenance_and_limitations
```

Research implication:

A later hypothesis should test whether these ten field groups are sufficient as the minimum safe packet structure for all five M1 seed source records.

### Finding I3 — Future runs must preserve memory-layer separation

The memory rule records that released guidance is not authorization, authorization is not source approval, source approval is not active RAG, and active RAG is not Organizational Memory promotion.

Research implication:

The packet structure must include an explicit `memory_layer_boundary` field and a `non_approval_boundary_acknowledgement` field.

### Finding I4 — Existing source register supports placeholders only

The current source register contains five records, all in `DISCOVERED` state, with pending source-owner confirmation, pending inventory, pending checksum, `review_status: not_reviewed`, `approval_status: not_approved`, and `active_rag_index: false`.

Research implication:

The packet structure should accept pending reasons without converting any source into reviewed, approved, indexed or active state.

## External research staging findings

These findings are staged for review only. They are not Organizational Memory, source approval, RAG evidence, or factual-answer permission.

### Finding E1 — NIST AI RMF emphasizes trustworthiness and risk management across AI design, development, use and evaluation

Source: NIST AI Risk Management Framework page, accessed 2026-07-07.

URL: https://www.nist.gov/itl/ai-risk-management-framework

Relevant staged interpretation:

NIST describes the AI RMF as a voluntary framework to improve the ability to incorporate trustworthiness considerations into the design, development, use and evaluation of AI products, services and systems. NIST also notes that AI RMF 1.0 is being revised and that a 2026 concept note addresses trustworthy AI in critical infrastructure.

Research implication for HosPrime:

Because HosPrime supports healthcare and public-health organizations, source-owner packets should capture trustworthiness-relevant information before AI-assisted retrieval or answer generation: provenance, authority, limitations, reviewer routing, access boundary and audit readiness.

Limitations:

- NIST AI RMF is voluntary guidance and not a HosPrime source approval record.
- This finding remains in Research Staging until reviewed.
- It does not authorize any source ingestion, indexing or factual answer.

### Finding E2 — ISO/IEC 42001 frames AI management as an organizational management system requiring responsible use, traceability, transparency, reliability and continual improvement

Source: ISO/IEC 42001:2023 official ISO page, accessed 2026-07-07.

URL: https://www.iso.org/standard/42001

Relevant staged interpretation:

ISO states that ISO/IEC 42001 specifies requirements for establishing, implementing, maintaining and continually improving an Artificial Intelligence Management System. The ISO page highlights responsible development and use, risk management, traceability, transparency, reliability and governance.

Research implication for HosPrime:

A source-owner evidence packet should be treated as documented governance information supporting traceability and transparency, not as a substitute for human review, source approval, ingestion approval, retrieval evaluation or release approval.

Limitations:

- The full ISO standard text was not reproduced or embedded.
- This finding remains in Research Staging until reviewed.
- It does not create certification, compliance, source approval or execution authority.

### Finding E3 — OECD AI Principles emphasize inclusive growth, human-centered values, transparency, robustness, safety, security and accountability

Source: OECD.AI Principles page, accessed 2026-07-07.

URL: https://oecd.ai/en/ai-principles

Relevant staged interpretation:

The OECD AI Principles are used here only as a high-level governance reference for transparency, accountability, safety and human-centered values.

Research implication for HosPrime:

Source-owner evidence packets should make accountability visible: who owns the source, who can request review, who may review, what the source can and cannot support, and which access constraints apply.

Limitations:

- This is high-level policy guidance, not operational evidence for any M1 source.
- This finding remains in Research Staging until reviewed.
- It does not authorize any real-world source collection, source approval or AI deployment action.

## Minimum safe source-owner evidence packet structure staged for hypothesis

The following structure is staged as a research output only.

```yaml
packet_id: pending_later_authorized_execution
source_id: required_existing_register_source_id
source_identity:
  source_title: required_or_pending_reason
  knowledge_pack: required_or_pending_reason
  source_type: required_or_pending_reason
organization_scope:
  responsible_organization_or_office: required_or_pending_reason
  accountable_sponsor_role_or_office: required_or_pending_reason
  jurisdiction_or_operational_scope: required_or_pending_reason
source_owner:
  owner_person_or_office: required_or_pending_reason
  custody_statement: required_or_pending_reason
  decision_right_boundary: required_or_pending_reason
controlled_location:
  file_system_repository_or_custody_location: required_or_pending_reason
  access_method: required_or_pending_reason
  location_control_owner: required_or_pending_reason
version_and_freshness:
  version: required_or_pending_reason
  source_period: required_or_pending_reason
  effective_date: required_or_pending_reason
  replacement_or_supersession_rule: required_or_pending_reason
integrity:
  checksum_or_integrity_method: required_or_pending_reason
  checksum_pending_reason: required_if_checksum_missing
classification_and_access:
  classification: required_existing_or_reviewed_change
  access_policy: required_existing_or_reviewed_change
  allowed_roles: required_existing_or_reviewed_change
  restricted_handling_note: required_if_restricted
provenance_and_limitations:
  provenance_path: required_or_pending_reason
  method_of_collection: required_later_only
  assumptions: required_or_none_declared
  known_limitations: required_or_none_declared
  applicability_boundary: required_or_pending_reason
review_routing:
  independent_reviewer_or_office: required_or_pending_reason
  reviewer_independence_note: required_or_pending_reason
  precheck_status: not_started_by_default
non_authorization_controls:
  non_approval_boundary_acknowledgement: required
  source_register_mutation_attempted: false
  source_approval_claimed: false
  ingestion_claimed: false
  active_rag_claimed: false
  organizational_memory_promotion_claimed: false
receipt_fields_for_later_authorized_execution:
  authorized_executor_role: pending_later_authorized_execution
  receipt_timestamp: pending_later_authorized_execution
  audit_event_reference: pending_later_authorized_execution
memory_layer_boundary:
  current_layer: Research Staging / governance working memory only
  promotion_status: not_promoted
  promotion_review_record: null
```

## Minimum acceptance rules staged for hypothesis

```text
RULE_1_EXISTING_SOURCE_ID_REQUIRED = true
RULE_2_ALL_10_FIELD_GROUPS_PRESENT_OR_PENDING_WITH_REASON = true
RULE_3_PENDING_REASON_ALLOWED_WITHOUT_APPROVAL = true
RULE_4_CLASSIFICATION_AND_ACCESS_MUST_NOT_BE_EXPANDED_BY_PACKET = true
RULE_5_SOURCE_OWNER_SELF_APPROVAL_FORBIDDEN = true
RULE_6_REVIEW_ROUTING_IS_NOT_REVIEW_DECISION = true
RULE_7_PACKET_COMPLETION_IS_NOT_SOURCE_APPROVAL = true
RULE_8_SOURCE_APPROVAL_IS_NOT_INGESTION_PERMISSION = true
RULE_9_INGESTION_IS_NOT_ACTIVE_RAG = true
RULE_10_ACTIVE_RAG_IS_NOT_ORGANIZATIONAL_MEMORY_PROMOTION = true
```

## Per-source applicability staged for hypothesis

| Source ID | Knowledge pack | Minimum packet structure applies? | Special handling note |
|---|---|---:|---|
| `M1A-PM25-001` | PM2.5 and Environmental Health | yes | internal, role-scoped access; preserve limitation note |
| `M1A-TB-001` | Tuberculosis and Communicable Disease Control | yes | restricted_internal; protect sensitive program context |
| `M1A-NCD-001` | NCD and Chronic Care Service Model | yes | internal, role-scoped access; no factual-answer permission |
| `M1A-EOC-001` | Disaster, EOC and Public Health Emergency Operations | yes | restricted_internal; protect incident-command sensitivity |
| `M1A-DIGITAL-001` | Digital Health, Data Governance and AI Workflow | yes | internal, role-scoped access; no Organizational Memory promotion |

## Boundary controls preserved

```text
SOURCE_REGISTER_MODIFIED = false
SOURCE_OWNER_EVIDENCE_COLLECTED = false
SOURCE_OWNER_ATTESTATION_CLAIMED = false
INDEPENDENT_REVIEW_CLAIMED = false
SOURCE_APPROVAL_CLAIMED = false
INGESTION_PERMISSION_CLAIMED = false
SOURCE_INGESTION_CLAIMED = false
SOURCE_PARSING_CLAIMED = false
SOURCE_EMBEDDING_CLAIMED = false
SOURCE_INDEXING_CLAIMED = false
RAG_ACTIVATION_CLAIMED = false
FACTUAL_ANSWER_PERMISSION_CLAIMED = false
ORGANIZATIONAL_MEMORY_PROMOTION_CLAIMED = false
REAL_WORLD_COMPLETION_CLAIMED = false
EXTERNAL_FINDINGS_PROMOTED_TO_ORGANIZATIONAL_TRUTH = false
CI_PASS_CLAIMED = false
```

## Test and CI status

```text
MANUAL_RESEARCH_COMPLETED = true
AUTOMATED_TEST_ADDED = false
CI_PASS_CLAIMED = false
```

No CI pass is claimed because this run created a documentation/evidence research file only and did not inspect a successful workflow result for the new commit.

## Memory layer affected

Affected:

- engineering-run evidence;
- issue traceability;
- Research Staging for external governance references;
- governance working memory for the M1-B loop.

Not affected:

- Personal / Staff Twin Memory;
- Person Memory;
- Role Memory;
- Organizational Memory / Governed RAG;
- source-register lifecycle state;
- source-register review status;
- source-register approval status;
- source-register active-RAG status.

## Risks or blockers

```text
RISK_PACKET_STRUCTURE_CONFUSED_WITH_PACKET_EXECUTION = still_present
RISK_PACKET_EXECUTION_CONFUSED_WITH_SOURCE_APPROVAL = still_present
RISK_SOURCE_APPROVAL_CONFUSED_WITH_ACTIVE_RAG = still_present
RISK_EXTERNAL_GOVERNANCE_FINDINGS_PROMOTED_WITHOUT_REVIEW = still_present
BLOCKER_TO_SOURCE_OWNER_EVIDENCE_COLLECTION = true until later authorized execution stage exists
BLOCKER_TO_SOURCE_APPROVAL = true until explicit human review decision exists
BLOCKER_TO_ACTIVE_RAG = true until approval, ingestion, retrieval evaluation and activation gates pass
```

## Acceptance result

```text
M1_B_RESEARCH_COMPLETED = true
SOURCE_OWNER_PACKET_MINIMUM_SAFE_STRUCTURE_STAGED = true
RESEARCH_STAGING_ONLY = true
SOURCE_REGISTER_MODIFIED = false
SOURCE_OWNER_EVIDENCE_COLLECTED = false
SOURCE_APPROVAL_CLAIMED = false
RAG_ACTIVATION_CLAIMED = false
CI_PASS_CLAIMED = false
```

## Single next stage

```text
NEXT_STAGE = HYPOTHESIS
NEXT_ISSUE_TITLE = M1-B Hypothesis: Source-owner packet structure reduces unsafe approval ambiguity
```
