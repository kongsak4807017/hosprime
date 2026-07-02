# HosPrime Project Control System

## 1. Purpose

This document defines how HosPrime is directed, controlled, inspected and accepted. It converts the project from feature-driven development into evidence-driven delivery.

The control system applies to:

- product scope;
- architecture;
- data and knowledge;
- AI agents and models;
- security and privacy;
- software quality;
- budget and model cost;
- user adoption;
- milestone acceptance;
- release and change management.

## 2. Governance structure

### 2.1 Executive Sponsor

Accountable for strategic alignment, funding, cross-organization authority and final milestone acceptance.

Approves:

- project charter;
- annual budget;
- milestone entry and exit;
- high-impact production use cases;
- material scope or risk changes.

### 2.2 Product Owner

Accountable for product value and user outcomes.

Owns:

- product backlog;
- user priorities;
- acceptance criteria;
- pilot selection;
- adoption and benefit realization.

### 2.3 Delivery Lead / PMO

Accountable for schedule, dependencies, reporting and evidence packs.

Owns:

- integrated plan;
- sprint and milestone tracking;
- risk and issue registers;
- change log;
- status reporting;
- decision follow-up.

### 2.4 Architecture Review Board

Members should cover product architecture, software architecture, data architecture, security and AI engineering.

Approves:

- bounded contexts;
- new platform dependencies;
- database and event contracts;
- integration patterns;
- technical debt exceptions;
- architecture decision records.

### 2.5 Data Governance Council

Accountable for organizational data and knowledge quality.

Owns:

- data and document ownership;
- classification;
- retention;
- metadata standards;
- source approval;
- lineage;
- quality rules;
- access policy.

### 2.6 AI Governance Board

Accountable for safe, explainable and cost-controlled AI behavior.

Owns:

- agent registry;
- model approval;
- tool permissions;
- evaluation standards;
- human approval matrix;
- prohibited behavior;
- drift and incident review.

### 2.7 Security and Privacy Lead

Accountable for cybersecurity, PDPA controls and incident response.

Owns:

- threat model;
- access reviews;
- secret management;
- vulnerability management;
- privacy impact assessment;
- security incident handling.

### 2.8 Domain and Safety Reviewers

Public-health, clinical, legal, finance, HR and procurement reviewers validate domain-specific content and risks. AI output does not replace their professional authority.

## 3. Decision rights

| Decision | Recommends | Reviews | Approves |
|---|---|---|---|
| Product priority | Product Owner | Delivery Lead, users | Executive Sponsor |
| Architecture change | Technical Lead | Architecture Board | Architecture Board Chair |
| New data source | Data Steward | Data Governance, Security | Data Owner |
| New AI model | AI Lead | Security, AI Governance | AI Governance Board |
| New agent/tool permission | Agent Owner | AI Governance, Security | Authorized business owner |
| Production release | Delivery Lead | QA, Security, Product Owner | Release Authority |
| High-impact automated action | Product Owner | Domain, Legal, Security | Executive Sponsor |
| Emergency change | Technical Lead | Security | Emergency Change Authority |

## 4. Delivery hierarchy

Every item must trace through this hierarchy:

```text
Vision
  -> Strategic outcome
  -> Milestone
  -> Epic
  -> Feature
  -> User story
  -> Acceptance criterion
  -> Test evidence
  -> Release evidence
  -> Measured outcome
```

No item is considered complete because code exists. Completion requires acceptance evidence and an accountable owner.

## 5. Core control artifacts

The repository must maintain:

1. Project Charter
2. Product Roadmap
3. Architecture Decision Records
4. Product Backlog
5. Requirements Traceability Matrix
6. Risk Register
7. Issue Log
8. Dependency Log
9. Change Log
10. Data Source Register
11. Agent Registry
12. Model Registry
13. Test and Evaluation Plan
14. Release Evidence Pack
15. Benefit Realization Scorecard
16. Post-implementation Review

## 6. Cadence

### Daily delivery control

- blocker review;
- failed build review;
- security alert review;
- critical defect review;
- decision and dependency updates.

Output: updated board and owner for every blocker.

### Weekly product and delivery review

- planned versus completed work;
- milestone burn-up;
- open risks and issues;
- quality trend;
- model cost;
- user feedback;
- decisions required.

Output: one-page weekly status report.

### Fortnightly architecture and AI review

- architecture deviations;
- new dependencies;
- agent or model changes;
- retrieval and grounding metrics;
- privacy and security findings;
- technical debt.

Output: approved ADRs and remediation actions.

### Monthly steering committee

- overall RAG status;
- budget and forecast;
- benefit realization;
- milestone confidence;
- scope changes;
- unresolved P0/P1 risks;
- go, hold, reduce scope or stop decision.

Output: steering decision log.

### Quarterly value review

- adoption;
- time saved;
- decision quality;
- knowledge reuse;
- safety performance;
- total cost of ownership;
- roadmap re-prioritization.

Output: benefit realization report.

## 7. RAG status rules

### Green

- milestone forecast within 10 percent of approved schedule;
- no unresolved P0 issue;
- P1 risks have funded mitigation;
- quality gates are passing;
- budget variance within 10 percent.

### Amber

- schedule or budget variance between 10 and 20 percent;
- one or more P1 issues threaten the milestone;
- quality trend is declining;
- dependency or data readiness is uncertain.

Amber requires a dated recovery plan and named owner.

### Red

- unresolved P0 security, privacy or safety issue;
- milestone acceptance cannot be achieved with current scope;
- variance greater than 20 percent;
- evidence or audit integrity is compromised;
- production claims exceed proven capability.

Red requires immediate escalation and a go, hold or stop decision.

## 8. Priority definitions

### P0 — Critical

Potential unauthorized disclosure, fabricated evidence, unauthorized action, data corruption, credential exposure or production outage.

Response: contain immediately, same-day owner and executive notification.

### P1 — High

Blocks milestone acceptance or creates significant trust, compliance, reliability or adoption risk.

Response: remediation committed in the current sprint or accepted by governance.

### P2 — Medium

Material defect or debt that does not immediately block the milestone.

Response: prioritized within two sprints.

### P3 — Low

Improvement, optimization or cosmetic issue.

Response: backlog prioritization.

## 9. Change control

A change request is required when any proposal affects:

- approved milestone scope;
- delivery date;
- budget;
- data classification;
- AI risk tier;
- external integration;
- production infrastructure;
- human approval authority;
- legal or privacy obligations.

Each change request must include:

1. problem and rationale;
2. options considered;
3. impact on scope, time, cost and risk;
4. architecture impact;
5. data and security impact;
6. testing impact;
7. rollback plan;
8. recommendation;
9. approver and decision date.

## 10. Evidence-based milestone control

Each milestone has an evidence folder containing:

- approved scope;
- acceptance criteria;
- architecture diagram;
- threat model;
- data inventory;
- test results;
- evaluation report;
- defect summary;
- user acceptance sign-off;
- cost report;
- release and rollback plan;
- residual-risk acceptance;
- final go/no-go decision.

A presentation or live demo is supporting evidence, not acceptance evidence by itself.

## 11. Stop conditions

Development or release must stop when:

- a secret or sensitive dataset is exposed;
- AI produces fabricated evidence without clear containment;
- a high-impact action can execute without authorized approval;
- audit records are missing or alterable without control;
- a production release has no rollback path;
- source ownership or lawful use cannot be established;
- the milestone cannot be evaluated objectively.

## 12. Definition of project success

HosPrime is successful only when all four conditions are met:

1. **Useful:** users repeatedly complete valuable work with the platform.
2. **Trusted:** answers and actions are evidence-based, explainable and governed.
3. **Operable:** the platform is secure, reliable, supportable and cost-controlled.
4. **Impactful:** measurable organizational outcomes improve without unacceptable harm.
