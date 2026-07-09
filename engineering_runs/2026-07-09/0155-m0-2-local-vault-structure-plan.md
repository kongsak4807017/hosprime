# HosPrime Loop Engineering Run 0155 — M0.2 Local Vault Structure PLAN

Date: 2026-07-09

Stage: PLAN

Linked issue: #155

## North Star outcome supported

Knowledge continuity, reduced repetitive workload, evidence quality, decision-to-outcome traceability, knowledge reuse, user trust, and zero unauthorized high-impact action.

This PLAN stage supports Milestone 0 — Personal Twin OS v0.1 by defining the smallest safe build plan for a repository-visible local vault contract. It does not build the vault, migrate personal content, activate RAG, promote Organizational Memory, claim deployment, claim CI success, or claim real-user acceptance.

## Real user and real work problem

Real user: an individual healthcare or public-health staff member using Personal Twin OS v0.1 for daily work capture, decision tracking, meeting follow-up, source linking, and lessons learned.

Real work problem: without a stable local Markdown / Obsidian-compatible vault contract, daily notes, tasks, decisions, meetings, sources and lessons cannot be reliably linked, inspected, reviewed, corrected, reused or later promoted through governed memory boundaries.

## Stage selection justification

The latest completed stage for issue #155 is HYPOTHESIS. The ordered loop requires PLAN next before BUILD.

The selected next step is bounded and supports the README current controlled release target:

```text
CONTROLLED_RELEASE_TARGET = Milestone 0 — Personal Twin OS v0.1
README_M0_2_STATUS = NEXT
ORDERED_NEXT_STAGE = PLAN
```

## Baseline carried forward

From the HYPOTHESIS run `0154-m0-2-local-vault-structure-hypothesis.md`:

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
- open issue #155
- open PR lookup
- recent commit lookup
- latest HYPOTHESIS run: `engineering_runs/2026-07-09/0154-m0-2-local-vault-structure-hypothesis.md`
- `docs/architecture/LOOP_ENGINEERING_ARCHITECTURE.md`
- `docs/governance/MATURITY_GATES.md`
- CI combined status and workflow run lookup for commit `19e49a87b39d43ecf22021eff85a8597a1ba9552`

Research staging evidence carried forward only from run 0153:

- Obsidian Help — Internal links: `https://obsidian.md/help/links`
- Obsidian Help — Properties: `https://obsidian.md/help/properties`
- Obsidian Help — Graph view: `https://obsidian.md/help/plugins/graph`

Limitations:

- External Obsidian documentation remains product guidance, not HosPrime policy.
- External findings remain Research Staging only.
- This run does not promote any external finding into Organizational Memory or Governed RAG.
- This run does not approve source ingestion, RAG activation, access control, or healthcare policy.

## Plan objective

Define a minimal repository-visible vault contract that can be built in the next stage without introducing real personal content, organizational evidence, source approval, RAG activation, deployment claims, or memory promotion.

## Planned build artifact

The BUILD stage should create only these repository artifacts:

```text
storage/personal_memory/README.md
storage/personal_memory/example-person/README.md
storage/personal_memory/example-person/vault/README.md
storage/personal_memory/example-person/vault/people/.gitkeep
storage/personal_memory/example-person/vault/projects/.gitkeep
storage/personal_memory/example-person/vault/tasks/.gitkeep
storage/personal_memory/example-person/vault/decisions/.gitkeep
storage/personal_memory/example-person/vault/meetings/.gitkeep
storage/personal_memory/example-person/vault/sources/.gitkeep
storage/personal_memory/example-person/vault/lessons/.gitkeep
```

No real person note, real project note, real meeting note, real organizational source, clinical/patient data, credentials, embeddings, indexes, database migrations, API endpoints, UI screens, or deploy scripts should be created during BUILD.

## Contract to document in README files

The READMEs should define these boundaries:

```text
PERSONAL_MEMORY_SCOPE = local personal workspace only
ORGANIZATIONAL_TRUTH = false unless reviewed promotion exists
RAG_ACTIVE = false
SOURCE_APPROVAL = false
GRAPH_LINKS_ARE_NAVIGATION_NOT_PROOF = true
PROMOTION_REQUIRES_REVIEW_RECORD = true
NO_REAL_PERSONAL_CONTENT_IN_EXAMPLE = true
NO_PATIENT_OR_SENSITIVE_CONTENT_IN_EXAMPLE = true
```

The vault README should define a required front-matter contract for future notes:

```yaml
note_id: ""
title: ""
person_id: ""
note_type: "person | project | task | decision | meeting | source | lesson"
memory_scope: "personal"
review_state: "draft | reviewed | rejected | promoted"
sensitivity: "public | internal | restricted | confidential"
source_refs: []
links: []
created_at: "YYYY-MM-DD"
updated_at: "YYYY-MM-DD"
retention_until: "YYYY-MM-DD | indefinite"
version: "0.1"
```

## Acceptance criteria for the next BUILD stage

The BUILD stage should be accepted only if all of the following are true:

```text
BUILD_SCOPE_LIMITED_TO_REPOSITORY_VAULT_CONTRACT = true
STORAGE_PERSONAL_MEMORY_README_CREATED = true
EXAMPLE_PERSON_README_CREATED = true
VAULT_README_CREATED = true
REQUIRED_NOTE_FOLDERS_CREATED = true
REQUIRED_NOTE_FOLDERS_COUNT = 7
FRONT_MATTER_CONTRACT_DOCUMENTED = true
PERSONAL_MEMORY_BOUNDARY_DOCUMENTED = true
NOT_ORGANIZATIONAL_TRUTH_DOCUMENTED = true
REVIEW_REQUIRED_FOR_PROMOTION_DOCUMENTED = true
RAG_NOT_ACTIVE_DOCUMENTED = true
GRAPH_LINKS_NAVIGATION_NOT_PROOF_DOCUMENTED = true
REAL_PERSONAL_CONTENT_INCLUDED = false
ORGANIZATIONAL_SOURCE_APPROVAL_INCLUDED = false
PATIENT_OR_SENSITIVE_CONTENT_INCLUDED = false
EMBEDDINGS_OR_INDEX_CREATED = false
API_OR_UI_CREATED = false
DEPLOYABILITY_CLAIM_INCLUDED = false
CI_PASS_CLAIMED_WITHOUT_RUN = false
```

## Planned test for the later TEST stage

After BUILD, the TEST stage should validate repository contents only:

```text
EXPECTED_PATHS_EXIST = true
UNEXPECTED_REAL_CONTENT_FILES_EXIST = false
README_BOUNDARY_STRINGS_PRESENT = true
YAML_FRONT_MATTER_FIELDS_DOCUMENTED = true
REQUIRED_NOTE_FOLDERS_EXACTLY_MATCH_EXPECTED_SET = true
NO_RAG_INDEX_ARTIFACTS_CREATED = true
NO_ORGANIZATIONAL_MEMORY_PROMOTION_CLAIMED = true
```

The TEST stage should not claim runtime deployability unless a separate runtime test is performed and recorded.

## Work completed

Completed one bounded PLAN stage. The run defined the smallest safe BUILD scope for M0.2 Local Vault Structure: README contract files plus empty folder placeholders under `storage/personal_memory/example-person/vault/`.

No vault structure was built in this run. No templates, schemas, tests, indexes, embeddings, source registers, ingestion routes, UI screens, deploy artifacts, Organizational Memory objects, or RAG activation were created.

## Test / CI status

```text
CODE_CHANGED = false
DOCUMENTATION_EVIDENCE_ADDED = true
VAULT_STRUCTURE_CREATED = false
AUTOMATED_TESTS_RUN = false
LATEST_OBSERVED_COMMIT = 19e49a87b39d43ecf22021eff85a8597a1ba9552
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

- A repository vault contract may be mistaken for a deployable Personal Twin. The next BUILD must not claim deployability.
- Graph links may be mistaken for verified truth. The README must explicitly state that links are navigation, not proof.
- Source notes may be mistaken for approved organizational sources. The README must explicitly state source notes are personal references only unless separately reviewed and promoted.
- Example content can accidentally introduce personal or organizational facts. The next BUILD should use `.gitkeep` placeholders, not real notes.

## Single next stage

BUILD — create only the planned repository-visible local vault contract artifacts under `storage/personal_memory/`, preserving all memory-boundary and non-promotion constraints.
