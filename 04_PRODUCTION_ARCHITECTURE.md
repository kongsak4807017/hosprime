# HosPRIME - Production Architecture

## 1. Architecture Overview

HosPRIME follows a **Cloud-Native, Microservices-Ready Architecture** designed for scalability, reliability, and maintainability.

### 1.1 Architecture Principles
- **Separation of Concerns**: Clear boundaries between frontend, backend, data, and AI layers
- **Scalability**: Horizontal scaling capability at every layer
- **Resilience**: Fault tolerance and graceful degradation
- **Security**: Defense in depth, zero-trust principles
- **Observability**: Comprehensive logging, monitoring, and tracing

### 1.2 Architecture Style
**Current:** Modular Monolith (Phase 1)
**Future:** Microservices (Phase 2+)

## 2. System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     CLIENT LAYER                            │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐          │
│  │  Browser   │  │   Tablet   │  │   Mobile   │          │
│  │  (Chrome,  │  │   (iPad)   │  │ (Responsive)│         │
│  │  Firefox)  │  │            │  │            │          │
│  └──────┬─────┘  └──────┬─────┘  └──────┬─────┘          │
└─────────┼────────────────┼────────────────┼────────────────┘
          │ HTTPS/TLS      │ HTTPS/TLS      │ HTTPS/TLS
          └────────────────┴────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                   EDGE LAYER                                 │
│  ┌────────────────────────────────────────────────────┐    │
│  │         Load Balancer / API Gateway                 │    │
│  │         (Nginx / AWS ALB / Kubernetes Ingress)      │    │
│  │  - SSL Termination                                  │    │
│  │  - Rate Limiting                                    │    │
│  │  - DDoS Protection                                  │    │
│  └──────────────────┬─────────────────────────────────┘    │
└─────────────────────┼──────────────────────────────────────┘
                      │
        ┌─────────────┴─────────────┐
        │                           │
┌───────▼────────┐         ┌────────▼────────┐
│ FRONTEND LAYER │         │  BACKEND LAYER  │
│                │         │                 │
│ ┌────────────┐ │         │ ┌─────────────┐ │
│ │   React    │ │         │ │  FastAPI    │ │
│ │   19.0.0   │ │         │ │  Backend    │ │
│ │            │ │         │ │  (Port 8001)│ │
│ │ - Radix UI │ │         │ │             │ │
│ │ - Tailwind │ │         │ │ ┌─────────┐ │ │
│ │ - React    │ │         │ │ │  Auth   │ │ │
│ │   Router   │ │         │ │ │ Service │ │ │
│ │            │ │         │ │ └─────────┘ │ │
│ │ Port 3000  │ │         │ │             │ │
│ └────────────┘ │         │ │ ┌─────────┐ │ │
│                │         │ │ │ Patient │ │ │
│                │         │ │ │ Service │ │ │
│                │         │ │ └─────────┘ │ │
│                │         │ │             │ │
│                │         │ │ ┌─────────┐ │ │
│                │         │ │ │   Lab   │ │ │
│                │         │ │ │ Service │ │ │
│                │         │ │ └─────────┘ │ │
│                │         │ │             │ │
│                │         │ │ ┌─────────┐ │ │
│                │         │ │ │Pharmacy │ │ │
│                │         │ │ │ Service │ │ │
│                │         │ │ └─────────┘ │ │
│                │         │ │             │ │
│                │         │ │ ┌─────────┐ │ │
│                │         │ │ │ Billing │ │ │
│                │         │ │ │ Service │ │ │
│                │         │ │ └─────────┘ │ │
│                │         │ └─────────────┘ │
└────────────────┘         └─────────┬───────┘
                                     │
              ┌──────────────────────┼──────────────────────┐
              │                      │                      │
              │                      │                      │
┌─────────────▼──────┐    ┌──────────▼─────────┐  ┌────────▼────────┐
│   DATA LAYER       │    │   CACHE LAYER      │  │  AI/ML LAYER    │
│                    │    │                    │  │                 │
│ ┌────────────────┐ │    │ ┌────────────────┐ │  │ ┌─────────────┐ │
│ │    MongoDB     │ │    │ │     Redis      │ │  │ │ LLM Service │ │
│ │   (Primary)    │ │    │ │   (Future)     │ │  │ │             │ │
│ │                │ │    │ │                │ │  │ │ - GPT-5.2   │ │
│ │ - patients     │ │    │ │ - Sessions     │ │  │ │ - Claude 4.5│ │
│ │ - appointments │ │    │ │ - API Cache    │ │  │ │ - Gemini 3  │ │
│ │ - staff        │ │    │ │ - Real-time    │ │  │ │             │ │
│ │ - prescriptions│ │    │ │   Data         │ │  │ │ Emergent    │ │
│ │ - lab_tests    │ │    │ │                │ │  │ │ Universal   │ │
│ │ - billing      │ │    │ └────────────────┘ │  │ │ Key         │ │
│ │ - beds         │ │    │                    │  │ └─────────────┘ │
│ │ - audit_logs   │ │    │                    │  │                 │
│ └────────────────┘ │    └────────────────────┘  │ ┌─────────────┐ │
│                    │                             │ │   Neo4j     │ │
│ ┌────────────────┐ │                             │ │ Knowledge   │ │
│ │     Neo4j      │ │                             │ │   Graph     │ │
│ │  Graph Database│ │                             │ │             │ │
│ │                │ │                             │ │ - Diseases  │ │
│ │ - Medical      │ │                             │ │ - Drugs     │ │
│ │   Knowledge    │ │                             │ │ - Symptoms  │ │
│ │ - Drug         │ │                             │ │ - Relations │ │
│ │   Interactions │ │                             │ └─────────────┘ │
│ │ - Clinical     │ │                             │                 │
│ │   Pathways     │ │                             │ ┌─────────────┐ │
│ └────────────────┘ │                             │ │ML Prediction│ │
│                    │                             │ │  Models     │ │
└────────────────────┘                             │ │             │ │
                                                   │ │ - No-Show   │ │
                                                   │ │ - Bed Demand│ │
                                                   │ │ - Risk Score│ │
                                                   │ └─────────────┘ │
                                                   └─────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                 OBSERVABILITY LAYER                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │ Logging  │  │Monitoring│  │ Tracing  │  │  Alerts  │  │
│  │(Future:  │  │(Future:  │  │(Future:  │  │(Future:  │  │
│  │ELK/Loki) │  │Prometheus│  │  Jaeger) │  │PagerDuty)│  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## 3. Component Architecture

### 3.1 Frontend Architecture

**Technology:** React 19.0.0 + Radix UI + Tailwind CSS

**Structure:**
```
frontend/
├── src/
│   ├── components/          # Reusable UI components
│   │   ├── common/          # Buttons, inputs, cards
│   │   ├── patient/         # Patient-specific components
│   │   ├── appointment/     # Appointment components
│   │   ├── pharmacy/        # Pharmacy components
│   │   └── dashboard/       # Dashboard widgets
│   ├── pages/               # Page-level components
│   │   ├── Dashboard.js
│   │   ├── Patients.js
│   │   ├── Appointments.js
│   │   └── ...
│   ├── services/            # API service layer
│   │   ├── api.js           # Axios configuration
│   │   ├── patientService.js
│   │   ├── appointmentService.js
│   │   └── ...
│   ├── hooks/               # Custom React hooks
│   ├── utils/               # Utility functions
│   ├── context/             # React Context for state
│   └── App.js               # Main application
```

**Key Patterns:**
- Component-based architecture
- Custom hooks for business logic
- Service layer for API communication
- Context API for global state
- React Query for server state management

### 3.2 Backend Architecture

**Technology:** FastAPI + Python 3.11+

**Structure:**
```
backend/
├── server.py                # Main application entry
├── config/
│   ├── settings.py          # Configuration management
│   └── database.py          # Database connections
├── models/                  # Pydantic models
│   ├── patient.py
│   ├── appointment.py
│   ├── staff.py
│   └── ...
├── routers/                 # API route handlers
│   ├── patients.py
│   ├── appointments.py
│   ├── pharmacy.py
│   ├── lab.py
│   ├── billing.py
│   └── ai_assistant.py
├── services/                # Business logic layer
│   ├── patient_service.py
│   ├── appointment_service.py
│   ├── ai_service.py
│   └── ...
├── repositories/            # Data access layer
│   ├── patient_repository.py
│   ├── appointment_repository.py
│   └── ...
├── middleware/              # Custom middleware
│   ├── auth_middleware.py
│   └── logging_middleware.py
├── utils/
│   ├── security.py          # JWT, hashing
│   └── validators.py
└── requirements.txt
```

**Key Patterns:**
- **Layered Architecture**: Router → Service → Repository
- **Dependency Injection**: FastAPI's DI system
- **API Versioning**: /api/v1/
- **Error Handling**: Centralized exception handlers
- **Validation**: Pydantic models

### 3.3 Database Architecture

#### 3.3.1 MongoDB (Primary Database)

**Collections:**
```
- patients              # Patient master data
- appointments          # Appointment scheduling
- staff                 # Healthcare staff
- prescriptions         # Medication prescriptions
- drugs                 # Drug inventory
- lab_tests             # Laboratory tests and results
- invoices              # Billing invoices
- payments              # Payment transactions
- beds                  # Bed/room management
- audit_logs            # System audit trail
- users                 # Authentication
```

**Indexing Strategy:**
```javascript
// patients collection
db.patients.createIndex({ "patient_number": 1 }, { unique: true })
db.patients.createIndex({ "email": 1 })
db.patients.createIndex({ "phone": 1 })
db.patients.createIndex({ "first_name": 1, "last_name": 1 })

// appointments collection
db.appointments.createIndex({ "patient_id": 1 })
db.appointments.createIndex({ "doctor_id": 1 })
db.appointments.createIndex({ "appointment_date": 1, "appointment_time": 1 })
db.appointments.createIndex({ "status": 1 })

// lab_tests collection
db.lab_tests.createIndex({ "patient_id": 1 })
db.lab_tests.createIndex({ "test_number": 1 }, { unique: true })
db.lab_tests.createIndex({ "status": 1 })
```

#### 3.3.2 Neo4j (Knowledge Graph)

**Node Types:**
- Disease
- Symptom
- Treatment
- Drug
- Patient (lightweight reference)

**Relationship Types:**
- (Disease)-[:HAS_SYMPTOM]->(Symptom)
- (Disease)-[:TREATED_BY]->(Treatment)
- (Treatment)-[:USES_DRUG]->(Drug)
- (Drug)-[:INTERACTS_WITH]->(Drug)
- (Patient)-[:DIAGNOSED_WITH]->(Disease)

**Indexes:**
```cypher
CREATE INDEX disease_name FOR (d:Disease) ON (d.name)
CREATE INDEX drug_name FOR (dr:Drug) ON (dr.name)
CREATE INDEX symptom_name FOR (s:Symptom) ON (s.name)
```

### 3.4 AI/ML Architecture

#### 3.4.1 LLM Integration Layer

**Provider:** Emergent Universal Key

**Models:**
1. **GPT-5.2** - Complex reasoning, diagnosis assistance
2. **Claude Sonnet 4.5** - Medical knowledge, treatment plans
3. **Gemini 3 Flash** - Quick queries, chatbot

**Integration Pattern:**
```python
from emergentintegrations import LLMClient

class AIService:
    def __init__(self):
        self.llm_client = LLMClient(api_key=EMERGENT_KEY)
    
    async def generate_diagnosis_suggestions(self, symptoms, history):
        prompt = self._build_diagnosis_prompt(symptoms, history)
        response = await self.llm_client.chat(
            model="gpt-5.2",
            messages=[{"role": "user", "content": prompt}]
        )
        return self._parse_diagnosis_response(response)
```

#### 3.4.2 ML Model Architecture

**Model Storage:**
- Models stored in `/backend/ml_models/`
- Version control for model artifacts
- A/B testing capability

**Prediction Pipeline:**
```
Request → Feature Extraction → Model Inference → Post-processing → Response
```

**Models:**
1. **No-Show Prediction**: sklearn RandomForest
2. **Bed Demand Forecasting**: Prophet (time series)
3. **Patient Risk Scoring**: XGBoost

## 4. Deployment Architecture

### 4.1 Development Environment

```
Local Machine
├── Docker Compose
│   ├── MongoDB Container
│   ├── Neo4j Container
│   ├── Redis Container (future)
│   └── Backend Container
├── Node.js (Frontend dev server)
└── Supervisord (Process management)
```

### 4.2 Production Environment (Future)

**Platform:** Kubernetes on AWS/GCP/Azure

```
Kubernetes Cluster
├── Ingress Controller (Nginx)
├── Frontend Deployment (3+ replicas)
├── Backend Deployment (5+ replicas)
├── MongoDB StatefulSet (Replica Set)
├── Neo4j StatefulSet
├── Redis StatefulSet
└── Horizontal Pod Autoscaler
```

**Services:**
- **Load Balancer**: AWS ALB / GCP Load Balancer
- **CDN**: CloudFront / CloudFlare
- **Object Storage**: S3 / GCS (for documents)
- **Secret Management**: AWS Secrets Manager / Vault

### 4.3 Network Architecture

**Production Network Layout:**
```
Internet
    |
    ▼
[WAF - Web Application Firewall]
    |
    ▼
[Load Balancer / API Gateway]
    |
    ├─────────────────┬─────────────────┐
    ▼                 ▼                 ▼
[Frontend Tier]  [Backend Tier]   [Data Tier]
 Public Subnet    Private Subnet   Private Subnet
    │                 │                 │
    │                 ├─ MongoDB        │
    │                 ├─ Neo4j          │
    │                 └─ Redis          │
    │                                   │
    └───────────[NAT Gateway]───────────┘
                     │
                     ▼
              [External APIs]
              (LLM Services)
```

## 5. Security Architecture

### 5.1 Authentication Flow

```
1. User Login (POST /api/auth/login)
   ↓
2. Validate Credentials (bcrypt compare)
   ↓
3. Generate JWT Token (15 min expiry)
   ↓
4. Generate Refresh Token (7 days expiry)
   ↓
5. Return Tokens to Client
   ↓
6. Client stores tokens (httpOnly cookies)
   ↓
7. Every request includes JWT in Authorization header
   ↓
8. Backend validates JWT (signature, expiry)
   ↓
9. Extract user_id and role from JWT
   ↓
10. Apply RBAC (Role-Based Access Control)
```

### 5.2 Data Security Layers

**Layer 1: Network Security**
- HTTPS/TLS 1.3 encryption
- Firewall rules (restrict ports)
- VPC isolation
- DDoS protection

**Layer 2: Application Security**
- JWT authentication
- RBAC authorization
- Input validation (Pydantic)
- SQL injection prevention
- XSS protection
- CSRF tokens

**Layer 3: Data Security**
- Encryption at rest (MongoDB encryption)
- Encryption in transit (TLS)
- Sensitive field encryption (PHI/PII)
- Database access controls

**Layer 4: Audit & Compliance**
- Comprehensive audit logging
- Access logs with IP tracking
- Data retention policies
- PDPA/HIPAA compliance

### 5.3 Secrets Management

**Development:**
- `.env` files (not committed to git)
- Environment variables

**Production:**
- AWS Secrets Manager / HashiCorp Vault
- Kubernetes Secrets
- Rotate secrets regularly

## 6. Scalability Strategy

### 6.1 Horizontal Scaling

**Frontend:**
- Stateless React app
- Multiple replicas behind load balancer
- CDN for static assets

**Backend:**
- Stateless FastAPI services
- Horizontal pod autoscaling (HPA)
- Scale based on CPU/memory/request rate

**Database:**
- MongoDB replica set (read replicas)
- Sharding for large datasets
- Neo4j clustering

### 6.2 Caching Strategy

**Levels:**
1. **Browser Cache**: Static assets
2. **CDN Cache**: Images, CSS, JS
3. **API Cache (Redis)**: Frequent queries
4. **Database Cache**: MongoDB query cache

**Cache Invalidation:**
- Time-based expiry (TTL)
- Event-based invalidation
- Manual cache clearing

### 6.3 Performance Optimization

**Frontend:**
- Code splitting (React lazy loading)
- Image optimization (WebP format)
- Minification and compression
- Service Worker (future PWA)

**Backend:**
- Database query optimization
- Connection pooling
- Async/await operations
- Background tasks (Celery)

**Database:**
- Proper indexing
- Query optimization
- Aggregation pipelines
- Read preferences

## 7. Disaster Recovery & Business Continuity

### 7.1 Backup Strategy

**MongoDB:**
- Daily full backups
- Hourly incremental backups
- Retention: 30 days
- Cross-region replication

**Neo4j:**
- Daily backups
- Retention: 30 days

**Application Code:**
- Git version control
- CI/CD pipelines

### 7.2 High Availability

**Target SLA:** 99.9% uptime (8.76 hours downtime/year)

**Strategies:**
- Multi-zone deployment
- Database replica sets
- Load balancer health checks
- Auto-restart on failure

### 7.3 Disaster Recovery Plan

**RTO (Recovery Time Objective):** 4 hours
**RPO (Recovery Point Objective):** 1 hour

**Steps:**
1. Detect failure (monitoring alerts)
2. Assess impact
3. Failover to backup systems
4. Restore from backups
5. Verify data integrity
6. Resume operations

## 8. Monitoring & Observability

### 8.1 Logging

**Current:**
- Python logging module
- FastAPI request logging
- Supervisor logs

**Future:**
- ELK Stack (Elasticsearch, Logstash, Kibana)
- Structured logging (JSON format)
- Log aggregation

### 8.2 Monitoring

**Metrics to Track:**
- API response times
- Error rates
- Database query performance
- System resources (CPU, memory, disk)
- User activity

**Tools (Future):**
- Prometheus (metrics collection)
- Grafana (dashboards)
- Sentry (error tracking)

### 8.3 Alerting

**Alert Triggers:**
- API error rate > 5%
- Response time > 2 seconds
- Database connection failures
- Disk space > 80%
- Security incidents

**Channels:**
- Email
- Slack
- PagerDuty (on-call rotation)

## 9. CI/CD Pipeline

### 9.1 Development Workflow

```
1. Developer commits code to feature branch
   ↓
2. GitHub Actions triggered
   ↓
3. Run linters (ESLint, Black, isort)
   ↓
4. Run unit tests (Jest, pytest)
   ↓
5. Build Docker images
   ↓
6. Push to staging environment
   ↓
7. Run E2E tests (Playwright)
   ↓
8. Code review and approval
   ↓
9. Merge to main branch
   ↓
10. Deploy to production (blue-green deployment)
```

### 9.2 Deployment Strategy

**Blue-Green Deployment:**
- Maintain two production environments
- Deploy to inactive environment
- Test thoroughly
- Switch traffic to new environment
- Keep old environment for quick rollback

## 10. Technology Evolution Path

### Current State (Phase 1)
- Modular monolith
- MongoDB + Neo4j
- Basic deployment

### Future State (Phase 2)
- Microservices architecture
- Event-driven communication
- Advanced caching (Redis)
- Kubernetes orchestration
- Comprehensive monitoring

### Future State (Phase 3)
- Multi-region deployment
- Edge computing
- Real-time analytics
- Advanced AI/ML models

---
*Document Version: 1.0*
*Last Updated: June 2026*