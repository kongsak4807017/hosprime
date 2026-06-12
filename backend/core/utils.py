from datetime import datetime, timezone

from pymongo import ReturnDocument

from core.database import db


async def next_number(counter_name: str, prefix: str) -> str:
    doc = await db.counters.find_one_and_update(
        {"_id": counter_name},
        {"$inc": {"seq": 1}},
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )
    return f"{prefix}-{doc['seq']:06d}"


async def audit_log(user: dict, action: str, resource_type: str, resource_id: str, detail: str = ""):
    await db.audit_logs.insert_one({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "user_id": user.get("id"),
        "user_email": user.get("email"),
        "user_role": user.get("role"),
        "action": action,
        "resource_type": resource_type,
        "resource_id": resource_id,
        "detail": detail,
    })


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()
