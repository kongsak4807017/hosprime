# HosPRIME - Technology Stack Specification

## 1. Architecture Overview

**Architecture Style:** Microservices-Ready Monolith (Modular Monolith)

**Deployment Model:** Cloud-Native, Container-Based

**Design Principles:**
- Separation of Concerns
- Domain-Driven Design (DDD)
- API-First Development
- Security by Design
- Scalability and Performance

## 2. Frontend Stack

### 2.1 Core Framework
- **React 19.0.0** - Latest version with concurrent features
- **JavaScript (ES2022+)** - Modern JavaScript features

### 2.2 UI Component Libraries
- **Radix UI** - Accessible, unstyled component primitives
  - Dialogs, Dropdowns, Tooltips, Accordions, Tabs
  - Form components (Select, Checkbox, Radio, Switch)
- **Lucide React** - Icon library (512+ icons)
- **Shadcn/ui patterns** - Pre-built component patterns

### 2.3 Styling & Design
- **Tailwind CSS 3.4.17** - Utility-first CSS framework
- **PostCSS 8.4.49** - CSS processing
- **tailwindcss-animate** - Animation utilities
- **class-variance-authority (CVA)** - Type-safe variant styling
- **clsx & tailwind-merge** - Conditional class management

### 2.4 State Management & Data Fetching
- **TanStack Query (React Query) 5.56.2** - Server state management
- **SWR 2.3.8** - Stale-while-revalidate data fetching
- **React Hook Form 7.56.2** - Form state management
- **Zod 3.24.4** - Schema validation

### 2.5 Routing & Navigation
- **React Router DOM 7.5.1** - Client-side routing

### 2.6 Data Visualization
- **Recharts 3.6.0** - Chart library for analytics dashboard

### 2.7 Animation & Motion
- **Framer Motion 11.18.0** - Animation library

### 2.8 HTTP Client
- **Axios 1.8.4** - Promise-based HTTP client

### 2.9 Utilities
- **date-fns 4.1.0** - Date manipulation
- **dayjs 1.11.13** - Date parsing and formatting
- **lodash 4.18.1** - Utility functions

### 2.10 Build Tools
- **CRACO 7.1.0** - Create React App Configuration Override
- **Webpack** (via React Scripts)

## 3. Backend Stack

### 3.1 Core Framework
- **FastAPI 0.110.1** - Modern Python web framework
  - Fast performance (based on Starlette)
  - Automatic OpenAPI documentation
  - Type hints and validation (Pydantic)
  - Async/await support

### 3.2 ASGI Server
- **Uvicorn 0.25.0** - Lightning-fast ASGI server

### 3.3 Data Validation
- **Pydantic 2.6.4** - Data validation using Python type hints

### 3.4 Authentication & Security
- **PyJWT 2.10.1** - JSON Web Token implementation
- **python-jose 3.3.0** - JOSE implementation (JWS, JWE, JWK)
- **bcrypt 4.1.3** - Password hashing
- **passlib 1.7.4** - Password hashing library
- **cryptography 42.0.8** - Cryptographic recipes

### 3.5 Database Drivers
- **Motor 3.3.1** - Async MongoDB driver
- **PyMongo 4.5.0** - MongoDB driver
- **Neo4j Python Driver 5.x** (to be added) - Graph database driver

### 3.6 HTTP & External APIs
- **Requests 2.31.0** - HTTP library
- **requests-oauthlib 2.0.0** - OAuth support

### 3.7 File Processing
- **python-multipart 0.0.9** - Multipart form data parsing

### 3.8 Data Processing
- **Pandas 2.2.0** - Data analysis and manipulation
- **NumPy 1.26.0** - Numerical computing

### 3.9 AI/ML Integration
- **emergentintegrations 0.2.0** - Unified LLM integration library
  - OpenAI GPT-5.2
  - Anthropic Claude Sonnet 4.5
  - Google Gemini 3 Flash
- **LangChain** (to be added) - LLM application framework
- **scikit-learn** (to be added) - Machine learning library

### 3.10 Task Queue & Background Jobs
- **Celery** (to be added) - Distributed task queue
- **Redis** (to be added) - Message broker

### 3.11 Utilities
- **python-dotenv 1.0.1** - Environment variable management
- **typer 0.9.0** - CLI application builder
- **jq 1.6.0** - JSON processing

### 3.12 Development Tools
- **pytest 8.0.0** - Testing framework
- **black 24.1.1** - Code formatter
- **isort 5.13.2** - Import sorter
- **flake8 7.0.0** - Linting
- **mypy 1.8.0** - Static type checker

## 4. Database Stack

### 4.1 Primary Database
**MongoDB 5.x/6.x**
- Document-oriented NoSQL database
- Flexible schema for healthcare data
- Horizontal scalability
- Rich query capabilities
- ACID transactions support

**Collections:**
- `patients` - Patient records and EHR
- `appointments` - Appointment schedules
- `staff` - Healthcare staff information
- `prescriptions` - Prescription records
- `lab_tests` - Laboratory tests and results
- `pharmacy_inventory` - Drug inventory
- `billing` - Invoices and payments
- `beds_rooms` - Bed and room management
- `audit_logs` - System audit trail

### 4.2 Graph Database
**Neo4j 5.x**
- Graph database for medical knowledge representation
- Relationship-heavy data modeling
- Complex query patterns (Cypher)

**Use Cases:**
- Medical knowledge graph (diseases, symptoms, treatments)
- Drug interaction network
- Patient relationship mapping
- Clinical pathway modeling
- Diagnosis reasoning chains

### 4.3 Caching Layer
**Redis 7.x** (to be added)
- In-memory data structure store
- Session management
- Real-time data caching
- Message broker for Celery

## 5. AI/ML Stack

### 5.1 Large Language Models (LLMs)
**Provider:** Emergent Universal Key Integration

**Models:**
1. **OpenAI GPT-5.2**
   - Primary LLM for complex medical reasoning
   - Medical report generation
   - Clinical decision support

2. **Anthropic Claude Sonnet 4.5**
   - Medical diagnosis assistance
   - Treatment recommendation
   - Drug interaction analysis

3. **Google Gemini 3 Flash**
   - Quick patient queries
   - Chatbot responses
   - Symptom checking

### 5.2 ML Frameworks
- **scikit-learn** - Classical ML algorithms
  - Predictive models (bed occupancy, no-show prediction)
  - Patient risk stratification
- **TensorFlow/PyTorch** (future) - Deep learning models

### 5.3 NLP Processing
- **spaCy** (to be added) - Medical NER (Named Entity Recognition)
- **Medical NLP models** - Clinical text processing

### 5.4 Knowledge Graph Processing
- **Neo4j Graph Data Science Library**
  - Graph algorithms
  - Similarity searches
  - Path finding

## 6. DevOps & Infrastructure

### 6.1 Containerization
- **Docker** - Container platform
- **Docker Compose** - Multi-container orchestration

### 6.2 Process Management
- **Supervisord** - Process control system
  - Backend service management
  - Frontend development server

### 6.3 Web Server
- **Nginx** (production) - Reverse proxy and static file serving

### 6.4 CI/CD
- **GitHub Actions** - Automated testing and deployment
- **Git** - Version control

### 6.5 Monitoring & Logging
- **Python logging** - Application logging
- **FastAPI built-in logging**
- **Future:** Sentry for error tracking

## 7. Security Stack

### 7.1 Authentication
- JWT (JSON Web Tokens) - Stateless authentication
- Refresh token rotation
- Multi-factor authentication (MFA) ready

### 7.2 Authorization
- Role-Based Access Control (RBAC)
- Permission-based access
- Resource-level authorization

### 7.3 Data Security
- HTTPS/TLS encryption
- Password hashing (bcrypt)
- Data encryption at rest
- SQL injection prevention (NoSQL)
- XSS protection
- CSRF protection

### 7.4 Compliance
- PDPA (Personal Data Protection Act) compliance
- HIPAA-ready architecture
- Audit logging for all data access

## 8. API Architecture

### 8.1 API Design
- RESTful API principles
- JSON request/response format
- API versioning (/api/v1/)
- Consistent error handling

### 8.2 API Documentation
- **FastAPI automatic OpenAPI/Swagger** - Interactive API docs
- **ReDoc** - Alternative API documentation

### 8.3 API Security
- JWT Bearer token authentication
- Rate limiting
- CORS configuration

## 9. Testing Stack

### 9.1 Backend Testing
- **pytest** - Unit and integration tests
- **pytest-asyncio** - Async test support
- **httpx** - Async HTTP client for testing

### 9.2 Frontend Testing
- **React Testing Library** - Component testing
- **Jest** - Test runner (via React Scripts)

### 9.3 E2E Testing
- **Playwright** (to be added) - End-to-end testing

## 10. Development Tools

### 10.1 Code Quality
- **ESLint** - JavaScript linting
- **Prettier** - Code formatting
- **Black** - Python code formatting
- **isort** - Python import sorting

### 10.2 Type Safety
- **TypeScript** (future migration)
- **mypy** - Python static type checking
- **Pydantic** - Runtime type validation

### 10.3 IDE Support
- VS Code recommended
- IntelliJ IDEA / PyCharm compatible

## 11. Deployment Architecture

### 11.1 Development Environment
- Local development with hot reload
- Docker Compose for service orchestration
- Environment-based configuration

### 11.2 Production Environment (Future)
- **Kubernetes** - Container orchestration
- **AWS/GCP/Azure** - Cloud platform
- **Load balancing** - High availability
- **Auto-scaling** - Dynamic resource allocation

## 12. Data Flow Architecture

```
┌─────────────┐
│   Browser   │
└──────┬──────┘
       │ HTTPS
       ▼
┌─────────────────────┐
│   React Frontend    │
│   (Port 3000)       │
└──────┬──────────────┘
       │ REST API
       ▼
┌─────────────────────┐
│  FastAPI Backend    │
│   (Port 8001)       │
└──┬──────────┬───────┘
   │          │
   │          └─────────┐
   ▼                    ▼
┌──────────┐    ┌──────────────┐
│ MongoDB  │    │  Neo4j Graph │
└──────────┘    └──────────────┘
       │                 │
       └────────┬────────┘
                ▼
       ┌─────────────────┐
       │  LLM Services   │
       │ (Emergent Key)  │
       └─────────────────┘
```

## 13. Technology Decision Rationale

### 13.1 Why React?
- Large ecosystem and community
- Component reusability
- Performance with virtual DOM
- Rich UI library support (Radix UI)

### 13.2 Why FastAPI?
- High performance (async/await)
- Automatic API documentation
- Type safety with Pydantic
- Modern Python framework

### 13.3 Why MongoDB?
- Flexible schema for diverse healthcare data
- Horizontal scalability
- Rich query capabilities
- JSON-like documents

### 13.4 Why Neo4j?
- Optimal for relationship-heavy medical knowledge
- Graph queries for complex connections
- Drug interaction networks
- Clinical pathway modeling

### 13.5 Why Emergent Universal Key?
- Single key for multiple LLM providers
- Cost-effective
- Easy switching between models
- Unified API

## 14. Future Technology Considerations

### 14.1 Planned Additions
- **TypeScript migration** - Type safety in frontend
- **GraphQL API** - Alternative to REST for complex queries
- **WebSocket support** - Real-time notifications
- **Redis caching** - Performance optimization
- **Elasticsearch** - Full-text search capabilities
- **MinIO/S3** - Document and image storage
- **RabbitMQ/Kafka** - Event streaming

### 14.2 Scalability Enhancements
- Microservices decomposition
- Service mesh (Istio)
- Database sharding
- Read replicas

---
*Document Version: 1.0*
*Last Updated: June 2026*