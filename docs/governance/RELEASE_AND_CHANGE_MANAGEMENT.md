# HosPrime Release and Change Management

## 1. Purpose

This policy controls how HosPrime changes move from idea to production. It protects organizational knowledge, user trust, data integrity and AI accountability.

## 2. Branch model

- `main`: releasable, protected and evidence-backed.
- feature branches: one coherent change or epic slice.
- release branches: optional stabilization branch for pilot or production release.
- hotfix branches: urgent containment of production P0 or P1 issue.

Direct unreviewed changes to `main` are prohibited.

## 3. Pull request requirements

Every pull request must include:

1. problem and user value;
2. scope and non-scope;
3. linked issue or decision;
4. architecture and data impact;
5. AI or model impact;
6. security and privacy impact;
7. tests added or updated;
8. screenshots or API examples when relevant;
9. deployment and migration impact;
10. rollback plan;
11. acceptance evidence;
12. residual risks.

## 4. Required reviews

| Change type | Required review |
|---|---|
| Documentation only | owner or Delivery Lead |
| UI without data or authority change | frontend owner and Product Owner |
| API or domain change | backend owner and Architecture reviewer |
| Data model or migration | Data owner and Platform reviewer |
| Authentication or authorization | Security reviewer |
| AI prompt, model, retrieval or tool | AI Governance reviewer |
| Sensitive data handling | Privacy and Security reviewers |
| High-impact workflow | Business owner, Security and AI Governance |
| Production infrastructure | Platform owner and Release Authority |

An author cannot be the only approver of a high-risk change.

## 5. Automated checks

The protected branch should require:

- backend compile and tests;
- frontend TypeScript and production build;
- secret scan;
- dependency scan;
- static analysis;
- migration validation;
- API contract tests;
- RAG regression tests when AI behavior changes;
- authorization tests when route or role behavior changes.

## 6. Versioning

Use semantic versioning:

- MAJOR: incompatible API, data or governance change;
- MINOR: backward-compatible capability;
- PATCH: backward-compatible defect or security fix.

Agents, prompts, models, schemas and evaluation datasets also carry versions.

A release manifest records:

- application version;
- commit SHA;
- database revision;
- frontend build ID;
- agent versions;
- prompt versions;
- model providers and model IDs;
- evaluation dataset version;
- feature flags;
- deployment time and approver.

## 7. Release classes

### Experimental

- synthetic or controlled data;
- limited users;
- no production claim;
- no high-impact action.

### Internal alpha

- authenticated internal users;
- approved test data;
- enhanced monitoring;
- frequent breaking change allowed.

### Pilot

- selected real users and approved data;
- milestone gate passed;
- support, backup and incident response active;
- residual risk approved.

### Production

- full release evidence;
- security and privacy approval;
- reliability objectives;
- support ownership;
- rollback tested;
- benefit measurement active.

## 8. Feature flags

Future-milestone and high-risk capabilities are disabled by default.

Feature flags must specify:

- owner;
- purpose;
- environment;
- eligible roles or tenants;
- start and expiry date;
- monitoring;
- rollback condition.

A flag is not a substitute for authorization.

## 9. Database change policy

Production schema changes require:

- Alembic revision;
- forward and rollback path;
- data backup;
- dry run on production-like data;
- lock and downtime assessment;
- compatibility window where needed;
- post-migration validation.

`Base.metadata.create_all()` is development convenience only.

Destructive migration through a normal application endpoint is prohibited.

## 10. AI behavior change policy

The following changes require RAG or agent regression evaluation:

- model or provider;
- embedding model;
- chunking;
- retrieval filters;
- reranking;
- prompt or response contract;
- confidence logic;
- tool set;
- memory policy;
- source classification;
- fallback behavior.

The evaluation report compares the new candidate with the current approved baseline.

## 11. Release decision

The Release Authority chooses:

- GO;
- GO WITH CONDITIONS;
- HOLD;
- ROLLBACK;
- STOP.

The decision records:

- gate status;
- open defects;
- residual risks;
- monitoring plan;
- approver;
- date and release version.

## 12. Deployment procedure

1. freeze release candidate;
2. generate release manifest;
3. confirm backup;
4. apply migrations;
5. deploy backend and workers;
6. run readiness checks;
7. deploy frontend;
8. execute smoke tests;
9. enable feature flags progressively;
10. observe enhanced monitoring;
11. record final deployment status.

## 13. Rollback triggers

Rollback or disable the affected feature when:

- authentication or authorization fails;
- fabricated evidence rate exceeds threshold;
- sensitive data leakage occurs;
- error or latency exceeds release threshold;
- database integrity check fails;
- model cost anomaly is uncontrolled;
- high-impact action lacks valid approval;
- audit events are missing;
- Product Owner declares user harm.

## 14. Emergency change

Emergency change requires:

- incident or critical issue ID;
- minimum necessary scope;
- technical and security approval;
- backup and rollback;
- immediate smoke test;
- retrospective within two working days;
- permanent fix entered into backlog.

Emergency does not mean unrecorded.

## 15. Change request template

```text
Change ID:
Title:
Requester:
Problem:
Expected value:
Scope:
Non-scope:
Options considered:
Architecture impact:
Data impact:
Security/privacy impact:
AI/model impact:
Schedule impact:
Cost impact:
Risk impact:
Testing required:
Migration plan:
Rollback plan:
Recommendation:
Approver:
Decision and date:
```

## 16. Post-release review

Within five working days of pilot or production release, review:

- incidents and defects;
- quality and RAG metrics;
- adoption and task completion;
- cost;
- performance;
- user feedback;
- open conditions;
- lessons learned;
- next release decision.
