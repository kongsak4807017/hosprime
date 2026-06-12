from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from core.ai import EMERGENT_MODELS, chat_completion, get_ai_settings, save_ai_settings
from core.security import require_roles
from core.utils import audit_log

router = APIRouter(prefix="/ai", tags=["ai-settings"])


class AISettingsUpdate(BaseModel):
    provider: str
    llm_provider: Optional[str] = "openai"
    model: str
    base_url: Optional[str] = ""
    api_key: Optional[str] = None  # None = keep existing


def _mask(settings: dict) -> dict:
    s = dict(settings)
    key = s.get("api_key") or ""
    s["api_key_set"] = bool(key)
    s["api_key"] = f"••••{key[-4:]}" if key else ""
    return s


@router.get("/settings")
async def get_settings(user: dict = Depends(require_roles("admin"))):
    settings = await get_ai_settings()
    return {**_mask(settings), "available_models": EMERGENT_MODELS}


@router.put("/settings")
async def update_settings(body: AISettingsUpdate, user: dict = Depends(require_roles("admin"))):
    if body.provider not in ("emergent", "custom"):
        raise HTTPException(status_code=400, detail="provider ต้องเป็น emergent หรือ custom")
    if body.provider == "emergent" and body.llm_provider not in EMERGENT_MODELS:
        raise HTTPException(status_code=400, detail="llm_provider ไม่ถูกต้อง (openai/anthropic/gemini)")
    if body.provider == "custom" and not body.base_url:
        raise HTTPException(status_code=400, detail="กรุณาระบุ Base URL สำหรับ custom endpoint")
    current = await get_ai_settings()
    updates = {
        "provider": body.provider,
        "llm_provider": body.llm_provider or "openai",
        "model": body.model,
        "base_url": body.base_url or "",
    }
    if body.api_key is not None:
        updates["api_key"] = body.api_key
    else:
        updates["api_key"] = current.get("api_key", "")
    await save_ai_settings(updates)
    await audit_log(user, "update", "ai_settings", "ai", f"provider={body.provider} model={body.model}")
    return {**_mask(await get_ai_settings()), "available_models": EMERGENT_MODELS}


@router.post("/settings/test")
async def test_connection(user: dict = Depends(require_roles("admin"))):
    try:
        reply = await chat_completion(
            "You are a connection tester. Answer in Thai, very briefly.",
            [],
            "ตอบสั้นๆ ว่า 'เชื่อมต่อสำเร็จ' พร้อมบอกชื่อโมเดลที่คุณเป็น",
            session_id="ai-settings-test",
        )
        return {"success": True, "reply": reply}
    except Exception as e:
        return {"success": False, "error": str(e)}
