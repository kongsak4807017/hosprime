# HosPrime Loop Engineering Run 0184 — M0.3 Runtime Observation Gate HYPOTHESIS

Date: 2026-07-10

Linked issue: #157  
Parent trace: #156

## North Star outcome supported

Enable a healthcare / public-health manager to recover trusted work context in a local Personal Twin OS by navigating meeting -> decision -> task/source -> lesson with reproducible evidence, explicit human acceptance and zero unauthorized high-impact action.

## Current loop stage

```text
HYPOTHESIS
```

Previous completed stage: RESEARCH.

This run completes exactly one stage. It defines one falsifiable hypothesis for a later authorized synthetic Obsidian trial. It does not execute Obsidian, change the fixture, conduct a user trial, approve a release, activate RAG, or promote Research Staging findings into Organizational Memory.

## Real user and bounded work problem

Primary user role:

```text
healthcare / public-health manager resuming accountable work after a meeting in a local Personal Twin OS
```

Bounded work task:

```text
open synthetic meeting note
-> follow decision
-> reach task
-> inspect source reference
-> reach lesson
-> determine whether the chain is understandable and useful for resuming work
```

The repository proves the Markdown/Wikilink text contract but does not yet prove runtime visibility, graph/backlink behavior, task completion or user acceptance in Obsidian.

## Baseline retained

```text
CONTROLLED_RELEASE_TARGET = Milestone 0 — Personal Twin OS v0.1
README_M0_3_STATUS = NEXT
README_M0_4_STATUS = WAITING
CURRENT_ISSUE = #157 open
OPEN_PULL_REQUESTS_OBSERVED = 0
LATEST_MAIN_COMMIT_AT_INSPECTION = 3713d042c5b4871249c000f141b067452cc7c22a
COMBINED_STATUSES_FOR_LATEST_COMMIT = []
WORKFLOW_RUNS_FOR_LATEST_COMMIT = []
AUTHORIZED_RUNTIME_TRIALS_ATTEMPTED = 0
AUTHORIZED_USER_TRIALS = 0
TRUSTED_TASK_COMPLETION_RATE = not computable because denominator is zero
CI_PASS_CLAIMED = false
```

## Research basis retained in Research Staging

Official Obsidian documentation reviewed in run 0183 supports the following candidate conditions and observations:

- an existing local folder can be opened as a vault;
- the fixture's `[[Wikilink]]` syntax is supported;
- Backlinks and Graph view are core plugins;
- graph mode/depth, search filters, Existing files only and excluded-file patterns can change visibility;
- runtime and application settings must be recorded for reproducibility;
- technical visibility is not equivalent to manager acceptance.

These external findings remain Research Staging evidence pending review. They are not Organizational Memory or an execution receipt.

## Single falsifiable hypothesis

### H1 — Recorded configuration enables trusted graph-memory task completion

```text
IF
  an authorized executor opens the unchanged synthetic fixture at a recorded repository SHA
  as an existing-folder Obsidian vault,
  records the operating system and Obsidian version,
  enables the Backlinks and Graph View core plugins,
  records graph mode/depth, graph filter, Existing files only and excluded-file patterns,
  uses no community plugin dependency,
  uses no real personal or patient data,
  and a separately authorized healthcare/public-health manager performs the bounded work task,

THEN
  the technical runtime receipt will show:
    5/5 expected fixture notes visible,
    4/4 selected path transitions opening the intended existing notes,
    at least 1 expected linked mention visible in Backlinks,
    5/5 expected fixture notes represented as graph nodes under the recorded settings,
    all 4 selected path relationships represented as graph connections,
    at least 1 selected graph node opening the intended note,
    0 broken links on the selected path;

  and the separate user receipt will show:
    the manager completes the 4-transition path without executor intervention,
    an explicit accepted or rejected decision with rationale,
    task duration recorded rather than estimated,
    evidence completeness recorded,
    0 unauthorized high-impact actions,
    0 real personal or patient records used.
```

For this first controlled trial, Trusted Task Completion Rate becomes computable only after one approved target task is attempted:

```text
TTCR = 1/1 only if output is accepted,
      required evidence and human approval are complete,
      and no material governance incident occurs.

TTCR = 0/1 if the approved trial is attempted but any mandatory acceptance condition fails.
```

No time-saved improvement claim is permitted from one trial because no comparable prior-task duration baseline exists. The first observed duration becomes a baseline for later repeated trials.

## Mandatory pass conditions

The hypothesis is supported only when every condition below is evidenced:

```text
AUTHORIZATION_RECEIPT_COMPLETE = true
RUNTIME_ENVIRONMENT_RECEIPT_COMPLETE = true
REPOSITORY_SHA_RECORDED = true
FIXTURE_UNCHANGED_OR_DIFF_RECORDED = true
EXPECTED_NOTES_VISIBLE = 5/5
SELECTED_PATH_TRANSITIONS_NAVIGABLE = 4/4
EXPECTED_BACKLINK_OBSERVED = at least 1
EXPECTED_GRAPH_NODES_VISIBLE = 5/5
SELECTED_GRAPH_RELATIONSHIPS_VISIBLE = 4/4
GRAPH_NODE_NAVIGATION_OBSERVED = at least 1
BROKEN_LINKS_ON_SELECTED_PATH = 0
USER_TASK_ATTEMPTED = true
USER_COMPLETED_PATH_WITHOUT_EXECUTOR_INTERVENTION = true
USER_ACCEPTANCE_DECISION_RECORDED = accepted
USER_ACCEPTANCE_RATIONALE_RECORDED = true
TASK_DURATION_RECORDED = true
TECHNICAL_AND_USER_RECEIPTS_SEPARATE = true
UNAUTHORIZED_HIGH_IMPACT_ACTIONS = 0
REAL_PERSONAL_OR_PATIENT_DATA_USED = 0
MATERIAL_GOVERNANCE_INCIDENTS = 0
```

## Pre-registered failure and inconclusive conditions

### Hypothesis falsified for the tested configuration

The hypothesis is falsified for the tested configuration if an authorized and fully recorded trial has any of the following:

```text
fewer than 5 expected notes visible;
any selected Wikilink opens the wrong note or no note;
no expected linked mention is observable after the recorded Backlinks check;
fewer than 5 expected graph nodes or fewer than 4 selected graph relationships are visible under the recorded settings;
a selected graph node does not open the intended note;
any broken link occurs on the selected path;
the manager cannot complete the path without executor intervention;
the authorized manager rejects the chain as understandable/useful;
any unauthorized high-impact action, real personal/patient data use or material governance incident occurs.
```

### Trial inconclusive, not a product failure

The trial is inconclusive and must not be counted as a successful or failed user trial when:

```text
authorization is absent or incomplete;
repository SHA, fixture path, OS, Obsidian version or relevant settings are not recorded;
plugin state, graph filters or exclusions are unknown;
the fixture changed without a recorded diff;
technical and user acceptance roles/receipts are conflated;
the user task is not attempted;
evidence is missing or cannot be independently reviewed.
```

An inconclusive trial must produce a blocker record, accountable owner and next executable correction. It must not produce a M0.3 DONE claim.

## Competing explanations to control in PLAN

A later plan must distinguish fixture defects from environment/configuration effects:

```text
C1: graph/backlink core plugin disabled
C2: graph search filter hides expected notes
C3: Existing files only setting changes visible nodes
C4: excluded-file patterns hide notes
C5: duplicate or ambiguous note names change link resolution
C6: executor assistance inflates apparent user task completion
C7: graph rendering is technically correct but the manager rejects usefulness
C8: evidence capture is incomplete despite apparent runtime success
```

## HYPOTHESIS stage decision

```text
ONE_FALSIFIABLE_HYPOTHESIS_DEFINED = true
TECHNICAL_AND_USER_GATES_SEPARATED = true
MANDATORY_PASS_CONDITIONS_DEFINED = true
FAILURE_CONDITIONS_DEFINED = true
INCONCLUSIVE_CONDITIONS_DEFINED = true
TTCR_CALCULATION_RULE_DEFINED = true
TIME_SAVED_IMPROVEMENT_CLAIMED = false
OBSIDIAN_EXECUTED = false
USER_TRIAL_EXECUTED = false
EXTERNAL_FINDINGS_PROMOTED_TO_ORGANIZATIONAL_MEMORY = false
M0_3_MARKED_DONE = false
UNAUTHORIZED_CLAIMS_ADDED = 0
NEXT_STAGE = PLAN
```

## Tests and CI

No application code, fixture, runtime configuration or governed memory content changed.

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
Synthetic fixture: referenced only; unchanged
```

## Risks and blockers

```text
RISK_CONFIGURATION_FALSE_NEGATIVE = controlled by mandatory settings receipt
RISK_RUNTIME_SUCCESS_MISLABELED_AS_USER_ACCEPTANCE = controlled by separate receipts
RISK_EXECUTOR_ASSISTANCE_BIASES_USER_RESULT = controlled by no-intervention condition
RISK_SINGLE_TRIAL_TIME_SAVED_OVERCLAIM = controlled; duration becomes baseline only
RISK_MISSING_EVIDENCE_MISLABELED_AS_FAILURE = controlled by inconclusive classification
RISK_UNAUTHORIZED_RUNTIME_ACTION = controlled by authorization receipt requirement
RISK_PERSONAL_OR_PATIENT_DATA_EXPOSURE = controlled by synthetic-only boundary
RISK_SEQUENCE_SKIP_TO_M0_4 = controlled; M0.4 remains WAITING
RISK_CI_AMBIGUITY = present; no statuses or workflow runs found
```

Current execution blocker remains:

```text
No consenting participant, delegated acceptance authority, authorized Obsidian executor, runtime environment or completed authorization receipt is recorded.
```

Accountable owner: repository/product owner or explicitly delegated M0.3 reviewer.

## Next single stage

```text
PLAN
```

Create the minimum non-executing, receipt-driven trial plan that can test H1 after authorization. The plan must specify roles, fixture SHA, environment/settings capture, exact task script, evidence artifacts, stop conditions and acceptance review. Do not execute Obsidian or conduct a user trial during PLAN.