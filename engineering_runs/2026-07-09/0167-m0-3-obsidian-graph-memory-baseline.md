# HosPrime Loop Engineering Run 0167 — M0.3 Obsidian-Compatible Graph Memory BASELINE

Date: 2026-07-09

Stage: BASELINE

Linked issue: #156

## North Star outcome supported

Knowledge continuity, evidence quality, user trust, decision-to-outcome traceability, knowledge reuse, reduced repetitive search, and zero unauthorized high-impact action.

This BASELINE stage supports the North Star by measuring the current repository gap for the selected Personal Twin OS user scenario before any research, hypothesis, planning, building, testing, or release work begins.

## Repository state inspected on main

- `README.md` states the North Star: trusted data, knowledge, organizational memory and governed AI must help healthcare and public-health organizations complete real work faster with evidence, accountability and continuous learning.
- `README.md` marks Milestone 0 — Personal Twin OS v0.1 as the current controlled release target.
- `README.md` marks M0.2 Local vault structure as DONE and M0.3 Obsidian-compatible graph memory as NEXT.
- `README.md` requires the ordered loop and memory-layer separation.
- Issue #156 is open and records REAL PROBLEM and REAL USER as completed for M0.3.
- The latest M0.3 REAL USER evidence package is `engineering_runs/2026-07-09/0166-m0-3-obsidian-graph-memory-real-user.md`.
- `storage/personal_memory/README.md` confirms local personal-memory storage only and states that Personal Memory is not Organizational Memory by default.
- `storage/personal_memory/example-person/vault/README.md` confirms the required vault folders and future minimum front-matter contract.
- No open pull requests were found for the repository in this run.
- Workflow runs for prior M0.3 REAL USER commit `2a33b7401e1e7880bee72ddc4b4e6859408268c5` returned an empty list.

## Real user and problem carried forward

```text
USER_ROLE = healthcare / public-health manager using Personal Twin OS locally
WORK_SCENARIO = meeting -> decision -> task/source -> lesson navigation
USER_ENVIRONMENT = local Markdown / Obsidian-compatible vault
AUTHORITY_BOUNDARY = personal workspace user, not organizational approver by default
```

The measured problem is not that the folders are missing. The folder contract exists. The measured problem is that no released, testable, Obsidian-compatible graph navigation convention yet tells the user how to connect meeting, decision, task, source and lesson notes safely.

## Baseline measurement

```text
CONTROLLED_RELEASE_TARGET = Milestone 0 — Personal Twin OS v0.1
README_M0_STATUS = NOW
README_M0_2_STATUS = DONE
README_M0_3_STATUS = NEXT
REAL_PROBLEM_DEFINED = true
REAL_USER_SCENARIO_DEFINED = true
VAULT_CONTRACT_EXISTS = true
REQUIRED_NOTE_FOLDERS_DOCUMENTED = true
MINIMUM_FRONT_MATTER_DOCUMENTED_AS_FUTURE_CONTRACT = true
OBSIDIAN_GRAPH_NAVIGATION_CONVENTION_RELEASED = false
OBSIDIAN_GRAPH_NAVIGATION_TESTED = false
MEETING_DECISION_TASK_SOURCE_LESSON_CHAIN_DEFINED = false
BACKLINK_PATTERN_DEFINED = false
GRAPH_ACCEPTANCE_FIXTURE_EXISTS = false
GRAPH_ACCEPTANCE_TEST_EXISTS = false
GRAPH_LINKS_ARE_NAVIGATION_NOT_PROOF = true
REAL_PERSONAL_MEMORY_MIGRATED = false
RAG_ACTIVE = false
ORGANIZATIONAL_MEMORY_PROMOTION_CLAIMED = false
REAL_USER_ACCEPTANCE_CLAIMED = false
REAL_WORLD_EXECUTION_CLAIMED = false
CI_PASS_CLAIMED = false
```

## Baseline gap

The current repository has:

1. a Personal Memory storage boundary;
2. a vault root contract;
3. required note-type folders;
4. future front-matter fields;
5. explicit graph-link and promotion boundaries.

The current repository does not yet have:

1. a released graph-link naming convention;
2. a minimum note chain from meeting -> decision -> task/source -> lesson;
3. a backlink pattern for navigation;
4. an acceptance fixture that can be inspected without using real personal content;
5. an automated or manual graph-navigation test record;
6. a reviewed promotion path from personal graph notes to any Organizational Memory layer.

## Target metric for the next RESEARCH stage

The next stage should research only the smallest safe convention needed for M0.3. It should not build templates or fixtures yet.

```text
RESEARCH_QUESTION_DEFINED = true
MINIMUM_OBSIDIAN_LINK_PATTERN_IDENTIFIED = true
MINIMUM_NOTE_CHAIN_ACCEPTANCE_CRITERIA_DRAFTED = true
BOUNDARY_LANGUAGE_RETAINED = true
EXTERNAL_FINDINGS_STAGED_ONLY = true
NOTE_TEMPLATES_CREATED = false
SAMPLE_NOTES_CREATED = false
GRAPH_RUNTIME_CODE_CREATED = false
OBSIDIAN_GRAPH_TEST_CLAIMED = false
SOURCE_APPROVAL_CLAIMED = false
RAG_ACTIVATION_CLAIMED = false
ORGANIZATIONAL_MEMORY_PROMOTION_CLAIMED = false
CI_PASS_CLAIMED = false
REAL_USER_ACCEPTANCE_CLAIMED = false
REAL_WORLD_EXECUTION_CLAIMED = false
NEXT_STAGE = RESEARCH
```

## Bounded research question for the next stage

```text
What is the smallest Obsidian-compatible Markdown linking and backlink convention that can connect one meeting note, one decision note, one task note, one source-reference note and one lesson note for local Personal Twin OS navigation, while preserving that graph links are navigation only and not proof, approval, RAG activation, Organizational Memory, or execution evidence?
```

## Evidence and limitations

Internal repository evidence was sufficient for this BASELINE stage. External research was not material because this run only measured the repository gap before deciding the link convention.

Limitations:

- No real user session was observed.
- No user acceptance was collected.
- No note template, sample note, fixture, runtime code, Obsidian graph rendering, or automated test was created.
- No external source was promoted into Research Staging in this run.
- No CI pass is claimed because no workflow run was found for the prior commit.

## Test / CI status

```text
AUTOMATED_TESTS_RUN_IN_THIS_STAGE = false
RUNTIME_DEPLOY_TEST_RUN = false
OPEN_PULL_REQUESTS_FOUND = 0
WORKFLOW_RUNS_FOR_PRIOR_REAL_USER_COMMIT = []
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

- Graph navigation can be misread as evidence authority unless every future convention keeps boundary language close to the links.
- A too-large convention could delay daily-use value; M0.3 should stay limited to one minimal work chain.
- The selected user scenario remains a product assumption until observed with a real user in a later stage.

## Work completed

Recorded the M0.3 BASELINE stage as an engineering-run evidence package.

No templates, sample notes, code, runtime behavior, RAG, Organizational Memory promotion, deployment proof, CI success, user acceptance, or real-world execution were created or claimed.

## Single next stage

RESEARCH — identify the smallest safe Obsidian-compatible link/backlink convention for the selected Personal Twin OS work chain, with findings kept in Research Staging only until reviewed.
