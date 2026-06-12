import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from core.ai import chat_completion
from core.database import db
from core.security import STAFF_ROLES, require_roles
from core.utils import now_iso

router = APIRouter(prefix="/agents", tags=["digital-twin-agents"])


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None


# ---------- Live context builders per department head ----------

async def _ctx_director() -> str:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    total_patients = await db.patients.count_documents({"is_active": True})
    appts_today = await db.appointments.count_documents({"appointment_date": today})
    staff_count = await db.users.count_documents({"is_active": True, "role": {"$ne": "patient"}})
    outstanding = await db.invoices.aggregate([
        {"$match": {"status": {"$in": ["pending", "partially_paid"]}}},
        {"$group": {"_id": None, "sum": {"$sum": "$balance"}, "count": {"$sum": 1}}},
    ]).to_list(1)
    low_stock = await db.drugs.count_documents({"is_active": True, "$expr": {"$lte": ["$quantity_in_stock", "$reorder_level"]}})
    pending_lab = await db.lab_tests.count_documents({"status": {"$in": ["ordered", "sample_collected", "in_progress"]}})
    out_sum = outstanding[0]["sum"] if outstanding else 0
    out_count = outstanding[0]["count"] if outstanding else 0
    return (
        f"ผู้ป่วยทั้งหมด: {total_patients} ราย | นัดหมายวันนี้: {appts_today} | บุคลากร: {staff_count} คน\n"
        f"ยอดค้างชำระ: {out_sum:,.0f} บาท ({out_count} บิล) | ยาใกล้หมดสต็อก: {low_stock} รายการ | แล็บค้างดำเนินการ: {pending_lab} รายการ"
    )


async def _ctx_cmo() -> str:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    status_agg = await db.appointments.aggregate([
        {"$match": {"appointment_date": today}},
        {"$group": {"_id": "$status", "count": {"$sum": 1}}},
    ]).to_list(20)
    statuses = ", ".join(f"{i['_id']}: {i['count']}" for i in status_agg) or "ไม่มีนัดหมายวันนี้"
    abnormal = await db.lab_tests.find({"status": "completed", "results.has_abnormal": True}, {"_id": 0, "test_number": 1, "patient_name": 1, "test_type": 1}).sort("performed_at", -1).limit(5).to_list(5)
    abnormal_txt = "\n".join(f"- {t['test_number']} {t['patient_name']}: {t['test_type']}" for t in abnormal) or "ไม่มี"
    active_pres = await db.prescriptions.count_documents({"status": "active"})
    chronic = await db.patients.aggregate([
        {"$match": {"is_active": True}}, {"$unwind": "$chronic_conditions"},
        {"$group": {"_id": "$chronic_conditions.condition", "count": {"$sum": 1}}}, {"$sort": {"count": -1}}, {"$limit": 5},
    ]).to_list(5)
    chronic_txt = ", ".join(f"{c['_id']} ({c['count']})" for c in chronic) or "ไม่มีข้อมูล"
    return (
        f"นัดหมายวันนี้แยกสถานะ: {statuses}\n"
        f"ใบสั่งยารอจ่าย: {active_pres}\nโรคเรื้อรังที่พบบ่อย: {chronic_txt}\n"
        f"ผลแล็บผิดปกติล่าสุด:\n{abnormal_txt}"
    )


async def _ctx_head_nurse() -> str:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    queue = await db.appointments.find(
        {"appointment_date": today, "status": {"$nin": ["completed", "cancelled", "no_show"]}}, {"_id": 0}
    ).sort("appointment_time", 1).limit(10).to_list(10)
    queue_txt = "\n".join(f"- {a['appointment_time']} {a['patient_name']} ({a['doctor_name']}) สถานะ: {a['status']}" for a in queue) or "ไม่มีคิวค้าง"
    allergy_patients = await db.patients.count_documents({"is_active": True, "allergies.0": {"$exists": True}})
    return f"คิวผู้ป่วยวันนี้ที่ยังไม่เสร็จ:\n{queue_txt}\n\nผู้ป่วยที่มีประวัติแพ้ยาในระบบ: {allergy_patients} ราย (ต้องระวังเป็นพิเศษ)"


async def _ctx_head_pharmacy() -> str:
    low = await db.drugs.find({"is_active": True, "$expr": {"$lte": ["$quantity_in_stock", "$reorder_level"]}}, {"_id": 0}).to_list(20)
    low_txt = "\n".join(f"- {d['name']}: เหลือ {d['quantity_in_stock']} (จุดสั่งซื้อ {d['reorder_level']})" for d in low) or "ไม่มี"
    horizon = (datetime.now(timezone.utc) + timedelta(days=90)).strftime("%Y-%m-%d")
    expiring = await db.drugs.find({"is_active": True, "batches": {"$elemMatch": {"expiry_date": {"$lte": horizon}, "quantity": {"$gt": 0}}}}, {"_id": 0}).to_list(20)
    exp_txt = "\n".join(f"- {d['name']}: batch หมดอายุ {min(b['expiry_date'] for b in d['batches'] if b.get('expiry_date'))}" for d in expiring) or "ไม่มี"
    active = await db.prescriptions.find({"status": "active"}, {"_id": 0, "prescription_number": 1, "patient_name": 1, "medications": 1}).limit(10).to_list(10)
    active_txt = "\n".join(f"- {p['prescription_number']} {p['patient_name']}: {', '.join(m['drug_name'] for m in p['medications'])}" for p in active) or "ไม่มี"
    return f"ยาใกล้หมดสต็อก:\n{low_txt}\n\nยาใกล้หมดอายุ (90 วัน):\n{exp_txt}\n\nใบสั่งยารอจ่าย:\n{active_txt}"


async def _ctx_head_lab() -> str:
    status_agg = await db.lab_tests.aggregate([{"$group": {"_id": "$status", "count": {"$sum": 1}}}]).to_list(20)
    statuses = ", ".join(f"{i['_id']}: {i['count']}" for i in status_agg) or "ไม่มีข้อมูล"
    pending = await db.lab_tests.find({"status": {"$in": ["ordered", "sample_collected", "in_progress"]}}, {"_id": 0}).sort("ordered_at", 1).limit(10).to_list(10)
    pending_txt = "\n".join(f"- {t['test_number']} {t['patient_name']}: {t['test_type']} ({t['status']}, {t['priority']})" for t in pending) or "ไม่มี"
    abnormal = await db.lab_tests.count_documents({"status": "completed", "results.has_abnormal": True})
    return f"สถานะรายการตรวจทั้งหมด: {statuses}\nผลผิดปกติสะสม: {abnormal} รายการ\n\nรายการค้างดำเนินการ:\n{pending_txt}"


async def _ctx_head_finance() -> str:
    now = datetime.now(timezone.utc)
    today_p, month_p = now.strftime("%Y-%m-%d"), now.strftime("%Y-%m")
    agg = await db.invoices.aggregate([
        {"$unwind": "$payments"},
        {"$group": {
            "_id": None,
            "today": {"$sum": {"$cond": [{"$regexMatch": {"input": "$payments.paid_at", "regex": f"^{today_p}"}}, "$payments.amount", 0]}},
            "month": {"$sum": {"$cond": [{"$regexMatch": {"input": "$payments.paid_at", "regex": f"^{month_p}"}}, "$payments.amount", 0]}},
        }},
    ]).to_list(1)
    rev_t = agg[0]["today"] if agg else 0
    rev_m = agg[0]["month"] if agg else 0
    outstanding = await db.invoices.find({"status": {"$in": ["pending", "partially_paid"]}}, {"_id": 0, "invoice_number": 1, "patient_name": 1, "balance": 1}).sort("balance", -1).limit(10).to_list(10)
    out_txt = "\n".join(f"- {i['invoice_number']} {i['patient_name']}: ค้าง {i['balance']:,.0f} บาท" for i in outstanding) or "ไม่มี"
    claims = await db.invoices.count_documents({"insurance_claim.status": "submitted"})
    return f"รายรับวันนี้: {rev_t:,.0f} บาท | รายรับเดือนนี้: {rev_m:,.0f} บาท | เคลมรอพิจารณา: {claims} รายการ\n\nบิลค้างชำระสูงสุด:\n{out_txt}"


AGENTS = {
    "director": {
        "name": "ผู้อำนวยการโรงพยาบาล",
        "name_en": "Hospital Director",
        "icon": "building",
        "description": "ภาพรวมองค์กร กลยุทธ์ ประสิทธิภาพทุกแผนก และการตัดสินใจระดับบริหาร",
        "system": "คุณคือ Digital Twin ของผู้อำนวยการโรงพยาบาล HosPRIME มีประสบการณ์บริหารโรงพยาบาล 25 ปี เชี่ยวชาญกลยุทธ์องค์กร การเงินโรงพยาบาล คุณภาพบริการ (HA/JCI) และการบริหารทรัพยากร ให้คำแนะนำเชิงกลยุทธ์ มองภาพรวม เชื่อมโยงทุกแผนก อ้างอิงข้อมูลจริงที่ให้มา ตอบภาษาไทย กระชับ เป็นขั้นตอนปฏิบัติได้จริง",
        "context": _ctx_director,
    },
    "cmo": {
        "name": "หัวหน้าแพทย์ (CMO)",
        "name_en": "Chief Medical Officer",
        "icon": "stethoscope",
        "description": "คุณภาพการรักษา แนวทางเวชปฏิบัติ ผลแล็บผิดปกติ และความปลอดภัยผู้ป่วย",
        "system": "คุณคือ Digital Twin ของหัวหน้าแพทย์ (Chief Medical Officer) โรงพยาบาล HosPRIME อายุรแพทย์ประสบการณ์ 20 ปี เชี่ยวชาญ clinical governance, แนวทางเวชปฏิบัติ (CPG), patient safety และการพัฒนาคุณภาพการรักษา วิเคราะห์ข้อมูลคลินิกจริงที่ให้มา เตือนความเสี่ยงทางคลินิก ตอบภาษาไทย อ้างหลักวิชาการ หมายเหตุ: คำแนะนำเป็นข้อมูลสนับสนุนการตัดสินใจ ไม่แทนคำวินิจฉัยแพทย์",
        "context": _ctx_cmo,
    },
    "head_nurse": {
        "name": "หัวหน้าพยาบาล",
        "name_en": "Chief Nursing Officer",
        "icon": "heart",
        "description": "การจัดการคิวผู้ป่วย การดูแลผู้ป่วย อัตรากำลังพยาบาล และความปลอดภัย",
        "system": "คุณคือ Digital Twin ของหัวหน้าพยาบาลโรงพยาบาล HosPRIME พยาบาลวิชาชีพประสบการณ์ 18 ปี เชี่ยวชาญการบริหารการพยาบาล การจัดอัตรากำลัง การดูแลผู้ป่วยแบบองค์รวม และ medication safety ใช้ข้อมูลคิวผู้ป่วยจริงที่ให้มา จัดลำดับความสำคัญการดูแล เน้นความปลอดภัยผู้ป่วยเป็นหลัก ตอบภาษาไทย อบอุ่นแต่เป็นมืออาชีพ",
        "context": _ctx_head_nurse,
    },
    "head_pharmacy": {
        "name": "หัวหน้าเภสัชกรรม",
        "name_en": "Chief Pharmacist",
        "icon": "pill",
        "description": "คลังยา ยาตีกัน การจ่ายยา และการบริหารเวชภัณฑ์",
        "system": "คุณคือ Digital Twin ของหัวหน้าเภสัชกรรมโรงพยาบาล HosPRIME เภสัชกรประสบการณ์ 15 ปี เชี่ยวชาญ drug interaction, การบริหารคลังเวชภัณฑ์, rational drug use และ medication reconciliation วิเคราะห์ข้อมูลคลังยาจริงที่ให้มา เตือนยาตีกันและยาใกล้หมดอายุ แนะนำการสั่งซื้อ ตอบภาษาไทย แม่นยำเรื่องขนาดยาและความปลอดภัย",
        "context": _ctx_head_pharmacy,
    },
    "head_lab": {
        "name": "หัวหน้าห้องปฏิบัติการ",
        "name_en": "Laboratory Director",
        "icon": "flask",
        "description": "คิวตรวจแล็บ ผลผิดปกติ turnaround time และคุณภาพการตรวจ",
        "system": "คุณคือ Digital Twin ของหัวหน้าห้องปฏิบัติการโรงพยาบาล HosPRIME นักเทคนิคการแพทย์ประสบการณ์ 16 ปี เชี่ยวชาญ quality control (ISO 15189), การแปลผลแล็บ, turnaround time management ใช้ข้อมูลรายการตรวจจริงที่ให้มา จัดลำดับ STAT/urgent ก่อน แนะนำการแปลผลค่าผิดปกติ ตอบภาษาไทย เชิงวิชาการแต่เข้าใจง่าย",
        "context": _ctx_head_lab,
    },
    "head_finance": {
        "name": "หัวหน้าการเงิน",
        "name_en": "Chief Financial Officer",
        "icon": "banknote",
        "description": "รายรับ ลูกหนี้ค้างชำระ เคลมประกัน และการวางแผนการเงิน",
        "system": "คุณคือ Digital Twin ของหัวหน้าการเงินโรงพยาบาล HosPRIME นักการเงินประสบการณ์ 17 ปี เชี่ยวชาญ revenue cycle management, การเคลมประกัน/สิทธิ สปสช./ประกันสังคม, การบริหารลูกหนี้ และการวางแผนงบประมาณ วิเคราะห์ข้อมูลการเงินจริงที่ให้มา แนะนำการเร่งรัดหนี้และเพิ่มรายรับ ตอบภาษาไทย พร้อมตัวเลขชัดเจน",
        "context": _ctx_head_finance,
    },
}


@router.get("")
async def list_agents(user: dict = Depends(require_roles(*STAFF_ROLES))):
    return [
        {"key": k, "name": a["name"], "name_en": a["name_en"], "icon": a["icon"], "description": a["description"]}
        for k, a in AGENTS.items()
    ]


@router.get("/{agent_key}/sessions")
async def list_sessions(agent_key: str, user: dict = Depends(require_roles(*STAFF_ROLES))):
    if agent_key not in AGENTS:
        raise HTTPException(status_code=404, detail="ไม่พบ Agent")
    sessions = await db.agent_sessions.find(
        {"agent_key": agent_key, "user_id": user["id"]}, {"_id": 0}
    ).sort("updated_at", -1).limit(30).to_list(30)
    return sessions


@router.get("/sessions/{session_id}/messages")
async def get_messages(session_id: str, user: dict = Depends(require_roles(*STAFF_ROLES))):
    session = await db.agent_sessions.find_one({"id": session_id, "user_id": user["id"]}, {"_id": 0})
    if not session:
        raise HTTPException(status_code=404, detail="ไม่พบ session")
    messages = await db.agent_messages.find({"session_id": session_id}, {"_id": 0}).sort("created_at", 1).to_list(200)
    return {"session": session, "messages": messages}


@router.delete("/sessions/{session_id}")
async def delete_session(session_id: str, user: dict = Depends(require_roles(*STAFF_ROLES))):
    result = await db.agent_sessions.delete_one({"id": session_id, "user_id": user["id"]})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="ไม่พบ session")
    await db.agent_messages.delete_many({"session_id": session_id})
    return {"message": "ลบ session สำเร็จ"}


@router.post("/{agent_key}/chat")
async def chat_with_agent(agent_key: str, body: ChatRequest, user: dict = Depends(require_roles(*STAFF_ROLES))):
    agent = AGENTS.get(agent_key)
    if not agent:
        raise HTTPException(status_code=404, detail="ไม่พบ Agent")
    if not body.message.strip():
        raise HTTPException(status_code=400, detail="กรุณาพิมพ์ข้อความ")

    # Session
    if body.session_id:
        session = await db.agent_sessions.find_one({"id": body.session_id, "user_id": user["id"], "agent_key": agent_key}, {"_id": 0})
        if not session:
            raise HTTPException(status_code=404, detail="ไม่พบ session")
        session_id = session["id"]
    else:
        session_id = str(uuid.uuid4())
        await db.agent_sessions.insert_one({
            "id": session_id,
            "agent_key": agent_key,
            "user_id": user["id"],
            "title": body.message.strip()[:60],
            "created_at": now_iso(),
            "updated_at": now_iso(),
        })

    # History (last 12 messages)
    history_docs = await db.agent_messages.find({"session_id": session_id}, {"_id": 0}).sort("created_at", -1).limit(12).to_list(12)
    history = [{"role": m["role"], "content": m["content"]} for m in reversed(history_docs)]

    # Live department context
    try:
        live_context = await agent["context"]()
    except Exception:
        live_context = "(ไม่สามารถโหลดข้อมูล real-time ได้)"

    system = (
        f"{agent['system']}\n\n"
        f"=== ข้อมูล Real-time ของโรงพยาบาล ณ ขณะนี้ ===\n{live_context}\n"
        f"=== จบข้อมูล Real-time ===\n"
        f"ผู้สนทนากับคุณคือ: {user['full_name']} (ตำแหน่ง: {user['role']})"
    )

    try:
        reply = await chat_completion(system, history, body.message.strip(), session_id=f"agent-{agent_key}-{session_id}")
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"AI ตอบไม่สำเร็จ: {str(e)[:200]}")

    now = now_iso()
    await db.agent_messages.insert_many([
        {"id": str(uuid.uuid4()), "session_id": session_id, "role": "user", "content": body.message.strip(), "created_at": now},
        {"id": str(uuid.uuid4()), "session_id": session_id, "role": "assistant", "content": reply, "created_at": now_iso()},
    ])
    await db.agent_sessions.update_one({"id": session_id}, {"$set": {"updated_at": now_iso()}})

    return {"session_id": session_id, "reply": reply, "agent_key": agent_key}
