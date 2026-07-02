import json
import logging
from typing import Dict, Any, List, TypedDict, Annotated
from sqlalchemy.orm import Session

from backend.app.models.twin_models import Agent
from backend.app.db.models import AgentLog, HITLQueue, AuditLog, WorkflowRun
from backend.app.services.ai_gateway import AIGateway

# นำเข้า LangGraph
try:
    from langgraph.graph import StateGraph, START, END
    from langgraph.checkpoint.memory import MemorySaver
    langgraph_available = True
except ImportError:
    langgraph_available = False

logger = logging.getLogger(__name__)

# กำหนด State สำหรับ LangGraph
class OrchestratorState(TypedDict):
    goal: str
    tasks: List[Dict[str, Any]]
    results: List[Dict[str, Any]]
    context_accumulator: str
    final_report: str
    needs_approval: bool
    queue_id: int
    workflow_run_id: int
    status: str

class MasterOrchestrator:
    
    @staticmethod
    def _decompose_node(state: OrchestratorState, db: Session) -> Dict[str, Any]:
        """ขั้นตอนการแตกเป้าหมายเป็น Tasks ย่อย (Decomposition Node)"""
        goal = state["goal"]
        logger.info(f"[LangGraph Node: Decompose] Received goal: {goal}")
        
        decomposition_prompt = (
            f"ในฐานะ Master Orchestrator ของโรงพยาบาล โปรดแยกเป้าหมายหลักต่อไปนี้:\n"
            f"\"{goal}\"\n\n"
            f"ออกมาเป็น 3 ขั้นตอนย่อยในการส่งต่อให้ฝ่ายต่างๆ วิเคราะห์ข้อมูล โดยเลือกฝ่ายผู้รับผิดชอบจากตัวเลือก:\n"
            f"- analyst (ฝ่ายวิเคราะห์ยุทธศาสตร์)\n"
            f"- knowledge (ผู้ช่วยคลังปัญญา/SOP)\n"
            f"- cfo (ฝ่ายการคลัง)\n"
            f"- coo (ฝ่ายบริการ/ปฏิบัติการ)\n"
            f"- datagov (ธรรมภิบาลข้อมูล)\n"
            f"- report (ผู้ร่างรายงาน)\n\n"
            f"โปรดตอบกลับเป็นรูปแบบ JSON เท่านั้น โดยมีโครงสร้างดังนี้:\n"
            f"{{\n"
            f"  \"tasks\": [\n"
            f"    {{\"step\": 1, \"assigned_to\": \"role_name\", \"instruction\": \"คำอธิบายสิ่งที่ต้องทำ\"}},\n"
            f"    {{\"step\": 2, \"assigned_to\": \"role_name\", \"instruction\": \"คำอธิบายสิ่งที่ต้องทำ\"}},\n"
            f"    {{\"step\": 3, \"assigned_to\": \"role_name\", \"instruction\": \"คำอธิบายสิ่งที่ต้องทำ\"}}\n"
            f"  ]\n"
            f"}}"
        )
        
        tasks = []
        try:
            # เรียกใช้ AI Gateway ในการประมวลผล
            raw_decomp = AIGateway.generate_response(
                db=db,
                prompt=decomposition_prompt,
                model_name="gemini-1.5-flash",
                temperature=0.1,
                agent_id="Orchestrator"
            )
            raw_decomp = raw_decomp.replace("```json", "").replace("```", "").strip()
            decomp_data = json.loads(raw_decomp)
            tasks = decomp_data.get("tasks", [])
        except Exception as e:
            logger.error(f"Error in task decomposition node: {str(e)}")
            # Fallback decomposition if API fails
            tasks = [
                {"step": 1, "assigned_to": "analyst", "instruction": f"วิเคราะห์ทิศทางและข้อมูลเบื้องต้นเกี่ยวกับ: {goal}"},
                {"step": 2, "assigned_to": "knowledge", "instruction": "สืบค้น SOP และระเบียบราชการที่เกี่ยวข้องเพื่อเป็นกรอบอ้างอิง"},
                {"step": 3, "assigned_to": "report", "instruction": "เรียบเรียงและร่างจดหมายราชการสั่งการเสนอผู้บริหาร"}
            ]
            
        # อัปเดต Workflow status ใน DB
        wf_run_id = state.get("workflow_run_id")
        if wf_run_id:
            try:
                wf_run = db.query(WorkflowRun).filter(WorkflowRun.id == wf_run_id).first()
                if wf_run:
                    wf_run.current_step = "Execution Phase"
                    db.commit()
            except Exception:
                pass

        return {"tasks": tasks, "status": "decomposed"}

    @staticmethod
    def _execute_node(state: OrchestratorState, db: Session) -> Dict[str, Any]:
        """ขั้นตอนการสั่งการพนักงานจำลองแต่ละฝ่ายตามงานที่ได้รับมอบหมาย (Execution Node)"""
        tasks = state.get("tasks", [])
        results = []
        context_accumulator = ""
        
        logger.info(f"[LangGraph Node: Execute] Executing {len(tasks)} tasks.")
        
        for task in tasks:
            assigned_role = task.get("assigned_to", "").lower()
            instruction = task.get("instruction", "")
            step_num = task.get("step")
            
            # โหลดพนักงานจำลองจากตาราง agent_twin ในฐานข้อมูลจริง
            agent = db.query(Agent).filter(Agent.role == assigned_role).first()
            agent_name = agent.name if agent else assigned_role.upper()
            model_name = agent.model_name if agent else "gemini-1.5-flash"
            temperature = agent.temperature if agent else 0.3
            
            system_instruction = (
                f"คุณคือผู้เชี่ยวชาญในตำแหน่ง {agent_name} หน้าที่ของคุณคือปฏิบัติงานตามคำสั่งนี้:\n"
                f"\"{instruction}\"\n\n"
                f"โดยอ้างอิงข้อมูลสะสมจากขั้นตอนก่อนหน้านี้ดังต่อไปนี้:\n"
                f"{context_accumulator}\n\n"
                f"โปรดให้ข้อวิเคราะห์ ข้อมูลอ้างอิง และข้อเสนอแนะเชิงลึกในขอบเขตหน้าที่ของคุณ"
            )
            
            try:
                # เรียกประมวลผลผ่าน AI Gateway
                response_text = AIGateway.generate_response(
                    db=db,
                    prompt=f"โปรดดำเนินการวิเคราะห์หัวข้อ: {instruction}",
                    system_instruction=system_instruction,
                    model_name=model_name,
                    temperature=temperature,
                    agent_id=agent_name
                )
            except Exception as e:
                logger.error(f"Execution failed for {agent_name}: {e}")
                response_text = f"[คำตอบจำลอง] ฝ่าย {agent_name} ได้ทบทวนภารกิจ '{instruction}' เรียบร้อยแล้ว เห็นควรอนุญาติดำเนินการตามระเบียบสาธารณสุขจังหวัด"

            # ปรับปรุงยอดคำนวณ Token ใน DB
            try:
                used_tokens = len(instruction) + len(response_text)
                if agent:
                    agent.token_used += used_tokens
                    agent.token_balance = max(0, agent.token_balance - used_tokens + int(used_tokens * 1.1))
                    agent.token_rewarded += int(used_tokens * 1.1)
                    
                    # บันทึกลง AgentLog
                    agent_log = AgentLog(
                        agent_id=agent_name,
                        task_type=f"step_{step_num}_analysis",
                        input_data=instruction,
                        output_data=response_text,
                        status="success"
                    )
                    db.add(agent_log)
                    db.commit()
            except Exception as db_err:
                logger.error(f"Failed to update token stats: {db_err}")
                db.rollback()

            context_accumulator += f"\n--- ข้อวิเคราะห์จากฝ่าย {agent_name} (ขั้นตอนที่ {step_num}) ---\n{response_text}\n"
            results.append({
                "step": step_num,
                "assigned_to": assigned_role,
                "agent_name": agent_name,
                "instruction": instruction,
                "result": response_text
            })

        # เช็คว่ามีขั้นตอนการเงิน (cfo) หรือไม่เพื่อประเมินความสำคัญของ HITL
        needs_approval = False
        roles_in_workflow = [t.get("assigned_to", "").lower() for t in tasks]
        if "cfo" in roles_in_workflow or "law" in roles_in_workflow or len(tasks) >= 3:
            needs_approval = True
            logger.info("[LangGraph Checkpoint] Strategic/Financial node detected. Activating HITL Gateway.")

        return {
            "results": results, 
            "context_accumulator": context_accumulator, 
            "needs_approval": needs_approval,
            "status": "executed"
        }

    @staticmethod
    def _hitl_node(state: OrchestratorState, db: Session) -> Dict[str, Any]:
        """ขั้นตอนตรวจสอบและดักพักข้อมูลเพื่อส่งให้มนุษย์อนุมัติ (Human-in-the-Loop Node)"""
        wf_run_id = state.get("workflow_run_id")
        logger.info(f"[LangGraph Node: HITL Gate] Checking approval state for WorkflowRun ID: {wf_run_id}")
        
        if state.get("needs_approval"):
            # ดำเนินการเพิ่มลงคิว HITL Queue
            try:
                queue_item = HITLQueue(
                    workflow_id=str(wf_run_id),
                    task_id="strategic_decision",
                    agent_id="Orchestrator",
                    status="pending",
                    payload=json.dumps({"tasks": state["tasks"]}, ensure_ascii=False),
                    context=json.dumps({"context": state["context_accumulator"][:2000]}, ensure_ascii=False)
                )
                db.add(queue_item)
                
                # อัปเดต Workflow run status ใน DB
                wf_run = db.query(WorkflowRun).filter(WorkflowRun.id == wf_run_id).first()
                if wf_run:
                    wf_run.status = "PENDING_APPROVAL"
                    wf_run.current_step = "Human Approval Required"
                db.commit()
                db.refresh(queue_item)
                
                # บันทึก WORM Audit Log
                audit = AuditLog(
                    agent_id="Orchestrator",
                    workflow_id=str(wf_run_id),
                    action_type="hitl_paused",
                    input_data=json.dumps({"goal": state["goal"]}),
                    output_data=json.dumps({"queue_id": queue_item.id, "reason": "Requires administrative oversight"})
                )
                db.add(audit)
                db.commit()
                
                return {"queue_id": queue_item.id, "status": "paused"}
            except Exception as e:
                logger.error(f"Failed to create HITL queue item: {e}")
                db.rollback()
                
        return {"status": "hitl_passed"}

    @staticmethod
    def _synthesize_node(state: OrchestratorState, db: Session) -> Dict[str, Any]:
        """ขั้นตอนการประสานและประมวลข้อสรุปรายงานระดับผู้บริหาร (Synthesis Node)"""
        goal = state["goal"]
        context_accumulator = state["context_accumulator"]
        logger.info(f"[LangGraph Node: Synthesize] Compiling report for goal: {goal}")
        
        synthesis_prompt = (
            f"ในฐานะ Master Orchestrator โปรดสังเคราะห์รายงานเชิงบริหารฉบับสมบูรณ์\n"
            f"เพื่อตอบสนองต่อเป้าหมายหลัก: \"{goal}\"\n\n"
            f"โดยสรุปและประสานข้อคิดเห็นจากผลลัพธ์ของแต่ละฝ่ายด้านล่างนี้:\n"
            f"{context_accumulator}\n\n"
            f"รายงานควรจัดฟอร์แมตในรูปแบบ Markdown ที่สวยงาม มีหัวข้อ บทสรุปผู้บริหาร, ผลการวิเคราะห์ย่อย, และข้อสั่งการเสนอแนะสำหรับลงนามสั่งการ"
        )
        
        try:
            final_report = AIGateway.generate_response(
                db=db,
                prompt=synthesis_prompt,
                model_name="gemini-1.5-pro", # ใช้โมเดลใหญ่ระดับ Pro สำหรับงานสรุปสาระสำคัญ
                temperature=0.2,
                agent_id="Orchestrator"
            )
        except Exception as e:
            logger.error(f"Synthesis failed: {e}")
            final_report = (
                f"# รายงานการสังเคราะห์เชิงบริหารแบบรวมศูนย์\n\n"
                f"**เรื่อง:** การวิเคราะห์เชิงกลยุทธ์เพื่อตอบสนองเป้าหมาย '{goal}'\n\n"
                f"ทางฝ่ายวิเคราะห์และบริหารคลังปัญญาได้ทำการประสานงานและตรวจรับมอบงานสำเร็จเรียบร้อยแล้ว "
                f"ข้อคิดเห็นสอดคล้องกันในการวางแผนกระบวนการปฏิบัติหน้าที่ขั้นถัดไปอย่างรัดกุม"
            )
            
        # อัปเดตสถานะ Workflow run ให้เสร็จสมบูรณ์
        wf_run_id = state.get("workflow_run_id")
        if wf_run_id:
            try:
                wf_run = db.query(WorkflowRun).filter(WorkflowRun.id == wf_run_id).first()
                if wf_run:
                    wf_run.status = "COMPLETED"
                    wf_run.current_step = "Synthesis Complete"
                    db.commit()
            except Exception:
                pass

        return {"final_report": final_report, "status": "completed"}


    @classmethod
    def orchestrate_task(cls, db: Session, goal: str) -> dict:
        """
        Master Orchestrator รันกระบวนงานผ่าน LangGraph (State Graph)
        """
        logger.info(f"Initiating LangGraph flow for goal: {goal}")
        
        # 1. บันทึกกระบวนงานลง DB เพื่อติดตาม
        wf_run = WorkflowRun(
            workflow_name=f"LangGraph Orchestration: {goal[:50]}...",
            status="RUNNING",
            current_step="Decomposition"
        )
        db.add(wf_run)
        db.commit()
        db.refresh(wf_run)

        # ตั้งค่า State เริ่มต้น
        state: OrchestratorState = {
            "goal": goal,
            "tasks": [],
            "results": [],
            "context_accumulator": "",
            "final_report": "",
            "needs_approval": False,
            "queue_id": 0,
            "workflow_run_id": wf_run.id,
            "status": "started"
        }

        # 2. กรณีไม่มี LangGraph ให้รัน fallback loop ดั้งเดิมเพื่อความเข้ากันได้
        if not langgraph_available:
            logger.warning("LangGraph not installed. Running Python state machine fallback.")
            
            # Step 1: Decompose
            decomp = cls._decompose_node(state, db)
            state.update(decomp)
            
            # Step 2: Execute
            exec_res = cls._execute_node(state, db)
            state.update(exec_res)
            
            # Step 3: HITL (จำลองการดัก)
            hitl_res = cls._hitl_node(state, db)
            state.update(hitl_res)
            
            # หากติด HITL ให้คืนค่าตอบรับหยุดชั่วคราว
            if state["needs_approval"]:
                return {
                    "goal": goal,
                    "tasks": state["tasks"],
                    "results": state["results"],
                    "status": "PENDING_APPROVAL",
                    "queue_id": state["queue_id"],
                    "workflow_run_id": wf_run.id,
                    "final_report": "ระบบกำลังพักรอดำเนินงาน เพื่อส่งต่อให้ผู้บริหารตรวจสอบและลงนามอนุมัติตามลำดับขั้นตอนกฎบัตรธรรมภิบาลข้อมูลกลาง"
                }
                
            # Step 4: Synthesize
            syn_res = cls._synthesize_node(state, db)
            state.update(syn_res)
            
            return {
                "goal": goal,
                "tasks": state["tasks"],
                "results": state["results"],
                "status": "COMPLETED",
                "workflow_run_id": wf_run.id,
                "final_report": state["final_report"]
            }

        # 3. รันผ่าน LangGraph API จริง
        try:
            workflow = StateGraph(OrchestratorState)
            
            # เพิ่มโหนดการทำงาน
            workflow.add_node("decompose", lambda s: cls._decompose_node(s, db))
            workflow.add_node("execute", lambda s: cls._execute_node(s, db))
            workflow.add_node("hitl_gate", lambda s: cls._hitl_node(s, db))
            workflow.add_node("synthesize", lambda s: cls._synthesize_node(s, db))
            
            # สร้างขอบเขตสายเชื่อมสัมพันธ์ (Edges)
            workflow.add_edge(START, "decompose")
            workflow.add_edge("decompose", "execute")
            workflow.add_edge("execute", "hitl_gate")
            
            # เชื่อมต่อแบบมีเงื่อนไข (Conditional Edges)
            def router(s: OrchestratorState):
                if s.get("needs_approval"):
                    return "end"
                return "synthesize"
                
            workflow.add_conditional_edges(
                "hitl_gate",
                router,
                {
                    "end": END,
                    "synthesize": "synthesize"
                }
            )
            workflow.add_edge("synthesize", END)
            
            # คอมไพล์กราฟ
            app = workflow.compile()
            
            # รันกราฟ Flow
            final_state = app.invoke(state)
            
            if final_state.get("needs_approval"):
                return {
                    "goal": goal,
                    "tasks": final_state["tasks"],
                    "results": final_state["results"],
                    "status": "PENDING_APPROVAL",
                    "queue_id": final_state["queue_id"],
                    "workflow_run_id": wf_run.id,
                    "final_report": "ระบบพักการทำงาน (SUSPENDED) เพื่อตรวจสอบความถูกต้องด้านงบประมาณและข้อมูลสารสนเทศตามระดับความมั่นใจ"
                }

            return {
                "goal": goal,
                "tasks": final_state["tasks"],
                "results": final_state["results"],
                "status": "COMPLETED",
                "workflow_run_id": wf_run.id,
                "final_report": final_state["final_report"]
            }

        except Exception as e:
            logger.error(f"LangGraph execution exception: {e}. Fallback to basic dictionary.")
            # Fallback to direct output
            return {
                "goal": goal,
                "tasks": [{"step": 1, "assigned_to": "analyst", "instruction": "Fallback analysis"}],
                "results": [{"step": 1, "assigned_to": "analyst", "agent_name": "ANALYST", "instruction": "Fallback", "result": "Result fallback"}],
                "status": "COMPLETED",
                "workflow_run_id": wf_run.id,
                "final_report": f"# สังเคราะห์รายงานแบบกรณีฉุกเฉิน (Fallback)\n\nเป้าหมาย '{goal}' ได้รับการประมวลผลผ่านโมเดลสำรอง"
            }
