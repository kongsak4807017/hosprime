# HosPrime Engineering Run 0050 — M1-B Source Owner Evidence Collection Readiness Hypothesis

Date: 2026-07-05
Stage: HYPOTHESIS
Parent issue: #10
Memory epic: #8
Control issue: #68
Previous stage: RESEARCH (#67)
Next stage: PLAN

## North Star outcome supported

Enable healthcare and public-health organizations to use trusted data, knowledge, organizational memory and governed AI to complete real work and make better decisions faster, with evidence, accountability and continuous learning.

This bounded HYPOTHESIS stage supports:

- evidence quality;
- user trust;
- decision-to-outcome traceability;
- knowledge reuse;
- zero unauthorized high-impact action.

## Repository evidence checked before selecting work

- `README.md` on `main` confirms the North Star, ordered Loop Engineering sequence, Core Rules, memory boundaries and current controlled release target: **Milestone 1 — Governed Knowledge Oracle MVP**.
- Open issue #68 is the next ordered M1-B stage: **HYPOTHESIS** after #67 RESEARCH.
- Previous run `engineering_runs/2026-07-05/0049-m1b-source-owner-evidence-collection-readiness-research.md` completed RESEARCH and selected HYPOTHESIS as the next stage.
- Parent issue #10 requires a governed backoffice source lifecycle and states that backoffice agents cannot self-approve high-impact sources.
- `docs/governance/MATURITY_GATES.md` requires named owners, source/version/classification/review-date capture, restricted access protection and review gates before M1 progression.
- `data/source_register/m1_source_register.yml` was inspected only. It remains placeholder-only, with five DISCOVERED seed records, no approval, no active RAG activation and pending owner/location/version/checksum fields.
- Recent PR inspection found no open PR that supersedes this bounded HYPOTHESIS stage.
- Combined commit status for previous run commit `eb29eb8a59ca4c26ad91243f4200df4258cba6d5` returned no statuses; no CI pass is claimed.

## Real organizational work problem

The organization needs a source-owner collection packet that can make placeholder records ready for later human review without accidentally converting collection into source approval or RAG activation.

Current gap: source records contain placeholder owner, organization, controlled location, version and checksum fields. Without a measurable hypothesis, the next PLAN / BUILD steps may add form fields or documents without proving whether those fields reduce decision-rights readiness risk.

## Real users

- Public-health executive / accountable sponsor who needs trusted answers with visible ownership and accountability.
- Provincial program source owner who must identify and attest to controlled evidence before review.
- Source inventory operator who collects file/system/version/checksum evidence.
- Data governance lead who checks classification, access boundary and review route.
- Knowledge reviewer / independent reviewer who later accepts or rejects source use.

## Baseline preserved from #66 and #67

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

## Hypothesis

```text
If a source-owner collection packet requires named organization, named source owner, controlled location, version evidence, checksum or checksum-pending reason, classification, access policy, reviewer expectation, provenance, limitations and an explicit non-approval assertion, then later collection work can reduce DECISION_RIGHTS_READINESS_GAP_RATE from 50.0% to <= 30% and increase FULLY_COLLECTION_READY_RECORDS from 0/5 to >= 3/5 without changing approval_status, ingestion state or active_rag_index.
```

## Measurable target for later PLAN / BUILD / TEST stages

```text
TARGET_DECISION_RIGHTS_READINESS_GAP_RATE_AFTER_LATER_COLLECTION_PACKET <= 30%
TARGET_FULLY_COLLECTION_READY_RECORDS_AFTER_LATER_COLLECTION_PACKET >= 3 / 5
TARGET_FULLY_APPROVED_RECORDS_AFTER_LATER_REVIEW = 0 unless authorized human review evidence exists
TARGET_ACTIVE_RAG_RECORDS = 0 until approved source, retrieval evaluation and activation gate exist
```

## Hypothesis variables

### Independent variable

A controlled source-owner collection packet requiring these ten control groups:

```text
1. organization and organization scope confirmation
2. accountable sponsor role/person
3. source owner role/person
4. controlled file or system location
5. version and source date/period evidence
6. checksum or checksum-pending reason
7. classification and access policy
8. reviewer role/person or reviewer expectation
9. provenance, limitations and applicability boundary
10. explicit non-approval assertion
```

### Dependent variables

```text
DECISION_RIGHTS_READINESS_GAP_RATE
FULLY_COLLECTION_READY_RECORDS
FIELD_GROUP_COMPLETENESS_BY_RECORD
ILLEGAL_APPROVAL_OR_RAG_ACTIVATION_COUNT
```

### Safety invariants

```text
SOURCE_REGISTER_MODIFIED = false in this HYPOTHESIS stage
SOURCE_APPROVAL_CLAIMED = false
SOURCE_INGESTION_CLAIMED = false
SOURCE_PARSING_CLAIMED = false
SOURCE_EMBEDDING_CLAIMED = false
SOURCE_INDEXING_CLAIMED = false
RAG_ACTIVATION_CLAIMED = false
ORGANIZATIONAL_MEMORY_PROMOTION_CLAIMED = false
```

## Falsification criteria

The hypothesis should be rejected or revised if a later packet design cannot satisfy any of the following:

1. It cannot distinguish `collection_status` from `review_status`, `approval_status` and `active_rag_index`.
2. It cannot represent checksum-pending justification without pretending integrity verification is complete.
3. It cannot keep restricted records inactive until access policy and reviewer gates are complete.
4. It cannot identify accountable source owner and reviewer roles for at least 3 of 5 seed records.
5. It reduces documentation friction but leaves the measured decision-rights readiness gap above 30%.
6. It creates a route for self-approval by an agent or source collector.

## Planned evaluation design for later stages

Later PLAN / BUILD stages should define a packet template and completeness check. Later TEST should score each of the five seed records against the ten control groups without approving, ingesting or activating any source.

The expected scoring rule is:

```text
resolved_control_groups / total_control_groups
```

The expected gap rule is:

```text
1 - resolved_control_groups / total_control_groups
```

A record should be called `collection_ready` only when all required collection groups are complete and the non-approval assertion is present. `collection_ready` must not imply `review_pending`, `approved`, `index_ready` or `indexed`.

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
M1_B_HYPOTHESIS_COMPLETED = true
COLLECTION_PACKET_HYPOTHESIS_DEFINED = true
TARGET_DECISION_RIGHTS_READINESS_GAP_RATE_AFTER_LATER_COLLECTION_PACKET <= 30%
RESEARCH_STAGING_ONLY = true
NEXT_STAGE = PLAN
SOURCE_REGISTER_MODIFIED = false
SOURCE_APPROVAL_CLAIMED = false
SOURCE_INGESTION_CLAIMED = false
RAG_ACTIVATION_CLAIMED = false
```

## Test / CI status

No executable CI success is claimed for this governance HYPOTHESIS stage.

Evidence basis:

- README inspection on `main`;
- open issue #68 inspection;
- previous run 0049 inspection;
- `data/source_register/m1_source_register.yml` inspection only;
- `docs/governance/MATURITY_GATES.md` inspection;
- recent PR inspection;
- combined commit status check for previous run commit.

## Memory layer affected

Research Staging / Governance evidence only.

No Personal/Staff Twin Memory, Person Memory, Role Memory or Organizational Memory / Governed RAG was modified. No external research was promoted into organizational truth.

## Risks and blockers

- The hypothesis is not yet a packet template, schema or test.
- No real source-owner evidence has been collected.
- No human reviewer has approved any source.
- No ingestion, parsing, embedding, indexing or retrieval activation is permitted from this run.

## Next single stage

PLAN — define the bounded packet design plan, fields, scoring method and test scope for the collection packet readiness control without modifying the source register or claiming approval.
