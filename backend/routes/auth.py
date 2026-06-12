import uuid
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import APIRouter, Depends, HTTPException, Request, Response

from core.database import db
from core.security import (
    JWT_ALGORITHM,
    clear_auth_cookies,
    create_access_token,
    create_refresh_token,
    get_current_user,
    get_jwt_secret,
    hash_password,
    require_roles,
    set_auth_cookies,
    verify_password,
)
from core.utils import audit_log, now_iso
from models.schemas import ROLES, LoginRequest, RegisterRequest

router = APIRouter(prefix="/auth", tags=["auth"])

MAX_ATTEMPTS = 5
LOCKOUT_MINUTES = 15


async def _check_lockout(identifier: str):
    rec = await db.login_attempts.find_one({"identifier": identifier})
    if rec and rec.get("count", 0) >= MAX_ATTEMPTS:
        locked_until = datetime.fromisoformat(rec["locked_until"])
        if datetime.now(timezone.utc) < locked_until:
            raise HTTPException(
                status_code=429,
                detail=f"บัญชีถูกล็อกชั่วคราว กรุณาลองใหม่ใน {LOCKOUT_MINUTES} นาที",
            )
        await db.login_attempts.delete_one({"identifier": identifier})


async def _record_failure(identifier: str):
    await db.login_attempts.update_one(
        {"identifier": identifier},
        {
            "$inc": {"count": 1},
            "$set": {
                "locked_until": (datetime.now(timezone.utc) + timedelta(minutes=LOCKOUT_MINUTES)).isoformat()
            },
        },
        upsert=True,
    )


@router.post("/login")
async def login(body: LoginRequest, request: Request, response: Response):
    email = body.email.lower().strip()
    ip = request.client.host if request.client else "unknown"
    identifier = f"{ip}:{email}"
    await _check_lockout(identifier)

    user = await db.users.find_one({"email": email})
    if not user or not verify_password(body.password, user["password_hash"]):
        await _record_failure(identifier)
        raise HTTPException(status_code=401, detail="อีเมลหรือรหัสผ่านไม่ถูกต้อง")
    if not user.get("is_active", True):
        raise HTTPException(status_code=403, detail="บัญชีนี้ถูกระงับการใช้งาน")

    await db.login_attempts.delete_one({"identifier": identifier})
    access = create_access_token(user["id"], user["email"], user["role"])
    refresh = create_refresh_token(user["id"])
    set_auth_cookies(response, access, refresh)
    user.pop("_id", None)
    user.pop("password_hash", None)
    await audit_log(user, "login", "user", user["id"])
    return {**user, "access_token": access}


@router.post("/logout")
async def logout(response: Response, user: dict = Depends(get_current_user)):
    clear_auth_cookies(response)
    await audit_log(user, "logout", "user", user["id"])
    return {"message": "ออกจากระบบสำเร็จ"}


@router.get("/me")
async def me(user: dict = Depends(get_current_user)):
    return user


@router.post("/refresh")
async def refresh_token(request: Request, response: Response):
    token = request.cookies.get("refresh_token")
    if not token:
        raise HTTPException(status_code=401, detail="No refresh token")
    try:
        payload = jwt.decode(token, get_jwt_secret(), algorithms=[JWT_ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
        user = await db.users.find_one({"id": payload["sub"]}, {"_id": 0, "password_hash": 0})
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        access = create_access_token(user["id"], user["email"], user["role"])
        new_refresh = create_refresh_token(user["id"])
        set_auth_cookies(response, access, new_refresh)
        return {"message": "refreshed"}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")


@router.post("/register", status_code=201)
async def register_user(body: RegisterRequest, admin: dict = Depends(require_roles("admin"))):
    email = body.email.lower().strip()
    if body.role not in ROLES:
        raise HTTPException(status_code=400, detail=f"บทบาทไม่ถูกต้อง: {body.role}")
    if await db.users.find_one({"email": email}):
        raise HTTPException(status_code=409, detail="อีเมลนี้ถูกใช้งานแล้ว")
    user = {
        "id": str(uuid.uuid4()),
        "email": email,
        "password_hash": hash_password(body.password),
        "full_name": body.full_name,
        "role": body.role,
        "department": body.department or "",
        "specialization": body.specialization or "",
        "phone": body.phone or "",
        "is_active": True,
        "created_at": now_iso(),
    }
    await db.users.insert_one(user)
    await audit_log(admin, "create", "user", user["id"], f"created {body.role}: {email}")
    user.pop("_id", None)
    user.pop("password_hash", None)
    return user


@router.get("/users")
async def list_users(admin: dict = Depends(require_roles("admin"))):
    users = await db.users.find({}, {"_id": 0, "password_hash": 0}).sort("created_at", -1).to_list(500)
    return users
