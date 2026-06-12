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


SAMPLE_DRUGS = [
    {"name": "Paracetamol 500 mg", "generic_name": "Paracetamol", "category": "ยาแก้ปวด", "dosage_form": "Tablet", "strength": "500 mg", "quantity_in_stock": 5000, "reorder_level": 1000, "cost_price": 0.5, "selling_price": 1.0, "expiry_offset": 540},
    {"name": "Amoxicillin 500 mg", "generic_name": "Amoxicillin", "category": "ยาปฏิชีวนะ", "dosage_form": "Capsule", "strength": "500 mg", "quantity_in_stock": 800, "reorder_level": 500, "cost_price": 2.5, "selling_price": 5.0, "expiry_offset": 45},
    {"name": "Metformin 500 mg", "generic_name": "Metformin HCl", "category": "ยาเบาหวาน", "dosage_form": "Tablet", "strength": "500 mg", "quantity_in_stock": 3000, "reorder_level": 800, "cost_price": 1.0, "selling_price": 2.0, "expiry_offset": 400},
    {"name": "Amlodipine 5 mg", "generic_name": "Amlodipine", "category": "ยาความดัน", "dosage_form": "Tablet", "strength": "5 mg", "quantity_in_stock": 150, "reorder_level": 300, "cost_price": 1.5, "selling_price": 3.0, "expiry_offset": 300},
    {"name": "Simvastatin 20 mg", "generic_name": "Simvastatin", "category": "ยาลดไขมัน", "dosage_form": "Tablet", "strength": "20 mg", "quantity_in_stock": 1200, "reorder_level": 400, "cost_price": 2.0, "selling_price": 4.0, "expiry_offset": 365},
    {"name": "Omeprazole 20 mg", "generic_name": "Omeprazole", "category": "ยาระบบทางเดินอาหาร", "dosage_form": "Capsule", "strength": "20 mg", "quantity_in_stock": 900, "reorder_level": 300, "cost_price": 2.0, "selling_price": 4.5, "expiry_offset": 280},
    {"name": "Cetirizine 10 mg", "generic_name": "Cetirizine", "category": "ยาแก้แพ้", "dosage_form": "Tablet", "strength": "10 mg", "quantity_in_stock": 600, "reorder_level": 200, "cost_price": 1.0, "selling_price": 2.5, "expiry_offset": 420},
    {"name": "Losartan 50 mg", "generic_name": "Losartan", "category": "ยาความดัน", "dosage_form": "Tablet", "strength": "50 mg", "quantity_in_stock": 700, "reorder_level": 250, "cost_price": 2.5, "selling_price": 5.0, "expiry_offset": 330},
    {"name": "Aspirin 81 mg", "generic_name": "Acetylsalicylic acid", "category": "ยาโรคหัวใจ", "dosage_form": "Tablet", "strength": "81 mg", "quantity_in_stock": 1100, "reorder_level": 300, "cost_price": 0.8, "selling_price": 1.5, "expiry_offset": 500},
    {"name": "Vitamin B Complex", "generic_name": "Vitamin B Complex", "category": "วิตามิน", "dosage_form": "Tablet", "strength": "", "quantity_in_stock": 2000, "reorder_level": 500, "cost_price": 0.5, "selling_price": 1.0, "expiry_offset": 600},
]


async def seed_clinical():
    if await db.drugs.count_documents({}) > 0:
        return
    now = datetime.now(timezone.utc)
    drugs = []
    for d in SAMPLE_DRUGS:
        expiry = (now + timedelta(days=d.pop("expiry_offset"))).strftime("%Y-%m-%d")
        drug = {
            "id": str(uuid.uuid4()),
            "drug_code": await next_number("drug", "DRG"),
            **d,
            "unit": "เม็ด",
            "location": "คลังยาหลัก",
            "batches": [{"batch_number": f"B{now.strftime('%y%m')}-{len(drugs)+1:03d}", "expiry_date": expiry, "quantity": d["quantity_in_stock"]}],
            "storage_conditions": "เก็บในที่แห้ง อุณหภูมิไม่เกิน 30°C",
            "is_active": True,
            "created_at": now_iso(),
            "updated_at": now_iso(),
        }
        await db.drugs.insert_one(drug)
        drugs.append(drug)

    patients = await db.patients.find({}, {"_id": 0}).sort("patient_number", 1).to_list(10)
    doctors = await db.users.find({"role": "doctor"}, {"_id": 0}).to_list(5)
    pharmacist = await db.users.find_one({"role": "pharmacist"}, {"_id": 0})
    finance = await db.users.find_one({"role": "finance"}, {"_id": 0})
    lab_tech = await db.users.find_one({"role": "lab_technician"}, {"_id": 0})
    if not (patients and doctors):
        return

    def drug_by_name(name):
        return next(d for d in drugs if d["name"].startswith(name))

    # Prescriptions
    metformin, amlodipine, para = drug_by_name("Metformin"), drug_by_name("Amlodipine"), drug_by_name("Paracetamol")
    pres1 = {
        "id": str(uuid.uuid4()),
        "prescription_number": await next_number("prescription", "PRE"),
        "patient_id": patients[2]["id"],
        "patient_name": f"{patients[2]['first_name']} {patients[2]['last_name']}",
        "patient_number": patients[2]["patient_number"],
        "doctor_id": doctors[0]["id"],
        "doctor_name": doctors[0]["full_name"],
        "medications": [
            {"drug_id": metformin["id"], "drug_name": metformin["name"], "strength": "500 mg", "dosage": "1 เม็ด", "frequency": "วันละ 2 ครั้ง หลังอาหาร", "duration_days": 30, "quantity": 60, "instructions": "เช้า-เย็น", "unit_price": 2.0},
            {"drug_id": amlodipine["id"], "drug_name": amlodipine["name"], "strength": "5 mg", "dosage": "1 เม็ด", "frequency": "วันละ 1 ครั้ง เช้า", "duration_days": 30, "quantity": 30, "instructions": "", "unit_price": 3.0},
        ],
        "diagnosis": "เบาหวานชนิดที่ 2 และความดันโลหิตสูง",
        "notes": "",
        "status": "active",
        "issued_at": now_iso(),
        "dispensed_at": None,
        "dispensed_by_name": None,
        "created_at": now_iso(),
    }
    pres2 = {
        "id": str(uuid.uuid4()),
        "prescription_number": await next_number("prescription", "PRE"),
        "patient_id": patients[1]["id"],
        "patient_name": f"{patients[1]['first_name']} {patients[1]['last_name']}",
        "patient_number": patients[1]["patient_number"],
        "doctor_id": doctors[1]["id"] if len(doctors) > 1 else doctors[0]["id"],
        "doctor_name": doctors[1]["full_name"] if len(doctors) > 1 else doctors[0]["full_name"],
        "medications": [
            {"drug_id": para["id"], "drug_name": para["name"], "strength": "500 mg", "dosage": "1-2 เม็ด", "frequency": "ทุก 4-6 ชั่วโมง เมื่อมีอาการ", "duration_days": 5, "quantity": 20, "instructions": "ไม่เกินวันละ 8 เม็ด", "unit_price": 1.0},
        ],
        "diagnosis": "ไข้หวัด ปวดศีรษะ",
        "notes": "",
        "status": "dispensed",
        "issued_at": now_iso(),
        "dispensed_at": now_iso(),
        "dispensed_by": pharmacist["id"] if pharmacist else None,
        "dispensed_by_name": pharmacist["full_name"] if pharmacist else None,
        "created_at": now_iso(),
    }
    await db.prescriptions.insert_many([pres1, pres2])

    # Lab tests
    lab1 = {
        "id": str(uuid.uuid4()),
        "test_number": await next_number("lab_test", "LAB"),
        "patient_id": patients[0]["id"],
        "patient_name": f"{patients[0]['first_name']} {patients[0]['last_name']}",
        "patient_number": patients[0]["patient_number"],
        "doctor_id": doctors[0]["id"], "doctor_name": doctors[0]["full_name"],
        "test_type": "CBC (Complete Blood Count)", "test_category": "blood", "price": 250,
        "priority": "routine", "clinical_notes": "ตรวจสุขภาพประจำปี",
        "status": "ordered", "sample": None, "results": None,
        "ordered_at": now_iso(), "created_at": now_iso(),
    }
    lab2 = {
        "id": str(uuid.uuid4()),
        "test_number": await next_number("lab_test", "LAB"),
        "patient_id": patients[2]["id"],
        "patient_name": f"{patients[2]['first_name']} {patients[2]['last_name']}",
        "patient_number": patients[2]["patient_number"],
        "doctor_id": doctors[0]["id"], "doctor_name": doctors[0]["full_name"],
        "test_type": "FBS (Fasting Blood Sugar)", "test_category": "blood", "price": 80,
        "priority": "urgent", "clinical_notes": "ติดตามเบาหวาน",
        "status": "sample_collected",
        "sample": {"sample_id": await next_number("sample", "SMP"), "collected_at": now_iso(), "collected_by": lab_tech["full_name"] if lab_tech else "เจ้าหน้าที่"},
        "results": None,
        "ordered_at": now_iso(), "created_at": now_iso(),
    }
    lab3 = {
        "id": str(uuid.uuid4()),
        "test_number": await next_number("lab_test", "LAB"),
        "patient_id": patients[3]["id"],
        "patient_name": f"{patients[3]['first_name']} {patients[3]['last_name']}",
        "patient_number": patients[3]["patient_number"],
        "doctor_id": doctors[0]["id"], "doctor_name": doctors[0]["full_name"],
        "test_type": "Lipid Profile", "test_category": "blood", "price": 350,
        "priority": "routine", "clinical_notes": "ติดตามไขมันในเลือด",
        "status": "completed",
        "sample": {"sample_id": await next_number("sample", "SMP"), "collected_at": now_iso(), "collected_by": lab_tech["full_name"] if lab_tech else "เจ้าหน้าที่"},
        "results": {
            "parameters": [
                {"name": "Total Cholesterol", "value": "215", "unit": "mg/dL", "reference_range": "0.0 - 200.0", "is_abnormal": True},
                {"name": "Triglyceride", "value": "140", "unit": "mg/dL", "reference_range": "0.0 - 150.0", "is_abnormal": False},
                {"name": "HDL", "value": "52", "unit": "mg/dL", "reference_range": "40.0 - 100.0", "is_abnormal": False},
                {"name": "LDL", "value": "148", "unit": "mg/dL", "reference_range": "0.0 - 130.0", "is_abnormal": True},
            ],
            "interpretation": "ไขมันรวมและ LDL สูงกว่าค่าอ้างอิง ควรควบคุมอาหารและติดตามผล",
            "notes": "",
            "has_abnormal": True,
        },
        "performed_by": lab_tech["full_name"] if lab_tech else "เจ้าหน้าที่",
        "performed_at": now_iso(),
        "ordered_at": now_iso(), "created_at": now_iso(),
    }
    await db.lab_tests.insert_many([lab1, lab2, lab3])

    # Invoices
    today = now.strftime("%Y-%m-%d")
    inv1_total = 500.0
    inv1 = {
        "id": str(uuid.uuid4()),
        "invoice_number": await next_number("invoice", "INV"),
        "patient_id": patients[3]["id"],
        "patient_name": f"{patients[3]['first_name']} {patients[3]['last_name']}",
        "patient_number": patients[3]["patient_number"],
        "line_items": [{"item_type": "consultation", "description": "ค่าตรวจรักษา (อายุรกรรม)", "quantity": 1, "unit_price": 500.0, "total": 500.0}],
        "subtotal": inv1_total, "discount": 0, "tax": 0, "total_amount": inv1_total,
        "paid_amount": inv1_total, "balance": 0.0, "status": "paid",
        "payments": [{"id": str(uuid.uuid4()), "amount": inv1_total, "method": "cash", "reference": "", "paid_at": now_iso(), "received_by": finance["full_name"] if finance else "การเงิน"}],
        "insurance_claim": None,
        "invoice_date": today, "due_date": today, "notes": "",
        "created_by": finance["id"] if finance else None, "created_at": now_iso(),
    }
    inv2 = {
        "id": str(uuid.uuid4()),
        "invoice_number": await next_number("invoice", "INV"),
        "patient_id": patients[2]["id"],
        "patient_name": f"{patients[2]['first_name']} {patients[2]['last_name']}",
        "patient_number": patients[2]["patient_number"],
        "line_items": [
            {"item_type": "consultation", "description": "ค่าตรวจรักษา", "quantity": 1, "unit_price": 500.0, "total": 500.0},
            {"item_type": "lab", "description": "FBS (Fasting Blood Sugar)", "quantity": 1, "unit_price": 80.0, "total": 80.0},
            {"item_type": "pharmacy", "description": "Metformin 500 mg x60, Amlodipine 5 mg x30", "quantity": 1, "unit_price": 210.0, "total": 210.0},
        ],
        "subtotal": 790.0, "discount": 0, "tax": 0, "total_amount": 790.0,
        "paid_amount": 0.0, "balance": 790.0, "status": "pending",
        "payments": [], "insurance_claim": None,
        "invoice_date": today, "due_date": today, "notes": "",
        "created_by": finance["id"] if finance else None, "created_at": now_iso(),
    }
    inv3 = {
        "id": str(uuid.uuid4()),
        "invoice_number": await next_number("invoice", "INV"),
        "patient_id": patients[1]["id"],
        "patient_name": f"{patients[1]['first_name']} {patients[1]['last_name']}",
        "patient_number": patients[1]["patient_number"],
        "line_items": [
            {"item_type": "consultation", "description": "ค่าตรวจรักษา", "quantity": 1, "unit_price": 800.0, "total": 800.0},
            {"item_type": "lab", "description": "CBC (Complete Blood Count)", "quantity": 1, "unit_price": 250.0, "total": 250.0},
        ],
        "subtotal": 1050.0, "discount": 50.0, "tax": 0, "total_amount": 1000.0,
        "paid_amount": 400.0, "balance": 600.0, "status": "partially_paid",
        "payments": [{"id": str(uuid.uuid4()), "amount": 400.0, "method": "card", "reference": "TXN-001234", "paid_at": now_iso(), "received_by": finance["full_name"] if finance else "การเงิน"}],
        "insurance_claim": {"claim_id": await next_number("claim", "CLM"), "provider": "ประกันสังคม", "claim_amount": 600.0, "approved_amount": 0, "status": "submitted", "submitted_at": now_iso()},
        "invoice_date": today, "due_date": today, "notes": "",
        "created_by": finance["id"] if finance else None, "created_at": now_iso(),
    }
    await db.invoices.insert_many([inv1, inv2, inv3])
    logger.info("Clinical seed data created (drugs, prescriptions, lab tests, invoices)")


async def create_indexes():
    await db.users.create_index("email", unique=True)
    await db.users.create_index("id")
    await db.patients.create_index("id")
    await db.patients.create_index("patient_number")
    await db.appointments.create_index("id")
    await db.appointments.create_index([("appointment_date", 1), ("doctor_id", 1)])
    await db.login_attempts.create_index("identifier")
    await db.audit_logs.create_index("timestamp")
    await db.drugs.create_index("id")
    await db.drugs.create_index("drug_code")
    await db.prescriptions.create_index("id")
    await db.prescriptions.create_index([("status", 1), ("created_at", -1)])
    await db.lab_tests.create_index("id")
    await db.lab_tests.create_index([("status", 1), ("created_at", -1)])
    await db.invoices.create_index("id")
    await db.invoices.create_index([("status", 1), ("created_at", -1)])


async def seed_all():
    await create_indexes()
    await seed_admin()
    await seed_staff()
    await seed_patients_and_appointments()
    await seed_clinical()
