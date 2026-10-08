# HosPrime Twin Milestone Roadmap

Status: Controlled milestone blueprint  
Scope: Healthcare Twin Ecosystem development sequence

## 1. Purpose

This roadmap defines how HosPrime should build the Healthcare Twin Ecosystem in a controlled, evidence-based sequence. The goal is to answer real user needs at every level without overbuilding speculative twins.

## 2. Roadmap principle

```text
Do not build every twin first.
Build the minimum connected twin chain that enables real work completion.
```

The first chain is:

```text
Hospital Twin -> Department Twin -> Staff Twin -> Process Twin -> Decision Twin
```

This chain connects executives, department heads, staff and governance reviewers.

## 3. Milestone 0: Twin Foundation

### Objective

Create the controlled language, data model and governance boundary for all twins.

### Deliverables

- Twin Ecosystem Vision
- Twin Taxonomy
- Twin Data Model
- User-Level Mapping
- Twin Acceptance Criteria

### Exit criteria

- Each twin type has a defined owner, user, data source and decision pathway.
- Product team agrees that Hospital Twin is one type inside a larger ecosystem.
- No new twin is added without evidence of user value.

## 4. Milestone 1: Hospital Twin Lite

### Objective

Create a daily executive operating view for a hospital.

### Initial scope

- OPD status
- ER status
- IPD and bed status
- finance and claim status
- workforce pressure
- risk and decision queue

### Key users

- hospital director;
- deputy director;
- executive office;
- data reviewer.

### Exit criteria

- User can understand hospital status within one executive view.
- Each alert links to source evidence and owner.
- The system separates observation, recommendation, approval and execution record.

## 5. Milestone 2: Department Twin

### Objective

Give department heads a practical workbench.

### Initial departments

- OPD
- ER
- IPD ward
- Pharmacy
- Finance
- HR
- IT or data unit

### Core functions

- department KPI;
- workload;
- backlog;
- process bottleneck;
- task follow-up;
- weekly brief generation.

### Exit criteria

- Department head can identify current risk and next action.
- Department summary uses approved evidence.
- Tasks are connected to decisions and outcomes.

## 6. Milestone 3: Staff / Role Twin

### Objective

Create a governed workspace for staff and roles, while establishing the Role Twin / Person Overlay separation required for safe future agents.

### Core functions

- My Tasks
- My Knowledge
- My Meetings
- My Documents
- My Role Responsibilities
- My AI Copilot
- Role Twin
- Person Overlay
- Responsibility Graph
- Competency Graph
- reviewed Decision Episodes
- Collaboration / Escalation Graph
- Agent Manifest preview

### Governance boundary

- Personal notes are not organizational evidence by default.
- Role Memory and Person Memory remain separated.
- The system models work and authority, not an employee's whole personality.
- Promotion to Role or Organizational Memory requires review and provenance.
- Observed behavior does not automatically override formal policy or authority.
- Sensitive psychological or protected characteristics are not inferred for convenience.
- A Person Overlay never grants tool or data permissions by itself.

### Exit criteria

- Staff can complete routine knowledge and documentation work faster than baseline.
- AI answers only with approved evidence or declares insufficient evidence.
- Staff Twin does not expose unnecessary sensitive information.
- Role Twin remains usable independently of the current employee.
- Person Overlay can be archived or re-bound without losing approved Role Memory.
- A versioned Agent Manifest can be compiled from approved twin artifacts, but no increased autonomy is implied.

## 7. Milestone 4: Process Twin

### Objective

Make bottlenecks explainable and actionable.

### First processes

- OPD flow
- ER triage to admission
- IPD discharge
- referral
- claim submission
- procurement
- meeting to decision to action

### Exit criteria

- Process owner can see step, actor, system, delay and failure mode.
- Bottleneck recommendation links to evidence and responsible owner.
- Improvement action can be tracked to outcome.

## 8. Milestone 5: Decision Twin and Semantica-style decision intelligence

### Objective

Every important AI recommendation or management decision becomes traceable.

### Core functions

- decision graph;
- evidence graph;
- policy reference;
- approval state;
- conflict detection;
- outcome and lesson learned.

### Exit criteria

- A reviewer can answer why a recommendation was made.
- Evidence and policy references are visible.
- Approval and execution states are not confused.
- Lessons learned can update organizational memory after review.

## 9. Milestone 6: Population and Provincial Twin

### Objective

Expand from hospital operations to public-health intelligence.

### Initial scope

- NCD burden
- TB surveillance
- dengue risk
- PM2.5 vulnerable groups
- aging and LTC
- disaster/PHEOC
- workforce and resource distribution

### Exit criteria

- Provincial users can compare districts or hospitals using aggregate data.
- Patient-level data is not shared by default.
- System supports policy and resource decisions with evidence.

## 10. Milestone 7: AI Agent Twin and Agent Harness

### Objective

Make AI agents auditable operating entities that run only through a governed Agent Harness.

### Core capabilities

- unique nonhuman agent identity and accountable sponsor;
- versioned Agent Manifest;
- task-scoped Context Builder;
- separated Working, Episodic, Semantic, Decision, Role and Organizational Memory;
- governed retrieval through Semantic Layer / Data Mart / Knowledge Graph / RAG;
- Tool / MCP Gateway;
- policy and least-privilege permission engine;
- Human Approval Gateway;
- sandbox and resource limits;
- evaluation suite;
- trace / audit service;
- kill switch and revocation;
- shadow-mode evaluation before autonomy expansion.

### Core metrics

- recommendation count;
- accepted task rate;
- approval rate;
- rejection reason;
- human override rate;
- evidence completeness;
- unsupported assertion rate;
- policy conflict rate;
- unauthorized tool-call attempt rate;
- unsafe action attempt rate;
- incident count;
- cost per accepted task;
- last validation date.

### Exit criteria

- Every production agent has a unique identity, owner, version and revocation path.
- Governance team can reconstruct agent runs from evidence, policy, tools, approvals and outcomes.
- Agents cannot exceed their authority boundary even if model instructions attempt to do so.
- High-impact actions require the configured human approval and downstream authorization.
- Kill switch, credential revocation and tool revocation are tested.
- Shadow/evaluation evidence meets approved thresholds.
- Agent certification status is visible.

## 11. Milestone 8: Federated Regional Twin

### Objective

Connect multiple provinces and hospitals without moving raw patient-level data by default.

### Shared artifacts

- aggregate metrics;
- decision intelligence summaries;
- lessons learned;
- risk indicators;
- resource status;
- policy execution status.

### Exit criteria

- Regional users can coordinate planning and disaster response.
- Local data sovereignty is preserved.
- Federation governance is reviewed and documented.

## 12. Delivery cadence

Each milestone must produce:

1. user problem statement;
2. baseline;
3. target metric;
4. product specification;
5. evidence and data-source list;
6. prototype or implementation;
7. test evidence;
8. governance review;
9. release observation;
10. lesson learned.

## 13. Stop conditions

Pause or defer a twin if:

- no owner is assigned;
- data source is not governed;
- privacy risk is unresolved;
- user value is not measurable;
- the twin has no decision or task pathway;
- evidence cannot be traced.

## 14. Recommended first GitHub issues

1. Define MVP Hospital Twin data contract.
2. Define Department Twin workbench requirements.
3. Implement Decision Twin metadata schema.
4. Add Staff Twin and Role Memory boundary tests.
5. Add AI Agent Twin acceptance metrics.
6. Implement Role Twin + Person Overlay schema and boundary tests.
7. Implement Decision Episode + provenance schema.
8. Implement Agent Manifest schema and fail-closed compiler.
9. Implement Agent Identity / Permission registry and Tool Gateway contract.
10. Implement shadow-mode evaluator, Human Approval Gateway and kill-switch tests.
