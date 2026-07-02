# HosPrime Requirements Traceability Matrix

## Purpose

This matrix links strategic requirements to architecture, implementation, tests, evidence and ownership. It is updated in every release.

| ID | Requirement | Milestone | Architecture / component | Current implementation | Acceptance test | Evidence | Owner | Status |
|---|---|---|---|---|---|---|---|---|
| HP-KNO-001 | Answer only from approved organizational evidence | M1 | Knowledge Oracle | grounded prompt and retrieval pipeline | unanswerable set returns no factual answer >=98% | RAG evaluation report | AI Lead | In progress |
| HP-KNO-002 | Every material answer has traceable citations | M1 | Citation layer | chunk references returned | citation precision and completeness >=0.90 | citation evaluation | Knowledge Lead | In progress |
| HP-KNO-003 | Restricted sources are filtered by user authority | M1 | Identity, Policy, Retrieval | router auth exists; source ABAC incomplete | unauthorized source retrieval = 0 | access-control test | Security Lead | Gap |
| HP-KNO-004 | Documents have owner, classification, version and review date | M1 | Knowledge metadata | partial document fields | metadata completeness >=95% | source register | Knowledge Owner | Gap |
| HP-KNO-005 | Provider outage does not generate fabricated evidence | M1 | AI Gateway | safe failure added in governance branch | provider disabled test produces no factual answer | automated test and logs | AI Lead | Implemented, test needed |
| HP-KNO-006 | Retrieval quality is measured with versioned gold set | M1 | Evaluation harness | not implemented | Recall@5 >=0.85 and MRR >=0.70 | retrieval report | QA Lead | Gap |
| HP-SEC-001 | No real credential is stored in current source | Global | Configuration | current files cleaned | secret scan passes | scan artifact | Security Lead | Implemented, rotation pending |
| HP-SEC-002 | All non-public APIs require identity | Global | API router | router-level dependencies added | anonymous requests receive 401 | API security tests | Backend Lead | Implemented, test needed |
| HP-SEC-003 | Privileged routes require approved roles | Global | Authorization | admin, workflow and HITL role gates added | role matrix tests | access test report | Security Lead | Implemented, test needed |
| HP-SEC-004 | Uploads are size-limited and stored with generated names | Global | Document service | safe upload logic added | path traversal and oversized upload tests | security test | Backend Lead | Implemented, test needed |
| HP-OPS-001 | Production configuration fails closed | Global | Settings and readiness | production guard added | missing secret causes not-ready | health check test | Platform Lead | Implemented, test needed |
| HP-OPS-002 | Backend and frontend builds are automated | Global | CI | workflow pending | PR cannot merge on failed check | CI records | Technical Lead | Gap |
| HP-OPS-003 | Production schema uses controlled migrations | Global | Database | create_all remains for MVP | Alembic upgrade and rollback test | migration report | Platform Lead | Gap |
| HP-OPS-004 | Backup and restore are proven | Global | Operations | not implemented | quarterly restore succeeds | restore report | Platform Lead | Gap |
| HP-MEM-001 | Meeting creates reviewed Decision objects | M2 | Organization Memory | Meeting and Action Item only | extraction precision >=0.90 | memory evaluation | Memory Owner | Gap |
| HP-MEM-002 | Decision rationale and alternatives are preserved | M2 | Decision Graph | not implemented | reviewed record contains rationale and alternatives | UAT record | Memory Owner | Gap |
| HP-MEM-003 | Outcome and lesson link to original decision | M2 | Organization Memory | not implemented | end-to-end trace demonstrated | trace report | Memory Owner | Gap |
| HP-TWN-001 | Person and Role Memory are separated | M3 | Twin Runtime | structural models only | succession and privacy test | Twin evaluation | Twin Owner | Gap |
| HP-TWN-002 | Role Twin uses current authority and responsibility | M3 | Organization and Role | basic role model | effective-role test | authorization report | Twin Owner | Gap |
| HP-AGT-001 | Start with five Core Office agents | M3 | Agent Registry | current registry not canonical | exact five core roles certified | agent registry | Product Owner | Gap |
| HP-AGT-002 | Agents reuse governed capabilities | M3 | Capability Registry | not implemented | capability reuse and permission tests | agent acceptance pack | AI Governance | Gap |
| HP-AGT-003 | Agent cannot change its own authority or tools | M3/M4 | Agent Governance | static permissions partial | prohibited mutation test | security test | AI Governance | Gap |
| HP-WFL-001 | AI workflow output is a plan, not execution evidence | M4 | Workflow Planning | plan-only semantics added | no step marked completed by LLM | workflow tests | AI Governance | Implemented, test needed |
| HP-WFL-002 | Human approval identity comes from authentication | M4 | HITL | authenticated identity added | spoofed approver rejected | HITL tests | Security Lead | Implemented, test needed |
| HP-WFL-003 | Approved plan is not reported as executed | M4 | Workflow state model | APPROVED_NOT_EXECUTED added | state transition test | audit record | Workflow Owner | Implemented, test needed |
| HP-WFL-004 | External action requires authorized executor and receipt | M4 | Tool execution | executor absent | action cannot enter completed without receipt | execution contract test | Workflow Owner | Gap |
| HP-AIO-001 | Agent health, cost, failure and quality are visible | M4 | AIOC | logs and cost tables exist | AIOC dashboard acceptance | operations evidence | AgentOps Owner | Gap |
| HP-FCT-001 | Forecast includes assumptions and uncertainty | M5 | Forecast Runtime | not implemented | all forecast responses include interval and assumptions | model evaluation | Forecast Owner | Future |
| HP-FCT-002 | Forecast is backtested and monitored for drift | M5 | Model Registry | not implemented | temporal holdout and drift alert | validation report | Forecast Owner | Future |
| HP-VAL-001 | User value is measured against baseline | M1+ | Benefit Realization | plan documented | task-time and acceptance study complete | benefit report | Product Owner | Planned |
| HP-GOV-001 | Every milestone passes evidence-based gates | All | Project Governance | maturity gates documented | gate review recorded | evidence pack | Delivery Lead | Implemented, operationalization needed |

## Update rules

- Every new requirement receives a unique ID.
- Every pull request references affected requirement IDs.
- A status of `Implemented` requires linked tests and evidence before release.
- `Future` requirements cannot be marketed as current production capability.
- Any failed test updates the requirement status and risk register.
