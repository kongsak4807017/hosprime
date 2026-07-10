# HosPrime Loop Engineering 0196 — M0.3 Trial Readiness — REAL USER

Date: 2026-07-11
Controlling issue: #158
Parent issue: #157
Loop stage completed: REAL USER
Single next stage: BASELINE

## North Star outcome supported

Protect Trusted Task Completion Rate, evidence quality, user trust, decision-to-outcome traceability and zero unauthorized high-impact action by defining the role-level users, authority boundaries, consent responsibilities and handoffs required before the first legitimate M0.3 Obsidian runtime/user trial.

## Real user and real work problem

Primary future user:

- a consenting healthcare/public-health manager who must independently recover the synthetic meeting → decision → task/source → lesson chain in Obsidian for work-continuity evaluation.

The manager is not yet a recruited or identified participant. Employment, repository access, prior conversation, organizational seniority or product ownership must not be interpreted as consent to participate.

The work problem remains that a controlled receipt template exists, but no role-backed chain currently proves who may authorize, execute, participate, accept or stop the trial. Without that separation, technical operation could be mistaken for user acceptance and an unauthorized activity could be counted as a Trusted Task Completion Rate attempt.

## Required accountable role users

### 1. M0.3 authorizer

Accountability:

- approve or reject the bounded synthetic trial scope;
- approve the fixed repository SHA, fixture path, execution window and permitted actions;
- confirm the synthetic-data-only boundary;
- identify or delegate the technical executor and acceptance authority;
- withdraw or suspend authorization when scope or risk changes.

Authority boundary:

- authorization permits only the recorded trial;
- repository ownership alone is not an authorization receipt;
- the authorizer cannot declare runtime success or participant acceptance without the corresponding observed receipts.

Required evidence:

- role or authorized identity reference;
- authorization decision and timestamp;
- approved SHA, fixture, execution window and prohibited actions;
- delegation references where applicable.

### 2. Technical executor

Accountability:

- perform only the authorized preflight and technical observation;
- verify the checked-out SHA and unchanged synthetic fixture;
- record operating system, Obsidian version, plugin/settings state and observed technical results;
- stop immediately when a stop condition is triggered;
- preserve evidence without coaching the manager during the independent task.

Authority boundary:

- may not recruit a participant, infer consent, expand scope, alter the fixture, use real confidential data, activate RAG, promote memory, approve their own technical result as user acceptance or perform high-impact actions.

Required evidence:

- executor role or authorized identity reference;
- permitted-action statement;
- technical observation and attestation;
- incident or blocker receipt when stopped.

### 3. Manager participant

Accountability:

- provide explicit voluntary consent before participation;
- attempt the stated synthetic navigation task within the authorized window;
- report task result, usefulness and acceptance or rejection in their own judgment;
- report confusion, evidence gaps, intervention or safety concerns;
- withdraw consent at any time.

Authority boundary:

- participation does not authorize repository changes, Organizational Memory promotion, RAG activation or high-impact action;
- participant acceptance applies only to the observed bounded task and does not by itself mark M0.3 complete.

Required evidence:

- consent reference;
- authorized participant role;
- task timestamps, duration, transitions and intervention count;
- acceptance or rejection decision with rationale.

### 4. Acceptance authority

Accountability:

- independently review the authorization, fixture, runtime, technical, manager-task and incident/blocker receipts;
- decide whether evidence is accepted for later M0.3 evaluation, rejected with reasons or inconclusive;
- distinguish technical success from user usefulness and governance compliance;
- prevent unsupported milestone or TTCR claims.

Authority boundary:

- cannot replace missing participant consent or missing observed evidence;
- cannot approve work outside the authorization receipt;
- acceptance for evaluation is not M0.3 completion.

Required evidence:

- acceptance-authority role or delegated identity reference;
- reviewed-artifact checklist;
- decision, rationale and review timestamp.

### 5. Evidence custodian / repository recorder

Accountability:

- preserve the receipt package and engineering-run traceability at the authorized repository location;
- ensure records distinguish `NOT_RUN`, `STOPPED`, `INCONCLUSIVE`, technical observation and user acceptance;
- prevent personal or external findings from being promoted into Organizational Memory without review.

Authority boundary:

- recording evidence does not grant authorization, execution authority or acceptance authority;
- must not edit observed results to create a pass claim.

This role may be held by the technical executor only for evidence recording, not for independent acceptance.

## Separation of duties

Minimum required separation:

```text
AUTHORIZER != PARTICIPANT
TECHNICAL_EXECUTOR != PARTICIPANT_DURING_INDEPENDENT_TASK
TECHNICAL_OBSERVATION != USER_ACCEPTANCE
REPOSITORY_RECORDER != AUTOMATIC_ACCEPTANCE_AUTHORITY
```

Preferred separation where practicable:

```text
TECHNICAL_EXECUTOR != ACCEPTANCE_AUTHORITY
```

When preferred separation is not practicable, the conflict and compensating review control must be explicitly recorded before authorization. No separation exception may be inferred after the trial.

## Consent responsibilities

Valid participant consent must be:

- explicit and recorded before execution;
- limited to the synthetic M0.3 task, evidence captured and execution window;
- voluntary and withdrawable;
- clear that no real patient, personal, staff-confidential or restricted organizational data is permitted;
- clear that participation is not organizational approval of HosPrime or M0.3 completion.

Consent is invalid or insufficient when inferred from employment, hierarchy, repository ownership, previous messages, meeting attendance or general interest in the project.

## Role handoff sequence

```text
1. Authorizer defines bounded scope and delegations
2. Evidence custodian opens a draft receipt package
3. Technical executor records preflight without running outside scope
4. Manager participant provides explicit consent
5. Authorizer confirms all readiness evidence and changes status only to AUTHORIZED_NOT_RUN
6. Technical executor performs the authorized technical observation
7. Manager participant performs the independent task without coaching
8. Evidence custodian records receipts and incidents
9. Acceptance authority independently reviews the complete package
10. Later EVALUATE stage determines TTCR eligibility and milestone implications
```

A missing or out-of-order handoff is a stop/defer condition, not permission to improvise.

## Verified current baseline

```text
ACCOUNTABLE_ROLE_MODEL_DEFINED = false -> true in this engineering evidence
NAMED_OR_AUTHORIZED_AUTHOR = false
AUTHORIZED_TECHNICAL_EXECUTOR_RECORDED = false
CONSENTING_MANAGER_PARTICIPANT_RECORDED = false
ACCEPTANCE_AUTHORITY_RECORDED = false
RUNTIME_ENVIRONMENT_RECORDED = false
AUTHORIZED_RUNTIME_TRIALS = 0
AUTHORIZED_MANAGER_TRIALS = 0
REAL_USER_ACCEPTANCE_OBSERVED = false
TRUSTED_TASK_COMPLETION_RATE = NOT_COMPUTABLE
UNAUTHORIZED_HIGH_IMPACT_ACTIONS = 0
M0_3_DONE = false
```

The role model is now defined, but no real person is named, recruited, consented, delegated or treated as authorized.

Repository control-state inspection at the start of the run:

- README North Star and Core Rules remained present on `main`;
- controlled release target remained Milestone 0 — Personal Twin OS v0.1;
- M0.3 remained `NEXT` with usable backlinks and graph navigation as its acceptance signal;
- controlling issue #158 remained open;
- open pull requests found: 0;
- latest pre-run `main` commit: `a8cc64763144de6208dc6ca2560ec6e1c45d8c18`;
- combined status records on that commit: 0;
- no CI pass is claimed.

## Measurable target for the next BASELINE stage

Measure role-readiness coverage against the defined contract:

```text
REQUIRED_ACCOUNTABLE_ROLE_CLASSES = 5
ROLE_CLASS_DEFINITIONS_COMPLETE_TARGET = 5/5
AUTHORITY_BOUNDARIES_COMPLETE_TARGET = 5/5
REQUIRED_HANDOFFS_DEFINED_TARGET = 10/10
CONSENT_RULES_DEFINED_TARGET = PASS
SEPARATION_OF_DUTIES_RULES_DEFINED_TARGET = PASS
ACTUAL_AUTHORIZATION_RECEIPTS_COMPLETE = 0 until observed
UNAUTHORIZED_HIGH_IMPACT_ACTIONS = 0
```

This target measures the readiness model only. It does not claim an authorized trial, runtime usability, user acceptance, time saved, cost per accepted task or M0.3 completion.

## Stop conditions and zero-unauthorized-action boundary

Stop or defer when:

- any accountable role is absent, ambiguous or outside delegated authority;
- participant consent is absent, incomplete or withdrawn;
- technical executor and participant independence cannot be maintained;
- acceptance authority has an undisclosed conflict without a compensating review control;
- authorized SHA, fixture, environment, execution window or evidence location is missing or changes;
- real confidential data appears;
- requested activity includes fixture mutation, RAG activation, memory promotion, publication or high-impact action;
- evidence capture fails or technical observation is being represented as user acceptance.

No Obsidian runtime, participant recruitment, fixture mutation, RAG activation, Organizational Memory promotion or high-impact action occurred in this stage.

## Evidence and traceability

- North Star, milestone board, controlled release target and Core Rules: `README.md` on `main`.
- Real-problem evidence: `engineering_runs/2026-07-11/0195-m0-3-trial-readiness-real-problem.md`.
- Controlled receipt contract: `docs/testing/M0_3_OBSIDIAN_RUNTIME_TRIAL_RECEIPT_TEMPLATE.yml`.
- Controlling issue: https://github.com/kongsak4807017/hosprime/issues/158
- Parent issue: https://github.com/kongsak4807017/hosprime/issues/157

## Test and CI status

No parser, Obsidian runtime, manager acceptance or product test was executed. Repository state, controlling issue, open issues, open pull requests, latest commit and combined status records were inspected.

- open pull requests: 0;
- combined statuses on pre-run latest commit: none;
- CI pass: not claimed;
- runtime execution: not performed;
- manager trial: not performed;
- user acceptance: not observed.

## Memory layer affected

Engineering-run evidence and issue traceability only. Personal/Staff Twin Memory, Person Memory, Role Memory, Organizational Memory/Governed RAG and Research Staging were not modified or promoted. The synthetic fixture and controlled receipt template were unchanged.

## Risks and blockers

- No completed authorization receipt.
- No recorded authorized technical executor.
- No consenting manager participant.
- No delegated acceptance authority.
- No recorded runtime environment.
- No authorized fixed repository SHA or execution window.
- Independent acceptance separation may require an explicit compensating control if staffing is limited.

Accountable owner for resolving the gate: repository/product owner or explicitly delegated M0.3 authorizer.

## Stage outcome

```text
REAL_USER_ROLE_MODEL_DEFINED = true
ROLE_CLASSES_DEFINED = 5/5
REAL_PARTICIPANT_RECRUITED = false
CONSENT_OBTAINED = false
AUTHORIZATION_GRANTED = false
AUTHORIZED_TRIAL_EXECUTED = false
UNAUTHORIZED_CLAIMS_ADDED = 0
MEMORY_PROMOTIONS = 0
M0_3_DONE = false
```

## Single next stage

BASELINE — measure current trial-readiness coverage against the defined role, consent, separation-of-duties, authorization, environment and handoff requirements without recruiting a participant or executing Obsidian.