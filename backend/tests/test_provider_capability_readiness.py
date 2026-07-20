from pathlib import Path

from backend.app.core.config import Settings


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]


def make_settings(**overrides: object) -> Settings:
    values: dict[str, object] = {
        "ENVIRONMENT": "development",
        "JWT_SECRET": "a" * 48,
        "GEMINI_API_KEY": "",
        "NEO4J_PASSWORD": "local-test-password-not-a-default",
        "DATABASE_URL": (
            "postgresql://hosprime:safe-local-test-password@postgres:5432/hosprime"
        ),
        "POSTGRES_URL": (
            "postgresql://hosprime:safe-local-test-password@postgres:5432/hosprime"
        ),
        "BOOTSTRAP_ADMIN_USERNAME": "admin",
        "BOOTSTRAP_ADMIN_PASSWORD": "safe-local-admin-password",
        "ALLOW_DEMO_FALLBACKS": False,
        "ALLOW_PSEUDO_EMBEDDINGS": False,
        "SEED_DEMO_DATA": False,
    }
    values.update(overrides)
    return Settings(_env_file=None, **values)


def test_missing_optional_provider_is_not_a_security_warning() -> None:
    settings = make_settings()

    assert settings.fatal_configuration_issues() == []
    assert settings.security_warnings() == []
    assert settings.capability_warnings() == [
        "External AI provider is not configured"
    ]


def test_configured_provider_clears_capability_warning() -> None:
    settings = make_settings(GEMINI_API_KEY="newly-issued-provider-key")

    assert settings.security_warnings() == []
    assert settings.capability_warnings() == []


def test_insecure_nonempty_provider_value_still_fails_closed() -> None:
    settings = make_settings(GEMINI_API_KEY="CHANGE_ME_WITH_A_NEW_PROVIDER_KEY")

    assert any(
        "GEMINI_API_KEY" in issue
        for issue in settings.fatal_configuration_issues()
    )


def test_production_can_run_without_optional_provider() -> None:
    settings = make_settings(ENVIRONMENT="production")

    assert settings.fatal_configuration_issues() == []
    assert settings.security_warnings() == []
    assert settings.capability_warnings()


def test_ready_endpoint_separates_security_and_capability_warnings() -> None:
    main_source = (REPOSITORY_ROOT / "backend" / "app" / "main.py").read_text(
        encoding="utf-8"
    )

    assert '"capability_warnings": settings.capability_warnings()' in main_source
    assert '"status": "ready" if not security_warnings else "degraded"' in main_source
    assert "Optional capabilities unavailable" in main_source
    assert "if settings.is_production:" in main_source
