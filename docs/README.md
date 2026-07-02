# HosPrime Controlled Documentation Index

## Architecture

- [`architecture/CURRENT_STATE_REASSESSMENT.md`](architecture/CURRENT_STATE_REASSESSMENT.md) — latest technical and product maturity assessment
- [`architecture/LOOP_ENGINEERING_ARCHITECTURE.md`](architecture/LOOP_ENGINEERING_ARCHITECTURE.md) — evidence-driven daily, sprint, milestone and strategic learning loops
- [`architecture/TWO_LAYER_MEMORY_ARCHITECTURE.md`](architecture/TWO_LAYER_MEMORY_ARCHITECTURE.md) — Personal/Twin Obsidian graph memory, Role Memory, Organizational RAG and promotion boundaries

## Operations

- [`operations/CONTINUOUS_RESEARCH_AND_LEARNING_LOOP.md`](operations/CONTINUOUS_RESEARCH_AND_LEARNING_LOOP.md) — continuous external research, source governance, synthesis and research-to-code traceability

## Project governance

- [`governance/PROJECT_CONTROL_SYSTEM.md`](governance/PROJECT_CONTROL_SYSTEM.md) — governance bodies, decision rights, cadence, RAG status and stop conditions
- [`governance/MATURITY_GATES.md`](governance/MATURITY_GATES.md) — measurable entry and exit gates for Milestones 1–5
- [`governance/SUCCESS_SCORECARD.md`](governance/SUCCESS_SCORECARD.md) — product, knowledge, AI, security, reliability, cost and delivery metrics
- [`governance/RISK_REGISTER.md`](governance/RISK_REGISTER.md) — initial strategic, technical, security, AI and adoption risks
- [`governance/TEST_AND_VALIDATION_STRATEGY.md`](governance/TEST_AND_VALIDATION_STRATEGY.md) — code, RAG, security, privacy, workflow and user validation
- [`governance/AI_GOVERNANCE_AND_AGENT_ACCEPTANCE.md`](governance/AI_GOVERNANCE_AND_AGENT_ACCEPTANCE.md) — agent specification, risk tiers, authority, lifecycle and certification
- [`governance/RELEASE_AND_CHANGE_MANAGEMENT.md`](governance/RELEASE_AND_CHANGE_MANAGEMENT.md) — branch, PR, version, release, rollback and emergency change controls
- [`governance/TRACEABILITY_MATRIX.md`](governance/TRACEABILITY_MATRIX.md) — links requirements to components, tests, evidence and owners
- [`governance/STATUS_REPORT_TEMPLATE.md`](governance/STATUS_REPORT_TEMPLATE.md) — weekly executive and delivery reporting template

## Roadmap

- [`roadmap/MASTER_IMPLEMENTATION_PLAN.md`](roadmap/MASTER_IMPLEMENTATION_PLAN.md) — controlled 90-day Milestone 1 plan and later milestone sequence

## Implemented foundations

- `backend/app/memory/` — governed memory contracts and Obsidian-compatible Personal Graph Store
- `backend/app/engineering_loop/` — loop run manifest, evidence package and ordered state transitions
- `backend/tests/test_personal_graph_memory.py` — Personal Graph behavior and boundary tests
- `backend/tests/test_engineering_loop.py` — engineering-loop contract tests

## Operating rule

A document, screen, API or class name does not prove maturity. Capability status is determined by evidence, tests and a recorded gate decision.
