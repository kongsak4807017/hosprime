import logging

logger = logging.getLogger(__name__)

class WorkflowService:
    @staticmethod
    def start_temporal_workflow(workflow_name: str, payload: dict) -> str:
        """[Milestone 5] ประสานงานเปิดรัน Workflow สนับสนุนการตัดสินใจด้วย Temporal Engine"""
        wf_id = f"wf_temporal_{workflow_name}_auto"
        logger.info(f"Mock Temporal: Started workflow '{workflow_name}' with ID '{wf_id}' and payload {payload}")
        return wf_id

    @staticmethod
    def get_workflow_execution_status(workflow_id: str) -> str:
        """[Milestone 5] ตรวจเช็คสถานะของ Workflow ใน Temporal"""
        return "RUNNING"
