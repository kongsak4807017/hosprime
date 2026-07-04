# HosPrime Engineering Run 0047 — M1-B Source Owner Evidence Collection Readiness Real User

Date: 2026-07-04
Stage: REAL USER
Parent issue: #10
Memory epic: #8
Control issue: #65
Previous stage: REAL PROBLEM (#64)
Next stage: BASELINE

## North Star outcome supported

Enable healthcare and public-health organizations to use trusted data, knowledge, organizational memory and governed AI to complete real work and make better decisions faster, with evidence, accountability and continuous learning.

This bounded REAL USER stage supports:

- evidence quality;
- user trust;
- decision-to-outcome traceability;
- knowledge reuse;
- zero unauthorized high-impact action.

## Repository evidence checked before selecting work

- `README.md` on `main` confirms the North Star, ordered Loop Engineering sequence, Core Rules, memory boundaries and the current controlled release target: **Milestone 1 — Governed Knowledge Oracle MVP**.
- Open issue #65 is the next ordered M1-B stage: **REAL USER** for controlled source-owner evidence collection readiness.
- Previous run `engineering_runs/2026-07-04/0046-m1b-source-owner-evidence-collection-readiness-real-problem.md` completed the REAL PROBLEM stage and selected REAL USER as the next single stage.
- Parent issue #10 requires a governed backoffice pipeline with source discovery, quarantine, classification, review, approval, indexing only after authorization, retrieval evaluation and no backoffice-agent self-approval.
- `docs/governance/MATURITY_GATES.md` requires named document owners, captured source/version/classification/review dates, access controls and review gates before M1 can progress.
- `data/source_register/m1_source_register.yml` remains a placeholder register: all five seed records are `lifecycle_state: DISCOVERED`, `approval_status: not_approved`, and `active_rag_index: false`.
- Workflow check for commit `c15fd88da048e8b8de766095accd833dbd552f47` returned no workflow runs; no CI pass is claimed.
- Recent pull request inspection found no open PR superseding this bounded stage.

## Real organizational work problem

The five seed source records cannot safely advance toward collection, review, approval, ingestion, indexing or retrieval until accountable real users and decision rights are defined.

The practical risk is that source-owner evidence collection can be confused with approval. This stage therefore defines who may collect, confirm, classify, review and later approve or reject evidence, while keeping all placeholder records out of Organizational Memory / Governed RAG.

## Real users and decision rights

### 1. Public-health executive / accountable sponsor

Primary responsibility:

- owns the organizational need for trusted Knowledge Oracle outputs;
- confirms the priority of the five seed knowledge packs;
- accepts or rejects residual operational risk after formal review.

Decision rights in this stage:

- may confirm that controlled source-owner evidence collection is worth pursuing;
- may not approve sources for ingestion, indexing or retrieval without the later review record;
- may not override the Core Rules or memory-boundary controls.

Evidence boundary:

- executive sponsorship is governance intent, not source authority.

### 2. Provincial program source owner

Primary responsibility:

- confirms whether a source represents current operational truth for a knowledge pack;
- identifies the authoritative file, system, version, effective date and owner role;
- flags obsolete, superseded, duplicate, sensitive or conflicting records.

Decision rights in this stage:

- may provide or withhold source-owner evidence in a later collection packet;
- may confirm source authority and operational currency;
- may not self-approve a source into active Organizational RAG.

Evidence boundary:

- source-owner confirmation is required evidence, but it still needs later independent review before approval.

### 3. Source inventory operator

Primary responsibility:

- collects source metadata using the controlled packet;
- records file/system location, version, checksum or checksum-pending reason, provenance and limitations;
- preserves audit trail and does not alter the source register without authorized stage scope.

Decision rights in this stage:

- may prepare collection evidence in a later collection stage;
- may not classify approval status as approved;
- may not parse, embed, index, retrieve from or answer from collected files unless a later approved stage explicitly permits it.

Evidence boundary:

- inventory evidence is collection evidence only, not review or approval.

### 4. Data governance lead

Primary responsibility:

- confirms classification, access policy, allowed roles, retention concern and privacy/security constraints;
- enforces separation of Research Staging, Personal/Staff Twin Memory, Person Memory, Role Memory and Organizational Memory / Governed RAG.

Decision rights in this stage:

- may block progression if classification or access-policy evidence is incomplete;
- may require restricted handling for sensitive public-health, communicable disease, incident-command or staff-related sources;
- may not promote external or personal findings into organizational truth without a review record.

Evidence boundary:

- classification confirmation is a gate input, not source approval by itself.

### 5. Knowledge reviewer / independent reviewer

Primary responsibility:

- checks source-owner evidence completeness, consistency, currency and conflicts;
- recommends approve, reject, hold, expire or supersede in a later review stage;
- ensures reviewers are independent from collection-only actors for high-impact or restricted sources.

Decision rights in this stage:

- may define review expectations;
- may not claim a completed review until a review artifact, accountable reviewer and audit record exist;
- may not activate retrieval or factual-answer permission.

Evidence boundary:

- review readiness is not review completion.

## RACI-style boundary for later collection readiness

| Work decision | Sponsor | Source owner | Inventory operator | Data governance lead | Independent reviewer |
| --- | --- | --- | --- | --- | --- |
| Prioritize seed knowledge pack | Accountable | Consulted | Informed | Consulted | Informed |
| Identify authoritative source | Informed | Accountable | Responsible | Consulted | Consulted |
| Record metadata/checksum/provenance | Informed | Consulted | Responsible | Consulted | Informed |
| Confirm classification/access policy | Informed | Consulted | Responsible for capture | Accountable | Consulted |
| Check evidence completeness | Informed | Consulted | Consulted | Consulted | Accountable |
| Approve/reject source for later ingestion | Accountable after review | Consulted | No authority | Required gate | Responsible recommendation |
| Activate RAG retrieval | No authority in this stage | No authority in this stage | No authority in this stage | Gate only | No authority in this stage |

## Baseline and target metric

Baseline inherited from issue #65 and previous M1-B evidence:

```text
M1_B_REAL_PROBLEM_COMPLETED = true
REAL_PROBLEM_DEFINED_FOR_SOURCE_OWNER_EVIDENCE_COLLECTION_READINESS = true
ROLE_READINESS_GAP_RATE = 54.3%
CONFIRMATION_GAP_RATE = 70%
FULLY_ROLE_READY_RECORDS = 0 / 5
FULLY_CONFIRMED_RECORDS = 0 / 5
SOURCE_REGISTER_MODIFIED = false
SOURCE_OWNER_EVIDENCE_COLLECTED = false
SOURCE_APPROVAL_CLAIMED = false
SOURCE_INGESTION_CLAIMED = false
RAG_ACTIVATION_CLAIMED = false
```

Target for this stage only:

```text
M1_B_REAL_USER_COMPLETED = true
REAL_USERS_DEFINED_FOR_SOURCE_OWNER_EVIDENCE_COLLECTION_READINESS = true
ROLE_BOUNDARIES_DEFINED = true
DECISION_RIGHTS_DEFINED = true
NEXT_STAGE = BASELINE
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

## Work completed

- Defined the accountable real users for controlled source-owner evidence collection readiness.
- Defined role boundaries and decision rights for sponsor, source owner, inventory operator, data governance lead and independent reviewer.
- Added a RACI-style boundary separating collection, confirmation, classification, review recommendation, approval and retrieval activation.
- Preserved the inherited 54.3% role-readiness gap and 70% confirmation gap baseline.
- Preserved the later target of reducing the confirmation gap to <= 30% and reaching at least 3 / 5 fully confirmed records after a future collection packet.
- Preserved source-register and memory boundaries: no source was approved, ingested, parsed, embedded, indexed, retrieved from, answered from or promoted into Organizational RAG.
- Selected the next single stage: BASELINE.

## Boundary assertions

```text
M1_B_REAL_USER_COMPLETED = true
REAL_USERS_DEFINED_FOR_SOURCE_OWNER_EVIDENCE_COLLECTION_READINESS = true
ROLE_BOUNDARIES_DEFINED = true
DECISION_RIGHTS_DEFINED = true
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

No executable CI success is claimed for this governance REAL USER stage.

Evidence basis:

- README inspection on `main`;
- open issue #65 inspection;
- parent issue #10 inspection;
- prior run 0046 inspection;
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
- Named source owners remain unconfirmed in the source register.
- Controlled source locations remain unconfirmed.
- Version/effective date evidence remains unconfirmed.
- Checksum evidence or non-file verification method remains unconfirmed.
- Classification and access-policy confirmation remain unverified by real source owners.
- Reviewer assignments remain unconfirmed.
- The 70% confirmation gap remains until accountable source owners fill the packet and reviewers verify it.
- No CI run is available for this evidence-only stage.

## Stage result

```text
M1_B_REAL_USER_COMPLETED = true
REAL_USERS_DEFINED_FOR_SOURCE_OWNER_EVIDENCE_COLLECTION_READINESS = true
ROLE_BOUNDARIES_DEFINED = true
DECISION_RIGHTS_DEFINED = true
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

BASELINE — measure the current source-owner evidence collection readiness baseline against the defined user roles and decision-right boundaries before research, hypothesis, plan, build, test, evaluate, review, release, observe, learn or memory correction.
