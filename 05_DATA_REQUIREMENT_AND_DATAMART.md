# HosPRIME - Data Requirements & Data Mart Specification

## 1. Overview

This document defines the comprehensive data requirements, data models, data warehouse, and analytical data mart specifications for HosPRIME.

## 2. Core Data Entities

### 2.1 Patient Data

**Entity:** Patient

**Purpose:** Central repository for all patient information

**Attributes:**
```json
{
  "id": "UUID (Primary Key)",
  "patient_number": "String (Unique, Auto-generated: PAT-XXXXXX)",
  "personal_info": {
    "first_name": "String (Required)",
    "middle_name": "String (Optional)",
    "last_name": "String (Required)",
    "date_of_birth": "Date (Required)",
    "age": "Integer (Calculated)",
    "gender": "Enum: [Male, Female, Other]",
    "national_id": "String (Unique)",
    "blood_type": "Enum: [A+, A-, B+, B-, O+, O-, AB+, AB-]",
    "marital_status": "Enum: [Single, Married, Divorced, Widowed]",
    "occupation": "String",
    "nationality": "String"
  },
  "contact_info": {
    "phone_primary": "String (Required)",
    "phone_secondary": "String",
    "email": "String",
    "address": {
      "street": "String",
      "city": "String",
      "state": "String",
      "postal_code": "String",
      "country": "String"
    }
  },
  "emergency_contact": {
    "name": "String",
    "relationship": "String",
    "phone": "String"
  },
  "insurance_info": {
    "provider": "String",
    "policy_number": "String",
    "group_number": "String",
    "coverage_type": "String",
    "expiry_date": "Date"
  },
  "medical_profile": {
    "allergies": "Array[{allergen, severity, reaction}]",
    "chronic_conditions": "Array[{condition, diagnosed_date, status}]",
    "current_medications": "Array[{drug_name, dosage, frequency, start_date}]",
    "past_surgeries": "Array[{procedure, date, hospital}]",
    "family_history": "Array[{relation, condition}]",
    "lifestyle": {
      "smoking": "Enum: [Never, Former, Current]",
      "alcohol": "Enum: [Never, Occasionally, Regularly]",
      "exercise": "String"
    }
  },
  "vitals_history": "Array[VitalSigns]",
  "risk_score": "Float (0-100, AI-calculated)",
  "created_at": "DateTime",
  "updated_at": "DateTime",
  "created_by": "UUID (staff_id)",
  "is_active": "Boolean",
  "is_deceased": "Boolean",
  "deceased_date": "Date"
}
```

**Data Volume:** 10,000 - 100,000+ patients

**Retention:** Permanent (legal requirement)

---

### 2.2 Appointment Data

**Entity:** Appointment

**Purpose:** Manage all patient appointments and scheduling

**Attributes:**
```json
{
  "id": "UUID",
  "appointment_number": "String (APT-XXXXXX)",
  "patient_id": "UUID (FK: Patient)",
  "doctor_id": "UUID (FK: Staff)",
  "department": "String",
  "specialty": "String",
  "appointment_type": "Enum: [Consultation, Follow-up, Emergency, Procedure]",
  "appointment_date": "Date",
  "appointment_time": "Time",
  "duration_minutes": "Integer (default: 30)",
  "reason_for_visit": "Text",
  "symptoms": "Array[String]",
  "status": "Enum: [Scheduled, Confirmed, CheckedIn, InProgress, Completed, Cancelled, NoShow, Rescheduled]",
  "priority": "Enum: [Normal, Urgent, Emergency]",
  "room_number": "String",
  "notes": "Text",
  "reminder_sent": "Boolean",
  "reminder_sent_at": "DateTime",
  "checked_in_at": "DateTime",
  "completed_at": "DateTime",
  "no_show_prediction": "Float (0-1)",
  "created_at": "DateTime",
  "created_by": "UUID",
  "cancelled_at": "DateTime",
  "cancellation_reason": "Text"
}
```

**Data Volume:** 500-2,000 appointments/day

**Retention:** 5 years

---

### 2.3 Staff Data

**Entity:** Staff

**Purpose:** Healthcare professional and administrative staff information

**Attributes:**
```json
{
  "id": "UUID",
  "staff_number": "String (STF-XXXXXX)",
  "personal_info": {
    "first_name": "String",
    "last_name": "String",
    "date_of_birth": "Date",
    "gender": "Enum",
    "phone": "String",
    "email": "String"
  },
  "professional_info": {
    "role": "Enum: [Doctor, Nurse, Pharmacist, LabTechnician, Radiologist, Admin, Finance, Reception]",
    "department": "String",
    "specialization": "String (for doctors)",
    "qualification": "Array[{degree, institution, year}]",
    "license_number": "String",
    "license_expiry": "Date",
    "certifications": "Array[{name, issued_by, date}]",
    "years_of_experience": "Integer",
    "languages_spoken": "Array[String]"
  },
  "employment_info": {
    "hire_date": "Date",
    "employee_type": "Enum: [FullTime, PartTime, Contract]",
    "salary": "Decimal (encrypted)",
    "shift": "String",
    "work_schedule": {
      "monday": "Array[{start_time, end_time}]",
      "tuesday": "Array[{start_time, end_time}]",
      "...": "..."
    }
  },
  "availability": {
    "is_available": "Boolean",
    "current_status": "Enum: [Available, Busy, OnLeave, OffDuty]",
    "leave_requests": "Array[{start_date, end_date, reason, status}]"
  },
  "performance_metrics": {
    "patient_satisfaction_score": "Float",
    "average_appointment_duration": "Float",
    "total_patients_treated": "Integer"
  },
  "created_at": "DateTime",
  "updated_at": "DateTime",
  "is_active": "Boolean"
}
```

**Data Volume:** 50-500 staff members

**Retention:** 7 years after termination

---

### 2.4 Prescription & Pharmacy Data

**Entity:** Prescription

```json
{
  "id": "UUID",
  "prescription_number": "String (PRE-XXXXXX)",
  "patient_id": "UUID",
  "doctor_id": "UUID",
  "appointment_id": "UUID",
  "issued_date": "DateTime",
  "medications": "Array[{
    drug_id: UUID,
    drug_name: String,
    dosage: String,
    frequency: String,
    duration_days: Integer,
    quantity: Integer,
    instructions: Text,
    route: Enum[Oral, Topical, Injection, Inhalation]
  }]",
  "diagnosis": "String",
  "notes": "Text",
  "status": "Enum: [Active, Dispensed, Completed, Cancelled]",
  "dispensed_at": "DateTime",
  "dispensed_by": "UUID (pharmacist_id)",
  "refills_allowed": "Integer",
  "refills_remaining": "Integer"
}
```

**Entity:** Drug (Inventory)

```json
{
  "id": "UUID",
  "drug_code": "String (Unique)",
  "name": "String",
  "generic_name": "String",
  "brand_name": "String",
  "manufacturer": "String",
  "category": "String (Antibiotic, Analgesic, etc.)",
  "dosage_form": "Enum: [Tablet, Capsule, Syrup, Injection, Cream]",
  "strength": "String",
  "unit": "String (mg, ml, etc.)",
  "inventory": {
    "quantity_in_stock": "Integer",
    "reorder_level": "Integer",
    "reorder_quantity": "Integer",
    "location": "String (shelf/bin number)"
  },
  "pricing": {
    "cost_price": "Decimal",
    "selling_price": "Decimal",
    "currency": "String"
  },
  "batch_info": "Array[{
    batch_number: String,
    manufacturing_date: Date,
    expiry_date: Date,
    quantity: Integer
  }]",
  "storage_conditions": "String",
  "interactions": "Array[drug_id] (drugs that interact)",
  "contraindications": "Array[String]",
  "side_effects": "Array[String]",
  "created_at": "DateTime",
  "updated_at": "DateTime"
}
```

**Data Volume:** 
- Prescriptions: 500-2,000/day
- Drugs: 1,000-5,000 items

**Retention:** 7 years (legal requirement)

---

### 2.5 Laboratory Data

**Entity:** LabTest

```json
{
  "id": "UUID",
  "test_number": "String (LAB-XXXXXX)",
  "patient_id": "UUID",
  "doctor_id": "UUID",
  "appointment_id": "UUID",
  "test_type": "String (CBC, Lipid Panel, X-Ray, etc.)",
  "test_category": "Enum: [Blood, Urine, Imaging, Pathology, Microbiology]",
  "sample_info": {
    "sample_id": "String",
    "sample_type": "String",
    "collection_date": "DateTime",
    "collected_by": "UUID (staff_id)"
  },
  "ordered_at": "DateTime",
  "status": "Enum: [Ordered, SampleCollected, InProgress, ResultsReady, Validated, Delivered]",
  "priority": "Enum: [Routine, Urgent, STAT]",
  "results": {
    "parameters": "Array[{
      name: String,
      value: String/Float,
      unit: String,
      reference_range: String,
      is_abnormal: Boolean,
      flags: Array[String]
    }]",
    "interpretation": "Text",
    "notes": "Text"
  },
  "performed_by": "UUID (lab_tech_id)",
  "performed_at": "DateTime",
  "validated_by": "UUID (pathologist_id)",
  "validated_at": "DateTime",
  "report_url": "String (PDF storage path)",
  "created_at": "DateTime"
}
```

**Data Volume:** 300-1,000 tests/day

**Retention:** 10 years

---

### 2.6 Billing & Finance Data

**Entity:** Invoice

```json
{
  "id": "UUID",
  "invoice_number": "String (INV-XXXXXX)",
  "patient_id": "UUID",
  "invoice_date": "Date",
  "due_date": "Date",
  "line_items": "Array[{
    item_type: Enum[Consultation, Procedure, Lab, Pharmacy, Bed],
    description: String,
    reference_id: UUID (appointment/prescription/test),
    quantity: Integer,
    unit_price: Decimal,
    discount: Decimal,
    tax: Decimal,
    total: Decimal
  }]",
  "subtotal": "Decimal",
  "total_discount": "Decimal",
  "total_tax": "Decimal",
  "total_amount": "Decimal",
  "currency": "String",
  "payment_info": {
    "paid_amount": "Decimal",
    "balance": "Decimal",
    "status": "Enum: [Pending, PartiallyPaid, Paid, Overdue, Cancelled]",
    "payment_method": "Enum: [Cash, Card, BankTransfer, Insurance]",
    "payment_date": "DateTime",
    "transaction_id": "String"
  },
  "insurance_claim": {
    "claim_id": "String",
    "insurance_provider": "String",
    "claim_amount": "Decimal",
    "approved_amount": "Decimal",
    "status": "Enum: [Submitted, Approved, Rejected, PartiallyApproved]"
  },
  "created_by": "UUID",
  "created_at": "DateTime"
}
```

**Data Volume:** 500-2,000 invoices/day

**Retention:** 10 years (tax/audit requirements)

---

### 2.7 Bed & Room Management Data

**Entity:** Bed

```json
{
  "id": "UUID",
  "bed_number": "String (Unique)",
  "room_number": "String",
  "ward": "String",
  "floor": "Integer",
  "building": "String",
  "bed_type": "Enum: [ICU, GeneralWard, PrivateRoom, SemiPrivate, Maternity, Pediatric]",
  "features": "Array[String] (Ventilator, Cardiac Monitor, etc.)",
  "status": "Enum: [Available, Occupied, Reserved, UnderMaintenance, Cleaning]",
  "current_admission": {
    "patient_id": "UUID",
    "admitted_at": "DateTime",
    "expected_discharge": "Date",
    "admission_type": "Enum: [Emergency, Elective, Transfer]",
    "attending_doctor": "UUID"
  },
  "housekeeping_status": "Enum: [Clean, InProgress, NeedsCleaning, Inspected]",
  "last_cleaned_at": "DateTime",
  "daily_rate": "Decimal",
  "created_at": "DateTime",
  "updated_at": "DateTime"
}
```

**Data Volume:** 50-500 beds

**Retention:** 5 years

---

### 2.8 Audit Log Data

**Entity:** AuditLog

```json
{
  "id": "UUID",
  "timestamp": "DateTime (indexed)",
  "user_id": "UUID",
  "user_role": "String",
  "action": "Enum: [Create, Read, Update, Delete, Login, Logout]",
  "resource_type": "String (Patient, Appointment, etc.)",
  "resource_id": "UUID",
  "changes": {
    "before": "JSON",
    "after": "JSON"
  },
  "ip_address": "String",
  "user_agent": "String",
  "result": "Enum: [Success, Failure]",
  "error_message": "Text"
}
```

**Data Volume:** 10,000-50,000 logs/day

**Retention:** 7 years (compliance)

---

## 3. Data Relationships

### 3.1 Entity Relationship Diagram (ERD)

```
          ┌──────────────┐
          │   Patient    │
          └──────┬───────┘
                 │
      ┌────────┼────────────────────────┐
      │        │                           │
      ▼        ▼                           ▼
┌────────────┐  ┌────────────┐  ┌────────────┐
│Appointment│  │Prescription│  │  Lab Test  │
└────┬───────┘  └───┬───────┘  └────────────┘
     │             │
     │             ▼
     │      ┌────────────┐
     │      │    Drug    │
     │      └────────────┘
     │
     ▼
┌────────────┐
│  Invoice   │
└────────────┘

┌────────────┐
│   Staff    │ ───> (doctor_id in Appointment, Prescription, etc.)
└────────────┘

┌────────────┐
│    Bed     │ ───> (current_admission.patient_id)
└────────────┘
```

### 3.2 Data Flow

**Patient Journey Data Flow:**
```
1. Patient Registration → patients collection
2. Appointment Booking → appointments collection
3. Doctor Consultation → Update appointment, Create prescription
4. Lab Test Ordered → lab_tests collection
5. Pharmacy Dispensation → Update prescription status
6. Billing → invoices collection
7. Payment → Update invoice
8. Discharge/Bed Release → Update bed status
9. All actions → audit_logs collection
```

---

## 4. Data Warehouse & Analytics

### 4.1 Data Mart Structure

**Purpose:** Analytical reporting and business intelligence

**Architecture:** Star Schema

#### 4.1.1 Fact Tables

**Fact_Appointment:**
```sql
fact_appointment_id (PK)
date_key (FK)
patient_key (FK)
doctor_key (FK)
department_key (FK)
appointment_count
duration_minutes
wait_time_minutes
revenue_generated
status
no_show_flag
```

**Fact_Lab_Test:**
```sql
fact_lab_test_id (PK)
date_key (FK)
patient_key (FK)
test_type_key (FK)
turnaround_time_hours
test_cost
abnormal_result_flag
```

**Fact_Prescription:**
```sql
fact_prescription_id (PK)
date_key (FK)
patient_key (FK)
doctor_key (FK)
drug_key (FK)
quantity_prescribed
total_cost
```

**Fact_Revenue:**
```sql
fact_revenue_id (PK)
date_key (FK)
patient_key (FK)
service_type_key (FK)
invoice_amount
paid_amount
outstanding_amount
payment_method
```

**Fact_Bed_Occupancy:**
```sql
fact_bed_occupancy_id (PK)
date_key (FK)
bed_key (FK)
patient_key (FK)
occupancy_hours
daily_rate
revenue
```

#### 4.1.2 Dimension Tables

**Dim_Date:**
```sql
date_key (PK)
date
day_of_week
week_of_year
month
quarter
year
is_weekend
is_holiday
holiday_name
```

**Dim_Patient:**
```sql
patient_key (PK)
patient_id (business key)
age_group
gender
blood_type
city
state
insurance_type
risk_level
```

**Dim_Doctor:**
```sql
doctor_key (PK)
staff_id (business key)
name
specialization
department
years_of_experience
```

**Dim_Department:**
```sql
department_key (PK)
department_name
department_type
floor
head_of_department
```

**Dim_Drug:**
```sql
drug_key (PK)
drug_id (business key)
drug_name
generic_name
category
manufacturer
```

**Dim_Service_Type:**
```sql
service_type_key (PK)
service_name
service_category (Consultation, Lab, Pharmacy, Bed)
standard_price
```

### 4.2 ETL Process

**Extract-Transform-Load Pipeline:**

```
1. EXTRACT (Daily at 2 AM)
   - Pull data from MongoDB (operational database)
   - Extract previous day's transactions

2. TRANSFORM
   - Data cleaning and validation
   - Apply business rules
   - Calculate derived metrics
   - Aggregate data
   - Handle slowly changing dimensions (SCD Type 2)

3. LOAD
   - Load into data warehouse (MongoDB analytics database)
   - Update fact tables
   - Update dimension tables
   - Create aggregated views

4. VALIDATE
   - Data quality checks
   - Reconciliation with source
   - Alert on anomalies
```

### 4.3 Analytical Queries & KPIs

**Key Performance Indicators (KPIs):**

1. **Patient Metrics:**
   - Total active patients
   - New patient registrations (daily/monthly)
   - Patient retention rate
   - Average patient age
   - Patient satisfaction score

2. **Appointment Metrics:**
   - Total appointments (daily/monthly)
   - Appointment show rate
   - No-show rate
   - Average wait time
   - Appointment utilization rate

3. **Clinical Metrics:**
   - Average length of stay
   - Bed occupancy rate
   - Lab test turnaround time
   - Prescription fill rate
   - Re-admission rate (within 30 days)

4. **Financial Metrics:**
   - Daily/monthly revenue
   - Revenue by department
   - Average revenue per patient
   - Outstanding receivables
   - Collection rate
   - Insurance claim approval rate

5. **Operational Metrics:**
   - Staff utilization rate
   - Average consultation time
   - Pharmacy stock turnover
   - Lab test volume
   - Emergency response time

**Sample Analytical Queries:**

```python
# Query 1: Monthly appointment trends by department
db.fact_appointment.aggregate([
    {"$lookup": {"from": "dim_date", "localField": "date_key", "foreignField": "date_key", "as": "date"}},
    {"$lookup": {"from": "dim_department", "localField": "department_key", "foreignField": "department_key", "as": "dept"}},
    {"$group": {
        "_id": {"month": "$date.month", "year": "$date.year", "department": "$dept.department_name"},
        "total_appointments": {"$sum": "$appointment_count"},
        "avg_duration": {"$avg": "$duration_minutes"},
        "no_show_count": {"$sum": {"$cond": ["$no_show_flag", 1, 0]}}
    }}
])

# Query 2: Top 10 revenue-generating departments
db.fact_revenue.aggregate([
    {"$lookup": {"from": "dim_department", "localField": "department_key", "foreignField": "department_key", "as": "dept"}},
    {"$group": {
        "_id": "$dept.department_name",
        "total_revenue": {"$sum": "$paid_amount"}
    }},
    {"$sort": {"total_revenue": -1}},
    {"$limit": 10}
])

# Query 3: Bed occupancy trends
db.fact_bed_occupancy.aggregate([
    {"$lookup": {"from": "dim_date", "localField": "date_key", "foreignField": "date_key", "as": "date"}},
    {"$group": {
        "_id": {"date": "$date.date"},
        "total_occupied_beds": {"$sum": 1},
        "occupancy_hours": {"$sum": "$occupancy_hours"},
        "revenue": {"$sum": "$revenue"}
    }},
    {"$addFields": {
        "occupancy_rate": {"$divide": ["$occupancy_hours", {"$multiply": ["$total_occupied_beds", 24]}]}
    }}
])
```

---

## 5. Data Quality & Governance

### 5.1 Data Quality Rules

**Validation Rules:**
1. **Completeness**: Required fields must not be null
2. **Accuracy**: Data must match expected formats (email, phone, dates)
3. **Consistency**: Cross-field validation (e.g., discharge date > admission date)
4. **Uniqueness**: Unique identifiers must be unique
5. **Timeliness**: Data should be current and up-to-date

**Data Quality Checks:**
```python
# Example validation
def validate_patient_data(patient):
    errors = []
    
    # Completeness
    if not patient.get('first_name'):
        errors.append("First name is required")
    
    # Accuracy
    if patient.get('email') and not is_valid_email(patient['email']):
        errors.append("Invalid email format")
    
    # Consistency
    if patient.get('date_of_birth'):
        age = calculate_age(patient['date_of_birth'])
        if age < 0 or age > 150:
            errors.append("Invalid date of birth")
    
    return errors
```

### 5.2 Data Governance

**Data Ownership:**
- **Patient Data**: Medical Records Department
- **Financial Data**: Finance Department
- **Operational Data**: Operations Manager
- **Clinical Data**: Chief Medical Officer

**Data Access Policies:**
1. **Role-Based Access**: Access based on user role
2. **Need-to-Know Basis**: Access only to required data
3. **Audit All Access**: Log all data access attempts
4. **Data Anonymization**: Anonymize data for analytics when possible

### 5.3 Data Retention Policy

| Data Type | Retention Period | Reason |
|-----------|------------------|--------|
| Patient Records | Permanent | Legal requirement |
| Lab Results | 10 years | Medical necessity |
| Prescriptions | 7 years | Legal requirement |
| Financial Records | 10 years | Tax/Audit |
| Audit Logs | 7 years | Compliance |
| Appointments | 5 years | Operational |
| System Logs | 1 year | Troubleshooting |

**Archival Strategy:**
- Move data older than retention period to cold storage
- Compressed format for archived data
- Retrieval process for archived data

---

## 6. Data Security & Privacy

### 6.1 Sensitive Data Handling

**PII/PHI Fields:**
- Patient name, contact info, national ID
- Medical history, diagnoses, test results
- Financial information
- Insurance details

**Encryption:**
- **At Rest**: AES-256 encryption for MongoDB
- **In Transit**: TLS 1.3 for all communications
- **Field-Level**: Encrypt sensitive fields (e.g., national_id, salary)

### 6.2 Data Anonymization

**For Analytics/Research:**
```python
def anonymize_patient_data(patient):
    return {
        "patient_id": hash(patient['id']),  # One-way hash
        "age_group": get_age_group(patient['date_of_birth']),
        "gender": patient['gender'],
        "city": patient['address']['city'],
        # Remove: name, contact info, national ID
    }
```

### 6.3 PDPA Compliance

**Personal Data Protection Act (PDPA) Requirements:**

1. **Consent Management**:
   - Obtain explicit consent for data collection
   - Allow consent withdrawal
   - Record consent history

2. **Data Subject Rights**:
   - Right to access personal data
   - Right to correction
   - Right to deletion ("Right to be forgotten")
   - Right to data portability

3. **Data Processing**:
   - Process only for legitimate purposes
   - Minimize data collection
   - Ensure data accuracy

4. **Data Breach Notification**:
   - Detect breaches within 24 hours
   - Notify authorities within 72 hours
   - Notify affected individuals

---

## 7. Backup & Disaster Recovery

### 7.1 Backup Strategy

**MongoDB Backup:**
- **Full Backup**: Daily at 2 AM
- **Incremental Backup**: Hourly
- **Retention**: 30 days online, 1 year archived
- **Storage**: AWS S3 / Azure Blob (cross-region)

**Backup Process:**
```bash
# Daily full backup
mongodump --uri="$MONGO_URL" --out="/backup/$(date +%Y%m%d)"

# Compress and upload to S3
tar -czf backup_$(date +%Y%m%d).tar.gz /backup/$(date +%Y%m%d)
aws s3 cp backup_$(date +%Y%m%d).tar.gz s3://hosprime-backups/
```

### 7.2 Disaster Recovery

**Recovery Objectives:**
- **RTO (Recovery Time Objective)**: 4 hours
- **RPO (Recovery Point Objective)**: 1 hour

**Recovery Steps:**
1. Declare disaster
2. Spin up backup infrastructure
3. Restore latest backup
4. Replay transaction logs (if available)
5. Verify data integrity
6. Switch DNS to backup site
7. Resume operations

---

## 8. Data Migration & Integration

### 8.1 Legacy System Migration

**Migration Strategy:**
1. **Assessment**: Analyze legacy data structure
2. **Mapping**: Map legacy fields to new schema
3. **Extraction**: Extract data from legacy system
4. **Transformation**: Clean and transform data
5. **Validation**: Validate migrated data
6. **Load**: Import into HosPRIME
7. **Reconciliation**: Verify data accuracy

### 8.2 External System Integration

**Integration Points:**
- **Laboratory Equipment**: HL7 interface
- **Radiology (PACS)**: DICOM integration
- **Insurance Providers**: API integration
- **Government Health Systems**: Secure data exchange
- **Pharmacy Suppliers**: EDI integration

---

*Document Version: 1.0*
*Last Updated: June 2026*