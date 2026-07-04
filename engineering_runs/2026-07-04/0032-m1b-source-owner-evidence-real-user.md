# HosPrime Engineering Run 0032 — M1-B Source Owner Evidence Real User

Date: 2026-07-04
Stage: REAL USER
Parent issue: #10
Control issue: #50
Previous stage: REAL PROBLEM (#49)
Next stage: BASELINE

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
- Open issue #50 is the next ordered M1-B stage: REAL USER.
- No open pull request was available or selected for this governance stage.
- Parent issue #10 requires governed source lifecycle controls, approved source versions, mandatory ownership / organization / classification / checksum / review evidence, restricted-source filtering, retrieval evaluation before activation, authenticated reviewer decisions and no backoffice-agent self-approval.
- `data/source_register/m1_source_register.yml` still shows five seed source records with `lifecycle_state: DISCOVERED`, `approval_status: not_approved` and `active_rag_index: false`.
- Prior run `engineering_runs/2026-07-04/0030-m1b-source-owner-evidence-next-goal.md` selected controlled source-owner evidence collection as the next loop goal, starting again from REAL PROBLEM.

## Real user and real organizational work problem

Real organizational users for this bounded M1-B evidence-collection loop:

1. **Public-health executive / accountable sponsor**
   - Uses the final approved Knowledge Oracle outputs for high-accountability briefings, decisions and follow-up.
   - Needs assurance that no source becomes authoritative without ownership, review and audit evidence.
   - May approve the controlled release boundary and accept residual risk, but should not self-approve source evidence that they personally submitted.

2. **Provincial program source owner**
   - Provides source-owner evidence for each knowledge pack, such as PM2.5/environmental health, TB, NCD, EOC/disaster or digital health/data governance.
   - Confirms whether the source exists, where the controlled source is held, which version/effective date is current, who owns it, and whether it is appropriate for internal or restricted use.
   - May not self-approve a source for active Organizational RAG.

3. **Source inventory operator**
   - Collects the confirmation packet from source owners.
   - Records packet completeness, missing fields and limitations.
   - May not reinterpret, approve, ingest, parse, embed, index or activate sources.

4. **Data governance lead**
   - Confirms classification, access policy, retention sensitivity and whether the source contains restricted operational or personal information.
   - Defines whether a source is internal, restricted internal or requires additional controls before review.
   - May stop or defer evidence collection when access classification is unclear.

5. **Knowledge reviewer / independent reviewer**
   - Reviews source-owner evidence and confirms whether the packet is ready for later source-register update.
   - Must be separate from the source submitter for high-impact or restricted sources.
   - May recommend approval, rejection, deferral or additional evidence, but active RAG promotion requires the later governed stage and audit record.

## Decision-rights matrix

| Decision or action | Source owner | Inventory operator | Data governance lead | Knowledge reviewer | Executive sponsor |
|---|---:|---:|---:|---:|---:|
| Provide controlled source existence evidence | Responsible | Support | Consult | Consult | Informed |
| Identify controlled source location | Responsible | Record | Consult | Consult | Informed |
| Confirm version/effective date | Responsible | Record | Consult | Review | Informed |
| Provide checksum or non-file verification method | Responsible | Record | Consult | Review | Informed |
| Confirm classification and access policy | Consult | Record | Responsible | Review | Informed |
| Mark packet fields present/pending/missing | Consult | Responsible | Consult | Review | Informed |
| Declare source approved | Not alone | No | No | Recommend only | Approve only through later governed review |
| Ingest, parse, embed or index source | No | No | No | No | No in this stage |
| Activate source for Organizational RAG | No | No | No | No | No in this stage |
| Generate factual answer from source | No | No | No | No | No in this stage |

## Baseline and target metric

Baseline inherited from #36 through #50:

```text
TOTAL_SOURCE_RECORDS = 5
TOTAL_CONFIRMATION_CELLS = 50
PRESENT_CELLS = 15 / 50 = 30%
PENDING_CELLS = 15 / 50 = 30%
MISSING_CELLS = 20 / 50 = 40%
BASELINE_GAP_RATE = 35 / 50 pending_or_missing_cells = 70%
FULLY_CONFIRMED_RECORDS = 0 / 5
```

Target framing for later packet collection, not claimed in this stage:

```text
REAL_USER_DEFINED = true
SOURCE_OWNER_EVIDENCE_COLLECTION_ROLES_DEFINED = true
DECISION_RIGHTS_DEFINED = true
TARGET_GAP_RATE_AFTER_LATER_COLLECTION_PACKET <= 30%
TARGET_FULLY_CONFIRMED_RECORDS_AFTER_LATER_COLLECTION_PACKET >= 3 / 5
```

## Work completed

- Completed exactly one loop stage: REAL USER.
- Defined accountable real users for source-owner evidence collection.
- Defined role boundaries for source owner, inventory operator, data governance lead, independent reviewer and executive sponsor.
- Defined decision rights and prohibited actions for this stage.
- Preserved all M1 source-register approval, ingestion and active-RAG boundaries.
- Created the next executable issue for the BASELINE stage.

## Boundary assertions

```text
M1_B_REAL_USER_COMPLETED = true
REAL_USERS_DEFINED = true
SOURCE_OWNER_EVIDENCE_COLLECTION_ROLES_DEFINED = true
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

No executable CI success is claimed for this governance role-definition stage.

Evidence basis:

- README inspection on `main`;
- open issue #50 inspection;
- parent issue #10 search result inspection;
- source-register inspection;
- prior engineering run 0030 inspection;
- open pull request lookup returned no open pull requests.

## Memory layer affected

Affected:

- engineering-run evidence;
- issue traceability;
- governance planning memory.

Not affected:

- Personal/Staff Twin Memory;
- Person Memory;
- Role Memory as active runtime memory;
- Organizational Memory / Governed RAG;
- Research Staging promotion state;
- source-register approval status;
- source-register active-RAG status.

No source was ingested, approved, indexed, retrieved from, answered from or promoted into Organizational RAG.

## Risks and blockers

- Source-owner evidence has not been collected.
- Named source owners remain unconfirmed.
- Controlled source locations remain unconfirmed.
- Version/effective date evidence remains unconfirmed.
- Checksum or non-file verification evidence remains unconfirmed.
- Reviewer assignments remain unconfirmed.
- The 70% confirmation gap remains until accountable source owners fill the packet and reviewers verify it.

## Stage result

```text
M1_B_REAL_USER_COMPLETED = true
REAL_USERS_DEFINED = true
SOURCE_OWNER_EVIDENCE_COLLECTION_ROLES_DEFINED = true
DECISION_RIGHTS_DEFINED = true
SOURCE_APPROVAL_CLAIMED = false
SOURCE_INGESTION_CLAIMED = false
RAG_ACTIVATION_CLAIMED = false
```

## Single next stage

BASELINE — measure the role-coverage and decision-rights readiness baseline for the five M1 placeholder source records before any evidence collection, source-register update, ingestion planning or RAG activation.
