import io
import re
import uuid
from typing import Optional

import pandas as pd
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel

from core.ai import chat_completion
from core.database import db
from core.security import require_roles
from core.utils import audit_log, now_iso

router = APIRouter(prefix="/connector", tags=["data-connector"])

PII_KEYWORDS = {
    "national_id": "เลขบัตรประชาชน", "citizen": "เลขบัตรประชาชน", "ssn": "เลขประจำตัว",
    "phone": "เบอร์โทรศัพท์", "mobile": "เบอร์โทรศัพท์", "tel": "เบอร์โทรศัพท์",
    "email": "อีเมล", "first_name": "ชื่อ", "last_name": "นามสกุล", "full_name": "ชื่อ-นามสกุล",
    "name": "ชื่อ", "address": "ที่อยู่", "date_of_birth": "วันเกิด", "dob": "วันเกิด", "birth": "วันเกิด",
    "password": "รหัสผ่าน (ความลับ)", "salary": "เงินเดือน (อ่อนไหว)", "patient": "ข้อมูลผู้ป่วย",
    "diagnosis": "การวินิจฉัย (ข้อมูลสุขภาพ)", "allerg": "การแพ้ (ข้อมูลสุขภาพ)",
    "insurance": "ข้อมูลประกัน", "emergency_contact": "ผู้ติดต่อฉุกเฉิน",
}

SYSTEM_COLLECTIONS = {"login_attempts", "counters", "settings"}


class SourceCreate(BaseModel):
    name: str
    connection_string: str
    db_name: str


def _detect_pii(field_name: str) -> Optional[str]:
    low = field_name.lower()
    for kw, reason in PII_KEYWORDS.items():
        if kw in low:
            return reason
    return None


def _type_name(v) -> str:
    if v is None:
        return "null"
    return {bool: "bool", int: "int", float: "float", str: "str", dict: "object", list: "array"}.get(type(v), type(v).__name__)


def _analyze_docs(docs: list) -> list:
    """Infer field schema from sample documents."""
    stats = {}
    for doc in docs:
        for k, v in doc.items():
            if k == "_id":
                continue
            s = stats.setdefault(k, {"types": set(), "non_null": 0})
            t = _type_name(v)
            if t != "null":
                s["types"].add(t)
                s["non_null"] += 1
    n = max(1, len(docs))
    fields = []
    for name, s in sorted(stats.items()):
        pii = _detect_pii(name)
        fields.append({
            "name": name,
            "types": sorted(s["types"]) or ["null"],
            "fill_rate": round(s["non_null"] / n * 100, 1),
            "is_pii": bool(pii),
            "pii_reason": pii or "",
        })
    return fields


async def _scan_mongo(target_db) -> list:
    names = await target_db.list_collection_names()
    collections = []
    for name in sorted(names)[:30]:
        if name.startswith("system."):
            continue
        count = await target_db[name].count_documents({})
        docs = await target_db[name].find({}, {"_id": 0}).limit(100).to_list(100)
        collections.append({
            "name": name,
            "count": count,
            "is_system": name in SYSTEM_COLLECTIONS,
            "fields": _analyze_docs(docs),
        })
    return collections


def _scan_summary_text(collections: list) -> str:
    lines = []
    for c in collections:
        field_strs = []
        for f in c["fields"][:25]:
            pii = " [PII]" if f["is_pii"] else ""
            field_strs.append(f"{f['name']}({'/'.join(f['types'])},{f['fill_rate']}%{pii})")
        lines.append(f"- collection '{c['name']}': {c['count']} records | fields: {', '.join(field_strs)}")
    text = "\n".join(lines)
    return text[:7000]


AI_ANALYSIS_PROMPT = """คุณคือ Data Connector & Data Governance Agent ของระบบโรงพยาบาล HosPRIME
วิเคราะห์ schema ฐานข้อมูลต่อไปนี้ และตอบเป็นภาษาไทยในรูปแบบ markdown 4 หัวข้อ:

## 🔗 การ Mapping เข้าระบบ HosPRIME
จับคู่แต่ละ collection/ตาราง กับ entity มาตรฐานของ HosPRIME (patients, appointments, users/staff, drugs, prescriptions, lab_tests, invoices) พร้อมระบุฟิลด์สำคัญที่ map กัน และฟิลด์ที่ขาด

## 🛡️ ธรรมาภิบาลข้อมูล (PDPA)
ระบุฟิลด์ข้อมูลส่วนบุคคล/ข้อมูลสุขภาพที่ต้องคุ้มครองตาม PDPA พร้อมข้อเสนอแนะ (การเข้ารหัส, การจำกัดสิทธิ์เข้าถึง, การ anonymize)

## 📊 คุณภาพข้อมูล
ประเมินจาก fill rate และโครงสร้าง: ฟิลด์ที่ข้อมูลขาดมาก, ความเสี่ยงข้อมูลซ้ำ, ข้อเสนอแนะการปรับปรุง

## 🕸️ ข้อเสนอแนะ Knowledge Graph
แนะนำ nodes และ relationships ที่ควรสร้างจากข้อมูลชุดนี้ เพื่อให้ AI Agents ทุกตัวใช้งานร่วมกันได้

ตอบกระชับ ตรงประเด็น ใช้ bullet points"""


async def _run_ai_analysis(collections: list) -> dict:
    summary = _scan_summary_text(collections)
    try:
        analysis = await chat_completion(
            AI_ANALYSIS_PROMPT, [], f"Schema ที่สแกนได้:\n{summary}", session_id=f"connector-scan-{uuid.uuid4()}"
        )
        return {"success": True, "analysis": analysis}
    except Exception as e:
        return {"success": False, "analysis": "", "error": str(e)}


async def ensure_internal_source():
    existing = await db.data_sources.find_one({"type": "internal"})
    if not existing:
        await db.data_sources.insert_one({
            "id": str(uuid.uuid4()),
            "name": "ฐานข้อมูล HosPRIME (ภายใน)",
            "type": "internal",
            "connection_string": "",
            "db_name": "",
            "filename": "",
            "status": "ready",
            "last_scan_at": None,
            "created_at": now_iso(),
        })


@router.get("/sources")
async def list_sources(user: dict = Depends(require_roles("admin"))):
    await ensure_internal_source()
    sources = await db.data_sources.find({}, {"_id": 0}).sort("created_at", 1).to_list(100)
    for s in sources:
        cs = s.get("connection_string") or ""
        s["connection_string"] = re.sub(r"//([^:@/]+):([^@/]+)@", r"//\1:••••@", cs) if cs else ""
    return sources


@router.post("/sources", status_code=201)
async def add_source(body: SourceCreate, user: dict = Depends(require_roles("admin"))):
    source = {
        "id": str(uuid.uuid4()),
        "name": body.name,
        "type": "mongodb",
        "connection_string": body.connection_string,
        "db_name": body.db_name,
        "filename": "",
        "status": "ready",
        "last_scan_at": None,
        "created_at": now_iso(),
    }
    await db.data_sources.insert_one(source)
    await audit_log(user, "create", "data_source", source["id"], body.name)
    source.pop("_id", None)
    source["connection_string"] = "••••"
    return source


@router.post("/upload", status_code=201)
async def upload_file(file: UploadFile = File(...), user: dict = Depends(require_roles("admin"))):
    filename = file.filename or "dataset"
    content = await file.read()
    if len(content) > 20 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="ไฟล์ใหญ่เกิน 20MB")
    try:
        if filename.lower().endswith(".csv"):
            try:
                df = pd.read_csv(io.BytesIO(content))
            except UnicodeDecodeError:
                df = pd.read_csv(io.BytesIO(content), encoding="cp874")
        elif filename.lower().endswith((".xlsx", ".xls")):
            df = pd.read_excel(io.BytesIO(content))
        else:
            raise HTTPException(status_code=400, detail="รองรับเฉพาะไฟล์ .csv, .xlsx, .xls")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"อ่านไฟล์ไม่สำเร็จ: {str(e)[:150]}")

    df = df.where(pd.notnull(df), None)
    rows = df.head(1000).to_dict(orient="records")
    # Convert numpy types to native python
    clean_rows = []
    for row in rows:
        clean = {}
        for k, v in row.items():
            if hasattr(v, "item"):
                v = v.item()
            clean[str(k)] = v
        clean_rows.append(clean)

    source = {
        "id": str(uuid.uuid4()),
        "name": f"ไฟล์: {filename}",
        "type": "file",
        "connection_string": "",
        "db_name": "",
        "filename": filename,
        "row_count": int(len(df)),
        "status": "ready",
        "last_scan_at": None,
        "created_at": now_iso(),
    }
    await db.data_sources.insert_one(source)
    await db.uploaded_datasets.insert_one({"source_id": source["id"], "rows": clean_rows})
    await audit_log(user, "upload", "data_source", source["id"], filename)
    source.pop("_id", None)
    return source


@router.delete("/sources/{source_id}")
async def delete_source(source_id: str, user: dict = Depends(require_roles("admin"))):
    source = await db.data_sources.find_one({"id": source_id}, {"_id": 0})
    if not source:
        raise HTTPException(status_code=404, detail="ไม่พบแหล่งข้อมูล")
    if source["type"] == "internal":
        raise HTTPException(status_code=400, detail="ไม่สามารถลบฐานข้อมูลภายในได้")
    await db.data_sources.delete_one({"id": source_id})
    await db.uploaded_datasets.delete_many({"source_id": source_id})
    await db.scans.delete_many({"source_id": source_id})
    await audit_log(user, "delete", "data_source", source_id)
    return {"message": "ลบแหล่งข้อมูลสำเร็จ"}


@router.post("/sources/{source_id}/scan")
async def scan_source(source_id: str, user: dict = Depends(require_roles("admin"))):
    """One-click scan: schema discovery + PII detection + AI governance analysis."""
    source = await db.data_sources.find_one({"id": source_id}, {"_id": 0})
    if not source:
        raise HTTPException(status_code=404, detail="ไม่พบแหล่งข้อมูล")

    if source["type"] == "internal":
        collections = await _scan_mongo(db)
    elif source["type"] == "mongodb":
        try:
            client = AsyncIOMotorClient(source["connection_string"], serverSelectionTimeoutMS=5000)
            target = client[source["db_name"]]
            collections = await _scan_mongo(target)
            client.close()
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"เชื่อมต่อฐานข้อมูลไม่สำเร็จ: {str(e)[:150]}")
    elif source["type"] == "file":
        dataset = await db.uploaded_datasets.find_one({"source_id": source_id}, {"_id": 0})
        if not dataset:
            raise HTTPException(status_code=404, detail="ไม่พบข้อมูลไฟล์")
        rows = dataset["rows"]
        collections = [{
            "name": source["filename"],
            "count": source.get("row_count", len(rows)),
            "is_system": False,
            "fields": _analyze_docs(rows[:100]),
        }]
    else:
        raise HTTPException(status_code=400, detail="ประเภทแหล่งข้อมูลไม่รองรับ")

    ai_result = await _run_ai_analysis(collections)

    scan = {
        "id": str(uuid.uuid4()),
        "source_id": source_id,
        "source_name": source["name"],
        "scanned_at": now_iso(),
        "scanned_by": user["full_name"],
        "collections": collections,
        "total_collections": len(collections),
        "total_records": sum(c["count"] for c in collections),
        "pii_field_count": sum(1 for c in collections for f in c["fields"] if f["is_pii"]),
        "ai_analysis": ai_result.get("analysis", ""),
        "ai_success": ai_result.get("success", False),
        "ai_error": ai_result.get("error", ""),
    }
    await db.scans.insert_one(dict(scan))
    await db.data_sources.update_one({"id": source_id}, {"$set": {"last_scan_at": scan["scanned_at"], "status": "scanned"}})
    await audit_log(user, "scan", "data_source", source_id, source["name"])
    scan.pop("_id", None)
    return scan


@router.get("/sources/{source_id}/scan")
async def get_latest_scan(source_id: str, user: dict = Depends(require_roles("admin"))):
    scan = await db.scans.find_one({"source_id": source_id}, {"_id": 0}, sort=[("scanned_at", -1)])
    if not scan:
        raise HTTPException(status_code=404, detail="ยังไม่เคยสแกนแหล่งข้อมูลนี้")
    return scan
