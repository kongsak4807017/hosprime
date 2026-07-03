# Engineering Run 0016 — M1-B Controlled Source Inventory Real Problem

## Loop stage

REAL PROBLEM

## North Star outcome supported

Evidence-based decisions, knowledge continuity, reduced repetitive workload, decision-to-outcome traceability and zero unauthorized high-impact action.

This run supports the North Star by preventing the Governed Knowledge Oracle from treating placeholder source records as organizational truth before there is accountable source ownership, controlled location evidence, version/checksum evidence, classification and a human review path.

## Controlled release target

Milestone 1 — Governed Knowledge Oracle MVP.

## Evidence inspected at start of run

- `README.md` on `main`: North Star, loop sequence, current release target, Core Rules and Memory Boundaries.
- Open issue #34: `M1-B Real Problem: Confirm controlled source inventory before ingestion planning`.
- Parent issue #10: `M1/M4: Build Organizational Memory Backoffice Pipeline`.
- Parent epic #8: `Epic: Loop Engineering and Two-Layer Memory Runtime`.
- Recent engineering run `engineering_runs/2026-07-03/0015-m1-source-readiness-next-goal.md`.
- Open backlog issues #22-#30 and #11, #3-#6, #8-#10 were noted but not selected because #34 is the ordered next stage.
- Recent PR search showed no newer open PR that should supersede #34.

No external research was required for this stage because the question is an internal governance and source-control problem, not a material external fact claim.

## Real organizational problem

The real blocker to M1-B is not the absence of an ingestion parser, embedding workflow, screen, agent or document volume.

The real blocker is:

```text
HosPrime cannot safely begin controlled ingestion planning while the five M1 source-register records remain placeholders without accountable source inventory evidence.
```

A candidate source must not move toward parsing, embedding, indexing, factual answering or Organizational RAG promotion until the organization can show, at minimum:

```text
SOURCE_OWNER_CONFIRMED
CONTROLLED_FILE_OR_SYSTEM_LOCATION_CONFIRMED
VERSION_OR_DATE_CONFIRMED
CHECKSUM_OR_CHECKSUM_PENDING_EVIDENCE_RECORDED
CLASSIFICATION_CONFIRMED
ACCESS_POLICY_SCOPE_CONFIRMED
HUMAN_REVIEW_PATH_CONFIRMED
SOURCE_STATUS_REMAINS_NON_APPROVED_UNTIL REVIEWED
```

## Real user and work decision framed for the next stage

Real users affected:

- Executive Sponsor
- Data Governance Lead
- Knowledge Reviewer
- Program/source owners
- Future Knowledge Oracle implementer

Work decision they must make:

```text
Which candidate organizational sources are safe enough to enter a controlled inventory workflow for later review, without yet approving, ingesting, indexing or using them for answers?
```

This decision supports the Knowledge Oracle only if it preserves evidence boundaries and avoids unauthorized high-impact factual answers.

## Baseline at start of REAL PROBLEM stage

```text
SOURCE_REGISTER_EXISTS = true
SEED_RECORDS_PRESENT = 5
PRIORITY_KNOWLEDGE_PACKS_REPRESENTED = 5 / 5
MANDATORY_FIELD_COMPLETENESS = 125 / 125 = 100%
APPROVED_PLACEHOLDER_SOURCES = 0 / 5
ACTIVE_RAG_INDEXED_RECORDS = 0 / 5
SOURCE_OWNER_CONFIRMATION_MISSING = true
CONTROLLED_FILE_LOCATION_MISSING = true
CHECKSUM_EVIDENCE_MISSING = true
HUMAN_REVIEW_RECORD_MISSING = true
ACTIVE_RAG_INDEXING_ALLOWED = false
```

## Target metric for this stage

```text
M1_B_REAL_PROBLEM_DEFINED = true
REAL_SOURCE_INVENTORY_PROBLEM_ACCEPTED = true
INGESTION_PLANNING_ALLOWED = false
SOURCE_APPROVAL_CLAIMED = false
RAG_ACTIVATION_CLAIMED = false
NEXT_STAGE = REAL_USER
```

## Stage decision

The M1-B real problem is accepted as a controlled source inventory problem.

The next ordered stage is **REAL USER**, not research, plan, build or ingestion.

The next run should identify the specific accountable user roles, their decision rights and the exact minimum inventory confirmation workflow required before any ingestion planning may begin.

## Work completed

- Defined the controlled source inventory problem blocking M1-B.
- Confirmed that the issue supports a real organizational work problem: safe identification of candidate organizational evidence before ingestion.
- Preserved the boundary that placeholders are not approved evidence.
- Prevented premature jump to parsing, embedding, indexing, retrieval or factual answering.
- Prepared the next stage as REAL USER.

## GitHub update required

```text
CURRENT_STAGE_ISSUE = #34
PARENT_ISSUE = #10
PARENT_EPIC = #8
NEXT_STAGE = REAL_USER
NEXT_RECOMMENDED_ISSUE_TITLE = M1-B Real User: Define accountable source inventory decision roles
```

## Test / CI status

```text
DOC_AND_ISSUE_ONLY_CHANGE = true
PYTEST_REQUIRED_FOR_THIS_STAGE = false
CI_PASS_CLAIMED_FOR_THIS_STAGE = false
PR_REQUIRED_FOR_THIS_STAGE = false
PRIOR_M1_SOURCE_REGISTER_CI_GATE = passed in earlier TEST stage
```

This run does not claim new executable test success because the bounded work was a governance problem-definition stage.

## Memory layer affected

```text
Personal / Staff Twin Memory = not modified
Person Memory = not modified
Role Memory = not modified
Research Staging = not modified
Organizational Memory / Governed RAG = not modified; no source promoted
Repository engineering evidence = updated
Repository issue control path = updated
```

## Safety boundary

No source was ingested, parsed, embedded, approved, indexed, retrieved from, answered from or promoted into Organizational RAG.

No external findings were promoted into organizational truth.

No real-world execution was claimed.

## Risks and blockers

```text
SOURCE_OWNER_CONFIRMATION_MISSING = true
CONTROLLED_FILE_LOCATION_MISSING = true
CHECKSUM_EVIDENCE_MISSING = true
CLASSIFICATION_CONFIRMATION_MISSING = true
ACCESS_POLICY_CONFIRMATION_MISSING = true
HUMAN_REVIEW_RECORD_MISSING = true
RETRIEVAL_EVALUATION_MISSING = true
ACTIVE_RAG_INDEXING_ALLOWED = false
```

## Completion criteria

```text
M1_B_REAL_PROBLEM_DEFINED = true
REAL_SOURCE_INVENTORY_PROBLEM_ACCEPTED = true
ISSUE_34_CAN_CLOSE_AS_COMPLETED = true
INGESTION_PLANNING_ALLOWED = false
SOURCE_APPROVAL_CLAIMED = false
RAG_ACTIVATION_CLAIMED = false
```

## Next single stage

REAL USER — define accountable source inventory decision roles and authority boundaries before any baseline, research, plan, build or ingestion work begins.
