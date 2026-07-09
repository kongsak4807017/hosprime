# M0.2 Graph Links Are Not Memory Authority — Memory Correction

Date: 2026-07-09

Controlling issue: #155

Related milestone: M0.2 Local vault structure

Applies before: M0.3 Obsidian-compatible graph memory

## Correction summary

The M0.2 local vault structure is a repository-visible contract for where local Personal Twin notes may live. It is not itself runtime memory, evidence approval, source approval, graph usability, user acceptance, deployment proof, Organizational Memory, or active RAG.

Before M0.3 work begins, every future graph-memory implementation must preserve this boundary:

```text
FOLDER_EXISTS != PERSONAL_MEMORY_CAPTURED
NOTE_SHELL_EXISTS != FACTUAL_EVIDENCE
BACKLINK_EXISTS != SOURCE_APPROVAL
GRAPH_EDGE_EXISTS != GOVERNANCE_REVIEW
GRAPH_VIEW_EXISTS != USER_ACCEPTANCE
LOCAL_PERSONAL_NOTE != ORGANIZATIONAL_MEMORY
LOCAL_PERSONAL_NOTE != ACTIVE_RAG
MEMORY_CORRECTION != ORGANIZATIONAL_MEMORY_PROMOTION
```

## Rule to carry into M0.3

Obsidian-style links, backlinks, folders, graph nodes and graph edges are navigation evidence only.

They may help a user move between related local personal work notes, but they do not prove:

- factual correctness;
- source-owner approval;
- organizational approval;
- official minutes;
- task execution;
- decision authorization;
- clinical validity;
- Personal Memory ingestion success;
- retrieval quality;
- user acceptance;
- deployment completion;
- CI success;
- active RAG;
- Organizational Memory promotion;
- permission for high-impact action.

## Required M0.3 entry constraint

The first M0.3 graph-memory step must be bounded to a minimum linking convention or test that improves personal work navigation without changing memory authority.

Any M0.3 artifact must keep these controls explicit:

```text
MEMORY_SCOPE_DEFAULT = personal
ORGANIZATIONAL_TRUTH_DEFAULT = false
SOURCE_APPROVAL_DEFAULT = false
RAG_ACTIVE_DEFAULT = false
PROMOTION_REQUIRES_REVIEW_RECORD = true
HIGH_IMPACT_ACTION_AUTHORIZED = false
```

## Promotion boundary

A local personal note, graph node, backlink, source note, decision note, meeting note, task note or lesson note can become Role Memory, Organizational Memory or Governed RAG only after a separate reviewed promotion record exists.

The promotion record must include at minimum:

```text
owner
provenance
classification
version
review_state
approval_evidence
promotion_target
reviewer_or_approver
promotion_date
limitations
```

## Non-goals

This correction does not:

- add note templates;
- migrate real personal memory;
- create graph runtime code;
- test Obsidian or graph rendering;
- approve any source;
- ingest, parse, embed or index content;
- activate RAG;
- promote Organizational Memory;
- claim CI success;
- claim real-user acceptance;
- claim real-world execution.

## Durable control statement

```text
M0_2_GRAPH_MEMORY_CORRECTION_RECORDED = true
GRAPH_LINKS_ARE_NAVIGATION_NOT_PROOF = true
GRAPH_LINKS_ARE_NOT_MEMORY_AUTHORITY = true
M0_3_MUST_PRESERVE_MEMORY_BOUNDARIES = true
ORGANIZATIONAL_MEMORY_PROMOTION_CLAIMED = false
RAG_ACTIVATION_CLAIMED = false
REAL_USER_ACCEPTANCE_CLAIMED = false
REAL_WORLD_EXECUTION_CLAIMED = false
```
