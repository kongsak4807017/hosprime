# HosPrime Loop Engineering Run 0153 — M0.2 Local Vault Structure RESEARCH

Date: 2026-07-09

Stage: RESEARCH

Linked issue: #155

## North Star outcome supported

Knowledge continuity, reduced repetitive workload, evidence quality, decision-to-outcome traceability, knowledge reuse, user trust, and zero unauthorized high-impact action.

This RESEARCH stage supports Milestone 0 — Personal Twin OS v0.1 by validating the smallest safe local vault contract before any M0.2 plan or build step. The result is research staging only. It does not release a vault structure, create folders, migrate personal content, activate RAG, promote Organizational Memory, claim deployment, claim CI success, or claim real-user acceptance.

## Real user and real work problem

Real user: an individual healthcare or public-health staff member using Personal Twin OS v0.1 for daily work capture, decision tracking, meeting follow-up, source linking, and lessons learned.

Real work problem: without a stable local Markdown / Obsidian-compatible vault contract, daily notes, tasks, decisions, meetings, sources and lessons cannot be reliably linked, inspected, reviewed, corrected, reused or later promoted through governed memory boundaries.

## Baseline carried forward

From BASELINE run `0152-m0-2-local-vault-structure-baseline.md`:

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
- issue #155 and comments
- open pull request lookup
- recent commits on `main`
- CI status and workflow lookup for latest observed commit `758e2701959855598dad57feb8187db89e01cdb6`
- `docs/architecture/TWO_LAYER_MEMORY_ARCHITECTURE.md`
- `docs/architecture/LOOP_ENGINEERING_ARCHITECTURE.md`
- `backend/app/memory/personal_graph_store.py`
- `backend/app/memory/contracts.py`
- prior engineering run `engineering_runs/2026-07-09/0152-m0-2-local-vault-structure-baseline.md`

External research staging evidence, retrieved 2026-07-09:

1. Obsidian Help — Internal links: `https://obsidian.md/help/links`
2. Obsidian Help — Properties: `https://obsidian.md/help/properties`
3. Obsidian Help — Graph view: `https://obsidian.md/help/plugins/graph`

Limitations:

- External Obsidian documentation is product guidance, not HosPrime policy.
- External findings are not Organizational Memory and are not approved institutional truth.
- Findings only inform the next HYPOTHESIS stage for a local personal vault contract.
- No external source was used to approve source ingestion, RAG activation, access control, or healthcare policy.

## Internal architecture findings

`docs/architecture/TWO_LAYER_MEMORY_ARCHITECTURE.md` already defines the intended storage model:

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

It also requires each note to contain YAML properties, Markdown content, internal `[[Wiki Links]]`, source references, review status, sensitivity, and retention metadata. Required node types include Person, Role, Responsibility, Project, Task, Meeting, Decision, Lesson, Skill, Relationship, Source and Daily Note.

`backend/app/memory/personal_graph_store.py` already contains a code-level direction for an Obsidian-compatible Markdown graph scoped to one staff member. It writes Markdown notes under:

```text
<storage_dir>/personal_memory/<person-id>/vault/<note_type>/<note_id>.md
```

It extracts wiki links with a `[[...]]` pattern, builds graph nodes from Markdown files, and creates unresolved nodes when a linked target is referenced but no note exists. This is useful for graph continuity but does not by itself release a repository-visible M0.2 vault contract.

`backend/app/memory/contracts.py` already defines `MemoryNote`, `MemoryScope`, `ReviewState`, `Sensitivity`, `PromotionRequest`, `GraphNode`, `GraphEdge`, and `GraphSnapshot`. This supports a controlled contract, but M0.2 still needs a repository-level vault contract that is inspectable by humans before build and test.

## External research staging findings

### Finding 1 — Notes should remain normal Markdown files with internal links

Obsidian's internal link documentation says internal links create a network of knowledge and supports wiki links such as `[[Three laws of motion]]` and Markdown links. It also notes that wiki links are compact by default and that Markdown links can be used when interoperability matters.

Implication for HosPrime M0.2:

```text
M0_2_LINK_CONTRACT_SHOULD_SUPPORT_WIKILINKS = true
M0_2_LINK_CONTRACT_SHOULD_NOT_DEPEND_ON_OBSIDIAN_ONLY_FEATURES_FOR_CORE_IDENTITY = true
```

A safe minimum vault contract should use `[[note-id]]` or clear note IDs in properties for graph edges, while preserving plain Markdown readability outside Obsidian.

### Finding 2 — Properties should be structured, atomic metadata

Obsidian's properties documentation says properties organize information about a note, can store structured values such as text, links, dates, checkboxes and numbers, and are stored in YAML format at the top of a file. It also notes that Markdown in properties is not supported because properties are meant to be small, atomic, human- and machine-readable information.

Implication for HosPrime M0.2:

```text
M0_2_METADATA_CONTRACT_SHOULD_USE_SIMPLE_TOP_OF_FILE_PROPERTIES = true
M0_2_PROPERTIES_SHOULD_KEEP_LONG_RATIONALE_IN_MARKDOWN_BODY = true
M0_2_PROPERTIES_SHOULD_INCLUDE_MEMORY_BOUNDARY_FIELDS = true
```

A safe minimum contract should keep fields such as `note_id`, `note_type`, `person_id`, `memory_scope`, `review_state`, `sensitivity`, `source_refs`, `created_at`, `updated_at`, `retention_until`, and `version` in structured front matter, while keeping narrative, rationale and observations in the Markdown body.

### Finding 3 — Graph view is relationship visualization, not proof of truth

Obsidian's graph documentation describes nodes as notes and lines as internal links between notes. It also provides filters such as existing files, tags, attachments and local graph depth.

Implication for HosPrime M0.2:

```text
M0_2_GRAPH_SHOULD_BE_BUILT_FROM_LINKS = true
M0_2_GRAPH_EDGE_TRUTH_SHOULD_REQUIRE_PROVENANCE_AND_REVIEW_STATE = true
```

This matches the HosPrime architecture boundary: a visual graph does not prove that a relationship is correct. Every edge later used for trusted answers must remain tied to provenance and review state.

## Minimum research-backed vault contract candidate for next HYPOTHESIS

The next HYPOTHESIS stage should test whether M0.2 can safely define a small repository-visible contract with:

```text
storage/personal_memory/README.md
storage/personal_memory/example-person/vault/README.md
storage/personal_memory/example-person/vault/people/.gitkeep
storage/personal_memory/example-person/vault/projects/.gitkeep
storage/personal_memory/example-person/vault/tasks/.gitkeep
storage/personal_memory/example-person/vault/decisions/.gitkeep
storage/personal_memory/example-person/vault/meetings/.gitkeep
storage/personal_memory/example-person/vault/sources/.gitkeep
storage/personal_memory/example-person/vault/lessons/.gitkeep
```

Candidate minimum note types for M0.2 acceptance:

```text
Person
Project
Task
Decision
Meeting
Source
Lesson
```

Candidate required properties:

```yaml
note_id: example-task-001
title: Example task
person_id: example-person
note_type: task
memory_scope: personal
review_state: captured
sensitivity: internal
source_refs: []
links: []
created_at: 2026-07-09T00:00:00+07:00
updated_at: 2026-07-09T00:00:00+07:00
retention_until: null
version: 1
```

Candidate contract boundaries:

```text
PERSONAL_MEMORY_IS_NOT_ORGANIZATIONAL_TRUTH = true
RESEARCH_STAGING_IS_NOT_ORGANIZATIONAL_TRUTH = true
SOURCE_NOTES_RECORD_REFERENCES_ONLY_UNTIL_APPROVED = true
PROMOTION_REQUIRES_REVIEW_RECORD = true
RAG_ACTIVATION_NOT_INCLUDED_IN_M0_2 = true
DEPLOYABILITY_NOT_CLAIMED_BY_M0_2_CONTRACT_ALONE = true
```

## Research stage target metric

```text
RESEARCH_STAGE_COMPLETED = true
README_READ = true
OPEN_ISSUES_INSPECTED = true
OPEN_PRS_INSPECTED = true
RECENT_ENGINEERING_RUN_INSPECTED = true
CI_STATUS_INSPECTED = true
INTERNAL_ARCHITECTURE_INSPECTED = true
CURRENT_CODE_CONTRACT_INSPECTED = true
PRIMARY_EXTERNAL_OBSIDIAN_SOURCES_RETRIEVED = 3
EXTERNAL_FINDINGS_STAGED_ONLY = true
MINIMUM_VAULT_CONTRACT_CANDIDATE_DEFINED = true
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

Completed one bounded RESEARCH stage. The run validated the minimum Obsidian-compatible local vault contract direction, recorded provenance and limitations, identified relevant existing architecture and code, and defined a candidate contract for the next HYPOTHESIS stage.

No vault folders, note templates, schemas, tests, indexes, embeddings, source registers, ingestion routes, UI screens, deploy artifacts, Organizational Memory objects, or RAG activation were created.

## Test / CI status

```text
CODE_CHANGED = false
VAULT_STRUCTURE_CREATED = false
AUTOMATED_TESTS_RUN = false
LATEST_OBSERVED_COMMIT = 758e2701959855598dad57feb8187db89e01cdb6
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
Research Staging = updated as staged research findings inside this engineering-run evidence file only
Organizational Memory / Governed RAG = not affected
Engineering-run evidence = updated
Issue traceability = to be updated
```

## Risks or blockers

- Obsidian compatibility can be over-implemented. M0.2 should stay to a minimal readable Markdown vault contract, not plugin dependency or UI expansion.
- Current code renders properties as JSON inside front matter, which Obsidian can interpret and later save as YAML, but the user-facing repository contract should prefer simple YAML examples for human readability.
- A graph can make relationships look authoritative. The next contract must state that links are navigational until supported by provenance and review state.
- Source notes in a personal vault may reference external or organizational information, but they must not become approved source records or active RAG entries without review.

## Single next stage

HYPOTHESIS — state a testable hypothesis for the smallest repository-visible M0.2 vault contract that can support Person, Project, Task, Decision, Meeting, Source and Lesson notes while preserving memory boundaries.