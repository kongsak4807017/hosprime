# HosPrime Engineering Run 0036 — M1-B Source Owner Evidence Plan

Date: 2026-07-04
Stage: PLAN
Parent issue: #10
Control issue: #54
Previous stage: HYPOTHESIS (#53)
Next stage: BUILD

## North Star outcome supported

Enable healthcare and public-health organizations to use trusted data, knowledge, organizational memory and governed AI to complete real work and make better decisions faster, with evidence, accountability and continuous learning.

This bounded PLAN stage supports:

- evidence quality;
- user trust;
- decision-to-outcome traceability;
- knowledge reuse;
- zero unauthorized high-impact action.

## Repository evidence checked before selecting work

- `README.md` on `main` confirms the North Star, ordered loop, current controlled release target and Core Rules.
- Current controlled release target remains **Milestone 1 — Governed Knowledge Oracle MVP**.
- Open issue #54 is the next ordered M1-B stage: **PLAN**.
- Parent issue #10 requires governed source lifecycle with ownership, classification, quality checking, review evidence and activation only after authorized review.
- `docs/governance/MATURITY_GATES.md` requires named owner for every document, source/version/classification/review date captured and restricted documents inaccessible to unauthorized roles.
- `data/source_register/m1_source_register.yml` still contains five seed records, all `lifecycle_state: DISCOVERED`, `approval_status: not_approved`, and `active_rag_index: false`.
- `docs/governance/M1_B_CONTROLLED_SOURCE_CONFIRMATION_PACKET.md` is a controlled release artifact for inventory confirmation only and explicitly prohibits approval, ingestion, indexing, factual-answer permission or Organizational RAG promotion claims.
- Prior run `engineering_runs/2026-07-04/0035-m1b-source-owner-evidence-hypothesis.md` defined the hypothesis for adding role-assignment evidence field groups to a later packet update.
- Open pull request lookup returned no open pull requests for this governance plan stage.
- Workflow-run lookup for commit `3bed2d5912beefcd80e892c738b4d0588bfde3e3` returned no workflow runs; no CI pass is claimed.

## Real user and real organizational work problem

Real users:

- public-health executive / accountable sponsor;
- provincial program source owner;
- source inventory operator;
- data governance lead;
- knowledge reviewer / independent reviewer.

Real work problem:

The M1 placeholder source records cannot safely proceed toward source-owner evidence collection because role authority, named assignment, independent reviewer routing and decision scope remain unconfirmed. The next packet revision needs an explicit plan for collecting role-assignment evidence without implying source approval, ingestion, indexing, retrieval activation or permission to answer factual questions from those sources.

## Current loop stage

Completed exactly one stage: **PLAN**.

No build, test, evaluation, review, release, observation, learning, memory-correction or next-goal stage was performed in this run.

## Baseline inherited from #51–#53

```text
TOTAL_SOURCE_RECORDS = 5
CONFIRMATION_GAP_RATE = 70%
ROLE_READINESS_GAP_RATE = 54.3%
FULLY_CONFIRMED_RECORDS = 0 / 5
FULLY_ROLE_READY_RECORDS = 0 / 5
ROLE_ASSIGNMENT_PACKET_HYPOTHESIS_DEFINED = true
SOURCE_OWNER_EVIDENCE_COLLECTED = false
SOURCE_APPROVAL_CLAIMED = false
SOURCE_INGESTION_CLAIMED = false
RAG_ACTIVATION_CLAIMED = false
```

## Plan objective

Define a bounded build plan for updating the controlled source confirmation packet with role-assignment evidence fields that can later reduce the role-readiness gap from **54.3%** to **<=30%** after accountable completion and reviewer check.

This plan does **not** update the packet itself.

## Planned packet field groups for the later BUILD stage

The later BUILD stage should add a distinct `role_assignment_evidence` section to the packet template, separate from the existing ten inventory confirmation cells.

Planned field groups:

### 1. Authority basis and decision scope

Purpose: prove why the named person or office can act as source owner or accountable office for a source record.

Planned fields:

```yaml
authority_basis:
  status: ""
  authority_type: ""
  authority_reference: ""
  decision_scope: "inventory_confirmation_only"
  approval_boundary_acknowledged: true
  evidence_note: ""
  accountable_owner_for_pending: ""
```

Gap addressed:

- owner role exists but authority basis is not proven;
- source ownership must not be confused with source approval.

### 2. Named human or approved office assignment mapped to source ID

Purpose: identify a real accountable person or approved office without inventing names or authority.

Planned fields:

```yaml
source_owner_assignment:
  status: ""
  source_id: ""
  assigned_person_or_office: ""
  assignment_method: ""
  assignment_date: ""
  assigned_by: ""
  assignment_limitations: ""
  evidence_note: ""
  accountable_owner_for_pending: ""
```

Gap addressed:

- `owner_person` remains `pending_human_assignment` in all five seed records;
- fully role-ready records remain 0 / 5.

### 3. Independent reviewer routing by gate

Purpose: define who checks the role assignment before any later source review proceeds.

Planned fields:

```yaml
independent_reviewer_routing:
  status: ""
  reviewer_person_or_office: ""
  reviewer_role: ""
  review_gate: "role_assignment_precheck"
  conflict_of_interest_check: ""
  escalation_path: ""
  evidence_note: ""
  accountable_owner_for_pending: ""
```

Gap addressed:

- `reviewer` remains `pending_human_reviewer` in all five seed records;
- independent review route is not yet auditable.

### 4. Access/classification confirmation with restricted-source handling

Purpose: confirm that role assignment does not weaken classification or bypass restricted-source access controls.

Planned fields:

```yaml
access_classification_role_check:
  status: ""
  classification_confirmed_or_disputed: ""
  access_policy_confirmed_or_disputed: ""
  restricted_source_handling_required: false
  permitted_roles_confirmed: []
  access_boundary_note: ""
  evidence_note: ""
  accountable_owner_for_pending: ""
```

Gap addressed:

- restricted sources such as TB and EOC must remain inaccessible to unauthorized roles;
- role readiness must include access boundary preservation, not only owner naming.

### 5. Provenance, version/freshness and no-execution boundary acknowledgement

Purpose: keep role assignment evidence traceable and prevent claims of source approval or real-world execution.

Planned fields:

```yaml
role_assignment_provenance:
  status: ""
  evidence_collected_by: ""
  evidence_collection_date: ""
  evidence_collection_method: ""
  version_or_effective_date_checked: ""
  no_execution_boundary_acknowledged: true
  no_source_approval_boundary_acknowledged: true
  evidence_note: ""
  accountable_owner_for_pending: ""
```

Gap addressed:

- provenance and currentness must be explicit before role assignment can be treated as review-ready;
- an approved plan or filled packet must not be reported as source approval, ingestion, indexing or executed operational action.

## Field-group mapping to baseline gaps

| Baseline gap | Planned field group | Later test expectation |
|---|---|---|
| Role-readiness gap 54.3% | All five role-assignment field groups | Each source can be scored for role readiness without modifying approval/RAG status |
| `owner_person: pending_human_assignment` for 5 / 5 records | Named human or approved office assignment | Pending owner/person ambiguity becomes measurable per source |
| `reviewer: pending_human_reviewer` for 5 / 5 records | Independent reviewer routing by gate | Reviewer route becomes auditable without claiming source review approval |
| Restricted/internal access boundary unresolved for role readiness | Access/classification role check | Restricted handling must remain intact for TB/EOC and any restricted source |
| No authority basis or decision-scope proof | Authority basis and decision scope | Ownership evidence is separated from source approval authority |
| No role-assignment provenance proof | Provenance and no-execution boundary | Later collection can be audited without promoting evidence into Organizational RAG |

## Later BUILD acceptance criteria

The next BUILD stage should update only `docs/governance/M1_B_CONTROLLED_SOURCE_CONFIRMATION_PACKET.md` to include the planned role-assignment section.

Minimum BUILD acceptance criteria:

```text
ROLE_ASSIGNMENT_PACKET_BUILD_COMPLETED = true
ROLE_ASSIGNMENT_EVIDENCE_SECTION_ADDED = true
ROLE_ASSIGNMENT_FIELD_GROUP_COUNT = 5
SOURCE_REGISTER_MODIFICATION_REQUIRED = false
SOURCE_OWNER_EVIDENCE_COLLECTION_REQUIRED = false
SOURCE_APPROVAL_CLAIMED = false
SOURCE_INGESTION_CLAIMED = false
RAG_ACTIVATION_CLAIMED = false
```

## Later TEST scope

The later TEST stage should validate the packet update without collecting real source-owner evidence.

Planned static checks:

1. the packet contains a separate `role_assignment_evidence` section;
2. all five planned field groups exist;
3. each field group includes a `status`, `evidence_note` and `accountable_owner_for_pending` pattern or equivalent accountability field;
4. `decision_scope` defaults to `inventory_confirmation_only`;
5. `approval_boundary_acknowledged`, `no_execution_boundary_acknowledged` and `no_source_approval_boundary_acknowledged` remain true;
6. the source register remains unchanged;
7. every source register record remains `approval_status: not_approved`;
8. every source register record remains `active_rag_index: false`.

## Non-goals and prohibited work in this PLAN stage

This run did not:

- modify the controlled packet template;
- collect source-owner evidence;
- assign real owners or reviewers;
- approve any source;
- ingest, parse, embed, index or retrieve any source;
- generate factual answers from source records;
- promote any external research, personal memory or role memory into Organizational Memory / Governed RAG.

## Boundary assertions

```text
M1_B_PLAN_COMPLETED = true
ROLE_ASSIGNMENT_PACKET_PLAN_DEFINED = true
FIELD_GROUPS_MAPPED_TO_BASELINE_GAPS = true
PACKET_UPDATE_TEST_SCOPE_DEFINED = true
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
```

## Test / CI status

No executable CI success is claimed for this governance planning stage.

Evidence basis:

- README inspection on `main`;
- open issue #54 inspection;
- prior hypothesis run 0035 inspection;
- controlled source confirmation packet inspection;
- source register inspection;
- maturity-gate inspection;
- open pull request lookup;
- workflow-run lookup for the previous run commit.

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
- Research Staging content promotion;
- source-register approval status;
- source-register active-RAG status.

No source was ingested, approved, indexed, retrieved from, answered from or promoted into Organizational RAG.

## Risks and blockers

- This plan does not prove any named owner, reviewer assignment or organizational authority.
- The confirmation gap remains 70% and the role-readiness gap remains 54.3% until accountable humans complete and reviewers check a later packet.
- The later BUILD stage must not add wording that implies source approval, ingestion, indexing, retrieval activation or factual-answer permission.
- Thai PDPA official source content retrieval remained unresolved in prior research and still requires legal review before restricted health-data source approval.

## Stage result

```text
M1_B_PLAN_COMPLETED = true
ROLE_ASSIGNMENT_PACKET_PLAN_DEFINED = true
FIELD_GROUPS_MAPPED_TO_BASELINE_GAPS = true
PACKET_UPDATE_TEST_SCOPE_DEFINED = true
CURRENT_ROLE_READINESS_GAP_RATE = 54.3%
TARGET_ROLE_READINESS_GAP_RATE_AFTER_LATER_COLLECTION_PACKET <= 30%
SOURCE_REGISTER_MODIFIED = false
SOURCE_APPROVAL_CLAIMED = false
SOURCE_INGESTION_CLAIMED = false
RAG_ACTIVATION_CLAIMED = false
```

## Next single stage

**BUILD** — update the controlled source confirmation packet with the planned role-assignment evidence section without collecting source-owner evidence or modifying source-register approval/RAG status.
