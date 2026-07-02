import json
import logging
from sqlalchemy.orm import Session
from backend.app.db.models import WorkflowRun
from backend.app.services.workflow_service import WorkflowService
from backend.app.services.gemini_service import GeminiService
from backend.app.agents.agents import log_agent_activity

logger = logging.getLogger(__name__)

class WorkflowAgent:
    @staticmethod
    def execute_backoffice_action(db: Session, workflow_name: str, parameters: dict) -> dict:
        """[Milestone 5] ควบคุมการเปิดทำงานและการอนุมัติขั้นตอนการทำงานผ่านปัญญาประดิษฐ์สนับสนุน Backoffice"""
        logger.info(f"WorkflowAgent executing workflow: {workflow_name} with params: {parameters}")
        
        # 1. เรียกใช้ Gemini เพื่อวิเคราะห์และสร้างขั้นตอนการรันงานอย่างเป็นโครงสร้าง
        system_instruction = (
            "You are the Health Organization OS Workflow Agent. "
            "Analyze the requested backoffice workflow and parameters. "
            "Generate 3 to 5 realistic sequential steps for this workflow. "
            "Return ONLY a JSON object with a single key 'steps' which contains a list of objects. "
            "Each object must have 'step' (a detailed Thai string explaining the step) and 'status' "
            "(either 'completed' or 'pending_human_approval' or 'pending'). "
            "Ensure that at least one step is 'pending_human_approval' if human verification is required (e.g., final approval)."
        )
        
        prompt = (
            f"Workflow Name: {workflow_name}\n"
            f"Parameters: {json.dumps(parameters, ensure_ascii=False)}\n\n"
            f"Please generate the execution steps."
        )
        
        extracted_steps = GeminiService.generate_json_response(prompt, system_instruction)
        
        # Fallback หากเรียก Gemini ไม่ได้หรือวิเคราะห์ขัดข้อง
        if not extracted_steps or "steps" not in extracted_steps:
            if workflow_name == "DisasterAlert":
                extracted_steps = {
                    "steps": [
                        {"step": f"ตรวจวัดค่าฝุ่นละออง PM2.5 ในพื้นที่ {parameters.get('location', 'เชียงราย')} เกินค่ามาตรฐาน (วิกฤต)", "status": "completed"},
                        {"step": "AI คาดการณ์ยอดผู้ป่วยทางเดินหายใจล่วงหน้า 3 วันและแจ้งเตือนหน่วยงานที่เกี่ยวข้อง", "status": "completed"},
                        {"step": f"ร่างหนังสือราชการประกาศภัยพิบัติและขออนุมัติจัดส่งหน้ากาก N95 จำนวน {parameters.get('mask_qty', '50,000')} ชิ้น", "status": "completed"},
                        {"step": "เสนออนุมัติให้นายแพทย์สาธารณสุขจังหวัด (PHO) ลงนามยืนยันคำสั่งเพื่อประสาน อบจ. ท้องถิ่น", "status": "pending_human_approval"}
                    ]
                }
            else:
                extracted_steps = {
                    "steps": [
                        {"step": f"เริ่มต้นระบบประมวลผลสำหรับเวิร์กโฟลว์ {workflow_name}", "status": "completed"},
                        {"step": "ตรวจสอบทรัพยากรและความพร้อมของระบบย่อย", "status": "completed"},
                        {"step": "เสนอผู้บริหารพิจารณาอนุมัติสั่งการดำเนินการ", "status": "pending_human_approval"}
                    ]
                }
        
        # 2. เริ่มรัน Temporal workflow จำลอง
        temporal_wf_id = WorkflowService.start_temporal_workflow(workflow_name, parameters)
        
        # ค้นหา step ที่กำลังรอการตัดสินใจ
        current_step = "Human Approval Pending"
        for st in extracted_steps.get("steps", []):
            if st.get("status") == "pending_human_approval":
                current_step = st.get("step")
                break
                
        # 3. บันทึกลงตาราง WorkflowRun ใน SQLite
        wf_run = WorkflowRun(
            workflow_name=workflow_name,
            status="RUNNING" if any(s.get("status") != "completed" for s in extracted_steps.get("steps", [])) else "COMPLETED",
            current_step=current_step,
            payload_data=json.dumps({
                "parameters": parameters,
                "steps": extracted_steps.get("steps", []),
                "temporal_id": temporal_wf_id
            }, ensure_ascii=False)
        )
        db.add(wf_run)
        db.commit()
        db.refresh(wf_run)
        
        result = {
            "id": wf_run.id,
            "workflow_name": wf_run.workflow_name,
            "status": wf_run.status,
            "current_step": wf_run.current_step,
            "temporal_id": temporal_wf_id,
            "steps": extracted_steps.get("steps", [])
        }
        
        log_agent_activity(db, "WorkflowAgent", "execute_workflow", {"workflow_name": workflow_name}, result)
        return result

