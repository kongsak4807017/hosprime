import re
import uuid

from fastapi import APIRouter, Depends, HTTPException, Query

from core.database import db
from core.security import STAFF_ROLES, require_roles
from core.utils import audit_log, next_number, now_iso
from models.clinical import LabOrderCreate, LabResultsSubmit

router = APIRouter(prefix="/lab", tags=["laboratory"])

ORDER_ROLES = ("admin", "doctor")
COLLECT_ROLES = ("admin", "lab_technician", "nurse")
RESULT_ROLES = ("admin", "lab_technician")

TEST_CATALOG = [
    {
        "test_type": "CBC (Complete Blood Count)", "test_category": "blood", "price": 250,
        "parameters": [
            {"name": "WBC", "unit": "x10³/µL", "ref_min": 4.0, "ref_max": 10.0},
            {"name": "RBC", "unit": "x10⁶/µL", "ref_min": 4.2, "ref_max": 5.9},
            {"name": "Hemoglobin", "unit": "g/dL", "ref_min": 12.0, "ref_max": 16.0},
            {"name": "Hematocrit", "unit": "%", "ref_min": 36.0, "ref_max": 48.0},
            {"name": "Platelets", "unit": "x10³/µL", "ref_min": 150.0, "ref_max": 400.0},
        ],
    },
    {
        "test_type": "FBS (Fasting Blood Sugar)", "test_category": "blood", "price": 80,
        "parameters": [{"name": "Glucose", "unit": "mg/dL", "ref_min": 70.0, "ref_max": 100.0}],
    },
    {
        "test_type": "Lipid Profile", "test_category": "blood", "price": 350,
        "parameters": [
            {"name": "Total Cholesterol", "unit": "mg/dL", "ref_min": 0.0, "ref_max": 200.0},
            {"name": "Triglyceride", "unit": "mg/dL", "ref_min": 0.0, "ref_max": 150.0},
            {"name": "HDL", "unit": "mg/dL", "ref_min": 40.0, "ref_max": 100.0},
            {"name": "LDL", "unit": "mg/dL", "ref_min": 0.0, "ref_max": 130.0},
        ],
    },
    {
        "test_type": "HbA1c", "test_category": "blood", "price": 300,
        "parameters": [{"name": "HbA1c", "unit": "%", "ref_min": 4.0, "ref_max": 5.6}],
    },
    {
        "test_type": "Liver Function Test (LFT)", "test_category": "blood", "price": 400,
        "parameters": [
            {"name": "AST", "unit": "U/L", "ref_min": 5.0, "ref_max": 40.0},
            {"name": "ALT", "unit": "U/L", "ref_min": 5.0, "ref_max": 40.0},
            {"name": "ALP", "unit": "U/L", "ref_min": 40.0, "ref_max": 120.0},
        ],
    },
    {
        "test_type": "Kidney Function (BUN/Cr)", "test_category": "blood", "price": 250,
        "parameters": [
            {"name": "BUN", "unit": "mg/dL", "ref_min": 7.0, "ref_max": 20.0},
            {"name": "Creatinine", "unit": "mg/dL", "ref_min": 0.6, "ref_max": 1.2},
        ],
    },
    {
        "test_type": "Urinalysis (UA)", "test_category": "urine", "price": 150,
        "parameters": [
            {"name": "pH", "unit": "", "ref_min": 4.6, "ref_max": 8.0},
            {"name": "Specific Gravity", "unit": "", "ref_min": 1.005, "ref_max": 1.03},
        ],
    },
    {
        "test_type": "Thyroid Function (TSH)", "test_category": "blood", "price": 450,
        "parameters": [{"name": "TSH", "unit": "mIU/L", "ref_min": 0.4, "ref_max": 4.0}],
    },
]

CATALOG_MAP = {t["test_type"]: t for t in TEST_CATALOG}


@router.get("/catalog")
async def get_catalog(user: dict = Depends(require_roles(*STAFF_ROLES))):
    return TEST_CATALOG


@router.post("/tests", status_code=201)
async def order_test(body: LabOrderCreate, user: dict = Depends(require_roles(*ORDER_ROLES))):
    patient = await db.patients.find_one({"id": body.patient_id}, {"_id": 0})
    if not patient:
        raise HTTPException(status_code=404, detail="ไม่พบข้อมูลผู้ป่วย")
    catalog = CATALOG_MAP.get(body.test_type)
    if not catalog:
        raise HTTPException(status_code=400, detail=f"ไม่พบรายการตรวจ: {body.test_type}")
    if body.priority not in ("routine", "urgent", "stat"):
        raise HTTPException(status_code=400, detail="ระดับความเร่งด่วนไม่ถูกต้อง")
    test = {
        "id": str(uuid.uuid4()),
        "test_number": await next_number("lab_test", "LAB"),
        "patient_id": patient["id"],
        "patient_name": f"{patient['first_name']} {patient['last_name']}",
        "patient_number": patient["patient_number"],
        "doctor_id": user["id"],
        "doctor_name": user["full_name"],
        "test_type": body.test_type,
        "test_category": catalog["test_category"],
        "price": catalog["price"],
        "priority": body.priority,
        "clinical_notes": body.clinical_notes,
        "status": "ordered",
        "sample": None,
        "results": None,
        "ordered_at": now_iso(),
        "created_at": now_iso(),
    }
    await db.lab_tests.insert_one(test)
    await audit_log(user, "create", "lab_test", test["id"], test["test_number"])
    test.pop("_id", None)
    return test


@router.get("/tests")
async def list_tests(
    status: str = "",
    patient_id: str = "",
    search: str = "",
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    user: dict = Depends(require_roles(*STAFF_ROLES)),
):
    query = {}
    if status:
        query["status"] = status
    if patient_id:
        query["patient_id"] = patient_id
    if search:
        safe = re.escape(search)
        query["$or"] = [
            {"patient_name": {"$regex": safe, "$options": "i"}},
            {"test_number": {"$regex": safe, "$options": "i"}},
            {"test_type": {"$regex": safe, "$options": "i"}},
        ]
    total = await db.lab_tests.count_documents(query)
    items = (
        await db.lab_tests.find(query, {"_id": 0})
        .sort("created_at", -1)
        .skip((page - 1) * limit)
        .limit(limit)
        .to_list(limit)
    )
    return {"items": items, "total": total, "page": page, "pages": max(1, -(-total // limit))}


@router.get("/tests/{test_id}")
async def get_test(test_id: str, user: dict = Depends(require_roles(*STAFF_ROLES))):
    test = await db.lab_tests.find_one({"id": test_id}, {"_id": 0})
    if not test:
        raise HTTPException(status_code=404, detail="ไม่พบรายการตรวจ")
    return test


@router.post("/tests/{test_id}/collect")
async def collect_sample(test_id: str, user: dict = Depends(require_roles(*COLLECT_ROLES))):
    test = await db.lab_tests.find_one({"id": test_id}, {"_id": 0})
    if not test:
        raise HTTPException(status_code=404, detail="ไม่พบรายการตรวจ")
    if test["status"] != "ordered":
        raise HTTPException(status_code=400, detail="เก็บตัวอย่างได้เฉพาะรายการที่สถานะ 'สั่งตรวจแล้ว'")
    sample = {
        "sample_id": await next_number("sample", "SMP"),
        "collected_at": now_iso(),
        "collected_by": user["full_name"],
    }
    await db.lab_tests.update_one(
        {"id": test_id},
        {"$set": {"status": "sample_collected", "sample": sample}},
    )
    await audit_log(user, "collect_sample", "lab_test", test_id, sample["sample_id"])
    return await db.lab_tests.find_one({"id": test_id}, {"_id": 0})


@router.post("/tests/{test_id}/results")
async def submit_results(test_id: str, body: LabResultsSubmit, user: dict = Depends(require_roles(*RESULT_ROLES))):
    test = await db.lab_tests.find_one({"id": test_id}, {"_id": 0})
    if not test:
        raise HTTPException(status_code=404, detail="ไม่พบรายการตรวจ")
    if test["status"] not in ("sample_collected", "in_progress"):
        raise HTTPException(status_code=400, detail="บันทึกผลได้เฉพาะรายการที่เก็บตัวอย่างแล้ว")
    catalog = CATALOG_MAP.get(test["test_type"], {"parameters": []})
    param_refs = {p["name"]: p for p in catalog["parameters"]}
    parameters = []
    has_abnormal = False
    for pv in body.parameters:
        ref = param_refs.get(pv.name)
        if param_refs and not ref:
            raise HTTPException(status_code=400, detail=f"ไม่พบพารามิเตอร์ '{pv.name}' ในรายการตรวจนี้")
        is_abnormal = False
        reference_range = ""
        unit = ""
        if ref:
            unit = ref["unit"]
            reference_range = f"{ref['ref_min']} - {ref['ref_max']}"
            try:
                val = float(pv.value)
                is_abnormal = val < ref["ref_min"] or val > ref["ref_max"]
            except (ValueError, TypeError):
                is_abnormal = False
        has_abnormal = has_abnormal or is_abnormal
        parameters.append({
            "name": pv.name,
            "value": pv.value,
            "unit": unit,
            "reference_range": reference_range,
            "is_abnormal": is_abnormal,
        })
    results = {
        "parameters": parameters,
        "interpretation": body.interpretation,
        "notes": body.notes,
        "has_abnormal": has_abnormal,
    }
    await db.lab_tests.update_one(
        {"id": test_id},
        {"$set": {
            "status": "completed",
            "results": results,
            "performed_by": user["full_name"],
            "performed_at": now_iso(),
        }},
    )
    await audit_log(user, "submit_results", "lab_test", test_id, test["test_number"])
    return await db.lab_tests.find_one({"id": test_id}, {"_id": 0})


@router.post("/tests/{test_id}/cancel")
async def cancel_test(test_id: str, user: dict = Depends(require_roles(*ORDER_ROLES))):
    test = await db.lab_tests.find_one({"id": test_id}, {"_id": 0})
    if not test:
        raise HTTPException(status_code=404, detail="ไม่พบรายการตรวจ")
    if test["status"] in ("completed", "cancelled"):
        raise HTTPException(status_code=400, detail="ไม่สามารถยกเลิกรายการที่เสร็จสิ้นหรือถูกยกเลิกแล้ว")
    await db.lab_tests.update_one(
        {"id": test_id},
        {"$set": {"status": "cancelled", "cancelled_at": now_iso()}},
    )
    await audit_log(user, "cancel", "lab_test", test_id)
    return await db.lab_tests.find_one({"id": test_id}, {"_id": 0})
