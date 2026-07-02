import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from core.agent_office import (
    CAPABILITY_REGISTRY,
    UNIVERSAL_AGENT_RULES,
    get_core_agent,
    list_core_agents,
    validate_core_office_registry,
)
from core.ai import chat_completion
from core.database import db
from core.security import STAFF_ROLES, require_roles
from core.utils import audit_log, now_iso

router = APIRouter(prefix="/executive-office", tags=["executive-office"])


class OfficeChatRequest(BaseModel):
    agent_key: str
    message: str = Field(min_length=1, max_length=12000)
    session_id: Optional[str] = None


async def _safe_count(collection_name: str, query: Optional[dict] = None) -> int:
    try:
        return await db[collection_name].count_documents(query or {})
    except Exception:
        return 0


async def _brief_snapshot() -> Dict:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    patients = await _safe_count("patients", {"is_active": True})
    appointments_today = await _safe_count("appointments", {"appointment_date": today})
    completed_today = await _safe_count(
        "appointments", {"appointment_date": today, "status": "completed"}
    )
    pending_labs = await _safe_count(
        "lab_tests", {"status": {"$in": ["ordered", "sample_collected", "in_progress"]}}
    )
    low_stock = await _safe_count(
        "drugs", {"is_active": True, "$expr": {"$lte": ["$quantity_in_stock", "$reorder_level"]}}
    )
    overdue_actions = await _safe_count(
        "actions", {"status": {"$nin": ["completed", "cancelled"]}, "due_date": {"$lt": today}}
    )
    pending_decisions = await _safe_count("decisions", {"status": "pending"})
    approved_documents = await _safe_count("documents", {"status": "approved"})

    outstanding_amount = 0.0
    outstanding_count = 0
    try:
        result = await db.invoices.aggregate(
            [
                {"$match": {"status": {"$in": ["pending", "partially_paid"]}}},
                {
                    "$group": {
                        "_id": None,
                        "amount": {"$sum": "$balance"},
                        "count": {"$sum": 1},
                    }
                },
            ]
        ).to_list(1)
        if result:
            outstanding_amount = float(result[0].get("amount", 0) or 0)
            outstanding_count = int(result[0].get("count", 0) or 0)
    except Exception:
        pass

    risks: List[Dict] = []
    if low_stock:
        risks.append({"key": "drug_stock", "severity": "high", "title": f"ยา/เวชภัณฑ์ต่ำกว่าจุดสั่งซื้อ {low_stock} รายการ"})
    if pending_labs:
        risks.append({"key": "pending_lab", "severity": "medium", "title": f"รายการแล็บค้างดำเนินการ {pending_labs} รายการ"})
    if overdue_actions:
        risks.append({"key": "overdue_action", "severity": "high", "title": f"Action items เกินกำหนด {overdue_actions} รายการ"})
    if outstanding_amount > 0:
        risks.append({"key": "outstanding_finance", "severity": "medium", "title": f"ลูกหนี้คงค้าง {outstanding_amount:,.0f} บาท"})

    return {
        "generated_at": now_iso(),
        "metrics": {
            "patients": patients,
            "appointments_today": appointments_today,
            "completed_today": completed_today,
            "pending_labs": pending_labs,
            "low_stock_items": low_stock,
            "outstanding_amount": outstanding_amount,
            "outstanding_count": outstanding_count,
            "pending_decisions": pending_decisions,
            "overdue_actions": overdue_actions,
            "approved_documents": approved_documents,
        },
        "risks": risks[:8],
        "data_readiness": {
            "status": "prototype",
            "warning": "Metrics currently come from HosPrime operational collections. They are not yet a governed management data mart.",
        },
    }


async def _recent_documents(limit: int = 8) -> List[Dict]:
    try:
        return await db.documents.find(
            {},
            {
                "_id": 0,
                "id": 1,
                "doc_number": 1,
                "title": 1,
                "category": 1,
                "status": 1,
                "updated_at": 1,
            },
        ).sort("updated_at", -1).limit(limit).to_list(limit)
    except Exception:
        return []


async def _latest_scans(limit: int = 5) -> List[Dict]:
    try:
        return await db.scans.find(
            {}, {"_id": 0, "source_id": 1, "created_at": 1, "collections": 1}
        ).sort("created_at", -1).limit(limit).to_list(limit)
    except Exception:
        return []


async def _build_agent_context(agent_key: str) -> Tuple[str, List[Dict]]:
    brief = await _brief_snapshot()
    evidence: List[Dict] = [
        {"source_type": "operational_snapshot", "source_id": "current", "label": "HosPrime operational snapshot"}
    ]

    if agent_key == "knowledge":
        docs = await _recent_documents()
        graph_meta = await db.settings.find_one({"_id": "kg_meta"}, {"_id": 0}) or {}
        evidence.extend(
            {
                "source_type": "document",
                "source_id": item.get("id", ""),
                "label": item.get("title", "Untitled document"),
            }
            for item in docs
        )
        context = (
            f"Recent governed documents: {docs}\n"
            f"Current graph metadata: {graph_meta}\n"
            "Important: the current graph is an operational clinical graph, not yet the target organization/decision ontology."
        )
        return context, evidence

    if agent_key == "analyst":
        scans = await _latest_scans()
        context = f"Management snapshot: {brief}\nLatest data-source scans: {scans}"
        evidence.append({"source_type": "data_catalog", "source_id": "latest-scans", "label": "Latest connector scans"})
        return context, evidence

    if agent_key == "planner":
        decisions = []
        actions = []
        try:
            decisions = await db.decisions.find({}, {"_id": 0}).sort("created_at", -1).limit(10).to_list(10)
            actions = await db.actions.find({}, {"_id": 0}).sort("created_at", -1).limit(20).to_list(20)
        except Exception:
            pass
        return f"Management snapshot: {brief}\nRecent decisions: {decisions}\nRecent actions: {actions}", evidence

    if agent_key == "action":
        templates = []
        try:
            templates = await db.doc_templates.find(
                {}, {"_id": 0, "id": 1, "name": 1, "category": 1, "description": 1}
            ).limit(50).to_list(50)
        except Exception:
            pass
        evidence.append({"source_type": "template_catalog", "source_id": "document-templates", "label": "Approved document templates"})
        return f"Management snapshot: {brief}\nAvailable document templates: {templates}", evidence

    return f"Management snapshot: {brief}", evidence


def _system_prompt(agent: Dict, user: Dict) -> str:
    capabilities = [CAPABILITY_REGISTRY[c]["name"] for c in agent["capabilities"]]
    rules = "\n".join(f"- {rule}" for rule in UNIVERSAL_AGENT_RULES)
    return f"""You are {agent['name']} ({agent['name_th']}), role: {agent['role']} in HosPrime AI Agent Office v2.

MISSION
{agent['mission']}

PERSONALITY
{', '.join(agent['personality'])}

REASONING STYLE
{', '.join(agent['reasoning_style'])}

ALLOWED CAPABILITIES
{', '.join(capabilities)}

AUTHORITY
Level {agent['authority_level']}. Approval required: {agent['approval_required']}.

UNIVERSAL RULES
{rules}

RESPONSE CONTRACT
Respond in Thai unless the user requests another language. Use these sections when relevant:
1. Executive summary
2. Facts and evidence
3. Analysis or proposed plan
4. Risks / limitations / uncertainty
5. Recommended next step
6. Human approval required
Never claim that an action was executed unless a tool or database record confirms it.

CURRENT USER
Name: {user.get('full_name', '')}
Role: {user.get('role', '')}
Department: {user.get('department', '')}
"""


@router.get("/agents")
async def get_agents(user: dict = Depends(require_roles(*STAFF_ROLES))):
    errors = validate_core_office_registry()
    if errors:
        raise HTTPException(status_code=500, detail={"message": "Core Office registry invalid", "errors": errors})
    return list_core_agents()


@router.get("/capabilities")
async def get_capabilities(user: dict = Depends(require_roles(*STAFF_ROLES))):
    return [{"key": key, **value} for key, value in CAPABILITY_REGISTRY.items()]


@router.get("/brief")
async def get_executive_brief(user: dict = Depends(require_roles(*STAFF_ROLES))):
    brief = await _brief_snapshot()
    await audit_log(user, "view", "executive_brief", "current")
    return brief


@router.get("/sessions")
async def get_sessions(user: dict = Depends(require_roles(*STAFF_ROLES))):
    return await db.core_office_sessions.find(
        {"user_id": user["id"]}, {"_id": 0}
    ).sort("updated_at", -1).limit(50).to_list(50)


@router.get("/sessions/{session_id}/messages")
async def get_session_messages(session_id: str, user: dict = Depends(require_roles(*STAFF_ROLES))):
    session = await db.core_office_sessions.find_one(
        {"id": session_id, "user_id": user["id"]}, {"_id": 0}
    )
    if not session:
        raise HTTPException(status_code=404, detail="ไม่พบ session")
    messages = await db.core_office_messages.find(
        {"session_id": session_id}, {"_id": 0}
    ).sort("created_at", 1).limit(200).to_list(200)
    return {"session": session, "messages": messages}


@router.post("/chat")
async def office_chat(body: OfficeChatRequest, user: dict = Depends(require_roles(*STAFF_ROLES))):
    agent = get_core_agent(body.agent_key)
    if not agent:
        raise HTTPException(status_code=404, detail="ไม่พบ Core Office Agent")

    if body.session_id:
        session = await db.core_office_sessions.find_one(
            {"id": body.session_id, "user_id": user["id"]}, {"_id": 0}
        )
        if not session:
            raise HTTPException(status_code=404, detail="ไม่พบ session")
        if session["agent_key"] != body.agent_key:
            raise HTTPException(status_code=400, detail="Agent ไม่ตรงกับ session")
        session_id = body.session_id
    else:
        session_id = str(uuid.uuid4())
        await db.core_office_sessions.insert_one(
            {
                "id": session_id,
                "user_id": user["id"],
                "agent_key": body.agent_key,
                "title": body.message.strip()[:80],
                "created_at": now_iso(),
                "updated_at": now_iso(),
            }
        )

    history_docs = await db.core_office_messages.find(
        {"session_id": session_id}, {"_id": 0}
    ).sort("created_at", -1).limit(12).to_list(12)
    history = [
        {"role": item["role"], "content": item["content"]}
        for item in reversed(history_docs)
    ]

    context, evidence = await _build_agent_context(body.agent_key)
    user_prompt = f"ORGANIZATIONAL CONTEXT\n{context}\n\nUSER REQUEST\n{body.message.strip()}"

    try:
        reply = await chat_completion(
            _system_prompt(agent, user),
            history,
            user_prompt,
            session_id=f"core-office-{body.agent_key}-{session_id}",
        )
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"AI ตอบไม่สำเร็จ: {str(exc)[:200]}")

    confidence = "medium"
    if body.agent_key == "knowledge" and len(evidence) <= 1:
        confidence = "low"
    elif len(evidence) >= 3:
        confidence = "high"

    now = now_iso()
    await db.core_office_messages.insert_many(
        [
            {
                "id": str(uuid.uuid4()),
                "session_id": session_id,
                "role": "user",
                "content": body.message.strip(),
                "created_at": now,
            },
            {
                "id": str(uuid.uuid4()),
                "session_id": session_id,
                "role": "assistant",
                "content": reply,
                "agent_key": body.agent_key,
                "evidence": evidence,
                "confidence": confidence,
                "created_at": now_iso(),
            },
        ]
    )
    await db.core_office_sessions.update_one(
        {"id": session_id}, {"$set": {"updated_at": now_iso()}}
    )
    await audit_log(
        user,
        "chat",
        "core_office_agent",
        agent["id"],
        f"session={session_id}; evidence={len(evidence)}; confidence={confidence}",
    )

    return {
        "session_id": session_id,
        "agent_key": body.agent_key,
        "reply": reply,
        "evidence": evidence,
        "confidence": confidence,
        "approval_required": agent["approval_required"],
    }
