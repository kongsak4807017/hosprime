import logging
from uuid import uuid4

logger = logging.getLogger(__name__)


class WorkflowService:
    """Workflow execution boundary.

    The current repository does not contain a Temporal worker or tool executor.
    Therefore this service creates a plan identifier only and must not report
    that an external workflow has started or completed.
    """

    @staticmethod
    def create_plan_reference(workflow_name: str) -> str:
        reference = f"plan_{workflow_name}_{uuid4().hex[:12]}"
        logger.info(
            "Created plan-only workflow reference '%s'. No external action was executed.",
            reference,
        )
        return reference

    @staticmethod
    def start_temporal_workflow(workflow_name: str, payload: dict) -> str:
        """Backward-compatible alias returning a plan-only reference."""
        return WorkflowService.create_plan_reference(workflow_name)

    @staticmethod
    def get_workflow_execution_status(workflow_id: str) -> str:
        return "PLAN_ONLY_NOT_EXECUTED"
