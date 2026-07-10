# HosPrime Loop Engineering 0198 — M0.3 Trial Readiness — RESEARCH

Date: 2026-07-11
Controlling issue: #158
Parent issue: #157
Loop stage completed: RESEARCH
Single next stage: HYPOTHESIS

## North Star outcome supported

Protect Trusted Task Completion Rate, evidence quality, user trust, decision-to-outcome traceability and zero unauthorized high-impact action by defining the minimum reviewable evidence needed before one synthetic-data-only M0.3 Obsidian usability trial can be authorized.

## Real user and real work problem

The future user is a consenting healthcare/public-health manager who must independently recover the synthetic meeting → decision → task/source → lesson chain in Obsidian.

The real organizational problem is that a governance model exists, but no trial-specific authorization, delegation, consent, runtime or evidence-retention record exists. Without a minimum field contract, an incomplete or ambiguous record could be treated as permission to execute or as evidence of user acceptance.

## Repository control state inspected

At the start of this run:

- README North Star and Core Rules were read on `main`;
- the controlled release target remained Milestone 0 — Personal Twin OS v0.1;
- M0.3 remained `NEXT`, requiring usable backlinks and graph navigation;
- issue #158 remained open and controlling;
- engineering runs 0195, 0196 and 0197 preserved REAL PROBLEM → REAL USER → BASELINE;
- latest pre-run `main` commit was `dc64bc4c70c69a02743a956d06784fe2bdb7ba4d`;
- open pull requests found: 0;
- no runtime execution, manager acceptance, CI pass or M0.3 completion was evidenced.

## Baseline and target metric

Baseline from run 0197:

```text
MODEL_READY = true
EXECUTION_READINESS_GATES_COMPLETE = 0/8
TRIAL_READY = false
AUTHORIZED_RUNTIME_TRIALS = 0
AUTHORIZED_MANAGER_TRIALS = 0
TRUSTED_TASK_COMPLETION_RATE = NOT_COMPUTABLE
```

RESEARCH target:

```text
OFFICIAL_SOURCE_FAMILIES_REVIEWED >= 3
EIGHT_BASELINE_GATES_MAPPED = 8/8
CANDIDATE_AUTHORIZATION_FIELDS_DEFINED = true
CANDIDATE_CONSENT_FIELDS_DEFINED = true
CANDIDATE_DELEGATION_FIELDS_DEFINED = true
CANDIDATE_CONFLICT_CONTROL_FIELDS_DEFINED = true
CANDIDATE_RETENTION_DECISION_RULE_DEFINED = true
EXTERNAL_FINDINGS_PROMOTED = 0
UNAUTHORIZED_ACTIONS = 0
```

## Work completed

Created one bounded Research Staging record:

- `research_staging/2026-07-11/m0-3-trial-authorization-consent-evidence-fields.md`

The record reviewed three official-source families:

1. NIST AI Risk Management Framework 1.0 and NIST AI RMF Playbook;
2. HHS Office for Human Research Protections informed-consent guidance;
3. NIST SP 800-53 Rev. 5 Update 1 audit/accountability controls.

It derived candidate minimum fields for:

- authorization receipt;
- technical-executor delegation;
- participant information and affirmative consent;
- independent acceptance authority;
- separation-of-duties conflicts and compensating review;
- runtime and evidence package;
- retention authority, period and disposal approval.

All eight baseline readiness gates were mapped to later completion evidence.

## Key research findings

### 1. Authorization must be bounded and revocable

A defensible receipt needs a unique trial ID, accountable authorizer, authority basis, purpose, exact approved task, immutable repository SHA, environment, permitted and prohibited actions, validity window, evidence location, stop conditions, decision record and revocation state.

Repository ownership or prior conversation alone is not treated as trial authorization.

### 2. Delegation and acceptance must remain distinct

The technical executor may perform only delegated actions and record technical evidence. Technical operation cannot serve as independent user acceptance.

The acceptance authority needs a recorded scope, validity window, conflict declaration, predeclared criteria and reviewable decision rationale.

### 3. Participant consent must be explicit and evidence-aware

The candidate consent record includes purpose, task, procedures, expected duration, evidence captured, foreseeable privacy/workplace-power risks, expected benefit, confidentiality/access, withdrawal mechanism and the effect of withdrawal on already-created audit evidence.

The HHS source is used only as a conservative design reference. This run does not classify the trial as regulated human-subjects research.

### 4. Role overlap requires a fail-closed compensating control

If authorizer, executor, participant or acceptance roles overlap, trial readiness remains false unless an independent accountable reviewer approves a documented compensating control before execution.

### 5. Retention duration cannot be invented

The reviewed official sources do not establish one universally correct retention period for this repository usability trial. Therefore:

```text
EVIDENCE_RETENTION_AUTHORITY = NOT_ASSIGNED
EVIDENCE_RETENTION_PERIOD = PENDING_APPROVAL
TRIAL_READY = false
```

A later stage may require the accountable organization to select and approve a period under its applicable records, privacy, security, employment and research-governance requirements.

## Provenance

Official sources consulted on 2026-07-11:

- NIST AI Risk Management Framework: https://www.nist.gov/itl/ai-risk-management-framework
- NIST AI RMF Playbook: https://airc.nist.gov/airmf-resources/playbook/
- HHS OHRP informed consent: https://www.hhs.gov/ohrp/regulations-and-policy/guidance/informed-consent/index.html
- NIST SP 800-53 Rev. 5 Update 1: https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final

## Limitations

- NIST AI RMF and Playbook are voluntary guidance and are not Thai law or trial authorization.
- NIST SP 800-53 is a selectable control catalog and does not set one mandatory retention duration for this use case.
- HHS OHRP guidance applies directly only within its regulatory scope; it is used here as a conservative consent-design reference.
- No Thailand-specific legal conclusion was made. Applicable institutional HR, ethics, PDPA, records-management and cybersecurity requirements require accountable local review before a real-person trial.
- All findings remain in Research Staging until reviewed.

## Test and CI status

No parser, product, Obsidian runtime or manager acceptance test was executed during RESEARCH. The work was source review and repository evidence creation only.

- open pull requests: 0;
- runtime execution: not performed;
- manager task: not performed;
- user acceptance: not observed;
- CI pass: not claimed.

## Memory layer affected

Research Staging and engineering-run evidence only.

No external finding was promoted into Personal/Staff Twin Memory, Person Memory, Role Memory or Organizational Memory/Governed RAG. The synthetic fixture and controlled receipt template were unchanged.

## Risks and blockers

- All eight execution-readiness gates remain incomplete.
- No completed authorization receipt, executor delegation, participant consent or acceptance-authority record exists.
- No recorded runtime environment, authorized fixed SHA or opened audit package exists.
- Evidence-retention authority and period remain unassigned.
- Thai institutional applicability has not been reviewed by an accountable local authority.

Accountable owner: repository/product owner or explicitly delegated M0.3 authorizer.

## Stage outcome

```text
OFFICIAL_SOURCE_FAMILIES_REVIEWED = 3
EIGHT_BASELINE_GATES_MAPPED = 8/8
MINIMUM_CANDIDATE_FIELD_GROUPS_DEFINED = 6/6
RETENTION_PERIOD_INVENTED = false
AUTHORIZED_TRIAL_EXECUTED = false
UNAUTHORIZED_CLAIMS_ADDED = 0
EXTERNAL_FINDINGS_PROMOTED = 0
M0_3_DONE = false
```

## Single next stage

HYPOTHESIS — state one falsifiable proposition that a single fail-closed readiness record containing the reviewed candidate fields can represent all eight trial-specific gates without implying authorization, execution, consent or acceptance when any required field is absent.