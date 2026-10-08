# SOP — Employee / Role Twin to Governed AI Agent Production Pipeline

Document ID: HOSPRIME-SOP-TWIN-AGENT-001  
Version: 1.0  
Status: Production Pilot SOP  
Owner: HosPrime Product + AI Governance  
Scope: Employee Selection -> Approved Agent Mode  
Related architecture:
- docs/twin/06_HUMAN_ORGANIZATION_TWIN_AGENT_HARNESS.md
- docs/twin/07_EMPLOYEE_TWIN_CAPTURE_AND_EVALUATION_PLAYBOOK.md

## 1. Purpose

This SOP defines the operational procedure for converting a real organizational role and approved person-specific work knowledge into a governed AI Copilot / Agent.

The pipeline is:

~~~text
01 Employee Selection
-> 02 Role Discovery
-> 03 Data Consent / Governance
-> 04 Knowledge Collection
-> 05 Workflow Observation
-> 06 Process Mining
-> 07 Decision Capture
-> 08 Skill Graph
-> 09 Knowledge Graph
-> 10 Role Twin
-> 11 Person Overlay
-> 12 Agent Manifest
-> 13 Agent Harness
-> 14 Shadow Mode
-> 15 Evaluation
-> 16 Copilot Mode
-> 17 Approved Agent Mode
~~~

No stage may be skipped solely for speed.

## 2. Operating Principles

1. Model work, responsibility, evidence and authority — not a whole personality.
2. Keep Role Memory and Person Memory separate.
3. No evidence -> no factual organizational claim.
4. No identity -> no access.
5. No explicit permission -> no tool action.
6. No required human approval -> no high-impact action.
7. No audit record -> action is not considered valid.
8. Observed behavior is evidence, not automatically approved policy.
9. Every persistent memory write needs provenance and review state.
10. Autonomy expands only after measured evidence.

## 3. Core Roles

- Executive Sponsor — authorizes business use case and resources.
- Role Owner — accountable for the organizational role being modeled.
- Employee / Subject-Matter Expert (SME) — contributes real work knowledge.
- Product Owner — owns scope, baseline and outcome.
- Process Analyst — maps designed and observed workflows.
- Knowledge Engineer — builds knowledge structures and provenance.
- Data Steward — validates data sources, definitions and quality.
- DPO / Privacy Officer — reviews personal-data use and privacy controls.
- Legal / Compliance — reviews regulatory and policy constraints.
- Security / IAM — owns agent identity, secrets and authorization.
- AI Engineer — implements model, retrieval, tools and orchestration.
- Evaluation Lead — owns test set, metrics and release evidence.
- AI Governance Committee — approves risk class and deployment state.
- Internal Audit / Quality — independently reviews evidence where required.

## 4. Required State Machine

~~~text
CANDIDATE
-> DISCOVERED
-> GOVERNANCE_CLEARED
-> KNOWLEDGE_CAPTURED
-> WORKFLOW_OBSERVED
-> PROCESS_MODELED
-> DECISION_MODEL_READY
-> SKILL_GRAPH_READY
-> KNOWLEDGE_GRAPH_READY
-> ROLE_TWIN_READY
-> PERSON_OVERLAY_READY
-> MANIFEST_READY
-> HARNESS_READY
-> SHADOW
-> EVALUATED
-> COPILOT
-> APPROVED_AGENT
-> SUSPENDED / RETIRED
~~~

A system administrator must not manually mark a stage complete without the required evidence artifact.

# 01 Employee Selection

## Objective

Select one employee/role where AI assistance has measurable organizational value and an acceptable initial risk.

## Entry criteria

- identifiable work problem;
- identifiable role owner;
- measurable current baseline;
- accessible evidence;
- willing SME or alternative authoritative evidence source.

## Procedure

1. Define the exact work problem.
2. Identify the organizational role, not just the employee name.
3. Record current workload, turnaround time, error/rework, backlog or other baseline.
4. Identify the expected AI-assisted tasks.
5. Classify impact:
   - informational;
   - operational support;
   - consequential/high-impact.
6. Identify affected stakeholders.
7. Identify whether patient, employee, financial, procurement or other restricted data may be involved.
8. Estimate expected benefit and failure consequence.
9. Select a pilot only if value can be measured and governance is feasible.

## Required artifact

Twin Charter:

~~~yaml
twin_id:
role_id:
candidate_person_id:
business_owner:
role_owner:
problem_statement:
baseline:
target_outcome:
initial_scope:
out_of_scope:
data_classes:
expected_agent_mode:
maximum_autonomy:
review_date:
~~~

## Exit gate G01

Role Owner + Product Owner approve the Twin Charter.

## Stop conditions

- no accountable owner;
- no measurable problem;
- unclear benefit;
- unacceptable privacy or safety risk;
- purpose is primarily surveillance or personality imitation.

# 02 Role Discovery

## Objective

Create the canonical organizational description of the role independent of the current employee.

## Inputs

- Twin Charter;
- job description;
- appointment/delegation orders;
- SOP;
- RACI;
- KPI;
- committee assignments;
- official workflow;
- supervisor interview.

## Procedure

1. List formal responsibilities.
2. List delegated authorities.
3. Identify actions that require approval.
4. Identify prohibited actions.
5. Map recurring tasks.
6. Map decision points.
7. Map required evidence.
8. Map upstream/downstream handoffs.
9. Map escalation paths.
10. Compare written role with actual work.
11. Mark differences as:
    - formal;
    - local practice;
    - exception;
    - unresolved conflict.
12. Resolve authority conflicts with the Role Owner / governance body.

## Required artifact

Role Contract:

~~~yaml
role_id:
purpose:
responsibilities:
authority:
required_approvals:
prohibited_actions:
kpis:
inputs:
outputs:
systems:
escalations:
policies:
~~~

## Exit gate G02

Role Owner confirms that the Role Contract reflects current authorized work.

# 03 Data Consent / Governance

## Objective

Establish lawful, ethical and organizational permission to collect and use data for the Twin/Agent.

## Procedure

1. Create a personal-data and organizational-data inventory.
2. For each source record:
   - owner;
   - purpose;
   - classification;
   - lawful/organizational basis;
   - access group;
   - retention;
   - allowed use;
   - prohibited use.
3. Apply data minimization.
4. Separate:
   - Personal Memory;
   - Person Work Memory;
   - Role Memory;
   - Organizational Memory;
   - Research Staging.
5. Define whether employee consent is required or whether another valid organizational/legal basis applies; DPO/Legal must decide rather than assuming consent is always the correct basis.
6. Prepare or update privacy notice where applicable.
7. Define correction and challenge process for the employee.
8. Define deletion/archive/offboarding rules.
9. Define sensitive inference prohibitions.
10. Define model-provider/data-transfer boundaries.
11. Record the governance decision.

## Required artifacts

- Data Register
- Privacy / Governance Assessment
- Access Matrix
- Retention Matrix
- Data Processing Decision Record

## Exit gate G03

DPO/Privacy + Role Owner + Security approve the intended data scope.

## Stop conditions

- source collected for an incompatible purpose without review;
- excessive personal data;
- unknown source ownership;
- unclear retention;
- unrestricted ingestion of email/chat;
- hidden psychological or sensitive profiling.

# 04 Knowledge Collection

## Objective

Collect explicit and approved tacit knowledge required to perform the role.

## Source classes

- policies;
- SOPs;
- guidelines;
- job aids;
- templates;
- official reports;
- meeting decisions;
- training materials;
- validated examples;
- expert interview;
- approved lessons learned.

## Procedure

1. Create Source Register.
2. Assign each source:
   - source_id;
   - authority;
   - owner;
   - version;
   - date;
   - classification;
   - review status;
   - expiry/review date.
3. Remove duplicates and obsolete copies.
4. Mark conflicting sources.
5. Interview SME using task-based questions.
6. Capture tacit knowledge as candidate knowledge, not truth.
7. Require review before candidate tacit knowledge becomes Role Memory.
8. Chunk/index only approved sources for production retrieval.
9. Keep unreviewed research in Research Staging.

## Required artifacts

- Source Register
- Approved Knowledge Corpus
- Conflict Register
- Tacit Knowledge Candidate Register

## Exit gate G04

Knowledge Owner/Data Steward confirm authority and provenance of production knowledge.

# 05 Workflow Observation

## Objective

Understand how work is actually performed.

## Procedure

1. Select representative normal cases and exception cases.
2. Observe the employee performing the task.
3. Record:
   - trigger;
   - steps;
   - evidence used;
   - systems;
   - handoffs;
   - waits;
   - rework;
   - decision points;
   - exceptions;
   - outcome.
4. Use task walkthrough / think-aloud only where appropriate and non-intrusive.
5. Compare observed process with SOP.
6. Mark workarounds and shadow processes.
7. Do not promote a workaround into approved policy automatically.
8. Validate the observation map with the worker and process owner.

## Required artifact

Observed Workflow Map.

## Exit gate G05

Process Owner accepts the distinction between Designed, Observed and Approved workflows.

# 06 Process Mining

## Objective

Use event data to validate workflow patterns, bottlenecks and process variants.

## Minimum event schema

~~~text
case_id
activity
timestamp
actor_or_role
system
status
outcome
source_event_id
~~~

## Procedure

1. Identify event-producing systems.
2. Build event dictionary.
3. Validate case-id logic.
4. Validate timestamp quality.
5. Normalize activity names.
6. Reconstruct process variants.
7. Quantify:
   - throughput time;
   - waiting;
   - rework;
   - loops;
   - handoffs;
   - abandonment;
   - exception frequency.
8. Compare process-mining output to observed workflow.
9. Investigate discrepancies.
10. Tag process variants as:
    - approved;
    - tolerated exception;
    - unsafe;
    - unknown.
11. Submit unresolved variants to Process Owner.

## Required artifacts

- Event Dictionary
- Process Model
- Variant Register
- Bottleneck Baseline

## Exit gate G06

Process Owner confirms which process path the Twin/Agent is expected to support.

# 07 Decision Capture

## Objective

Capture reviewable decision structure without attempting to collect private chain-of-thought.

## Decision Episode schema

~~~yaml
decision_id:
role_id:
situation:
objective:
evidence_considered:
evidence_missing:
constraints:
options_considered:
selected_option:
externalizable_rationale:
authority:
approver:
action:
outcome:
uncertainty:
lesson:
reviewed_by:
~~~

## Procedure

1. Select recurring and high-value decision types.
2. Collect historical reviewed cases.
3. Ask the SME what evidence was decisive.
4. Record options that were genuinely available.
5. Record policy constraints.
6. Record required approvals.
7. Record outcome if known.
8. Tag hindsight bias and unknowns.
9. Review with Role Owner.
10. Store rationale as accountable business reasoning, not hidden internal thought.

## Required artifact

Decision Episode Dataset.

## Exit gate G07

Role Owner validates the decision schema and sample episodes.

# 08 Skill Graph

## Objective

Represent capabilities required by the role and validated capabilities of the person.

## Procedure

1. Derive required skills from responsibilities.
2. Decompose broad skills into observable competencies.
3. Link each competency to evidence.
4. Record level and validator.
5. Link skill to responsibility/process.
6. Record review date.
7. Identify skill gaps.
8. Separate:
   - Role-required skill;
   - Person-validated skill.
9. Do not infer skill from communication style alone.

## Required artifact

Skill Graph.

## Example

~~~text
Role -> requires_skill -> TB cohort analysis
Person -> validated_skill -> TB cohort analysis
Skill -> supported_by -> reviewed report / certificate / outcome
~~~

## Exit gate G08

Role Owner validates required skills; designated validator confirms person-specific assertions.

# 09 Knowledge Graph

## Objective

Connect people, roles, work, evidence, decisions, policies and outcomes into a provenance-aware graph.

## Minimum nodes

~~~text
Person
Role
Department
Responsibility
Skill
KnowledgeArtifact
Process
Task
Decision
Evidence
Policy
KPI
Tool
Agent
Approval
Outcome
Lesson
~~~

## Procedure

1. Establish canonical identifiers.
2. Create controlled relationship types.
3. Load only governed assertions.
4. Attach provenance to material edges.
5. Add valid-from / valid-to where required.
6. Represent conflicts rather than overwriting them.
7. Link decisions to evidence and outcomes.
8. Link roles to authority and escalation.
9. Run orphan-node and provenance checks.
10. Validate graph with domain experts.

## Required artifact

Governed Knowledge Graph v1.

## Exit gate G09

Knowledge/Data Governance approves graph schema and provenance completeness.

# 10 Role Twin

## Objective

Create a versioned organizational twin of the role that remains usable when the employee changes.

## Build content

- role identity;
- responsibilities;
- authority;
- required skills;
- approved knowledge;
- process;
- decision patterns;
- tools required;
- escalation;
- policies;
- KPIs;
- expected outcomes;
- risk controls.

## Procedure

1. Compile role-level artifacts from G02-G09.
2. Remove person-specific material unless it has been formally promoted to Role Memory.
3. Validate authority.
4. Validate current policies.
5. Assign owner/version.
6. Run completeness checks.
7. Publish Role Twin candidate.
8. Obtain Role Owner sign-off.

## Exit gate G10

Role Twin is independently valid without a Person Overlay.

# 11 Person Overlay

## Objective

Bind approved person-specific work context to the Role Twin without contaminating organizational Role Memory.

## Allowed examples

- current assignments;
- validated expertise;
- approved historical cases;
- reviewed personal lessons;
- declared communication preferences;
- current projects;
- temporary delegations.

## Procedure

1. Create Person Overlay with its own identifier/version.
2. Link to Role Twin; do not merge storage blindly.
3. Classify every field.
4. Define visibility.
5. Define expiry / offboarding behavior.
6. Allow correction/challenge.
7. Test unbinding:
   - remove Person Overlay;
   - verify Role Twin still works.
8. Test role change:
   - bind person to new role;
   - ensure previous role permissions do not follow automatically.

## Exit gate G11

Privacy + Role Owner confirm separation and lifecycle behavior.

# 12 Agent Manifest

## Objective

Compile approved twin artifacts into an explicit, machine-readable runtime contract.

## Mandatory fields

~~~yaml
agent_id:
version:
owner:
sponsor:
role_twin:
person_overlay:
mission:
objectives:
knowledge_scope:
data_scope:
tools:
permissions:
prohibited_actions:
autonomy_level:
approval_rules:
escalation:
model_policy:
memory_policy:
audit_policy:
eval_suite:
kill_switch:
expiry_or_review_date:
~~~

## Procedure

1. Generate manifest from approved artifacts.
2. Resolve all references to exact versions.
3. Deny unspecified tools by default.
4. Deny unspecified data by default.
5. Encode prohibited actions.
6. Encode approval rules.
7. Encode escalation.
8. Encode max steps/time/cost.
9. Sign/version manifest.
10. Run fail-closed validation.

## Exit gate G12

Manifest compiler returns VALID and governance owner approves version.

# 13 Agent Harness

## Objective

Place deterministic controls around the model.

## Mandatory components

~~~text
Unique Agent Identity
Instruction Builder
Context Builder
Memory Boundary
Governed Retrieval
Tool / MCP Gateway
Policy Engine
Permission Engine
Input Guardrails
Output Guardrails
Tool Guardrails
Human Approval Gateway
Sandbox
Step / Time / Cost Limits
Audit / Trace
Monitoring
Kill Switch / Revocation
~~~

## Procedure

1. Provision unique nonhuman agent identity.
2. Bind manifest to identity.
3. Configure short-lived/scoped authorization.
4. Configure retrieval allowlist.
5. Configure tool allowlist.
6. Implement per-tool/per-action authorization.
7. Configure approval interrupts.
8. Configure output validation/redaction.
9. Configure sandbox/egress boundary.
10. Configure resource limits.
11. Enable full trace correlation.
12. Test disable, credential revoke and tool revoke.
13. Test failure behavior.
14. Ensure downstream systems re-authorize consequential actions.

## Exit gate G13

Security + AI Governance sign Harness Readiness Report.

# 14 Shadow Mode

## Objective

Run the agent on real or representative work without allowing it to become the authoritative operator.

## Procedure

1. Freeze Agent Manifest version for the trial.
2. Define trial period and case mix before evaluation.
3. Include normal and exception cases.
4. Human performs the real task.
5. Agent independently produces output/recommendation.
6. Do not expose agent output to the operator until required by study design.
7. Compare:
   - answer;
   - evidence;
   - action;
   - escalation;
   - policy;
   - outcome prediction.
8. Record disagreements.
9. Classify error severity.
10. Root-cause significant errors.
11. Update twin/knowledge/harness only through controlled change.
12. Re-run affected tests after change.

## Shadow record

~~~yaml
case_id:
manifest_version:
human_output:
agent_output:
agreement:
critical_difference:
evidence_difference:
policy_difference:
tool_error:
escalation_difference:
severity:
reviewer:
root_cause:
corrective_action:
~~~

## Exit gate G14

Evaluation Lead confirms the shadow dataset is representative enough for the approved risk class.

# 15 Evaluation

## Objective

Determine whether the system is sufficiently useful, grounded, safe and governable to enter Copilot Mode.

## Evaluation domains

- Task correctness
- Evidence grounding
- Unsupported assertion
- Policy compliance
- Tool correctness
- Escalation correctness
- Privacy leakage
- Prohibited action attempt
- Human override
- Latency
- Cost
- Audit completeness
- User usefulness
- Outcome relevance

## Error severity

~~~text
S0 Informational difference
S1 Minor quality issue
S2 Material rework
S3 High-impact wrong recommendation
S4 Unauthorized / dangerous action attempt
~~~

## Procedure

1. Define thresholds before reviewing final results.
2. Separate development and acceptance cases.
3. Evaluate normal, edge and adversarial cases.
4. Test prompt injection / malicious content where tools or external documents are used.
5. Test stale/conflicting knowledge.
6. Test permission boundary.
7. Test wrong-user / wrong-role context.
8. Test agent revocation.
9. Test audit reconstruction.
10. Review errors by severity and root cause.
11. Do not average away S3/S4 failures.
12. Produce Go / Hold / Reject recommendation.

## Required artifact

Agent Evaluation & Release Readiness Report.

## Exit gate G15

Role Owner + AI Governance + Security approve Copilot Mode.

# 16 Copilot Mode — Production SOP

## 16.1 Objective

Deploy the agent to real users as an assistant while keeping the human user responsible for accepting, editing, rejecting, escalating or executing consequential work.

Copilot Mode is not autonomous mode.

## 16.2 Allowed default task classes

- search approved knowledge;
- retrieve evidence;
- summarize;
- compare;
- explain;
- draft documents;
- draft reports;
- draft meeting outputs;
- prepare checklists;
- prefill forms;
- calculate from approved structured data;
- highlight anomalies;
- suggest next steps;
- suggest escalation;
- prepare task packages;
- create draft workflow items.

## 16.3 Default prohibited actions

Unless a separate approved workflow explicitly permits them:

- final clinical diagnosis or prescribing;
- signing clinical orders;
- changing EMR/HIS clinical records;
- approving payment;
- approving procurement;
- approving HR disciplinary action;
- changing access permissions;
- publishing external official statements;
- deleting authoritative records;
- executing irreversible infrastructure/security changes.

## 16.4 Runtime pipeline

~~~text
A. Human Login
        |
        v
B. Bind Human Identity + Role + Agent Identity
        |
        v
C. Intent / Task Classification
        |
        v
D. Risk Classification
        |
        +---- high/unsupported ----> Escalate / Refuse / Human-only
        |
        v
E. Context Builder
        |
        v
F. Governed Retrieval
        |
        v
G. Draft / Recommendation Generation
        |
        v
H. Evidence + Policy Validation
        |
        v
I. Output Guardrails
        |
        v
J. Human Review UI
        |
        +--> Reject
        +--> Edit
        +--> Ask Again
        +--> Escalate
        +--> Accept Draft
        |
        v
K. Optional Tool Proposal
        |
        v
L. Permission Check
        |
        v
M. Human Approval if required
        |
        v
N. Controlled Tool Execution
        |
        v
O. Result Verification
        |
        v
P. Audit + Feedback
        |
        v
Q. Memory Promotion Queue
~~~

## 16.5 Detailed runtime procedure

### A. Human authentication

1. Authenticate human user.
2. Resolve user role, department, current assignments and applicable constraints.
3. Do not assume that because the user can see data, the agent may automatically use all of it.
4. Record initiator identity.

### B. Agent binding

1. Resolve the approved Agent Manifest.
2. Verify status = ACTIVE.
3. Verify version and review date.
4. Verify unique agent identity is enabled.
5. Verify no revocation flag.
6. Record human-on-behalf-of-agent relationship.

### C. Task classification

Classify the request:

~~~text
Q&A
Search
Summary
Draft
Analysis
Recommendation
Workflow proposal
Tool action
High-impact decision
Unsupported
~~~

If unsupported, do not improvise a new authority.

### D. Risk classification

At runtime classify:

- data sensitivity;
- action reversibility;
- clinical/financial/HR/legal/security impact;
- external publication impact;
- uncertainty;
- evidence sufficiency.

A high-impact task must route to the configured human-only or approval workflow.

### E. Context Builder

Load only task-relevant context:

~~~text
Task
+ User Role
+ Agent Role
+ Current Organizational State
+ Approved Evidence
+ Applicable Policy
+ Relevant Role Memory
+ Allowed Person Overlay
+ Recent Task Context
~~~

Do not load the employee's entire history.

### F. Governed Retrieval

1. Search approved knowledge first.
2. Query Semantic Layer / Data Mart / Knowledge Graph according to manifest.
3. Attach source IDs.
4. Check source version/freshness.
5. Surface conflicting sources.
6. If evidence is insufficient, return INSUFFICIENT_EVIDENCE rather than inventing an answer.

### G. Generation

Generate a draft/recommendation that distinguishes:

- observed facts;
- derived calculations;
- assumptions;
- recommendation;
- uncertainty;
- missing evidence;
- required approval.

### H. Evidence validation

Before showing final content:

1. Verify factual organizational claims have source support.
2. Verify source authority.
3. Verify data freshness where required.
4. Detect conflicts.
5. Validate calculations.
6. Ensure policy references match current version.

### I. Output guardrails

Check for:

- prohibited content/action;
- unauthorized data exposure;
- unnecessary patient/employee identifiers;
- unsupported claims;
- confidential information outside user scope;
- hidden external action;
- misleading certainty.

Block/redact/route for review as policy requires.

### J. Human Review UI

Every Copilot output should expose:

- AI-generated label;
- task status;
- evidence links;
- source date/version;
- assumptions;
- uncertainty or limitations;
- policy/approval requirement;
- buttons for Accept / Edit / Reject / Escalate / Report Error.

For important drafts, show the human's edits as a diff so the system can measure where the Copilot was wrong or incomplete.

### K. Tool proposal

The Copilot may propose:

~~~text
"Create draft task"
"Prepare email draft"
"Open approval request"
"Save reviewed note"
"Query updated metric"
~~~

The model's decision to use a tool is not authorization.

### L. Permission engine

For every tool call verify:

~~~text
WHO = human + agent identity
WHAT = exact action
RESOURCE = exact target
WHY = task/workflow
SCOPE = fields / records / amount / destination
TIME = current authorization validity
AUTHORITY = role + policy
APPROVAL = required or not
~~~

Deny-by-default if any required authorization element is missing.

### M. Human approval

When approval is required:

1. Pause run.
2. Show exact proposed action.
3. Show target/resource.
4. Show key data affected.
5. Show risk.
6. Show evidence.
7. Require explicit approve/reject.
8. Record approver identity and timestamp.
9. Do not treat silence/time-out as approval.

### N. Controlled execution

If the approved Copilot workflow permits action:

1. Use scoped/short-lived credential.
2. Call only the registered tool.
3. Limit parameters to approved scope.
4. Record correlation ID.
5. Receive structured tool result.
6. Do not assume success from model text.

### O. Result verification

1. Verify downstream result.
2. Compare intended vs actual effect.
3. Report partial failure.
4. Where possible support rollback or compensating action.
5. Do not claim completion without execution evidence.

### P. Audit and feedback

Record:

- human user;
- agent;
- manifest version;
- task;
- sources;
- tool calls;
- approvals;
- output;
- edits;
- reject reason;
- execution evidence;
- latency/cost;
- incident flag.

### Q. Memory promotion

Copilot interaction is not automatically Organizational Memory.

Route learning to:

~~~text
Raw interaction
-> Candidate Lesson
-> Review
-> Person Memory / Role Memory / Organizational Memory
~~~

The reviewer must decide destination.

## 16.6 Copilot output states

~~~text
AI_DRAFT
AI_RECOMMENDATION
NEEDS_EVIDENCE
NEEDS_APPROVAL
ESCALATED
HUMAN_EDITED
HUMAN_ACCEPTED
HUMAN_REJECTED
TOOL_PROPOSED
TOOL_APPROVED
TOOL_EXECUTED
TOOL_FAILED
CLOSED
~~~

## 16.7 Copilot UI minimum requirements

- visible AI identity;
- human user identity/context;
- current role;
- evidence drawer;
- source freshness;
- policy/approval banner;
- editable draft;
- Accept/Edit/Reject;
- Escalate;
- Report Error;
- audit reference;
- no silent auto-send for consequential outputs.

## 16.8 Daily operational monitoring

Monitor:

- task volume;
- accepted outputs;
- edited outputs;
- rejected outputs;
- escalation rate;
- unsupported-claim rate;
- evidence failure;
- tool denial;
- approval requests;
- tool failure;
- latency;
- cost;
- privacy/security incidents.

## 16.9 Weekly Copilot review

Role Owner + Product + Evaluation review:

1. top rejected tasks;
2. high-edit tasks;
3. recurring missing knowledge;
4. policy conflicts;
5. false escalations;
6. missed escalations;
7. unsafe tool attempts;
8. user feedback;
9. time saved;
10. candidate improvements.

No change to the production manifest should bypass change control.

## 16.10 Incident triggers

Immediately suspend or restrict the Copilot if:

- unauthorized sensitive-data exposure;
- unauthorized tool execution;
- S4 event;
- repeated S3 event;
- identity/permission bypass;
- audit failure;
- material source poisoning;
- compromised credentials;
- inability to revoke agent access.

## 16.11 Exit criteria from Copilot Mode

Advance toward Approved Agent Mode only when:

- agreed user-value target is achieved;
- evidence grounding is within approved threshold;
- no unresolved critical privacy/security issue;
- role owner accepts outputs;
- user training is complete;
- audit reconstruction passes;
- permission tests pass;
- kill switch test passes;
- approval workflow passes;
- monitoring is operational;
- stability is demonstrated for the defined evaluation period;
- AI Governance formally approves the specific workflow moving forward.

# 17 Approved Agent Mode

## Objective

Allow the agent to execute only explicitly approved bounded workflows under deterministic authorization.

Approved Agent Mode does not equal unrestricted autonomy.

## Procedure

1. Define one exact workflow.
2. Define trigger.
3. Define allowed data.
4. Define allowed tools.
5. Define permitted side effects.
6. Define maximum action scope.
7. Define approval points.
8. Define escalation.
9. Define rollback/compensation.
10. Define max steps/time/cost.
11. Use short-lived/JIT privilege where practical.
12. Re-authorize at downstream system.
13. Record every tool action.
14. Verify real-world effect.
15. Monitor outcomes and incidents.
16. Revalidate after material changes.
17. Support immediate suspend/revoke.

## Prohibited model

~~~text
"Agent can do anything the employee can do"
~~~

This is never an acceptable permission rule.

## Acceptable model

~~~text
Agent X may perform Action Y
on Resource Z
for Workflow W
within Scope S
when Condition C is met
after Approval A
using Tool T
until Expiry E.
~~~

## Exit gate G17

Production Workflow Approval Record is signed by required business, governance, security and domain owners.

# 18. Cross-stage Quality Gates

No stage is DONE unless its artifact exists and is reviewable.

| Gate | Required evidence |
|---|---|
| G01 | Twin Charter |
| G02 | Role Contract |
| G03 | Governance/Data approval |
| G04 | Governed Knowledge Corpus |
| G05 | Observed Workflow |
| G06 | Process Model/Variants |
| G07 | Decision Dataset |
| G08 | Skill Graph |
| G09 | Knowledge Graph |
| G10 | Role Twin |
| G11 | Person Overlay |
| G12 | Versioned Agent Manifest |
| G13 | Harness Readiness Report |
| G14 | Shadow Dataset |
| G15 | Evaluation/Release Report |
| G16 | Copilot Operations & Monitoring Evidence |
| G17 | Approved Workflow Record |

# 19. Recommended Repository Structure

~~~text
twins/
  roles/
    <role_id>/
      charter.yaml
      role_contract.yaml
      responsibilities.yaml
      authority.yaml
      skills.yaml
      processes/
      decisions/
      knowledge/
      role_twin.yaml
      manifests/
      evals/
      approvals/

  people/
    <person_id>/
      overlay.yaml
      assignments.yaml
      reviewed_lessons/
      consent_governance/
      offboarding/

agents/
  <agent_id>/
    manifest.yaml
    policy.yaml
    tool_allowlist.yaml
    eval_suite.yaml
    shadow/
    copilot/
    approvals/
    audit/
~~~

# 20. Go-Live Checklist for First Real Pilot

Before the first real employee uses Copilot Mode:

- Twin Charter approved.
- Role Contract approved.
- Privacy/governance review complete.
- Knowledge corpus approved.
- Workflow/process validated.
- Decision episodes reviewed.
- Role Twin signed off.
- Person Overlay can be unbound safely.
- Agent Manifest version locked.
- Unique agent identity active.
- Least-privilege access tested.
- Tool allowlist tested.
- Human approval tested.
- Audit trace tested.
- Kill switch tested.
- Shadow Mode completed.
- Evaluation approved.
- User trained.
- Feedback/report-error channel active.
- Monitoring dashboard active.
- Incident owner on call / reachable.

# 21. Recommended First Production Pilot

Prefer a bounded coordinator/analyst role where the initial Copilot tasks are:

~~~text
Evidence Search
-> Evidence Summary
-> Draft Report
-> Follow-up Checklist
-> Risk / Missing Data Flag
-> Escalation Recommendation
-> Human Review
~~~

Do not use the first production pilot to test autonomous high-impact clinical, procurement, payment, personnel or security decisions.

# 22. Governance Alignment

This SOP is designed to align with risk-based AI lifecycle governance, human oversight, least privilege, unique agent identity, per-action authorization, guardrails, auditability and controlled deployment.

Local legal, DPO, security, clinical and organizational requirements remain authoritative.

# 23. Final Rule

~~~text
Select carefully.
Discover the role.
Govern the data.
Capture evidence.
Observe real work.
Model the process.
Capture reviewable decisions.
Build skills and knowledge graphs.
Create Role Twin.
Add a separable Person Overlay.
Compile an explicit Agent Manifest.
Run it through a deterministic Harness.
Shadow before exposure.
Evaluate before trust.
Use Copilot before autonomy.
Approve only bounded workflows.
Measure outcomes.
Audit everything.
Revoke quickly when needed.
~~~
