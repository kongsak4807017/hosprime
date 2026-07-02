# Engineering Run 2026-07-03-0003 — M1-A Source Register Build

## Run status

- Loop stage: `BUILD`
- Terminal state: not terminal
- Linked issue: #15 — M1-A Build: Initial source register
- Controlling plan issue: #14 — M1-A source-register plan
- Parent issue: #10 — Organizational Memory Backoffice Pipeline
- Memory layer affected: Research Staging / engineering evidence only; no promotion into Organizational RAG

## North Star outcome supported

This build supports evidence-based decisions, reduced repetitive workload and continuous organizational learning by creating the first auditable source-readiness register before M1 ingestion, embedding or retrieval activation.

## Real user and real work problem

Public-health executives, program owners, data governance officers and knowledge reviewers need answers from approved, traceable and access-controlled organizational evidence. Before retrieval can be trusted, HosPrime must know which sources exist, who owns them, how they are classified, whether they were reviewed and whether they may be retrieved.

## Current controlled release target

M1 remains **Governed Knowledge Oracle MVP**: approved document ingestion, evidence retrieval, sufficient-evidence answering, traceable citations, access control, and audit/cost recording.

## Work completed

Added the initial register:

```text
data/source_register/m1_source_register.yml
```

Seed records created:

1. `M1A-PM25-001` — PM2.5 and Environmental Health
2. `M1A-TB-001` — Tuberculosis and Communicable Disease Control
3. `M1A-NCD-001` — NCD and Chronic Care Service Model
4. `M1A-EOC-001` — Disaster, EOC and Public Health Emergency Operations
5. `M1A-DIGITAL-001` — Digital Health, Data Governance and AI Workflow

All records are placeholders only. They are not approved evidence.

## Governance boundary preserved

The register states that active RAG activation is not allowed and human approval is required before any approved state.

Every seed record remains:

```text
lifecycle_state: DISCOVERED
review_status: not_reviewed
approval_status: not_approved
active_rag_index: false
```

No source was ingested, embedded, indexed or promoted into Organizational RAG.

## Validation tests added

Added:

```text
tests/test_m1_source_register.py
```

The tests validate that the register exists, contains five priority knowledge packs, includes mandatory metadata fields, keeps seed records in allowed seed states, prevents approval/indexing, and requires role-scoped access for restricted records.

## Baseline and target metric update

Previous baseline:

```text
M1_A_SOURCE_REGISTER_EXISTS = false
M1_A_BASELINE_COVERAGE = not measurable
```

Current build state:

```text
M1_A_SOURCE_REGISTER_EXISTS = true
M1_A_SEED_RECORDS = 5
M1_A_SEED_KNOWLEDGE_PACKS = 5
M1_A_APPROVED_RECORDS = 0
M1_A_ACTIVE_RAG_INDEXED_RECORDS = 0
M1_A_SEED_RECORDS_WITH_REQUIRED_FIELDS = pending TEST stage
```

## Test / CI status

- Validation test file added: yes.
- No GitHub Actions workflow runs were found for commit `2f372776aa0bce3454102ffd3c65af49376df432` at inspection time.
- Test success is not claimed in this BUILD run.

## GitHub changes

- Register commit: `d466a8d633903d507737b33e847da83ded223585`
- Test commit: `2f372776aa0bce3454102ffd3c65af49376df432`

## Risks and blockers

- Actual source files, owners and reviewers are still pending human inventory.
- Seed records are placeholders only and cannot be used as factual evidence.
- Future implementation must not allow activation without reviewer, decision date, classification and access policy validation.

## Decision

BUILD for issue #15 is complete because the initial register file and validation test file now exist on `main`.

This does not complete TEST, EVALUATE, REVIEW, RELEASE or OBSERVE.

## Next single stage

`TEST`: execute `tests/test_m1_source_register.py`, record pass/fail evidence, and make a bounded correction only if validation fails.
