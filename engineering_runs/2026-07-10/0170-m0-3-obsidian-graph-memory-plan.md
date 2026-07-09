# HosPrime Loop Engineering Run 0170 — M0.3 Obsidian-Compatible Graph Memory PLAN

Date: 2026-07-10

Stage: PLAN

Linked issue: #156

## North Star outcome supported

Knowledge continuity, evidence quality, user trust, decision-to-outcome traceability, knowledge reuse, reduced repetitive search, and zero unauthorized high-impact action.

This PLAN stage supports the North Star by defining the smallest safe build plan for a non-sensitive Obsidian-compatible graph-navigation fixture. It does not build the fixture, create templates, migrate real personal content, run Obsidian, activate RAG, promote Organizational Memory, claim user acceptance, or claim real-world execution.

## Repository state inspected on main

- `README.md` states the North Star: trusted data, knowledge, organizational memory and governed AI must help healthcare and public-health organizations complete real work faster with evidence, accountability and continuous learning.
- `README.md` marks Milestone 0 — Personal Twin OS v0.1 as the current controlled release target.
- `README.md` marks M0.2 Local vault structure as DONE and M0.3 Obsidian-compatible graph memory as NEXT.
- `README.md` requires Personal / Staff Twin Memory, Person Memory, Role Memory, Organizational Memory / Governed RAG, and Research Staging to remain separated.
- Open issue #156 tracks M0.3 and previous comments show ordered completion through HYPOTHESIS.
- No open pull request was found for this repository during this run.
- Workflow runs for prior HYPOTHESIS commit `35c6bd5870659a31cc52905c10819def692b522c` returned an empty list.

## Real user and problem carried forward

```text
USER_ROLE = healthcare / public-health manager using Personal Twin OS locally
WORK_SCENARIO = meeting -> decision -> task/source -> lesson navigation
USER_ENVIRONMENT = local Markdown / Obsidian-compatible vault
AUTHORITY_BOUNDARY = personal workspace user, not organizational approver by default
```

The user problem is that the vault folder contract exists, but there is still no built, released or tested convention for navigating a daily work chain from meeting context to decision, task/source reference and lesson.

## Baseline

```text
CONTROLLED_RELEASE_TARGET = Milestone 0 — Personal Twin OS v0.1
README_M0_2_STATUS = DONE
README_M0_3_STATUS = NEXT
VAULT_CONTRACT_EXISTS = true
OBSIDIAN_GRAPH_NAVIGATION_CONVENTION_RELEASED = false
OBSIDIAN_GRAPH_NAVIGATION_CONVENTION_TESTED = false
REAL_PERSONAL_CONTENT_USED = false
PATIENT_OR_SENSITIVE_CONTENT_USED = false
RAG_ACTIVE = false
ORGANIZATIONAL_MEMORY_PROMOTION_CLAIMED = false
```

## Hypothesis carried forward

```text
HYPOTHESIS_ID = M0.3-H1
HYPOTHESIS = If a non-sensitive fixture note chain uses visible body Wikilinks connecting one meeting note, one decision note, one task note, one source-reference note and one lesson note, with boundary text near source-reference links, then a healthcare / public-health manager can inspect work continuity in a local Obsidian-compatible vault without mistaking graph links for evidence authority, source approval, RAG activation, Organizational Memory, user acceptance, or real-world execution.
```

Research Staging remains staged only. This plan does not promote Obsidian findings into Organizational Memory or Governed RAG.

## Selected bounded next step for BUILD

Create exactly one non-sensitive fixture note chain under the existing example vault, plus one lightweight repository-local validation script or checklist artifact that can be tested in the next stage.

Planned fixture scope:

```text
FIXTURE_ROOT = storage/personal_memory/example-person/vault/
MEETING_NOTE = meetings/m0-3-demo-meeting.md
DECISION_NOTE = decisions/m0-3-demo-decision.md
TASK_NOTE = tasks/m0-3-demo-task.md
SOURCE_NOTE = sources/m0-3-demo-source-reference.md
LESSON_NOTE = lessons/m0-3-demo-lesson.md
```

Required link chain for BUILD:

```text
MEETING_NOTE links to DECISION_NOTE
DECISION_NOTE links to MEETING_NOTE
DECISION_NOTE links to TASK_NOTE
DECISION_NOTE links to SOURCE_NOTE
TASK_NOTE links to DECISION_NOTE
TASK_NOTE links to LESSON_NOTE
LESSON_NOTE links to TASK_NOTE
LESSON_NOTE links back to DECISION_NOTE
SOURCE_NOTE contains boundary text that the source reference is navigation/staging only, not authority or approval
```

Required content boundaries for BUILD:

```text
USE_ONLY_NON_SENSITIVE_SYNTHETIC_CONTENT = true
REAL_PERSONAL_CONTENT_USED = false
PATIENT_OR_SENSITIVE_CONTENT_USED = false
REAL_ORGANIZATIONAL_SOURCE_COPIED = false
SOURCE_APPROVAL_CLAIMED = false
RAG_ACTIVATION_CLAIMED = false
ORGANIZATIONAL_MEMORY_PROMOTION_CLAIMED = false
USER_ACCEPTANCE_CLAIMED = false
REAL_WORLD_EXECUTION_CLAIMED = false
```

## Validation plan for later TEST stage

The later TEST stage should verify repository text only, without claiming Obsidian runtime execution unless an authorized runtime test is actually performed.

Minimum validation checks:

```text
EXACTLY_FIVE_FIXTURE_NOTES_EXIST = true
VISIBLE_WIKILINKS_PRESENT = true
MEETING_TO_DECISION_LINK_PRESENT = true
DECISION_TO_MEETING_LINK_PRESENT = true
DECISION_TO_TASK_LINK_PRESENT = true
DECISION_TO_SOURCE_LINK_PRESENT = true
TASK_TO_DECISION_LINK_PRESENT = true
TASK_TO_LESSON_LINK_PRESENT = true
LESSON_TO_TASK_LINK_PRESENT = true
LESSON_TO_DECISION_LINK_PRESENT = true
SOURCE_BOUNDARY_TEXT_PRESENT = true
GRAPH_LINKS_ARE_NAVIGATION_NOT_PROOF_TEXT_PRESENT = true
REAL_PERSONAL_CONTENT_USED = false
PATIENT_OR_SENSITIVE_CONTENT_USED = false
RAG_ACTIVATION_CLAIMED = false
ORGANIZATIONAL_MEMORY_PROMOTION_CLAIMED = false
```

## Acceptance for this PLAN stage

```text
ONE_BUILD_PLAN_DEFINED = true
REAL_USER_CARRIED_FORWARD = true
REAL_PROBLEM_CARRIED_FORWARD = true
BASELINE_CARRIED_FORWARD = true
HYPOTHESIS_CARRIED_FORWARD = true
BUILD_SCOPE_LIMITED_TO_ONE_FIXTURE_CHAIN = true
TEST_SCOPE_DRAFTED = true
RESEARCH_STAGING_NOT_PROMOTED = true
FIXTURE_NOTES_CREATED = false
NOTE_TEMPLATES_CREATED = false
GRAPH_RUNTIME_CODE_CREATED = false
OBSIDIAN_GRAPH_TEST_CLAIMED = false
SOURCE_APPROVAL_CLAIMED = false
RAG_ACTIVATION_CLAIMED = false
ORGANIZATIONAL_MEMORY_PROMOTION_CLAIMED = false
CI_PASS_CLAIMED = false
REAL_USER_ACCEPTANCE_CLAIMED = false
REAL_WORLD_EXECUTION_CLAIMED = false
NEXT_STAGE = BUILD
```

## Test / CI status

```text
AUTOMATED_TESTS_RUN_IN_THIS_STAGE = false
RUNTIME_DEPLOY_TEST_RUN = false
WORKFLOW_RUNS_FOR_PRIOR_HYPOTHESIS_COMMIT = []
CI_PASS_CLAIMED = false
```

No CI pass is claimed.

## Memory layer affected

```text
Personal / Staff Twin Memory = not changed
Person Memory = not changed
Role Memory = not changed
Research Staging = referenced only; not promoted
Organizational Memory / Governed RAG = not changed
Engineering-run evidence = updated
Issue traceability = to be updated through #156
```

This run does not promote anything into Organizational Memory or Governed RAG.

## Risks or blockers

- Wikilinks are Obsidian-compatible but not universal Markdown; the fixture must remain explicitly Obsidian-compatible, not general Markdown portability proof.
- A fixture chain proves repository convention presence only; it does not prove runtime Obsidian graph rendering unless later observed in Obsidian.
- Source-reference notes may be mistaken for authority unless visible boundary text is included and tested.
- No repository CI evidence exists for this stage or the immediately prior HYPOTHESIS commit.

## Work completed

Defined the smallest safe BUILD plan for one non-sensitive fixture note chain and a bounded validation path. No fixture notes, templates, runtime graph code, real personal-memory migration, RAG, Organizational Memory promotion, deployment proof, CI success, user acceptance or real-world execution were created or claimed.

## Single next stage

BUILD — create the one non-sensitive fixture note chain and the minimal validation artifact/check, preserving all authority and memory-layer boundaries.
