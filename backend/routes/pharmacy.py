import re
import uuid
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, Query

from core.database import db
from core.security import STAFF_ROLES, require_roles
from core.utils import audit_log, next_number, now_iso
from models.clinical import DrugCreate, DrugUpdate, PrescriptionCreate, StockAdjust

router = APIRouter(prefix="/pharmacy", tags=["pharmacy"])

DRUG_WRITE = ("admin", "pharmacist")
PRESCRIBE = ("admin", "doctor")
DISPENSE = ("admin", "pharmacist")

EXPIRY_HORIZON_DAYS = 90


def _expiry_horizon() -> str:
    return (datetime.now(timezone.utc) + timedelta(days=EXPIRY_HORIZON_DAYS)).strftime("%Y-%m-%d")


# ---------- Drugs (Inventory) ----------

@router.post("/drugs", status_code=201)
async def create_drug(body: DrugCreate, user: dict = Depends(require_roles(*DRUG_WRITE))):
    drug = {
        "id": str(uuid.uuid4()),
        "drug_code": await next_number("drug", "DRG"),
        **body.model_dump(),
        "is_active": True,
        "created_at": now_iso(),
        "updated_at": now_iso(),
    }
    await db.drugs.insert_one(drug)
    await audit_log(user, "create", "drug", drug["id"], drug["drug_code"])
    drug.pop("_id", None)
    return drug


@router.get("/drugs")
async def list_drugs(
    search: str = "",
    category: str = "",
    low_stock: bool = False,
    expiring: bool = False,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    user: dict = Depends(require_roles(*STAFF_ROLES)),
):
    query = {"is_active": True}
    if search:
        safe = re.escape(search)
        query["$or"] = [
            {"name": {"$regex": safe, "$options": "i"}},
            {"generic_name": {"$regex": safe, "$options": "i"}},
            {"drug_code": {"$regex": safe, "$options": "i"}},
        ]
    if category:
        query["category"] = category
    if low_stock:
        query["$expr"] = {"$lte": ["$quantity_in_stock", "$reorder_level"]}
    if expiring:
        query["batches"] = {"$elemMatch": {"expiry_date": {"$lte": _expiry_horizon()}, "quantity": {"$gt": 0}}}
    total = await db.drugs.count_documents(query)
    items = (
        await db.drugs.find(query, {"_id": 0})
        .sort("name", 1)
        .skip((page - 1) * limit)
        .limit(limit)
        .to_list(limit)
    )
    return {"items": items, "total": total, "page": page, "pages": max(1, -(-total // limit))}


@router.get("/alerts")
async def pharmacy_alerts(user: dict = Depends(require_roles(*STAFF_ROLES))):
    low_stock = await db.drugs.find(
        {"is_active": True, "$expr": {"$lte": ["$quantity_in_stock", "$reorder_level"]}},
        {"_id": 0},
    ).to_list(200)
    expiring = await db.drugs.find(
        {"is_active": True, "batches": {"$elemMatch": {"expiry_date": {"$lte": _expiry_horizon()}, "quantity": {"$gt": 0}}}},
        {"_id": 0},
    ).to_list(200)
    return {"low_stock": low_stock, "expiring": expiring, "horizon_days": EXPIRY_HORIZON_DAYS}


@router.get("/drugs/{drug_id}")
async def get_drug(drug_id: str, user: dict = Depends(require_roles(*STAFF_ROLES))):
    drug = await db.drugs.find_one({"id": drug_id}, {"_id": 0})
    if not drug:
        raise HTTPException(status_code=404, detail="ไม่พบข้อมูลยา")
    return drug


@router.put("/drugs/{drug_id}")
async def update_drug(drug_id: str, body: DrugUpdate, user: dict = Depends(require_roles(*DRUG_WRITE))):
    updates = {k: v for k, v in body.model_dump(exclude_unset=True).items() if v is not None}
    if not updates:
        raise HTTPException(status_code=400, detail="ไม่มีข้อมูลที่ต้องการแก้ไข")
    updates["updated_at"] = now_iso()
    result = await db.drugs.update_one({"id": drug_id}, {"$set": updates})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="ไม่พบข้อมูลยา")
    await audit_log(user, "update", "drug", drug_id)
    return await db.drugs.find_one({"id": drug_id}, {"_id": 0})


@router.delete("/drugs/{drug_id}")
async def delete_drug(drug_id: str, user: dict = Depends(require_roles("admin"))):
    result = await db.drugs.update_one({"id": drug_id}, {"$set": {"is_active": False, "updated_at": now_iso()}})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="ไม่พบข้อมูลยา")
    await audit_log(user, "delete", "drug", drug_id)
    return {"message": "ลบข้อมูลยาสำเร็จ"}


@router.post("/drugs/{drug_id}/stock")
async def adjust_stock(drug_id: str, body: StockAdjust, user: dict = Depends(require_roles(*DRUG_WRITE))):
    drug = await db.drugs.find_one({"id": drug_id}, {"_id": 0})
    if not drug:
        raise HTTPException(status_code=404, detail="ไม่พบข้อมูลยา")
    new_qty = drug["quantity_in_stock"] + body.quantity_change
    if new_qty < 0:
        raise HTTPException(status_code=400, detail="จำนวนสต็อกไม่เพียงพอสำหรับการปรับลด")
    updates = {"quantity_in_stock": new_qty, "updated_at": now_iso()}
    ops = {"$set": updates}
    if body.quantity_change > 0 and body.batch_number:
        ops["$push"] = {"batches": {
            "batch_number": body.batch_number,
            "expiry_date": body.expiry_date or "",
            "quantity": body.quantity_change,
        }}
    await db.drugs.update_one({"id": drug_id}, ops)
    await audit_log(user, "stock_adjust", "drug", drug_id, f"{body.quantity_change:+d} ({body.note})")
    return await db.drugs.find_one({"id": drug_id}, {"_id": 0})


# ---------- Prescriptions ----------

@router.post("/prescriptions", status_code=201)
async def create_prescription(body: PrescriptionCreate, user: dict = Depends(require_roles(*PRESCRIBE))):
    patient = await db.patients.find_one({"id": body.patient_id}, {"_id": 0})
    if not patient:
        raise HTTPException(status_code=404, detail="ไม่พบข้อมูลผู้ป่วย")
    medications = []
    for med in body.medications:
        drug = await db.drugs.find_one({"id": med.drug_id, "is_active": True}, {"_id": 0})
        if not drug:
            raise HTTPException(status_code=404, detail=f"ไม่พบยาในคลัง (id: {med.drug_id})")
        medications.append({
            **med.model_dump(),
            "drug_name": drug["name"],
            "strength": drug.get("strength", ""),
            "unit_price": drug.get("selling_price", 0),
        })
    prescription = {
        "id": str(uuid.uuid4()),
        "prescription_number": await next_number("prescription", "PRE"),
        "patient_id": patient["id"],
        "patient_name": f"{patient['first_name']} {patient['last_name']}",
        "patient_number": patient["patient_number"],
        "doctor_id": user["id"],
        "doctor_name": user["full_name"],
        "medications": medications,
        "diagnosis": body.diagnosis,
        "notes": body.notes,
        "status": "active",
        "issued_at": now_iso(),
        "dispensed_at": None,
        "dispensed_by_name": None,
        "created_at": now_iso(),
    }
    await db.prescriptions.insert_one(prescription)
    await audit_log(user, "create", "prescription", prescription["id"], prescription["prescription_number"])
    prescription.pop("_id", None)
    return prescription


@router.get("/prescriptions")
async def list_prescriptions(
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
            {"prescription_number": {"$regex": safe, "$options": "i"}},
            {"doctor_name": {"$regex": safe, "$options": "i"}},
        ]
    total = await db.prescriptions.count_documents(query)
    items = (
        await db.prescriptions.find(query, {"_id": 0})
        .sort("created_at", -1)
        .skip((page - 1) * limit)
        .limit(limit)
        .to_list(limit)
    )
    return {"items": items, "total": total, "page": page, "pages": max(1, -(-total // limit))}


@router.get("/prescriptions/{prescription_id}")
async def get_prescription(prescription_id: str, user: dict = Depends(require_roles(*STAFF_ROLES))):
    pres = await db.prescriptions.find_one({"id": prescription_id}, {"_id": 0})
    if not pres:
        raise HTTPException(status_code=404, detail="ไม่พบใบสั่งยา")
    return pres


@router.post("/prescriptions/{prescription_id}/dispense")
async def dispense_prescription(prescription_id: str, user: dict = Depends(require_roles(*DISPENSE))):
    pres = await db.prescriptions.find_one({"id": prescription_id}, {"_id": 0})
    if not pres:
        raise HTTPException(status_code=404, detail="ไม่พบใบสั่งยา")
    if pres["status"] != "active":
        raise HTTPException(status_code=400, detail="ใบสั่งยานี้ถูกจ่ายยาหรือยกเลิกไปแล้ว")
    # Verify stock for all medications first
    for med in pres["medications"]:
        drug = await db.drugs.find_one({"id": med["drug_id"]}, {"_id": 0})
        if not drug or drug["quantity_in_stock"] < med["quantity"]:
            available = drug["quantity_in_stock"] if drug else 0
            raise HTTPException(
                status_code=400,
                detail=f"ยา {med['drug_name']} ในคลังไม่เพียงพอ (ต้องการ {med['quantity']} มี {available})",
            )
    # Deduct stock atomically (guard against concurrent dispensing)
    deducted = []
    for med in pres["medications"]:
        result = await db.drugs.update_one(
            {"id": med["drug_id"], "quantity_in_stock": {"$gte": med["quantity"]}},
            {"$inc": {"quantity_in_stock": -med["quantity"]}, "$set": {"updated_at": now_iso()}},
        )
        if result.modified_count == 0:
            # Roll back already-deducted items
            for d_id, qty in deducted:
                await db.drugs.update_one({"id": d_id}, {"$inc": {"quantity_in_stock": qty}})
            raise HTTPException(status_code=400, detail=f"ยา {med['drug_name']} ในคลังไม่เพียงพอ (สต็อกเปลี่ยนแปลงระหว่างจ่ายยา)")
        deducted.append((med["drug_id"], med["quantity"]))
    await db.prescriptions.update_one(
        {"id": prescription_id},
        {"$set": {
            "status": "dispensed",
            "dispensed_at": now_iso(),
            "dispensed_by": user["id"],
            "dispensed_by_name": user["full_name"],
        }},
    )
    await audit_log(user, "dispense", "prescription", prescription_id, pres["prescription_number"])
    return await db.prescriptions.find_one({"id": prescription_id}, {"_id": 0})


@router.post("/prescriptions/{prescription_id}/cancel")
async def cancel_prescription(prescription_id: str, user: dict = Depends(require_roles(*PRESCRIBE))):
    pres = await db.prescriptions.find_one({"id": prescription_id}, {"_id": 0})
    if not pres:
        raise HTTPException(status_code=404, detail="ไม่พบใบสั่งยา")
    if pres["status"] != "active":
        raise HTTPException(status_code=400, detail="ยกเลิกได้เฉพาะใบสั่งยาที่ยังไม่ถูกจ่าย")
    await db.prescriptions.update_one(
        {"id": prescription_id},
        {"$set": {"status": "cancelled", "cancelled_at": now_iso()}},
    )
    await audit_log(user, "cancel", "prescription", prescription_id)
    return await db.prescriptions.find_one({"id": prescription_id}, {"_id": 0})
