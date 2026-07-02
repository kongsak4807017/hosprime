# HosPrime Maturity Gates

## 1. Purpose

Maturity gates prevent prototype breadth from being mistaken for production readiness. A module may exist in code and still remain experimental.

Gate status is one of:

- `NOT_STARTED`
- `IN_PROGRESS`
- `EVIDENCE_INCOMPLETE`
- `PASS_WITH_CONDITIONS`
- `PASS`
- `FAILED`

Only `PASS` permits unrestricted progression. `PASS_WITH_CONDITIONS` requires a named owner, due date and accepted residual risk.

## 2. Global Gate 0 — Security and Delivery Foundation

This gate applies before any milestone pilot.

### Required evidence

- no active credential in source, documentation or build artifacts;
- exposed credentials revoked or rotated;
- authenticated access on every non-public route;
- role matrix approved;
- production configuration fails closed;
- secure upload limits and filename handling;
- dependency inventory and vulnerability scan;
- automated backend and frontend build checks;
- database migration strategy;
- backup and restore test;
- incident response owner and process;
- rollback procedure.

### Pass criteria

- zero unresolved P0 finding;
- zero critical known vulnerability without approved containment;
- all protected-route tests pass;
- CI passes on the release commit;
- restore test meets agreed recovery objectives.

## 3. Milestone 1 — Governed Knowledge Oracle

### Gate M1-A: Source and ingestion readiness

Required:

- at least 100 approved documents across five knowledge packs;
- named owner for every document;
- source, version, classification and review date captured;
- duplicate detection;
- file parsing success greater than or equal to 95 percent;
- failed documents visible and recoverable;
- restricted documents inaccessible to unauthorized roles.

### Gate M1-B: Retrieval readiness

Evaluation set:

- at least 100 answerable questions;
- at least 30 unanswerable questions;
- at least 20 ambiguous or conflicting-source questions;
- representation from every knowledge pack.

Pass criteria:

- Recall@5 greater than or equal to 0.85;
- Mean Reciprocal Rank greater than or equal to 0.70;
- source access violations equal to zero;
- duplicate or obsolete source rate below 5 percent;
- p95 retrieval latency below 2 seconds under pilot load.

### Gate M1-C: Answer and citation trust

Pass criteria:

- material-claim groundedness greater than or equal to 0.90;
- citation precision greater than or equal to 0.90;
- citation completeness greater than or equal to 0.90;
- false factual answer rate on unanswerable questions below 2 percent;
- explicit uncertainty present when sources conflict;
- no fabricated document title, page or metric;
- every answer records model, prompt version, evidence IDs and cost.

### Gate M1-D: User acceptance

Pass criteria:

- at least 15 pilot users across leadership, program and knowledge roles;
- at least 80 percent task completion on approved scenarios;
- median usefulness score at least 4 of 5;
- median trust score at least 4 of 5;
- at least 30 percent median time reduction for target knowledge tasks;
- all high-severity user findings resolved or accepted.

### Gate M1-E: Pilot release

Required:

- production-like deployment;
- support owner and operating procedure;
- usage, failure, cost and quality dashboards;
- release and rollback rehearsal;
- approved residual-risk register;
- executive go/no-go decision.

## 4. Milestone 2 — Organization Memory

Entry requirement: Milestone 1 pilot gate passed.

### Required domain model

- Meeting
- Agenda
- Participant
- Evidence
- Decision
- Decision Rationale
- Alternative Considered
- Action
- Owner
- Due Date
- Outcome
- Lesson Learned

### Pass criteria

- decision extraction precision at least 0.90 on reviewed meetings;
- action-owner extraction precision at least 0.95;
- 100 percent of promoted decisions reviewed by an authorized human;
- no decision promoted without source transcript or document evidence;
- overdue actions measurable and attributable;
- meeting-to-decision-to-outcome traceability demonstrated end to end;
- memory correction and deletion workflow tested.

## 5. Milestone 3 — Executive Office and Role Twin

Entry requirement: Organization Memory gate passed.

### Pass criteria

- five Core Office roles use a shared capability registry;
- every Role Twin has authority, knowledge and memory boundaries;
- Person Memory and Role Memory are separated;
- role succession test proves knowledge continuity;
- Executive Brief metrics have approved semantic definitions;
- recommendations expose evidence, assumptions, confidence and alternatives;
- user adoption at least 60 percent weekly active use among pilot executives;
- no strategic action executes without authorized approval.

## 6. Milestone 4 — Backoffice AI Workforce and AIOC

Entry requirement: Executive Office gate passed.

### Pass criteria

- every agent registered with owner, version, risk tier and permitted tools;
- agent health, latency, failure, cost and quality visible in AIOC;
- DataOps quality rules cover at least 90 percent of critical datasets;
- knowledge freshness and expiry measurable;
- prompt and tool security tests pass;
- agent rollback and retirement tested;
- agent-to-agent communication limited by explicit workflow contracts;
- autonomous execution restricted to low-risk reversible operations.

## 7. Milestone 5 — Forecast, Scenario and Provincial Health Brain

Entry requirement: governed data layer and AIOC gates passed.

### Pass criteria

- every model has owner, purpose, dataset, version and validation report;
- temporal holdout and backtesting completed;
- baseline model comparison documented;
- calibration and error by population segment reported;
- drift monitoring active;
- scenario assumptions editable and visible;
- forecast is never represented as certainty;
- policy recommendation separates observed facts, forecast and value judgment;
- executive users can inspect uncertainty and alternative scenarios;
- post-decision outcomes feed back into model and organizational learning.

## 8. Gate review procedure

1. Delivery Lead submits evidence pack.
2. Quality Lead checks completeness.
3. Security, Data and AI Governance review their domains.
4. Product Owner verifies user value and acceptance.
5. Architecture Board records deviations and debt.
6. Release Authority records `PASS`, `PASS_WITH_CONDITIONS` or `FAILED`.
7. Conditions become tracked issues with owner and due date.

## 9. Anti-bypass rule

A future-milestone prototype may be demonstrated, but it must be labeled:

```text
EXPERIMENTAL — NOT MILESTONE ACCEPTED — NOT FOR PRODUCTION DECISION OR EXECUTION
```

No screen label, route name, class name or marketing statement can override gate status.
