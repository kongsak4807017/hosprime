# HosPrime Engineering Run 0049 — M1-B Source Owner Evidence Collection Readiness Research

Date: 2026-07-05
Stage: RESEARCH
Parent issue: #10
Memory epic: #8
Control issue: #67
Previous stage: BASELINE (#66)
Next stage: HYPOTHESIS

## North Star outcome supported

Enable healthcare and public-health organizations to use trusted data, knowledge, organizational memory and governed AI to complete real work and make better decisions faster, with evidence, accountability and continuous learning.

This bounded RESEARCH stage supports:

- evidence quality;
- user trust;
- decision-to-outcome traceability;
- knowledge reuse;
- zero unauthorized high-impact action.

## Repository evidence checked before selecting work

- `README.md` on `main` confirms the North Star, ordered Loop Engineering sequence, Core Rules, memory boundaries and current controlled release target: **Milestone 1 — Governed Knowledge Oracle MVP**.
- Open issue #67 is the next ordered M1-B stage: **RESEARCH** for source-owner evidence collection packet controls.
- Previous run `engineering_runs/2026-07-04/0048-m1b-source-owner-evidence-collection-readiness-baseline.md` completed BASELINE and selected RESEARCH as the next stage.
- Parent issue #10 requires a governed backoffice source lifecycle and states that backoffice agents cannot self-approve high-impact sources.
- `docs/governance/MATURITY_GATES.md` requires named owners, source/version/classification/review-date capture, restricted access protection and review gates before M1 progression.
- `data/source_register/m1_source_register.yml` was inspected only. It was not modified.
- Recent PR inspection found PR #33 already closed and merged; no open PR was identified as superseding this bounded stage.

## Real organizational work problem

The organization needs a collection packet that source owners can complete consistently before any placeholder source can move toward review. Without packet controls, later runs may confuse evidence collection with source approval, or may collect incomplete owner/location/version evidence that cannot support governed retrieval.

This research therefore defines the minimum packet control requirements needed to reduce the measured readiness gap while preserving the non-approval boundary.

## Real users

- Public-health executive / accountable sponsor
- Provincial program source owner
- Source inventory operator
- Data governance lead
- Knowledge reviewer / independent reviewer

## Baseline from #66

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

## Target metric for later collection work

Not achieved in this research stage:

```text
TARGET_DECISION_RIGHTS_READINESS_GAP_RATE_AFTER_LATER_COLLECTION_PACKET <= 30%
TARGET_FULLY_COLLECTION_READY_RECORDS_AFTER_LATER_COLLECTION_PACKET >= 3 / 5
TARGET_FULLY_APPROVED_RECORDS_AFTER_LATER_REVIEW = 0 unless authorized review evidence exists
TARGET_ACTIVE_RAG_RECORDS = 0 until approved source, retrieval evaluation and activation gate exist
```

## Research staging sources

External findings below remain in Research Staging only. They are not promoted into Organizational Memory / Governed RAG and do not approve any HosPrime source record.

| Source | Date checked | Applicability | Limitation |
| --- | --- | --- | --- |
| NIST AI Risk Management Framework page: https://www.nist.gov/itl/ai-risk-management-framework | 2026-07-05 | Supports trustworthiness, risk management and evaluation framing for governed AI use. | Voluntary framework; must be localized to Thai public-health governance before use as policy. |
| NIST SP 800-53 Rev. 5 page: https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final | 2026-07-05 | Supports access control, audit/accountability, security/privacy control thinking and assurance boundary. | U.S. federal security-control catalog; not a direct Thai legal mandate. |
| ISO 15489-1:2016 page: https://www.iso.org/standard/62542.html | 2026-07-05 | Supports records-management framing for records, metadata, responsibilities and trustworthiness of evidence. | ISO page is a summary; full standard text was not accessed in this run. |
| W3C PROV Overview: https://www.w3.org/TR/prov-overview/ | 2026-07-05 | Supports provenance pattern for entity, activity, agent and traceability relationships. | Technical provenance model; does not define healthcare source approval authority by itself. |

## Research synthesis

The collection packet should make a placeholder source review-ready, not approved. Minimum controls should establish:

1. **Accountability** — named source owner role, owner person, sponsoring organization and reviewer expectation.
2. **Provenance** — controlled file or system location, source type, version, collection timestamp, collector identity and change/supersession notes.
3. **Integrity** — checksum or controlled checksum-pending reason, duplicate/superseded indicator and immutable evidence-package link.
4. **Classification and access** — classification, access policy, allowed roles, restricted-data warning and any personal/sensitive-data handling constraint.
5. **Review separation** — collection status separate from review status, approval status and RAG activation status.
6. **Limitations** — known gaps, uncertainty, incomplete inventory notes, applicability boundary and date sensitivity.
7. **Non-approval assertion** — explicit statement that collection does not equal approval, ingestion, indexing, factual-answer permission or Organizational RAG promotion.

## Minimum collection-packet control requirements

A later BUILD stage should not be started until the packet design can represent all of the following fields.

### A. Source identity and organizational scope

```text
source_id
knowledge_pack
source_title
source_type
organization
organization_scope_confirmation
accountable_sponsor_role
accountable_sponsor_person
source_owner_role
source_owner_person
```

Purpose: close the current 100% sponsor/organization and source-owner assignment gaps without claiming approval.

### B. Inventory and version control

```text
file_or_system_location
location_control_type
version
source_date_or_period
collection_timestamp
collector_role
collector_person
checksum
checksum_algorithm
checksum_pending_reason
supersedes_source_id
conflict_or_duplicate_note
```

Purpose: close location/version gaps while preserving traceability and allowing checksum-pending only with controlled justification.

### C. Classification and access boundary

```text
classification
access_policy
allowed_roles
restricted_data_indicator
personal_or_sensitive_data_indicator
minimum_access_review_required
```

Purpose: prevent accidental access expansion before review.

### D. Review expectation without approval

```text
collection_status
review_status
reviewer_role
reviewer_person
review_due_date
approval_status
approval_decision_date
active_rag_index
```

Required invariant:

```text
collection_status = collected or collection_ready does not imply approval_status = approved
active_rag_index must remain false unless approval, retrieval evaluation and activation gate exist
```

### E. Provenance, limitations and evidence package

```text
provenance_summary
collection_method
limitations_note
applicability_boundary
freshness_risk
linked_issue
evidence_package_path
review_record_path
```

Purpose: support decision-to-outcome traceability and avoid fabricated or ungrounded factual answers.

## Control logic recommended for later stages

The later HYPOTHESIS stage should test this claim:

```text
If a collection packet requires named organization, named owner, controlled location, version, reviewer expectation, access boundary and explicit non-approval assertion, then later collection work can reduce DECISION_RIGHTS_READINESS_GAP_RATE from 50.0% to <= 30% without changing approval_status, ingestion state or active_rag_index.
```

The later PLAN / BUILD stages should preserve these blocked transitions:

```text
DISCOVERED -> COLLECTION_READY allowed only after packet completeness check
COLLECTION_READY -> REVIEW_PENDING allowed only after reviewer assignment exists
REVIEW_PENDING -> APPROVED allowed only after authorized human review record exists
APPROVED -> INDEX_READY allowed only after quality and retrieval evaluation requirements exist
INDEX_READY -> INDEXED allowed only after activation gate and audit record exist
```

## Explicit non-actions in this run

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
M1_B_RESEARCH_COMPLETED = true
SOURCE_OWNER_COLLECTION_PACKET_CONTROL_REQUIREMENTS_DEFINED = true
RESEARCH_STAGING_ONLY = true
NEXT_STAGE = HYPOTHESIS
SOURCE_REGISTER_MODIFIED = false
SOURCE_APPROVAL_CLAIMED = false
SOURCE_INGESTION_CLAIMED = false
RAG_ACTIVATION_CLAIMED = false
```

## Test / CI status

No executable CI success is claimed for this governance RESEARCH stage.

Evidence basis:

- README inspection on `main`;
- open issue #67 inspection;
- previous run 0048 inspection;
- `data/source_register/m1_source_register.yml` inspection only;
- `docs/governance/MATURITY_GATES.md` inspection;
- recent PR inspection;
- current external research source inspection.

## Memory layer affected

Research Staging / Governance evidence only.

No Personal/Staff Twin Memory, Person Memory, Role Memory or Organizational Memory / Governed RAG was modified. No external research was promoted into organizational truth.

## Risks and blockers

- The packet controls are researched but not yet translated into a tested template or schema.
- No real source-owner evidence has been collected.
- No human reviewer has approved any source.
- No ingestion, parsing, embedding, indexing or retrieval activation is permitted from this run.

## Next single stage

HYPOTHESIS — define the testable hypothesis and measurable expectation for a collection packet that can reduce the current decision-rights readiness gap without bypassing review or approval gates.
