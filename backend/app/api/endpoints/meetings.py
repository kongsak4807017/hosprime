from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import os
import shutil
from backend.app.db.session import get_db
from backend.app.db.models import Meeting, ActionItem
from backend.app.agents.meeting_memory_agent import MeetingMemoryAgent

router = APIRouter()

@router.post("/upload-audio")
async def upload_meeting_audio(
    file: UploadFile = File(...),
    title: str = Form(...),
    db: Session = Depends(get_db)
):
    """[Milestone 2] อัปโหลดไฟล์บันทึกเสียงการประชุมสาธารณสุข และใช้ Agent วิเคราะห์มติจริงลงฐานข้อมูล SQLite"""
    # สร้างโฟลเดอร์สำหรับเก็บไฟล์เสียงชั่วคราว
    upload_dir = os.path.join("storage", "meetings")
    os.makedirs(upload_dir, exist_ok=True)
    
    file_path = os.path.join(upload_dir, file.filename)
    
    try:
        # บันทึกไฟล์ลงดิสก์
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # เรียกใช้ MeetingMemoryAgent สกัดความและบันทึก DB
        result = MeetingMemoryAgent.process_meeting_recording(db, title, file_path)
        return {
            "status": "success",
            "message": "Audio file uploaded and processed successfully [Milestone 2 Active]",
            "data": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing meeting recording: {str(e)}"
        )

@router.get("/list")
def list_meetings(db: Session = Depends(get_db)):
    """[Milestone 2] ดึงประวัติการประชุมและ Action Items จากฐานข้อมูล SQLite จริง"""
    try:
        meetings = db.query(Meeting).order_by(Meeting.id.desc()).all()
        result = []
        for m in meetings:
            action_items = db.query(ActionItem).filter(ActionItem.meeting_id == m.id).all()
            result.append({
                "id": m.id,
                "title": m.title,
                "date": m.date or "2026-06-16",
                "summary": m.summary,
                "action_items": [
                    {
                        "task": ai.task,
                        "assignee": ai.assignee,
                        "due_date": ai.due_date,
                        "status": ai.status
                    } for ai in action_items
                ]
            })
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch meetings: {str(e)}"
        )


from pydantic import BaseModel
from backend.app.services.document_parser import DocumentParser
from backend.app.services.gemini_service import GeminiService
from backend.app.auth import get_current_user
from backend.app.db.models import User as DBUser

class MeetingAskRequest(BaseModel):
    question: str

@router.post("/{meeting_id}/upload-document")
async def upload_meeting_document(
    meeting_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user)
):
    """[Milestone 2 - NotebookLM] อัปโหลดเอกสารประกอบการประชุม (PDF/DOCX/TXT/MD) แนบเข้าบันทึกการประชุม"""
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    if not meeting:
        raise HTTPException(status_code=404, detail="ไม่พบข้อมูลบันทึกประชุมนี้")
        
    upload_dir = os.path.join("storage", "meetings")
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # สกัดข้อความจากเอกสาร
        pages_data = DocumentParser.parse_document(file_path)
        parsed_text = "\n".join([page["text"] for page in pages_data])
        
        # แนบต่อท้ายบันทึกคำสนทนา
        meeting.transcript = (meeting.transcript or "") + f"\n\n[เอกสารแนบประกอบการประชุม: {file.filename}]\n" + parsed_text
        db.commit()
        db.refresh(meeting)
        
        return {
            "status": "success",
            "message": f"สกัดเนื้อหาจากไฟล์เอกสาร '{file.filename}' และเพิ่มเข้าบันทึกประชุมสำเร็จ",
            "filename": file.filename
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"เกิดข้อผิดพลาดในการสกัดไฟล์เอกสาร: {str(e)}"
        )


@router.post("/{meeting_id}/ask")
def ask_meeting_oracle(
    meeting_id: int,
    req: MeetingAskRequest,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user)
):
    """[Milestone 2 - NotebookLM] แชทถามตอบอ้างอิงข้อมูลเฉพาะภายในบันทึกการประชุมและการประชุมแนบนั้นๆ"""
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    if not meeting:
        raise HTTPException(status_code=404, detail="ไม่พบข้อมูลบันทึกประชุมนี้")
        
    context = (
        f"หัวข้อการประชุม: {meeting.title}\n"
        f"วันที่จัดประชุม: {meeting.date or '2026-06-16'}\n\n"
        f"สรุปมติที่ประชุมหลัก:\n{meeting.summary or 'ไม่มี'}\n\n"
        f"บันทึกบทสนทนาถอดรหัสและเนื้อหาเอกสารแนบประกอบ:\n{meeting.transcript or 'ไม่มี'}"
    )
    
    system_instruction = (
        "คุณคือ AI Meeting Oracle ประจำสำนักงานสาธารณสุข "
        "หน้าที่ของคุณคือตอบคำถามโดยอ้างอิงจากบริบทการประชุมที่แนบมาด้านล่างนี้เท่านั้น "
        "ห้ามอ้างอิงข้อมูลภายนอกบริบทเด็ดขาด ตอบเป็นภาษาไทยด้วยข้อมูลและข้อเท็จจริงในบริบท "
        "หากไม่สามารถหาคำตอบได้ในบริบท ให้แจ้งผู้ใช้ตรงๆ ว่า 'ไม่พบข้อมูลนี้ในบันทึกและเอกสารแนบของการประชุม'"
    )
    
    prompt = f"บริบทข้อมูลการประชุม:\n{context}\n\nคำถาม: {req.question}"
    
    try:
        response = GeminiService.generate_response(prompt, system_instruction=system_instruction)
        return {"response": response, "status": "success"}
    except Exception as e:
        # Fallback ตอบจำลอง
        return {
            "response": f"ขออภัย ระบบ RAG ขัดข้อง แต่จากการสืบค้นในบันทึกการประชุมหัวข้อ '{meeting.title}' (มติ: {meeting.summary[:100]}...) ระบบไม่สามารถสืบค้นเชิงลึกให้คุณได้ในขณะนี้",
            "status": "fallback"
        }
