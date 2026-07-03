# HosPrime Twin Taxonomy

Status: Controlled taxonomy  
Scope: Healthcare Twin Ecosystem

## 1. Purpose

This document defines the initial twin taxonomy for HosPrime. It prevents the product from using the term Digital Twin too broadly and creates a controlled naming system for architecture, UI, API, data model and governance.

## 2. Definition

A HosPrime Twin is a governed digital representation of a real organizational entity, process, role, resource, knowledge object, decision or AI agent.

A valid twin must have:

- a unique identifier;
- an owner;
- a user group;
- at least one data source or approved knowledge source;
- relationships to other twins;
- status or metrics;
- decision, task or learning relevance;
- audit and provenance requirements.

## 3. Twin families

### 3.1 Organization Twin

Represents a public-health organization or healthcare organization.

Examples:

- Ministry or department unit
- Health region
- Provincial public health office
- Hospital
- District health office
- Primary care network

Primary users:

- executives;
- provincial public health officers;
- hospital directors;
- regional inspectors.

### 3.2 Hospital Twin

Represents the whole hospital as an operating entity.

Core views:

- executive status;
- OPD, ER, IPD and bed pressure;
- finance and claims;
- workforce pressure;
- quality and safety;
- risk and incident state;
- decision timeline.

### 3.3 Department Twin

Represents a department, service unit, cost center or management unit.

Examples:

- OPD;
- ER;
- IPD ward;
- pharmacy;
- laboratory;
- finance;
- HR;
- IT;
- procurement;
- quality.

### 3.4 Process Twin

Represents a workflow that crosses people, departments and systems.

Examples:

- OPD flow;
- ER triage to admission;
- IPD discharge;
- referral;
- claim submission;
- procurement;
- incident management;
- meeting to decision to action.

### 3.5 Workforce / Staff Twin

Represents a person, position or role in the organization. Person Memory and Role Memory must remain separated.

Views:

- role responsibility;
- tasks;
- calendar;
- workload;
- competency;
- assigned KPI;
- knowledge needs;
- decision participation.

### 3.6 Patient Group Twin

Represents a governed patient cohort or service group, not an unrestricted individual patient replica.

Examples:

- DM high-risk group;
- HT uncontrolled group;
- CKD stage 4-5;
- TB lost-to-follow-up risk;
- elderly dependency group;
- disaster-affected patient group.

Patient-level twin functionality must be treated as a high-risk future capability with stricter privacy, clinical and approval controls.

### 3.7 Population Twin

Represents population health patterns across geography and time.

Examples:

- province population health;
- NCD burden;
- TB surveillance;
- dengue hotspots;
- PM2.5 vulnerable groups;
- aging and long-term care demand;
- resource distribution.

### 3.8 Asset Twin

Represents equipment, vehicles, infrastructure or digital assets.

Examples:

- ambulance;
- ventilator;
- CT/MRI;
- generator;
- UPS;
- network device;
- server;
- IoT sensor.

### 3.9 Knowledge Twin

Represents a governed knowledge object.

Examples:

- SOP;
- policy;
- guideline;
- TOR;
- meeting minutes;
- lesson learned;
- report;
- research summary.

### 3.10 Decision Twin

Represents a decision event or recommendation lifecycle.

Core fields:

- context;
- evidence;
- recommendation;
- alternatives;
- confidence;
- policy references;
- conflict flags;
- approving authority;
- outcome;
- lesson learned.

### 3.11 AI Agent Twin

Represents an AI agent as an auditable operating entity.

Core fields:

- agent role;
- owner;
- data access;
- tools;
- risk tier;
- recommendation history;
- approval rate;
- error rate;
- evidence completeness;
- policy compliance;
- incident record.

### 3.12 Governance Twin

Represents policy, compliance, risk and audit state.

Examples:

- PDPA control;
- cybersecurity control;
- access control;
- audit finding;
- model approval;
- risk register item;
- maturity gate.

### 3.13 Project Twin

Represents a project, initiative or improvement program.

Views:

- objective;
- owner;
- budget;
- milestones;
- risks;
- decisions;
- tasks;
- evidence;
- outcome metrics.

### 3.14 Budget Twin

Represents budget, cost center, procurement package or financial plan.

Views:

- allocation;
- commitment;
- spending;
- variance;
- claim status;
- financial risk;
- approval history.

### 3.15 Incident Twin

Represents a disaster, cyber incident, patient-safety incident or operational disruption.

Views:

- event timeline;
- impact;
- response team;
- decisions;
- resources;
- escalation;
- outcome;
- lesson learned.

## 4. Naming convention

```text
TWIN-{TYPE}-{ORG}-{YYYY}-{SEQUENCE}
```

Examples:

```text
TWIN-HOSP-CRH-2026-0001
TWIN-DEPT-OPD-2026-0001
TWIN-STAFF-ROLE-2026-0001
TWIN-DECISION-2026-0001
```

## 5. Status model

Every twin should support a simple traffic-light state for executive readability:

```text
GREEN = operating within agreed threshold
YELLOW = risk emerging or evidence incomplete
RED = action or escalation required
GRAY = insufficient data or not yet governed
```

## 6. Maturity state

```text
L0 Concept only
L1 Manual profile
L2 Data-connected profile
L3 Evidence-linked twin
L4 Decision-linked twin
L5 Outcome-learning twin
```

A twin should not be labeled production-ready until it reaches at least L3 with evidence, owner and governance controls.
