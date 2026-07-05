# HosPrime Engineering Run 0064 — M1-B Source Owner Evidence Collection Execution Readiness Research

Date: 2026-07-05
Stage: RESEARCH
Parent issue: #10
Memory epic: #8
Control issue: #82
Previous stage: BASELINE (#81)
Next stage: HYPOTHESIS

## North Star outcome supported

Enable healthcare and public-health organizations to use trusted data, knowledge, organizational memory and governed AI to complete real work and make better decisions faster, with evidence, accountability and continuous learning.

This bounded RESEARCH stage supports evidence quality, user trust, decision-to-outcome traceability, knowledge reuse and zero unauthorized high-impact action by staging official guidance for a later controlled filled-packet workflow before any source-owner evidence is collected.

## Repository evidence checked before selecting work

- `README.md` on `main` was read before work selection and confirms the North Star, ordered Loop Engineering sequence, Core Rules, memory boundaries and current controlled release target: Milestone 1 — Governed Knowledge Oracle MVP.
- Open issue #82 is the active ordered M1-B stage: RESEARCH after #81 BASELINE.
- Previous run inspected: `engineering_runs/2026-07-05/0063-m1b-source-owner-evidence-collection-execution-readiness-baseline.md`.
- Maturity gate inspected: `docs/governance/MATURITY_GATES.md`.
- Source register inspected only: `data/source_register/m1_source_register.yml`.
- Open issue inspection identified #10 as the parent governed source lifecycle workstream and #82 as the active sequenced control issue.
- PR inspection found no newer user PR superseding this bounded stage.

## Real organizational work problem

HosPrime has a released collection-readiness packet and an execution-readiness baseline, but a later filled-packet workflow must be designed against current primary or official guidance before anyone collects source-owner evidence.

The immediate problem is not lack of more documents or agents. The problem is that the future collection workflow must preserve provenance, source ownership, identity/access boundaries, human review, uncertainty, and explicit non-activation until approved.

## Real users and real work need

- Public-health executive / accountable sponsor: needs assurance that future source-owner collection will not become an unsupported factual-answer or high-impact action pathway.
- Provincial program source owner: needs a clear evidence-collection route that records authority and limitations without making the owner an automatic approver.
- Source inventory operator: needs official guidance for what must be captured before controlled files/systems are processed.
- Data governance lead: needs access, classification, privacy and accountability controls before any source moves beyond placeholder status.
- Knowledge reviewer / independent reviewer: needs reviewable provenance and limitations to decide whether a filled packet is eligible for later source-register update.

## Baseline and target carried forward

```text
DECISION_RIGHTS_READINESS_GAP_RATE = 50.0%
FULLY_COLLECTION_READY_RECORDS = 0 / 5
FULLY_REVIEW_READY_RECORDS = 0 / 5
FULLY_APPROVED_RECORDS = 0 / 5
ACTIVE_RAG_RECORDS = 0 / 5

TARGET_DECISION_RIGHTS_READINESS_GAP_RATE_AFTER_LATER_FILLED_PACKET <= 30%
TARGET_FULLY_COLLECTION_READY_RECORDS_AFTER_LATER_FILLED_PACKET >= 3 / 5
TARGET_FULLY_APPROVED_RECORDS = 0 unless authorized human review evidence exists
TARGET_ACTIVE_RAG_RECORDS = 0 until approved source, retrieval evaluation and activation gate exist
```

This RESEARCH run does not claim any target improvement.

## Research staging method

Only official or primary sources were used for this stage. Findings are staged as design inputs, not Organizational Memory / Governed RAG truth. They must be reviewed before use in policy, source approval, ingestion, indexing, retrieval, or factual answering.

## Official guidance staged

### 1. NIST AI Risk Management Framework and AI RMF updates

Source checked: NIST AI Risk Management Framework official page.

Key staged finding:

- NIST describes AI RMF 1.0 as a voluntary framework for improving the ability to incorporate trustworthiness considerations into AI design, development, use and evaluation.
- NIST notes AI RMF 1.0 is being revised and that NIST released a Generative AI Profile on 2024-07-26 plus a critical-infrastructure concept note on 2026-04-07.

Implication for future HosPrime filled-packet workflow:

- Treat source-owner collection as an AI governance input to Map/Measure/Manage-style controls, not as automatic organizational truth.
- Record source purpose, intended use, limitation, risk sensitivity, accountable reviewer and evidence sufficiency before any AI use.
- Add a research-staging freshness check because AI RMF is explicitly under revision.

Official URL: https://www.nist.gov/itl/ai-risk-management-framework

### 2. NIST SP 800-53 Rev. 5, Release 5.2.0 planning note

Source checked: NIST CSRC official SP 800-53 Rev. 5 page.

Key staged finding:

- NIST SP 800-53 provides a catalog of security and privacy controls for information systems and organizations.
- NIST records an August 27, 2025 planning note for Release 5.2.0 updates, including control and discussion changes.
- The page identifies relevant control families including Access Control, Audit and Accountability, Identification and Authentication, PII Processing and Transparency, Risk Assessment, System and Services Acquisition, and Supply Chain Risk Management.

Implication for future HosPrime filled-packet workflow:

- The packet should require identity of submitter/reviewer, access policy, classification, audit event reference, provenance, retention/review date, and a no-activation boundary.
- Crosswalks must not be treated as equivalency; HosPrime should map controls as design rationale only until reviewed.

Official URL: https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final

### 3. WHO ethics and governance of AI for health

Source checked: WHO official publication page, `Ethics and governance of artificial intelligence for health`, dated 2021-06-28.

Key staged finding:

- WHO identifies this as guidance for AI ethics and governance in health.

Implication for future HosPrime filled-packet workflow:

- Because HosPrime is health/public-health oriented, the collection workflow should preserve human accountability, evidence provenance, limitations, and review before AI-assisted factual answers or operational recommendations.
- Health-sector use raises higher trust and governance requirements than a generic document inventory.

Official URL: https://www.who.int/publications/i/item/9789240029200

### 4. WHO guidance on large multi-modal models for health

Source checked: WHO official publication page, `Ethics and governance of artificial intelligence for health: Guidance on large multi-modal models`, dated 2025-03-25.

Key staged finding:

- WHO states the guidance addresses large multi-modal models, a type of generative AI, and notes that LMMs may have wide use in health care, scientific research, public health and drug development.

Implication for future HosPrime filled-packet workflow:

- Since HosPrime may use generative AI or LMM-style interfaces later, collected source evidence must not be mixed with unreviewed model output.
- The packet should distinguish source evidence, submitter assertion, AI-generated summary, reviewer decision, and final approved organizational memory.

Official URL: https://www.who.int/publications/i/item/9789240084759

### 5. ISO/IEC 42001:2023 AI management system

Source checked: ISO official standard page.

Key staged finding:

- ISO/IEC 42001:2023 is an international standard for an artificial intelligence management system.
- ISO describes it as specifying requirements for establishing, implementing, maintaining and continually improving an AIMS, and designed for organizations providing or using AI-based products or services.
- ISO highlights traceability, transparency and reliability as benefits.

Implication for future HosPrime filled-packet workflow:

- The later workflow should be framed as part of an AI management system control, with repeatable Plan-Do-Check-Act evidence, owner/reviewer accountability, traceability and continuous improvement.
- Do not claim ISO conformity; use it only as an official design reference until a formal review and compliance decision exists.

Official URL: https://www.iso.org/standard/42001

## Research-to-design constraints for next HYPOTHESIS stage

The next HYPOTHESIS should test whether a controlled filled-packet workflow can reduce the decision-rights readiness gap without approving or activating any source.

Minimum constraints to carry forward:

1. Use official guidance only as Research Staging until reviewed.
2. Require submitter identity, source-owner role, organization, controlled source location, version/currentness, checksum or non-file verification, classification, access policy, limitation, and reviewer routing.
3. Separate source-owner assertion from authorized reviewer decision.
4. Record no-activation boundary in every filled packet.
5. Preserve auditability: who submitted, what was checked, what remained unresolved, who may review, and what cannot yet be claimed.
6. Do not update `data/source_register/m1_source_register.yml` until a later reviewed filled packet exists.
7. Do not ingest, parse, embed, index, answer from, or activate any source during collection readiness.

## Work completed in this run

- Read the latest README North Star, Core Rules, ordered loop, memory boundaries and controlled release target.
- Inspected open issue #82, maturity gates, source register, recent PR list and previous baseline evidence.
- Conducted bounded official-source research for controlled source-owner evidence collection workflow design.
- Staged findings in this engineering-run evidence package only.
- Did not collect source-owner evidence.
- Did not modify `data/source_register/m1_source_register.yml`.
- Did not approve, ingest, parse, embed, index, answer from, or activate any source.

## Acceptance result

```text
M1_B_RESEARCH_COMPLETED = true
OFFICIAL_GUIDANCE_FOR_CONTROLLED_COLLECTION_WORKFLOW_STAGED = true
RESEARCH_STAGING_ONLY = true
SOURCE_REGISTER_MODIFIED = false
SOURCE_OWNER_EVIDENCE_COLLECTED = false
SOURCE_APPROVAL_CLAIMED = false
SOURCE_INGESTION_CLAIMED = false
SOURCE_PARSING_CLAIMED = false
SOURCE_EMBEDDING_CLAIMED = false
SOURCE_INDEXING_CLAIMED = false
RAG_ACTIVATION_CLAIMED = false
FACTUAL_ANSWER_PERMISSION_CLAIMED = false
ORGANIZATIONAL_MEMORY_PROMOTION_CLAIMED = false
CI_PASS_CLAIMED = false
NEXT_STAGE = HYPOTHESIS
```

## Memory layer affected

Affected:

- Research Staging;
- engineering-run evidence;
- issue traceability.

Not affected:

- Personal/Staff Twin Memory;
- Person Memory;
- Role Memory;
- Organizational Memory / Governed RAG;
- source-register approval status;
- source-register active-RAG status.

## Risks and blockers

```text
RISK_EXTERNAL_GUIDANCE_NEEDS_LOCAL_REVIEW = true
RISK_AI_RMF_REVISION_IN_PROGRESS = true
RISK_UNRESOLVED_OWNER_ASSIGNMENT = true
RISK_UNRESOLVED_CONTROLLED_LOCATION = true
RISK_UNRESOLVED_VERSION_AND_CHECKSUM = true
RISK_UNRESOLVED_REVIEWER_ROUTING = true
RISK_PREMATURE_APPROVAL_OR_RAG_ACTIVATION = controlled_by_non_approval_boundary
```

## Single next stage

HYPOTHESIS — define a testable hypothesis for a controlled filled-packet workflow that may reduce decision-rights readiness gaps while preserving non-approval, non-ingestion and non-activation boundaries.
