# M1-B Controlled Authorized Packet Execution Checklist

Status: controlled RELEASE artifact / checklist guidance only / non-authoritative for source approval  
Release target: Milestone 1 — Governed Knowledge Oracle MVP  
Parent issue: #10  
Memory epic: #8  
Control issue: #119  
Previous stage: REVIEW (#118)  
Current stage: RELEASE  
Next stage: OBSERVE

## 1. Purpose and scope

This checklist gives a bounded, repeatable way to prepare later authorized source-owner packet execution for the five current M1-B source records.

It supports the North Star by improving evidence quality, decision-rights traceability, knowledge reuse and zero unauthorized high-impact action before any source is approved, ingested, indexed, activated in RAG or promoted into Organizational Memory.

This artifact is released as controlled checklist guidance only. It does not fill a real source-owner packet, authorize source-owner evidence collection, mutate the source register, approve sources, authorize ingestion, activate RAG, promote Organizational Memory or record any real-world execution outcome.

## 2. Non-authorization boundary

```text
SOURCE_REGISTER_MODIFIED = false
SOURCE_OWNER_EVIDENCE_COLLECTED = false
SOURCE_OWNER_ATTESTATION_CLAIMED = false
INDEPENDENT_REVIEW_CLAIMED = false
SOURCE_APPROVAL_CLAIMED = false
SOURCE_INGESTION_CLAIMED = false
SOURCE_PARSING_CLAIMED = false
SOURCE_EMBEDDING_CLAIMED = false
SOURCE_INDEXING_CLAIMED = false
RAG_ACTIVATION_CLAIMED = false
FACTUAL_ANSWER_PERMISSION_CLAIMED = false
ORGANIZATIONAL_MEMORY_PROMOTION_CLAIMED = false
EXTERNAL_FINDINGS_PROMOTED_TO_ORGANIZATIONAL_TRUTH = false
```

A completed packet-execution checklist is not source approval. Source approval requires a separate explicit human review decision with accountable reviewer identity, review record, limitations and gate evidence.

## 3. Release boundary

This RELEASE stage publishes the reviewed checklist as controlled guidance only.

```text
CONTROLLED_AUTHORIZED_PACKET_EXECUTION_GUIDANCE_RELEASED = true
RELEASE_SCOPE = controlled_guidance_only
RELEASE_MAY_AUTHORIZE_SOURCE_OWNER_PACKET_EXECUTION = false
RELEASE_MAY_MUTATE_SOURCE_REGISTER = false
RELEASE_MAY_APPROVE_SOURCE = false
RELEASE_MAY_INGEST_PARSE_EMBED_OR_INDEX_SOURCE = false
RELEASE_MAY_ACTIVATE_RAG = false
RELEASE_MAY_PROMOTE_ORGANIZATIONAL_MEMORY = false
RELEASE_MAY_CLAIM_REAL_WORLD_ACTION_COMPLETION = false
```

## 4. Source scope

The checklist covers exactly these five current source IDs from `data/source_register/m1_source_register.yml`:

```text
M1A-PM25-001
M1A-TB-001
M1A-NCD-001
M1A-EOC-001
M1A-DIGITAL-001
```

```text
SOURCE_COUNT_COVERED_BY_CHECKLIST = 5 / 5
```

## 5. Role separation matrix

| Role | May do in later authorized packet execution | Must not do |
|---|---|---|
| source_inventory_operator | prepare packet fields, locate controlled file/system path, record checksum pending reason | approve source, change lifecycle to APPROVED, activate RAG |
| program_source_owner | attest custody, context, ownership boundary and source period | self-approve source, bypass independent review |
| data_governance_lead | confirm classification/access boundary and route reviewer | loosen restricted access without review, approve source alone |
| independent_knowledge_reviewer | perform readiness precheck and record limitations | claim technical ingestion/indexing success |
| technical_ingestion_operator | later ingest only after source approval and technical gate | ingest before approval, activate retrieval without evaluation |
| executive_sponsor | authorize request for source review | convert packet receipt into source approval or real-world completion |

## 6. Packet field-group checklist

Every later authorized packet execution must check all ten field groups for every source record.

| # | Field group | Required completion evidence or pending reason | Minimum accountable role | Boundary |
|---|---|---|---|---|
| 1 | source_identity | source ID, source title, knowledge pack and source type verified against register | source_inventory_operator | identity verification is not approval |
| 2 | organization_scope | responsible organization or office confirmed, or explicit pending reason | accountable_sponsor or data_governance_lead | organization confirmation is not active RAG permission |
| 3 | accountable_sponsor | sponsor person/office authorized to request source review, or pending reason | public-health executive or delegated sponsor | sponsor authorization is not source approval |
| 4 | source_owner | named source owner person/office or explicit pending assignment | program_source_owner | source-owner custody is not independent review |
| 5 | controlled_location | controlled file, system, repository or custody location, or pending inventory reason | source_inventory_operator | locating a file is not ingestion |
| 6 | version_or_source_period | version, date range, operational period or replacement rule | source_inventory_operator | period metadata is not freshness certification |
| 7 | checksum_or_checksum_pending_reason | checksum, integrity method or pending reason | source_inventory_operator | checksum is not quality approval |
| 8 | classification_and_access | classification, access policy and allowed roles preserved from register or routed for review | data_governance_lead | access cannot be expanded by packet execution |
| 9 | reviewer_precheck_routing | named reviewer/reviewer office or explicit pending assignment | data_governance_lead | routing is not review decision |
| 10 | provenance_and_limitations | provenance path, method, assumptions, limitations and applicability boundary | knowledge_reviewer | provenance is not factual-answer permission |

```text
FIELD_GROUPS_PER_SOURCE = 10
TOTAL_PACKET_FIELD_GROUPS_COVERED_BY_CHECKLIST = 5 sources x 10 groups = 50 / 50
```

## 7. Per-source execution rows

| Source ID | Knowledge pack | Required groups | Restricted handling note | Later authorized next action |
|---|---|---:|---|---|
| M1A-PM25-001 | PM2.5 and Environmental Health | 10 / 10 | internal, role-scoped access | Prepare owner-confirmation packet without changing register state |
| M1A-TB-001 | Tuberculosis and Communicable Disease Control | 10 / 10 | restricted_internal; sensitive program context possible | Prepare restricted packet and route reviewer before any approval claim |
| M1A-NCD-001 | NCD and Chronic Care Service Model | 10 / 10 | internal, role-scoped access | Prepare owner-confirmation packet without factual-answer permission |
| M1A-EOC-001 | Disaster, EOC and Public Health Emergency Operations | 10 / 10 | restricted_internal; incident context possible | Prepare restricted packet and preserve operational sensitivity boundary |
| M1A-DIGITAL-001 | Digital Health, Data Governance and AI Workflow | 10 / 10 | internal, role-scoped access | Prepare owner-confirmation packet without Organizational Memory promotion |

## 8. Required receipt fields for later collection only

A later authorized operator may use these receipt fields only after a separate authorized packet-execution stage exists. This RELEASE stage records no actual receipt.

```text
source_id
packet_id
field_group_name
evidence_value_or_pending_reason
source_owner_or_accountable_office
provenance_path_or_controlled_location
version_or_source_period
checksum_or_integrity_pending_reason
classification_and_access_boundary
limitation_note
attestation_timestamp
executor_identity_or_authorized_role
reviewer_routing_target
non_approval_boundary_acknowledgement
```

## 9. Review precheck gate

A packet can move to independent review precheck only when:

```text
ALL_10_FIELD_GROUPS_PRESENT_OR_PENDING_WITH_REASON = true
NON_APPROVAL_BOUNDARY_ACKNOWLEDGED = true
SOURCE_OWNER_SELF_APPROVAL_ATTEMPTED = false
SOURCE_REGISTER_STATE_CHANGE_ATTEMPTED = false
ACCESS_POLICY_EXPANSION_ATTEMPTED = false
RAG_ACTIVATION_ATTEMPTED = false
```

## 10. Prohibited claims

The following claims are prohibited from this checklist and from later packet execution unless separate gate evidence exists:

```text
PROHIBITED_CLAIM_SOURCE_APPROVED = true
PROHIBITED_CLAIM_SOURCE_INGESTED = true
PROHIBITED_CLAIM_SOURCE_PARSED = true
PROHIBITED_CLAIM_SOURCE_EMBEDDED = true
PROHIBITED_CLAIM_SOURCE_INDEXED = true
PROHIBITED_CLAIM_ACTIVE_RAG_READY = true
PROHIBITED_CLAIM_FACTUAL_ANSWER_ALLOWED = true
PROHIBITED_CLAIM_ORGANIZATIONAL_MEMORY_PROMOTED = true
PROHIBITED_CLAIM_REAL_WORLD_ACTION_COMPLETED_WITHOUT_RECEIPT_AUDIT_AND_OBSERVED_OUTCOME = true
```

## 11. Next-stage OBSERVE criteria

The next OBSERVE stage should verify whether the released guidance remains bounded as guidance only.

```text
CHECKLIST_STATUS_RELEASED_AS_GUIDANCE_ONLY = true
RELEASE_BOUNDARY_VISIBLE = true
SOURCE_REGISTER_MODIFIED = false
SOURCE_OWNER_EVIDENCE_COLLECTED = false
SOURCE_APPROVAL_CLAIMED = false
RAG_ACTIVATION_CLAIMED = false
ORGANIZATIONAL_MEMORY_PROMOTION_CLAIMED = false
CI_PASS_CLAIMED_ONLY_IF_WORKFLOW_EVIDENCE_EXISTS = true
```

## 12. Acceptance result for this RELEASE artifact

```text
M1_B_RELEASE_COMPLETED = true
CONTROLLED_AUTHORIZED_PACKET_EXECUTION_GUIDANCE_RELEASED = true
RELEASE_SCOPE = controlled_guidance_only
SOURCE_COUNT_COVERED_BY_CHECKLIST = 5 / 5
PACKET_FIELD_GROUPS_COVERED_BY_CHECKLIST = 50 / 50
SOURCE_REGISTER_MODIFIED = false
SOURCE_OWNER_EVIDENCE_COLLECTED = false
SOURCE_APPROVAL_CLAIMED = false
RAG_ACTIVATION_CLAIMED = false
NEXT_STAGE = OBSERVE
```
