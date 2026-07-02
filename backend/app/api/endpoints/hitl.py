import json
import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from backend.app.db.session import get_db
from backend.app.db.models import HITLQueue, AuditLog

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/queue")
def get_hitl_queue(
    status: str = Query(default="pending"),
    db: Session = Depends(get_db)
):
    """
    ดึงรายการที่กำลังรอการตรวจสอบหรืออนุมัติจากมนุษย์ (HITL Queue)
    """
    try:
        queue_items = db.query(HITLQueue).filter(HITLQueue.status == status).order_by(HITLQueue.requested_at.desc()).all()
        result = []
        for item in queue_items:
            result.append({
                "id": item.id,
                "workflow_id": item.workflow_id,
                "task_id": item.task_id,
                "agent_id": item.agent_id,
                "status": item.status,
                "requested_at": item.requested_at.isoformat() if item.requested_at else None,
                "payload": json.loads(item.payload) if item.payload else {},
                "context": json.loads(item.context) if item.context else {}
            })
        return result
    except Exception as e:
        logger.error(f"Failed to fetch HITL queue: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch HITL queue: {str(e)}")

@router.post("/approve/{queue_id}")
def approve_hitl_task(
    queue_id: int,
    approved_by: Optional[str] = Query(default="admin"),
    db: Session = Depends(get_db)
):
    """
    อนุมัติขั้นตอนงานที่รออยู่ในคิว
    """
    item = db.query(HITLQueue).filter(HITLQueue.id == queue_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="HITL task not found")
        
    if item.status != "pending":
        raise HTTPException(status_code=400, detail=f"Task is already {item.status}")

    try:
        import datetime
        item.status = "approved"
        item.approved_by = approved_by
        item.approved_at = datetime.datetime.now()
        item.approval_token = f"TOKEN-{item.workflow_id}-{int(datetime.datetime.now().timestamp())}"
        
        # บันทึกลง Audit Log
        audit = AuditLog(
            agent_id=item.agent_id,
            workflow_id=item.workflow_id,
            user_id=approved_by,
            action_type="hitl_approved",
            input_data=item.payload,
            output_data=json.dumps({"status": "approved", "token": item.approval_token}),
            tools_used=json.dumps(["hitl_gateway"]),
            decisions=json.dumps({"hitl_decision": "approved"}),
            approval_token=item.approval_token
        )
        db.add(audit)
        db.commit()
        
        return {
            "status": "success",
            "message": "Task approved successfully",
            "approval_token": item.approval_token
        }
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to approve task: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/reject/{queue_id}")
def reject_hitl_task(
    queue_id: int,
    rejected_by: Optional[str] = Query(default="admin"),
    reason: Optional[str] = Query(default="Rejected by user"),
    db: Session = Depends(get_db)
):
    """
    ปฏิเสธขั้นตอนงานที่รออยู่ในคิว
    """
    item = db.query(HITLQueue).filter(HITLQueue.id == queue_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="HITL task not found")
        
    if item.status != "pending":
        raise HTTPException(status_code=400, detail=f"Task is already {item.status}")

    try:
        import datetime
        item.status = "rejected"
        item.approved_by = rejected_by
        item.approved_at = datetime.datetime.now()
        
        # บันทึกลง Audit Log
        audit = AuditLog(
            agent_id=item.agent_id,
            workflow_id=item.workflow_id,
            user_id=rejected_by,
            action_type="hitl_rejected",
            input_data=item.payload,
            output_data=json.dumps({"status": "rejected", "reason": reason}),
            tools_used=json.dumps(["hitl_gateway"]),
            decisions=json.dumps({"hitl_decision": "rejected", "reason": reason})
        )
        db.add(audit)
        db.commit()
        
        return {
            "status": "success",
            "message": "Task rejected successfully"
        }
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to reject task: {e}")
        raise HTTPException(status_code=500, detail=str(e))
