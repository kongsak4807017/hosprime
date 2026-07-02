import json
import logging
from typing import Any

from sqlalchemy.orm import Session

from backend.app.agents.agents import log_agent_activity
from backend.app.db.models import HITLQueue, WorkflowRun
from backend.app.services.ai_gateway import AIGateway
from backend.app.services.workflow_service import WorkflowService

logger = logging.getLogger(__name__)


class WorkflowAgent:
    @staticmethod
    def _validate_plan(raw: dict[str, Any]) -> list[dict[str, str]]:
        steps = raw.get("steps") if isinstance(raw, dict) else None
        if not isinstance(steps, list) or not 1 <= len(steps) <= 10:
            raise ValueError("Workflow plan must contain 1 to 10 steps.")

        validated: list[dict[str, str]] = []
        for index, step in enumerate(steps, start=1):
            if not isinstance(step, dict):
                raise ValueError(f"Workflow step {index} must be an object.")
            description = str(step.get("step", "")).strip()
            if not description:
                raise ValueError(f"Workflow step {index} has no description.")
            # An LLM can propose work but cannot mark real-world work completed.
            validated.append(
                {
                    "step": description[:1000],
                    "status": "planned",
                }
            )
        return validated

    @staticmethod
    def execute_backoffice_action(
        db: Session,
        workflow_name: str,
        parameters: dict,
    ) -> dict:
        """Create a governed workflow plan; do not execute external actions."""
        normalized_name = workflow_name.strip()[:255]
        if not normalized_name:
            raise ValueError("workflow_name is required")
        if not isinstance(parameters, dict):
            raise ValueError("parameters must be an object")

        system_instruction = (
            "You are the HosPrime Workflow Planning Agent. "
            "Create a plan only. You have not executed any step. "
            "Return JSON with key 'steps', containing 3 to 7 objects. "
            "Each object contains only 'step', written in Thai. "
            "Include verification, evidence review, risk control, human approval, "
            "and outcome measurement where relevant. Never use the word completed."
        )
        prompt = (
            f"Workflow name: {normalized_name}\n"
            f"Parameters: {json.dumps(parameters, ensure_ascii=False)}\n"
            "Create an auditable execution plan."
        )

        raw_plan = AIGateway.generate_json_response(
            db=db,
            prompt=prompt,
            system_instruction=system_instruction,
            model_name="gemini-2.5-flash",
            agent_id="WorkflowPlanningAgent",
        )
        steps = WorkflowAgent._validate_plan(raw_plan)
        plan_reference = WorkflowService.create_plan_reference(normalized_name)

        workflow_run = WorkflowRun(
            workflow_name=normalized_name,
            status="PENDING_APPROVAL",
            current_step="Human review of proposed plan",
            payload_data=json.dumps(
                {
                    "parameters": parameters,
                    "steps": steps,
                    "plan_reference": plan_reference,
                    "execution_mode": "plan_only",
                    "external_actions_executed": False,
                },
                ensure_ascii=False,
            ),
        )
        db.add(workflow_run)
        db.commit()
        db.refresh(workflow_run)

        queue_item = HITLQueue(
            workflow_id=str(workflow_run.id),
            task_id=f"review_plan_{workflow_run.id}",
            agent_id="WorkflowPlanningAgent",
            status="pending",
            payload=json.dumps(
                {
                    "workflow_name": normalized_name,
                    "steps": steps,
                },
                ensure_ascii=False,
            ),
            context=json.dumps(
                {
                    "parameters": parameters,
                    "external_actions_executed": False,
                },
                ensure_ascii=False,
            ),
        )
        db.add(queue_item)
        db.commit()
        db.refresh(queue_item)

        result = {
            "id": workflow_run.id,
            "workflow_name": workflow_run.workflow_name,
            "status": workflow_run.status,
            "current_step": workflow_run.current_step,
            "plan_reference": plan_reference,
            "hitl_queue_id": queue_item.id,
            "steps": steps,
            "external_actions_executed": False,
        }
        log_agent_activity(
            db,
            "WorkflowPlanningAgent",
            "create_workflow_plan",
            {"workflow_name": normalized_name},
            result,
        )
        return result
