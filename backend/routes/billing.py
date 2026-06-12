import re
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query

from core.database import db
from core.security import STAFF_ROLES, require_roles
from core.utils import audit_log, next_number, now_iso
from models.clinical import ClaimCreate, ClaimUpdate, InvoiceCreate, PaymentCreate

router = APIRouter(prefix="/billing", tags=["billing"])

BILLING_WRITE = ("admin", "finance")

PAYMENT_METHODS = ("cash", "card", "transfer", "insurance")
CLAIM_STATUSES = ("submitted", "approved", "rejected", "partially_approved")


def _invoice_status(total: float, paid: float) -> str:
    if paid <= 0:
        return "pending"
    if paid >= total - 0.001:
        return "paid"
    return "partially_paid"


@router.post("/invoices", status_code=201)
async def create_invoice(body: InvoiceCreate, user: dict = Depends(require_roles(*BILLING_WRITE))):
    patient = await db.patients.find_one({"id": body.patient_id}, {"_id": 0})
    if not patient:
        raise HTTPException(status_code=404, detail="ไม่พบข้อมูลผู้ป่วย")
    line_items = []
    subtotal = 0.0
    for item in body.line_items:
        total = round(item.quantity * item.unit_price, 2)
        subtotal += total
        line_items.append({**item.model_dump(), "total": total})
    total_amount = round(subtotal - body.discount + body.tax, 2)
    if total_amount < 0:
        raise HTTPException(status_code=400, detail="ยอดรวมต้องไม่ติดลบ")
    invoice = {
        "id": str(uuid.uuid4()),
        "invoice_number": await next_number("invoice", "INV"),
        "patient_id": patient["id"],
        "patient_name": f"{patient['first_name']} {patient['last_name']}",
        "patient_number": patient["patient_number"],
        "line_items": line_items,
        "subtotal": round(subtotal, 2),
        "discount": body.discount,
        "tax": body.tax,
        "total_amount": total_amount,
        "paid_amount": 0.0,
        "balance": total_amount,
        "status": "pending",
        "payments": [],
        "insurance_claim": None,
        "invoice_date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "due_date": body.due_date,
        "notes": body.notes,
        "created_by": user["id"],
        "created_at": now_iso(),
    }
    await db.invoices.insert_one(invoice)
    await audit_log(user, "create", "invoice", invoice["id"], invoice["invoice_number"])
    invoice.pop("_id", None)
    return invoice


@router.get("/invoices")
async def list_invoices(
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
            {"invoice_number": {"$regex": safe, "$options": "i"}},
        ]
    total = await db.invoices.count_documents(query)
    items = (
        await db.invoices.find(query, {"_id": 0})
        .sort("created_at", -1)
        .skip((page - 1) * limit)
        .limit(limit)
        .to_list(limit)
    )
    return {"items": items, "total": total, "page": page, "pages": max(1, -(-total // limit))}


@router.get("/stats")
async def billing_stats(user: dict = Depends(require_roles(*STAFF_ROLES))):
    now = datetime.now(timezone.utc)
    today_prefix = now.strftime("%Y-%m-%d")
    month_prefix = now.strftime("%Y-%m")
    agg = await db.invoices.aggregate([
        {"$unwind": "$payments"},
        {"$group": {
            "_id": None,
            "revenue_today": {"$sum": {"$cond": [
                {"$regexMatch": {"input": "$payments.paid_at", "regex": f"^{today_prefix}"}},
                "$payments.amount", 0,
            ]}},
            "revenue_month": {"$sum": {"$cond": [
                {"$regexMatch": {"input": "$payments.paid_at", "regex": f"^{month_prefix}"}},
                "$payments.amount", 0,
            ]}},
        }},
    ]).to_list(1)
    revenue_today = round(agg[0]["revenue_today"], 2) if agg else 0
    revenue_month = round(agg[0]["revenue_month"], 2) if agg else 0

    outstanding_agg = await db.invoices.aggregate([
        {"$match": {"status": {"$in": ["pending", "partially_paid"]}}},
        {"$group": {"_id": None, "outstanding": {"$sum": "$balance"}, "count": {"$sum": 1}}},
    ]).to_list(1)
    outstanding = round(outstanding_agg[0]["outstanding"], 2) if outstanding_agg else 0
    pending_count = outstanding_agg[0]["count"] if outstanding_agg else 0

    return {
        "revenue_today": revenue_today,
        "revenue_month": revenue_month,
        "outstanding": outstanding,
        "pending_invoices": pending_count,
    }


@router.get("/invoices/{invoice_id}")
async def get_invoice(invoice_id: str, user: dict = Depends(require_roles(*STAFF_ROLES))):
    invoice = await db.invoices.find_one({"id": invoice_id}, {"_id": 0})
    if not invoice:
        raise HTTPException(status_code=404, detail="ไม่พบใบแจ้งหนี้")
    return invoice


@router.post("/invoices/{invoice_id}/payments")
async def record_payment(invoice_id: str, body: PaymentCreate, user: dict = Depends(require_roles(*BILLING_WRITE))):
    invoice = await db.invoices.find_one({"id": invoice_id}, {"_id": 0})
    if not invoice:
        raise HTTPException(status_code=404, detail="ไม่พบใบแจ้งหนี้")
    if invoice["status"] in ("paid", "cancelled"):
        raise HTTPException(status_code=400, detail="ใบแจ้งหนี้นี้ชำระครบหรือถูกยกเลิกแล้ว")
    if body.method not in PAYMENT_METHODS:
        raise HTTPException(status_code=400, detail="วิธีชำระเงินไม่ถูกต้อง")
    if body.amount > invoice["balance"] + 0.001:
        raise HTTPException(status_code=400, detail=f"ยอดชำระเกินยอดค้าง (ค้างชำระ {invoice['balance']:.2f} บาท)")
    payment = {
        "id": str(uuid.uuid4()),
        "amount": round(body.amount, 2),
        "method": body.method,
        "reference": body.reference,
        "paid_at": now_iso(),
        "received_by": user["full_name"],
    }
    new_paid = round(invoice["paid_amount"] + payment["amount"], 2)
    new_balance = round(invoice["total_amount"] - new_paid, 2)
    await db.invoices.update_one(
        {"id": invoice_id},
        {
            "$push": {"payments": payment},
            "$set": {
                "paid_amount": new_paid,
                "balance": new_balance,
                "status": _invoice_status(invoice["total_amount"], new_paid),
            },
        },
    )
    await audit_log(user, "payment", "invoice", invoice_id, f"{payment['amount']} via {payment['method']}")
    return await db.invoices.find_one({"id": invoice_id}, {"_id": 0})


@router.post("/invoices/{invoice_id}/claim")
async def submit_claim(invoice_id: str, body: ClaimCreate, user: dict = Depends(require_roles(*BILLING_WRITE))):
    invoice = await db.invoices.find_one({"id": invoice_id}, {"_id": 0})
    if not invoice:
        raise HTTPException(status_code=404, detail="ไม่พบใบแจ้งหนี้")
    if invoice["status"] == "cancelled":
        raise HTTPException(status_code=400, detail="ใบแจ้งหนี้ถูกยกเลิกแล้ว")
    if invoice.get("insurance_claim"):
        raise HTTPException(status_code=400, detail="ใบแจ้งหนี้นี้มีการยื่นเคลมแล้ว")
    claim = {
        "claim_id": await next_number("claim", "CLM"),
        "provider": body.provider,
        "claim_amount": round(body.claim_amount, 2),
        "approved_amount": 0,
        "status": "submitted",
        "submitted_at": now_iso(),
    }
    await db.invoices.update_one({"id": invoice_id}, {"$set": {"insurance_claim": claim}})
    await audit_log(user, "submit_claim", "invoice", invoice_id, claim["claim_id"])
    return await db.invoices.find_one({"id": invoice_id}, {"_id": 0})


@router.patch("/invoices/{invoice_id}/claim")
async def update_claim(invoice_id: str, body: ClaimUpdate, user: dict = Depends(require_roles(*BILLING_WRITE))):
    invoice = await db.invoices.find_one({"id": invoice_id}, {"_id": 0})
    if not invoice:
        raise HTTPException(status_code=404, detail="ไม่พบใบแจ้งหนี้")
    if not invoice.get("insurance_claim"):
        raise HTTPException(status_code=400, detail="ใบแจ้งหนี้นี้ยังไม่มีการยื่นเคลม")
    if body.status not in CLAIM_STATUSES:
        raise HTTPException(status_code=400, detail=f"สถานะเคลมไม่ถูกต้อง: {body.status}")
    updates = {
        "insurance_claim.status": body.status,
        "insurance_claim.approved_amount": round(body.approved_amount, 2),
        "insurance_claim.updated_at": now_iso(),
    }
    await db.invoices.update_one({"id": invoice_id}, {"$set": updates})
    await audit_log(user, "update_claim", "invoice", invoice_id, body.status)
    return await db.invoices.find_one({"id": invoice_id}, {"_id": 0})


@router.post("/invoices/{invoice_id}/cancel")
async def cancel_invoice(invoice_id: str, user: dict = Depends(require_roles(*BILLING_WRITE))):
    invoice = await db.invoices.find_one({"id": invoice_id}, {"_id": 0})
    if not invoice:
        raise HTTPException(status_code=404, detail="ไม่พบใบแจ้งหนี้")
    if invoice["status"] == "paid":
        raise HTTPException(status_code=400, detail="ไม่สามารถยกเลิกใบแจ้งหนี้ที่ชำระครบแล้ว")
    if invoice["paid_amount"] > 0:
        raise HTTPException(status_code=400, detail="ไม่สามารถยกเลิกใบแจ้งหนี้ที่มีการชำระเงินแล้ว")
    await db.invoices.update_one(
        {"id": invoice_id},
        {"$set": {"status": "cancelled", "cancelled_at": now_iso()}},
    )
    await audit_log(user, "cancel", "invoice", invoice_id)
    return await db.invoices.find_one({"id": invoice_id}, {"_id": 0})
