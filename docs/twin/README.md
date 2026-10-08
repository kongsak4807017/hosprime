# HosPrime Twin Ecosystem Index

This folder contains the controlled blueprint for the HosPrime Healthcare Twin Ecosystem.

## Documents

- `00_TWIN_ECOSYSTEM_VISION.md` — Healthcare Twin Ecosystem vision and North Star alignment.
- `01_TWIN_TAXONOMY.md` — controlled taxonomy for organization, hospital, department, process, staff, population, decision and AI agent twins.
- `02_TWIN_DATA_MODEL.md` — minimum metadata model for twin identity, relationships, evidence, decisions and audit events.
- `03_TWIN_USER_LEVEL_MAPPING.md` — user-level mapping from executives to staff and governance teams.
- `04_TWIN_MILESTONE_ROADMAP.md` — milestone sequence from Twin Foundation to Federated Regional Twin.
- `05_DECISION_TWIN_SEMANTICA.md` — Decision Twin and Semantica-style decision intelligence integration blueprint.
- `06_HUMAN_ORGANIZATION_TWIN_AGENT_HARNESS.md` — canonical Role Twin / Person Overlay -> Agent Manifest -> Agent Harness architecture, identity, permissions, memory, tools, approval, audit and lifecycle controls.
- `07_EMPLOYEE_TWIN_CAPTURE_AND_EVALUATION_PLAYBOOK.md` — production playbook for extracting governed work knowledge from an employee/role, shadow-mode validation, evaluation, onboarding and offboarding.

## Core product statement

HosPrime is a Healthcare Twin Ecosystem plus AI Agent Office plus Decision Intelligence Layer.

The Hospital Twin is only one twin type. Every meaningful entity in a healthcare organization can have a governed twin when it has an owner, evidence, relationships, decision pathway and audit trail.

## MVP twin chain

```text
Hospital Twin -> Department Twin -> Role Twin / Staff Twin -> Process Twin -> Decision Twin
```

This chain is the recommended first implementation path because it serves executives, department heads, staff and governance reviewers without overbuilding.

## Operating rule

```text
No Twin Without Owner
No Twin Without Evidence
No Twin Without Relationship
No Twin Without Decision Pathway
No Twin Without Audit Trail
```


## Twin-to-agent controlled path

```text
Role Twin
+ approved Person Overlay
+ Responsibility / Competency / Decision Memory
        |
        v
Agent Manifest
        |
        v
Agent Harness
        |
        v
Governed AI Agent
```

The goal is correct, accountable role performance — not personality imitation.

Additional operating rules:

```text
No Agent Without Unique Identity
No Agent Without Explicit Authority
No Tool Without Least-Privilege Authorization
No High-impact Action Without Required Human Approval
No Agent Release Without Shadow/Evaluation Evidence
No Agent Without Audit and Kill Switch
```
