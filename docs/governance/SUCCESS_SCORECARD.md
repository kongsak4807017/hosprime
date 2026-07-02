# HosPrime Success Scorecard

## 1. North Star

HosPrime succeeds when authorized users complete important organizational work faster and with better evidence, while privacy, safety, accountability and cost remain controlled.

The North Star is not the number of agents, documents or screens.

**North Star metric:**

> Percentage of approved target tasks completed with trusted evidence, within the expected time, without a material governance incident.

Formula:

```text
Trusted Task Completion Rate
= tasks completed with accepted output and complete evidence
  / total target tasks attempted
```

Milestone 1 pilot target: **at least 80 percent**.

## 2. Scorecard domains

### 2.1 User value and adoption

| Metric | Definition | M1 target | Source | Frequency |
|---|---|---:|---|---|
| Weekly active pilot users | Unique authorized users completing one target task per week | 60% of enrolled users | usage log | weekly |
| Repeat-use rate | Users returning in at least 3 of 4 weeks | 50% | usage log | monthly |
| Target task completion | Approved scenarios completed successfully | >=80% | UAT records | sprint |
| Median task time reduction | Baseline time minus HosPrime time divided by baseline | >=30% | time study | monthly |
| User usefulness score | Median 1–5 rating | >=4.0 | feedback | monthly |
| User trust score | Median 1–5 rating | >=4.0 | feedback | monthly |
| Abandonment rate | Started target tasks not completed | <=15% | product analytics | weekly |

### 2.2 Knowledge readiness

| Metric | Definition | M1 target |
|---|---|---:|
| Approved document coverage | Approved documents divided by identified priority documents | >=90% |
| Metadata completeness | Required metadata fields populated | >=95% |
| Named ownership | Documents with accountable owner | 100% |
| Review-date coverage | Documents with next review date | >=95% |
| Parsing success | Files producing usable text and page anchors | >=95% |
| Duplicate rate | Duplicate or near-duplicate active sources | <5% |
| Obsolete-source rate | Active sources beyond review or expiry date | <5% |

### 2.3 Retrieval quality

| Metric | Definition | M1 target |
|---|---|---:|
| Recall@5 | Relevant evidence found in top five chunks | >=0.85 |
| Recall@10 | Relevant evidence found in top ten chunks | >=0.92 |
| MRR | Reciprocal rank of first relevant source | >=0.70 |
| Retrieval precision@5 | Relevant chunks among top five | >=0.70 |
| Access-boundary violations | Unauthorized source returned | 0 |
| Retrieval p95 latency | 95th percentile retrieval time | <2 seconds |

### 2.4 Answer and citation trust

| Metric | Definition | M1 target |
|---|---|---:|
| Claim groundedness | Material claims entailed by approved evidence | >=0.90 |
| Citation precision | Citations that support the linked claim | >=0.90 |
| Citation completeness | Material claims with supporting citation | >=0.90 |
| False answer rate | Factual answer to unanswerable question | <2% |
| Fabricated-source rate | Invented source, title, page or identifier | 0 |
| Conflict disclosure | Conflicting evidence explicitly disclosed | >=95% |
| Correct no-answer behavior | Unanswerable questions refused safely | >=98% |
| Human reviewer acceptance | Answers accepted without major correction | >=85% |

### 2.5 Security, privacy and governance

| Metric | M1 target |
|---|---:|
| Unresolved P0 findings | 0 |
| Protected routes covered by authorization tests | 100% |
| Secret scanning coverage | 100% of commits and build artifacts |
| Critical dependency vulnerability without containment | 0 |
| Audit event coverage for sensitive actions | 100% |
| High-impact action without human approval | 0 |
| Cross-organization data leakage | 0 |
| Data-retention rule coverage | 100% of critical object types |
| Quarterly access review completion | 100% |

### 2.6 Reliability and operability

| Metric | Pilot target |
|---|---:|
| API availability | >=99.5% |
| p95 Oracle response latency | <10 seconds |
| Ingestion job success | >=95% |
| Mean time to detect P1 failure | <30 minutes |
| Mean time to recover P1 failure | <4 hours |
| Backup success | 100% scheduled jobs |
| Restore test success | 100% quarterly tests |
| Failed jobs with owner and reason | 100% |

### 2.7 Cost and efficiency

| Metric | Definition | Target |
|---|---|---:|
| Cost per accepted answer | AI and infrastructure cost divided by accepted answers | baseline then reduce 20% |
| Cost per active user | Monthly platform cost divided by WAU | tracked |
| Token budget variance | Actual versus approved budget | within 10% |
| Cache or retrieval reuse | Requests served without unnecessary generation | upward trend |
| Expensive-model utilization | Calls requiring approved high-cost model | <=20% unless justified |
| Cost attribution coverage | Calls linked to user, agent and purpose | 100% |

### 2.8 Delivery health

| Metric | Target |
|---|---:|
| Sprint goal achievement | >=80% |
| Escaped high-severity defects | 0 P0, <=2 P1 per release |
| Pull requests with acceptance evidence | 100% |
| Automated build pass rate on main | >=95% |
| Mean review time | <2 working days |
| Unplanned work | <20% of sprint capacity |
| Architecture decisions documented | 100% of material decisions |
| Open conditions past due | 0 critical, <10% total |

## 3. Benefit realization measures

Milestone 1 must measure at least three real organizational benefits:

1. time to find approved policy, SOP or historical evidence;
2. time to prepare an evidence-based executive brief;
3. percentage of repeated questions resolved without recreating analysis.

Later milestones may add:

- action completion improvement;
- reduction in lost decision rationale;
- data-quality improvement;
- reduced audit preparation effort;
- faster incident response;
- improved resource allocation;
- forecast value and avoided cost.

## 4. Baseline protocol

Before pilot release:

1. select 20–30 representative tasks;
2. observe current process without HosPrime;
3. record elapsed time, touch time, people involved, errors and rework;
4. repeat the tasks with HosPrime;
5. compare median and distribution, not only averages;
6. document qualitative changes in trust and workload.

A benefit cannot be claimed without a baseline or a defensible comparison.

## 5. Metric ownership

| Domain | Accountable owner |
|---|---|
| Adoption and value | Product Owner |
| Knowledge quality | Knowledge Owner / Data Governance |
| Retrieval and answer quality | AI Lead |
| Security and privacy | Security and Privacy Lead |
| Reliability | Platform Operations Lead |
| Cost | Product Owner and Finance |
| Delivery | Delivery Lead / PMO |

Every metric must have:

- owner;
- formula;
- source system;
- refresh frequency;
- target;
- warning threshold;
- escalation threshold.

## 6. Anti-gaming rules

- Document count does not equal knowledge coverage.
- Query count does not equal adoption.
- Positive feedback alone does not equal correctness.
- Similarity score does not equal answer confidence.
- Approved plan does not equal executed outcome.
- Agent count does not equal workforce capacity.
- Demo success does not equal pilot acceptance.
- Average latency must not hide p95 or failure rates.

## 7. Monthly executive score

Use a weighted score only after raw metrics are visible.

Suggested M1 weighting:

```text
User value and adoption       25%
Answer and citation trust     25%
Knowledge readiness           15%
Security and governance       15%
Reliability and operability   10%
Cost efficiency                5%
Delivery health                5%
```

A high weighted score cannot override a P0 stop condition.
