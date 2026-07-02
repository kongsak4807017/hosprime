import json
import logging
import time
from typing import Any, Dict, Optional, Tuple

from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.db.models import CostLog
from backend.app.models.twin_models import Agent
from backend.app.services.gemini_service import AIProviderUnavailable, GeminiService

logger = logging.getLogger(__name__)


class CircuitBreaker:
    def __init__(self, failure_threshold: int = 3, recovery_time: float = 60.0):
        self.failure_threshold = failure_threshold
        self.recovery_time = recovery_time
        self.failure_count = 0
        self.last_failure_time = 0.0
        self.state = "CLOSED"

    def record_success(self) -> None:
        self.failure_count = 0
        self.state = "CLOSED"

    def record_failure(self) -> None:
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"

    def allow_request(self) -> bool:
        if self.state != "OPEN":
            return True
        if time.time() - self.last_failure_time > self.recovery_time:
            self.state = "HALF_OPEN"
            return True
        return False


class AIGateway:
    """Governed AI gateway.

    The gateway records the provider actually used. It never labels a Gemini
    response as OpenAI, Anthropic, DeepSeek, or a local model.
    """

    _breakers: Dict[str, CircuitBreaker] = {}

    @classmethod
    def _get_breaker(cls, provider: str) -> CircuitBreaker:
        if provider not in cls._breakers:
            cls._breakers[provider] = CircuitBreaker()
        return cls._breakers[provider]

    @classmethod
    def _map_agent_role(cls, agent_id: str) -> Optional[str]:
        if not agent_id:
            return None
        agent_id_lower = agent_id.lower()
        roles = [
            "executive",
            "cos",
            "analyst",
            "knowledge",
            "report",
            "meeting",
            "datagov",
            "cfo",
            "coo",
            "provincial",
        ]
        for role in roles:
            if role in agent_id_lower:
                return role
        mapping = {
            "answergenerationagent": "report",
            "metadataagent": "knowledge",
            "documentclassificationagent": "datagov",
            "knowledgeingestionagent": "knowledge",
            "retrievalagent": "knowledge",
            "rerankingagent": "analyst",
            "feedbacklearningagent": "datagov",
        }
        return mapping.get(agent_id_lower)

    @classmethod
    def _check_budget(
        cls,
        db: Session,
        agent_id: str,
    ) -> Tuple[bool, Optional[str], Optional[Agent]]:
        role_key = cls._map_agent_role(agent_id)
        if not role_key:
            return True, None, None

        try:
            agent = db.query(Agent).filter(Agent.role == role_key).first()
            if not agent:
                reason = f"Governed agent role '{role_key}' is not registered."
                if settings.is_production:
                    return False, reason, None
                logger.warning("%s Development request allowed without budget.", reason)
                return True, None, None
            if not agent.is_active:
                return False, f"Agent '{agent.name}' is inactive.", agent
            if agent.token_balance <= 0:
                return False, f"Agent '{agent.name}' has no token balance.", agent
            return True, None, agent
        except Exception as exc:
            logger.error("Agent budget check failed for %s: %s", agent_id, exc)
            if settings.is_production:
                return False, "Agent budget control is unavailable.", None
            return True, None, None

    @classmethod
    def _deduct_budget(
        cls,
        db: Session,
        agent: Optional[Agent],
        tokens_used: int,
    ) -> None:
        if not agent or tokens_used <= 0:
            return
        try:
            agent.token_used += tokens_used
            agent.token_balance = max(0, agent.token_balance - tokens_used)
            db.commit()
        except Exception as exc:
            db.rollback()
            logger.error("Failed to deduct agent budget: %s", exc)
            if settings.is_production:
                raise

    @classmethod
    def generate_response(
        cls,
        db: Session,
        prompt: str,
        system_instruction: Optional[str] = None,
        model_name: str = "gemini-2.5-flash",
        temperature: float = 0.3,
        agent_id: str = "system",
    ) -> str:
        allowed, reason, agent = cls._check_budget(db, agent_id)
        if not allowed:
            raise PermissionError(reason)

        provider = cls._detect_provider(model_name)
        if provider != "gemini":
            raise AIProviderUnavailable(
                f"Provider '{provider}' is not implemented. Requested model: {model_name}."
            )

        breaker = cls._get_breaker(provider)
        if not breaker.allow_request():
            raise AIProviderUnavailable("Gemini circuit breaker is open.")

        try:
            response_text = GeminiService.generate_response(
                prompt,
                system_instruction=system_instruction,
                temperature=temperature,
                model_name=model_name,
            )
            breaker.record_success()

            input_tokens = max(1, len(prompt) // 4) + max(
                0, len(system_instruction or "") // 4
            )
            output_tokens = max(1, len(response_text) // 4)
            total_tokens = input_tokens + output_tokens
            estimated_cost = cls._calculate_estimated_cost(
                provider, input_tokens, output_tokens
            )
            cls._deduct_budget(db, agent, total_tokens)
            cls._log_cost(
                db,
                agent_id,
                provider,
                model_name,
                input_tokens,
                output_tokens,
                estimated_cost,
            )
            return response_text
        except Exception:
            breaker.record_failure()
            raise

    @classmethod
    def generate_json_response(
        cls,
        db: Session,
        prompt: str,
        system_instruction: Optional[str] = None,
        model_name: str = "gemini-2.5-flash",
        agent_id: str = "system",
    ) -> Dict[str, Any]:
        allowed, reason, agent = cls._check_budget(db, agent_id)
        if not allowed:
            raise PermissionError(reason)

        provider = cls._detect_provider(model_name)
        if provider != "gemini":
            raise AIProviderUnavailable(
                f"Provider '{provider}' is not implemented. Requested model: {model_name}."
            )

        breaker = cls._get_breaker(provider)
        if not breaker.allow_request():
            raise AIProviderUnavailable("Gemini circuit breaker is open.")

        try:
            result = GeminiService.generate_json_response(
                prompt,
                system_instruction=system_instruction,
                model_name=model_name,
            )
            breaker.record_success()

            output_text = json.dumps(result, ensure_ascii=False)
            input_tokens = max(1, len(prompt) // 4) + max(
                0, len(system_instruction or "") // 4
            )
            output_tokens = max(1, len(output_text) // 4)
            total_tokens = input_tokens + output_tokens
            estimated_cost = cls._calculate_estimated_cost(
                provider, input_tokens, output_tokens
            )
            cls._deduct_budget(db, agent, total_tokens)
            cls._log_cost(
                db,
                agent_id,
                provider,
                model_name,
                input_tokens,
                output_tokens,
                estimated_cost,
            )
            return result
        except Exception:
            breaker.record_failure()
            raise

    @staticmethod
    def _detect_provider(model_name: str) -> str:
        value = (model_name or "").lower()
        if "gemini" in value:
            return "gemini"
        if "gpt" in value:
            return "openai"
        if "claude" in value:
            return "anthropic"
        if "deepseek" in value:
            return "deepseek"
        return "local"

    @staticmethod
    def _calculate_estimated_cost(
        provider: str,
        input_tokens: int,
        output_tokens: int,
    ) -> float:
        """Development estimate only; billing reconciliation is external."""
        if provider != "gemini":
            return 0.0
        input_cost = (input_tokens / 1_000_000) * 0.075
        output_cost = (output_tokens / 1_000_000) * 0.30
        return float(input_cost + output_cost)

    @staticmethod
    def _log_cost(
        db: Session,
        agent_id: str,
        provider: str,
        model: str,
        input_tokens: int,
        output_tokens: int,
        cost_usd: float,
    ) -> None:
        try:
            db.add(
                CostLog(
                    agent_id=agent_id,
                    provider=provider,
                    model=model,
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                    cost_usd=cost_usd,
                )
            )
            db.commit()
        except Exception as exc:
            db.rollback()
            logger.error("Failed to write cost log: %s", exc)
