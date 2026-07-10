# Research Staging — M0.3 Trial Authorization, Consent and Evidence Fields

Date reviewed: 2026-07-11
Controlling issue: #158
Loop stage: RESEARCH
Status: **STAGED — NOT ORGANIZATIONAL POLICY**

## Research question

What is the minimum defensible evidence content needed before authorizing one bounded, synthetic-data-only M0.3 Obsidian usability trial involving a healthcare/public-health manager, a technical executor and an independent acceptance authority?

This research does **not** determine that the activity is human-subjects research, does not provide legal advice, and does not itself authorize execution.

## Scope and baseline

Current execution-readiness baseline from engineering run 0197:

```text
EXECUTION_READINESS_GATES_COMPLETE = 0/8
TRIAL_READY = false
AUTHORIZED_RUNTIME_TRIALS = 0
AUTHORIZED_MANAGER_TRIALS = 0
TRUSTED_TASK_COMPLETION_RATE = NOT_COMPUTABLE
```

The target of this research is a minimum field set that can later be reviewed and converted into a bounded authorization/receipt mechanism. It is not to execute the trial or collect participant data.

## Official sources reviewed

### 1. NIST AI Risk Management Framework 1.0 and Playbook

Official sources:

- https://www.nist.gov/itl/ai-risk-management-framework
- https://airc.nist.gov/airmf-resources/playbook/

Relevant use:

- AI risk management should cover risks to individuals and organizations across design, development, use and evaluation.
- The Playbook organizes suggested actions under Govern, Map, Measure and Manage.
- The guidance is voluntary and must be tailored to the use case; it is not a universal checklist.

Practical implication for M0.3:

- record accountable roles and authority boundaries;
- record intended use, prohibited use and affected user;
- predefine measurable outcomes and stop conditions;
- preserve an audit trail showing who authorized, executed, observed, accepted or rejected the result.

### 2. HHS Office for Human Research Protections — informed-consent guidance

Official source:

- https://www.hhs.gov/ohrp/regulations-and-policy/guidance/informed-consent/index.html

Relevant use:

The M0.3 usability trial is not being classified here as regulated human-subjects research. However, OHRP informed-consent guidance provides a conservative reference for participant-facing clarity: purpose, procedures, foreseeable risks or discomforts, expected benefits, confidentiality, contacts and voluntary participation.

Practical implication for M0.3:

- use plain-language participation information;
- record affirmative consent before observation;
- state that participation can be stopped without penalty;
- define what evidence will be captured, who can access it and how withdrawal affects already-created records;
- avoid collecting health, patient or confidential organizational information.

### 3. NIST SP 800-53 Rev. 5 Update 1 — audit and accountability controls

Official source:

- https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final

Relevant use:

SP 800-53 provides a control catalog for security and privacy, including audit-event definition, audit-record content, review, protection and organization-defined retention. It does not prescribe one universal retention duration for this trial.

Practical implication for M0.3:

- define the events that must be recorded before execution;
- include identity/role, timestamp, action, target repository SHA/environment and result;
- protect records from untracked modification;
- assign an evidence custodian and an organization-approved retention/disposal rule rather than inventing a duration during this stage.

## Minimum trial-specific evidence field set

The following is a research-derived candidate field set for later review. No field is considered approved organizational policy yet.

### A. Authorization receipt

Required candidate fields:

1. unique trial ID;
2. authorizer name or accountable role identifier;
3. basis and boundary of authority;
4. approved purpose and approved target task;
5. authorized repository and immutable commit SHA;
6. authorized fixture inventory and hash/read-back result;
7. authorized runtime/device/vault boundary;
8. permitted actions;
9. explicitly prohibited actions;
10. start and expiry time;
11. evidence-capture location and custodian;
12. stop conditions;
13. authorizer decision, timestamp and reviewable signature/approval record;
14. revocation method and revocation status.

### B. Technical-executor delegation

Required candidate fields:

1. executor identity and role;
2. delegated actions and non-delegable decisions;
3. repository SHA/environment accepted by executor;
4. no-fixture-mutation and synthetic-data-only acknowledgement;
5. evidence-capture duties;
6. incident/escalation path;
7. execution-window acknowledgement;
8. executor acceptance and timestamp.

The executor cannot self-approve user acceptance merely because the runtime works technically.

### C. Participant information and consent

Required candidate fields:

1. participant role category, using the minimum identity needed for the evidence purpose;
2. purpose of the usability task;
3. exact task and expected duration;
4. procedures and what assistance is or is not permitted;
5. evidence captured, including screen/notes/timestamps if applicable;
6. foreseeable privacy, confidentiality and workplace-power risks;
7. expected direct benefit, including an explicit statement when none is guaranteed;
8. synthetic-data-only boundary;
9. who can access the evidence;
10. retention/disposal rule or pending-authority status;
11. voluntary participation and stop/withdraw mechanism;
12. consequence of withdrawal for already-created audit evidence;
13. contact/escalation route;
14. affirmative consent, timestamp and version of the information shown.

### D. Independent acceptance authority

Required candidate fields:

1. acceptance authority identity/role;
2. delegated acceptance scope;
3. conflict-of-interest declaration;
4. independence from technical execution, or documented compensating review;
5. predeclared acceptance/rejection criteria;
6. authority validity window;
7. decision and rationale fields;
8. signature/approval record and timestamp.

### E. Separation-of-duties and conflict control

Required candidate fields:

1. role-to-person assignment matrix;
2. detected role overlaps;
3. conflict description;
4. why separation is infeasible, if applicable;
5. compensating reviewer identity and authority;
6. actions the conflicted person cannot approve;
7. independent evidence reviewed;
8. conflict-control approval and timestamp.

Minimum fail-closed rule:

```text
If the executor is also the authorizer, participant, or acceptance authority,
trial readiness remains false unless an independent accountable reviewer
approves a documented compensating control before execution.
```

### F. Runtime and evidence package

Required candidate fields:

1. operating system and version;
2. Obsidian version;
3. enabled core/community plugins relevant to the observation;
4. graph/backlink settings affecting visibility;
5. vault path or non-sensitive environment identifier;
6. repository SHA and fixture inventory;
7. trial start/end timestamps;
8. required audit events and receipt filenames;
9. evidence custodian;
10. integrity/read-back method;
11. access list;
12. retention authority, retention period or explicit `PENDING_APPROVAL`;
13. disposal method and accountable approver;
14. incident/blocker record.

## Mapping to the eight baseline gates

| Baseline gate | Minimum evidence needed to count complete later |
|---|---|
| Authorization receipt | Section A completed, valid and reviewable |
| Authorized technical executor | Section B completed and accepted |
| Consenting manager participant | Section C completed before observation |
| Delegated acceptance authority | Section D completed before task evaluation |
| Runtime environment | Section F fields 1–5 recorded |
| Fixed SHA and fixture inventory | Sections A/F identify immutable SHA and verified inventory |
| Synthetic-data-only confirmation | Authorizer, executor and participant acknowledgements align |
| Opened audit/evidence package | Section F fields 7–14 assigned before execution |

## Retention conclusion

No authoritative source reviewed establishes a single correct retention period for this bounded repository usability trial. Therefore this stage must not invent one.

Required fail-closed state:

```text
EVIDENCE_RETENTION_AUTHORITY = NOT_ASSIGNED
EVIDENCE_RETENTION_PERIOD = PENDING_APPROVAL
TRIAL_READY = false
```

A later PLAN or BUILD stage may include a field requiring the accountable organization to choose and approve a retention period consistent with its records, privacy, security and employment policies.

## Limitations and applicability

- NIST AI RMF and its Playbook are voluntary risk-management guidance, not Thai law and not trial authorization.
- NIST SP 800-53 is a control catalog; applicability and retention duration must be selected by the accountable organization.
- HHS OHRP guidance applies directly to activities governed as human-subjects research under its jurisdiction. It is used here only as a conservative consent-design reference; this document makes no research-classification determination.
- No Thailand-specific legal conclusion was made in this run. Before any real-person trial within a Thai public-health organization, the accountable owner should confirm applicable institutional HR, research ethics, PDPA, records-management and cybersecurity requirements.
- External findings remain in Research Staging until an explicit review record approves their use.

## Research-stage decision

The minimum evidence content is now sufficiently bounded to support a falsifiable HYPOTHESIS about whether one consolidated fail-closed readiness record can cover all eight gates without implying authorization.

No participant was identified or recruited. No runtime was executed. No consent, delegation or authorization is claimed. No external finding was promoted into Personal/Staff Twin Memory, Person Memory, Role Memory or Organizational Memory/Governed RAG.
