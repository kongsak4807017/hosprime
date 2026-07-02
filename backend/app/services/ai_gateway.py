import os
import json
import time
import logging
from typing import Dict, Any, Optional, Tuple
from sqlalchemy.orm import Session
from backend.app.core.config import settings
from backend.app.db.models import CostLog
from backend.app.models.twin_models import Agent
from backend.app.services.gemini_service import GeminiService

logger = logging.getLogger(__name__)

class CircuitBreaker:
    def __init__(self, failure_threshold: int = 3, recovery_time: float = 60.0):
        self.failure_threshold = failure_threshold
        self.recovery_time = recovery_time
        self.failure_count = 0
        self.last_failure_time = 0.0
        self.state = "CLOSED" # CLOSED, OPEN, HALF-OPEN

    def record_success(self):
        self.failure_count = 0
        self.state = "CLOSED"

    def record_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"
            logger.warning(f"Circuit breaker state changed to OPEN. Temporary block for {self.recovery_time}s")

    def allow_request(self) -> bool:
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.recovery_time:
                self.state = "HALF-OPEN"
                logger.info("Circuit breaker state changed to HALF-OPEN. Attempting recovery request.")
                return True
            return False
        return True


class AIGateway:
    _breakers: Dict[str, CircuitBreaker] = {}

    @classmethod
    def _get_breaker(cls, provider: str) -> CircuitBreaker:
        if provider not in cls._breakers:
            cls._breakers[provider] = CircuitBreaker()
        return cls._breakers[provider]

    @classmethod
    def _map_agent_role(cls, agent_id: str) -> Optional[str]:
        """แมป agent_id หรือชื่อคลาสของเอเจนต์เข้ากับ role ในระบบ Token Economy (agent_twin)"""
        if not agent_id:
            return None
        
        agent_id_lower = agent_id.lower()
        
        # 1. เช็คว่ามีคำสำคัญตรงกับบทบาทหลักของเอเจนต์ในบอร์ดกำกับดูแลหรือไม่
        roles = ["executive", "cos", "analyst", "knowledge", "report", "meeting", "datagov", "cfo", "coo", "provincial"]
        for role in roles:
            if role in agent_id_lower:
                return role
                
        # 2. แมปชื่อคลาสเอเจนต์ทั่วไปที่อยู่นอกบอร์ด
        mapping = {
            "answergenerationagent": "report",
            "metadataagent": "knowledge",
            "documentclassificationagent": "datagov",
            "knowledgeingestionagent": "knowledge",
            "retrievalagent": "knowledge",
            "rerankingagent": "analyst",
            "feedbacklearningagent": "datagov"
        }
        return mapping.get(agent_id_lower)

    @classmethod
    def _check_budget(cls, db: Session, agent_id: str) -> Tuple[bool, Optional[str], Optional[Agent]]:
        """ตรวจสอบสถานะของเอเจนต์และตรวจสอบยอดคงเหลือของโทเค็นก่อนรัน API"""
        role_key = cls._map_agent_role(agent_id)
        if not role_key:
            # หากไม่มีการแมป ถือเป็นคำขอของระบบส่วนกลาง ไม่บล็อกและไม่มีขีดจำกัดงบ
            return True, None, None

        try:
            agent = db.query(Agent).filter(Agent.role == role_key).first()
            if not agent:
                # ลองค้นหาด้วยชื่อเต็มเผื่อ
                agent = db.query(Agent).filter(Agent.name.like(f"%{role_key}%")).first()
                
            if not agent:
                logger.warning(f"Agent with role '{role_key}' not found in database. Proceeding without budget limitation.")
                return True, None, None

            if not agent.is_active:
                return False, f"Agent '{agent.name}' is inactive (disabled by administrator).", agent

            if agent.token_balance <= 0:
                return False, f"Agent '{agent.name}' has exceeded its daily token budget limit (Balance: {agent.token_balance}).", agent

            return True, None, agent
        except Exception as e:
            logger.error(f"Error checking budget for agent {agent_id}: {e}")
            return True, None, None # ในกรณี DB ขัดข้องชั่วคราว ให้ปล่อยผ่านเพื่อไม่ขัดขวางการทำงานหลัก

    @classmethod
    def _deduct_budget(cls, db: Session, agent: Optional[Agent], tokens_used: int):
        """หักลบจำนวนโทเค็นที่ใช้งานจริงออกจากกระเป๋าของเอเจนต์"""
        if not agent or tokens_used <= 0:
            return
        try:
            # อัปเดตและหัก Token
            agent.token_used += tokens_used
            agent.token_balance -= tokens_used
            db.commit()
            logger.info(f"Deducted {tokens_used} tokens from Agent '{agent.name}'. Remaining balance: {agent.token_balance}")
        except Exception as e:
            logger.error(f"Failed to deduct budget for agent {agent.name}: {e}")
            db.rollback()

    @classmethod
    def generate_response(
        cls, 
        db: Session, 
        prompt: str, 
        system_instruction: Optional[str] = None, 
        model_name: str = "gemini-1.5-flash",
        temperature: float = 0.3,
        agent_id: str = "system"
    ) -> str:
        """
        AI Gateway ทำหน้าที่ส่งคำขอไปยังโมเดลที่เหมาะสม 
        มีระบบควบคุมงบโทเค็น (Budget Check) และ Circuit Breaker
        """
        # 1. ตรวจสอบ Budget ของเอเจนต์ก่อน
        allowed, reason, agent = cls._check_budget(db, agent_id)
        if not allowed:
            logger.warning(f"Request blocked: {reason}")
            return f"[ระบบควบคุมเอเจนต์] ปฏิเสธการทำงานเนื่องจาก: {reason}"

        provider = cls._detect_provider(model_name)
        breaker = cls._get_breaker(provider)

        # 2. เช็ค Circuit Breaker
        if not breaker.allow_request():
            logger.warning(f"Provider {provider} is currently blocked by Circuit Breaker. Routing to fallback provider.")
            if provider != "gemini":
                # Fallback ไปยัง Gemini
                return cls.generate_response(db, prompt, system_instruction, "gemini-1.5-flash", temperature, agent_id)
            else:
                return "[คำตอบจำลองเนื่องจากระบบ AI Gateway เกิดความขัดข้องชั่วคราว] ขออภัยในความไม่สะดวก"

        # 3. ส่งคำขอไปยังผู้ให้บริการที่เลือก
        try:
            response_text = ""
            if provider == "gemini":
                response_text = GeminiService.generate_response(
                    prompt, 
                    system_instruction=system_instruction, 
                    temperature=temperature
                )
            elif provider in ["openai", "anthropic", "deepseek"]:
                logger.info(f"Simulating API request for provider {provider} using model {model_name}")
                adjusted_system = f"{system_instruction or ''}\n[ระบบจำลองสมอง {model_name} ของฝั่ง {provider.upper()}]"
                response_text = GeminiService.generate_response(
                    prompt,
                    system_instruction=adjusted_system,
                    temperature=temperature
                )
            else:
                response_text = GeminiService.generate_response(
                    prompt,
                    system_instruction=system_instruction,
                    temperature=temperature
                )

            # บันทึกความสำเร็จใน Circuit Breaker
            breaker.record_success()

            # 4. คิดจำนวนโทเค็นและคำนวณราคา
            input_tokens = len(prompt) // 4 + (len(system_instruction or "") // 4)
            output_tokens = len(response_text) // 4
            total_tokens = input_tokens + output_tokens
            cost = cls._calculate_cost(provider, model_name, input_tokens, output_tokens)
            
            # บันทึกประวัติการใช้จ่ายของเอเจนต์
            cls._deduct_budget(db, agent, total_tokens)
            cls._log_cost(db, agent_id, provider, model_name, input_tokens, output_tokens, cost)

            return response_text

        except Exception as e:
            logger.error(f"Error in AIGateway calling {provider} / {model_name}: {e}")
            breaker.record_failure()
            
            if provider != "gemini":
                logger.info("Attempting recovery fallback to Gemini...")
                return cls.generate_response(db, prompt, system_instruction, "gemini-1.5-flash", temperature, agent_id)
            
            raise e

    @classmethod
    def generate_json_response(
        cls,
        db: Session,
        prompt: str,
        system_instruction: Optional[str] = None,
        model_name: str = "gemini-1.5-flash",
        agent_id: str = "system"
    ) -> Dict[str, Any]:
        """
        AI Gateway สำหรับส่งคำขอที่ต้องการโครงสร้างข้อมูลแบบ JSON
        """
        # 1. ตรวจสอบ Budget ของเอเจนต์ก่อน
        allowed, reason, agent = cls._check_budget(db, agent_id)
        if not allowed:
            logger.warning(f"Request blocked: {reason}")
            return {"error": "budget_exceeded", "reason": reason}

        provider = cls._detect_provider(model_name)
        breaker = cls._get_breaker(provider)

        # 2. เช็ค Circuit Breaker
        if not breaker.allow_request():
            logger.warning(f"Provider {provider} is currently blocked by Circuit Breaker. Routing to fallback.")
            if provider != "gemini":
                return cls.generate_json_response(db, prompt, system_instruction, "gemini-1.5-flash", agent_id)
            else:
                return {"error": "service_unavailable", "reason": "Circuit breaker is open"}

        # 3. ส่งคำขอ JSON
        try:
            result = {}
            if provider == "gemini":
                result = GeminiService.generate_json_response(
                    prompt, 
                    system_instruction=system_instruction
                )
            elif provider in ["openai", "anthropic", "deepseek"]:
                logger.info(f"Simulating JSON request for provider {provider} using model {model_name}")
                adjusted_system = f"{system_instruction or ''}\n[จำลองสมอง {model_name} ของฝั่ง {provider.upper()} - ต้องตอบกลับเป็น JSON ที่ถูกต้อง]"
                result = GeminiService.generate_json_response(
                    prompt,
                    system_instruction=adjusted_system
                )
            else:
                result = GeminiService.generate_json_response(
                    prompt,
                    system_instruction=system_instruction
                )

            # บันทึกความสำเร็จใน Circuit Breaker
            breaker.record_success()

            # 4. คิดปริมาณโทเค็นและคำนวณราคา
            output_str = json.dumps(result, ensure_ascii=False)
            input_tokens = len(prompt) // 4 + (len(system_instruction or "") // 4)
            output_tokens = len(output_str) // 4
            total_tokens = input_tokens + output_tokens
            cost = cls._calculate_cost(provider, model_name, input_tokens, output_tokens)
            
            # ตัดยอดเงินโทเค็นของเอเจนต์
            cls._deduct_budget(db, agent, total_tokens)
            cls._log_cost(db, agent_id, provider, model_name, input_tokens, output_tokens, cost)

            return result

        except Exception as e:
            logger.error(f"Error in AIGateway generate_json_response for {provider} / {model_name}: {e}")
            breaker.record_failure()
            
            if provider != "gemini":
                logger.info("Attempting recovery fallback to Gemini...")
                return cls.generate_json_response(db, prompt, system_instruction, "gemini-1.5-flash", agent_id)
            
            raise e

    @classmethod
    def _detect_provider(cls, model_name: str) -> str:
        if not model_name:
            return "gemini"
        model_name_lower = model_name.lower()
        if "gemini" in model_name_lower:
            return "gemini"
        elif "gpt" in model_name_lower:
            return "openai"
        elif "claude" in model_name_lower:
            return "anthropic"
        elif "deepseek" in model_name_lower:
            return "deepseek"
        return "local"

    @classmethod
    def _calculate_cost(cls, provider: str, model_name: str, input_tokens: int, output_tokens: int) -> float:
        rates = {
            "gemini": {"input": 0.075, "output": 0.30},
            "openai": {"input": 2.50, "output": 10.00},
            "anthropic": {"input": 3.00, "output": 15.00},
            "deepseek": {"input": 0.14, "output": 0.28},
            "local": {"input": 0.00, "output": 0.00}
        }
        prov_rates = rates.get(provider, {"input": 0.1, "output": 0.2})
        input_cost = (input_tokens / 1_000_000) * prov_rates["input"]
        output_cost = (output_tokens / 1_000_000) * prov_rates["output"]
        return float(input_cost + output_cost)

    @classmethod
    def _log_cost(
        cls, 
        db: Session, 
        agent_id: str, 
        provider: str, 
        model: str, 
        input_tokens: int, 
        output_tokens: int, 
        cost_usd: float
    ):
        try:
            cost_log = CostLog(
                agent_id=agent_id,
                provider=provider,
                model=model,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                cost_usd=cost_usd
            )
            db.add(cost_log)
            db.commit()
        except Exception as e:
            logger.error(f"Failed to write cost log: {e}")
            db.rollback()
