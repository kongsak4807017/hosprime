# HosPrime Engineering Run 0006 — M1 Source Register CI Test Gate

## Loop stage

TEST — bounded correction inside the same TEST stage.

## North Star outcome supported

Evidence-based decisions and zero unauthorized high-impact action.

The source register is a required gate for the Governed Knowledge Oracle because active retrieval must not use unowned, unreviewed or unapproved organizational evidence.

## Real user / problem

Public-health executives, program owners, data governance officers and knowledge reviewers need trusted answers from approved organizational evidence. Without executable validation evidence, the project cannot prove that the M1 source register blocks unapproved or unreviewed sources before ingestion and indexing.

## Current controlled release target

Milestone 1 — Governed Knowledge Oracle MVP.

## Baseline

```text
M1_A_SOURCE_REGISTER_EXISTS = true
M1_A_SEED_RECORDS = 5
M1_A_APPROVED_RECORDS = 0
M1_A_ACTIVE_RAG_INDEXED_RECORDS = 0
PYTEST_PASS_CLAIMED = false
CI_PASS_CLAIMED = false
ISSUE_16_CLOSED = false
```

Previous TEST attempts recorded that static repository review passed, but executable pytest or CI evidence was missing.

## Target metric

```text
M1_A_SOURCE_REGISTER_TEST_EXECUTABLE = true
CI_GATE_AVAILABLE_FOR_SOURCE_REGISTER = true
PYTEST_PASS_CLAIMED = only after GitHub Actions or local pytest transcript exists
```

## Work completed in this run

Added a dedicated GitHub Actions workflow:

```text
.github/workflows/m1-source-register-test.yml
```

The workflow runs:

```bash
python -m pytest -q tests/test_m1_source_register.py
```

It is triggered by:

- pull requests that change the source register, test file or workflow file;
- pushes to `main` that change the same paths;
- manual `workflow_dispatch`.

## Evidence

Repository files already present on `main` before this bounded correction:

- `data/source_register/m1_source_register.yml`
- `tests/test_m1_source_register.py`

The test file validates:

- source register file exists;
- exactly five priority knowledge packs are present;
- required metadata fields exist;
- seed records are not approved or indexed;
- restricted sources have role-scoped restricted access.

This run does **not** claim the tests passed. It only creates the executable CI gate required to obtain pass/fail evidence.

## Governance and memory boundary

No source was ingested, parsed, embedded, indexed, approved or promoted into Organizational RAG.

All five source-register records remain placeholder records with:

```text
lifecycle_state = DISCOVERED
review_status = not_reviewed
approval_status = not_approved
active_rag_index = false
```

Memory layer affected: Research/engineering evidence package only. Organizational RAG remains unchanged.

## Issue linkage

- Parent organizational-memory pipeline: #10
- TEST control issue: #16

## Risks / blockers

- CI pass is not yet available until this workflow is reviewed, merged or otherwise executed.
- Issue #16 must remain open until executable pass/fail evidence exists.

## Next single stage

Continue TEST: open or merge the CI-gate branch, obtain GitHub Actions pass/fail evidence for `python -m pytest -q tests/test_m1_source_register.py`, then close #16 only if the test passes.
