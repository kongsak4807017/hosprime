# Personal Twin Vault Contract

This vault is the minimal Milestone 0.2 Markdown / Obsidian-compatible structure for local Personal Twin OS v0.1 development.

It is a repository-visible contract only. It does not contain real notes, real personal memory, organizational truth, approved sources, patient data, embeddings, indexes, API endpoints, UI screens, deploy evidence, or active RAG.

## Required folders

```text
people/
projects/
tasks/
decisions/
meetings/
sources/
lessons/
```

Each folder is kept with `.gitkeep` only during this BUILD stage.

## Folder intent

| Folder | Future note type | Boundary |
|---|---|---|
| `people/` | `person` | Local personal context only; not an identity authority. |
| `projects/` | `project` | Local project memory only; not an approved organizational plan. |
| `tasks/` | `task` | Local task tracking only; not execution proof. |
| `decisions/` | `decision` | Local decision notes only; not approval proof without review and audit record. |
| `meetings/` | `meeting` | Local meeting notes only; not official minutes unless separately reviewed. |
| `sources/` | `source` | Personal source references only; not source-owner approval or RAG ingestion authorization. |
| `lessons/` | `lesson` | Personal learning notes only; not Organizational Memory unless reviewed and promoted. |

## Required future front matter

Future Markdown notes created by the application or local workspace should use this minimum front-matter contract:

```yaml
note_id: ""
title: ""
person_id: ""
note_type: "person | project | task | decision | meeting | source | lesson"
memory_scope: "personal"
review_state: "draft | reviewed | rejected | promoted"
sensitivity: "public | internal | restricted | confidential"
source_refs: []
links: []
created_at: "YYYY-MM-DD"
updated_at: "YYYY-MM-DD"
retention_until: "YYYY-MM-DD | indefinite"
version: "0.1"
```

## Graph-link boundary

Obsidian-style links and backlinks are navigation aids. They are not proof of factual correctness, source approval, user acceptance, execution, clinical validity, organizational approval, or governance review.

```text
GRAPH_LINKS_ARE_NAVIGATION_NOT_PROOF = true
```

## Promotion boundary

A local personal note may be considered for promotion only through a separate reviewed promotion record. Promotion must preserve separation between Personal / Staff Twin Memory, Person Memory, Role Memory, Organizational Memory / Governed RAG, and Research Staging.

```text
PROMOTION_REQUIRES_REVIEW_RECORD = true
ORGANIZATIONAL_TRUTH = false unless reviewed promotion exists
RAG_ACTIVE = false
SOURCE_APPROVAL = false
```

## Prohibited content in this repository example

Do not commit these into the example vault:

- real personal diary or staff memory;
- patient-identifiable information;
- credentials or secrets;
- organizational documents treated as approved truth;
- source-owner packets;
- embeddings, vector indexes, or generated RAG stores;
- execution receipts or approval records not actually produced by an authorized workflow.
