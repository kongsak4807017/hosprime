# HosPrime Loop Engineering Run 0183 — M0.3 Runtime Observation Gate RESEARCH

Date: 2026-07-10

Linked issue: #157  
Parent trace: #156

## North Star outcome supported

Enable a healthcare / public-health manager to recover trusted work context in a local Personal Twin OS by navigating meeting -> decision -> task/source -> lesson in Obsidian, with evidence, accountability, measurable usability and zero unauthorized high-impact action.

## Current loop stage

```text
RESEARCH
```

Previous completed stage: BASELINE.

This run completes exactly one stage. It reviews current official Obsidian documentation to identify the minimum runtime configuration and observable behavior needed for a later authorized synthetic M0.3 trial. It does not run Obsidian, change the fixture, conduct a user trial, approve a release, or promote external findings into Organizational Memory.

## Real user and bounded work problem

Primary user role:

```text
healthcare / public-health manager resuming accountable work after a meeting in a local Personal Twin OS
```

Bounded task retained:

```text
open synthetic meeting note
-> follow decision
-> reach task
-> inspect source reference
-> reach lesson
-> decide whether the chain is understandable and useful for resuming work
```

The repository proves a Markdown/Wikilink text contract but has no runtime receipt showing that the expected notes, links, backlinks and graph relationships are visible or usable in Obsidian.

## Baseline retained

```text
CONTROLLED_RELEASE_TARGET = Milestone 0 — Personal Twin OS v0.1
README_M0_3_STATUS = NEXT
README_M0_4_STATUS = WAITING
CURRENT_ISSUE = #157 open
OPEN_PULL_REQUESTS_OBSERVED = 0
LATEST_MAIN_COMMIT_AT_INSPECTION = 1bacc2a12ad353e008f1386e7bac7a0d69b6cdc5
COMBINED_STATUSES_FOR_LATEST_COMMIT = []
AUTHORIZED_RUNTIME_TRIALS_ATTEMPTED = 0
AUTHORIZED_USER_TRIALS = 0
TRUSTED_TASK_COMPLETION_RATE = not computable
CI_PASS_CLAIMED = false
```

Target retained for a later authorized trial:

```text
EXPECTED_FIXTURE_NOTES_VISIBLE = 5/5
SELECTED_PATH_TRANSITIONS_NAVIGABLE = 4/4
BROKEN_LINKS_ON_SELECTED_PATH = 0
USER_ACCEPTANCE_DECISION_RECORDED = accepted or rejected with rationale
UNAUTHORIZED_HIGH_IMPACT_ACTIONS = 0
REAL_PERSONAL_OR_PATIENT_DATA_USED = 0
```

## Research method and source boundary

Only primary, official Obsidian Help pages were used. Findings remain in Research Staging pending review.

Accessed 2026-07-10:

1. Obsidian Help — Create a vault: https://obsidian.md/help/vault
2. Obsidian Help — Internal links: https://obsidian.md/help/links
3. Obsidian Help — Backlinks: https://obsidian.md/help/plugins/backlinks
4. Obsidian Help — Graph view: https://obsidian.md/help/plugins/graph
5. Obsidian Help — Settings: https://obsidian.md/help/settings

No community plugin documentation, forum post, third-party tutorial, benchmark, or marketing claim was used.

## Official-source findings retained in Research Staging

### R1 — Existing fixture folder can be opened as a vault

Official Obsidian Help defines a vault as a local file-system folder and documents opening an existing folder as a vault.

Implication for the later trial:

```text
The authorized executor can open the repository fixture root as an existing-folder vault without copying notes into a new knowledge store.
```

Required receipt fields:

```text
repository_commit_sha
fixture_root_path
vault_open_method = existing folder
```

Limitation: documentation establishes supported behavior, not that the HosPrime fixture has been opened successfully on any operating system.

### R2 — HosPrime Wikilink syntax is officially supported

Official Obsidian Help states that internal links support Wikilink forms such as `[[Note name]]` and Markdown-link forms. Obsidian generates Wikilinks by default unless the setting is disabled.

Implication for the later trial:

```text
The existing repository-local Wikilink fixture is a supported candidate input for runtime observation.
```

Required observation:

```text
Each selected visible link opens the intended existing note.
```

Limitation: supported syntax does not prove correct resolution where duplicate filenames, ambiguous paths, invalid characters, excluded files, or fixture errors exist.

### R3 — Backlinks require the Backlinks core plugin and an observable view

Official Obsidian Help defines a backlink as a link from another note to the active note. The Backlinks core plugin can show linked mentions in the sidebar, in a linked tab, or in the document. If the Backlinks tab is not visible, the documented command can show it.

Implication for the later trial:

```text
BACKLINKS_CORE_PLUGIN_ENABLED must be recorded.
BACKLINK_VIEW_METHOD must be recorded.
```

Minimum observable check:

```text
For at least one selected target note, the expected source note appears under Linked mentions.
```

Limitation: an outgoing link opening successfully is not by itself evidence that the backlink view was observed.

### R4 — Graph view is a core plugin; nodes and edges have explicit meanings

Official Obsidian Help states that Graph view is a core plugin. Circles represent notes/nodes and lines represent internal links. A node can be clicked to open the note. Local Graph shows notes connected to the active note and has a configurable depth.

Implication for the later trial:

```text
GRAPH_VIEW_CORE_PLUGIN_ENABLED must be recorded.
GRAPH_MODE = global or local must be recorded.
LOCAL_GRAPH_DEPTH must be recorded when Local Graph is used.
```

Minimum observable checks:

```text
5 expected fixture notes are visible as nodes under the selected graph settings.
Expected selected relationships are represented by graph connections.
Clicking a selected node opens the intended note.
```

Limitation: graph visualization alone does not establish that the manager understands the work chain or accepts it as useful.

### R5 — Graph filters and excluded-file settings can create false negatives

Official Graph view documentation states that Graph filters control visible nodes, including an Existing files only option, and that files matching excluded-file patterns do not appear in Graph view. Official Settings documentation states excluded files are hidden in Graph View and affect backlink-related unlinked mentions.

Implication for the later trial:

```text
EXCLUDED_FILE_PATTERNS must be recorded.
GRAPH_SEARCH_FILTER must be recorded.
EXISTING_FILES_ONLY_SETTING must be recorded.
```

A missing node cannot be classified as a fixture defect until these settings are checked.

Limitation: this does not imply filters should be disabled in normal use; it only requires trial configuration to be explicit and reproducible.

### R6 — Obsidian version is observable in Settings

Official Settings documentation states that the current Obsidian version and installer version are visible under General settings.

Implication for the later trial:

```text
obsidian_version
installer_version_when_available
operating_system_and_version
```

must be included in the runtime receipt.

Limitation: official documentation does not establish cross-version equivalence for the fixture or guarantee behavior on every supported platform.

## Minimum runtime configuration contract proposed for HYPOTHESIS

The following is a research-derived candidate, not an approved plan or executed configuration:

```text
vault_open_method = open existing folder
fixture_root_path = recorded
repository_commit_sha = recorded
obsidian_version = recorded
operating_system_and_version = recorded
backlinks_core_plugin_enabled = true
backlink_view_method = recorded
graph_view_core_plugin_enabled = true
graph_mode = recorded
local_graph_depth = recorded when applicable
graph_search_filter = recorded
existing_files_only_setting = recorded
excluded_file_patterns = recorded
community_plugins_required = false
synthetic_fixture_only = true
```

## Candidate observable runtime evidence for HYPOTHESIS

```text
O1: all 5 expected fixture notes appear in File Explorer or equivalent vault navigation
O2: selected Wikilinks open their intended existing notes
O3: at least one expected Linked mention is visible in Backlinks
O4: graph shows the expected fixture nodes under recorded settings
O5: graph shows the selected relationships under recorded settings
O6: clicking a selected graph node opens the intended note
O7: authorized manager completes the 4-transition path
O8: technical observation and user acceptance remain separate receipts
```

O1-O6 are technical runtime observations. O7-O8 concern later user testing and governance. Technical success must not be mislabeled as user acceptance.

## Research interpretation

The official documentation supports the feasibility of a bounded runtime trial using the existing local folder and Wikilink fixture. It also identifies configuration variables that can materially affect visibility: core-plugin state, graph mode/depth, graph filters, Existing files only, and excluded-file patterns.

Therefore, a valid later hypothesis should not merely predict that “Obsidian works.” It should predict that, under a recorded minimum configuration, the synthetic fixture produces specified observable notes, links, backlinks and graph relationships, while user acceptance remains a separate gate.

This research does not establish:

```text
OBSIDIAN_RUNTIME_EXECUTED = false
FIXTURE_RUNTIME_COMPATIBILITY_PROVEN = false
BACKLINKS_OBSERVED = false
GRAPH_RENDERING_OBSERVED = false
USER_TASK_COMPLETION_OBSERVED = false
USER_ACCEPTANCE_OBSERVED = false
TIME_SAVED_OBSERVED = false
CI_PASS_CLAIMED = false
M0_3_DONE = false
```

## Evidence inspected

```text
README.md on main
GitHub issue #157 and all current comments
engineering_runs/2026-07-10/0180-m0-3-runtime-observation-gate-real-problem.md
engineering_runs/2026-07-10/0181-m0-3-runtime-observation-gate-real-user.md
engineering_runs/2026-07-10/0182-m0-3-runtime-observation-gate-baseline.md
open GitHub issues
open GitHub pull requests
recent commits on main
combined status for commit 1bacc2a12ad353e008f1386e7bac7a0d69b6cdc5
official Obsidian Help pages listed above
```

Older open M1/M4 work was not selected because it does not supersede the current M0.3 controlled release gate.

## RESEARCH stage decision

```text
PRIMARY_OFFICIAL_SOURCES_USED = 5
EXTERNAL_FINDINGS_STAGED = true
MINIMUM_RUNTIME_VARIABLES_IDENTIFIED = true
CANDIDATE_OBSERVABLE_BEHAVIORS_IDENTIFIED = true
COMMUNITY_PLUGIN_DEPENDENCY_ADDED = false
EXTERNAL_FINDINGS_PROMOTED_TO_ORGANIZATIONAL_MEMORY = false
OBSIDIAN_EXECUTED = false
USER_TRIAL_EXECUTED = false
M0_3_MARKED_DONE = false
UNAUTHORIZED_CLAIMS_ADDED = 0
NEXT_STAGE = HYPOTHESIS
```

## Tests and CI

No application code, fixture, runtime configuration or governed memory content changed.

```text
REPOSITORY_TEST_RUN_IN_THIS_STAGE = false
OBSIDIAN_RUNTIME_TEST_RUN = false
USER_ACCEPTANCE_TEST_RUN = false
COMBINED_STATUSES_FOR_LATEST_INSPECTED_COMMIT = []
CI_PASS_CLAIMED = false
```

## Memory layer affected

```text
Engineering-run evidence: updated
Issue traceability: update required on #157
Research Staging: updated with official-source findings pending review
Personal / Staff Twin Memory: unchanged
Person Memory: unchanged
Role Memory: unchanged
Organizational Memory / Governed RAG: unchanged
Synthetic fixture: referenced only; unchanged
```

No external finding was promoted into organizational truth.

## Risks and blockers

```text
RISK_FILTER_CAUSES_FALSE_NEGATIVE = identified; record graph filters and exclusions
RISK_PLUGIN_STATE_CAUSES_FALSE_NEGATIVE = identified; record core-plugin state
RISK_GRAPH_VISIBILITY_MISLABELED_AS_USABILITY = controlled by separate technical and acceptance receipts
RISK_SUPPORTED_SYNTAX_MISLABELED_AS_RUNTIME_PROOF = controlled; no runtime claim made
RISK_UNAUTHORIZED_RUNTIME_ACTION = controlled; no execution performed
RISK_PERSONAL_OR_PATIENT_DATA_EXPOSURE = controlled; synthetic-only boundary retained
RISK_SEQUENCE_SKIP_TO_M0_4 = controlled; M0.4 remains WAITING
RISK_CI_AMBIGUITY = present; no statuses found
```

Current execution blocker remains:

```text
No consenting participant, delegated acceptance authority, authorized Obsidian executor, runtime environment or completed authorization receipt is recorded.
```

Accountable owner: repository/product owner or explicitly delegated M0.3 reviewer.

## Next single stage

```text
HYPOTHESIS
```

Define one falsifiable hypothesis linking the recorded minimum Obsidian configuration to the specified technical observations and later user-acceptance gate. Do not execute Obsidian or conduct a user trial during HYPOTHESIS.