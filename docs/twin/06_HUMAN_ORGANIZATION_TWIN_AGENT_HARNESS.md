# Human & Organization Twin + Agent Harness Architecture

Status: Controlled architecture blueprint  
Scope: HosPrime Staff / Role Twin, Organization Twin, AI Agent Office, and Agent Runtime  
Owner: Product, Architecture, Data Governance, AI Governance  
Target milestone: M2 -> M4

## 1. Purpose

This document defines how HosPrime converts governed organizational knowledge about real work into safe, auditable AI agents.

The target chain is:

```text
Human / Employee
    -> Role & Work Digital Twin
    -> Person Overlay
    -> Agent Manifest
    -> Agent Harness
    -> Governed AI Agent
    -> Recommendation / Approved Action
    -> Outcome
    -> Learning
```

HosPrime must not treat an employee as a prompt to be copied. The system models work, responsibility, knowledge, decisions, evidence, relationships, authority and escalation boundaries.

## 2. Core position

HosPrime does **not** build an "AI clone of an employee."

The production construct is:

```text
Institutional Knowledge
+ Role Twin
+ Person Overlay
+ Decision Memory
+ Governed Agent Identity
+ Agent Harness
= Governed Organizational Agent
```

The primary optimization target is correct, accountable role performance, not imitation of a person's personality.

## 3. Twin maturity model

Human-oriented twins should be treated as progressively stronger constructs.

### 3.1 Digital Model

A static representation of a role, person, skill set, responsibility or workflow.

### 3.2 Digital Shadow

The model is updated from observed work, events, systems or reviewed evidence.

### 3.3 Governed Digital Twin

A continuously maintained model linked to evidence, relationships, decision pathways, audit events and controlled feedback from real-world outcomes.

Cognitive and psychological modeling of whole persons remains a high-risk and immature area. HosPrime therefore prioritizes observable work and declared preferences over inferred personality.

## 4. Three distinct twin layers

### 4.1 Role Twin

Represents the organizational position independent of the current person.

Examples:

- Hospital Director
- Provincial TB Coordinator
- OPD Head
- Finance Manager
- Data Protection Officer
- Procurement Officer

Role Twin persists when personnel change.

### 4.2 Person Work Twin / Person Overlay

Represents person-specific work knowledge that is approved for use.

Examples:

- validated expertise;
- preferred briefing format;
- known work heuristics;
- reviewed decision episodes;
- collaboration patterns;
- lessons learned;
- approved personal working preferences.

Person Overlay must remain separable from Role Memory.

### 4.3 Agent Twin

Represents the AI operating entity that uses a Role Twin and, where permitted, a Person Overlay.

An Agent Twin has its own:

- identity;
- owner / sponsor;
- purpose;
- version;
- approved data scope;
- tools;
- permissions;
- autonomy level;
- validation state;
- audit trail;
- revocation / kill switch.

## 5. Organizational continuity model

```text
Hospital Director Role Twin
        |
        +-- Director A Person Overlay [archived]
        |
        +-- Director B Person Overlay [active]
```

When a person transfers, changes role or retires:

- Role Twin remains.
- Organizational Knowledge remains.
- Reviewed Role Memory remains.
- Approved lessons remain.
- Person Overlay is archived, transferred or retained according to policy.
- Agent privileges are revoked or re-bound.
- No inherited human credential is transferred to an agent.

## 6. Employee / Role DNA model

HosPrime should capture at least the following dimensions.

### 6.1 Organizational Identity

Fields may include:

- employee reference;
- role;
- position;
- profession;
- department;
- supervisor;
- subordinates;
- committees;
- projects;
- cost center;
- formal delegated authority.

Graph relationships may include:

```text
Person
 ├── works_in -> Department
 ├── reports_to -> Supervisor
 ├── owns -> KPI
 ├── leads -> Project
 ├── responsible_for -> Process
 ├── member_of -> Committee
 └── performs -> Role
```

### 6.2 Responsibility Twin

Derived from controlled sources such as:

- job description;
- appointment order;
- delegation order;
- TOR;
- RACI;
- KPI;
- SOP;
- official workflow;
- approved work instruction.

Example:

```yaml
responsibility:
  id: approve_monthly_tb_report
  role: provincial_tb_coordinator
  inputs:
    - district_tb_report
    - laboratory_report
    - treatment_outcome
  output:
    - validated_provincial_report
  authority:
    can_validate: true
    can_publish: false
  escalation:
    - provincial_public_health_physician
```

### 6.3 Competency Twin

Use a Skill Graph rather than flat labels.

```text
TB surveillance
    |
    +-- screening
    +-- cohort analysis
    +-- LTFU investigation
    +-- contact tracing
    +-- outbreak investigation
```

Every competency assertion should contain:

- evidence;
- level;
- confidence;
- validator;
- last verified date;
- expiry / review date where applicable.

Example:

```yaml
skill: TB cohort analysis
level: expert
evidence:
  - 14 quarterly reports
  - 6 reviewed outbreak investigations
confidence: 0.93
validated_by: TB_program_manager
last_verified: 2026-08-01
```

### 6.4 Knowledge Twin

Separate at least:

- Explicit Knowledge;
- Tacit Knowledge;
- Institutional Knowledge;
- Case Knowledge;
- Policy / Regulatory Knowledge;
- Lessons Learned.

Tacit knowledge must not become organizational truth automatically. Promotion requires review and provenance.

### 6.5 Workflow Twin

Capture how work is actually performed, not only how SOP describes it.

Possible evidence:

- HIS event logs;
- ERP events;
- ticketing;
- document workflow;
- task system;
- meeting action items;
- calendar metadata;
- reviewed email / message artifacts;
- direct observation;
- process-mining output.

The system should preserve the distinction:

```text
Designed Process
vs
Observed Process
vs
Approved Process
```

### 6.6 Decision Twin / Decision Memory

Decision episodes are a first-class object.

```text
Situation
 -> Evidence Observed
 -> Options Considered
 -> Rule / Reasoning
 -> Decision
 -> Action
 -> Outcome
 -> Lesson Learned
```

Example:

```yaml
decision_episode:
  context:
    bed_occupancy: 97
    er_boarding: 22
  evidence:
    - current_bed_census
    - predicted_discharge_next_6h
  options:
    - expedite_discharge
    - open_step_down_capacity
    - divert_selected_referrals
  selected_action: open_step_down_capacity
  rationale: predicted_discharge_next_6h_low
  outcome:
    er_boarding_after: 8
  lesson:
    discharge_coordination_should_start: "09:00"
```

The goal is not to reproduce hidden human thought. It is to preserve reviewable decision evidence, options, rationale, authority and outcome.

### 6.7 Collaboration Twin

Model who collaborates with whom and why.

```text
TB Coordinator
   |
   +-- asks -> Lab Expert
   +-- reports_to -> CDC Chief
   +-- coordinates -> District CDCU
   +-- escalates_to -> PHO
```

This graph is used for routing, escalation and expert discovery.

### 6.8 Communication Preferences

Only declared or explicitly approved preferences should be operationalized.

Example:

```yaml
communication:
  primary_language: Thai
  briefing_style:
    - concise
    - evidence_first
    - executive_summary
  preferred_formats:
    - table
    - chart
    - risk_prioritization
```

Do not automatically infer sensitive psychological attributes, political views, health status or other protected characteristics from workplace communications.

### 6.9 Tool Twin

Records which tools, applications and data products are required for the role.

Examples:

- HOSxP / HIS read access;
- ERP;
- HR;
- FHIR;
- document repository;
- knowledge search;
- forecast engine;
- reporting tools;
- workflow engine.

Tool inventory does not imply agent permission.

### 6.10 Authority Twin

Defines what the role may:

- observe;
- recommend;
- draft;
- validate;
- assign;
- approve;
- execute;
- publish;
- escalate.

Authority must be deterministic and enforceable outside the model.

### 6.11 Risk & Governance Twin

Records:

- data classification;
- AI risk level;
- approval requirements;
- conflict-of-interest rules;
- regulatory constraints;
- segregation of duties;
- retention rules;
- prohibited actions.

### 6.12 Outcome Twin

Links work and decisions to measurable outcomes.

Examples:

- time saved;
- waiting time;
- financial recovery;
- claim rejection reduction;
- quality improvement;
- treatment completion;
- policy execution;
- user acceptance;
- error / incident rate.

## 7. Graph model

Minimum node types:

```text
Person
Role
Department
Organization
Responsibility
Skill
KnowledgeArtifact
Process
Task
Decision
Evidence
Policy
KPI
Project
Tool
Agent
Approval
Outcome
Lesson
```

Minimum relationships:

```text
works_in
performs
reports_to
responsible_for
owns
requires_skill
knows
uses
participates_in
depends_on
observes
supports
recommends
decides
approves
executes
escalates_to
produces
affects
measured_by
learned_from
```

All material graph assertions require provenance.

## 8. Agent Manifest

A twin must not directly become an agent. It must first compile into a reviewed Agent Manifest.

Example:

```yaml
agent_id: TB_COORDINATOR_001
version: 1.0.0

twin_binding:
  role_twin: provincial_tb_coordinator
  person_overlay: employee_127

mission:
  Improve provincial TB surveillance and treatment outcomes.

objectives:
  - monitor_screening
  - detect_ltfu
  - detect_outbreak_signal
  - generate_weekly_brief

knowledge:
  - tb_guidelines
  - provincial_sop
  - reviewed_historical_cases
  - decision_memory

tools:
  - query_tb_datamart
  - query_lab_summary
  - search_policy
  - generate_report

permissions:
  read:
    - TB_DATAMART
    - APPROVED_KNOWLEDGE
  write:
    - DRAFT_REPORT
  prohibited:
    - modify_patient_record
    - approve_budget
    - publish_external_report

escalation:
  clinical: TB_physician
  policy: CDC_director

autonomy_level: 2
human_approval_required:
  - external_publication
  - patient_level_action
  - resource_commitment
```

## 9. Twin-to-Agent Compiler

The compiler is a controlled build process, not free-form prompting.

```text
Role Twin
+ Approved Person Overlay
+ Responsibility Graph
+ Knowledge Scope
+ Decision Memory
+ Tool Registry
+ Permission Policy
+ Risk Policy
        |
        v
Validation
        |
        v
Agent Manifest
        |
        v
Signed / Versioned Agent Package
```

Compilation must fail closed if required ownership, evidence, authority or risk metadata is missing.

## 10. Agent Harness

The Agent Harness is the runtime boundary around the model.

```text
                    EMPLOYEE / ROLE TWIN
                            |
                            v
                 +------------------+
                 |   Agent Manifest |
                 +--------+---------+
                          |
                          v
+------------------------------------------------+
|               HOSPRIME AGENT HARNESS           |
|                                                |
| Identity                                       |
| Instructions                                   |
| Context Builder                                |
| Memory                                         |
| Knowledge Retrieval                            |
| Tool Gateway                                   |
| Policy Engine                                  |
| Permission Engine                              |
| Workflow Engine                                |
| Human Approval                                 |
| Guardrails                                     |
| Evaluation                                     |
| Trace / Audit                                  |
| Sandbox                                        |
| Cost / Step Limits                             |
| Kill Switch                                    |
+----------------------+-------------------------+
                       |
                       v
                    LLM / SLM
                       |
                       v
             Recommendation / Action
```

The harness is separate from the model. Replacing the model must not bypass policy, identity, audit or approval controls.

## 11. Harness subsystems

### 11.1 Identity

Every production agent must have a unique nonhuman identity with:

- accountable owner / sponsor;
- lifecycle state;
- credentials or workload identity;
- explicit scope;
- revocation path;
- audit linkage.

Agents must not borrow shared human credentials.

### 11.2 Instructions

Runtime instructions are compiled from:

- mission;
- role;
- objectives;
- approved SOP;
- authority;
- constraints;
- escalation;
- evidence rules.

Prompt text is advisory. Deterministic enforcement must remain outside the model.

### 11.3 Context Builder

Use task-scoped context.

```text
Current Task
+ Role
+ Current State
+ Relevant Evidence
+ Relevant Knowledge
+ Relevant Memory
+ Policy
```

Do not load a person's entire history into every task.

### 11.4 Memory

Minimum memory classes:

- Working Memory;
- Episodic Memory;
- Semantic Memory;
- Decision Memory;
- Role Memory;
- Organizational Memory.

Every persistent memory item should carry:

- source;
- owner;
- author / system;
- timestamp;
- evidence type;
- classification;
- confidence;
- review status;
- retention;
- version.

### 11.5 Knowledge Retrieval

Preferred retrieval chain:

```text
Semantic Layer
+ Data Mart
+ Knowledge Graph
+ Governed RAG
+ Decision Memory
```

Production agents should not query source systems directly unless a separately governed connector explicitly allows it.

### 11.6 Tool Gateway

All external actions should pass through a controlled Tool / MCP Gateway.

Potential adapters:

- FHIR;
- HIS;
- HR;
- ERP;
- document system;
- email;
- calendar;
- workflow;
- forecast engine;
- report generator.

Every tool call must carry actor, agent, task, requested action, target resource and authorization context.

### 11.7 Policy & Permission Engine

Each consequential request must answer:

```text
WHO
wants to do
WHAT
to WHICH RESOURCE
under WHICH AUTHORITY
for WHICH TASK
```

Enforce deny-by-default for unregistered tools and unapproved actions.

### 11.8 Human Approval Gateway

HosPrime autonomy levels:

```text
L0 Observe
L1 Recommend
L2 Draft
L3 Coordinate
L4 Execute Approved Workflow
L5 Fully Autonomous High-Impact Action = NOT ALLOWED
```

Fresh human approval is required for high-impact actions, including clinical, financial, procurement, HR, legal, security and external publication actions according to policy.

### 11.9 Evaluation

Every agent version must have defined evals before release.

Minimum categories:

- task correctness;
- evidence grounding;
- policy compliance;
- tool correctness;
- escalation correctness;
- privacy leakage;
- unsafe action attempts;
- hallucination;
- human override;
- outcome quality.

### 11.10 Trace / Audit

Each run should be reconstructable.

Required audit fields include:

- timestamp;
- human initiator;
- agent identity;
- agent version;
- twin binding;
- task / workflow;
- input evidence;
- retrieved context;
- policy version;
- tool calls;
- permission decisions;
- model / runtime version;
- output;
- approval;
- execution result;
- outcome;
- incident / override.

### 11.11 Sandbox

Untrusted code, file transformations and external tool interactions should execute in controlled environments with:

- filesystem boundary;
- network / egress policy;
- resource limits;
- timeout;
- step limit;
- secret isolation;
- audit.

### 11.12 Kill Switch and Revocation

Production agents must support immediate:

- disable;
- credential revoke;
- token invalidate;
- tool revoke;
- memory write freeze;
- workflow stop;
- rollback to last approved manifest.

## 12. Security boundary

Agent identity and human identity are related but not interchangeable.

```text
Human User
   |
   +-- initiates / approves
   v
Agent Identity
   |
   +-- scoped permission
   v
Tool Gateway
   |
   +-- downstream re-authorization
   v
Target System
```

High-impact systems must re-check authorization at the downstream boundary.

## 13. Memory promotion model

```text
Personal / Staff Memory
        |
        | reviewed promotion
        v
Role Memory
        |
        | governance review
        v
Organizational Memory
```

External research follows a separate path:

```text
Research Staging
        |
        | authority + relevance + applicability review
        v
Approved Knowledge
```

No memory write becomes organizational truth merely because an LLM generated it.

## 14. From Organization Twin to Agent Office

```text
                    ORGANIZATION TWIN
                          |
        +-----------------+-----------------+
        |                 |                 |
 Hospital Twin      Workforce Twin    Process Twin
        |                 |                 |
        +-----------------+-----------------+
                          |
                    Knowledge Graph
                          |
                  +-------+--------+
                  |                |
              Role Twins       Person Twins
                  |                |
                  +-------+--------+
                          |
                    Agent Factory
                          |
                    Agent Harness
                          |
             +------------+------------+
             |            |            |
         Executive     Department    Staff
          Agents         Agents       Agents
```

The Digital Twin layer describes the organization.  
The Agent layer performs bounded cognitive work.  
The Harness provides control, execution safety and accountability.

## 15. Required HosPrime services

Target subsystems:

1. Employee Twin Registry
2. Role Twin Registry
3. Competency Graph
4. Responsibility Graph
5. Workflow Twin
6. Decision Memory
7. Knowledge Twin
8. Collaboration Graph
9. Agent Manifest Generator
10. Agent Harness Runtime
11. Agent Identity & Permission Service
12. Tool / MCP Gateway
13. Human Approval Gateway
14. Agent Evaluation Lab
15. Twin Versioning
16. Agent Lifecycle Management
17. Audit / Trace Service
18. Kill-Switch / Revocation Service

## 16. Recommended APIs

Illustrative contract:

```text
GET    /twins/roles/{role_id}
GET    /twins/people/{person_id}
GET    /twins/people/{person_id}/skills
GET    /twins/people/{person_id}/decisions
GET    /twins/roles/{role_id}/responsibilities

POST   /twins/roles/{role_id}/compile-agent
GET    /agents/{agent_id}/manifest
POST   /agents/{agent_id}/runs
POST   /agents/{agent_id}/approvals
POST   /agents/{agent_id}/revoke

GET    /agents/{agent_id}/audit
GET    /agents/{agent_id}/evals
GET    /agents/{agent_id}/permissions
```

No API above implies that patient-level or restricted data is available by default.

## 17. Acceptance criteria

A Staff / Role Twin is not production-ready until:

- role owner exists;
- person/role memory separation is tested;
- data classification is recorded;
- evidence provenance exists;
- responsibility and authority are explicit;
- consent / lawful basis is recorded where required;
- knowledge promotion path exists;
- decision episodes are reviewable;
- retention is defined.

An Agent is not production-ready until:

- unique agent identity exists;
- manifest is versioned;
- approved tool allowlist exists;
- least-privilege authorization is enforced;
- downstream authorization is tested;
- approval gates are tested;
- audit is complete;
- kill switch is tested;
- eval thresholds pass;
- shadow-mode evidence exists;
- accountable owner accepts the release.

## 18. Anti-patterns

Do not:

- create one giant "employee personality prompt";
- copy all private communications into memory by default;
- infer sensitive traits without a lawful, necessary use case;
- merge Person Memory and Role Memory;
- allow agents to inherit a human password or token;
- give an agent unrestricted database access;
- treat an LLM-generated statement as organizational evidence;
- allow high-impact execution because the prompt says it is allowed;
- call a prototype a Digital Twin when no feedback or evidence loop exists;
- call an agent validated because it "looks similar" to the employee.

## 19. Product metrics

Twin metrics:

- evidence completeness;
- role coverage;
- responsibility coverage;
- validated skill coverage;
- memory provenance coverage;
- stale knowledge rate;
- decision-to-outcome linkage.

Agent metrics:

- Trusted Task Completion Rate;
- task accuracy;
- evidence-grounded answer rate;
- policy compliance;
- tool success;
- correct escalation;
- human approval / rejection;
- human override;
- unsafe action attempt rate;
- privacy incident rate;
- cost per accepted task;
- time saved;
- outcome improvement.

## 20. Research and architecture references

The following external references support the architecture direction and must remain research inputs rather than automatic policy:

- OpenAI, "The next evolution of the Agents SDK" (2026): model-native agent harness, controlled sandbox execution, separation of harness and compute.
  https://openai.com/index/the-next-evolution-of-the-agents-sdk/
- Microsoft Learn, "Least privilege for AI agents": unique agent identity, explicit scope, approval, auditability, revocation and JIT access.
  https://learn.microsoft.com/en-us/security/zero-trust/sfi/least-privilege-for-ai-agents
- Microsoft Learn, "Identity, Access, and Least Privilege": explicit identities for users, agents, plugins and tools; per-tool authorization and stronger controls for high-impact actions.
  https://learn.microsoft.com/en-us/security/zero-trust/catalog-ai-defense-capabilities/identity-access-least-privilege
- Microsoft Learn, "AI agent shared responsibility model": per-tool permissions, per-action authorization, HITL for high-impact actions, memory isolation, sandboxing and audit logging.
  https://learn.microsoft.com/en-us/azure/security/fundamentals/shared-responsibility-ai-agent

## 21. Strategic statement

HosPrime should preserve institutional capability without pretending to reproduce the whole human being.

```text
Person leaves
but approved
Knowledge
Decision Patterns
Lessons Learned
Workflow Knowledge
Role Knowledge
and Organizational Memory
remain governed and reusable.
```

The intended end-state is an accountable AI organization in which humans retain authority and agents amplify institutional capability.
