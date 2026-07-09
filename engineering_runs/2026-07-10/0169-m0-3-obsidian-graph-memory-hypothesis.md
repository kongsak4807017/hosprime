# HosPrime Loop Engineering Run 0169 — M0.3 Obsidian-Compatible Graph Memory HYPOTHESIS

Date: 2026-07-10

Stage: HYPOTHESIS

Linked issue: #156

## North Star outcome supported

Knowledge continuity, evidence quality, user trust, decision-to-outcome traceability, knowledge reuse, reduced repetitive search, and zero unauthorized high-impact action.

This HYPOTHESIS stage supports the North Star by converting the reviewed RESEARCH-STAGING candidate into one bounded, testable assumption for Personal Twin OS v0.1 graph navigation. It does not build templates, migrate personal content, run Obsidian, activate RAG, or promote Organizational Memory.

## Repository state inspected on main

- `README.md` states the North Star: trusted data, knowledge, organizational memory and governed AI must help healthcare and public-health organizations complete real work faster with evidence, accountability and continuous learning.
- `README.md` marks Milestone 0 — Personal Twin OS v0.1 as the current controlled release target.
- `README.md` marks M0.2 Local vault structure as DONE and M0.3 Obsidian-compatible graph memory as NEXT.
- `README.md` requires ordered loop execution and separation of Personal / Staff Twin Memory, Person Memory, Role Memory, Organizational Memory / Governed RAG, and Research Staging.
- Open issue #156 tracks M0.3 and has completed REAL PROBLEM, REAL USER, BASELINE and RESEARCH stages.
- No open pull request was found for this repository during this run.
- Combined commit statuses for prior RESEARCH commit `1fc25dcfe18630ef5484af383612ea8006c4bdaa` returned no statuses.
- Workflow runs for prior RESEARCH commit `1fc25dcfe18630ef5484af383612ea8006c4bdaa` returned an empty list.

## Real user and problem carried forward

```text
USER_ROLE = healthcare / public-health manager using Personal Twin OS locally
WORK_SCENARIO = meeting -> decision -> task/source -> lesson navigation
USER_ENVIRONMENT = local Markdown / Obsidian-compatible vault
AUTHORITY_BOUNDARY = personal workspace user, not organizational approver by default
```

The user problem is that a local vault folder contract exists, but there is still no released, testable graph-navigation convention for following real work continuity from meeting context to decision, task/source reference and lesson.

## Baseline

```text
CONTROLLED_RELEASE_TARGET = Milestone 0 — Personal Twin OS v0.1
README_M0_2_STATUS = DONE
README_M0_3_STATUS = NEXT
VAULT_CONTRACT_EXISTS = true
OBSIDIAN_GRAPH_NAVIGATION_CONVENTION_RELEASED = false
OBSIDIAN_GRAPH_NAVIGATION_CONVENTION_TESTED = false
REAL_PERSONAL_CONTENT_USED = false
RAG_ACTIVE = false
ORGANIZATIONAL_MEMORY_PROMOTION_CLAIMED = false
```

## Research evidence carried forward, still staged only

Prior RESEARCH identified an official Obsidian-compatible direction but kept it in Research Staging only:

```text
PRIMARY_LINK_STYLE = Obsidian Wikilinks
MINIMUM_REQUIRED_CHAIN = meeting -> decision -> task -> lesson
SOURCE_REFERENCE_LINK = decision -> source and/or task -> source
BACKLINK_MECHANISM = created naturally by reciprocal or inbound Wikilinks visible in note bodies
OBSIDIAN_BLOCK_LINKS_REQUIRED = false
ORGANIZATIONAL_AUTHORITY_CREATED = false
```

Research Staging remains staged only. It is not Organizational Memory, not RAG, not source-owner approval, and not a claim that the convention has been reviewed, built or accepted by a user.

## Hypothesis

```text
HYPOTHESIS_ID = M0.3-H1
HYPOTHESIS = If a non-sensitive fixture note chain uses visible body Wikilinks connecting one meeting note, one decision note, one task note, one source-reference note and one lesson note, with boundary text near source-reference links, then a healthcare / public-health manager can inspect work continuity in a local Obsidian-compatible vault without mistaking graph links for evidence authority, source approval, RAG activation, Organizational Memory, user acceptance, or real-world execution.
```

## Why this is the smallest safe hypothesis

```text
ONE_USER_SCENARIO_ONLY = true
ONE_NOTE_CHAIN_ONLY = true
VISIBLE_BODY_LINKS_ONLY = true
NO_BLOCK_REFERENCE_DEPENDENCY = true
NO_RUNTIME_OBSIDIAN_DEPENDENCY_FOR_INITIAL_ACCEPTANCE = true
NO_REAL_PERSONAL_OR_PATIENT_CONTENT = true
BOUNDARY_TEXT_REQUIRED_NEAR_SOURCE_REFERENCE = true
```

This hypothesis is intentionally smaller than a full graph-memory system. It tests whether a minimal human-inspectable linking convention is worth planning and building before schema, vector memory, API, UI or Organizational Memory work begins.

## Target metric for later PLAN / BUILD / TEST stages

The later fixture test should be measurable without claiming real user acceptance:

```text
ONE_MEETING_NOTE_LINKS_TO_ONE_DECISION = true
ONE_DECISION_NOTE_LINKS_TO_ONE_SOURCE_REFERENCE = true
ONE_DECISION_NOTE_LINKS_TO_ONE_TASK = true
ONE_TASK_NOTE_LINKS_TO_ONE_LESSON = true
ONE_TASK_OR_LESSON_LINKS_BACK_TO_DECISION = true
BOUNDARY_TEXT_PRESENT_NEAR_SOURCE_REFERENCE = true
GRAPH_LINKS_ARE_NAVIGATION_NOT_PROOF_TEXT_PRESENT = true
REAL_PERSONAL_CONTENT_USED = false
PATIENT_OR_SENSITIVE_CONTENT_USED = false
RAG_ACTIVATION_CLAIMED = false
ORGANIZATIONAL_MEMORY_PROMOTION_CLAIMED = false
REAL_WORLD_EXECUTION_CLAIMED = false
```

## Acceptance for this HYPOTHESIS stage

```text
ONE_TESTABLE_HYPOTHESIS_DEFINED = true
REAL_USER_CARRIED_FORWARD = true
REAL_PROBLEM_CARRIED_FORWARD = true
BASELINE_CARRIED_FORWARD = true
TARGET_METRIC_DRAFTED = true
RESEARCH_STAGING_NOT_PROMOTED = true
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
NEXT_STAGE = PLAN
```

## Test / CI status

```text
AUTOMATED_TESTS_RUN_IN_THIS_STAGE = false
RUNTIME_DEPLOY_TEST_RUN = false
COMBINED_STATUSES_FOR_PRIOR_RESEARCH_COMMIT = []
WORKFLOW_RUNS_FOR_PRIOR_RESEARCH_COMMIT = []
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
Issue traceability = updated through #156
```

This run does not promote anything into Organizational Memory or Governed RAG.

## Risks or blockers

- Wikilinks are Obsidian-native but not universally portable as plain Markdown links; the PLAN stage must explicitly accept or reject Obsidian-first compatibility for M0.3.
- Graph links may still be misinterpreted as evidence authority unless source-reference boundaries remain visible and testable.
- The scenario is still a product assumption until later observation with a real user; no real user acceptance is claimed.
- No repository CI evidence exists for this stage or the immediately prior RESEARCH commit.

## Work completed

Defined one bounded M0.3 hypothesis for a future non-sensitive graph-navigation fixture. No template, sample note, code, runtime behavior, RAG, Organizational Memory promotion, deployment proof, CI success, user acceptance or real-world execution was created or claimed.

## Single next stage

PLAN — define the smallest safe plan for creating a non-sensitive fixture note chain and a bounded validation check for the hypothesis.
