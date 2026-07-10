# HosPrime Loop Engineering Run 0185 — M0.3 Runtime Observation Gate PLAN

Date: 2026-07-10

Linked issue: #157  
Parent trace: #156

## North Star outcome supported

Enable a healthcare / public-health manager to recover trusted work context in a local Personal Twin OS by navigating meeting -> decision -> task/source -> lesson with reproducible evidence, explicit human acceptance and zero unauthorized high-impact action.

## Current loop stage

```text
PLAN
```

Previous completed stage: HYPOTHESIS.

This run completes exactly one stage. It creates the minimum non-executing, receipt-driven trial plan required to test H1 after authorization. It does not execute Obsidian, conduct a user trial, modify the synthetic fixture, claim CI success, activate RAG, promote memory, or mark M0.3 DONE.

## Repository control state inspected

```text
CONTROLLED_RELEASE_TARGET = Milestone 0 — Personal Twin OS v0.1
README_M0_3_STATUS = NEXT
README_M0_4_STATUS = WAITING
CURRENT_ISSUE = #157 open
OPEN_PULL_REQUESTS_OBSERVED = 0
LATEST_MAIN_COMMIT_AT_INSPECTION = 4b57fd7cf1d0930a63d91741a3f7c26835a87914
COMBINED_STATUSES_FOR_LATEST_COMMIT = []
WORKFLOW_RUNS_FOR_LATEST_COMMIT = []
CI_PASS_CLAIMED = false
```

The current controlled scope remains M0.3 runtime and user observation. Advancing to M0.4 would skip the remaining M0.3 usability gate.

## Real user and bounded work problem

Primary user role:

```text
healthcare / public-health manager resuming accountable work after a meeting in a local Personal Twin OS
```

Bounded task:

```text
open synthetic meeting note
-> follow decision
-> reach task
-> inspect source reference
-> reach lesson
-> decide whether the chain is understandable and useful for resuming work
```

Baseline:

```text
AUTHORIZED_RUNTIME_TRIALS_ATTEMPTED = 0
AUTHORIZED_USER_TRIALS_ATTEMPTED = 0
TRUSTED_TASK_COMPLETION_RATE = not computable because denominator is zero
OBSERVED_TASK_DURATION_BASELINE = absent
```

Target for one later authorized trial:

```text
EXPECTED_NOTES_VISIBLE = 5/5
SELECTED_PATH_TRANSITIONS_NAVIGABLE = 4/4
EXPECTED_BACKLINK_OBSERVED = at least 1
EXPECTED_GRAPH_NODES_VISIBLE = 5/5
SELECTED_GRAPH_RELATIONSHIPS_VISIBLE = 4/4
GRAPH_NODE_NAVIGATION_OBSERVED = at least 1
BROKEN_LINKS_ON_SELECTED_PATH = 0
USER_COMPLETES_WITHOUT_EXECUTOR_INTERVENTION = true
USER_ACCEPTANCE_DECISION = accepted
UNAUTHORIZED_HIGH_IMPACT_ACTIONS = 0
REAL_PERSONAL_OR_PATIENT_DATA_USED = 0
MATERIAL_GOVERNANCE_INCIDENTS = 0
```

The first observed duration becomes a baseline only. No time-saved improvement claim is allowed from one trial.

## Trial authorization gate

No execution may begin until a complete authorization receipt records:

```text
trial_id
repository_owner_or_delegated_authorizer
technical_executor_identity_or_role
manager_participant_identity_or_role
acceptance_authority_identity_or_role
consent_or_delegation_reference
approved synthetic-only scope
approved fixture path
approved repository commit SHA
approved execution window
prohibited actions
receipt timestamp
```

Required separation:

- technical executor observes runtime behavior;
- manager participant performs the task;
- acceptance authority accepts or rejects the result;
- one person may hold multiple roles only when the authorization receipt explicitly records that delegation;
- technical success alone is never user acceptance.

Current blocker: no complete authorization receipt exists.

## Fixed fixture and version gate

Before execution, the executor must record:

```text
REPOSITORY_SHA = exact checked-out commit
FIXTURE_PATH = exact synthetic vault path
FIXTURE_FILE_LIST = five expected notes
FIXTURE_HASH_OR_DIFF = recorded before trial
REAL_DATA_PRESENT = false
```

The trial must stop if:

- the checked-out SHA differs from the approved SHA;
- expected fixture files are missing;
- unreviewed fixture changes are detected;
- real personal, staff, patient, or confidential organizational data is present.

## Runtime environment receipt

The technical receipt must capture:

```text
operating system and version
Obsidian version
vault open method = existing local folder
Backlinks core plugin enabled state
Graph View core plugin enabled state
community plugins used = none
graph mode = global or local
graph depth when local
search/filter expression
Existing files only setting
excluded-file patterns
fixture root path
trial start and end timestamps
```

Unknown or omitted settings make the trial inconclusive, not successful.

## Exact technical execution script

After authorization only, the technical executor performs this bounded script without changing fixture content:

1. Check out the authorized repository SHA.
2. Verify the fixture path, five-note inventory and pre-trial diff/hash receipt.
3. Open the approved synthetic fixture folder as an Obsidian vault.
4. Record OS, Obsidian version and all required settings.
5. Confirm Backlinks and Graph View core-plugin state.
6. Confirm all five expected notes are visible.
7. Open the synthetic meeting note.
8. Follow the four preselected Wikilink transitions through decision, task/source and lesson.
9. Record whether each transition opens the intended existing note.
10. Observe at least one expected linked mention in Backlinks.
11. Open the recorded graph mode and confirm five expected nodes and four selected relationships under the recorded settings.
12. Open at least one intended note from a graph node.
13. Record broken-link count for the selected path.
14. Save evidence receipts without adding real data or editing governed memory.

The executor must not coach the manager during the separate user task.

## Exact manager task script

After the technical receipt is complete and the participant is authorized:

1. Start timing when the manager opens the synthetic meeting note.
2. Ask the manager to recover the decision, assigned task, source reference and lesson using the visible links/backlinks/graph as they choose.
3. Do not provide navigation assistance.
4. Stop timing when the manager states the recovered chain or stops the attempt.
5. Record completion or non-completion of each of the four transitions.
6. Ask for an explicit acceptance decision:

```text
accepted = understandable and useful enough to resume this bounded work
rejected = not understandable or not useful enough
```

7. Record the rationale in the participant's own summarized words without storing sensitive personal information.

## Required evidence artifacts

The later trial must produce separate artifacts:

```text
A. authorization receipt
B. fixture/version receipt
C. runtime environment receipt
D. technical observation receipt
E. manager task receipt
F. acceptance review receipt
G. incident/blocker receipt when applicable
```

Minimum technical evidence:

- exact repository SHA and fixture path;
- five-note inventory and unchanged/diff record;
- settings receipt;
- note visibility count;
- transition-by-transition result;
- backlink observation;
- graph node and relationship counts;
- graph-node navigation result;
- broken-link count;
- timestamps.

Minimum manager evidence:

- authorized participant role;
- task attempted;
- four-transition completion result;
- executor intervention count;
- measured duration;
- accepted/rejected decision;
- rationale;
- governance incident count.

Screenshots may supplement receipts but cannot replace structured observations, authorization or human acceptance.

## Pass, fail and inconclusive decision rule

### PASS

H1 is supported for the tested configuration only when every mandatory condition in run 0184 is evidenced, including accepted manager decision and zero governance incidents.

For the first approved trial:

```text
TTCR = 1/1
```

only when the approved task is accepted, evidence and approval are complete, and no material governance incident occurs.

### FAIL

```text
TTCR = 0/1
```

when an authorized, fully evidenced trial is attempted but any mandatory product or user acceptance condition fails.

### INCONCLUSIVE

Do not count the trial in TTCR when authorization, configuration, evidence, task attempt or role separation is incomplete. Record the blocker, accountable owner and next bounded correction instead.

## Stop conditions

Stop immediately and record a blocker if any of the following occurs:

```text
missing or invalid authorization
repository SHA mismatch
fixture mutation without review
real personal/patient/confidential data discovered
required core-plugin/settings state cannot be recorded
technical executor must alter fixture content to proceed
manager asks for or receives executor navigation assistance
security, privacy or governance incident
required evidence cannot be captured
```

No stop condition authorizes a workaround that changes scope.

## Acceptance review

The acceptance authority reviews the seven evidence artifacts and records exactly one result:

```text
ACCEPTED_FOR_M0_3_EVALUATION
REJECTED_WITH_REASONS
INCONCLUSIVE_WITH_MISSING_EVIDENCE
```

This review does not itself mark M0.3 DONE, release the product, activate RAG, or promote any content to Organizational Memory. Later ordered stages remain TEST -> EVALUATE -> REVIEW -> RELEASE only after an authorized BUILD has created the approved receipt artifact or execution mechanism.

## PLAN stage decision

```text
MINIMUM_TRIAL_PLAN_DEFINED = true
AUTHORIZATION_GATE_DEFINED = true
ROLES_SEPARATED = true
FIXTURE_AND_SHA_GATE_DEFINED = true
RUNTIME_SETTINGS_RECEIPT_DEFINED = true
TECHNICAL_SCRIPT_DEFINED = true
MANAGER_TASK_SCRIPT_DEFINED = true
EVIDENCE_ARTIFACTS_DEFINED = true
PASS_FAIL_INCONCLUSIVE_RULE_DEFINED = true
STOP_CONDITIONS_DEFINED = true
OBSIDIAN_EXECUTED = false
USER_TRIAL_EXECUTED = false
CI_PASS_CLAIMED = false
M0_3_MARKED_DONE = false
UNAUTHORIZED_CLAIMS_ADDED = 0
NEXT_STAGE = BUILD
```

## Tests and CI

No application code, fixture, runtime configuration or governed memory content changed in this PLAN stage.

```text
REPOSITORY_TEST_RUN_IN_THIS_STAGE = false
OBSIDIAN_RUNTIME_TEST_RUN = false
USER_ACCEPTANCE_TEST_RUN = false
COMBINED_STATUSES_FOR_LATEST_INSPECTED_COMMIT = []
WORKFLOW_RUNS_FOR_LATEST_INSPECTED_COMMIT = []
CI_PASS_CLAIMED = false
```

## Memory layer affected

```text
Engineering-run evidence: updated
Issue traceability: update required on #157
Research Staging: referenced only; unchanged and not promoted
Personal / Staff Twin Memory: unchanged
Person Memory: unchanged
Role Memory: unchanged
Organizational Memory / Governed RAG: unchanged
Synthetic fixture: unchanged
```

## Risks and blockers

```text
BLOCKER_AUTHORIZATION_RECEIPT = present
BLOCKER_AUTHORIZED_EXECUTOR = present
BLOCKER_CONSENTING_MANAGER_PARTICIPANT = present
BLOCKER_ACCEPTANCE_AUTHORITY = present
BLOCKER_RUNTIME_ENVIRONMENT = present
RISK_CONFIGURATION_FALSE_NEGATIVE = controlled by settings receipt
RISK_EXECUTOR_COACHING = controlled by no-intervention script
RISK_TECHNICAL_SUCCESS_MISLABELED_AS_ACCEPTANCE = controlled by separate receipts
RISK_REAL_DATA_EXPOSURE = controlled by synthetic-only preflight and stop condition
RISK_TIME_SAVED_OVERCLAIM = controlled; first duration is baseline only
RISK_CI_AMBIGUITY = present; no status or workflow evidence found
```

Accountable owner for resolving authorization blockers: repository/product owner or explicitly delegated M0.3 reviewer.

## Next single stage

```text
BUILD
```

Create exactly one minimal non-executing trial-receipt artifact or validation mechanism implementing this approved plan. Do not execute Obsidian or conduct the manager trial during BUILD unless a separate complete authorization receipt and approved executor record already exist.