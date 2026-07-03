# HosPrime Engineering Run 0020 — M1-B Controlled Source Inventory Hypothesis

Date: 2026-07-03
Stage: HYPOTHESIS
Parent issue: #10
Control issue: #38
Previous stage: RESEARCH (#37)
Next stage: PLAN (#39)

## North Star outcome supported

Enable healthcare and public-health organizations to use trusted data, knowledge, organizational memory and governed AI to complete real work and make better decisions faster, with evidence, accountability and continuous learning.

This run supports:

- evidence-based decisions;
- user trust;
- decision-to-outcome traceability;
- knowledge reuse;
- zero unauthorized high-impact action.

## Real user and real organizational work problem

Real users:

- public-health executive;
- provincial program owner;
- data governance lead;
- knowledge reviewer;
- future source inventory operator.

Real work problem:

The current M1 source register contains five safe placeholder records, but none are fully confirmed for controlled source inventory. Before any ingestion, parsing, indexing or answering can occur, HosPrime must test whether a minimum confirmation-evidence packet can reduce unresolved inventory gaps while preserving human review and source-use boundaries.

## Baseline inherited from #36 and #37

```text
TOTAL_SOURCE_RECORDS = 5
TOTAL_CONFIRMATION_CELLS = 50
PRESENT_CELLS = 15 / 50 = 30%
PENDING_CELLS = 15 / 50 = 30%
MISSING_CELLS = 20 / 50 = 40%
BASELINE_GAP_RATE = 35 / 50 pending_or_missing_cells = 70%
FULLY_CONFIRMED_RECORDS = 0 / 5
M1_B_RESEARCH_COMPLETED = true
RESEARCH_STAGING_ONLY = true
```

## Repository evidence checked before selecting work

- README North Star and Core Rules on `main` were read.
- Current release target remains Milestone 1 — Governed Knowledge Oracle MVP.
- Open issue #38 is the next ordered M1-B stage: HYPOTHESIS.
- Issue #38 explicitly forbids plan, build, source-register modification, ingestion, parsing, embedding, indexing, source approval, factual answering from placeholders and Organizational Memory / Governed RAG promotion.
- Source register remains placeholder-only:
  - five records exist;
  - lifecycle state remains `DISCOVERED`;
  - owner person remains pending;
  - controlled file/system location remains pending;
  - version remains pending;
  - checksum remains pending;
  - reviewer remains pending;
  - approval status remains `not_approved`;
  - active RAG index remains `false`.
- Recent PR evidence: PR #33 is closed/merged and added the executable CI gate for the M1 source register test.

## Research Staging inputs used

The previous research run staged general confirmation principles from W3C PROV, ISO 15489 public standard metadata, HHS HIPAA Security Rule summary and NIST AI RMF context. These remain Research Staging inputs only. They are not promoted to Organizational Memory / Governed RAG and do not authorize source use.

## Hypothesis

If each M1-B placeholder source record receives a minimum confirmation-evidence packet containing:

1. accountable source owner or owning office;
2. controlled location type and controlled location reference;
3. version, effective date or currentness status;
4. checksum value or explicitly accountable checksum-pending reason;
5. classification and access-policy confirmation;
6. authorized reviewer role and named reviewer or named reviewing office;
7. provenance confirmation method, confirmer and confirmation date;
8. known limitation note and superseded/replacement relationship where applicable;

then the source inventory pending/missing gap can be reduced from 70% to a measurable target without authorizing ingestion, parsing, approval, indexing, retrieval, factual answering or Organizational RAG promotion.

## Target metric for later PLAN / BUILD / TEST stages

The future controlled experiment should target:

```text
BASELINE_GAP_RATE = 35 / 50 = 70%
TARGET_GAP_RATE_AFTER_PACKET = <= 15 / 50 = <= 30%
TARGET_FULLY_CONFIRMED_RECORDS = >= 3 / 5
SOURCE_APPROVAL_CLAIMED = false
SOURCE_INGESTION_CLAIMED = false
RAG_ACTIVATION_CLAIMED = false
```

Rationale:

- A target of `<=30%` unresolved cells is large enough to show practical inventory improvement.
- `>=3/5` fully confirmed placeholder records is sufficient to test feasibility without over-claiming full M1 readiness.
- The target does not imply source authority, source approval, ingestion permission or factual-answer permission.

## Testable acceptance logic for later stages

A later TEST stage should pass only if all of the following are true:

```text
MINIMUM_CONFIRMATION_PACKET_FIELDS_PRESENT = true
CONFIRMATION_PACKET_APPLIED_TO_PLACEHOLDER_RECORDS = true
GAP_RATE_RECOMPUTED_WITH_AUDITABLE_METHOD = true
TARGET_GAP_RATE_AFTER_PACKET <= 30%
FULLY_CONFIRMED_RECORDS >= 3 / 5
ALL_RECORDS_REMAIN_NOT_APPROVED = true
ALL_ACTIVE_RAG_INDEX_FLAGS_REMAIN_FALSE = true
NO_APPROVED_OR_INDEXED_PLACEHOLDER_SOURCES = true
```

A later TEST stage should fail if any placeholder record is treated as factual source authority without human approval evidence.

## Boundary conditions

This HYPOTHESIS stage does not:

- create a plan;
- modify the source register;
- collect human confirmation evidence;
- approve a source;
- ingest, parse, chunk, embed or index a source;
- run retrieval;
- answer from placeholder evidence;
- promote Research Staging into Organizational Memory / Governed RAG.

## Stage result

```text
M1_B_HYPOTHESIS_DEFINED = true
MINIMUM_CONFIRMATION_PACKET_HYPOTHESIS_DEFINED = true
MEASURABLE_GAP_REDUCTION_TARGET_DEFINED = true
RESEARCH_STAGING_ONLY = true
INGESTION_PLANNING_ALLOWED = false
SOURCE_APPROVAL_CLAIMED = false
SOURCE_INGESTION_CLAIMED = false
RAG_ACTIVATION_CLAIMED = false
ORGANIZATIONAL_MEMORY_PROMOTION_CLAIMED = false
NEXT_ISSUE_CREATED = #39
```

## Memory layer affected

Research Staging only.

No Personal/Staff Twin Memory, Person Memory, Role Memory, Organizational Memory or Governed RAG was updated.

## Risks and blockers

- Named source owners are still missing.
- Controlled file/system locations are still missing.
- Version/effective date evidence is still missing.
- Checksum evidence is still missing.
- Human reviewer assignments are still missing.
- A later plan must prevent confirmation packets from being misread as approval packets.

## Single next stage

PLAN — work #39 to define the controlled source confirmation packet implementation plan and acceptance tests without altering the source register or activating any source.
