# HosPrime Loop Engineering Run 0166 — M0.3 Obsidian-Compatible Graph Memory REAL USER

Date: 2026-07-09

Stage: REAL USER

Linked issue: #156

## North Star outcome supported

Knowledge continuity, reduced repetitive workload, evidence quality, user trust, decision-to-outcome traceability, knowledge reuse, and zero unauthorized high-impact action.

This stage supports the North Star by narrowing M0.3 from a general graph-memory idea into one concrete daily-work user scenario. It does not design, build, test, approve, ingest, index, or promote memory.

## Repository state inspected on main

- `README.md` states the North Star: trusted data, knowledge, organizational memory and governed AI must help healthcare and public-health organizations complete real work faster with evidence, accountability and continuous learning.
- `README.md` marks the current controlled release target as Milestone 0 — Personal Twin OS v0.1.
- `README.md` marks M0.2 Local vault structure as DONE and M0.3 Obsidian-compatible graph memory as NEXT.
- `README.md` requires the ordered loop and memory-layer separation.
- Issue #156 is open and the previous issue comment records REAL PROBLEM completed with REAL USER as the next stage.
- `storage/personal_memory/README.md` confirms the local personal-memory storage contract and boundary: personal memory is not Organizational Memory by default.
- `storage/personal_memory/example-person/vault/README.md` confirms the required note folders: people, projects, tasks, decisions, meetings, sources and lessons.
- Combined commit status for prior M0.3 REAL PROBLEM commit `5c7bdcb8ba04f89aea251ca76013075cbc501fd4` returned no statuses.
- Workflow runs for prior M0.3 REAL PROBLEM commit `5c7bdcb8ba04f89aea251ca76013075cbc501fd4` returned an empty list.

## Real user selected

Primary M0.3 user for this loop:

```text
USER_ROLE = healthcare / public-health manager using Personal Twin OS locally
USER_CONTEXT = daily organizational work continuity across meetings, decisions, tasks, sources and lessons
USER_ENVIRONMENT = local Markdown / Obsidian-compatible vault under storage/personal_memory/<person-id>/vault/
USER_AUTHORITY_LEVEL = personal workspace user, not organizational approver by default
```

This user may be a hospital, provincial public-health, program, quality, digital-health, planning, or operations manager who must keep continuity across many small work items without losing context.

The user is selected because M0.3 is still inside Personal Twin OS v0.1, not institutional Knowledge Oracle, Staff Twin, Role Twin, Hospital Twin, Province Twin, active RAG, or autonomous workflow execution.

## Real work scenario

The bounded scenario for M0.3 graph navigation is:

```text
After a meeting, the user creates or reviews a personal meeting note.
The meeting note points to one decision note.
The decision note points to one task note and one source-reference note.
The completed task later points to one lesson note.
The user needs to navigate the chain without searching manually or treating links as approved evidence.
```

Minimum user questions to support later stages:

```text
Which decision came from this meeting?
Which task came from this decision?
Which source reference is attached to this decision note?
Which lesson came from this completed task?
Which project connects these notes?
```

## User pain to solve

Current pain after M0.2:

```text
The folder contract exists, but the user still has no safe convention for linking notes across a daily work chain.
Manual search remains necessary.
The user can lose decision-to-task and task-to-lesson continuity.
The user can mistake a graph edge for proof, source approval, review, execution receipt, or organizational truth if future graph rules are not explicit.
```

## Baseline

```text
CONTROLLED_RELEASE_TARGET = Milestone 0 — Personal Twin OS v0.1
README_M0_STATUS = NOW
README_M0_2_STATUS = DONE
README_M0_3_STATUS = NEXT
REAL_PROBLEM_DEFINED = true
REAL_USER_SCENARIO_DEFINED = false before this run
VAULT_CONTRACT_EXISTS = true
REQUIRED_NOTE_FOLDERS_DOCUMENTED = true
OBSIDIAN_GRAPH_NAVIGATION_CONVENTION_RELEASED = false
OBSIDIAN_GRAPH_NAVIGATION_TESTED = false
GRAPH_LINKS_ARE_NAVIGATION_NOT_PROOF = true
REAL_PERSONAL_MEMORY_MIGRATED = false
RAG_ACTIVE = false
ORGANIZATIONAL_MEMORY_PROMOTION_CLAIMED = false
REAL_USER_ACCEPTANCE_CLAIMED = false
REAL_WORLD_EXECUTION_CLAIMED = false
CI_PASS_CLAIMED = false
```

## Target metric for this REAL USER stage

```text
REAL_USER_ROLE_DEFINED = true
REAL_WORK_SCENARIO_DEFINED = true
MINIMUM_NAVIGATION_QUESTIONS_DEFINED = true
USER_AUTHORITY_BOUNDARY_DEFINED = true
BASELINE_STATED = true
TARGET_METRIC_STATED = true
NOTE_TEMPLATES_CREATED = false
REAL_PERSONAL_MEMORY_MIGRATED = false
GRAPH_RUNTIME_CODE_CREATED = false
OBSIDIAN_GRAPH_TEST_CLAIMED = false
SOURCE_APPROVAL_CLAIMED = false
RAG_ACTIVATION_CLAIMED = false
ORGANIZATIONAL_MEMORY_PROMOTION_CLAIMED = false
CI_PASS_CLAIMED = false
REAL_USER_ACCEPTANCE_CLAIMED = false
REAL_WORLD_EXECUTION_CLAIMED = false
NEXT_STAGE = BASELINE
```

## Boundaries retained

This REAL USER stage does not authorize building. It defines who M0.3 is for and what daily work chain the next baseline must measure.

Forbidden in this stage:

- creating note templates;
- creating sample notes;
- migrating real personal notes;
- creating graph runtime code;
- testing Obsidian graph rendering;
- approving sources;
- ingesting, parsing, embedding, indexing, or activating RAG;
- promoting any note into Role Memory, Organizational Memory, or Governed RAG;
- claiming CI success;
- claiming real-user acceptance;
- claiming real-world execution.

## Evidence and limitations

Internal evidence only was material for this stage. No external research was required because the run selected a bounded repository/product user scenario, not a standards or technology decision.

Limitations:

- No real user session was observed.
- No user acceptance was collected.
- No fixture, template, runtime behavior, Obsidian graph rendering, or automated test was created.
- The scenario is a controlled product assumption that must be measured in the next BASELINE stage before research, hypothesis, plan, build, or test.

## Test / CI status

```text
AUTOMATED_TESTS_RUN_IN_THIS_STAGE = false
RUNTIME_DEPLOY_TEST_RUN = false
COMBINED_STATUS_FOR_PRIOR_REAL_PROBLEM_COMMIT = []
WORKFLOW_RUNS_FOR_PRIOR_REAL_PROBLEM_COMMIT = []
CI_PASS_CLAIMED = false
```

No CI pass is claimed.

## Memory layer affected

```text
Personal / Staff Twin Memory = not changed
Person Memory = not changed
Role Memory = not changed
Research Staging = not changed
Organizational Memory / Governed RAG = not changed
Engineering-run evidence = updated
Issue traceability = updated through #156
```

This run does not promote anything into Organizational Memory or Governed RAG.

## Risks or blockers

- The selected user scenario is plausible but not yet validated by an observed user session.
- Future graph work must prevent links from being treated as source approval, review approval, execution proof, clinical evidence, or organizational truth.
- The next BASELINE stage must measure the repository gap precisely before designing a convention.

## Work completed

Recorded the M0.3 REAL USER stage as an engineering-run evidence package.

No templates, sample notes, code, runtime behavior, RAG, Organizational Memory promotion, deployment proof, CI success, user acceptance, or real-world execution were created or claimed.

## Single next stage

BASELINE — measure the current repository gap for the selected M0.3 user scenario: required note-link chain, front matter fields, boundary language, and testable acceptance conditions for Obsidian-compatible navigation.
