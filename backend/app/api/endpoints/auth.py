from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from backend.app.db.session import get_db
from backend.app.db.models import User as DBUser
from backend.app.schemas.auth_schemas import UserCreate, UserResponse, Token, UserLogin
from backend.app.auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_user
)

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    # 1. ตรวจสอบว่ามีผู้ใช้รายนี้อยู่แล้วหรือไม่
    db_user = db.query(DBUser).filter(DBUser.username == user_in.username).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ชื่อผู้ใช้นี้ถูกใช้งานแล้วในระบบ"
        )
    
    # 2. ทำการแฮชรหัสผ่านและบันทึกผู้ใช้ใหม่
    hashed_password = get_password_hash(user_in.password)
    new_user = DBUser(
        username=user_in.username,
        hashed_password=hashed_password,
        role=user_in.role or "user",
        department=user_in.department,
        confidentiality_level=user_in.confidentiality_level or "Internal"
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=Token)
def login_user(user_in: UserLogin, db: Session = Depends(get_db)):
    # 1. ค้นหาผู้ใช้จาก username
    db_user = db.query(DBUser).filter(DBUser.username == user_in.username).first()
    if not db_user or not verify_password(user_in.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 2. สร้าง JWT Token
    access_token = create_access_token(data={"sub": db_user.username})
    
    # 3. เตรียมข้อมูลส่งกลับ
    user_resp = UserResponse.model_validate(db_user)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user_resp
    }

# สำหรับรองรับ Swagger UI OAuth2 login
@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    db_user = db.query(DBUser).filter(DBUser.username == form_data.username).first()
    if not db_user or not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": db_user.username})
    user_resp = UserResponse.model_validate(db_user)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user_resp
    }

@router.get("/me", response_model=UserResponse)
def get_me(current_user: DBUser = Depends(get_current_user)):
    return current_user
