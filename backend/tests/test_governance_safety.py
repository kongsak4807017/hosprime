import pytest

from backend.app.core.config import settings
from backend.app.services.gemini_service import AIProviderUnavailable, GeminiService
from backend.app.services.workflow_service import WorkflowService


def test_ai_generation_fails_without_provider_by_default(monkeypatch):
    monkeypatch.setattr(settings, "GEMINI_API_KEY", "")
    monkeypatch.setattr(settings, "ALLOW_DEMO_FALLBACKS", False)
    monkeypatch.setattr(settings, "ENVIRONMENT", "development")
    GeminiService._configured = False
    GeminiService._configured_key_fingerprint = None

    with pytest.raises(AIProviderUnavailable):
        GeminiService.generate_response("What is the approved policy?")


def test_demo_fallback_contains_no_factual_claim_or_citation(monkeypatch):
    monkeypatch.setattr(settings, "GEMINI_API_KEY", "")
    monkeypatch.setattr(settings, "ALLOW_DEMO_FALLBACKS", True)
    monkeypatch.setattr(settings, "ENVIRONMENT", "development")
    GeminiService._configured = False
    GeminiService._configured_key_fingerprint = None

    response = GeminiService.generate_response("PM2.5 annual report")

    assert "DEMO MODE" in response
    assert "NOT ORGANIZATIONAL EVIDENCE" in response
    assert "Source" not in response
    assert "หน้า" not in response


def test_pseudo_embeddings_are_disabled_by_default(monkeypatch):
    monkeypatch.setattr(settings, "GEMINI_API_KEY", "")
    monkeypatch.setattr(settings, "ALLOW_PSEUDO_EMBEDDINGS", False)
    monkeypatch.setattr(settings, "ENVIRONMENT", "development")
    GeminiService._configured = False
    GeminiService._configured_key_fingerprint = None

    with pytest.raises(AIProviderUnavailable):
        GeminiService.get_embedding("organizational evidence")


def test_workflow_service_never_claims_mock_execution():
    reference = WorkflowService.start_temporal_workflow("TestWorkflow", {})

    assert reference.startswith("plan_TestWorkflow_")
    assert WorkflowService.get_workflow_execution_status(reference) == (
        "PLAN_ONLY_NOT_EXECUTED"
    )
