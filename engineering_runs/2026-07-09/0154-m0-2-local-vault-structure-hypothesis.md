# HosPrime Loop Engineering Run 0154 — M0.2 Local Vault Structure HYPOTHESIS

Date: 2026-07-09

Stage: HYPOTHESIS

Linked issue: #155

## North Star outcome supported

Knowledge continuity, reduced repetitive workload, evidence quality, decision-to-outcome traceability, knowledge reuse, user trust, and zero unauthorized high-impact action.

This HYPOTHESIS stage supports Milestone 0 — Personal Twin OS v0.1 by defining one testable assumption for the smallest safe repository-visible local vault contract. It does not build the vault, migrate personal content, activate RAG, promote Organizational Memory, claim deployment, claim CI success, or claim real-user acceptance.

## Real user and real work problem

Real user: an individual healthcare or public-health staff member using Personal Twin OS v0.1 for daily work capture, decision tracking, meeting follow-up, source linking, and lessons learned.

Real work problem: without a stable local Markdown / Obsidian-compatible vault contract, daily notes, tasks, decisions, meetings, sources and lessons cannot be reliably linked, inspected, reviewed, corrected, reused or later promoted through governed memory boundaries.

## Baseline carried forward

From BASELINE run `0152-m0-2-local-vault-structure-baseline.md` and RESEARCH run `0153-m0-2-local-vault-structure-research.md`:

```text
LOCAL_VAULT_STRUCTURE_RELEASED = false
REPOSITORY_STORAGE_PERSONAL_MEMORY_README_FOUND = false
REPOSITORY_VAULT_README_FOUND = false
CODE_SEARCH_FOUND_RELEASED_VAULT_CONTRACT = false
EXPECTED_STORAGE_ROOT_DEFINED_IN_ARCHITECTURE = true
EXPECTED_STORAGE_ROOT_IMPLEMENTED_IN_REPOSITORY = false / not observed
PERSON_PROJECT_TASK_DECISION_MEETING_SOURCE_LESSON_NOTE_TYPES_SUPPORTED = false / not released as repository contract
OBSIDIAN_GRAPH_READY = false
MEMORY_BACKED_QA_READY = false
DEPLOYABLE_PERSONAL_TWIN_READY = false / not claimed
CI_PASS_CLAIMED = false
REAL_USER_ACCEPTANCE_CLAIMED = false
REAL_WORLD_EXECUTION_CLAIMED = false
```

## Evidence inspected

Internal evidence:

- `README.md` on `main`
- open issue #155 and its ordered-loop comments through RESEARCH
- open pull request lookup
- recent commits on `main`
- CI status and workflow lookup for latest observed commit `61f7815548541beb1fd70ededcc1405746c05a34`
- prior engineering run `engineering_runs/2026-07-09/0153-m0-2-local-vault-structure-research.md`

Research staging evidence carried forward from run 0153:

- Obsidian Help — Internal links: `https://obsidian.md/help/links`
- Obsidian Help — Properties: `https://obsidian.md/help/properties`
- Obsidian Help — Graph view: `https://obsidian.md/help/plugins/graph`

Limitations:

- External Obsidian documentation remains product guidance, not HosPrime policy.
- External findings remain Research Staging only.
- This run does not promote any external finding into Organizational Memory or Governed RAG.
- No external source was used to approve source ingestion, RAG activation, access control, or healthcare policy.

## Hypothesis

```text
If M0.2 releases a small repository-visible local vault contract under
storage/personal_memory/example-person/vault/ with only the seven required
note folders, one human-readable README, and a required front-matter contract
for Person, Project, Task, Decision, Meeting, Source and Lesson notes, then
Personal Twin OS v0.1 will have enough structure to support daily-use capture,
Obsidian-compatible navigation, later graph-memory testing, and governed
memory-boundary review without implying source approval, RAG activation,
Organizational Memory promotion, deployability, or real-world completion.
```

## Hypothesis acceptance criteria for the next PLAN stage

The hypothesis should be considered plan-ready only if the next PLAN can specify a build artifact that satisfies all of the following without expanding scope:

```text
CONTRACT_ROOT = storage/personal_memory/
EXAMPLE_PERSON_ROOT = storage/personal_memory/example-person/
VAULT_ROOT = storage/personal_memory/example-person/vault/
REQUIRED_NOTE_FOLDERS = people, projects, tasks, decisions, meetings, sources, lessons
REQUIRED_NOTE_TYPES = person, project, task, decision, meeting, source, lesson
README_EXPLAINS_PERSONAL_MEMORY_BOUNDARY = true
README_EXPLAINS_NOT_ORGANIZATIONAL_TRUTH = true
README_EXPLAINS_REVIEW_REQUIRED_FOR_PROMOTION = true
README_EXPLAINS_RAG_NOT_ACTIVE = true
README_EXPLAINS_GRAPH_LINKS_ARE_NAVIGATION_NOT_PROOF = true
FRONT_MATTER_FIELDS_DEFINED = note_id, title, person_id, note_type, memory_scope, review_state, sensitivity, source_refs, links, created_at, updated_at, retention_until, version
OBSIDIAN_COMPATIBLE_WIKILINKS_ALLOWED = true
OBSIDIAN_PLUGIN_DEPENDENCY_REQUIRED = false
PERSONAL_CONTENT_INCLUDED = false
ORGANIZATIONAL_SOURCE_APPROVAL_INCLUDED = false
RAG_ACTIVATION_INCLUDED = false
DEPLOYABILITY_CLAIM_INCLUDED = false
```

## Expected measurable target

```text
HYPOTHESIS_STAGE_COMPLETED = true
README_READ = true
OPEN_ISSUES_INSPECTED = true
OPEN_PRS_INSPECTED = true
RECENT_ENGINEERING_RUN_INSPECTED = true
CI_STATUS_INSPECTED = true
HYPOTHESIS_IS_SINGLE_AND_TESTABLE = true
HYPOTHESIS_SUPPORTS_M0_2 = true
PLAN_ACCEPTANCE_CRITERIA_DEFINED = true
BOUNDARIES_EXPLICIT = true
BUILD_NOT_PERFORMED = true
VAULT_STRUCTURE_CREATED = false
PERSONAL_CONTENT_MIGRATED = false
ORGANIZATIONAL_MEMORY_PROMOTION_CLAIMED = false
RAG_ACTIVATION_CLAIMED = false
DEPLOYMENT_CLAIMED = false
CI_PASS_CLAIMED = false
REAL_USER_ACCEPTANCE_CLAIMED = false
REAL_WORLD_EXECUTION_CLAIMED = false
```

## Work completed

Completed one bounded HYPOTHESIS stage. The run defined a single testable assumption for the smallest repository-visible M0.2 local vault contract and identified plan-stage acceptance criteria that preserve Personal Memory, Research Staging and Organizational Memory / Governed RAG boundaries.

No vault folders, note templates, schemas, tests, indexes, embeddings, source registers, ingestion routes, UI screens, deploy artifacts, Organizational Memory objects, or RAG activation were created.

## Test / CI status

```text
CODE_CHANGED = false
DOCUMENTATION_EVIDENCE_ADDED = true
VAULT_STRUCTURE_CREATED = false
AUTOMATED_TESTS_RUN = false
LATEST_OBSERVED_COMMIT = 61f7815548541beb1fd70ededcc1405746c05a34
COMBINED_STATUS_CONTEXTS = []
WORKFLOW_RUNS_FOR_LATEST_OBSERVED_COMMIT = []
CI_PASS_CLAIMED = false
```

No CI pass is claimed. The observed combined status lookup returned no statuses, and workflow lookup for the latest observed commit returned no workflow runs.

## Memory layer affected

```text
Personal / Staff Twin Memory = not affected
Person Memory = not affected
Role Memory = not affected
Research Staging = carried forward only as referenced staged findings from run 0153
Organizational Memory / Governed RAG = not affected
Engineering-run evidence = updated
Issue traceability = to be updated
```

## Risks or blockers

- A vault contract may be mistaken for a usable deployed Personal Twin. This run does not claim deployability.
- Graph links may be mistaken for verified truth. The next plan must preserve the rule that graph links are navigational until supported by provenance and review state.
- Source notes may be mistaken for approved organizational sources. The next plan must keep source notes as personal references only unless a separate reviewed promotion record exists.
- Adding example content could accidentally introduce personal or organizational facts. The next plan should prefer empty `.gitkeep` folders and README contract text, not real content.

## Single next stage

PLAN — define the smallest build plan for the repository-visible M0.2 local vault contract, limited to README / folder contract artifacts and explicit non-promotion boundaries before any build step.