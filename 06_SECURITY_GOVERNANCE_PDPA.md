# HosPRIME - Security, Governance & PDPA Compliance

## 1. Overview

This document outlines the comprehensive security framework, governance policies, and Personal Data Protection Act (PDPA) compliance measures for HosPRIME.

## 2. Security Architecture

### 2.1 Security Principles

**Core Principles:**
1. **Defense in Depth**: Multiple layers of security controls
2. **Least Privilege**: Minimum access rights for users and systems
3. **Zero Trust**: Verify every access request
4. **Security by Design**: Security built into architecture
5. **Data Protection**: Protect data at rest, in transit, and in use

### 2.2 Security Layers

```
┌───────────────────────────────────────────────────┐
│ Layer 1: Network Security                            │
│ - Firewall, WAF, DDoS Protection, VPN               │
└─────────────────────────┬────────────────────────┘
                          │
┌─────────────────────────▼────────────────────────┐
│ Layer 2: Application Security                        │
│ - Authentication, Authorization, Input Validation   │
└─────────────────────────┬────────────────────────┘
                          │
┌─────────────────────────▼────────────────────────┐
│ Layer 3: Data Security                               │
│ - Encryption, Access Control, Data Masking          │
└─────────────────────────┬────────────────────────┘
                          │
┌─────────────────────────▼────────────────────────┐
│ Layer 4: Audit & Monitoring                          │
│ - Logging, Alerting, Incident Response              │
└───────────────────────────────────────────────────┘
```

## 3. Authentication & Authorization

### 3.1 Authentication Mechanism

**JWT (JSON Web Token) Based Authentication:**

```python
# Authentication Flow
class AuthService:
    def login(self, email: str, password: str):
        # 1. Validate credentials
        user = self.validate_credentials(email, password)
        
        if not user:
            raise AuthenticationError("Invalid credentials")
        
        # 2. Check account status
        if not user.is_active:
            raise AuthenticationError("Account disabled")
        
        # 3. Generate tokens
        access_token = self.generate_access_token(user)
        refresh_token = self.generate_refresh_token(user)
        
        # 4. Log authentication event
        self.log_login(user)
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": 900  # 15 minutes
        }
    
    def generate_access_token(self, user):
        payload = {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role,
            "permissions": user.permissions,
            "exp": datetime.utcnow() + timedelta(minutes=15)
        }
        return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
```

**Password Policy:**
- Minimum 12 characters
- Must include: uppercase, lowercase, number, special character
- Cannot reuse last 5 passwords
- Password expiry: 90 days
- Account lockout after 5 failed attempts
- Stored using bcrypt hashing (cost factor 12)

**Multi-Factor Authentication (MFA):**
- Optional for regular users
- Mandatory for administrators
- Methods: TOTP (Google Authenticator), SMS, Email

### 3.2 Role-Based Access Control (RBAC)

**Roles & Permissions Matrix:**

| Resource | Admin | Doctor | Nurse | Pharmacist | Lab Tech | Finance | Patient |
|----------|-------|--------|-------|------------|----------|---------|--------|
| **Patients** |
| Create | ✓ | ✓ | ✓ | × | × | × | × |
| Read All | ✓ | Own only | Own only | Rx only | Test only | × | Own only |
| Update | ✓ | ✓ | Limited | × | × | × | Limited |
| Delete | ✓ | × | × | × | × | × | × |
| **Appointments** |
| Create | ✓ | ✓ | ✓ | × | × | × | ✓ |
| Read | ✓ | Own only | Assigned | × | × | × | Own only |
| Update | ✓ | ✓ | ✓ | × | × | × | Cancel only |
| Delete | ✓ | × | × | × | × | × | × |
| **Prescriptions** |
| Create | ✓ | ✓ | × | × | × | × | × |
| Read | ✓ | Own only | Read only | ✓ | × | × | Own only |
| Dispense | ✓ | × | × | ✓ | × | × | × |
| **Lab Tests** |
| Order | ✓ | ✓ | × | × | × | × | × |
| Enter Results | ✓ | × | × | × | ✓ | × | × |
| Read Results | ✓ | Own patients | Read only | × | ✓ | × | Own only |
| **Billing** |
| Create Invoice | ✓ | × | × | × | × | ✓ | × |
| Process Payment | ✓ | × | × | × | × | ✓ | ✓ |
| View Reports | ✓ | × | × | × | × | ✓ | Own only |
| **System Admin** |
| User Management | ✓ | × | × | × | × | × | × |
| System Config | ✓ | × | × | × | × | × | × |
| Audit Logs | ✓ | × | × | × | × | × | × |

**Permission Enforcement:**
```python
# Decorator for permission checking
def require_permission(permission: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            user = get_current_user()
            if not user.has_permission(permission):
                raise PermissionDenied(f"Permission required: {permission}")
            return await func(*args, **kwargs)
        return wrapper
    return decorator

# Usage
@api_router.get("/patients/{id}")
@require_permission("patient.read")
async def get_patient(id: str):
    return await patient_service.get_by_id(id)
```

## 4. Data Security

### 4.1 Encryption

**Encryption at Rest:**
- **MongoDB**: Encrypted storage engine (AES-256)
- **Neo4j**: Encrypted at file system level
- **Backups**: Encrypted before upload to cloud storage

**Encryption in Transit:**
- **HTTPS/TLS 1.3**: All external communications
- **Internal services**: mTLS (mutual TLS) for service-to-service

**Field-Level Encryption:**
```python
# Sensitive fields encrypted before storage
from cryptography.fernet import Fernet

class EncryptionService:
    def __init__(self):
        self.cipher = Fernet(ENCRYPTION_KEY)
    
    def encrypt_field(self, value: str) -> str:
        return self.cipher.encrypt(value.encode()).decode()
    
    def decrypt_field(self, encrypted: str) -> str:
        return self.cipher.decrypt(encrypted.encode()).decode()

# Apply to sensitive fields
patient_data = {
    "name": "John Doe",
    "national_id": encryption_service.encrypt_field("123456789"),
    "phone": encryption_service.encrypt_field("+1234567890")
}
```

### 4.2 Data Masking

**Dynamic Data Masking:**
```python
# Mask sensitive data for non-authorized users
def mask_patient_data(patient, user_role):
    if user_role in ["Admin", "Doctor"]:
        return patient  # Full access
    
    # Mask for other roles
    return {
        **patient,
        "national_id": "***-***-" + patient["national_id"][-4:],
        "phone": "***-***-" + patient["phone"][-4:],
        "email": "***@" + patient["email"].split("@")[1],
        "address": {"city": patient["address"]["city"]}  # Only city
    }
```

### 4.3 Secure Data Disposal

**Data Deletion Policy:**
- **Soft Delete**: Mark as deleted, retain for 30 days
- **Hard Delete**: Permanent removal after retention period
- **Secure Wipe**: Overwrite data 3 times before deletion

```python
async def delete_patient(patient_id: str, hard_delete: bool = False):
    if not hard_delete:
        # Soft delete
        await db.patients.update_one(
            {"id": patient_id},
            {"$set": {"is_deleted": True, "deleted_at": datetime.utcnow()}}
        )
    else:
        # Hard delete (admin only, after retention period)
        await db.patients.delete_one({"id": patient_id})
        # Also delete from all related collections
        await db.appointments.delete_many({"patient_id": patient_id})
        await db.prescriptions.delete_many({"patient_id": patient_id})
```

## 5. Application Security

### 5.1 Input Validation

**Pydantic Models for Validation:**
```python
from pydantic import BaseModel, EmailStr, constr, validator

class PatientCreate(BaseModel):
    first_name: constr(min_length=1, max_length=100)
    last_name: constr(min_length=1, max_length=100)
    email: EmailStr
    phone: constr(regex=r'^\+?[1-9]\d{1,14}$')
    date_of_birth: date
    
    @validator('date_of_birth')
    def validate_dob(cls, v):
        if v > date.today():
            raise ValueError('Date of birth cannot be in the future')
        age = (date.today() - v).days / 365
        if age > 150:
            raise ValueError('Invalid date of birth')
        return v
```

### 5.2 SQL/NoSQL Injection Prevention

**MongoDB Query Safety:**
```python
# BAD - Vulnerable to injection
query = {"email": user_input}

# GOOD - Use parameterized queries
from bson import ObjectId

async def get_patient_safe(patient_id: str):
    # Validate UUID format
    try:
        uuid.UUID(patient_id)
    except ValueError:
        raise ValidationError("Invalid patient ID")
    
    # Safe query
    patient = await db.patients.find_one({"id": patient_id})
    return patient
```

### 5.3 Cross-Site Scripting (XSS) Prevention

**Frontend Sanitization:**
```javascript
// Use React's built-in escaping
// React automatically escapes values in JSX

const PatientName = ({ name }) => {
  return <div>{name}</div>;  // Automatically escaped
};

// For dangerouslySetInnerHTML, sanitize first
import DOMPurify from 'dompurify';

const RichText = ({ html }) => {
  const clean = DOMPurify.sanitize(html);
  return <div dangerouslySetInnerHTML={{ __html: clean }} />;
};
```

### 5.4 Cross-Site Request Forgery (CSRF) Protection

**CSRF Token Implementation:**
```python
# Backend - Generate CSRF token
from fastapi import Cookie, Header
import secrets

@app.get("/csrf-token")
async def get_csrf_token(response: Response):
    token = secrets.token_urlsafe(32)
    response.set_cookie(
        key="csrf_token",
        value=token,
        httponly=True,
        secure=True,
        samesite="strict"
    )
    return {"csrf_token": token}

# Validate CSRF token on state-changing requests
@app.post("/patients")
async def create_patient(
    data: PatientCreate,
    csrf_token: str = Cookie(),
    x_csrf_token: str = Header()
):
    if csrf_token != x_csrf_token:
        raise HTTPException(401, "Invalid CSRF token")
    # Process request
```

### 5.5 Rate Limiting

**API Rate Limiting:**
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

# Apply rate limits
@app.post("/auth/login")
@limiter.limit("5/minute")  # 5 attempts per minute
async def login(request: Request, credentials: LoginRequest):
    return await auth_service.login(credentials)

@app.get("/api/patients")
@limiter.limit("100/minute")  # 100 requests per minute
async def list_patients(request: Request):
    return await patient_service.list_all()
```

## 6. Network Security

### 6.1 Firewall Rules

**Ingress Rules:**
```
# Public access
Port 443 (HTTPS) - Allow from 0.0.0.0/0
Port 80 (HTTP) - Redirect to 443

# Internal only
Port 8001 (Backend API) - Allow from frontend subnet only
Port 27017 (MongoDB) - Allow from backend subnet only
Port 7687 (Neo4j) - Allow from backend subnet only

# SSH (Admin access only)
Port 22 - Allow from VPN IP range only
```

### 6.2 Web Application Firewall (WAF)

**WAF Rules:**
- Block SQL injection patterns
- Block XSS attempts
- Block common attack signatures
- Rate limiting per IP
- Geo-blocking (optional)

### 6.3 DDoS Protection

**Mitigation Strategies:**
- CloudFlare / AWS Shield
- Rate limiting at edge
- Connection limits
- SYN flood protection

## 7. Audit & Compliance

### 7.1 Audit Logging

**Comprehensive Audit Trail:**
```python
class AuditLogger:
    async def log(self, action: str, user_id: str, resource_type: str,
                  resource_id: str, changes: dict = None):
        log_entry = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow(),
            "user_id": user_id,
            "user_role": get_user_role(user_id),
            "action": action,  # CREATE, READ, UPDATE, DELETE
            "resource_type": resource_type,
            "resource_id": resource_id,
            "changes": changes,
            "ip_address": get_client_ip(),
            "user_agent": get_user_agent()
        }
        await db.audit_logs.insert_one(log_entry)

# Usage
@api_router.put("/patients/{id}")
async def update_patient(id: str, data: PatientUpdate, user = Depends(get_current_user)):
    old_data = await patient_service.get(id)
    updated = await patient_service.update(id, data)
    
    # Log the change
    await audit_logger.log(
        action="UPDATE",
        user_id=user.id,
        resource_type="Patient",
        resource_id=id,
        changes={"before": old_data, "after": updated}
    )
    
    return updated
```

**Audit Log Retention**: 7 years (immutable)

### 7.2 Security Monitoring

**Monitor for:**
- Failed login attempts (brute force)
- Unusual access patterns
- Privilege escalation attempts
- Data exfiltration (large downloads)
- After-hours access
- Access from unusual locations

**Automated Alerts:**
```python
class SecurityMonitor:
    async def detect_anomalies(self):
        # Failed login attempts
        failed_logins = await db.audit_logs.count_documents({
            "action": "LOGIN_FAILED",
            "timestamp": {"$gte": datetime.utcnow() - timedelta(minutes=5)},
            "ip_address": ip
        })
        
        if failed_logins >= 5:
            await self.alert(f"Brute force attack detected from {ip}")
            await self.block_ip(ip)
```

## 8. PDPA Compliance

### 8.1 Personal Data Protection Act Requirements

**Key Requirements:**

1. **Consent Management**
2. **Data Subject Rights**
3. **Data Minimization**
4. **Data Accuracy**
5. **Storage Limitation**
6. **Integrity & Confidentiality**
7. **Accountability**

### 8.2 Consent Management

**Consent Model:**
```python
class Consent(BaseModel):
    patient_id: str
    consent_type: Enum  # DataCollection, DataProcessing, DataSharing, Marketing
    purpose: str
    given_at: datetime
    withdrawn_at: Optional[datetime]
    status: Enum  # Active, Withdrawn
    
# Request consent
async def request_consent(patient_id: str, consent_type: str, purpose: str):
    consent = Consent(
        patient_id=patient_id,
        consent_type=consent_type,
        purpose=purpose,
        given_at=datetime.utcnow(),
        status="Active"
    )
    await db.consents.insert_one(consent.dict())

# Check consent before processing
async def has_consent(patient_id: str, purpose: str) -> bool:
    consent = await db.consents.find_one({
        "patient_id": patient_id,
        "purpose": purpose,
        "status": "Active",
        "withdrawn_at": None
    })
    return consent is not None
```

### 8.3 Data Subject Rights

**Right to Access:**
```python
@api_router.get("/my-data")
async def get_my_data(user = Depends(get_current_patient)):
    """Patient can download all their data"""
    patient_data = await patient_service.get(user.id)
    appointments = await appointment_service.get_by_patient(user.id)
    prescriptions = await prescription_service.get_by_patient(user.id)
    lab_tests = await lab_service.get_by_patient(user.id)
    
    # Compile into downloadable format
    export_data = {
        "personal_info": patient_data,
        "appointments": appointments,
        "prescriptions": prescriptions,
        "lab_tests": lab_tests,
        "exported_at": datetime.utcnow()
    }
    
    return export_data
```

**Right to Rectification:**
```python
@api_router.put("/my-data/correct")
async def correct_my_data(corrections: PatientUpdate, user = Depends(get_current_patient)):
    """Patient can request correction of their data"""
    await patient_service.update(user.id, corrections)
    await audit_logger.log("DATA_CORRECTION", user.id, "Patient", user.id)
```

**Right to Erasure ("Right to be Forgotten"):**
```python
@api_router.delete("/my-data")
async def delete_my_data(user = Depends(get_current_patient)):
    """Patient can request deletion (subject to legal retention)"""
    # Check if legal retention applies
    retention_period = await check_retention_policy(user.id)
    
    if retention_period > 0:
        return {
            "message": f"Data cannot be deleted due to legal retention (remaining: {retention_period} years)"
        }
    
    # Anonymize instead of delete (to preserve medical research value)
    await patient_service.anonymize(user.id)
    await audit_logger.log("DATA_ERASURE", user.id, "Patient", user.id)
```

### 8.4 Data Breach Response

**Breach Response Plan:**

1. **Detection** (within 24 hours)
   - Automated monitoring
   - User reports
   - Security audits

2. **Assessment** (within 24 hours)
   - Scope of breach
   - Data affected
   - Number of individuals
   - Risk level

3. **Containment** (immediate)
   - Isolate affected systems
   - Revoke compromised credentials
   - Block attack vectors

4. **Notification** (within 72 hours)
   - Notify data protection authority
   - Notify affected individuals
   - Public disclosure (if required)

5. **Remediation**
   - Fix vulnerabilities
   - Restore from backups
   - Implement additional controls

6. **Post-Incident Review**
   - Root cause analysis
   - Update security policies
   - Staff training

**Breach Notification Template:**
```
Subject: Important Security Notice - Data Breach Notification

Dear [Patient Name],

We are writing to inform you of a data security incident that may affect your personal information.

What Happened:
[Description of the incident]

What Information Was Involved:
[List of data types affected]

What We Are Doing:
[Steps taken to address the breach]

What You Can Do:
[Recommended actions for the individual]

For More Information:
[Contact details]

Sincerely,
HosPRIME Data Protection Officer
```

## 9. Security Testing & Validation

### 9.1 Security Testing Schedule

| Test Type | Frequency | Responsibility |
|-----------|-----------|----------------|
| Vulnerability Scan | Weekly | Security Team |
| Penetration Testing | Quarterly | External Auditor |
| Code Security Review | Every Release | Dev Team |
| Access Control Audit | Monthly | IT Admin |
| Compliance Audit | Annually | External Auditor |

### 9.2 Incident Response Plan

**Incident Severity Levels:**

- **Critical**: Data breach, system compromise, ransomware
- **High**: Unauthorized access, DDoS attack
- **Medium**: Failed attacks, suspicious activity
- **Low**: Policy violations, minor vulnerabilities

**Response Team:**
- Incident Commander
- Security Team
- IT Operations
- Legal Counsel
- Public Relations
- Management

## 10. Security Training & Awareness

### 10.1 Staff Security Training

**Training Schedule:**
- **New employees**: Security training during onboarding
- **All staff**: Annual security awareness training
- **IT staff**: Quarterly advanced security training
- **Administrators**: Monthly security briefings

**Training Topics:**
- Password security
- Phishing awareness
- Social engineering
- Data handling best practices
- Incident reporting
- PDPA compliance

### 10.2 Security Policies

**Key Policies:**
1. **Acceptable Use Policy**: Proper use of system resources
2. **Password Policy**: Strong password requirements
3. **Data Classification Policy**: How to handle different data types
4. **Incident Response Policy**: Steps to report and respond to incidents
5. **BYOD Policy**: Guidelines for personal devices
6. **Remote Access Policy**: Secure remote access procedures

---

*Document Version: 1.0*
*Last Updated: June 2026*