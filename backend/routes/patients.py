import re
import uuid

from fastapi import APIRouter, Depends, HTTPException, Query

from core.database import db
from core.security import STAFF_ROLES, require_roles
from core.utils import audit_log, next_number, now_iso
from models.schemas import PatientCreate, PatientUpdate, VitalsCreate

router = APIRouter(prefix="/patients", tags=["patients"])

WRITE_ROLES = ("admin", "doctor", "nurse")


@router.post("", status_code=201)
async def create_patient(body: PatientCreate, user: dict = Depends(require_roles(*WRITE_ROLES))):
    if body.national_id:
        existing = await db.patients.find_one({"national_id": body.national_id, "is_active": True})
        if existing:
            raise HTTPException(status_code=409, detail="มีผู้ป่วยที่ใช้เลขบัตรประชาชนนี้อยู่แล้ว")
    patient = {
        "id": str(uuid.uuid4()),
        "patient_number": await next_number("patient", "PAT"),
        **body.model_dump(),
        "vitals": [],
        "is_active": True,
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "created_by": user["id"],
    }
    await db.patients.insert_one(patient)
    await audit_log(user, "create", "patient", patient["id"], patient["patient_number"])
    patient.pop("_id", None)
    return patient


@router.get("")
async def list_patients(
    search: str = "",
    gender: str = "",
    blood_type: str = "",
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    user: dict = Depends(require_roles(*STAFF_ROLES)),
):
    query = {"is_active": True}
    if search:
        safe = re.escape(search)
        query["$or"] = [
            {"first_name": {"$regex": safe, "$options": "i"}},
            {"last_name": {"$regex": safe, "$options": "i"}},
            {"patient_number": {"$regex": safe, "$options": "i"}},
            {"phone": {"$regex": safe, "$options": "i"}},
            {"national_id": {"$regex": safe, "$options": "i"}},
        ]
    if gender:
        query["gender"] = gender
    if blood_type:
        query["blood_type"] = blood_type
    total = await db.patients.count_documents(query)
    items = (
        await db.patients.find(query, {"_id": 0})
        .sort("created_at", -1)
        .skip((page - 1) * limit)
        .limit(limit)
        .to_list(limit)
    )
    return {"items": items, "total": total, "page": page, "pages": max(1, -(-total // limit))}


@router.get("/{patient_id}")
async def get_patient(patient_id: str, user: dict = Depends(require_roles(*STAFF_ROLES))):
    patient = await db.patients.find_one({"id": patient_id}, {"_id": 0})
    if not patient:
        raise HTTPException(status_code=404, detail="ไม่พบข้อมูลผู้ป่วย")
    return patient


@router.put("/{patient_id}")
async def update_patient(patient_id: str, body: PatientUpdate, user: dict = Depends(require_roles(*WRITE_ROLES))):
    updates = {k: v for k, v in body.model_dump(exclude_unset=True).items() if v is not None}
    if not updates:
        raise HTTPException(status_code=400, detail="ไม่มีข้อมูลที่ต้องการแก้ไข")
    updates["updated_at"] = now_iso()
    result = await db.patients.update_one({"id": patient_id}, {"$set": updates})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="ไม่พบข้อมูลผู้ป่วย")
    await audit_log(user, "update", "patient", patient_id)
    return await db.patients.find_one({"id": patient_id}, {"_id": 0})


@router.delete("/{patient_id}")
async def delete_patient(patient_id: str, user: dict = Depends(require_roles("admin"))):
    result = await db.patients.update_one(
        {"id": patient_id}, {"$set": {"is_active": False, "updated_at": now_iso()}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="ไม่พบข้อมูลผู้ป่วย")
    await audit_log(user, "delete", "patient", patient_id)
    return {"message": "ลบข้อมูลผู้ป่วยสำเร็จ"}


@router.post("/{patient_id}/vitals", status_code=201)
async def add_vitals(patient_id: str, body: VitalsCreate, user: dict = Depends(require_roles(*WRITE_ROLES))):
    vitals = {
        "id": str(uuid.uuid4()),
        **body.model_dump(),
        "recorded_at": now_iso(),
        "recorded_by": user["full_name"],
    }
    result = await db.patients.update_one(
        {"id": patient_id},
        {"$push": {"vitals": vitals}, "$set": {"updated_at": now_iso()}},
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="ไม่พบข้อมูลผู้ป่วย")
    await audit_log(user, "create", "vitals", patient_id)
    return vitals
