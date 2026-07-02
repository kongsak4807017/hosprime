# Continuous Research and Learning Loop

## 1. Objective

HosPrime continuously monitors relevant real-world evidence, technology, policy, standards and implementation experience. Research output is recorded as evidence, reviewed for applicability and then converted into project decisions, code changes or organizational knowledge.

Research is not a news feed. It is a governed input to Loop Engineering.

## 2. Research domains

### Public-health and healthcare domains

- communicable disease surveillance;
- TB, HIV, dengue and emerging infection control;
- NCD screening, remission and service redesign;
- disaster, PM2.5 and climate-health response;
- border and migrant health;
- workforce, finance and service capacity;
- road traffic injury;
- digital health, interoperability and health data governance.

### Technology domains

- RAG and GraphRAG;
- agent orchestration and memory;
- vector databases and knowledge graphs;
- identity, access and privacy engineering;
- observability, evaluation and AI safety;
- healthcare interoperability;
- on-premises and hybrid infrastructure;
- software supply-chain and DevSecOps.

### Governance domains

- Thai health policy and regulation;
- PDPA, cybersecurity and digital-government obligations;
- standards and technical guidance;
- procurement and auditability;
- AI governance and responsible automation.

## 3. Preferred source hierarchy

1. law, regulation, official standard or government publication;
2. international organization or recognized public institution;
3. peer-reviewed systematic review, guideline or original research;
4. official technical documentation and primary repository;
5. high-quality implementation report;
6. secondary analysis used only for discovery or context.

A lower-ranked source does not override a higher-authority current source without documented reasoning.

## 4. Initial machine-readable sources

### Biomedical literature

- PubMed and NCBI E-utilities for searching and retrieving biomedical records;
- Crossref REST API for DOI metadata, funders, updates and bibliographic relationships.

### Population and health indicators

- WHO Global Health Observatory data services;
- approved Thai Ministry of Public Health and provincial data sources;
- verified national statistical and administrative sources.

### Technical evidence

- official project documentation and primary source repositories;
- standards-body publications;
- release notes and security advisories.

## 5. Research run structure

```text
research_runs/YYYY-MM-DD/<research-id>/
├── manifest.json
├── 00-question.md
├── 01-search-strategy.md
├── 02-source-register.csv
├── 03-evidence-table.md
├── 04-analysis.md
├── 05-applicability.md
├── 06-recommendation.md
├── 07-review.md
└── 08-promotion-decision.md
```

## 6. Research manifest

Required fields:

- research ID;
- question;
- requester and owner;
- jurisdiction and target population;
- search date and time;
- databases and sources searched;
- inclusion and exclusion criteria;
- source identifiers and checksums where available;
- findings;
- limitations and conflicts;
- applicability to HosPrime;
- linked issue, requirement and engineering run;
- review status;
- promotion decision.

## 7. Daily research cycle

### Discover

- read open project gaps and milestone criteria;
- identify changes since the last search;
- search primary and official sources;
- store metadata before synthesis.

### Screen

- remove duplicates;
- identify retractions, corrections and superseded versions;
- classify source type, authority and relevance;
- exclude unsupported promotional material.

### Extract

- extract claims, methods, population, intervention, outcome and limitations;
- preserve exact identifiers and page or section references;
- separate source statements from analyst inference.

### Synthesize

- compare evidence with current project assumptions;
- identify consensus, disagreement and missing evidence;
- assess transferability to Thai provincial public health operations.

### Decide

Choose one or more outcomes:

- no project change;
- create an issue;
- update requirements;
- revise architecture;
- run an experiment;
- change code;
- update risk controls;
- propose organizational memory promotion.

### Review and promote

Research findings remain in staging until a qualified reviewer approves their use. Promotion records the reviewer, date, scope, limitations and expiration or re-review date.

## 8. Continuous research agents

### Research Scout Agent

Runs registered search queries and detects new or changed sources.

### Source Integrity Agent

Checks identifiers, source authority, duplicate records, corrections and retractions.

### Evidence Extraction Agent

Creates structured evidence tables without adding unsupported claims.

### Applicability Agent

Assesses population, jurisdiction, infrastructure, cost and operational fit.

### Research Synthesis Agent

Summarizes agreements, disagreements, uncertainty and implications.

### Research Governance Agent

Assigns classification, owner, review state, retention and promotion route.

### Change Proposal Agent

Links an approved finding to a requirement, issue, experiment or pull request.

No research agent may directly change production policy, code or organizational memory without the relevant review gate.

## 9. Search query registry

Each recurring query has:

- query ID;
- domain;
- query text;
- source connector;
- owner;
- frequency;
- last successful run;
- date range;
- duplicate key;
- alert threshold;
- linked project objective;
- active or retired state.

Queries should be versioned. A material query change creates a new version so trend comparisons remain interpretable.

## 10. Scheduling model

### Daily

- new official guidance;
- security advisories;
- critical dependency releases;
- public-health emergency and emerging-disease sources;
- active project research questions.

### Weekly

- peer-reviewed evidence;
- architecture and platform developments;
- implementation case studies;
- updates to standards and best practices.

### Monthly

- broad horizon scan;
- obsolete source review;
- research gap analysis;
- query effectiveness review;
- roadmap and investment implications.

Scheduled collection may use GitHub Actions or an external scheduler, but every run must also support manual `workflow_dispatch` execution and idempotent re-runs.

## 11. Quality controls

- source metadata stored before AI synthesis;
- exact identifiers retained;
- duplicate detection;
- correction and retraction checks;
- source authority and freshness score;
- claim-to-source traceability;
- separate fact, inference and recommendation fields;
- human review for high-impact conclusions;
- versioned synthesis and promotion decision;
- no automatic overwrite of approved organizational knowledge.

## 12. Research-to-code traceability

```text
Research question
-> source register
-> evidence finding
-> reviewed implication
-> requirement or risk
-> issue
-> engineering run
-> pull request
-> tests
-> release observation
-> lesson learned
```

The pull request must cite the research finding ID when research materially influenced the design.

## 13. Success measures

- percentage of active project questions with current evidence;
- time from relevant external change to internal review;
- percentage of promoted findings with complete provenance;
- number of decisions changed by verified new evidence;
- repeated searches avoided through reusable research memory;
- stale or superseded finding rate;
- percentage of code changes linked to a hypothesis and evaluation result.

## 14. Safety boundary

Research output is advisory until approved. It must not be represented as local policy, clinical instruction, legal interpretation or operational order unless the authorized owner formally adopts it.
