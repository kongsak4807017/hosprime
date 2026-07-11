# HosPrime Loop Engineering 0200 — M0.3 Trial Readiness — PLAN

Date: 2026-07-11
Controlling issue: #158
Parent issue: #157
Loop stage completed: PLAN
Single next stage: BUILD

## North Star outcome supported

Protect Trusted Task Completion Rate, evidence quality, user trust, decision-to-outcome traceability and zero unauthorized high-impact action by planning one deterministic, fail-closed, non-executing readiness record for the first bounded M0.3 Obsidian trial.

## Real user and real work problem

The future real user is a consenting healthcare/public-health manager who must independently recover the synthetic meeting → decision → task/source → lesson chain in Obsidian.

The organizational problem is that the repository has a controlled receipt template, accountable-role model, measured `0/8` trial-specific readiness baseline, staged research and a falsifiable hypothesis, but no deterministic consolidated record specification that can be built and tested without implying authorization, consent, execution, acceptance or milestone completion.

## Repository control state inspected

At the start of this run:

- README North Star and Core Rules were read on `main`;
- Milestone 0 — Personal Twin OS v0.1 remained the controlled release target;
- M0.3 remained `NEXT`, requiring usable backlinks and graph navigation;
- issue #158 remained open and controlling;
- engineering runs 0197, 0198 and 0199 preserved BASELINE → RESEARCH → HYPOTHESIS;
- latest pre-run `main` commit was `56e268dce25baa46bd4d81ae839563347c6ce56a`;
- open pull requests found: 0;
- combined status records on the latest pre-run commit: 0;
- no Obsidian runtime execution, manager task, user acceptance, CI pass or M0.3 completion was evidenced.

## Baseline and PLAN target

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

PLAN-stage target:

```text
DETERMINISTIC_SCHEMA_SPECIFIED = true
READINESS_GATES_MAPPED = 8/8
STATE_MODEL_SPECIFIED = true
DERIVATION_RULES_SPECIFIED = true
NEGATIVE_CASES_DEFINED >= 12
EVIDENCE_BOUNDARIES_SPECIFIED = true
DEFAULT_STATE_FAIL_CLOSED = true
UNAUTHORIZED_ACTIONS = 0
EXTERNAL_FINDINGS_PROMOTED = 0
```

## Planned artifact

BUILD will create exactly one non-executing YAML record template:

```text
docs/testing/M0_3_TRIAL_READINESS_RECORD_TEMPLATE.yml
```

The artifact will be a data contract only. It will not authorize a trial, open an execution window, identify a participant, run Obsidian, record acceptance, calculate TTCR or mark M0.3 complete.

## Minimum deterministic schema

The record will contain these top-level groups:

1. `record_control`
   - schema version;
   - record identifier;
   - created/updated timestamps;
   - lifecycle state;
   - controlling issue and milestone;
   - evidence custodian.

2. `scope_boundary`
   - bounded trial purpose;
   - allowed synthetic fixture path;
   - prohibited real/patient/confidential data;
   - prohibited RAG activation and memory promotion;
   - prohibited high-impact actions.

3. `gate_1_authorization`
   - authorizer identity reference;
   - authority basis reference;
   - bounded scope;
   - fixed execution window;
   - approval state, timestamp and evidence reference;
   - revocation state.

4. `gate_2_executor_delegation`
   - executor identity reference;
   - delegated scope;
   - acceptance timestamp;
   - conflict declaration;
   - evidence reference.

5. `gate_3_participant_consent`
   - participant pseudonymous reference;
   - consent version;
   - affirmative consent state and timestamp;
   - withdrawal path;
   - no-coaching acknowledgement;
   - evidence reference.

6. `gate_4_acceptance_authority`
   - acceptance-role identity reference;
   - delegation basis;
   - independence/conflict declaration;
   - compensating control where required;
   - evidence reference.

7. `gate_5_runtime_environment`
   - operating system;
   - Obsidian version;
   - relevant settings/plugins;
   - vault location class;
   - network state;
   - capture method;
   - environment evidence reference.

8. `gate_6_repository_and_fixture`
   - immutable repository commit SHA;
   - fixture root;
   - expected inventory count and hashes;
   - verification state and timestamp;
   - evidence reference.

9. `gate_7_synthetic_scope_acknowledgement`
   - authorizer acknowledgement;
   - executor acknowledgement;
   - participant acknowledgement;
   - alignment check;
   - evidence references.

10. `gate_8_audit_and_evidence_package`
    - package identifier;
    - custodian;
    - integrity method;
    - access restrictions;
    - retention authority;
    - retention status/period;
    - disposal owner and trigger;
    - opened timestamp;
    - evidence reference.

11. `separation_of_duties`
    - role map;
    - overlaps detected;
    - conflict state;
    - compensating-review approval and reference.

12. `derived_readiness`
    - per-gate validity;
    - invalid/pending reasons;
    - deterministic readiness result;
    - evaluated timestamp;
    - evaluator version;
    - explicit non-claims.

## State model

Permitted lifecycle states:

```text
DRAFT
PENDING_REVIEW
APPROVED_NOT_ACTIVE
ACTIVE_WITHIN_WINDOW
REVOKED
EXPIRED
CLOSED
```

Permitted gate evidence states:

```text
MISSING
PENDING
COMPLETE
INVALID
EXPIRED
REVOKED
CONFLICTED
NOT_APPLICABLE
```

Rules:

- defaults are `DRAFT` and `MISSING`;
- `NOT_APPLICABLE` is prohibited for the eight core gates;
- free text cannot override enumerated state;
- expiry or revocation overrides prior completion;
- conflicting evidence cannot be resolved by timestamp recency alone;
- a role overlap is invalid unless an accountable compensating review is complete and referenced.

## Deterministic derivation rules

`TRIAL_READY = true` only when all conditions are true:

```text
record_control.lifecycle_state in [APPROVED_NOT_ACTIVE, ACTIVE_WITHIN_WINDOW]
AND every core gate state = COMPLETE
AND every required evidence_reference is non-empty
AND authorization window is current
AND authorization is not revoked
AND participant consent is current and not withdrawn
AND repository SHA is immutable and fixture verification passes
AND synthetic acknowledgements are aligned across required roles
AND retention authority is assigned
AND evidence package is opened
AND no unresolved role conflict exists
AND no prohibited data/action flag is true
```

Otherwise:

```text
TRIAL_READY = false
```

Readiness must never derive or imply:

```text
TRIAL_EXECUTED
RUNTIME_SUCCESS
MANAGER_TASK_ACCEPTED
TTCR_IMPROVED
TIME_SAVED
M0_3_DONE
```

## Negative-case matrix for later TEST

BUILD and TEST must support at least these independent fail-closed cases:

1. authorization missing;
2. authorization pending;
3. authorization expired;
4. authorization revoked;
5. executor delegation missing;
6. participant consent missing;
7. participant consent withdrawn;
8. acceptance authority missing;
9. unresolved role overlap;
10. runtime environment missing;
11. repository SHA absent or mutable reference used;
12. fixture inventory mismatch;
13. synthetic acknowledgements not aligned;
14. evidence package not opened;
15. retention authority unassigned;
16. evidence reference missing despite `COMPLETE` state;
17. prohibited confidential-data flag true;
18. lifecycle state still `DRAFT`.

Every case must derive `TRIAL_READY = false`. A later complete synthetic example may derive `true` only for validator testing; it must be conspicuously marked `SYNTHETIC_VALIDATOR_EXAMPLE` and must not be usable as a real authorization receipt.

## Evidence boundaries

The planned artifact may store only:

- role or identity references appropriate for a controlled record;
- approval/consent/delegation references;
- timestamps and enumerated states;
- repository and fixture integrity metadata;
- environment metadata;
- audit-package metadata.

It must not store:

- patient data;
- confidential organizational operational data;
- personal health information;
- participant performance conclusions;
- runtime results or acceptance outcomes;
- external research promoted as organizational truth.

Research from run 0198 remains in Research Staging until accountable review. The BUILD artifact will implement a project control contract, not promote external findings into Organizational Memory.

## BUILD acceptance criteria

BUILD passes its own stage boundary only if:

- exactly one YAML template is created;
- all `8/8` gates are represented;
- defaults are non-authorizing, non-consenting and non-executing;
- deterministic states and derived-result placeholders are present;
- explicit non-claim fields are present;
- no real identity, patient or confidential data is included;
- no validator execution, runtime execution or user acceptance is claimed.

## Stop conditions

Stop BUILD and record a blocker if:

- schema fields require unresolved local legal interpretation to be encoded as fact;
- the artifact would imply authorization from repository ownership;
- any default can produce `TRIAL_READY = true`;
- real personal or confidential data would be required;
- scope expands into runtime execution, fixture modification, RAG activation, memory promotion or M0.4.

## Test and CI status

No schema, parser, validator, Obsidian runtime or manager acceptance test was executed during PLAN.

- open pull requests inspected: 0;
- latest pre-run combined status records: 0;
- runtime execution: not performed;
- manager task: not performed;
- user acceptance: not observed;
- CI pass: not claimed.

## Memory layer affected

Engineering-run evidence and issue traceability only.

External findings remain in Research Staging. Nothing was promoted into Personal/Staff Twin Memory, Person Memory, Role Memory or Organizational Memory/Governed RAG. The synthetic fixture and existing runtime-trial receipt template were unchanged.

## Risks and blockers

- All eight trial-specific readiness gates remain incomplete.
- Evidence-retention authority and period remain unassigned.
- Thai institutional HR, ethics, PDPA, records-management and cybersecurity applicability remains pending accountable local review.
- The deterministic schema may require revision after that review.
- A planned contract cannot substitute for a completed authorization receipt or observed user trial.

Accountable owner: repository/product owner or explicitly delegated M0.3 authorizer.

## Stage outcome

```text
DETERMINISTIC_SCHEMA_SPECIFIED = true
READINESS_GATES_MAPPED = 8/8
STATE_MODEL_SPECIFIED = true
DERIVATION_RULES_SPECIFIED = true
NEGATIVE_CASES_DEFINED = 18
EVIDENCE_BOUNDARIES_SPECIFIED = true
DEFAULT_STATE_FAIL_CLOSED = true
AUTHORIZED_TRIAL_EXECUTED = false
UNAUTHORIZED_CLAIMS_ADDED = 0
EXTERNAL_FINDINGS_PROMOTED = 0
M0_3_DONE = false
```

## Single next stage

BUILD — create exactly one non-executing, fail-closed YAML readiness-record template implementing this plan. Do not create a validator, execute Obsidian, recruit a participant, approve retention, promote memory or claim trial readiness.