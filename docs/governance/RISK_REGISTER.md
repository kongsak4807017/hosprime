# HosPrime Risk Register

## Scoring

- Likelihood: 1 rare to 5 almost certain
- Impact: 1 minor to 5 catastrophic
- Score: likelihood multiplied by impact
- 15–25: Red
- 8–14: Amber
- 1–7: Green

The register is reviewed weekly and at every milestone gate.

| ID | Risk | L | I | Score | Owner | Primary mitigation | Trigger / indicator | Contingency |
|---|---|---:|---:|---:|---|---|---|---|
| R-001 | Credential remains usable after source exposure | 4 | 5 | 20 | Security Lead | Revoke, rotate, restrict and scan history | provider usage after exposure | disable provider integration and investigate logs |
| R-002 | AI fabricates facts, numbers or citations | 4 | 5 | 20 | AI Lead | no-evidence refusal, groundedness tests, claim-level citation | unsupported claim or invented source | suspend factual generation and revert to retrieval-only mode |
| R-003 | Unauthorized user reads restricted documents | 3 | 5 | 15 | Security Lead | authenticated routes, ABAC, document classification tests | access-policy test failure | isolate affected tenant and revoke sessions |
| R-004 | High-impact workflow is executed without approval | 3 | 5 | 15 | AI Governance Lead | plan-only default, HITL, tool allowlist, execution receipts | action without approval token | disable executor and begin incident response |
| R-005 | System claims action completed when only planned | 4 | 4 | 16 | Product Owner | explicit execution states and evidence receipt | `completed` without tool record | relabel records and suspend workflow feature |
| R-006 | Pseudo-embeddings produce misleading retrieval | 3 | 4 | 12 | AI Lead | disabled by default; production guard | pseudo mode enabled outside isolated test | rebuild indexes with approved embeddings |
| R-007 | Similarity score is treated as correctness confidence | 4 | 4 | 16 | AI Lead | calibrated evaluation and separate confidence dimensions | dashboards label cosine as answer confidence | remove confidence display and recalibrate |
| R-008 | Citation list includes sources that do not support claims | 4 | 4 | 16 | Knowledge Lead | claim-evidence verifier and citation precision test | reviewer finds unsupported citation | switch to quote-first evidence display |
| R-009 | Obsolete policy remains active in Knowledge Oracle | 4 | 4 | 16 | Knowledge Owner | expiry, owner and review date required | source beyond review date | quarantine expired source and notify owner |
| R-010 | Sensitive prompts or outputs are stored in logs | 4 | 5 | 20 | Privacy Lead | redaction, field classification, minimized logging | personal or health data in AgentLog | purge affected logs and revise logging policy |
| R-011 | File upload contains malware or decompression attack | 3 | 5 | 15 | Security Lead | size limits, file inspection, malware scanning, sandbox parsing | scanner alert or parser resource spike | quarantine storage and stop ingestion |
| R-012 | Path traversal or unsafe filename writes outside storage | 3 | 5 | 15 | Technical Lead | generated storage IDs and safe path handling | unexpected path in storage record | disable uploads and inspect filesystem |
| R-013 | Database fallback silently moves production to SQLite | 3 | 5 | 15 | Platform Lead | fail closed in production; readiness check | primary DB unavailable and SQLite created | stop service and restore primary DB |
| R-014 | `create_all` causes uncontrolled production schema changes | 3 | 4 | 12 | Platform Lead | Alembic and deployment migration job | schema created during app startup | stop release and restore migration baseline |
| R-015 | Data migration endpoint deletes or overwrites target data | 3 | 5 | 15 | Data Lead | offline migration tool, dry run, backup, checksums | target delete or replication-role change | restore backup and revoke migration access |
| R-016 | Agent identities are duplicated across models and code | 4 | 3 | 12 | Architecture Lead | canonical Agent Spec and registry | different IDs for same role | freeze agent additions and reconcile registry |
| R-017 | Agent explosion increases cost and debugging complexity | 4 | 4 | 16 | Product Owner | start with Core Office and shared capabilities | agent count rises without unique value | consolidate agents into capability packs |
| R-018 | Model provider outage blocks critical work | 3 | 3 | 9 | Platform Lead | provider abstraction, retrieval-only mode, circuit breaker | provider error rate above threshold | degrade to source search without generated answer |
| R-019 | Provider substitution is logged inaccurately | 3 | 4 | 12 | AI Lead | record actual provider and model only | provider name differs from call path | invalidate cost and quality reports |
| R-020 | Hard-coded token prices create incorrect budget reports | 4 | 3 | 12 | Finance / AI Lead | dated pricing registry and billing reconciliation | variance versus provider invoice | label estimates and reconcile monthly |
| R-021 | Users reject system because it adds review work | 3 | 4 | 12 | Product Owner | workflow co-design, time study and progressive disclosure | low repeat use or high abandonment | simplify task flow and narrow use case |
| R-022 | Users over-trust confident language | 4 | 4 | 16 | UX Lead | evidence-first UI, uncertainty, source preview | user acts without reading evidence | require confirmation for material recommendations |
| R-023 | Meeting transcript contains errors that become memory | 4 | 4 | 16 | Memory Product Owner | transcript confidence and human review before promotion | disagreement with recording | quarantine decision memory and correct transcript |
| R-024 | Decision rationale is lost or oversimplified | 3 | 4 | 12 | Memory Product Owner | capture alternatives, evidence and dissent | decision record only contains summary | require decision review template |
| R-025 | Person memory contaminates role memory | 3 | 4 | 12 | Twin Owner | separate stores and promotion workflow | personal preference appears as role rule | roll back memory promotion and review lineage |
| R-026 | Role transfer exposes predecessor personal data | 3 | 5 | 15 | Privacy Lead | succession policy and memory classification | new role holder sees personal memory | suspend twin and perform access review |
| R-027 | Knowledge graph contains unverified relationships | 4 | 3 | 12 | Data Governance | provenance, confidence and review state on edges | graph answer cites unreviewed edge | restrict graph to discovery, not factual answer |
| R-028 | Forecast is mistaken for certainty | 3 | 5 | 15 | Forecast Owner | intervals, assumptions and scenario comparison | point prediction shown without uncertainty | disable recommendation layer |
| R-029 | Model bias affects vulnerable populations | 3 | 5 | 15 | AI Governance | subgroup evaluation and human review | error disparity exceeds threshold | suspend affected model and redesign features |
| R-030 | Cost grows faster than demonstrated value | 4 | 4 | 16 | Product Owner / Finance | per-task budgets, model routing and benefit tracking | cost per accepted task above ceiling | reduce scope and use retrieval-only path |
| R-031 | Repository shows future milestones as completed | 4 | 4 | 16 | Delivery Lead | maturity labels and gate status | stakeholder assumes prototype is production | issue correction and update release notes |
| R-032 | No automated CI allows broken main branch | 4 | 4 | 16 | Technical Lead | mandatory backend/frontend/security checks | main fails build or import | block release and revert commit |
| R-033 | Dependency vulnerability is untracked | 3 | 4 | 12 | Security Lead | lock files, dependency scan and patch SLA | critical CVE | isolate service and patch immediately |
| R-034 | Backup exists but restore fails | 3 | 5 | 15 | Platform Lead | scheduled restore tests | failed quarterly restore | initiate recovery plan and halt data migration |
| R-035 | Tenant or organization boundary is missing | 4 | 5 | 20 | Architecture Lead | tenant ID on all objects and policy tests | cross-organization query result | suspend multi-tenant pilot |
| R-036 | Audit records can be altered or deleted unnoticed | 3 | 5 | 15 | Security Lead | append-only store, integrity hash and restricted access | audit gap or modification | preserve forensic copy and investigate |
| R-037 | Team relies on AI-generated code without review | 4 | 4 | 16 | Technical Lead | PR review, tests, SAST and ownership | large unreviewed generated commit | freeze merge and conduct focused audit |
| R-038 | Project scope exceeds available delivery capacity | 5 | 4 | 20 | Executive Sponsor | milestone containment and capacity-based planning | work in progress across all milestones | stop later milestones and focus M1 |
| R-039 | Benefits are claimed without baseline | 4 | 3 | 12 | PMO | baseline protocol and benefit owner | presentation uses unsupported savings | withdraw claim and run time study |
| R-040 | Public or executive communication overstates readiness | 4 | 4 | 16 | Product Owner | approved product claims and maturity labels | claim exceeds gate status | correct communication and record incident |

## Weekly review questions

1. Has likelihood or impact changed?
2. Has a trigger occurred?
3. Is mitigation funded and progressing?
4. Is residual risk acceptable?
5. Does the risk block a maturity gate?
6. Is an executive decision required?
7. Should the risk become an active issue or incident?

## Risk acceptance

Risk acceptance must state:

- specific risk and scope;
- residual score;
- reason mitigation is not completed;
- duration of acceptance;
- compensating controls;
- accountable approver;
- expiry date and re-review trigger.

P0 risks cannot be accepted for production release.
