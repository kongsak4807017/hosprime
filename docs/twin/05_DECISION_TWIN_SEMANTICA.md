# Decision Twin and Semantica Integration Blueprint

Status: Controlled architecture blueprint  
Scope: Decision Intelligence Layer for HosPrime Twin Ecosystem

## 1. Purpose

This document defines how a Semantica-style decision intelligence layer should support HosPrime twins. The intent is not to replace the core HosPrime architecture, data mart, knowledge store, vector store or agent framework. The intent is to add context, provenance, governance and explainability around recommendations and decisions.

## 2. Architectural role

```text
Agent Orchestrator
        |
        v
Decision Intelligence Layer
        |
        +-- Context Graph
        +-- Decision Graph
        +-- Evidence Graph
        +-- Policy Graph
        +-- Provenance Graph
        +-- Outcome and Lesson Graph
        |
        v
Knowledge Graph / Data Mart / Audit Store
```

The layer should record how a recommendation was created, what evidence was used, what policy was referenced, what uncertainty or conflict existed, who approved it and what outcome followed.

## 3. Why this matters

Healthcare and public-health AI cannot depend on memory alone. It needs accountable reasoning. For every important recommendation, HosPrime should preserve a reviewable path:

```text
Context -> Evidence -> Reasoning -> Recommendation -> Approval -> Execution Record -> Outcome -> Lesson
```

## 4. Decision Twin schema

```yaml
DecisionTwin:
  decision_id: string
  decision_type: enum
  source_twin_id: string
  requesting_user_role: string
  responsible_owner_role: string
  context_summary: string
  recommendation: string
  alternatives: list
  evidence_refs: list
  policy_refs: list
  data_freshness: string
  confidence: optional float
  uncertainty_notes: string
  conflict_flags: list
  risk_level: enum
  approval_required: boolean
  approval_state: enum
  outcome_state: enum
  lesson_ref: optional string
  created_at: datetime
  reviewed_at: optional datetime
```

## 5. Decision types

```text
INFORMATIONAL_SUMMARY
OPERATIONAL_RECOMMENDATION
FINANCIAL_RECOMMENDATION
WORKFORCE_RECOMMENDATION
QUALITY_OR_SAFETY_RECOMMENDATION
GOVERNANCE_REVIEW
POLICY_INTERPRETATION
INCIDENT_RESPONSE
RESOURCE_ALLOCATION
```

## 6. Governance states

```text
DRAFT
AI_RECOMMENDED
HUMAN_REVIEW_REQUIRED
APPROVED_NOT_EXECUTED
EXECUTION_RECORDED
REJECTED
DEFERRED
CLOSED_WITH_OUTCOME
CLOSED_WITH_LESSON
```

The system must not claim real-world execution unless an execution record exists.

## 7. Evidence graph

Each decision should connect to evidence nodes:

```text
Decision --USES_EVIDENCE--> Evidence
Evidence --DERIVED_FROM--> DataSource
Evidence --HAS_FRESHNESS--> Timestamp
Evidence --HAS_CLASSIFICATION--> Classification
```

Evidence examples:

- KPI value;
- data mart metric;
- approved document;
- meeting record;
- incident report;
- policy;
- prior decision;
- validated external source.

## 8. Policy graph

Each decision should connect to policy nodes when policy affects authority, privacy, finance, procurement, clinical safety, cybersecurity or public communication.

```text
Decision --REFERENCES_POLICY--> Policy
Decision --REQUIRES_APPROVAL_FROM--> Role
Decision --HAS_CONFLICT_WITH--> Policy
```

## 9. Provenance requirements

Every decision record must store enough metadata to answer:

1. Which agent or user produced the recommendation?
2. Which twin was the recommendation about?
3. Which evidence was used?
4. Which assumptions were made?
5. Which policy or rule constrained the recommendation?
6. Which human role approved or rejected it?
7. What happened afterward?

## 10. Agent integration pattern

```text
Agent Output
    -> Convert to DecisionTwin candidate
    -> Validate required evidence
    -> Run governance and policy checks
    -> Assign approval state
    -> Record audit event
    -> Display recommendation with evidence and next action
```

## 11. Minimum viable integration

MVP should implement only four functions first:

1. create_decision_candidate
2. attach_evidence
3. record_human_review
4. close_with_outcome_or_lesson

## 12. Example: ER surge recommendation

```yaml
decision_type: OPERATIONAL_RECOMMENDATION
source_twin_id: TWIN-HOSP-ER-2026-0001
context_summary: ER boarding and bed pressure above agreed threshold.
recommendation: Review surge bed plan and accelerate discharge coordination.
evidence_refs:
  - ER boarding metric
  - bed occupancy metric
  - staffing pressure metric
policy_refs:
  - hospital surge SOP
  - patient safety escalation policy
approval_required: true
approval_state: HUMAN_REVIEW_REQUIRED
outcome_state: PENDING
```

## 13. Example: PDPA-sensitive recommendation

```yaml
decision_type: GOVERNANCE_REVIEW
source_twin_id: TWIN-DATA-2026-0001
context_summary: Proposed data sharing includes restricted patient-level fields.
recommendation: Do not share patient-level data until DPO review and de-identification are completed.
policy_refs:
  - privacy classification policy
  - data sharing policy
conflict_flags:
  - restricted_data_sharing
approval_required: true
approval_state: HUMAN_REVIEW_REQUIRED
```

## 14. Dashboard requirements

The first Decision Twin dashboard should include:

- decision timeline;
- open decision queue;
- evidence completeness;
- policy conflict list;
- approval state;
- outcome state;
- lessons learned awaiting review.

## 15. Safety boundary

Decision intelligence is not an autonomous execution engine. It records, explains and governs decisions. High-impact action still requires authorized human approval and an execution record.

## 16. Future expansion

Future work may include:

- RDF/PROV-O export;
- SHACL-style policy validation;
- SPARQL decision search;
- graph-based precedent search;
- agent reliability scoring;
- audit package export for governance review.
