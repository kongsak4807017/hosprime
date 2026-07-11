# HosPrime Loop Engineering 0199 — M0.3 Trial Readiness — HYPOTHESIS

Date: 2026-07-11
Controlling issue: #158
Parent issue: #157
Loop stage completed: HYPOTHESIS
Single next stage: PLAN

## North Star outcome supported

Protect Trusted Task Completion Rate, evidence quality, user trust, decision-to-outcome traceability and zero unauthorized high-impact action by defining a falsifiable proposition for a trial-readiness record that cannot be mistaken for authorization, consent, execution or acceptance.

## Real user and real work problem

The future real user is a consenting healthcare/public-health manager who must independently recover the synthetic meeting → decision → task/source → lesson chain in Obsidian.

The organizational problem is that the repository has a controlled evidence contract and a research-derived candidate field set, but no single trial-specific readiness record yet demonstrates whether all eight required gates can be represented consistently and fail closed when evidence is missing, expired, conflicted or unapproved.

## Repository control state inspected

At the start of this run:

- README North Star and Core Rules were read on `main`;
- Milestone 0 — Personal Twin OS v0.1 remained the current controlled release target;
- M0.3 remained `NEXT`, requiring usable backlinks and graph navigation;
- issue #158 remained open and controlling;
- engineering runs 0196, 0197 and 0198 preserved REAL USER → BASELINE → RESEARCH;
- latest pre-run `main` commit was `d8394bc581491aebbbf0e3334bdc576843943451`;
- open pull requests found: 0;
- combined commit status records on the latest pre-run commit: 0;
- no Obsidian runtime execution, manager task, user acceptance, CI pass or M0.3 completion was evidenced.

## Baseline and target metric

Baseline:

```text
MODEL_READY = true
EXECUTION_READINESS_GATES_COMPLETE = 0/8
TRIAL_READY = false
AUTHORIZED_RUNTIME_TRIALS = 0
AUTHORIZED_MANAGER_TRIALS = 0
TRUSTED_TASK_COMPLETION_RATE = NOT_COMPUTABLE
EVIDENCE_RETENTION_AUTHORITY = NOT_ASSIGNED
EVIDENCE_RETENTION_PERIOD = PENDING_APPROVAL
```

HYPOTHESIS-stage target:

```text
ONE_FALSIFIABLE_PROPOSITION_RECORDED = true
EIGHT_READINESS_GATES_INCLUDED = 8/8
PASS_CONDITIONS_PREDECLARED = true
FAIL_CONDITIONS_PREDECLARED = true
INCONCLUSIVE_CONDITIONS_PREDECLARED = true
UNAUTHORIZED_ACTIONS = 0
EXTERNAL_FINDINGS_PROMOTED = 0
```

## Falsifiable hypothesis

> **H1:** A single consolidated M0.3 trial-readiness record can represent all eight trial-specific readiness gates and remain fail closed: it will report `TRIAL_READY = true` only when every required gate has complete, internally consistent, current and reviewable evidence, and it will report `TRIAL_READY = false` without implying authorization, consent, execution or acceptance whenever any required field is absent, pending, expired, revoked, conflicting or lacks accountable approval.

The eight gates are:

1. completed bounded authorization receipt;
2. accepted technical-executor delegation;
3. affirmative manager-participant consent recorded before observation;
4. delegated independent acceptance authority;
5. recorded runtime environment;
6. immutable repository SHA and verified synthetic fixture inventory;
7. aligned synthetic-data-only acknowledgement by authorizer, executor and participant;
8. opened audit/evidence package with custodian, integrity method, access, retention authority/status and disposal accountability.

## Predicted mechanism

A later minimal record should:

- use explicit enumerated states rather than free-text inference;
- require evidence references and accountable timestamps for each gate;
- distinguish `PENDING`, `COMPLETE`, `INVALID`, `EXPIRED`, `REVOKED` and `NOT_APPLICABLE` only where an accountable rule permits it;
- prevent a derived ready state when retention authority remains unassigned or any conflict-control requirement is unresolved;
- separate readiness evidence from technical results and acceptance decisions;
- preserve zero claims of real user value until an authorized trial produces receipts and observed outcomes.

## Predeclared pass conditions for later TEST

H1 passes only if a later built record and validator demonstrate all of the following:

1. the record contains explicit coverage for all `8/8` gates;
2. a fully complete synthetic example derives `TRIAL_READY = true`;
3. removing or invalidating any one required gate independently derives `TRIAL_READY = false` in `8/8` negative cases;
4. `PENDING_APPROVAL`, expired, revoked and conflicting evidence each derive `TRIAL_READY = false`;
5. role overlap without an approved compensating control derives `TRIAL_READY = false`;
6. the record never derives runtime execution, participant acceptance, TTCR improvement or M0.3 completion from readiness alone;
7. no real personal, patient or confidential organizational data is required;
8. all defaults remain non-authorizing and non-executing.

## Predeclared failure conditions

H1 fails if any later implementation:

- can derive `TRIAL_READY = true` with fewer than `8/8` valid gates;
- treats repository ownership, conversation history or template existence as authorization;
- treats technical execution as independent acceptance;
- accepts missing retention authority/status without an accountable approved rule;
- permits unresolved role conflict without compensating review;
- requires collection of real confidential data;
- defaults to an authorized, consented, executed or accepted state;
- conflates readiness with runtime success, user value or milestone completion.

## Inconclusive conditions

The hypothesis remains inconclusive if:

- the later PLAN does not define deterministic derivation rules;
- the BUILD artifact is not available for read-back;
- the validator cannot exercise each gate independently;
- evidence-field applicability remains ambiguous enough that pass/fail cannot be reproduced;
- local legal or institutional review changes the required gate set before testing.

## Scope boundary

This stage does not:

- create or approve an authorization receipt;
- name, recruit or consent a participant;
- delegate an executor or acceptance authority;
- select a retention period;
- execute Obsidian;
- modify the synthetic fixture;
- activate RAG or promote Organizational Memory;
- claim runtime usability, user acceptance, TTCR improvement, CI success or M0.3 completion.

## Test and CI status

No parser, schema validator, Obsidian runtime or manager acceptance test was executed during HYPOTHESIS.

- open pull requests inspected: 0;
- latest pre-run combined status records: 0;
- runtime execution: not performed;
- manager task: not performed;
- user acceptance: not observed;
- CI pass: not claimed.

## Memory layer affected

Engineering-run evidence and issue traceability only.

The external findings remain in Research Staging. Nothing was promoted into Personal/Staff Twin Memory, Person Memory, Role Memory or Organizational Memory/Governed RAG. The synthetic fixture and controlled receipt template were unchanged.

## Risks and blockers

- All eight execution-readiness gates remain incomplete.
- Evidence-retention authority and period remain unassigned.
- Thai institutional HR, ethics, PDPA, records-management and cybersecurity applicability has not been reviewed by an accountable local authority.
- A future deterministic record may require revision if accountable local review changes the minimum gate set.

Accountable owner: repository/product owner or explicitly delegated M0.3 authorizer.

## Stage outcome

```text
ONE_FALSIFIABLE_PROPOSITION_RECORDED = true
EIGHT_READINESS_GATES_INCLUDED = 8/8
PASS_CONDITIONS_PREDECLARED = true
FAIL_CONDITIONS_PREDECLARED = true
INCONCLUSIVE_CONDITIONS_PREDECLARED = true
AUTHORIZED_TRIAL_EXECUTED = false
UNAUTHORIZED_CLAIMS_ADDED = 0
EXTERNAL_FINDINGS_PROMOTED = 0
M0_3_DONE = false
```

## Single next stage

PLAN — define the minimum deterministic schema, state model, derivation rules, negative-case matrix and evidence boundaries for one non-executing consolidated readiness record. The plan must not authorize or execute the trial.