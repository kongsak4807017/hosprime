# Engineering Run 2026-07-03-0001 — M1 Organizational Memory Baseline

## Run status

- Loop stage: `BASELINED`
- Terminal state: not terminal
- Linked issue: #10 — M1/M4: Build Organizational Memory Backoffice Pipeline
- Parent epic: #8 — Loop Engineering and Two-Layer Memory Runtime
- Commit inspected: `1380e1915d7cf9171ebcbfb5d5017d5f0a4de4ae`
- CI/status check inspected: GitHub combined status returned no statuses for the inspected commit
- Memory layer affected: Research Staging / engineering evidence only; no promotion into Organizational RAG

## North Star outcome supported

This run supports evidence-based decisions, reduced repetitive workload and continuous organizational learning. It does not add agents, screens or autonomous execution. It clarifies the baseline needed before the Governed Knowledge Oracle can safely ingest and retrieve organizational evidence.

## Real user and real work problem

Target user group:

- Public-health executive, program owner, knowledge officer, data governance officer and quality reviewer.

Real work problem:

- Users need to ask policy, SOP, operational and historical decision questions and receive answers only from approved, traceable and access-controlled evidence.
- Current project artifacts define the goal and gate requirements, but the M1 organizational-memory ingestion baseline is not yet recorded as an executable evidence package.

## Current controlled release target

M1 remains **Governed Knowledge Oracle MVP**. Success requires approved document ingestion, evidence retrieval, sufficient-evidence answering, traceable citations, access control, and audit/cost recording.

## Internal evidence inspected

1. `README.md`
   - North Star requires trusted data, knowledge, organizational memory and governed AI to complete real work faster with evidence, accountability and learning.
   - Core rules include: No Evidence -> No Factual Answer; No Identity -> No Access; No Human Approval -> No High-impact Action; No Execution Record -> Never Claim Completion; No Baseline -> No Improvement Claim; No Quality Gate -> No Release; No Observation -> No Learning.
   - Memory boundaries require Research Staging, Personal/Staff Twin Memory, Role Memory and Organizational RAG to remain separated.

2. `docs/governance/MATURITY_GATES.md`
   - M1-A Source and ingestion readiness requires at least 100 approved documents across five knowledge packs; named owner for every document; source, version, classification and review date; duplicate detection; parsing success >=95%; failed documents visible and recoverable; restricted documents inaccessible to unauthorized roles.
   - M1-B Retrieval readiness requires at least 100 answerable questions, 30 unanswerable questions, 20 ambiguous/conflicting-source questions and representation from every knowledge pack.
   - M1-C Answer and citation trust requires groundedness >=0.90, citation precision >=0.90, citation completeness >=0.90, false factual answer rate below 2%, no fabricated document title/page/metric, and recording model, prompt version, evidence IDs and cost.

3. `docs/governance/SUCCESS_SCORECARD.md`
   - M1 pilot target for Trusted Task Completion Rate is at least 80%.
   - Knowledge readiness targets include approved document coverage >=90%, metadata completeness >=95%, named ownership 100%, review-date coverage >=95%, parsing success >=95%, duplicate rate <5% and obsolete-source rate <5%.
   - Baseline protocol requires selecting 20–30 representative tasks, observing the current process, recording elapsed time/touch time/people/errors/rework, repeating with HosPrime, and comparing medians and distributions.

4. Issue #10
   - Defines the Organizational Memory Backoffice Pipeline with source discovery, quarantine, parsing, classification, quality, review, approval, indexing, retrieval evaluation, promotion and freshness controls.

## Baseline finding

Baseline is **not yet sufficient for M1-A execution**.

Current baseline recorded in this run:

| Capability | Baseline state | Evidence | M1 target / required state |
|---|---|---|---|
| Approved source inventory | Not yet found as a concrete inventory artifact in this run | README, maturity gates and issue #10 define requirements, not an actual source register | >=100 approved documents across five knowledge packs |
| Mandatory source metadata | Requirement exists; actual completeness not yet measured | Maturity Gates + Scorecard | source owner 100%, metadata completeness >=95%, review-date coverage >=95% |
| Parsing readiness | Not yet measured | Maturity Gates | parsing success >=95% |
| Duplicate/obsolete control | Requirement exists; active rate not measured | Maturity Gates + Scorecard | duplicate rate <5%, obsolete-source rate <5% |
| Access filtering | Requirement exists; no baseline test result captured in this run | README + Maturity Gates | zero restricted-source access violations |
| Retrieval evaluation set | Not yet found as a concrete evaluation dataset in this run | Maturity Gates | 100 answerable, 30 unanswerable, 20 ambiguous/conflicting-source questions |
| Cost/audit evidence | Requirement exists; no baseline measurement captured in this run | README + M1 target | every answer records model, prompt version, evidence IDs and cost |

## Baseline metric selected

Primary baseline metric for the next M1 step:

```text
M1-A Source Readiness Baseline Coverage
= source records with all mandatory fields complete
  / identified priority source records
```

Mandatory fields for the baseline register:

- source_id
- title
- knowledge_pack
- source_owner
- organization
- source_type
- file_or_system_location
- version
- checksum
- classification
- access_role
- review_date
- expiry_or_next_review_date
- ingestion_status
- parsing_status
- quality_status
- approval_status
- reviewer
- decision_date
- limitation_note

Initial measured value for this run: **not measurable yet** because the source register has not been created or located.

Baseline state is therefore recorded as:

```text
M1_A_SOURCE_REGISTER_EXISTS = false
M1_A_BASELINE_COVERAGE = not measurable
```

## Target metric

Next measurable target:

```text
Create an initial source-readiness register schema and seed at least 5 placeholder priority source records representing the five required knowledge packs, with status set to DISCOVERED or QUARANTINED only, not APPROVED.
```

Acceptance target for the next stage:

- 100% of seeded records contain required metadata fields.
- 0 records are marked approved without reviewer and decision date.
- 0 records are indexed into active Organizational RAG.
- The schema can later measure M1-A coverage against the >=100 document target.

## Decision

Proceed to **Plan** in the next bounded run for issue #10.

The next run should create a minimal, auditable source-register plan and schema before implementing ingestion or indexing. No code should index organizational knowledge until the source register, review state and access metadata exist.

## Risks and blockers

- Risk: implementing retrieval before source ownership and approval states would violate M1-A and the README core rule `No Evidence -> No Factual Answer`.
- Risk: marking documents approved from an automation run would violate the required human-review boundary.
- Blocker: actual priority document list and accountable source owners are not yet captured in repository evidence.

## Next single stage

`PLAN`: define the M1-A source register schema, lifecycle states, seed-register file location, validation rules and tests linked to issue #10.
