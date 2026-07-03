# HosPrime Twin User-Level Mapping

Status: Controlled product blueprint  
Scope: Users, work problems, twin families and MVP views

## 1. Purpose

This document maps HosPrime twin families to real user levels. It prevents building twins that have no user, no decision pathway and no measurable work outcome.

## 2. User levels

```text
L1 Regional / Provincial executive
L2 Hospital director and deputy director
L3 Department head and program manager
L4 Staff and operator
L5 Data, IT, security and governance team
```

## 3. L1 Regional / Provincial executive

### Primary work problems

- See cross-hospital and cross-district status.
- Prioritize resource allocation.
- Detect population health risk.
- Track policy execution.
- Coordinate disaster and PHEOC response.
- Understand budget, workforce and service-network gaps.

### Main twin families

```text
Provincial Twin
Regional Twin
Population Twin
Budget Twin
Policy Twin
Decision Twin
Incident Twin
```

### Required screens

- Provincial Situation Room
- Population Health Twin
- Resource and Workforce Map
- Risk and Incident Board
- Decision Timeline
- Policy Execution Dashboard

### Acceptance evidence

- User can identify top 5 system risks with evidence.
- User can trace a recommendation to source, owner and approval state.
- User can compare hospitals or districts without using raw patient-level data.

## 4. L2 Hospital director and deputy director

### Primary work problems

- Understand hospital status today.
- Manage OPD, ER, IPD, finance, claims and workforce pressure.
- Prioritize daily executive decisions.
- Track high-risk tasks and unresolved decisions.
- Review quality, safety and service plan performance.

### Main twin families

```text
Hospital Twin
Department Twin
Process Twin
Finance Twin
Workforce Twin
Quality Twin
Decision Twin
```

### Required screens

- Hospital Command View
- Daily Executive Brief
- Department Heatmap
- Bottleneck Analysis
- Decision Queue
- Outcome and Lesson Review

### Acceptance evidence

- User can complete daily review in less time than baseline.
- Each executive recommendation has evidence, confidence, policy reference and approval requirement.
- User can distinguish recommendation, approved plan and completed action.

## 5. L3 Department head and program manager

### Primary work problems

- Know current workload and backlog.
- Track department KPI.
- Manage staff pressure.
- Identify workflow bottlenecks.
- Convert meetings into tasks and follow-up.
- Report progress to executives.

### Main twin families

```text
Department Twin
Process Twin
Staff Twin
Project Twin
Quality Twin
Knowledge Twin
Decision Twin
```

### Required screens

- Department Workbench
- Workload and Backlog Board
- Process Bottleneck View
- Task Assignment Board
- Department Knowledge Panel
- Weekly Progress Brief

### Acceptance evidence

- User can identify the current bottleneck and responsible next action.
- User can prepare a department summary with approved evidence.
- User can assign and track tasks without losing decision context.

## 6. L4 Staff and operator

### Primary work problems

- Know what to do today.
- Find approved guidance quickly.
- Prepare routine documents and reports.
- Track personal or role-based tasks.
- Ask an AI copilot within permission boundaries.

### Main twin families

```text
Staff Twin
Role Twin
Task Twin
Knowledge Twin
Meeting Twin
AI Copilot Twin
```

### Required screens

- My Work Twin
- My Tasks
- My Knowledge
- Meeting Summary and Action Items
- Drafting Assistant
- Personal Evidence Pack

### Acceptance evidence

- User completes assigned work with accepted output.
- AI answer contains approved evidence or states that evidence is insufficient.
- Personal notes are not promoted to organizational memory without review.

## 7. L5 Data, IT, security and governance team

### Primary work problems

- Monitor data quality and source freshness.
- Monitor system and integration health.
- Review access, audit and security events.
- Validate agent behavior.
- Detect policy conflicts.
- Prepare maturity-gate evidence.

### Main twin families

```text
Data Twin
System Twin
AI Agent Twin
Governance Twin
Decision Twin
Knowledge Twin
```

### Required screens

- Data Quality Console
- Source Freshness Monitor
- AI Agent Reliability Dashboard
- Policy Conflict Dashboard
- Audit Export Console
- Maturity Gate Evidence Board

### Acceptance evidence

- Team can identify missing, stale or conflicting data sources.
- Team can inspect agent output quality and evidence completeness.
- Team can export audit evidence for governance review.

## 8. MVP user coverage

The first controlled MVP should cover these users:

```text
Hospital director
Department head
Staff/operator
Data/governance reviewer
```

MVP twin families:

```text
Hospital Twin
Department Twin
Staff Twin
Process Twin
Decision Twin
Knowledge Twin
AI Agent Twin Lite
```

## 9. What not to build first

Do not begin with:

- fully autonomous action;
- unrestricted individual patient twin;
- national federation;
- complex 3D visualization;
- AI agent marketplace;
- real-time IoT-heavy architecture.

These are later capabilities and must pass privacy, security, clinical and governance gates first.

## 10. Product rule

A twin screen is accepted only when it helps a user complete a real task faster, safer or with better evidence. A screen that only displays status without decision pathway is not enough.
