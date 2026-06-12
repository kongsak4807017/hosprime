import uuid

from fastapi import APIRouter, Depends, HTTPException, Query

from core.database import db
from core.security import STAFF_ROLES, require_roles
from core.utils import audit_log, next_number, now_iso
from models.schemas import APPOINTMENT_STATUSES, AppointmentCreate, AppointmentUpdate, StatusUpdate

router = APIRouter(prefix="/appointments", tags=["appointments"])

WRITE_ROLES = ("admin", "doctor", "nurse")


@router.get("/doctors")
async def list_doctors(user: dict = Depends(require_roles(*STAFF_ROLES))):
    doctors = await db.users.find(
        {"role": "doctor", "is_active": True},
        {"_id": 0, "id": 1, "full_name": 1, "department": 1, "specialization": 1},
    ).to_list(200)
    return doctors


@router.post("", status_code=201)
async def create_appointment(body: AppointmentCreate, user: dict = Depends(require_roles(*WRITE_ROLES))):
    patient = await db.patients.find_one({"id": body.patient_id}, {"_id": 0})
    if not patient:
        raise HTTPException(status_code=404, detail="ไม่พบข้อมูลผู้ป่วย")
    doctor = await db.users.find_one({"id": body.doctor_id, "role": "doctor"}, {"_id": 0})
    if not doctor:
        raise HTTPException(status_code=404, detail="ไม่พบข้อมูลแพทย์")

    conflict = await db.appointments.find_one({
        "doctor_id": body.doctor_id,
        "appointment_date": body.appointment_date,
        "appointment_time": body.appointment_time,
        "status": {"$nin": ["cancelled", "no_show"]},
    })
    if conflict:
        raise HTTPException(status_code=409, detail="แพทย์มีนัดหมายในช่วงเวลานี้แล้ว")

    appointment = {
        "id": str(uuid.uuid4()),
        "appointment_number": await next_number("appointment", "APT"),
        **body.model_dump(),
        "patient_name": f"{patient['first_name']} {patient['last_name']}",
        "patient_number": patient["patient_number"],
        "doctor_name": doctor["full_name"],
        "status": "scheduled",
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "created_by": user["id"],
    }
    await db.appointments.insert_one(appointment)
    await audit_log(user, "create", "appointment", appointment["id"], appointment["appointment_number"])
    appointment.pop("_id", None)
    return appointment


@router.get("")
async def list_appointments(
    date: str = "",
    doctor_id: str = "",
    patient_id: str = "",
    status: str = "",
    search: str = "",
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    user: dict = Depends(require_roles(*STAFF_ROLES)),
):
    query = {}
    if date:
        query["appointment_date"] = date
    if doctor_id:
        query["doctor_id"] = doctor_id
    if patient_id:
        query["patient_id"] = patient_id
    if status:
        query["status"] = status
    if search:
        query["$or"] = [
            {"patient_name": {"$regex": search, "$options": "i"}},
            {"appointment_number": {"$regex": search, "$options": "i"}},
            {"doctor_name": {"$regex": search, "$options": "i"}},
        ]
    total = await db.appointments.count_documents(query)
    items = (
        await db.appointments.find(query, {"_id": 0})
        .sort([("appointment_date", -1), ("appointment_time", 1)])
        .skip((page - 1) * limit)
        .limit(limit)
        .to_list(limit)
    )
    return {"items": items, "total": total, "page": page, "pages": max(1, -(-total // limit))}


@router.get("/{appointment_id}")
async def get_appointment(appointment_id: str, user: dict = Depends(require_roles(*STAFF_ROLES))):
    appointment = await db.appointments.find_one({"id": appointment_id}, {"_id": 0})
    if not appointment:
        raise HTTPException(status_code=404, detail="ไม่พบข้อมูลนัดหมาย")
    return appointment


@router.put("/{appointment_id}")
async def update_appointment(appointment_id: str, body: AppointmentUpdate, user: dict = Depends(require_roles(*WRITE_ROLES))):
    updates = {k: v for k, v in body.model_dump(exclude_unset=True).items() if v is not None}
    if not updates:
        raise HTTPException(status_code=400, detail="ไม่มีข้อมูลที่ต้องการแก้ไข")
    if "doctor_id" in updates:
        doctor = await db.users.find_one({"id": updates["doctor_id"], "role": "doctor"}, {"_id": 0})
        if not doctor:
            raise HTTPException(status_code=404, detail="ไม่พบข้อมูลแพทย์")
        updates["doctor_name"] = doctor["full_name"]
    updates["updated_at"] = now_iso()
    result = await db.appointments.update_one({"id": appointment_id}, {"$set": updates})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="ไม่พบข้อมูลนัดหมาย")
    await audit_log(user, "update", "appointment", appointment_id)
    return await db.appointments.find_one({"id": appointment_id}, {"_id": 0})


@router.patch("/{appointment_id}/status")
async def update_status(appointment_id: str, body: StatusUpdate, user: dict = Depends(require_roles(*WRITE_ROLES))):
    if body.status not in APPOINTMENT_STATUSES:
        raise HTTPException(status_code=400, detail=f"สถานะไม่ถูกต้อง: {body.status}")
    updates = {"status": body.status, "updated_at": now_iso()}
    if body.status == "checked_in":
        updates["checked_in_at"] = now_iso()
    elif body.status == "completed":
        updates["completed_at"] = now_iso()
    elif body.status == "cancelled":
        updates["cancelled_at"] = now_iso()
    result = await db.appointments.update_one({"id": appointment_id}, {"$set": updates})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="ไม่พบข้อมูลนัดหมาย")
    await audit_log(user, "update_status", "appointment", appointment_id, body.status)
    return await db.appointments.find_one({"id": appointment_id}, {"_id": 0})
