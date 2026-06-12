import re
import uuid
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field

from core.ai import chat_completion
from core.database import db
from core.security import STAFF_ROLES, require_roles
from core.utils import audit_log, next_number, now_iso

router = APIRouter(prefix="/documents", tags=["documents"])

DOC_STATUSES = ["draft", "under_review", "approved", "rejected"]

THAI_MONTHS = ["มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน",
               "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"]


def thai_date() -> str:
    now = datetime.now(timezone.utc)
    return f"{now.day} {THAI_MONTHS[now.month - 1]} พ.ศ. {now.year + 543}"


# ---------- Schemas ----------

class TemplateCreate(BaseModel):
    name: str
    category: str = "ทั่วไป"
    description: Optional[str] = ""
    instructions: str = Field(min_length=10)


class TemplateUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    instructions: Optional[str] = None


class GenerateRequest(BaseModel):
    template_id: str
    subject: str
    details: str
    additional_instructions: Optional[str] = ""


class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    official_number: Optional[str] = None


class StatusUpdate(BaseModel):
    status: str


class AdhocCheck(BaseModel):
    content: str = Field(min_length=20)
    doc_type: Optional[str] = "หนังสือราชการทั่วไป"


# ---------- Seed templates ----------

SEED_TEMPLATES = [
    {
        "name": "หนังสือราชการภายนอก",
        "category": "หนังสือราชการ",
        "description": "หนังสือติดต่อราชการระหว่างหน่วยงานภายนอก ตามระเบียบงานสารบรรณ",
        "instructions": """สร้างหนังสือราชการภายนอกตามระเบียบสำนักนายกรัฐมนตรีว่าด้วยงานสารบรรณ โครงสร้างต้องมีครบ:
1. ที่ (เลขที่หนังสือ เว้นว่างเป็น "ที่ รพ.HosPRIME ๐๐๑/......")
2. ส่วนราชการเจ้าของหนังสือ: โรงพยาบาล HosPRIME
3. วันที่ (ใช้วันที่ที่ให้มา รูปแบบไทย)
4. เรื่อง (กระชับ ชัดเจน)
5. คำขึ้นต้น "เรียน" ตามฐานะผู้รับ
6. อ้างถึง / สิ่งที่ส่งมาด้วย (ถ้ามี)
7. ข้อความ 3 ส่วน: เหตุที่มีหนังสือไป → วัตถุประสงค์ → สรุปความ/ขอความร่วมมือ
8. คำลงท้าย "ขอแสดงความนับถือ"
9. ลงชื่อ (ผู้อำนวยการโรงพยาบาล HosPRIME) พร้อมตำแหน่ง
10. ส่วนราชการเจ้าของเรื่อง + เบอร์โทรติดต่อ
ใช้ภาษาราชการที่ถูกต้อง สุภาพ กระชับ""",
    },
    {
        "name": "บันทึกข้อความ (หนังสือภายใน)",
        "category": "หนังสือราชการ",
        "description": "หนังสือติดต่อภายในหน่วยงาน",
        "instructions": """สร้างบันทึกข้อความ (หนังสือภายใน) ตามระเบียบงานสารบรรณ โครงสร้าง:
1. หัวกระดาษ "บันทึกข้อความ"
2. ส่วนราชการ: (แผนก/ฝ่ายที่ระบุ) โรงพยาบาล HosPRIME
3. ที่ / วันที่ (รูปแบบไทย)
4. เรื่อง
5. คำขึ้นต้น "เรียน" (ผู้บังคับบัญชาที่เกี่ยวข้อง)
6. ข้อความ: ภูมิหลัง/ข้อเท็จจริง → ข้อพิจารณา → ข้อเสนอ (จึงเรียนมาเพื่อโปรดพิจารณา/ทราบ/อนุมัติ)
7. ลงชื่อ พร้อมตำแหน่งผู้เขียน
ภาษาราชการกระชับ ชัดเจน แบ่งย่อหน้าเหมาะสม""",
    },
    {
        "name": "คำสั่งโรงพยาบาล",
        "category": "คำสั่ง",
        "description": "คำสั่งแต่งตั้ง มอบหมายงาน หรือกำหนดแนวปฏิบัติ",
        "instructions": """สร้างคำสั่งโรงพยาบาล HosPRIME โครงสร้าง:
1. หัว "คำสั่งโรงพยาบาล HosPRIME ที่ ...../..... (เลขที่/ปี พ.ศ.)"
2. เรื่อง
3. อารัมภบท: เหตุผลความจำเป็น + อ้างอำนาจตามกฎหมาย/ระเบียบที่เกี่ยวข้อง
4. ข้อความสั่งการเป็นข้อๆ (ข้อ ๑, ข้อ ๒, ...) ระบุผู้รับผิดชอบ หน้าที่ และขอบเขตชัดเจน
5. "ทั้งนี้ ตั้งแต่บัดนี้เป็นต้นไป" หรือวันที่มีผล
6. "สั่ง ณ วันที่ ..." (วันที่ไทย)
7. ลงชื่อ ผู้อำนวยการโรงพยาบาล HosPRIME
ใช้เลขไทยในข้อคำสั่ง ภาษาราชการเป็นทางการ""",
    },
    {
        "name": "ประกาศโรงพยาบาล",
        "category": "ประกาศ",
        "description": "ประกาศแจ้งเรื่องให้บุคลากรหรือประชาชนทราบ",
        "instructions": """สร้างประกาศโรงพยาบาล HosPRIME โครงสร้าง:
1. หัว "ประกาศโรงพยาบาล HosPRIME"
2. เรื่อง
3. อารัมภบท: เหตุผล/ที่มาของประกาศ
4. เนื้อหาประกาศเป็นข้อๆ ชัดเจน (ถ้ามีหลายประเด็น)
5. "จึงประกาศมาเพื่อทราบโดยทั่วกัน" หรือ "จึงประกาศให้ทราบและถือปฏิบัติ"
6. "ประกาศ ณ วันที่ ..." (วันที่ไทย)
7. ลงชื่อ ผู้อำนวยการโรงพยาบาล HosPRIME
ภาษาทางการ เข้าใจง่าย""",
    },
    {
        "name": "หนังสือรับรอง",
        "category": "หนังสือรับรอง",
        "description": "หนังสือรับรองการทำงาน เงินเดือน หรือสถานภาพบุคลากร",
        "instructions": """สร้างหนังสือรับรองของโรงพยาบาล HosPRIME โครงสร้าง:
1. หัว "หนังสือรับรอง" + "ที่ ...../....."
2. ข้อความเริ่ม "หนังสือฉบับนี้ให้ไว้เพื่อรับรองว่า..." ระบุชื่อ-สกุล ตำแหน่ง สังกัด ตามรายละเอียดที่ให้
3. เนื้อหาการรับรอง (ระยะเวลาทำงาน เงินเดือน ความประพฤติ ตามที่ระบุ)
4. วัตถุประสงค์การใช้ (ถ้าระบุ): "ให้ไว้เพื่อ..."
5. "ให้ไว้ ณ วันที่ ..." (วันที่ไทย)
6. ลงชื่อ ผู้อำนวยการโรงพยาบาล HosPRIME พร้อมตำแหน่ง
ภาษาราชการกระชับ ข้อมูลต้องตรงตามที่ผู้ขอระบุเท่านั้น ห้ามแต่งเติมตัวเลข/ข้อเท็จจริงเอง หากข้อมูลไม่ครบให้เว้น "......" ไว้""",
    },
]


async def seed_templates():
    if await db.doc_templates.count_documents({}) > 0:
        return
    for t in SEED_TEMPLATES:
        await db.doc_templates.insert_one({
            "id": str(uuid.uuid4()),
            **t,
            "is_seed": True,
            "created_by": "system",
            "created_at": now_iso(),
            "updated_at": now_iso(),
        })


# ---------- Templates (unlimited custom instructions) ----------

@router.get("/templates")
async def list_templates(user: dict = Depends(require_roles(*STAFF_ROLES))):
    await seed_templates()
    return await db.doc_templates.find({}, {"_id": 0}).sort("created_at", 1).to_list(500)


@router.post("/templates", status_code=201)
async def create_template(body: TemplateCreate, user: dict = Depends(require_roles("admin"))):
    template = {
        "id": str(uuid.uuid4()),
        **body.model_dump(),
        "is_seed": False,
        "created_by": user["full_name"],
        "created_at": now_iso(),
        "updated_at": now_iso(),
    }
    await db.doc_templates.insert_one(template)
    await audit_log(user, "create", "doc_template", template["id"], body.name)
    template.pop("_id", None)
    return template


@router.put("/templates/{template_id}")
async def update_template(template_id: str, body: TemplateUpdate, user: dict = Depends(require_roles("admin"))):
    updates = {k: v for k, v in body.model_dump(exclude_unset=True).items() if v is not None}
    if not updates:
        raise HTTPException(status_code=400, detail="ไม่มีข้อมูลที่ต้องการแก้ไข")
    updates["updated_at"] = now_iso()
    result = await db.doc_templates.update_one({"id": template_id}, {"$set": updates})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="ไม่พบเทมเพลต")
    await audit_log(user, "update", "doc_template", template_id)
    return await db.doc_templates.find_one({"id": template_id}, {"_id": 0})


@router.delete("/templates/{template_id}")
async def delete_template(template_id: str, user: dict = Depends(require_roles("admin"))):
    result = await db.doc_templates.delete_one({"id": template_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="ไม่พบเทมเพลต")
    await audit_log(user, "delete", "doc_template", template_id)
    return {"message": "ลบเทมเพลตสำเร็จ"}


# ---------- AI Generation ----------

GEN_SYSTEM = (
    "คุณคือเจ้าหน้าที่สารบรรณมืออาชีพของโรงพยาบาล HosPRIME "
    "เชี่ยวชาญการร่างหนังสือราชการไทยตามระเบียบสำนักนายกรัฐมนตรีว่าด้วยงานสารบรรณ "
    "สร้างเอกสารภาษาไทยราชการที่ถูกต้อง สมบูรณ์ พร้อมใช้งานจริง "
    "ตอบกลับเฉพาะเนื้อหาเอกสารเท่านั้น ห้ามใส่คำอธิบาย คำนำ หรือ markdown code block"
)


@router.post("/generate", status_code=201)
async def generate_document(body: GenerateRequest, user: dict = Depends(require_roles(*STAFF_ROLES))):
    template = await db.doc_templates.find_one({"id": body.template_id}, {"_id": 0})
    if not template:
        raise HTTPException(status_code=404, detail="ไม่พบเทมเพลต")
    extra = f"\n- คำสั่งเพิ่มเติมจากผู้ใช้: {body.additional_instructions}" if body.additional_instructions else ""
    prompt = (
        f"คำสั่งการสร้างเอกสาร (Instruction ของเทมเพลต '{template['name']}'):\n{template['instructions']}\n\n"
        f"ข้อมูลสำหรับเอกสารฉบับนี้:\n"
        f"- เรื่อง: {body.subject}\n"
        f"- รายละเอียด/เนื้อหา: {body.details}\n"
        f"- วันที่เอกสาร: {thai_date()}\n"
        f"- หน่วยงาน: โรงพยาบาล HosPRIME\n"
        f"- ผู้จัดทำ: {user['full_name']}{extra}"
    )
    try:
        content = await chat_completion(GEN_SYSTEM, [], prompt, session_id=f"doc-gen-{uuid.uuid4()}")
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"AI สร้างเอกสารไม่สำเร็จ: {str(e)[:200]}")

    document = {
        "id": str(uuid.uuid4()),
        "doc_number": await next_number("document", "DOC"),
        "official_number": "",
        "title": body.subject,
        "content": content.strip(),
        "template_id": template["id"],
        "template_name": template["name"],
        "category": template["category"],
        "status": "draft",
        "ai_generated": True,
        "review": None,
        "created_by": user["id"],
        "created_by_name": user["full_name"],
        "created_at": now_iso(),
        "updated_at": now_iso(),
    }
    await db.documents.insert_one(document)
    await audit_log(user, "generate", "document", document["id"], document["doc_number"])
    document.pop("_id", None)
    return document


# ---------- Documents CRUD ----------

@router.get("")
async def list_documents(
    status: str = "",
    category: str = "",
    search: str = "",
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    user: dict = Depends(require_roles(*STAFF_ROLES)),
):
    query = {}
    if status:
        query["status"] = status
    if category:
        query["category"] = category
    if search:
        safe = re.escape(search)
        query["$or"] = [
            {"title": {"$regex": safe, "$options": "i"}},
            {"doc_number": {"$regex": safe, "$options": "i"}},
            {"created_by_name": {"$regex": safe, "$options": "i"}},
        ]
    total = await db.documents.count_documents(query)
    items = (
        await db.documents.find(query, {"_id": 0, "content": 0})
        .sort("created_at", -1)
        .skip((page - 1) * limit)
        .limit(limit)
        .to_list(limit)
    )
    return {"items": items, "total": total, "page": page, "pages": max(1, -(-total // limit))}


@router.get("/{document_id}")
async def get_document(document_id: str, user: dict = Depends(require_roles(*STAFF_ROLES))):
    doc = await db.documents.find_one({"id": document_id}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=404, detail="ไม่พบเอกสาร")
    return doc


@router.put("/{document_id}")
async def update_document(document_id: str, body: DocumentUpdate, user: dict = Depends(require_roles(*STAFF_ROLES))):
    doc = await db.documents.find_one({"id": document_id}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=404, detail="ไม่พบเอกสาร")
    if user["role"] != "admin" and doc["created_by"] != user["id"]:
        raise HTTPException(status_code=403, detail="แก้ไขได้เฉพาะผู้สร้างหรือผู้ดูแลระบบ")
    if doc["status"] == "approved" and user["role"] != "admin":
        raise HTTPException(status_code=400, detail="เอกสารที่อนุมัติแล้วแก้ไขไม่ได้")
    updates = {k: v for k, v in body.model_dump(exclude_unset=True).items() if v is not None}
    if not updates:
        raise HTTPException(status_code=400, detail="ไม่มีข้อมูลที่ต้องการแก้ไข")
    updates["updated_at"] = now_iso()
    await db.documents.update_one({"id": document_id}, {"$set": updates})
    await audit_log(user, "update", "document", document_id)
    return await db.documents.find_one({"id": document_id}, {"_id": 0})


@router.patch("/{document_id}/status")
async def update_doc_status(document_id: str, body: StatusUpdate, user: dict = Depends(require_roles("admin"))):
    if body.status not in DOC_STATUSES:
        raise HTTPException(status_code=400, detail=f"สถานะไม่ถูกต้อง: {body.status}")
    result = await db.documents.update_one(
        {"id": document_id},
        {"$set": {"status": body.status, "updated_at": now_iso(),
                  "status_changed_by": user["full_name"], "status_changed_at": now_iso()}},
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="ไม่พบเอกสาร")
    await audit_log(user, "update_status", "document", document_id, body.status)
    return await db.documents.find_one({"id": document_id}, {"_id": 0})


@router.delete("/{document_id}")
async def delete_document(document_id: str, user: dict = Depends(require_roles(*STAFF_ROLES))):
    doc = await db.documents.find_one({"id": document_id}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=404, detail="ไม่พบเอกสาร")
    if user["role"] != "admin" and not (doc["created_by"] == user["id"] and doc["status"] == "draft"):
        raise HTTPException(status_code=403, detail="ลบได้เฉพาะฉบับร่างของตนเอง หรือโดยผู้ดูแลระบบ")
    await db.documents.delete_one({"id": document_id})
    await audit_log(user, "delete", "document", document_id)
    return {"message": "ลบเอกสารสำเร็จ"}


# ---------- AI Review / ตรวจสอบ ----------

REVIEW_SYSTEM = (
    "คุณคือผู้ตรวจสอบเอกสารราชการอาวุโสของโรงพยาบาล HosPRIME "
    "เชี่ยวชาญระเบียบสำนักนายกรัฐมนตรีว่าด้วยงานสารบรรณ ตรวจสอบอย่างละเอียดและเที่ยงตรง "
    "รายงานผลเป็นภาษาไทย markdown ตามหัวข้อ:\n"
    "## ✅ ผลการตรวจสอบโดยรวม (พร้อมคะแนน เต็ม 100)\n"
    "## ⚠️ ข้อบกพร่องที่พบ (โครงสร้าง/องค์ประกอบที่ขาด)\n"
    "## ✏️ ภาษาและรูปแบบราชการ (คำผิด การใช้คำราชการ)\n"
    "## 📝 ข้อเสนอแนะการแก้ไข (ระบุชัดเจนว่าแก้ตรงไหนเป็นอะไร)"
)


@router.post("/{document_id}/review")
async def review_document(document_id: str, user: dict = Depends(require_roles(*STAFF_ROLES))):
    doc = await db.documents.find_one({"id": document_id}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=404, detail="ไม่พบเอกสาร")
    prompt = f"ตรวจสอบเอกสารราชการต่อไปนี้ (ประเภท: {doc['template_name']}):\n\n{doc['content'][:8000]}"
    try:
        report = await chat_completion(REVIEW_SYSTEM, [], prompt, session_id=f"doc-review-{document_id}")
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"AI ตรวจสอบไม่สำเร็จ: {str(e)[:200]}")
    review = {"report": report, "reviewed_at": now_iso(), "reviewed_by": user["full_name"]}
    await db.documents.update_one(
        {"id": document_id},
        {"$set": {"review": review, "status": "under_review" if doc["status"] == "draft" else doc["status"], "updated_at": now_iso()}},
    )
    await audit_log(user, "review", "document", document_id)
    return await db.documents.find_one({"id": document_id}, {"_id": 0})


@router.post("/check", status_code=200)
async def adhoc_check(body: AdhocCheck, user: dict = Depends(require_roles(*STAFF_ROLES))):
    prompt = f"ตรวจสอบเอกสารราชการต่อไปนี้ (ประเภท: {body.doc_type}):\n\n{body.content[:8000]}"
    try:
        report = await chat_completion(REVIEW_SYSTEM, [], prompt, session_id=f"doc-check-{uuid.uuid4()}")
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"AI ตรวจสอบไม่สำเร็จ: {str(e)[:200]}")
    return {"report": report, "checked_at": now_iso()}
