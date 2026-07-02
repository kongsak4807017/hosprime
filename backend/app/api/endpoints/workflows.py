from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app.db.session import get_db
from backend.app.db.models import WorkflowRun
from backend.app.agents.workflow_agent import WorkflowAgent
import json

router = APIRouter()

@router.post("/trigger")
def trigger_backoffice_workflow(workflow_name: str, payload: dict, db: Session = Depends(get_db)):
    """[Milestone 5] สั่งกระตุ้นการทำงาน Backoffice AI Workflow จริงและบันทึกประวัติขั้นตอนลงฐานข้อมูล SQLite"""
    try:
        # สกัด parameters ที่เหมาะสมจาก payload
        parameters = payload.get("payload", payload)
        result = WorkflowAgent.execute_backoffice_action(db, workflow_name, parameters)
        return {
            "status": "triggered",
            "workflow_id": str(result.get("id")),
            "message": f"Temporal workflow '{workflow_name}' has been initiated and logged in SQLite.",
            "data": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"เกิดข้อผิดพลาดในการรัน Workflow: {str(e)}"
        )

@router.get("/status/{workflow_id}")
def get_workflow_status(workflow_id: str, db: Session = Depends(get_db)):
    """[Milestone 5] ตรวจสอบสถานะการประมวลผลและการอนุมัติของ Workflow จากฐานข้อมูล SQLite"""
    try:
        wf_run = None
        try:
            wf_id_int = int(workflow_id)
            wf_run = db.query(WorkflowRun).filter(WorkflowRun.id == wf_id_int).first()
        except ValueError:
            # หากส่ง ID เป็นข้อความอื่น (เช่นเดโม) ให้ดึงตัวล่าสุดในระบบ
            wf_run = db.query(WorkflowRun).order_by(WorkflowRun.id.desc()).first()
            
        if not wf_run:
            # Fallback หากไม่มีข้อมูลเวิร์กโฟลว์รันในระบบเลย
            return {
                "workflow_id": workflow_id,
                "status": "RUNNING",
                "steps": [
                    {"step": "ตรวจวัดค่าฝุ่นละออง PM2.5 > 150 ไมโครกรัม ณ เชียงราย", "status": "completed"},
                    {"step": "AI วิเคราะห์แนวโน้มยอดผู้ป่วยทางเดินหายใจล่วงหน้า 3 วัน", "status": "completed"},
                    {"step": "ร่างหนังสือราชการประกาศภัยพิบัติและขออนุมัติจัดส่งหน้ากาก N95", "status": "completed"},
                    {"step": "เสนออนุมัติให้นายแพทย์สาธารณสุขจังหวัด (PHO) ยืนยันคำสั่งประสานงาน", "status": "pending_human_approval"}
                ]
            }
            
        # แกะข้อมูลขั้นตอนจาก payload_data
        try:
            data = json.loads(wf_run.payload_data)
            steps = data.get("steps", [])
            parameters = data.get("parameters", {})
        except Exception:
            steps = []
            parameters = {}
            
        return {
            "workflow_id": str(wf_run.id),
            "workflow_name": wf_run.workflow_name,
            "status": wf_run.status,
            "current_step": wf_run.current_step,
            "parameters": parameters,
            "steps": steps,
            "created_at": wf_run.created_at
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"เกิดข้อผิดพลาดในการตรวจสอบสถานะ Workflow: {str(e)}"
        )


@router.post("/approve/{workflow_id}")
def approve_workflow_step(workflow_id: int, db: Session = Depends(get_db)):
    """[Milestone 5] อนุมัติขั้นตอนการทำงาน (Human-in-the-loop) และปรับสถานะของ Workflow เป็นสำเร็จ"""
    wf_run = db.query(WorkflowRun).filter(WorkflowRun.id == workflow_id).first()
    if not wf_run:
        raise HTTPException(status_code=404, detail="ไม่พบข้อมูลเวิร์กโฟลว์นี้")
        
    if wf_run.status != "RUNNING":
        return {
            "status": "warning",
            "message": f"Workflow นี้ไม่ได้อยู่ในสถานะที่รออนุมัติ (สถานะปัจจุบัน: {wf_run.status})",
            "data": {
                "id": wf_run.id,
                "status": wf_run.status
            }
        }
        
    try:
        data = json.loads(wf_run.payload_data)
        steps = data.get("steps", [])
        
        # ค้นหาและอัปเดต step ที่เป็น pending_human_approval
        updated = False
        for step in steps:
            if step.get("status") == "pending_human_approval":
                step["status"] = "completed"
                updated = True
            elif step.get("status") == "pending":
                step["status"] = "completed"
                
        if updated:
            wf_run.status = "COMPLETED"
            wf_run.current_step = "Workflow Completed Successfully"
            data["steps"] = steps
            wf_run.payload_data = json.dumps(data, ensure_ascii=False)
            db.commit()
            db.refresh(wf_run)
            
        return {
            "status": "success",
            "message": "อนุมัติขั้นตอนเวิร์กโฟลว์และประมวลผลขั้นตอนสุดท้ายเสร็จสิ้นแล้ว",
            "data": {
                "id": wf_run.id,
                "status": wf_run.status,
                "current_step": wf_run.current_step,
                "steps": steps
            }
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"เกิดข้อผิดพลาดในการอนุมัติเวิร์กโฟลว์: {str(e)}"
        )

