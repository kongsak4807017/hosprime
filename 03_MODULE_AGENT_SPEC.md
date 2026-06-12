# HosPRIME - Module & AI Agent Specifications

## 1. System Architecture Overview

HosPRIME follows a **modular architecture** with integrated **AI Agent** capabilities across all modules.

### 1.1 Architecture Pattern
- **Modular Monolith** - Organized by domain modules
- **Service Layer Pattern** - Business logic separation
- **Repository Pattern** - Data access abstraction
- **AI Agent Layer** - Intelligent automation and assistance

## 2. Core Modules Specification

### Module 1: Patient Management System

**Module ID:** `patient_management`

**Responsibilities:**
- Complete patient lifecycle management
- Electronic Health Records (EHR) maintenance
- Patient demographics and contact information
- Medical history tracking
- Document management

**API Endpoints:**
```
POST   /api/patients                    # Create new patient
GET    /api/patients                    # List all patients (paginated)
GET    /api/patients/{id}               # Get patient details
PUT    /api/patients/{id}               # Update patient
DELETE /api/patients/{id}               # Soft delete patient
GET    /api/patients/{id}/history       # Get medical history
POST   /api/patients/{id}/documents     # Upload document
GET    /api/patients/{id}/documents     # Get patient documents
GET    /api/patients/search             # Advanced search
```

**Data Model:**
```python
Patient:
  - id: UUID
  - patient_number: String (auto-generated)
  - first_name: String
  - last_name: String
  - date_of_birth: Date
  - gender: Enum (Male, Female, Other)
  - blood_type: Enum (A+, A-, B+, B-, O+, O-, AB+, AB-)
  - phone: String
  - email: String
  - address: Object {street, city, state, zip, country}
  - emergency_contact: Object {name, relationship, phone}
  - insurance_info: Object {provider, policy_number, group_number}
  - allergies: Array[String]
  - chronic_conditions: Array[String]
  - current_medications: Array[String]
  - medical_history: Array[MedicalHistory]
  - created_at: DateTime
  - updated_at: DateTime
  - is_active: Boolean
```

**AI Agent Features:**
- **Patient Risk Scoring**: ML model predicts patient risk levels
- **History Summarization**: LLM generates concise medical history summaries
- **Smart Search**: Semantic search for patient records
- **Data Validation**: AI-powered data quality checks

---

### Module 2: Appointment Scheduling System

**Module ID:** `appointment_scheduling`

**Responsibilities:**
- Appointment booking and management
- Calendar management for providers
- Waitlist management
- Appointment reminders
- Resource allocation

**API Endpoints:**
```
POST   /api/appointments                # Book appointment
GET    /api/appointments                # List appointments
GET    /api/appointments/{id}           # Get appointment details
PUT    /api/appointments/{id}           # Update appointment
DELETE /api/appointments/{id}           # Cancel appointment
POST   /api/appointments/{id}/checkin   # Check-in patient
GET    /api/appointments/calendar       # Get calendar view
GET    /api/appointments/available-slots # Get available time slots
POST   /api/appointments/waitlist       # Add to waitlist
```

**Data Model:**
```python
Appointment:
  - id: UUID
  - appointment_number: String
  - patient_id: UUID (ref: Patient)
  - doctor_id: UUID (ref: Staff)
  - department: String
  - appointment_date: Date
  - appointment_time: Time
  - duration_minutes: Integer
  - reason: String
  - notes: Text
  - status: Enum (Scheduled, CheckedIn, InProgress, Completed, Cancelled, NoShow)
  - room_number: String
  - reminder_sent: Boolean
  - created_at: DateTime
  - updated_at: DateTime
```

**AI Agent Features:**
- **Smart Scheduling**: Optimal slot recommendations based on doctor availability
- **No-Show Prediction**: ML model predicts likelihood of no-show
- **Chatbot Booking**: Natural language appointment booking via AI chatbot
- **Demand Forecasting**: Predict appointment demand patterns

---

### Module 3: Staff Management System

**Module ID:** `staff_management`

**Responsibilities:**
- Healthcare professional profiles
- Shift and schedule management
- Credentials tracking
- Performance monitoring

**API Endpoints:**
```
POST   /api/staff                       # Add staff member
GET    /api/staff                       # List all staff
GET    /api/staff/{id}                  # Get staff details
PUT    /api/staff/{id}                  # Update staff
DELETE /api/staff/{id}                  # Remove staff
GET    /api/staff/doctors               # List doctors
GET    /api/staff/nurses                # List nurses
GET    /api/staff/{id}/schedule         # Get staff schedule
POST   /api/staff/{id}/leave            # Request leave
```

**Data Model:**
```python
Staff:
  - id: UUID
  - staff_number: String
  - first_name: String
  - last_name: String
  - role: Enum (Doctor, Nurse, Pharmacist, LabTech, Admin, Finance)
  - specialization: String (for doctors)
  - department: String
  - license_number: String
  - license_expiry: Date
  - phone: String
  - email: String
  - schedule: Object {work_days, work_hours}
  - is_available: Boolean
  - created_at: DateTime
  - updated_at: DateTime
```

**AI Agent Features:**
- **Workload Balancing**: AI recommends optimal staff allocation
- **Shift Optimization**: ML-based shift scheduling
- **Credential Monitoring**: Automated alerts for expiring licenses

---

### Module 4: Pharmacy Management System

**Module ID:** `pharmacy_management`

**Responsibilities:**
- Drug inventory management
- Prescription processing
- Dispensation tracking
- Reorder management

**API Endpoints:**
```
POST   /api/pharmacy/drugs              # Add drug to inventory
GET    /api/pharmacy/drugs              # List inventory
PUT    /api/pharmacy/drugs/{id}         # Update drug info
POST   /api/pharmacy/prescriptions      # Create prescription
GET    /api/pharmacy/prescriptions/{id} # Get prescription
POST   /api/pharmacy/dispense           # Dispense medication
GET    /api/pharmacy/low-stock          # Get low stock items
POST   /api/pharmacy/check-interaction  # Check drug interactions
```

**Data Model:**
```python
Drug:
  - id: UUID
  - drug_code: String
  - name: String
  - generic_name: String
  - manufacturer: String
  - dosage_form: String
  - strength: String
  - quantity_in_stock: Integer
  - reorder_level: Integer
  - unit_price: Decimal
  - expiry_date: Date
  - storage_conditions: String

Prescription:
  - id: UUID
  - prescription_number: String
  - patient_id: UUID
  - doctor_id: UUID
  - drug_id: UUID
  - dosage: String
  - frequency: String
  - duration_days: Integer
  - quantity: Integer
  - instructions: Text
  - status: Enum (Pending, Dispensed, Completed)
  - created_at: DateTime
  - dispensed_at: DateTime
```

**AI Agent Features:**
- **Drug Interaction Checker**: AI analyzes potential drug interactions
- **Inventory Optimization**: ML predicts reorder quantities and timing
- **Prescription Error Detection**: AI flags potential prescription errors
- **Dosage Validation**: Intelligent dosage calculation verification

---

### Module 5: Laboratory Management System

**Module ID:** `laboratory_management`

**Responsibilities:**
- Test ordering and tracking
- Sample management
- Result entry and validation
- Report generation

**API Endpoints:**
```
POST   /api/lab/tests                   # Order lab test
GET    /api/lab/tests                   # List all tests
GET    /api/lab/tests/{id}              # Get test details
PUT    /api/lab/tests/{id}/results      # Enter test results
GET    /api/lab/tests/{id}/report       # Generate report
GET    /api/lab/tests/patient/{id}      # Get patient's tests
POST   /api/lab/tests/{id}/validate     # Validate results
```

**Data Model:**
```python
LabTest:
  - id: UUID
  - test_number: String
  - patient_id: UUID
  - doctor_id: UUID
  - test_type: String
  - test_category: Enum (Blood, Urine, Imaging, Pathology)
  - sample_id: String
  - ordered_at: DateTime
  - sample_collected_at: DateTime
  - results_entered_at: DateTime
  - status: Enum (Ordered, SampleCollected, InProgress, Completed, Validated)
  - results: Object {parameters: [{name, value, unit, reference_range, is_abnormal}]}
  - notes: Text
  - validated_by: UUID (staff_id)
  - report_url: String
```

**AI Agent Features:**
- **Abnormal Result Detection**: AI flags unusual test results
- **Report Summarization**: LLM generates natural language summaries
- **Pattern Recognition**: ML identifies trends in test results
- **Predictive Diagnostics**: AI suggests potential diagnoses based on results

---

### Module 6: Billing & Finance System

**Module ID:** `billing_finance`

**Responsibilities:**
- Invoice generation
- Payment processing
- Insurance claims
- Financial reporting

**API Endpoints:**
```
POST   /api/billing/invoices            # Create invoice
GET    /api/billing/invoices/{id}       # Get invoice
POST   /api/billing/payments            # Record payment
GET    /api/billing/invoices/patient/{id} # Get patient invoices
GET    /api/billing/reports/revenue     # Revenue reports
POST   /api/billing/claims              # Submit insurance claim
GET    /api/billing/outstanding         # Outstanding payments
```

**Data Model:**
```python
Invoice:
  - id: UUID
  - invoice_number: String
  - patient_id: UUID
  - invoice_date: Date
  - due_date: Date
  - items: Array[{description, quantity, unit_price, total}]
  - subtotal: Decimal
  - tax: Decimal
  - discount: Decimal
  - total_amount: Decimal
  - paid_amount: Decimal
  - status: Enum (Pending, PartiallyPaid, Paid, Overdue, Cancelled)
  - payment_method: String
  - insurance_claim_id: UUID
```

**AI Agent Features:**
- **Revenue Prediction**: ML forecasts revenue trends
- **Payment Default Risk**: AI predicts payment likelihood
- **Claim Denial Prediction**: AI flags claims likely to be denied
- **Billing Error Detection**: Automated invoice validation

---

### Module 7: Bed & Room Management

**Module ID:** `bed_room_management`

**Responsibilities:**
- Real-time bed availability
- Admission, transfer, discharge (ATD)
- Occupancy tracking
- Housekeeping coordination

**API Endpoints:**
```
GET    /api/beds                        # List all beds/rooms
GET    /api/beds/available              # Available beds
POST   /api/beds/{id}/admit             # Admit patient to bed
POST   /api/beds/{id}/transfer          # Transfer patient
POST   /api/beds/{id}/discharge         # Discharge patient
GET    /api/beds/occupancy              # Occupancy statistics
PUT    /api/beds/{id}/status            # Update bed status
```

**Data Model:**
```python
Bed:
  - id: UUID
  - bed_number: String
  - room_number: String
  - ward: String
  - floor: Integer
  - bed_type: Enum (ICU, General, Private, Maternity)
  - status: Enum (Available, Occupied, Maintenance, Reserved)
  - current_patient_id: UUID
  - admitted_at: DateTime
  - expected_discharge: Date
  - housekeeping_status: Enum (Clean, InProgress, NeedsCleaning)
```

**AI Agent Features:**
- **Bed Demand Forecasting**: Predict bed requirements
- **Optimal Allocation**: AI recommends best bed for patient needs
- **Discharge Prediction**: ML estimates discharge dates
- **Capacity Planning**: AI-driven capacity management

---

### Module 8: Analytics & Reporting Dashboard

**Module ID:** `analytics_reporting`

**Responsibilities:**
- Executive dashboards
- KPI monitoring
- Custom reports
- Data visualization

**API Endpoints:**
```
GET    /api/analytics/dashboard         # Main dashboard data
GET    /api/analytics/kpis              # Key performance indicators
GET    /api/analytics/patients/stats    # Patient statistics
GET    /api/analytics/revenue           # Financial analytics
GET    /api/analytics/operations        # Operational metrics
POST   /api/analytics/reports/custom    # Generate custom report
```

**AI Agent Features:**
- **Predictive Analytics**: Forecast trends and patterns
- **Anomaly Detection**: Identify unusual patterns
- **Automated Insights**: AI-generated insights and recommendations
- **Natural Language Queries**: Ask questions in natural language

---

## 3. AI Agent Architecture

### 3.1 Medical AI Assistant Agent

**Agent ID:** `medical_ai_assistant`

**Capabilities:**
1. **Patient Chatbot**
   - Answer general medical queries
   - Symptom checking
   - Appointment booking assistance
   - Navigation help

2. **Clinical Decision Support**
   - Diagnosis assistance for doctors
   - Treatment recommendations
   - Clinical guideline lookup
   - Medical literature search

3. **Administrative Assistant**
   - Report generation
   - Data summarization
   - Task automation
   - Alert generation

**LLM Integration:**
```python
Agent Configuration:
  - Primary Model: GPT-5.2 (complex reasoning)
  - Secondary Model: Claude Sonnet 4.5 (medical knowledge)
  - Quick Queries: Gemini 3 Flash (fast responses)
  - Knowledge Base: Neo4j Medical Graph
```

**API Endpoints:**
```
POST   /api/ai/chat                     # Chat with AI assistant
POST   /api/ai/diagnose                 # Diagnosis assistance
POST   /api/ai/drug-interaction         # Check drug interactions
POST   /api/ai/summarize                # Summarize medical text
POST   /api/ai/search-knowledge         # Query medical knowledge graph
```

### 3.2 Predictive Analytics Agent

**Agent ID:** `predictive_analytics_agent`

**ML Models:**
1. **No-Show Prediction Model**
   - Features: Patient history, appointment time, weather, etc.
   - Algorithm: Gradient Boosting
   - Accuracy Target: 85%+

2. **Bed Demand Forecasting Model**
   - Features: Historical occupancy, seasonality, events
   - Algorithm: Time series forecasting (LSTM)
   - Accuracy Target: 90%+

3. **Patient Risk Stratification**
   - Features: Age, conditions, vitals, history
   - Algorithm: Random Forest
   - Output: Low/Medium/High risk scores

4. **Revenue Prediction Model**
   - Features: Historical revenue, seasonality, trends
   - Algorithm: Prophet (Facebook)
   - Accuracy Target: 85%+

### 3.3 Medical Knowledge Graph Agent

**Agent ID:** `knowledge_graph_agent`

**Graph Schema (Neo4j):**
```
Nodes:
  - Disease (name, icd_code, description)
  - Symptom (name, severity)
  - Treatment (name, type, efficacy)
  - Drug (name, category, side_effects)
  - Patient (patient_id)

Relationships:
  - Disease -[HAS_SYMPTOM]-> Symptom
  - Disease -[TREATED_BY]-> Treatment
  - Treatment -[USES_DRUG]-> Drug
  - Drug -[INTERACTS_WITH]-> Drug
  - Patient -[DIAGNOSED_WITH]-> Disease
  - Patient -[PRESCRIBED]-> Drug
```

**Capabilities:**
- Disease-symptom relationship queries
- Drug interaction pathfinding
- Treatment efficacy analysis
- Patient similarity matching
- Clinical pathway recommendations

## 4. Integration Specifications

### 4.1 Inter-Module Communication
- **Synchronous**: REST API calls
- **Asynchronous**: Event-driven (future: message queue)

### 4.2 Data Consistency
- MongoDB transactions for multi-collection operations
- Audit logging for all data changes
- Soft deletes for critical data

### 4.3 Authentication Flow
```
1. User login -> JWT token issued
2. Token includes: user_id, role, permissions
3. Every API request validates token
4. Role-based access control enforced
5. Audit log records all actions
```

## 5. Module Dependencies

```
Patient Management <- Appointment Scheduling
Patient Management <- Laboratory Management
Patient Management <- Pharmacy Management
Patient Management <- Billing & Finance
Staff Management <- Appointment Scheduling
Pharmacy Management -> Billing & Finance
Laboratory Management -> Billing & Finance
All Modules -> Analytics & Reporting
All Modules -> AI Medical Assistant
```

## 6. Performance Requirements

### 6.1 Response Times
- API endpoints: < 500ms (95th percentile)
- AI chat responses: < 3 seconds
- Report generation: < 10 seconds
- Dashboard load: < 2 seconds

### 6.2 Scalability
- Support 1000+ concurrent users
- Handle 10,000+ patients
- Process 500+ appointments/day
- Store 1M+ lab results

## 7. Security Specifications

### 7.1 Data Access Rules
- **Doctors**: Full access to their patients
- **Nurses**: Read access to assigned patients
- **Pharmacists**: Access to prescriptions only
- **Lab Techs**: Access to lab orders only
- **Finance**: Access to billing only
- **Patients**: Access to own records only
- **Admins**: Full system access

### 7.2 Audit Requirements
- Log all data access and modifications
- Include: user_id, action, timestamp, IP address
- Retention: 7 years (compliance)

---
*Document Version: 1.0*
*Last Updated: June 2026*