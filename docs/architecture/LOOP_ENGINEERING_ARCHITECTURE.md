# HosPrime Loop Engineering Architecture

## Purpose

HosPrime will be developed as a closed learning system. Every task must convert a real need, internal evidence, external research, code change, test result and operational feedback into the next decision.

```text
Goal
-> Baseline
-> Research
-> Hypothesis
-> Plan
-> Build
-> Test
-> Evaluate
-> Review
-> Decide
-> Release
-> Observe
-> Learn
-> Memory
-> Next Goal
```

## Core rules

- No task without an objective.
- No improvement claim without a baseline.
- No conclusion without evidence.
- No completion without tests.
- No release without review.
- No learning without observation.
- No organizational learning unless the result is stored in the correct memory layer.

## Loop levels

### Daily task loop

Used for one bounded research, design, code or quality task.

Required outputs:

- task statement;
- current baseline;
- evidence and sources;
- hypothesis;
- implementation or analysis;
- test result;
- review result;
- next action.

### Sprint loop

Used to deliver a vertical product slice.

Required outputs:

- sprint objective;
- target metric;
- accepted increment;
- regression and security evidence;
- user feedback;
- updated risks and backlog.

### Milestone loop

Used to prove readiness for pilot or production.

Required outputs:

- maturity-gate evidence pack;
- operational and security evidence;
- benefit realization;
- residual-risk decision;
- go, hold, reduce-scope or stop decision.

### Strategic learning loop

Used quarterly or after a major incident to revisit assumptions, architecture, investment and scope.

## Run states

```text
CAPTURED
BASELINED
RESEARCHING
HYPOTHESIS_READY
PLANNED
BUILDING
TESTING
EVALUATING
REVIEWING
DECIDED
RELEASED
OBSERVING
LEARNED
CLOSED
```

Alternative terminal states:

- `REJECTED_HYPOTHESIS`
- `STOPPED_RISK`
- `DEFERRED_DEPENDENCY`
- `NO_CHANGE_REQUIRED`

A rejected hypothesis is valid learning and must remain searchable.

## Run evidence package

```text
engineering_runs/YYYY-MM-DD/<run-id>/
├── manifest.json
├── 00-task.md
├── 01-baseline.md
├── 02-research.md
├── 03-hypothesis.md
├── 04-plan.md
├── 05-implementation.md
├── 06-tests.md
├── 07-evaluation.md
├── 08-review.md
├── 09-decision.md
├── 10-observation.md
└── 11-learning.md
```

The manifest records ownership, objective, target metric, linked issue, affected components, source references, commits, tests, decision, approver and memory objects created.

## Daily operating cycle

### Orient

- inspect milestone gates, risks, CI failures and feedback;
- select the highest-value bounded task;
- record objective, baseline and target metric.

### Research

- inspect current code and runtime behavior;
- review internal policies and prior decisions;
- search current external primary sources;
- record provenance and limitations;
- form a testable hypothesis.

### Build

- define acceptance criteria;
- implement the smallest coherent change;
- add tests and observability;
- update documentation and traceability.

### Validate

- run automated tests;
- run security, authorization and data-quality checks where relevant;
- compare results with the baseline;
- record negative and unexpected results.

### Review

- review code, architecture and evidence quality;
- review user, security, privacy and operational impact;
- record dissent and unresolved conditions;
- approve, revise, defer or stop.

### Learn

- observe actual behavior;
- record the lesson;
- promote reviewed knowledge to the correct memory layer;
- create the next task from the remaining gap.

## AI Agent roles

- Research Agent: finds current primary sources and records provenance.
- Analyst Agent: compares evidence, alternatives and expected impact.
- Planner Agent: creates a bounded plan linked to acceptance criteria.
- Builder Agent: creates controlled code or configuration changes.
- Test Agent: reports raw results without rewriting failure as success.
- Reviewer Agent: challenges architecture, security, privacy and claims.
- Data Governance Agent: selects memory scope, owner, retention and review state.
- Learning Agent: converts reviewed outcomes into reusable knowledge.

No agent may approve its own high-risk output.

## Progress metrics

- cycle time from task capture to decision;
- percentage of runs with complete evidence;
- rework and repeated-defect rate;
- regression and security pass rate;
- percentage of work linked to milestone criteria;
- time from external finding to reviewed decision;
- trusted task completion;
- time saved and cost per accepted outcome.

## Successful daily loop

A daily loop succeeds when it produces at least one of:

1. a validated improvement;
2. a disproved hypothesis that prevents wasted effort;
3. a detected and reduced risk;
4. a clarified requirement or architecture decision;
5. a reviewed knowledge object that improves later work.

The volume of generated text or code is not a success measure.
