import json
import logging
from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from backend.app.auth import get_current_user
from backend.app.db.models import AuditLog, HITLQueue, User, WorkflowRun
from backend.app.db.session import get_db

router = APIRouter()
logger = logging.getLogger(__name__)


def _safe_json(value: str | None) -> dict:
    if not value:
        return {}
    try:
        result = json.loads(value)
        return result if isinstance(result, dict) else {"value": result}
    except json.JSONDecodeError:
        return {"unparsed": True}


@router.get("/queue")
def get_hitl_queue(
    status_value: str = Query(default="pending", alias="status"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    items = (
        db.query(HITLQueue)
        .filter(HITLQueue.status == status_value)
        .order_by(HITLQueue.requested_at.desc())
        .all()
    )
    return [
        {
            "id": item.id,
            "workflow_id": item.workflow_id,
            "task_id": item.task_id,
            "agent_id": item.agent_id,
            "status": item.status,
            "requested_at": (
                item.requested_at.isoformat() if item.requested_at else None
            ),
            "payload": _safe_json(item.payload),
            "context": _safe_json(item.context),
        }
        for item in items
    ]


@router.post("/approve/{queue_id}")
def approve_hitl_task(
    queue_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    item = db.query(HITLQueue).filter(HITLQueue.id == queue_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="HITL task not found")
    if item.status != "pending":
        raise HTTPException(status_code=409, detail=f"Task is already {item.status}")

    try:
        approval_token = f"APR-{uuid4().hex}"
        item.status = "approved"
        item.approved_by = current_user.username
        item.approved_at = datetime.now(timezone.utc)
        item.approval_token = approval_token

        workflow = None
        if item.workflow_id.isdigit():
            workflow = (
                db.query(WorkflowRun)
                .filter(WorkflowRun.id == int(item.workflow_id))
                .first()
            )
        if workflow and workflow.status == "PENDING_APPROVAL":
            workflow.status = "APPROVED_NOT_EXECUTED"
            workflow.current_step = "Awaiting configured and authorized executor"

        db.add(
            AuditLog(
                agent_id=item.agent_id,
                workflow_id=item.workflow_id,
                user_id=current_user.username,
                action_type="hitl_plan_approved",
                input_data=item.payload,
                output_data=json.dumps(
                    {
                        "status": "approved",
                        "external_actions_executed": False,
                    }
                ),
                tools_used=json.dumps(["hitl_gateway"]),
                decisions=json.dumps(
                    {
                        "plan_approved": True,
                        "execution_authorized": False,
                    }
                ),
                approval_token=approval_token,
            )
        )
        db.commit()
        return {
            "status": "approved_not_executed",
            "message": "Plan approved; no external action was executed.",
            "approval_token": approval_token,
        }
    except Exception as exc:
        db.rollback()
        logger.error("Failed to approve HITL task: %s", exc)
        raise HTTPException(status_code=500, detail="HITL approval failed") from exc


@router.post("/reject/{queue_id}")
def reject_hitl_task(
    queue_id: int,
    reason: str = Query(default="Rejected by reviewer", min_length=3, max_length=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    item = db.query(HITLQueue).filter(HITLQueue.id == queue_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="HITL task not found")
    if item.status != "pending":
        raise HTTPException(status_code=409, detail=f"Task is already {item.status}")

    try:
        item.status = "rejected"
        item.approved_by = current_user.username
        item.approved_at = datetime.now(timezone.utc)

        workflow = None
        if item.workflow_id.isdigit():
            workflow = (
                db.query(WorkflowRun)
                .filter(WorkflowRun.id == int(item.workflow_id))
                .first()
            )
        if workflow and workflow.status == "PENDING_APPROVAL":
            workflow.status = "REJECTED"
            workflow.current_step = "Plan rejected by human reviewer"

        db.add(
            AuditLog(
                agent_id=item.agent_id,
                workflow_id=item.workflow_id,
                user_id=current_user.username,
                action_type="hitl_plan_rejected",
                input_data=item.payload,
                output_data=json.dumps({"status": "rejected", "reason": reason}),
                tools_used=json.dumps(["hitl_gateway"]),
                decisions=json.dumps(
                    {
                        "plan_approved": False,
                        "reason": reason,
                    },
                    ensure_ascii=False,
                ),
            )
        )
        db.commit()
        return {"status": "rejected", "message": "Plan rejected."}
    except Exception as exc:
        db.rollback()
        logger.error("Failed to reject HITL task: %s", exc)
        raise HTTPException(status_code=500, detail="HITL rejection failed") from exc
