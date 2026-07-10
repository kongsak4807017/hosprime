# HosPrime Loop Engineering 0195 — M0.3 Trial Readiness — REAL PROBLEM

Date: 2026-07-11
Controlling issue: #158
Parent issue: #157
Loop stage completed: REAL PROBLEM
Single next stage: REAL USER

## North Star outcome supported

Protect Trusted Task Completion Rate, evidence quality, user trust, decision-to-outcome traceability and zero unauthorized high-impact action by defining the governance problem that must be resolved before the first legitimate M0.3 Obsidian runtime/user trial.

## Real organizational work problem

A healthcare/public-health manager needs to resume accountable work through a meeting → decision → task/source → lesson chain in a local Personal Twin OS. The repository contains a reviewed, fail-closed receipt contract, but there is no recorded authorization, accountable technical executor, consenting manager participant, delegated acceptance authority or runtime environment.

Therefore the current problem is not a missing graph feature or missing document. The problem is that any trial performed now would lack the evidence needed to distinguish:

- authorized execution from repository access;
- technical operation from real-user acceptance;
- participant consent from assumed availability;
- an observation receipt from a completion claim;
- a synthetic bounded trial from unauthorized use of real personal, staff or patient data.

Without these controls, a successful-looking demonstration could not enter the Trusted Task Completion Rate numerator or denominator and could reduce trust by creating an unsupported execution or acceptance claim.

## Real user and accountable owner

Primary future user:

- a consenting healthcare/public-health manager who must independently navigate the synthetic meeting → decision → task/source → lesson chain.

Accountable governance roles required before execution:

- repository/product owner or explicitly delegated M0.3 authorizer;
- authorized technical executor;
- consenting manager participant;
- delegated acceptance authority independent from the technical execution claim where practicable.

At this REAL PROBLEM stage, these are role requirements only. No person is recruited, named as a participant or treated as authorized by repository ownership alone.

## Verified readiness baseline

```text
CONTRACT_READY = true
TRIAL_READY = false
AUTHORIZED_RUNTIME_TRIALS = 0
AUTHORIZED_MANAGER_TRIALS = 0
REAL_USER_ACCEPTANCE_OBSERVED = false
TRUSTED_TASK_COMPLETION_RATE = NOT_COMPUTABLE
M0_3_DONE = false
UNAUTHORIZED_HIGH_IMPACT_ACTIONS = 0
```

Repository control-state inspection at the start of the run:

- README North Star and Core Rules remained present on `main`;
- controlled release target remained Milestone 0 — Personal Twin OS v0.1;
- M0.3 remained `NEXT` with usable backlinks and graph navigation as the acceptance signal;
- controlling issue #158 was open;
- open pull requests found: 0;
- latest pre-run `main` commit: `b60f170d0a9020799cee8ab12cfa01c2db400f33`;
- combined commit statuses found: 0;
- no CI pass is claimed.

## Measurable readiness target for later stages

The trial may become ready only when the evidence record shows:

```text
AUTHORIZATION_RECEIPT_COMPLETE = true
AUTHORIZED_TECHNICAL_EXECUTOR_RECORDED = true
CONSENTING_MANAGER_PARTICIPANT_RECORDED = true
ACCEPTANCE_AUTHORITY_RECORDED = true
RUNTIME_ENVIRONMENT_RECORDED = true
FIXED_REPOSITORY_SHA_RECORDED = true
SYNTHETIC_DATA_ONLY_SCOPE_CONFIRMED = true
UNAUTHORIZED_HIGH_IMPACT_ACTIONS = 0
```

These are readiness measures only. They do not prove runtime usability, user acceptance, time saved, cost per accepted task or M0.3 completion.

## Exact evidence required before execution

1. Authorization receipt identifying scope, authorizer role, decision, date/time and validity window.
2. Technical-executor record identifying the accountable executor and permitted actions.
3. Participant-consent record for a healthcare/public-health manager, with no consent inferred from employment, repository access or prior conversation.
4. Acceptance-authority record stating who may accept or reject the observed task result.
5. Runtime-environment record including Obsidian version, operating system, relevant core-plugin/settings state and vault path boundary.
6. Fixed repository commit SHA and unchanged synthetic-fixture inventory.
7. Explicit confirmation that no real patient, personal, staff-confidential or organizationally restricted data will be used.
8. Planned audit/receipt location for technical observations, manager task result, acceptance decision and incidents.

## Stop conditions and safety boundary

Stop or defer the trial if any of the following is missing or changes:

- authorization is incomplete, expired, ambiguous or outside scope;
- executor, participant or acceptance authority is not recorded;
- consent is absent or withdrawn;
- the repository SHA or synthetic fixture differs from the authorized scope;
- real confidential data is introduced;
- execution would require access, mutation, publication or a high-impact action outside the receipt;
- technical execution is being represented as user acceptance;
- evidence capture cannot be completed.

Zero-unauthorized-action boundary:

- do not execute Obsidian in this stage;
- do not recruit or identify a participant without consent;
- do not infer authorization from repository ownership;
- do not modify the synthetic fixture;
- do not activate vector memory or RAG;
- do not promote Personal, Person, Role, Research Staging or external findings into Organizational Memory;
- do not claim runtime success, user value, CI success, TTCR improvement or M0.3 completion;
- do not advance M0.4.

## Why this is the bounded real problem

This problem directly blocks the first approved M0.3 task attempt. Resolving it creates a legitimate path to measure TTCR and user trust. Adding agents, screens, notes, templates or unrelated code would not resolve the authorization and accountability deficit.

## Evidence and traceability

- North Star, milestone board, controlled release target and Core Rules: `README.md` on `main`.
- Controlled receipt contract: `docs/testing/M0_3_OBSIDIAN_RUNTIME_TRIAL_RECEIPT_TEMPLATE.yml`.
- Selected successor goal: `engineering_runs/2026-07-11/0194-m0-3-runtime-observation-gate-next-goal.md`.
- Controlling issue: https://github.com/kongsak4807017/hosprime/issues/158
- Parent issue: https://github.com/kongsak4807017/hosprime/issues/157

## Test and CI status

No parser, Obsidian runtime, manager acceptance or product test was executed. Repository state, open issues, open pull requests, latest commit and combined status records were inspected.

- open pull requests: 0;
- combined statuses on pre-run latest commit: none;
- CI pass: not claimed;
- runtime execution: not performed;
- manager trial: not performed;
- user acceptance: not observed.

## Memory layer affected

Engineering-run evidence and issue traceability only. Personal/Staff Twin Memory, Person Memory, Role Memory, Organizational Memory/Governed RAG and Research Staging were not modified or promoted. The synthetic fixture and receipt template were unchanged.

## Risks and blockers

- No complete authorization receipt.
- No recorded authorized technical executor.
- No consenting manager participant.
- No delegated acceptance authority.
- No recorded Obsidian runtime environment.
- No authorized fixed repository SHA for execution.

Accountable owner for resolving the gate: repository/product owner or explicitly delegated M0.3 authorizer.

## Stage outcome

```text
REAL_PROBLEM_DEFINED = true
PROBLEM_TYPE = TRIAL_AUTHORIZATION_AND_ACCOUNTABILITY_GAP
AUTHORIZED_TRIAL_EXECUTED = false
UNAUTHORIZED_CLAIMS_ADDED = 0
MEMORY_PROMOTIONS = 0
M0_3_DONE = false
```

## Single next stage

REAL USER — define the accountable user roles, authority boundaries, consent responsibilities and handoffs required to make the bounded M0.3 synthetic trial ready for authorization.