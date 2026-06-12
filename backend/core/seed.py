import logging
import os
import uuid
from datetime import datetime, timedelta, timezone

from core.database import db
from core.security import hash_password, verify_password
from core.utils import next_number, now_iso

logger = logging.getLogger(__name__)

STAFF_USERS = [
    {"email": "doctor@hosprime.com", "full_name": "นพ.ปกรณ์ เวชศาสตร์", "role": "doctor", "department": "อายุรกรรม", "specialization": "อายุรศาสตร์ทั่วไป"},
    {"email": "doctor2@hosprime.com", "full_name": "พญ.สุดารัตน์ ใจเย็น", "role": "doctor", "department": "กุมารเวชกรรม", "specialization": "กุมารเวชศาสตร์"},
    {"email": "nurse@hosprime.com", "full_name": "พว.จิราพร ดูแลดี", "role": "nurse", "department": "อายุรกรรม"},
    {"email": "pharmacist@hosprime.com", "full_name": "ภก.ธนพล ยาดี", "role": "pharmacist", "department": "เภสัชกรรม"},
    {"email": "lab@hosprime.com", "full_name": "ทนพ.สมศักดิ์ วิเคราะห์ผล", "role": "lab_technician", "department": "ห้องปฏิบัติการ"},
    {"email": "finance@hosprime.com", "full_name": "คุณวรรณา บัญชีดี", "role": "finance", "department": "การเงิน"},
]

SAMPLE_PATIENTS = [
    {"first_name": "สมชาย", "last_name": "ใจดี", "date_of_birth": "1985-03-12", "gender": "male", "blood_type": "O+", "phone": "081-234-5678", "national_id": "1100501234561", "occupation": "พนักงานบริษัท",
     "allergies": [{"allergen": "Penicillin", "severity": "รุนแรง", "reaction": "ผื่นแพ้ หายใจลำบาก"}], "chronic_conditions": [], "current_medications": []},
    {"first_name": "สมหญิง", "last_name": "รักษ์สุขภาพ", "date_of_birth": "1990-07-25", "gender": "female", "blood_type": "A+", "phone": "082-345-6789", "national_id": "1100501234562", "occupation": "ครู",
     "allergies": [], "chronic_conditions": [], "current_medications": []},
    {"first_name": "วิชัย", "last_name": "พัฒนากุล", "date_of_birth": "1958-11-02", "gender": "male", "blood_type": "B+", "phone": "083-456-7890", "national_id": "1100501234563", "occupation": "ข้าราชการบำนาญ",
     "allergies": [], "chronic_conditions": [{"condition": "เบาหวานชนิดที่ 2", "diagnosed_date": "2015-06-01", "status": "active"}, {"condition": "ความดันโลหิตสูง", "diagnosed_date": "2018-02-15", "status": "active"}],
     "current_medications": [{"drug_name": "Metformin", "dosage": "500 mg", "frequency": "วันละ 2 ครั้ง"}, {"drug_name": "Amlodipine", "dosage": "5 mg", "frequency": "วันละ 1 ครั้ง"}]},
    {"first_name": "มาลี", "last_name": "ศรีสมบูรณ์", "date_of_birth": "1972-01-18", "gender": "female", "blood_type": "AB+", "phone": "084-567-8901", "national_id": "1100501234564", "occupation": "แม่บ้าน",
     "allergies": [], "chronic_conditions": [{"condition": "ไขมันในเลือดสูง", "diagnosed_date": "2020-09-10", "status": "active"}], "current_medications": [{"drug_name": "Simvastatin", "dosage": "20 mg", "frequency": "วันละ 1 ครั้ง ก่อนนอน"}]},
    {"first_name": "ประยุทธ์", "last_name": "มั่นคง", "date_of_birth": "1965-06-30", "gender": "male", "blood_type": "O-", "phone": "085-678-9012", "national_id": "1100501234565", "occupation": "เกษตรกร",
     "allergies": [], "chronic_conditions": [], "current_medications": []},
    {"first_name": "นภาพร", "last_name": "แสงทอง", "date_of_birth": "2001-09-14", "gender": "female", "blood_type": "A-", "phone": "086-789-0123", "national_id": "1100501234566", "occupation": "นักศึกษา",
     "allergies": [], "chronic_conditions": [], "current_medications": []},
    {"first_name": "กิตติ", "last_name": "วงศ์ไทย", "date_of_birth": "1995-04-08", "gender": "male", "blood_type": "B-", "phone": "087-890-1234", "national_id": "1100501234567", "occupation": "โปรแกรมเมอร์",
     "allergies": [], "chronic_conditions": [], "current_medications": []},
    {"first_name": "อรุณี", "last_name": "จันทร์เพ็ญ", "date_of_birth": "1980-12-22", "gender": "female", "blood_type": "O+", "phone": "088-901-2345", "national_id": "1100501234568", "occupation": "พยาบาล",
     "allergies": [{"allergen": "Aspirin", "severity": "ปานกลาง", "reaction": "ผื่นคัน"}], "chronic_conditions": [], "current_medications": []},
]


async def seed_admin():
    admin_email = os.environ["ADMIN_EMAIL"]
    admin_password = os.environ["ADMIN_PASSWORD"]
    existing = await db.users.find_one({"email": admin_email})
    if existing is None:
        await db.users.insert_one({
            "id": str(uuid.uuid4()),
            "email": admin_email,
            "password_hash": hash_password(admin_password),
            "full_name": "ผู้ดูแลระบบ HosPRIME",
            "role": "admin",
            "department": "บริหาร",
            "specialization": "",
            "phone": "",
            "is_active": True,
            "created_at": now_iso(),
        })
        logger.info("Admin user seeded: %s", admin_email)
    elif not verify_password(admin_password, existing["password_hash"]):
        await db.users.update_one(
            {"email": admin_email},
            {"$set": {"password_hash": hash_password(admin_password)}},
        )
        logger.info("Admin password updated from env")


async def seed_staff():
    password = os.environ.get("SEED_STAFF_PASSWORD", "Test@1234")
    for staff in STAFF_USERS:
        if await db.users.find_one({"email": staff["email"]}):
            continue
        await db.users.insert_one({
            "id": str(uuid.uuid4()),
            **staff,
            "password_hash": hash_password(password),
            "specialization": staff.get("specialization", ""),
            "phone": "",
            "is_active": True,
            "created_at": now_iso(),
        })
    logger.info("Staff users seeded")


async def seed_patients_and_appointments():
    if await db.patients.count_documents({}) > 0:
        return
    admin = await db.users.find_one({"role": "admin"})
    patient_ids = []
    for p in SAMPLE_PATIENTS:
        patient = {
            "id": str(uuid.uuid4()),
            "patient_number": await next_number("patient", "PAT"),
            **p,
            "marital_status": "",
            "nationality": "ไทย",
            "email": "",
            "address": {"street": "", "city": "กรุงเทพมหานคร", "state": "กรุงเทพมหานคร", "postal_code": "10110"},
            "emergency_contact": {"name": "", "relationship": "", "phone": ""},
            "insurance": {"provider": "สิทธิบัตรทอง (สปสช.)", "policy_number": "", "coverage_type": "หลักประกันสุขภาพถ้วนหน้า"},
            "vitals": [],
            "notes": "",
            "is_active": True,
            "created_at": now_iso(),
            "updated_at": now_iso(),
            "created_by": admin["id"],
        }
        await db.patients.insert_one(patient)
        patient_ids.append(patient)

    doctors = await db.users.find({"role": "doctor"}).to_list(10)
    if not doctors:
        return
    now = datetime.now(timezone.utc)
    today = now.strftime("%Y-%m-%d")
    tomorrow = (now + timedelta(days=1)).strftime("%Y-%m-%d")
    yesterday = (now - timedelta(days=1)).strftime("%Y-%m-%d")

    schedule = [
        (patient_ids[0], doctors[0], today, "09:00", "scheduled", "ปวดหัว มีไข้ 2 วัน"),
        (patient_ids[1], doctors[1], today, "09:30", "checked_in", "ตรวจสุขภาพประจำปี"),
        (patient_ids[2], doctors[0], today, "10:00", "in_progress", "ติดตามอาการเบาหวาน"),
        (patient_ids[3], doctors[0], today, "11:00", "completed", "ติดตามผลไขมันในเลือด"),
        (patient_ids[4], doctors[1], tomorrow, "09:00", "scheduled", "ปวดหลังเรื้อรัง"),
        (patient_ids[5], doctors[0], tomorrow, "10:30", "scheduled", "ตรวจสุขภาพก่อนทำงาน"),
        (patient_ids[6], doctors[1], yesterday, "14:00", "completed", "ไข้หวัดใหญ่"),
        (patient_ids[7], doctors[0], yesterday, "15:30", "no_show", "ปรึกษาอาการแพ้ยา"),
    ]
    for patient, doctor, date, time, status, reason in schedule:
        await db.appointments.insert_one({
            "id": str(uuid.uuid4()),
            "appointment_number": await next_number("appointment", "APT"),
            "patient_id": patient["id"],
            "patient_name": f"{patient['first_name']} {patient['last_name']}",
            "patient_number": patient["patient_number"],
            "doctor_id": doctor["id"],
            "doctor_name": doctor["full_name"],
            "department": doctor["department"],
            "appointment_type": "consultation",
            "appointment_date": date,
            "appointment_time": time,
            "duration_minutes": 30,
            "reason": reason,
            "priority": "normal",
            "room_number": "",
            "notes": "",
            "status": status,
            "created_at": now_iso(),
            "updated_at": now_iso(),
            "created_by": admin["id"],
        })
    logger.info("Sample patients and appointments seeded")


async def create_indexes():
    await db.users.create_index("email", unique=True)
    await db.users.create_index("id")
    await db.patients.create_index("id")
    await db.patients.create_index("patient_number")
    await db.appointments.create_index("id")
    await db.appointments.create_index([("appointment_date", 1), ("doctor_id", 1)])
    await db.login_attempts.create_index("identifier")
    await db.audit_logs.create_index("timestamp")


async def seed_all():
    await create_indexes()
    await seed_admin()
    await seed_staff()
    await seed_patients_and_appointments()
