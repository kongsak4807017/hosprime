# HosPrime Two-Layer Memory Architecture

## 1. Design goal

HosPrime memory is divided into two governed layers with a separate research staging area.

```text
Personal / Twin Memory
        |
        | reviewed promotion only
        v
Organizational Memory and RAG
        ^
        | reviewed external evidence
        |
Research Staging Memory
```

The layers must not be merged into one database because they have different owners, privacy rules, retention rules and standards of evidence.

## 2. Layer A — Personal and Staff Twin Memory

### Purpose

Maintain working context, experience, relationships, lessons and responsibilities for an individual staff member and their digital Twin.

### Storage model

Each staff member receives an Obsidian-compatible Markdown vault:

```text
storage/personal_memory/<person-id>/vault/
├── people/
├── roles/
├── projects/
├── tasks/
├── decisions/
├── lessons/
├── skills/
├── meetings/
├── sources/
└── daily/
```

Each note contains:

- YAML properties;
- Markdown content;
- internal `[[Wiki Links]]`;
- backlinks generated from those links;
- source references;
- review status;
- sensitivity and retention metadata.

Obsidian Graph View then renders the real relationships between notes. The graph is not a decorative mock-up.

### Node types

- Person
- Role
- Responsibility
- Project
- Task
- Meeting
- Decision
- Lesson
- Skill
- Relationship
- Source
- Daily Note

### Required properties

```yaml
note_id: staff-123-project-tb-screening
title: TB Active Case Finding
person_id: staff-123
note_type: project
memory_scope: personal
review_state: reviewed
sensitivity: internal
source_refs:
  - meeting-2026-07-02
created_at: 2026-07-02T10:00:00+07:00
updated_at: 2026-07-02T10:00:00+07:00
retention_until: 2029-07-02
```

### Personal memory rules

- The staff member is the primary owner.
- Access is limited to the person and explicitly authorized roles.
- Personal preferences do not become organizational policy.
- Unreviewed conversation memory remains personal working memory.
- Sensitive health, employment or private information is excluded unless specifically required and lawfully governed.
- A staff Twin may retrieve personal memory but may not silently publish it to other users.

## 3. Role Memory within Layer A

Person Memory and Role Memory remain separate.

### Person Memory

Contains personal working style, private task context and individual learning.

### Role Memory

Contains responsibilities, approved procedures, recurring duties and handover knowledge associated with a position.

When a person changes role:

- Person Memory stays with the person.
- Reviewed Role Memory stays with the role.
- Promotion from Person Memory to Role Memory requires review.
- Private preferences and personal relationships are not transferred automatically.

## 4. Layer B — Organizational Memory and Governed RAG

### Purpose

Provide trusted, organization-owned knowledge for decisions, operations, audits, planning and continuity.

### Source classes

- official policies and orders;
- SOPs and service standards;
- approved reports;
- meeting decisions and action outcomes;
- program and project records;
- data dictionaries and semantic definitions;
- dashboards and validated datasets;
- lessons learned;
- approved research and external guidance;
- legacy files and historical repositories.

### Storage architecture

```text
Raw source zone
-> Quarantine and parsing
-> Metadata and ownership
-> Data-quality validation
-> Human review where required
-> Approved source registry
-> Chunk and entity extraction
-> Vector index
-> Knowledge graph
-> Retrieval evaluation
-> Organizational RAG
```

Recommended baseline:

- PostgreSQL for source registry, metadata, access and audit;
- pgvector for semantic retrieval;
- object storage for original files;
- Neo4j or a governed graph projection for complex relationships;
- versioned evaluation datasets for retrieval and answer quality.

### Organizational memory objects

- Source
- SourceVersion
- Document
- Dataset
- Entity
- Relationship
- Claim
- Decision
- DecisionRationale
- Action
- Outcome
- LessonLearned
- EvidenceLink
- ResearchFinding
- PolicyInterpretation

Every object has owner, organization, classification, version, provenance, review status and effective date.

## 5. Backoffice Memory Agents

### Source Discovery Agent

Finds internal files, systems and approved external sources. Creates discovery records only.

### Ingestion Agent

Copies source content into quarantine, calculates checksum and extracts technical metadata.

### Data Governance Agent

Assigns owner, classification, retention, lawful purpose, organization scope and review route.

### Data Quality Agent

Checks completeness, duplication, date validity, structure, encoding and parsing quality.

### Data Mining Agent

Extracts entities, relationships, repeated patterns, candidate indicators and cross-document links.

### Knowledge Curator Agent

Groups and summarizes related sources while preserving provenance and disagreement.

### Indexing Agent

Creates chunks, embeddings and graph projections only from eligible source versions.

### Retrieval Evaluation Agent

Runs gold-set retrieval tests and reports Recall, MRR, precision, access violations and stale-source behavior.

### Memory Promotion Agent

Promotes reviewed findings into active organizational memory. It cannot self-approve high-risk content.

### Freshness and Drift Agent

Detects expired sources, changed policies, new versions, data drift and conflicting evidence.

## 6. Research Staging Memory

External research is stored separately from approved organizational memory.

```text
research_staging/
├── source_registry/
├── search_runs/
├── findings/
├── evidence_tables/
├── synthesis/
└── promotion_queue/
```

A research finding records:

- source title;
- publisher or institution;
- URL or identifier;
- publication and retrieval dates;
- source type;
- jurisdiction and population;
- methods and limitations;
- extracted claims;
- confidence and conflicts;
- reviewer;
- proposed organizational relevance.

External evidence becomes organizational memory only after relevance, authority, applicability and conflict review.

## 7. Promotion paths

### Personal to Role Memory

```text
Personal note
-> promotion request
-> privacy and relevance review
-> remove private content
-> role owner approval
-> role memory version
```

### Personal to Organizational Memory

```text
Personal lesson
-> evidence package
-> domain review
-> Data Governance review
-> organizational owner approval
-> approved source or lesson object
-> RAG indexing
```

### Research to Organizational Memory

```text
External source
-> research staging
-> quality and applicability review
-> conflict review
-> owner decision
-> approved finding or guidance object
-> RAG indexing
```

## 8. Query routing

The query router determines which memory layer may be used.

### Personal query

May use the caller's Personal Memory and authorized Role Memory.

### Role query

May use Role Memory and approved Organizational Memory.

### Organizational query

Uses only approved Organizational Memory and eligible Research Findings.

### Executive query

May combine approved organizational evidence with current operational data, but must expose source, assumptions, conflicts and uncertainty.

## 9. Non-negotiable boundaries

- Personal memory is not an organizational evidence source by default.
- Research staging is not organizational truth.
- A visual graph does not prove that a relationship is correct.
- Every edge requires provenance and review status.
- Deleted or corrected memory must be reflected in indexes and graph projections.
- No agent may promote its own high-risk finding without an authorized reviewer.
- Organizational RAG must enforce organization, role and source-level access before retrieval.

## 10. Initial implementation sequence

1. Build the Obsidian-compatible Personal Graph Store.
2. Add Person, Role and Organization memory scopes.
3. Add promotion queue and review contracts.
4. Add organizational source registry and ingestion states.
5. Integrate Data Governance and Data Quality agents.
6. Add retrieval evaluation before activating new sources.
7. Add continuous research staging and promotion workflow.
8. Replace all mock Twin graph data with real stored notes and links.
