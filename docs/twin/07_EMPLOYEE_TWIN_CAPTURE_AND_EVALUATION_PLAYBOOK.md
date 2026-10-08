# Employee / Role Twin Capture, Onboarding & Evaluation Playbook

Status: Controlled implementation playbook  
Scope: Staff Twin, Role Twin, Person Overlay, Decision Memory and Agent onboarding  
Depends on: `06_HUMAN_ORGANIZATION_TWIN_AGENT_HARNESS.md`

## 1. Purpose

This playbook defines the practical procedure for converting real employee work into a governed Staff / Role Twin and, only after validation, a bounded AI agent.

The process is:

```text
Select role
-> Define purpose
-> Governance / consent gate
-> Collect approved evidence
-> Map responsibility
-> Map competency
-> Observe workflow
-> Capture decision episodes
-> Build graph
-> Create Role Twin
-> Add Person Overlay
-> Compile Agent Manifest
-> Shadow Mode
-> Evaluate
-> Copilot Mode
-> Approved Agent Mode
-> Monitor / learn / revoke
```

## 2. Principle: capture work, not personality

The capture team should ask:

- What work is this role accountable for?
- What evidence does the person use?
- Which rules and policies apply?
- Which decisions recur?
- Which exceptions require expert judgment?
- Which tools are used?
- Who must be consulted?
- What must be escalated?
- Which outcomes define good work?
- Which knowledge should remain after the person changes role?

Avoid starting with:

- personality imitation;
- writing-style cloning;
- private-message scraping;
- psychological profiling;
- unvalidated "AI knows how this person thinks" claims.

## 3. Stage 0 — Candidate selection

Select a role only if there is a concrete user and measurable work problem.

Recommended first candidates have:

- frequent repetitive knowledge work;
- stable responsibility;
- accessible evidence;
- clear owner;
- measurable baseline;
- low-to-moderate action risk;
- willing subject-matter expert.

Examples:

- TB coordinator;
- quality officer;
- claim reviewer;
- executive secretary;
- HR workforce analyst;
- hospital data analyst;
- procurement documentation officer.

Do not begin with fully autonomous clinical treatment decisions.

## 4. Stage 1 — Twin Charter

Create a Twin Charter before collecting data.

Minimum fields:

```yaml
twin_id:
role_id:
person_id:
business_owner:
technical_owner:
purpose:
primary_tasks:
baseline:
target_metric:
approved_data_sources:
prohibited_sources:
data_classification:
retention:
agent_intent:
maximum_autonomy:
approval_owner:
review_date:
```

Questions:

1. Why is this twin necessary?
2. What user outcome should improve?
3. What is the baseline today?
4. Which evidence may be used?
5. Which information is out of scope?
6. What may the future agent do?
7. What must always remain human?

No charter -> no capture.

## 5. Stage 2 — Governance and consent / lawful-basis gate

Before personal data ingestion:

- identify data controller / owner;
- identify purpose;
- classify data;
- apply minimum-necessary principle;
- establish lawful basis and/or consent where required;
- define retention;
- define access;
- define correction process;
- define person/role separation;
- define offboarding behavior;
- define prohibited inferences.

The employee must be able to distinguish:

```text
Personal Memory
Role Memory
Organizational Memory
Research / External Evidence
```

These are not interchangeable.

## 6. Stage 3 — Source inventory

Create a source register.

Possible source classes:

### Formal organizational sources

- job description;
- appointment orders;
- delegated authority;
- official SOP;
- policy;
- work manual;
- KPI;
- approved workflow;
- committee orders;
- official reports.

### Work-product sources

- reviewed reports;
- templates;
- approved letters;
- dashboards;
- meeting minutes;
- action logs;
- case review records;
- checklists.

### System evidence

- workflow logs;
- task system;
- ERP events;
- HIS events;
- document routing;
- audit events;
- ticketing.

### Interview / observation

- structured interview;
- think-aloud task walkthrough where appropriate;
- expert demonstration;
- exception handling interview;
- retrospective decision review.

Every source should include:

- source owner;
- location;
- classification;
- version;
- date;
- authority;
- review state;
- retention;
- allowed uses.

## 7. Stage 4 — Role and responsibility extraction

Extract the role into a responsibility map.

For each responsibility capture:

```yaml
responsibility_id:
name:
trigger:
inputs:
required_evidence:
steps:
output:
quality_rule:
deadline:
authority:
approver:
escalation:
systems:
risk:
policy_reference:
```

Validate the result with:

- current role holder;
- supervisor / role owner;
- governance owner for high-risk processes.

The role holder alone should not redefine formal authority.

## 8. Stage 5 — Competency mapping

For each skill:

```yaml
skill_id:
skill_name:
domain:
level:
evidence:
validated_by:
confidence:
last_verified:
review_due:
related_responsibilities:
```

Evidence can include:

- validated work products;
- certifications;
- supervisor validation;
- peer validation;
- historical task outcomes;
- training completion.

Do not infer competency from message style.

## 9. Stage 6 — Workflow observation

Document at least three layers:

```text
Formal / Designed Workflow
Observed Workflow
Approved Target Workflow
```

Capture:

- actors;
- handoffs;
- tools;
- waiting;
- rework;
- exceptions;
- failure modes;
- shadow work;
- informal dependencies.

Where event logs are available, use process mining to compare designed and observed paths.

The output must not automatically legitimize unsafe workarounds. Observed behavior is evidence, not policy.

## 10. Stage 7 — Tacit knowledge interview

Use structured prompts.

Examples:

- What usually goes wrong?
- What do new staff misunderstand?
- Which data source do you trust first?
- When do you ignore the default sequence?
- Which exceptions require escalation?
- What early signal tells you a case is becoming risky?
- Who do you consult and why?
- Which apparently correct result is often misleading?
- What do you check before signing off?

Record each heuristic as a candidate knowledge item with:

- source person;
- date;
- applicability;
- evidence;
- confidence;
- review status;
- reviewer.

Tacit knowledge must be promoted before becoming Role Memory.

## 11. Stage 8 — Decision Episode capture

Capture real, reviewed examples.

Minimum schema:

```yaml
decision_id:
role:
timestamp:
situation:
objective:
evidence_considered:
evidence_not_available:
constraints:
options_considered:
selected_option:
rationale:
authority:
approver:
action:
outcome:
uncertainty:
lesson:
reviewed_by:
```

Decision capture is not private chain-of-thought capture.

The system stores externalizable decision rationale, evidence, options and outcome required for accountability.

## 12. Stage 9 — Collaboration and escalation graph

For each recurrent task map:

```text
Actor
-> consults
-> informs
-> hands_off_to
-> requests_approval_from
-> escalates_to
-> receives_data_from
-> supplies_output_to
```

Identify:

- formal approvers;
- informal experts;
- single points of failure;
- critical cross-department dependencies;
- backup roles.

## 13. Stage 10 — Communication preference capture

Collect explicitly declared preferences such as:

- language;
- summary length;
- table vs narrative;
- risk-first vs chronology-first;
- preferred meeting brief structure;
- channel preferences.

Do not silently infer sensitive characteristics.

## 14. Stage 11 — Build Role Twin

Role Twin package should contain:

```text
Role identity
Responsibilities
Authority
Skills required
Approved knowledge
Processes
Tools required
Decision patterns
Escalation
Policies
KPIs
Expected outcomes
Risk controls
```

Role Twin is organizational.

It must remain usable even when no current person is bound.

## 15. Stage 12 — Build Person Overlay

Person Overlay contains only approved person-specific work context.

Possible contents:

- validated expertise;
- assigned projects;
- approved task history;
- reviewed personal lessons;
- declared communication preferences;
- current responsibility variations;
- approved decision episodes.

It must exclude unnecessary personal data.

## 16. Stage 13 — Promotion rules

Candidate information may move between layers only through explicit review.

```text
Personal observation
      |
      | review
      v
Person Work Memory
      |
      | role owner validation
      v
Role Memory
      |
      | governance / knowledge approval
      v
Organizational Memory
```

Store rejected or superseded assertions when useful for audit. Do not overwrite history invisibly.

## 17. Stage 14 — Compile Agent Manifest

The manifest generator reads approved twin artifacts and produces a bounded runtime declaration.

Compilation checks:

- owner exists;
- role exists;
- authority exists;
- source scope exists;
- tool scope exists;
- prohibited actions exist;
- escalation exists;
- privacy classification exists;
- eval suite exists;
- kill switch exists.

If any mandatory field is absent, compilation fails.

## 18. Stage 15 — Agent identity provisioning

Create a unique machine / agent identity.

Required records:

- agent_id;
- sponsor;
- technical owner;
- role binding;
- environment;
- credential type;
- allowed resources;
- allowed tools;
- token lifetime;
- review date;
- revoke procedure.

Never copy a human password, API token or session into the agent.

## 19. Stage 16 — Shadow Mode

The first operational mode is observation and recommendation only.

```text
Same task
   |
   +-- Human performs real work
   |
   +-- Agent independently produces recommendation
   |
   v
Structured comparison
```

Do not let the agent's output alter the real process during initial shadow evaluation unless explicitly designed as a low-risk pilot.

Recommended sample size depends on task frequency and risk. Define it before testing; do not choose a sample size merely to reach a desired result.

## 20. Shadow comparison record

For every case store:

```yaml
case_id:
human_output:
agent_output:
agreement:
critical_difference:
evidence_difference:
policy_difference:
tool_error:
escalation_difference:
reviewer:
severity:
lesson:
```

Important disagreement classes:

- human correct / agent wrong;
- agent correct / human missed evidence;
- both acceptable;
- both wrong;
- insufficient evidence;
- policy conflict;
- escalation required.

## 21. Evaluation framework

Do not score "how much the AI feels like the employee."

### 21.1 Task metrics

- task accuracy;
- completion;
- turnaround time;
- accepted output rate;
- rework.

### 21.2 Evidence metrics

- citation / source coverage;
- provenance completeness;
- unsupported assertion rate;
- stale-evidence rate.

### 21.3 Decision metrics

- agreement with accepted decision;
- severe disagreement rate;
- option coverage;
- rationale traceability;
- outcome linkage.

### 21.4 Safety metrics

- unauthorized tool-call attempt;
- privacy leakage;
- prohibited action attempt;
- policy conflict;
- false approval assumption;
- missed escalation.

### 21.5 Human factors

- user usefulness;
- trust calibration;
- override rate;
- cognitive workload;
- time saved.

### 21.6 Operational metrics

- latency;
- cost;
- tool reliability;
- memory retrieval quality;
- failure recovery;
- audit completeness.

## 22. Error severity

Suggested severity model:

```text
S0 Informational difference
S1 Minor quality difference
S2 Material rework required
S3 High-impact wrong recommendation
S4 Unauthorized / dangerous action attempt
```

Release thresholds must be stricter as impact increases.

Any S4 event should trigger review before autonomy expansion.

## 23. Stage 17 — Copilot Mode

After shadow acceptance, allow user-facing assistance.

Typical Copilot permissions:

- search approved knowledge;
- summarize;
- prepare draft;
- assemble evidence;
- suggest next step;
- prefill a checklist;
- create draft task;
- draft report.

User remains responsible for acceptance.

## 24. Stage 18 — Coordinated Agent Mode

After further evidence, allow bounded workflow coordination.

Examples:

- assign an approved internal task;
- request missing evidence;
- route a draft for approval;
- schedule a review;
- update a controlled workflow state.

All actions remain under deterministic authorization and audit.

## 25. Stage 19 — Execute Approved Workflow

L4 execution is permitted only for workflows where:

- action is pre-approved;
- scope is explicit;
- identity is unique;
- downstream authorization exists;
- rollback / containment exists;
- audit is complete;
- human approval is fresh where required.

L4 does not mean general autonomy.

## 26. Offboarding and role change

When an employee leaves or changes role:

1. freeze person-bound agent privileges;
2. revoke credentials;
3. close active sessions;
4. archive Person Overlay according to policy;
5. review personal-to-role knowledge promotion;
6. transfer only approved Role Memory;
7. re-bind role to new employee if appropriate;
8. re-run authorization;
9. re-run evals for material manifest changes;
10. retain audit history.

## 27. Twin versioning

Version independently:

- Role Twin;
- Person Overlay;
- responsibility map;
- knowledge collection;
- decision memory;
- process model;
- Agent Manifest;
- policy;
- eval suite.

Every agent run should reference exact versions.

## 28. Change control

Material changes requiring revalidation include:

- new tool;
- broader data scope;
- new model class;
- new autonomous action;
- changed authority;
- changed role;
- changed policy;
- new external integration;
- memory source change;
- expansion to patient-level data.

## 29. Interview template

### Role

- What are the five most important responsibilities?
- Which responsibility cannot be delegated?
- What authority is formally assigned?
- Which decisions require approval?

### Evidence

- Which data sources are authoritative?
- Which reports do you distrust and why?
- What freshness is required?

### Process

- Walk through the last real case.
- Where did you wait?
- Where did you rework?
- What exception occurred?

### Decision

- What options did you consider?
- Which evidence changed your decision?
- What made you escalate?
- What outcome would have made the decision wrong?

### Knowledge

- What do experienced staff know that the SOP does not say?
- What mistake do new staff repeat?
- What should the organization remember if you leave tomorrow?

## 30. Minimum pilot deliverables

A single Employee / Role Twin pilot should produce:

1. Twin Charter
2. Source Register
3. Responsibility Map
4. Competency Map
5. Workflow Map
6. Decision Episode dataset
7. Collaboration / Escalation Graph
8. Role Twin
9. Person Overlay
10. Agent Manifest
11. Eval Suite
12. Shadow Run Report
13. Governance Review
14. Go / Hold / Reject decision

## 31. Recommended first pilot

Choose one bounded, evidence-rich, non-autonomous role.

A strong healthcare pilot is a coordinator / analyst role where output is primarily:

- surveillance review;
- evidence synthesis;
- report preparation;
- follow-up tracking;
- escalation.

The initial objective should be:

```text
reduce repetitive knowledge work
while preserving evidence, authority and human approval
```

not "replace the employee."

## 32. Exit criteria for production pilot

The pilot may advance only if:

- measurable user value is demonstrated;
- evidence quality is acceptable;
- no unresolved high-risk privacy issue exists;
- Role Memory / Person Memory separation works;
- agent identity is independent;
- least-privilege tool access is verified;
- approval gates work;
- audit can reconstruct runs;
- kill switch works;
- shadow-mode errors are within approved thresholds;
- role owner and governance owner accept the result.

## 33. Stop conditions

Stop or hold if:

- the business purpose is unclear;
- the employee cannot correct twin data;
- sensitive data scope expands without review;
- source authority is unknown;
- the agent relies on shared credentials;
- critical decisions cannot be audited;
- policy and observed behavior conflict without resolution;
- the team begins optimizing imitation instead of task outcome;
- high-impact actions are enabled before evidence supports them.

## 34. Engineering backlog derived from this playbook

Recommended implementation order:

```text
1. Role Twin schema
2. Person Overlay schema
3. Responsibility graph
4. Decision Episode schema
5. Provenance model
6. Twin Registry API
7. Agent Manifest schema
8. Manifest compiler
9. Agent identity registry
10. Permission / policy engine
11. Tool Gateway
12. Shadow-mode evaluator
13. Audit trace viewer
14. Human approval gateway
15. Kill switch
16. Twin / agent lifecycle UI
```

## 35. North Star alignment

This playbook supports HosPrime's North Star by preserving knowledge continuity while making AI-assisted work evidence-based and accountable.

The core measure remains Trusted Task Completion Rate, supplemented by twin and agent safety metrics.

## 36. Final operating rule

```text
Do not clone the person.
Model the role.
Preserve approved knowledge.
Capture reviewable decisions.
Bind explicit authority.
Compile a manifest.
Run through a harness.
Observe in shadow mode.
Evaluate.
Expand autonomy only with evidence.
```
