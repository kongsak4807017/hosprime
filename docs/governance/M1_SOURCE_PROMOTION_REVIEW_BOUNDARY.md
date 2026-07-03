# M1 Source Promotion Human Review Boundary

## Purpose

This document defines the human approval boundary for moving M1 source records beyond placeholder states in the Governed Knowledge Oracle source register.

It exists to prevent placeholder, personal, unreviewed or externally staged information from becoming Organizational Memory or active Governed RAG evidence without an accountable human review record.

## Scope

Applies to `data/source_register/m1_source_register.yml` and any future M1 source-register records used for the Governed Knowledge Oracle MVP.

This boundary governs movement from non-authoritative states into authority-bearing states:

```text
DISCOVERED / QUARANTINED / PARSED / CLASSIFIED / QUALITY_CHECKED / REVIEW_PENDING
-> APPROVED
-> INDEX_READY
-> INDEXED
```

A source may not be treated as approved organizational evidence until it satisfies this boundary.

## Baseline before this review boundary

```text
M1_A_SOURCE_REGISTER_EXISTS = true
M1_A_SEED_RECORDS = 5
APPROVED_PLACEHOLDER_SOURCES = 0
ACTIVE_RAG_INDEXED_RECORDS = 0
HUMAN_REVIEW_BOUNDARY_DEFINED = false
```

## Target after this review boundary

```text
HUMAN_REVIEW_BOUNDARY_DEFINED = true
BACKOFFICE_AGENT_SELF_APPROVAL_ALLOWED = false
APPROVED_PLACEHOLDER_SOURCES = 0
ACTIVE_RAG_INDEXED_RECORDS = 0
UNAUTHORIZED_HIGH_IMPACT_ACTIONS = 0
```

## Minimum required reviewer identity

A source promotion review must record a named accountable human reviewer or approved review body.

Required reviewer fields:

```yaml
reviewer_identity:
  reviewer_name: required
  reviewer_role: required
  reviewer_organization: required
  reviewer_authority_basis: required
  reviewer_contact_or_account_ref: required
```

Acceptable reviewer roles include:

- source owner;
- data governance lead;
- knowledge governance reviewer;
- information security or access-control reviewer for restricted sources;
- program owner for domain-specific operational evidence;
- release authority for milestone gate decisions.

A system account, AI agent, backoffice automation or unattributed role label is not a sufficient reviewer identity.

## Minimum required review dates

Every review decision must record:

```yaml
review_date: required
review_decision_date: required
next_review_date: required_when_approved_or_indexed
expiry_date: required_when_source_has_known_expiry_or_policy_validity_window
```

Dates must use ISO format:

```text
YYYY-MM-DD
```

A source with no review date may remain in `DISCOVERED`, `QUARANTINED`, `PARSED`, `CLASSIFIED`, `QUALITY_CHECKED` or `REVIEW_PENDING`, but it may not become `APPROVED`, `INDEX_READY` or `INDEXED`.

## Review decision values

Allowed review decision values:

```text
APPROVE_FOR_ORGANIZATIONAL_EVIDENCE
APPROVE_WITH_RESTRICTIONS
REJECT
EXPIRE
REPLACE_WITH_NEW_VERSION
RETURN_FOR_CORRECTION
DEFER_PENDING_OWNER_CONFIRMATION
DEFER_PENDING_SECURITY_REVIEW
```

A decision must include a short rationale and evidence reference.

Required decision fields:

```yaml
review_decision:
  value: required
  rationale: required
  evidence_refs: required
  residual_risk: required_if_approve_with_restrictions
  restrictions: required_if_approve_with_restrictions
```

## Rejection, expiry and replacement audit notes

Rejected, expired or superseded sources must remain auditable but excluded from active retrieval.

Required audit fields:

```yaml
source_audit:
  decision: REJECT | EXPIRE | REPLACE_WITH_NEW_VERSION
  reason: required
  reviewer_identity: required
  decision_date: required
  superseded_by_source_id: required_if_replaced
  active_rag_index: false
  retrieval_exclusion_reason: required
```

## Backoffice agent self-approval prohibition

Backoffice agents may prepare evidence, calculate checksums, detect duplicates, classify candidate sources, flag access risks and draft review packets.

Backoffice agents must not:

- approve a source for Organizational Memory;
- approve a source for active Governed RAG retrieval;
- change `approval_status` to `approved`;
- change `lifecycle_state` to `APPROVED`, `INDEX_READY` or `INDEXED` without a recorded human reviewer;
- override restricted-source access decisions;
- mark a high-impact source as approved based only on automated confidence.

## Promotion rules

A source can move to `APPROVED` only when all conditions are true:

```text
named human reviewer exists
source owner exists
organization exists
classification exists
source version exists
checksum exists or an approved checksum exception exists
review_date exists
review decision is approval-bearing
access policy exists
limitation note exists
active_rag_index remains false until separate index-readiness and retrieval gates pass
```

A source can move to `INDEX_READY` only after source approval and retrieval-readiness checks are recorded.

A source can move to `INDEXED` only after index activation is authorized and access-control tests pass.

## Memory-layer boundary

This review boundary does not promote any source by itself.

Current effect:

```text
Personal / Staff Twin Memory = not modified
Person Memory = not modified
Role Memory = not modified
Research Staging = not modified
Organizational Memory / Governed RAG = boundary documented only; no source promoted
```

External findings remain in Research Staging until authority, relevance and applicability are reviewed.

Personal or staff-twin material remains personal memory unless explicitly promoted through a reviewed organizational evidence path.

## Issue linkage

- Parent pipeline: #10
- Review boundary issue: #17
- Controlled plan: #14
- Prior evaluation evidence: `engineering_runs/2026-07-03/0009-m1-source-register-evaluate.md`

## Status

```text
HUMAN_REVIEW_BOUNDARY_DEFINED = true
APPROVED_PLACEHOLDER_SOURCES = 0
ACTIVE_RAG_INDEXED_RECORDS = 0
FULL_M1_A_GATE_PASS_CLAIMED = false
NEXT_STAGE = RELEASE
```
