# HosPrime Loop Engineering Run 0007 — M1 Source Register CI Dependency Correction

## North Star outcome supported

Evidence-based decisions, accountability and zero unauthorized high-impact action.

This run supports the M1 Governed Knowledge Oracle MVP by making the source-register validation gate executable before any source can be approved, embedded, indexed or promoted into Organizational RAG.

## Real user and real organizational problem

**Real users:** public-health executives, program owners, data governance officers and knowledge reviewers.

**Problem:** M1 source-register validation must produce executable pass/fail evidence. Without a reliable CI gate, the project could not prove that seed records remain unapproved, non-indexed and governed before later ingestion work begins.

## Current loop stage

TEST — bounded correction after executable CI failure.

The previous TEST run produced real CI evidence on PR #33:

- `M1 Source Register Test` completed with conclusion `failure` on commit `5a0bfe17f4948249e5f7100c247852ccf45e72e9`.
- Job `Validate M1 source register gate` failed at step `Run source register tests`.
- `HosPrime CI` completed with conclusion `success` for the same PR head.

## Baseline and target metric

```text
M1_A_SOURCE_REGISTER_EXISTS = true
M1_A_SEED_RECORDS = 5
M1_A_APPROVED_RECORDS = 0
M1_A_ACTIVE_RAG_INDEXED_RECORDS = 0
M1_SOURCE_REGISTER_CI_GATE = failing
PYTEST_PASS_CLAIMED = false
CI_PASS_CLAIMED = false
```

Target for this bounded correction:

```text
M1_SOURCE_REGISTER_CI_GATE_CAN_EXECUTE_PYTEST = true
M1_SOURCE_REGISTER_CI_GATE = pass_or_actionable_failure
NO_SOURCE_PROMOTED_TO_ORGANIZATIONAL_RAG = true
```

## Evidence inspected

- README `main` confirms the North Star and Core Rules.
- Issue #10 remains the parent organizational-memory backoffice pipeline.
- Issue #16 remains the TEST control issue and requires pass/fail evidence before closure.
- Issue #31 tracks the CI-gate correction.
- PR #33 is open and mergeable.
- Workflow run `28625826370` for `M1 Source Register Test` failed.
- Job `84891953340` failed at `Run source register tests`.
- The workflow called `python -m pytest -q tests/test_m1_source_register.py` without first installing `pytest`.

## Work completed in this run

Updated `.github/workflows/m1-source-register-test.yml` on branch `m1-source-register-ci-test-gate` to add an explicit dependency installation step:

```yaml
- name: Install pytest
  run: python -m pip install --upgrade pip pytest
```

This keeps the TEST correction bounded to the CI execution environment only.

## Governance boundary

No source was ingested, parsed, embedded, indexed, approved or promoted into Organizational RAG.

The five seed records remain placeholders only:

```text
approval_status = not_approved
active_rag_index = false
review_status = not_reviewed
```

## Test and CI status

```text
PREVIOUS_M1_SOURCE_REGISTER_TEST_RUN = failure
CURRENT_CORRECTION_COMMIT = a9b315384ac1f8395de9635a508f070f61a66ae2
PYTEST_PASS_CLAIMED = false
CI_PASS_CLAIMED = false
ISSUE_16_CLOSED = false
ISSUE_31_CLOSED = false
```

A new CI run is expected from the pushed branch update, but this evidence package does not claim success until GitHub Actions produces a completed passing run.

## Memory layer affected

Research Staging / engineering evidence only.

No Personal Memory, Role Memory or Organizational RAG truth was changed.

## Risks and blockers

- The previous CI gate failed, so the TEST stage is not complete.
- If the next run still fails, the failure must be treated as an actionable test result, not bypassed.
- #16 must remain open until executable pytest or CI pass evidence exists.

## Single next stage

Continue TEST: inspect the new GitHub Actions run for commit `a9b315384ac1f8395de9635a508f070f61a66ae2`; close #16 and #31 only if the M1 source-register gate passes.
