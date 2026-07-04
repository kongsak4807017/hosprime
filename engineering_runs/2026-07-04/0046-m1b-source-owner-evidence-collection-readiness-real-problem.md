# HosPrime Engineering Run 0046 — M1-B Source Owner Evidence Collection Readiness Real Problem

Date: 2026-07-04
Stage: REAL PROBLEM
Parent issue: #10
Memory epic: #8
Control issue: #64
Previous stage: NEXT GOAL (#63)
Next stage: REAL USER

## North Star outcome supported

Enable healthcare and public-health organizations to use trusted data, knowledge, organizational memory and governed AI to complete real work and make better decisions faster, with evidence, accountability and continuous learning.

This bounded REAL PROBLEM stage supports:

- evidence quality;
- user trust;
- decision-to-outcome traceability;
- knowledge reuse;
- zero unauthorized high-impact action.

## Repository evidence checked before selecting work

- `README.md` on `main` confirms the North Star, the ordered Loop Engineering sequence, the Core Rules, memory boundaries and the current controlled release target: **Milestone 1 — Governed Knowledge Oracle MVP**.
- Open issue #64 is the next ordered M1-B stage: **REAL PROBLEM** for controlled source-owner evidence collection readiness.
- Parent issue #10 requires a governed backoffice pipeline for approved RAG sources, including source discovery, quarantine, classification, review, approval, indexing only after authorization, retrieval evaluation and no backoffice-agent self-approval.
- Epic #8 anchors this work to evidence-driven loop engineering and separated memory layers.
- Previous stage evidence exists at `engineering_runs/2026-07-04/0045-m1b-source-owner-evidence-next-goal.md`, which selected this new ordered loop and explicitly set `NEXT_STAGE = REAL_PROBLEM`.
- `docs/governance/MATURITY_GATES.md` confirms that M1 source and ingestion readiness requires approved documents, named owners, source/version/classification/review dates, parsing success and access controls before unrestricted progression.
- `data/source_register/m1_source_register.yml` remains a placeholder register: all five seed records are `lifecycle_state: DISCOVERED`, `approval_status: not_approved`, and `active_rag_index: false`.
- Workflow check for commit `ac44e03980bb89ff664624d5cc4a7d518eb2362b` returned no workflow runs; no CI pass is claimed.
- Recent pull request inspection found no open PR superseding this bounded stage.

## Real organizational work problem

The immediate operational problem is that HosPrime cannot yet move the five seed knowledge-pack source records from placeholder inventory toward evidence collection readiness because the project lacks a controlled, auditable definition of what source-owner evidence must prove before any collection packet can be treated as review-ready.

The risk is not only that files are missing. The risk is that a future operator could collect partial information and mistakenly treat it as source authority, approval, ingestion permission, or Organizational RAG truth. That would violate the M1 controlled release target and the Core Rules.

The problem to solve in this loop is therefore:

> The five seed source records cannot safely advance toward collection, review, approval, ingestion, indexing or retrieval until the project defines the operational readiness gap: which owner/reviewer/location/version/checksum/classification/access-policy evidence is missing, who is affected by the gap, and what later evidence threshold would make collection reviewable without promoting placeholder data into organizational truth.

## Real user affected

The problem affects real organizational users who need trusted M1 Knowledge Oracle evidence for public-health and healthcare work:

- public-health executive / accountable sponsor who needs evidence-backed briefs and must avoid unowned source claims;
- provincial program source owner who must confirm whether a knowledge-pack source represents current operational truth;
- source inventory operator who must collect evidence without accidentally claiming approval;
- data governance lead who must confirm classification, access policy and memory boundary controls;
- knowledge reviewer / independent reviewer who must approve or reject a source using an audit trail.

## Baseline and target metric

Baseline inherited from issue #64 and prior M1-B evidence:

```text
M1_B_NEXT_GOAL_COMPLETED = true
NEXT_STAGE = REAL_PROBLEM
NEXT_GOAL_SUPPORTS_SOURCE_OWNER_EVIDENCE_COLLECTION_READINESS = true
ROLE_READINESS_GAP_RATE = 54.3%
FULLY_ROLE_READY_RECORDS = 0 / 5
CONFIRMATION_GAP_RATE = 70%
FULLY_CONFIRMED_RECORDS = 0 / 5
SOURCE_REGISTER_MODIFIED = false
SOURCE_OWNER_EVIDENCE_COLLECTED = false
SOURCE_APPROVAL_CLAIMED = false
SOURCE_INGESTION_CLAIMED = false
RAG_ACTIVATION_CLAIMED = false
```

Target for this stage only:

```text
M1_B_REAL_PROBLEM_COMPLETED = true
REAL_PROBLEM_DEFINED_FOR_SOURCE_OWNER_EVIDENCE_COLLECTION_READINESS = true
REAL_USER_GROUPS_REFERENCED = true
BASELINE_GAPS_REFERENCED = true
NEXT_STAGE = REAL_USER
SOURCE_REGISTER_MODIFIED = false
SOURCE_APPROVAL_CLAIMED = false
SOURCE_INGESTION_CLAIMED = false
RAG_ACTIVATION_CLAIMED = false
```

Later collection target, not achieved in this stage:

```text
TARGET_GAP_RATE_AFTER_LATER_COLLECTION_PACKET <= 30%
TARGET_FULLY_CONFIRMED_RECORDS_AFTER_LATER_COLLECTION_PACKET >= 3 / 5
```

## Stage decision

The bounded REAL PROBLEM is:

> M1-B source-owner evidence collection readiness is blocked because the project has five placeholder seed records but lacks reviewable evidence of accountable source owners, controlled source locations, authoritative versions/effective dates, checksums or non-file verification methods, reviewer assignments, classification/access-policy confirmation and audit records.

This stage only defines the problem. It does not collect evidence, update source records, review sources, approve sources, ingest sources, parse files, embed content, index content, activate retrieval, answer factual questions, execute external actions, or promote anything into Organizational Memory / Governed RAG.

## Work completed

- Defined the source-owner evidence collection readiness gap as a real operational problem, not a document-production task.
- Linked the problem to M1 Governed Knowledge Oracle MVP and the North Star metric: Trusted Task Completion Rate.
- Referenced the real user groups affected by the gap.
- Preserved the inherited 54.3% role-readiness gap and 70% confirmation gap baseline.
- Preserved the later target of reducing the confirmation gap to <= 30% and reaching at least 3 / 5 fully confirmed records after a future collection packet.
- Preserved memory and source-register boundaries: placeholder inventory is not approval, not ingestion permission and not Organizational RAG truth.
- Selected the next single stage: REAL USER.

## Boundary assertions

```text
M1_B_REAL_PROBLEM_COMPLETED = true
REAL_PROBLEM_DEFINED_FOR_SOURCE_OWNER_EVIDENCE_COLLECTION_READINESS = true
REAL_USER_GROUPS_REFERENCED = true
BASELINE_GAPS_REFERENCED = true
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
- open issue #64 inspection;
- parent issue #10 inspection;
- epic #8 inspection;
- prior run 0045 inspection through latest `main` commit;
- maturity gates inspection;
- source register inspection;
- workflow check for previous commit, which returned no workflow runs;
- recent PR lookup, which found no open PR selected for this stage.

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
- Classification and access-policy confirmation remain unverified by source owners.
- Reviewer assignments remain unconfirmed.
- The 70% confirmation gap remains until accountable source owners fill the packet and reviewers verify it.
- No CI run is available for this evidence-only stage.

## Stage result

```text
M1_B_REAL_PROBLEM_COMPLETED = true
REAL_PROBLEM_DEFINED_FOR_SOURCE_OWNER_EVIDENCE_COLLECTION_READINESS = true
ROLE_READINESS_GAP_RATE = 54.3%
CONFIRMATION_GAP_RATE = 70%
TARGET_GAP_RATE_AFTER_LATER_COLLECTION_PACKET <= 30%
TARGET_FULLY_CONFIRMED_RECORDS_AFTER_LATER_COLLECTION_PACKET >= 3 / 5
SOURCE_REGISTER_MODIFIED = false
SOURCE_APPROVAL_CLAIMED = false
SOURCE_INGESTION_CLAIMED = false
RAG_ACTIVATION_CLAIMED = false
CI_PASS_CLAIMED = false
```

## Single next stage

REAL USER — identify the accountable real users, role boundaries and decision rights for controlled source-owner evidence collection readiness before any packet collection, source-register update, approval, ingestion planning or RAG activation.
