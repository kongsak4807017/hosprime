import os
import uuid

import httpx
from emergentintegrations.llm.chat import LlmChat, UserMessage

from core.database import db

DEFAULT_SETTINGS = {
    "provider": "emergent",      # "emergent" (Universal Key) | "custom" (OpenAI-compatible endpoint / local model)
    "llm_provider": "openai",    # for emergent: openai | anthropic | gemini
    "model": "gpt-5.2",
    "base_url": "",              # for custom e.g. http://localhost:11434/v1 (Ollama) or https://api.openai.com/v1
    "api_key": "",               # for custom
}

EMERGENT_MODELS = {
    "openai": ["gpt-5.2", "gpt-5.1", "gpt-5", "gpt-5-mini", "gpt-5-nano", "gpt-4.1", "gpt-4o", "gpt-4o-mini"],
    "anthropic": ["claude-sonnet-4-6", "claude-sonnet-4-5-20250929", "claude-haiku-4-5-20251001"],
    "gemini": ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-3-flash-preview"],
}


async def get_ai_settings() -> dict:
    doc = await db.settings.find_one({"_id": "ai"})
    if not doc:
        return DEFAULT_SETTINGS.copy()
    return {**DEFAULT_SETTINGS, **{k: v for k, v in doc.items() if k != "_id"}}


async def save_ai_settings(settings: dict):
    await db.settings.update_one({"_id": "ai"}, {"$set": settings}, upsert=True)


async def chat_completion(system_message: str, history: list, user_text: str, session_id: str = "") -> str:
    """Unified LLM call. history = [{"role": "user"|"assistant", "content": str}]"""
    settings = await get_ai_settings()
    if settings["provider"] == "custom":
        return await _custom_chat(settings, system_message, history, user_text)
    return await _emergent_chat(settings, system_message, history, user_text, session_id)


async def _emergent_chat(settings: dict, system_message: str, history: list, user_text: str, session_id: str) -> str:
    api_key = os.environ.get("EMERGENT_LLM_KEY")
    if not api_key:
        raise RuntimeError("ไม่พบ EMERGENT_LLM_KEY ในระบบ")
    chat = LlmChat(
        api_key=api_key,
        session_id=session_id or str(uuid.uuid4()),
        system_message=system_message,
    ).with_model(settings["llm_provider"], settings["model"])
    if history:
        transcript = "\n".join(
            f"{'ผู้ใช้' if m['role'] == 'user' else 'ผู้ช่วย'}: {m['content']}" for m in history
        )
        prompt = f"บทสนทนาก่อนหน้า:\n{transcript}\n\nข้อความล่าสุดจากผู้ใช้: {user_text}"
    else:
        prompt = user_text
    response = await chat.send_message(UserMessage(text=prompt))
    return str(response)


async def _custom_chat(settings: dict, system_message: str, history: list, user_text: str) -> str:
    base_url = (settings.get("base_url") or "").rstrip("/")
    if not base_url:
        raise RuntimeError("ยังไม่ได้ตั้งค่า Base URL ของ AI endpoint")
    messages = [{"role": "system", "content": system_message}]
    messages += [{"role": m["role"], "content": m["content"]} for m in history]
    messages.append({"role": "user", "content": user_text})
    headers = {"Content-Type": "application/json"}
    if settings.get("api_key"):
        headers["Authorization"] = f"Bearer {settings['api_key']}"
    async with httpx.AsyncClient(timeout=120) as client:
        resp = await client.post(
            f"{base_url}/chat/completions",
            json={"model": settings["model"], "messages": messages},
            headers=headers,
        )
        if resp.status_code != 200:
            raise RuntimeError(f"AI endpoint ตอบกลับ {resp.status_code}: {resp.text[:200]}")
        data = resp.json()
        return data["choices"][0]["message"]["content"]
