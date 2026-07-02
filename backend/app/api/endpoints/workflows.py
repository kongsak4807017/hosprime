import json
from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.agents.workflow_agent import WorkflowAgent
from backend.app.auth import get_current_user
from backend.app.db.models import AuditLog, HITLQueue, User, WorkflowRun
from backend.app.db.session import get_db

router = APIRouter()


@router.post("/trigger")
def trigger_backoffice_workflow(
    workflow_name: str,
    payload: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create an AI-assisted plan and place it in the HITL approval queue."""
    try:
        parameters = payload.get("payload", payload)
        result = WorkflowAgent.execute_backoffice_action(
            db,
            workflow_name,
            parameters,
        )
        db.add(
            AuditLog(
                workflow_id=str(result["id"]),
                user_id=current_user.username,
                agent_id="WorkflowPlanningAgent",
                action_type="workflow_plan_created",
                input_data=json.dumps(parameters, ensure_ascii=False),
                output_data=json.dumps(result, ensure_ascii=False),
                tools_used=json.dumps(["ai_planning", "hitl_queue"]),
                decisions=json.dumps(
                    {
                        "execution_authorized": False,
                        "external_actions_executed": False,
                    }
                ),
            )
        )
        db.commit()
        return {
            "status": "pending_approval",
            "workflow_id": str(result["id"]),
            "message": "Workflow plan created. No external action was executed.",
            "data": result,
        }
    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Workflow plan creation failed. Review server logs.",
        ) from exc


@router.get("/status/{workflow_id}")
def get_workflow_status(
    workflow_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    workflow = db.query(WorkflowRun).filter(WorkflowRun.id == workflow_id).first()
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    try:
        data = json.loads(workflow.payload_data or "{}")
    except json.JSONDecodeError:
        data = {}

    return {
        "workflow_id": str(workflow.id),
        "workflow_name": workflow.workflow_name,
        "status": workflow.status,
        "current_step": workflow.current_step,
        "parameters": data.get("parameters", {}),
        "steps": data.get("steps", []),
        "execution_mode": data.get("execution_mode", "unknown"),
        "external_actions_executed": data.get(
            "external_actions_executed", False
        ),
        "created_at": workflow.created_at,
    }


@router.post("/approve/{workflow_id}")
def approve_workflow_plan(
    workflow_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Approve the plan only. This endpoint does not execute tools or actions."""
    workflow = db.query(WorkflowRun).filter(WorkflowRun.id == workflow_id).first()
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    if workflow.status != "PENDING_APPROVAL":
        raise HTTPException(
            status_code=409,
            detail=f"Workflow cannot be approved from status {workflow.status}",
        )

    try:
        approval_token = f"APR-{uuid4().hex}"
        workflow.status = "APPROVED_NOT_EXECUTED"
        workflow.current_step = "Awaiting configured and authorized executor"

        queue_item = (
            db.query(HITLQueue)
            .filter(
                HITLQueue.workflow_id == str(workflow_id),
                HITLQueue.status == "pending",
            )
            .order_by(HITLQueue.id.desc())
            .first()
        )
        if queue_item:
            queue_item.status = "approved"
            queue_item.approved_by = current_user.username
            queue_item.approved_at = datetime.now(timezone.utc)
            queue_item.approval_token = approval_token

        db.add(
            AuditLog(
                workflow_id=str(workflow_id),
                user_id=current_user.username,
                action_type="workflow_plan_approved",
                input_data=json.dumps({"workflow_id": workflow_id}),
                output_data=json.dumps(
                    {
                        "status": workflow.status,
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
        db.refresh(workflow)
        return {
            "status": "approved_not_executed",
            "message": (
                "The plan was approved. No external action was executed because "
                "an authorized executor is not configured."
            ),
            "data": {
                "id": workflow.id,
                "status": workflow.status,
                "current_step": workflow.current_step,
                "external_actions_executed": False,
            },
        }
    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Workflow approval failed. Review server logs.",
        ) from exc
