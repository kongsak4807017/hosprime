import os
import shutil
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from backend.app.db.session import get_db
from backend.app.db.models import Document, EntityRelation
from backend.app.schemas.schemas import DocumentResponse, EntityRelationResponse, DocumentUpdate
from backend.app.core.config import settings
from backend.app.agents.agents import KnowledgeIngestionAgent

router = APIRouter()

@router.post("/upload", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    title: Optional[str] = Form(None),
    confidentiality_level: Optional[str] = Form("Internal"),
    db: Session = Depends(get_db)
):
    """อัปโหลดไฟล์เอกสารเข้าสู่ระบบและเริ่มกระบวนการ Ingest & Extract ทันที"""
    # 1. ตรวจสอบนามสกุลไฟล์
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in [".pdf", ".docx", ".txt", ".md"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file format. Please upload PDF, DOCX, TXT, or MD."
        )

    # 2. บันทึกไฟล์ลง Disk
    doc_title = title or os.path.splitext(file.filename)[0]
    safe_filename = f"{doc_title.replace(' ', '_')}_{int(os.urandom(4).hex(), 16)}{ext}"
    dest_path = os.path.join(settings.DOCUMENT_DIR, safe_filename)
    
    try:
        with open(dest_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save file: {str(e)}"
        )

    # 3. เรียกใช้ Agent ในการนำข้อมูลเข้า
    try:
        doc = KnowledgeIngestionAgent.ingest(
            db=db,
            file_path=dest_path,
            title=doc_title,
            confidentiality_level=confidentiality_level
        )
        return doc
    except Exception as e:
        # หากล้มเหลว ลบไฟล์ที่อัปโหลด
        if os.path.exists(dest_path):
            os.remove(dest_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process document: {str(e)}"
        )

@router.get("/catalog", response_model=List[DocumentResponse])
def get_catalog(
    document_type: Optional[str] = None,
    department: Optional[str] = None,
    program: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """ดึงรายการเอกสารพร้อมตัวกรอง (Filters)"""
    query = db.query(Document)
    
    if document_type:
        query = query.filter(Document.document_type == document_type)
    if department:
        query = query.filter(Document.department == department)
    if program:
        query = query.filter(Document.program == program)
    if status:
        query = query.filter(Document.status == status)
        
    return query.order_by(Document.created_at.desc()).all()

@router.get("/{doc_id}/relations", response_model=List[EntityRelationResponse])
def get_document_relations(doc_id: int, db: Session = Depends(get_db)):
    """ดึงข้อมูลความสัมพันธ์ (HODT Entities) ที่สกัดออกมาจากเอกสาร"""
    relations = db.query(EntityRelation).filter(EntityRelation.document_id == doc_id).all()
    return relations

@router.delete("/{doc_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(doc_id: int, db: Session = Depends(get_db)):
    """ลบเอกสารและข้อมูลที่เกี่ยวข้องทั้งหมด"""
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
        
    # ลบไฟล์ใน Disk
    if os.path.exists(doc.file_path):
        try:
            os.remove(doc.file_path)
        except Exception as e:
            pass
            
    db.delete(doc)
    db.commit()
    return None
