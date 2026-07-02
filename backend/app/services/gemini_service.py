import hashlib
import json
import logging
from typing import Any, Dict, List, Optional

import google.generativeai as genai
import numpy as np

from backend.app.core.config import settings

logger = logging.getLogger(__name__)


class AIProviderUnavailable(RuntimeError):
    """Raised when an AI provider is unavailable and no safe fallback exists."""


class GeminiService:
    _configured = False
    _configured_key_fingerprint: Optional[str] = None

    @classmethod
    def _configure_api(cls) -> bool:
        """Configure Gemini without embedding credentials in source code."""
        api_key = settings.GEMINI_API_KEY.strip()
        if not api_key:
            cls._configured = False
            logger.warning("GEMINI_API_KEY is not configured.")
            return False

        fingerprint = hashlib.sha256(api_key.encode("utf-8")).hexdigest()[:12]
        if cls._configured and cls._configured_key_fingerprint == fingerprint:
            return True

        try:
            genai.configure(api_key=api_key)
            cls._configured = True
            cls._configured_key_fingerprint = fingerprint
            logger.info("Gemini API configured successfully.")
            return True
        except Exception as exc:
            cls._configured = False
            logger.error("Failed to configure Gemini API: %s", exc)
            return False

    @classmethod
    def get_embedding(cls, text: str, is_query: bool = False) -> List[float]:
        """Create a production embedding or fail explicitly.

        Pseudo-embeddings are disabled by default because arbitrary vectors can
        create false retrieval confidence and misleading citations.
        """
        if not text.strip():
            return [0.0] * 3072

        if cls._configure_api():
            try:
                task_type = "retrieval_query" if is_query else "retrieval_document"
                result = genai.embed_content(
                    model=settings.GEMINI_EMBEDDING_MODEL,
                    content=text,
                    task_type=task_type,
                )
                embedding = result.get("embedding")
                if embedding:
                    return embedding
            except Exception as exc:
                logger.error("Gemini embedding request failed: %s", exc)

        if settings.ALLOW_PSEUDO_EMBEDDINGS and not settings.is_production:
            logger.warning(
                "Using pseudo-embedding in non-production mode. "
                "Results must not be treated as organizational evidence."
            )
            return cls._generate_pseudo_embedding(text)

        raise AIProviderUnavailable(
            "Embedding provider unavailable. Configure GEMINI_API_KEY or an approved local embedding provider."
        )

    @classmethod
    def generate_response(
        cls,
        prompt: str,
        system_instruction: Optional[str] = None,
        temperature: Optional[float] = None,
        model_name: Optional[str] = None,
    ) -> str:
        """Generate text without inventing an offline factual answer."""
        if cls._configure_api():
            try:
                model = genai.GenerativeModel(
                    model_name=model_name or settings.GEMINI_GENERATION_MODEL,
                    system_instruction=system_instruction,
                    generation_config=(
                        {"temperature": temperature}
                        if temperature is not None
                        else None
                    ),
                )
                response = model.generate_content(prompt)
                if response and getattr(response, "text", None):
                    return response.text
                raise AIProviderUnavailable("AI provider returned an empty response.")
            except Exception as exc:
                logger.error("Gemini generation request failed: %s", exc)

        if settings.ALLOW_DEMO_FALLBACKS and not settings.is_production:
            return cls._generate_fallback_answer(prompt)

        raise AIProviderUnavailable(
            "AI generation provider unavailable. No factual fallback answer was generated."
        )

    @classmethod
    def generate_json_response(
        cls,
        prompt: str,
        system_instruction: Optional[str] = None,
        model_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Generate validated JSON or return an explicit non-evidence demo error."""
        if cls._configure_api():
            try:
                model = genai.GenerativeModel(
                    model_name=model_name or settings.GEMINI_GENERATION_MODEL,
                    system_instruction=system_instruction,
                    generation_config={"response_mime_type": "application/json"},
                )
                response = model.generate_content(prompt)
                parsed = json.loads(response.text)
                if not isinstance(parsed, dict):
                    raise ValueError("AI JSON response must be an object")
                return parsed
            except Exception as exc:
                logger.error("Gemini JSON generation failed: %s", exc)

        if settings.ALLOW_DEMO_FALLBACKS and not settings.is_production:
            return {
                "error": "demo_provider_unavailable",
                "evidence_status": "not_evidence",
                "message": "AI provider unavailable; no metadata was inferred.",
            }

        raise AIProviderUnavailable(
            "AI JSON provider unavailable. No inferred metadata was generated."
        )

    @staticmethod
    def _generate_pseudo_embedding(text: str) -> List[float]:
        """Deterministic vector for isolated UI tests only, never production RAG."""
        digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
        seed = int(digest[:8], 16) & 0xFFFFFFFF
        generator = np.random.default_rng(seed)
        vector = generator.standard_normal(3072)
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector = vector / norm
        return vector.tolist()

    @staticmethod
    def _generate_fallback_answer(prompt: str) -> str:
        """Safe demo fallback containing no claims, metrics, or citations."""
        return (
            "[DEMO MODE — NOT ORGANIZATIONAL EVIDENCE]\n\n"
            "AI provider is unavailable. HosPrime did not generate a factual answer, "
            "did not create citations, and did not use this output for a decision."
        )
