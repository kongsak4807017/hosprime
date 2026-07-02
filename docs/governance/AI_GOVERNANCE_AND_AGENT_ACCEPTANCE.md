# HosPrime AI Governance and Agent Acceptance

## 1. Principle

An HosPrime agent is a governed digital workforce role, not a prompt and not an autonomous employee.

Every agent must have:

- unique identity;
- mission;
- accountable human owner;
- approved capabilities;
- explicit knowledge scope;
- tool allowlist;
- forbidden actions;
- authority level;
- human approval requirements;
- model and prompt version;
- memory policy;
- evaluation dataset;
- cost budget;
- monitoring and retirement plan.

## 2. Canonical agent specification

```yaml
agent_id: CORE-KNOWLEDGE-001
name: Knowledge Agent
version: 1.0.0
family: Core Office
mission: Retrieve and explain approved organizational knowledge.
owner: Knowledge Management Lead
risk_tier: medium
authority_level: recommend
knowledge_scopes:
  - approved_documents
  - approved_graph_edges
capabilities:
  - search
  - retrieve
  - summarize
  - compare_sources
tools:
  allowed:
    - knowledge_search
    - graph_read
  prohibited:
    - external_send
    - record_delete
    - policy_approve
citation_required: true
human_approval:
  required_for:
    - public_release
    - policy_interpretation
memory:
  working: task_session
  episodic: reviewed_interactions
  organizational_promotion: human_review_required
models:
  primary: approved-model-id
  fallback: retrieval-only
budget:
  daily_tokens: 50000
  maximum_cost_usd: 10
success_metrics:
  - groundedness
  - citation_precision
  - task_acceptance
```

## 3. Authority levels

### Level 0 — Discover

May find and display authorized information. No generated recommendation.

### Level 1 — Explain

May summarize and explain evidence. Must cite sources.

### Level 2 — Recommend

May compare options and recommend. Must expose evidence, assumptions, uncertainty and alternatives.

### Level 3 — Prepare

May create drafts, plans or work products. Output remains unapproved.

### Level 4 — Execute low-risk reversible action

Permitted only for explicitly authorized tools and scopes. Must create execution receipt and audit event.

### Level 5 — High-impact execution

Not autonomously permitted. Requires authenticated human approval and, where applicable, dual approval.

## 4. Agent risk tiers

### Low

Read-only retrieval of non-sensitive approved knowledge.

### Medium

Generated summaries, analysis, recommendations or access to internal data.

### High

Sensitive data, financial, workforce, legal, clinical or public-communication outputs.

### Critical

Actions affecting clinical care, legal rights, procurement, payment, employment, public orders or external systems.

Critical agents remain human-controlled and cannot approve their own output.

## 5. Agent lifecycle

```text
Draft
  -> Sandbox
  -> Evaluated
  -> Governance Review
  -> Pilot
  -> Certified
  -> Production
  -> Suspended
  -> Retired
```

### Draft

Mission and specification exist. No user access.

### Sandbox

Uses synthetic or approved test data. No production tools.

### Evaluated

Passes task, safety, cost and failure-mode tests.

### Governance Review

AI Governance, Security, Data Owner and Business Owner approve scope.

### Pilot

Limited users, data and budget. Enhanced monitoring.

### Certified

Acceptance evidence and residual risk approved.

### Production

Operates within certified version and scope.

### Suspended

Temporarily disabled due to incident, drift or policy change.

### Retired

Removed from active use; records and decisions retained according to policy.

## 6. Acceptance checklist

An agent cannot enter pilot until all items pass.

### Identity and ownership

- unique agent ID;
- business owner;
- technical owner;
- purpose and non-purpose;
- user groups;
- risk tier.

### Knowledge and data

- approved sources only;
- access filters tested;
- source freshness rules;
- data classification;
- retention and deletion;
- no unauthorized model training.

### Behavior

- test scenarios versioned;
- no-answer behavior;
- uncertainty behavior;
- conflicting-source behavior;
- prompt-injection resistance;
- prohibited-action refusal;
- sensitive-content handling.

### Tools

- minimum tool allowlist;
- parameter validation;
- idempotency where applicable;
- timeout and retry policy;
- execution receipt;
- rollback or compensation;
- rate and cost limits.

### Human control

- approval matrix;
- authenticated approver;
- separation of duties;
- approval expiry;
- rejection and rework flow;
- no self-approval.

### Monitoring

- task success;
- groundedness;
- user acceptance;
- latency;
- errors;
- tool failures;
- token and cost;
- policy violations;
- model and prompt version.

## 7. Core Office strategy

HosPrime begins with five stable roles:

1. Executive Agent
2. Planner Agent
3. Analyst Agent
4. Knowledge Agent
5. Action Agent

Department and program behavior should be implemented primarily through:

- capability configuration;
- knowledge packs;
- role context;
- tool permissions;
- workflow templates.

A new agent is created only when it has a distinct mission, owner, risk profile and evaluation set. This controls Agent Explosion.

## 8. Multi-agent council rules

AI Council may be used when a decision requires distinct perspectives.

Required outputs:

- question and decision boundary;
- evidence used by each role;
- assumptions;
- recommendation;
- disagreement or dissent;
- risk and uncertainty;
- missing information;
- final human decision.

The Executive Agent synthesizes but does not erase dissent. Agents cannot create circular citations from each other's output. Every factual claim must trace to approved evidence.

## 9. Memory governance

### Working memory

Temporary task context. Deleted according to session policy.

### Episodic memory

Reviewed interaction history that may improve continuity.

### Role memory

Institutional knowledge associated with a position, not a person.

### Person memory

Personal preferences and working context, accessible only to the authorized person and approved services.

### Organization memory

Reviewed decisions, outcomes and lessons owned by the organization.

Promotion from conversation to shared memory requires:

- source;
- reviewer;
- classification;
- effective date;
- owner;
- correction and deletion path.

## 10. Prohibited agent behavior

Agents must not:

- invent facts, sources, pages, metrics or actions;
- claim execution without a verified receipt;
- bypass authentication or approval;
- expose restricted information;
- change their own authority or tool list;
- silently switch provider identity;
- hide uncertainty or disagreement;
- treat personal preference as organizational policy;
- make final clinical, legal, employment, procurement or payment decisions;
- learn from unreviewed sensitive content into shared memory.

## 11. Model and prompt change control

A model, system prompt, retrieval policy or tool change requires re-evaluation when it can affect:

- factual output;
- access behavior;
- authority;
- cost;
- latency;
- safety;
- data residency;
- user experience.

Major changes require a new agent version and pilot evidence. Emergency rollback must be possible without database reconstruction.

## 12. Agent suspension triggers

Immediately suspend an agent when:

- fabricated evidence is confirmed;
- unauthorized access occurs;
- prohibited tool call succeeds;
- high-impact action lacks valid approval;
- quality falls below the minimum threshold;
- budget anomaly exceeds escalation limit;
- source or model licensing becomes uncertain;
- an owner requests suspension.
