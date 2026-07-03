# HosPrime Engineering Run 0031 — M1-B Source Owner Evidence Real Problem

Date: 2026-07-04
Stage: REAL PROBLEM
Parent issue: #10
Control issue: #49
Previous stage: NEXT GOAL (#48)
Next stage: REAL USER

## North Star outcome supported

Enable healthcare and public-health organizations to use trusted data, knowledge, organizational memory and governed AI to complete real work and make better decisions faster, with evidence, accountability and continuous learning.

This stage supports:

- evidence quality;
- user trust;
- decision-to-outcome traceability;
- knowledge reuse;
- zero unauthorized high-impact action.

## Repository evidence checked before selecting work

- `README.md` on `main` confirms the North Star, ordered loop, current controlled release target and Core Rules.
- Current controlled release target remains Milestone 1 — Governed Knowledge Oracle MVP.
- Open issue #49 is the next ordered M1-B stage: REAL PROBLEM.
- Parent issue #10 requires governed source lifecycle controls, approved source versions, mandatory source owner / organization / classification / checksum / review evidence, restricted-source filtering, retrieval evaluation before activation, authenticated reviewer decisions and no backoffice-agent self-approval.
- Prior run `engineering_runs/2026-07-04/0030-m1b-source-owner-evidence-next-goal.md` selected controlled source-owner evidence collection as the next bounded goal.
- `docs/governance/M1_B_SOURCE_CONFIRMATION_MEMORY_BOUNDARY.md` states that inventory confirmation does not confer source authority, approval, ingestion, parsing, embedding, indexing, retrieval activation, factual-answer permission or Organizational Memory / Governed RAG promotion.
- `data/source_register/m1_source_register.yml` still shows five seed source records with `lifecycle_state: DISCOVERED`, `approval_status: not_approved` and `active_rag_index: false`.
- Recent pull request inspection found no open PR selected for this stage.

## Real organizational work problem

The immediate problem is not a lack of documents. The problem is that the organization cannot yet prove which source owner is accountable for each of the five M1 placeholder source records, where the controlled source is located, which version or effective date is authoritative, whether a checksum or non-file verification method exists, which classification and access policy apply, and which reviewer is assigned to make the later approval decision.

Because those controls are missing or pending, the five placeholder source records cannot support trusted retrieval, factual answers, executive briefs, decision support, audit evidence, or Organizational RAG promotion. Using them as if they were approved evidence would violate the Milestone 1 release target and the Core Rules:

```text
No Evidence -> No Factual Answer
No Human Approval -> No High-impact Action
No Execution Record -> Never Claim Completion
No Quality Gate -> No Release
```

## Real user affected

This problem affects real organizational users who need trusted knowledge for actual public-health and healthcare work:

- public-health executive who needs evidence-backed briefs and cannot rely on unowned placeholder sources;
- provincial program owner who must confirm whether a source package represents the current operational truth;
- data governance lead who must classify data, confirm access rules and prevent inappropriate retrieval;
- knowledge reviewer who must approve or reject sources with an audit trail;
- source inventory operator who must collect confirmation data without accidentally claiming source approval.

## Baseline and target metric

Baseline inherited from #36 through #49:

```text
TOTAL_SOURCE_RECORDS = 5
TOTAL_CONFIRMATION_CELLS = 50
PRESENT_CELLS = 15 / 50 = 30%
PENDING_CELLS = 15 / 50 = 30%
MISSING_CELLS = 20 / 50 = 40%
BASELINE_GAP_RATE = 35 / 50 pending_or_missing_cells = 70%
FULLY_CONFIRMED_RECORDS = 0 / 5
```

Target framing for the later collection packet, not achieved in this stage:

```text
TARGET_GAP_RATE_AFTER_LATER_COLLECTION_PACKET <= 30%
TARGET_FULLY_CONFIRMED_RECORDS_AFTER_LATER_COLLECTION_PACKET >= 3 / 5
```

## Stage decision

The bounded REAL PROBLEM is:

> M1 cannot safely proceed from placeholder source inventory toward review readiness because source-owner evidence is not yet collected, verified, or assigned to accountable reviewers for the five seed source records.

This stage only defines the problem. It does not collect evidence, update source records, review sources, approve sources, ingest sources, parse files, embed content, index content, activate retrieval, answer factual questions, or promote anything into Organizational Memory / Governed RAG.

## Work completed

- Defined the concrete source-owner evidence collection gap.
- Identified the real organizational users affected by the gap.
- Preserved the inherited 70% confirmation gap baseline.
- Preserved the later target of reducing the gap rate to <= 30% and reaching at least 3 / 5 fully confirmed source records after a future collection packet.
- Preserved the memory boundary that inventory confirmation is not source approval.
- Preserved the source register state: no approval, ingestion, indexing, retrieval activation, factual-answer permission or Organizational RAG promotion was claimed.
- Created the next executable issue for the REAL USER stage.

## Boundary assertions

```text
M1_B_REAL_PROBLEM_COMPLETED = true
SOURCE_OWNER_EVIDENCE_COLLECTION_GAP_DEFINED = true
REAL_ORGANIZATIONAL_PROBLEM_DEFINED = true
SOURCE_OWNER_EVIDENCE_COLLECTED = false
SOURCE_REGISTER_MODIFIED = false
SOURCE_APPROVAL_CLAIMED = false
SOURCE_INGESTION_CLAIMED = false
SOURCE_PARSING_CLAIMED = false
SOURCE_EMBEDDING_CLAIMED = false
SOURCE_INDEXING_CLAIMED = false
RAG_ACTIVATION_CLAIMED = false
FACTUAL_ANSWER_PERMISSION_CLAIMED = false
ORGANIZATIONAL_MEMORY_PROMOTION_CLAIMED = false
```

## Test / CI status

No executable CI success is claimed for this governance REAL PROBLEM stage.

Evidence basis:

- README inspection on `main`;
- open issue #49 inspection;
- parent issue #10 inspection via issue search result;
- prior run 0030 inspection;
- source confirmation memory-boundary document inspection;
- source register inspection;
- recent pull request lookup.

## Memory layer affected

Affected:

- engineering-run evidence;
- issue traceability;
- governance planning memory.

Not affected:

- Personal/Staff Twin Memory;
- Person Memory;
- Role Memory;
- Organizational Memory / Governed RAG;
- Research Staging promotion state;
- source-register approval status;
- source-register active-RAG status.

No source was collected, ingested, approved, indexed, retrieved from, answered from or promoted into Organizational RAG.

## Risks and blockers

- Source-owner evidence has not been collected.
- Named source owners remain unconfirmed.
- Controlled source locations remain unconfirmed.
- Version/effective date evidence remains unconfirmed.
- Checksum evidence or non-file verification method remains unconfirmed.
- Classification and access policy confirmation remain unverified by source owners.
- Reviewer assignments remain unconfirmed.
- The 70% confirmation gap remains until accountable source owners fill the packet and reviewers verify it.

## Stage result

```text
M1_B_REAL_PROBLEM_COMPLETED = true
SOURCE_OWNER_EVIDENCE_COLLECTION_GAP_DEFINED = true
TARGET_GAP_RATE_AFTER_LATER_COLLECTION_PACKET <= 30%
TARGET_FULLY_CONFIRMED_RECORDS_AFTER_LATER_COLLECTION_PACKET >= 3 / 5
SOURCE_APPROVAL_CLAIMED = false
SOURCE_INGESTION_CLAIMED = false
RAG_ACTIVATION_CLAIMED = false
```

## Single next stage

REAL USER — identify the accountable real users, roles and decision rights for collecting and reviewing source-owner evidence before any packet collection, source-register update, approval, ingestion planning or RAG activation.
