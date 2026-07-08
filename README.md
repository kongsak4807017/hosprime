# HosPrime — Health Organization Operating System

HosPrime is an institutional intelligence platform for healthcare and public-health organizations.

## North Star

> **Enable healthcare and public-health organizations to use trusted data, knowledge, organizational memory and governed AI to complete real work and make better decisions faster, with evidence, accountability and continuous learning.**

เป้าหมายสูงสุดของ HosPrime คือทำให้องค์กรสุขภาพใช้ข้อมูล ความรู้ ความทรงจำ และ AI เพื่อทำงานจริงและตัดสินใจได้ดีขึ้น เร็วขึ้น ตรวจสอบได้ และเรียนรู้จากผลลัพธ์จริงอย่างต่อเนื่อง

HosPrime is not successful because it has more agents, more screens, more documents or more commits. It is successful only when real users complete important organizational work with accepted evidence, within the required time, without a material governance incident.

## Real-world outcomes

HosPrime must create five measurable organizational outcomes:

1. **Knowledge continuity** — organizational knowledge, role responsibilities, decisions and lessons do not disappear when people move, change roles or retire.
2. **Evidence-based decisions** — leaders can see the source, freshness, assumptions, conflicts, uncertainty and accountable approver behind important recommendations.
3. **Reduced repetitive workload** — staff spend less time searching documents, preparing briefs, summarizing meetings, tracking actions and recreating analysis.
4. **Closed execution loop** — events move through detection, analysis, decision, assignment, execution, outcome measurement and learning.
5. **Continuous organizational learning** — observed results improve knowledge, memory, workflows, agents, architecture and future plans.

## North Star metric

**Trusted Task Completion Rate**

```text
Tasks completed with accepted output, complete evidence,
required human approval and no material governance incident
-----------------------------------------------------------
Total approved target tasks attempted
```

Supporting measures include:

- task completion and repeat use;
- median time saved;
- citation precision and groundedness;
- user trust and usefulness;
- cost per accepted task;
- decision-to-outcome traceability;
- knowledge reuse;
- repeated-defect reduction;
- zero unauthorized high-impact action.

## Product priority

The first **deployable** product is **HosPrime Personal Twin OS v0.1**.

The first **institutional** product remains **HosPrime Executive Office**, supported by:

1. Governed Knowledge Oracle
2. Personal and Staff Twin Memory
3. Role Memory and Organizational Memory
4. Five Core Office agents: Executive, Planner, Analyst, Knowledge and Action
5. Meeting → Decision → Action → Outcome → Lesson loop
6. Evidence, audit, cost control and human approval

The project must demonstrate practical value in a personal daily-use environment before expanding agent count, autonomous action, forecasting or national-scale federation.

## Current 20-day execution focus

**Milestone 0 — Personal Twin OS v0.1**

Purpose: create a usable personal digital twin and graph-memory workspace that can be run locally, improved every loop, and later expanded into Staff Twin, Role Twin, Hospital Twin, Province Twin and Region Twin.

Target operating model:

```text
git clone
-> docker compose up
-> open local workspace
-> create / inspect Personal Twin
-> sync Markdown / Obsidian vault
-> build graph memory
-> query memory with evidence
-> record tasks, decisions and lessons
```

Twenty days at 24 hourly loop opportunities per day creates up to **480 bounded engineering loops**. Each loop must move one usable capability forward or record a clear blocker.

## Project progression board

Status legend:

```text
DONE      = usable or released with evidence
NOW       = current active milestone
NEXT      = next executable work
WAITING   = depends on prior milestone
EXPERIMENT= allowed only as prototype / sandbox
```

| Milestone | Focus | Status | Acceptance signal |
|---|---|---:|---|
| M0 | Personal Twin OS v0.1 | NOW | Local app can run, hold personal memory, build graph memory, and answer with evidence |
| M0.1 | README progression board | DONE | Front page shows current milestone, completed work, next work and boundaries |
| M0.2 | Local vault structure | NEXT | `vault/` structure supports Person, Project, Task, Decision, Meeting, Source and Lesson notes |
| M0.3 | Obsidian-compatible graph memory | WAITING | Markdown notes create usable backlinks and graph navigation |
| M0.4 | Personal memory schema | WAITING | Person, Role, Project, Task, Decision and Lesson objects are defined and persisted |
| M0.5 | Local vector memory | WAITING | Approved local notes can be embedded and searched without promoting external claims |
| M0.6 | Personal Twin API | WAITING | API exposes profile, memory, graph, task and decision endpoints |
| M0.7 | Personal Twin UI | WAITING | Browser UI shows profile, graph, timeline, tasks, decisions and knowledge search |
| M0.8 | Docker Compose local deploy | WAITING | Windows, macOS and Linux can run the same local stack |
| M0.9 | Daily-use loop | WAITING | User can capture work, ask memory-backed questions, and record lessons daily |
| M0.10 | Personal Twin v0.1 release candidate | WAITING | `git clone -> docker compose up` works with documented limitations |
| M1 | Governed Knowledge Oracle MVP | WAITING | Approved documents can be ingested, retrieved and cited with access control and audit |
| M2 | Staff / Role Twin | WAITING | Person Memory, Staff Twin and Role Memory are separated and permissioned |
| M3 | Executive Office | WAITING | Executive, Planner, Analyst, Knowledge and Action agents support real work loops |
| M4 | Backoffice AI Workforce and AIOC | WAITING | Finance, HR, procurement, quality and security agents run under governance |
| M5 | Hospital / Province / Region Twin | WAITING | Aggregated intelligence scales without sharing patient-level data by default |

## Token economy rules

The project must spend tokens on usable progress, not repetition.

Default loop context should include only:

```text
README.md
current issue or current milestone note
last 3 relevant engineering runs
files directly affected by the selected next step
test or error output when available
```

Rules:

1. Do not read the whole repository unless the selected step requires it.
2. Do not create long governance documents when a small runnable artifact is more valuable.
3. Prefer one file, one test, one endpoint, one screen, or one documented blocker per loop.
4. Keep Research Staging separate from Personal Memory, Role Memory and Organizational Memory.
5. Never claim deployability, test success, source approval, RAG activation or real-world execution without evidence.
6. Target normal engineering loops at approximately 20k–60k tokens; allow larger loops only for code-heavy build or debugging work with a stated reason.

## Loop Engineering

HosPrime is developed through an evidence-driven learning loop:

```text
Real Problem
-> Real User
-> Baseline
-> Research
-> Hypothesis
-> Plan
-> Build
-> Test
-> Evaluate
-> Review
-> Release
-> Observe
-> Learn
-> Correct Memory Layer
-> Next Goal
```

Every task must answer:

1. Which HosPrime outcome does this support?
2. Which real user and real work problem does it address?
3. What is the current baseline?
4. What measurable result is expected?
5. What internal or external evidence supports the approach?
6. Which tests, reviews and approval gates are required?
7. How will the result be observed, learned from and stored in memory?

If these questions cannot be answered, the task should not consume development capacity.

## HosPrime Hourly Loop

The scheduled task `HosPrime Hourly Loop` runs every hour at minute 30 in the `Asia/Bangkok` timezone:

```text
00:30, 01:30, 02:30, ... 22:30, 23:30
```

Every run must read this North Star before selecting work. It may complete exactly one bounded next step—baseline, research, hypothesis, plan, build, test, evaluate, review, release observation or learning.

The hourly task must:

- prioritize measurable user and organizational outcomes over feature volume;
- inspect the latest `main`, issues, pull requests, CI, milestone gates, risks and recent engineering runs;
- link work to a baseline, target metric, issue and acceptance evidence;
- preserve sequence and never skip required gates;
- never fabricate evidence or claim execution without records;
- keep Personal/Twin Memory, Role Memory, Research Staging and Organizational RAG separated;
- record blockers, failed hypotheses, dissent and negative results;
- update GitHub with the justified issue, evidence, code, tests, pull request, observation or lesson;
- stop or defer work that does not contribute to the North Star.

Hourly execution is an **execution heartbeat**, not permission to change project strategy every hour. Strategy is reviewed through sprint, milestone and executive governance.

## Current release target

The repository contains prototypes for Knowledge Oracle, Meeting Memory, Digital Twins, Graph, AI Workflows and HITL. These components are not all production-ready.

The current controlled release target is:

**Milestone 0 — Personal Twin OS v0.1**

A successful Milestone 0 must provide a locally runnable personal twin with Markdown/Obsidian-compatible graph memory, local persistence, memory-backed Q&A with evidence boundaries, task/decision/lesson capture, and a documented path to Staff Twin and Organizational Memory.

Institutional Milestone 1 remains:

**Milestone 1 — Governed Knowledge Oracle MVP**

A successful Milestone 1 must ingest approved documents, retrieve evidence, answer only when evidence is sufficient, provide traceable citations, enforce access control, and record audit and cost data.

## Core rules

```text
No Evidence -> No Factual Answer
No Identity -> No Access
No Human Approval -> No High-impact Action
No Execution Record -> Never Claim Completion
No Baseline -> No Improvement Claim
No Quality Gate -> No Release
No Observation -> No Learning
```

## Memory boundaries

```text
Personal / Staff Twin Memory
        |
        | reviewed promotion only
        v
Role and Organizational Memory / Governed RAG
        ^
        | reviewed external evidence
        |
Research Staging
```

- Personal memory is not organizational evidence by default.
- Person Memory and Role Memory remain separate.
- External research remains in staging until reviewed for authority, relevance and applicability.
- Organizational RAG indexes only approved sources with ownership, provenance, classification, version and review status.

## Project control documents

See the controlled plans under:

- `docs/architecture/`
- `docs/governance/`
- `docs/operations/`
- `docs/roadmap/`

Important references:

- `docs/architecture/LOOP_ENGINEERING_ARCHITECTURE.md`
- `docs/architecture/TWO_LAYER_MEMORY_ARCHITECTURE.md`
- `docs/operations/CONTINUOUS_RESEARCH_AND_LEARNING_LOOP.md`
- `docs/governance/MATURITY_GATES.md`
- `docs/governance/SUCCESS_SCORECARD.md`

## Milestone sequence

```text
M0 Personal Twin OS v0.1
M1 Governed Knowledge Oracle
M2 Staff / Role Twin and Organization Memory
M3 Executive Office and Role Twin
M4 Backoffice AI Workforce and AIOC
M5 Forecast, Scenario and Provincial Health Brain
```

Future-milestone prototypes must remain labeled experimental until their evidence-based gates pass.

## Secure local setup

### Backend

```bash
cd backend
python -m venv .venv
pip install -r requirements.txt
cp .env.example .env
```

Configure the local `.env` file with newly issued credentials:

```env
ENVIRONMENT=development
GEMINI_API_KEY=replace-with-a-new-provider-key
JWT_SECRET=replace-with-a-long-random-secret
DATABASE_URL=sqlite:///./hosprime.db
ALLOW_DEMO_FALLBACKS=false
ALLOW_PSEUDO_EMBEDDINGS=false
```

Run from the repository root:

```bash
python -m backend.app.db.bootstrap
uvicorn backend.app.main:app --reload
```

API documentation: `http://localhost:8000/docs`

Health endpoints:

```text
GET /health/live
GET /health/ready
```

### Frontend

```bash
cd frontend
npm ci
npm run dev
```

Open `http://localhost:5173`.

## Security notice

A provider credential was previously committed to repository history and has been revoked or rotated. Historical exposure remains part of the security record. Never commit real credentials, passwords, tokens or connection strings.

## Workflow boundary

The current workflow module creates a plan and sends it to the HITL queue. It does not contain a configured external executor.

An approved plan is recorded as:

```text
APPROVED_NOT_EXECUTED
```

It must not be reported as a completed real-world action.
