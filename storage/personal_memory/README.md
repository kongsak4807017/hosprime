# HosPrime Personal Memory Storage

This directory is the repository-visible contract for Milestone 0.2 — Local vault structure.

It defines where a local Personal Twin workspace may store Markdown / Obsidian-compatible personal memory notes. It does not contain real personal content, organizational truth, approved source material, embeddings, indexes, runtime state, credentials, patient data, or production deployment evidence.

## Scope

```text
PERSONAL_MEMORY_SCOPE = local personal workspace only
ORGANIZATIONAL_TRUTH = false unless reviewed promotion exists
RAG_ACTIVE = false
SOURCE_APPROVAL = false
GRAPH_LINKS_ARE_NAVIGATION_NOT_PROOF = true
PROMOTION_REQUIRES_REVIEW_RECORD = true
NO_REAL_PERSONAL_CONTENT_IN_EXAMPLE = true
NO_PATIENT_OR_SENSITIVE_CONTENT_IN_EXAMPLE = true
```

## Contract root

The expected local runtime pattern is:

```text
storage/personal_memory/<person-id>/vault/
```

The repository includes only an `example-person` placeholder to show the required folder contract. Real deployments must use an installation-specific person identifier and must not commit private personal memory to the repository by default.

## Memory boundary

Personal Memory is not Organizational Memory by default.

A note in this folder is only a local personal workspace object until a separate review record explicitly promotes a specific item to Role Memory, Organizational Memory, or Governed RAG. Promotion requires ownership, provenance, classification, version, review status, and approval evidence.

## Non-goals

This directory does not authorize:

- source approval;
- organizational ingestion;
- parsing, embedding, indexing, or active RAG;
- factual answers from unreviewed notes;
- high-impact actions;
- deployment completion;
- CI success;
- real-user acceptance;
- real-world execution.
