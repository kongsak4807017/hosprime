from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field

# ---------- Auth ----------

ROLES = ["admin", "doctor", "nurse", "pharmacist", "lab_technician", "finance", "patient"]


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: str
    role: str
    department: Optional[str] = None
    specialization: Optional[str] = None
    phone: Optional[str] = None


# ---------- Patient ----------

class Address(BaseModel):
    street: Optional[str] = ""
    city: Optional[str] = ""
    state: Optional[str] = ""
    postal_code: Optional[str] = ""


class EmergencyContact(BaseModel):
    name: Optional[str] = ""
    relationship: Optional[str] = ""
    phone: Optional[str] = ""


class Insurance(BaseModel):
    provider: Optional[str] = ""
    policy_number: Optional[str] = ""
    coverage_type: Optional[str] = ""


class Allergy(BaseModel):
    allergen: str
    severity: Optional[str] = ""
    reaction: Optional[str] = ""


class ChronicCondition(BaseModel):
    condition: str
    diagnosed_date: Optional[str] = ""
    status: Optional[str] = "active"


class Medication(BaseModel):
    drug_name: str
    dosage: Optional[str] = ""
    frequency: Optional[str] = ""


class PatientCreate(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: str
    gender: str
    national_id: Optional[str] = ""
    blood_type: Optional[str] = ""
    marital_status: Optional[str] = ""
    occupation: Optional[str] = ""
    nationality: Optional[str] = "ไทย"
    phone: str
    email: Optional[str] = ""
    address: Address = Address()
    emergency_contact: EmergencyContact = EmergencyContact()
    insurance: Insurance = Insurance()
    allergies: List[Allergy] = []
    chronic_conditions: List[ChronicCondition] = []
    current_medications: List[Medication] = []
    notes: Optional[str] = ""


class PatientUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[str] = None
    gender: Optional[str] = None
    national_id: Optional[str] = None
    blood_type: Optional[str] = None
    marital_status: Optional[str] = None
    occupation: Optional[str] = None
    nationality: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[Address] = None
    emergency_contact: Optional[EmergencyContact] = None
    insurance: Optional[Insurance] = None
    allergies: Optional[List[Allergy]] = None
    chronic_conditions: Optional[List[ChronicCondition]] = None
    current_medications: Optional[List[Medication]] = None
    notes: Optional[str] = None
    is_active: Optional[bool] = None


class VitalsCreate(BaseModel):
    temperature: Optional[float] = None
    bp_systolic: Optional[int] = None
    bp_diastolic: Optional[int] = None
    heart_rate: Optional[int] = None
    respiratory_rate: Optional[int] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    notes: Optional[str] = ""


# ---------- Appointment ----------

APPOINTMENT_STATUSES = [
    "scheduled", "confirmed", "checked_in", "in_progress",
    "completed", "cancelled", "no_show",
]


class AppointmentCreate(BaseModel):
    patient_id: str
    doctor_id: str
    department: str
    appointment_type: str = "consultation"
    appointment_date: str
    appointment_time: str
    duration_minutes: int = 30
    reason: Optional[str] = ""
    priority: str = "normal"
    room_number: Optional[str] = ""
    notes: Optional[str] = ""


class AppointmentUpdate(BaseModel):
    doctor_id: Optional[str] = None
    department: Optional[str] = None
    appointment_type: Optional[str] = None
    appointment_date: Optional[str] = None
    appointment_time: Optional[str] = None
    duration_minutes: Optional[int] = None
    reason: Optional[str] = None
    priority: Optional[str] = None
    room_number: Optional[str] = None
    notes: Optional[str] = None


class StatusUpdate(BaseModel):
    status: str
