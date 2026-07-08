# HosPrime Loop Engineering Run 0151 — M0.2 Local Vault Structure REAL PROBLEM

Date: 2026-07-09

Stage: REAL PROBLEM

Linked issue: #155

## North Star outcome supported

Knowledge continuity, reduced repetitive workload, evidence quality, decision-to-outcome traceability, knowledge reuse, user trust, and zero unauthorized high-impact action.

This REAL PROBLEM stage supports the current controlled release target, Milestone 0 — Personal Twin OS v0.1, by defining why a stable local Markdown/Obsidian-compatible vault structure is required before graph memory, task capture, decision traceability, memory-backed Q&A, deploy claims, or daily-use acceptance can be safely attempted.

## Evidence inspected

- `README.md` on `main`
- issue #155
- open issue search results
- open pull request lookup
- `docs/architecture/TWO_LAYER_MEMORY_ARCHITECTURE.md`
- `docs/architecture/LOOP_ENGINEERING_ARCHITECTURE.md`
- latest relevant engineering run: `engineering_runs/2026-07-09/0150-m0-2-local-vault-structure-next-goal.md`
- attempted lookup: `storage/personal_memory/README.md` returned 404 Not Found
- attempted lookup: `vault/README.md` returned 404 Not Found

## README control observations

```text
NORTH_STAR_PRESENT = true
CURRENT_CONTROLLED_RELEASE_TARGET = Milestone 0 — Personal Twin OS v0.1
M0_STATUS = NOW
M0_2_LOCAL_VAULT_STRUCTURE_STATUS = NEXT
M0_2_ACCEPTANCE_SIGNAL = vault/ structure supports Person, Project, Task, Decision, Meeting, Source and Lesson notes
CORE_RULES_PRESENT = true
MEMORY_BOUNDARIES_PRESENT = true
```

The README makes M0 Personal Twin OS v0.1 the current controlled release target and marks M0.2 Local vault structure as NEXT. It also requires the loop to select bounded work tied to real users, baselines, target metrics, evidence, tests, review gates and correct memory storage.

## Architecture observations

The two-layer memory architecture already defines the intended Personal / Staff Twin Memory storage model as:

```text
storage/personal_memory/<person-id>/vault/
├── people/
├── roles/
├── projects/
├── tasks/
├── decisions/
├── lessons/
├── skills/
├── meetings/
├── sources/
└── daily/
```

It also states that the vault must use YAML properties, Markdown content, internal wiki links, source references, review state, sensitivity and retention metadata. This confirms that the real problem is not lack of architectural intent; it is the absence of a verified released repository structure and minimum note-type contract that can be tested and used safely.

The loop architecture requires no objective-free work, no improvement claim without baseline, no conclusion without evidence, no completion without tests, no release without review, no learning without observation, and no organizational learning unless stored in the correct memory layer.

## Real user

Primary real user for this stage:

```text
Healthcare/public-health executive or knowledge worker using HosPrime as a Personal Twin daily work memory.
```

Supporting users:

```text
Future Staff Twin user who needs Person Memory separated from Role Memory and Organizational Memory.
Technical maintainer who needs a deterministic local vault contract before graph memory, API, UI, tests, or deployment can be built.
```

## Real organizational work problem

```text
Personal Twin OS v0.1 cannot yet support reliable daily-use work memory because the repository does not have a verified released local vault structure for the minimum M0.2 note types: Person, Project, Task, Decision, Meeting, Source and Lesson.
```

In practical organizational work, this means a healthcare/public-health leader or staff member cannot yet depend on HosPrime to capture daily notes, meeting context, decisions, tasks, evidence sources and lessons in a predictable local file structure. Without the structure, later capabilities could create fragmented notes, hidden local-only assumptions, duplicated memory locations, weak backlinks, unclear ownership, weak retention metadata, and unsafe mixing of personal working memory with role or organizational truth.

## User impact

```text
WORK_CAPTURE_IS_FRAGMENTED = true
TASK_DECISION_LESSON_TRACEABILITY_BLOCKED = true
OBSIDIAN_GRAPH_MEMORY_TESTING_BLOCKED = true
MEMORY_BACKED_QA_WITH_EVIDENCE_BOUNDARIES_BLOCKED = true
PERSON_ROLE_ORGANIZATIONAL_MEMORY_SEPARATION_AT_IMPLEMENTATION_LEVEL_BLOCKED = true
LOCAL_DEPLOY_ACCEPTANCE_FOR_DAILY_USE_BLOCKED = true
```

The immediate user harm is not a missing screen. The harm is that real work cannot yet be captured in a stable, inspectable, portable memory substrate that supports later evidence-backed retrieval and learning.

## Baseline

```text
M0_CURRENT_RELEASE_TARGET = Personal Twin OS v0.1
M0_2_STATUS_IN_README = NEXT
LOCAL_VAULT_STRUCTURE_RELEASED = false
REPOSITORY_STORAGE_PERSONAL_MEMORY_README_FOUND = false
REPOSITORY_VAULT_README_FOUND = false
PERSON_PROJECT_TASK_DECISION_MEETING_SOURCE_LESSON_NOTE_TYPES_SUPPORTED = false / not released as a repository contract
OBSIDIAN_GRAPH_READY = false
MEMORY_BACKED_QA_READY = false
DEPLOYABLE_PERSONAL_TWIN_READY = false / not claimed
CI_PASS_CLAIMED = false
REAL_USER_ACCEPTANCE_CLAIMED = false
REAL_WORLD_EXECUTION_CLAIMED = false
```

## Target metric for this REAL PROBLEM stage

```text
REAL_PROBLEM_DEFINED = true
REAL_USER_IDENTIFIED = true
USER_WORK_PROBLEM_LINKED_TO_M0_2 = true
BASELINE_STATED = true
TARGET_FOR_NEXT_STAGE_STATED = true
MEMORY_BOUNDARIES_PRESERVED = true
VAULT_IMPLEMENTATION_CLAIMED = false
PERSONAL_CONTENT_MIGRATED = false
ORGANIZATIONAL_MEMORY_PROMOTION_CLAIMED = false
RAG_ACTIVATION_CLAIMED = false
DEPLOYMENT_CLAIMED = false
CI_PASS_CLAIMED = false
REAL_USER_ACCEPTANCE_CLAIMED = false
REAL_WORLD_EXECUTION_CLAIMED = false
```

## Target for next stage

The next BASELINE stage should measure the current repository against the minimum M0.2 vault contract, without building it yet:

```text
EXPECTED_MINIMUM_VAULT_CONTRACT = storage/personal_memory/<person-id>/vault/
REQUIRED_NOTE_TYPES = Person, Project, Task, Decision, Meeting, Source, Lesson
REQUIRED_METADATA_FAMILIES = identity, scope, ownership, review_state, sensitivity, source_refs, timestamps, retention
REQUIRED_LINKING_PATTERN = Obsidian-compatible [[Wiki Links]]
REQUIRED_BOUNDARY = Personal / Staff Twin Memory only, no Organizational Memory promotion
```

## Work completed

Defined and recorded the bounded REAL PROBLEM for issue #155. This run did not create the vault, migrate content, activate indexing, change source registers, approve sources, run RAG, deploy software, claim CI success, claim user acceptance, or claim real-world execution.

## Test / CI status

```text
CODE_CHANGED = false
VAULT_STRUCTURE_CREATED = false
AUTOMATED_TESTS_RUN = false
CI_STATUS_OBSERVED = not_checked_for_new_commit_because_this_is_document_only
CI_PASS_CLAIMED = false
```

No CI pass is claimed. This stage is problem definition only.

## Memory layer affected

```text
Personal / Staff Twin Memory = not affected
Person Memory = not affected
Role Memory = not affected
Research Staging = not affected
Organizational Memory / Governed RAG = not affected
Engineering-run evidence = updated
Issue traceability = updated
```

## Risks or blockers

- The architecture describes the intended vault structure, but the repository does not yet expose a verified released local vault contract.
- If future build work creates folders without metadata templates and note-type boundaries, M0.2 could appear complete while still failing graph memory and evidence-boundary needs.
- M1-B source-owner evidence remains out of scope and must not be mixed with this Personal Twin memory step.
- No deployment, CI success, or real user acceptance has been observed.

## Single next stage

BASELINE — measure the current repository against the minimum M0.2 local vault contract before any build step.
