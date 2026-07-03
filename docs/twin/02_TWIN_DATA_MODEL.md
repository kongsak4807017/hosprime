# HosPrime Twin Data Model

Status: Controlled data-model blueprint  
Scope: Twin of Everything foundation

## 1. Purpose

This document defines the minimum metadata model for HosPrime twins. It is technology-neutral and can be implemented in PostgreSQL, Neo4j, RDF/PROV-O or a hybrid architecture.

The model must support evidence, decision traceability, human approval and organizational learning without exposing unnecessary sensitive data.

## 2. Core entity: Twin

```yaml
Twin:
  twin_id: string
  twin_type: enum
  name: string
  description: string
  owner_role_id: string
  organization_unit_id: string
  maturity_level: enum
  status: enum
  classification: enum
  data_sources: list
  knowledge_sources: list
  related_twins: list
  kpis: list
  risks: list
  tasks: list
  decisions: list
  agents: list
  audit_requirements: list
  created_at: datetime
  updated_at: datetime
  reviewed_at: datetime
```

## 3. Required common fields

### twin_id

Globally unique twin identifier. It must not depend on display name because organizational names change.

### twin_type

Controlled vocabulary from `01_TWIN_TAXONOMY.md`.

### owner_role_id

The accountable business or governance role. Technical teams may operate the twin, but they do not own the business meaning.

### organization_unit_id

The unit responsible for the twin or primarily affected by it.

### maturity_level

```text
L0 Concept
L1 Manual profile
L2 Data-connected
L3 Evidence-linked
L4 Decision-linked
L5 Outcome-learning
```

### status

```text
GREEN
YELLOW
RED
GRAY
```

### classification

```text
PUBLIC
INTERNAL
CONFIDENTIAL
RESTRICTED
```

## 4. Relationship model

```yaml
TwinRelationship:
  source_twin_id: string
  relationship_type: enum
  target_twin_id: string
  evidence_ref: optional string
  confidence: optional float
  valid_from: optional datetime
  valid_to: optional datetime
```

Recommended relationship types:

```text
owns
belongs_to
reports_to
depends_on
supports
impacts
uses_data_from
uses_knowledge_from
produces_decision
executes_task
monitored_by
approved_by
conflicts_with
learns_from
```

## 5. Data source reference

```yaml
DataSourceRef:
  source_id: string
  source_name: string
  source_type: enum
  owner_role: string
  refresh_policy: string
  quality_status: enum
  classification: enum
  provenance_required: boolean
```

Source types:

```text
HIS
HOSxP
LIS
PACS
ERP
HR
Inventory
Manual Upload
Meeting Record
Approved Document
External Public Source
Surveillance System
```

## 6. KPI reference

```yaml
KPIRef:
  kpi_id: string
  name: string
  definition: string
  numerator: optional string
  denominator: optional string
  threshold_green: optional string
  threshold_yellow: optional string
  threshold_red: optional string
  source_of_truth: string
  last_value: optional number
  last_updated: optional datetime
```

Every KPI must have a single source of truth. Conflicting definitions must be recorded as governance risks.

## 7. Decision reference

```yaml
DecisionRef:
  decision_id: string
  decision_type: enum
  context: string
  recommendation: string
  evidence_refs: list
  policy_refs: list
  alternatives: list
  confidence: optional float
  risk_level: enum
  approval_state: enum
  approver_role_id: optional string
  outcome_ref: optional string
```

Approval states:

```text
DRAFT
RECOMMENDED
NEEDS_REVIEW
APPROVED_NOT_EXECUTED
APPROVED_EXECUTED
REJECTED
DEFERRED
CLOSED_WITH_LESSON
```

## 8. Staff Twin profile

```yaml
StaffTwin:
  twin_id: string
  role_ref: string
  department_ref: string
  responsibility_map: list
  active_tasks: list
  assigned_kpis: list
  workload_indicators: list
  competency_profile: list
  knowledge_permissions: list
  decision_participation: list
```

Privacy note: person memory, staff twin memory and role memory must remain separated until promotion is reviewed and approved.

## 9. Department Twin profile

```yaml
DepartmentTwin:
  twin_id: string
  department_code: string
  head_role_twin_id: string
  service_scope: list
  processes: list
  staff_twins: list
  kpis: list
  risks: list
  backlog: list
  decisions: list
```

## 10. Process Twin profile

```yaml
ProcessTwin:
  twin_id: string
  process_name: string
  start_event: string
  end_event: string
  steps: list
  owner_role: string
  departments: list
  systems: list
  bottleneck_indicators: list
  improvement_actions: list
```

## 11. AI Agent Twin profile

```yaml
AIAgentTwin:
  twin_id: string
  agent_id: string
  role: string
  owner_role: string
  risk_tier: enum
  allowed_tools: list
  allowed_data_domains: list
  prohibited_actions: list
  recommendation_count: integer
  approval_rate: float
  evidence_completeness_rate: float
  policy_conflict_rate: float
  incident_count: integer
  last_validation_date: datetime
```

## 12. Audit event

```yaml
AuditEvent:
  audit_id: string
  twin_id: string
  event_type: enum
  actor_role: string
  actor_type: enum
  timestamp: datetime
  input_ref: optional string
  output_ref: optional string
  evidence_refs: list
  decision_ref: optional string
  result: enum
```

Event types:

```text
VIEWED
UPDATED
RECOMMENDED
APPROVED
REJECTED
EXECUTION_RECORDED
EXPORTED
ESCALATED
POLICY_CONFLICT_DETECTED
```

## 13. Graph implementation guidance

Recommended graph node labels:

```text
Twin
Organization
Department
Role
Process
KPI
Risk
Task
Decision
Evidence
Policy
Agent
Outcome
Lesson
```

Recommended edges:

```text
OWNS
BELONGS_TO
DEPENDS_ON
IMPACTS
USES_EVIDENCE
REFERENCES_POLICY
RECOMMENDS
APPROVES
RECORDS_EXECUTION
PRODUCES_OUTCOME
LEARNS_FROM
```

## 14. Minimum viable schema

For MVP, implement only these tables or graph nodes first:

1. twin
2. twin_relationship
3. twin_kpi
4. twin_decision
5. twin_audit_event
6. twin_data_source

This is sufficient to support Hospital Twin, Department Twin, Staff Twin, Process Twin and Decision Twin without over-engineering.
