import logging
from sqlalchemy.orm import Session
from backend.app.services.gemini_service import GeminiService
from backend.app.agents.agents import log_agent_activity

logger = logging.getLogger(__name__)

class ExecutiveTwinAgent:
    @staticmethod
    def simulate_executive_decision(db: Session, role: str, issue_description: str, model_name: str = None) -> dict:
        """[Milestone 3] ใช้ Gemini จำลองทัศนะและการพิจารณาโครงการของผู้บริหาร (PHO) อ้างอิงตามเป้าหมายสาธารณสุขของจังหวัด"""
        logger.info(f"ExecutiveTwinAgent simulating decision for role: {role}")
        
        system_instruction = (
            "You are the HosPrime Executive Twin (PHO Twin). "
            "You represent the Chief Provincial Public Health Officer (นายแพทย์สาธารณสุขจังหวัด). "
            "Analyze the project/issue description and simulate the executive's decision, "
            "reasoning (in professional Thai medical management tone), and key KPIs to monitor. "
            "You must return ONLY a JSON object with keys: "
            "'decision' (e.g. อนุมัติ / อนุมัติโดยมีเงื่อนไข / ตีกลับให้แก้ไข), "
            "'reasoning' (professional explanation in Thai), "
            "'key_kpis' (list of relevant public health KPIs to monitor)."
        )
        
        prompt = (
            f"Analyze this issue for executive decision:\n\n"
            f"Issue: {issue_description}"
        )
        
        result = GeminiService.generate_json_response(prompt, system_instruction, model_name=model_name)
        
        if not result:
            result = {
                "decision": "อนุมัติโดยมีเงื่อนไข",
                "reasoning": "โครงการมีวัตถุประสงค์ในการยกระดับคุณภาพชีวิต แต่ต้องมีระบบติดตามตัวชี้วัดที่เป็นรูปธรรม",
                "key_kpis": ["อัตราความร่วมมือการคัดกรองวัณโรคเชิงรุก > 90%"]
            }
            
        log_agent_activity(db, "ExecutiveTwinAgent", "executive_decision", {"issue": issue_description}, result)
        return result

    @staticmethod
    def draft_official_letter(db: Session, prompt_text: str, model_name: str = None) -> dict:
        """[Milestone 3] ใช้ Gemini ในการร่างหนังสือจดหมายสั่งการของจังหวัด (สสจ.) โดยใช้สำนวนภาษาทางการของ PHO"""
        system_instruction = (
            "You are the HosPrime Executive Twin (PHO Twin). "
            "Your task is to draft a formal Thai official government letter (หนังสือสั่งการราชการ) "
            "from the Chief Provincial Public Health Officer (นายแพทย์สาธารณสุขจังหวัดเชียงราย). "
            "The tone must be extremely formal, commanding, yet professional. "
            "Include official headings, structure, and signed by the executive's role twin."
        )
        
        prompt = (
            f"Draft an official letter regarding: {prompt_text}\n\n"
            f"Generate the letter in standard Thai government letter structure."
        )
        
        letter_content = GeminiService.generate_response(prompt, system_instruction, model_name=model_name)
        
        result = {
            "status": "drafted",
            "draft_content": letter_content
        }
        
        log_agent_activity(db, "ExecutiveTwinAgent", "draft_letter", {"prompt": prompt_text}, result)
        return result
