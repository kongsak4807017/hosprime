from pathlib import Path

from backend.app.core.config import Settings


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]


def make_settings(**overrides: object) -> Settings:
    values: dict[str, object] = {
        "ENVIRONMENT": "development",
        "JWT_SECRET": "a" * 48,
        "GEMINI_API_KEY": "test-provider-key-not-for-production",
        "NEO4J_PASSWORD": "local-test-password-not-a-default",
        "DATABASE_URL": "postgresql://hosprime:safe-local-test-password@postgres:5432/hosprime",
        "POSTGRES_URL": "postgresql://hosprime:safe-local-test-password@postgres:5432/hosprime",
        "ALLOW_DEMO_FALLBACKS": False,
        "ALLOW_PSEUDO_EMBEDDINGS": False,
    }
    values.update(overrides)
    return Settings(_env_file=None, **values)


def test_secure_configuration_has_no_fatal_issues() -> None:
    assert make_settings().fatal_configuration_issues() == []


def test_placeholder_credentials_fail_closed() -> None:
    settings = make_settings(
        JWT_SECRET="CHANGE_ME_WITH_AT_LEAST_32_RANDOM_CHARACTERS",
        GEMINI_API_KEY="CHANGE_ME_WITH_A_NEW_PROVIDER_KEY",
        NEO4J_PASSWORD="CHANGE_ME_USE_A_LONG_RANDOM_NEO4J_PASSWORD",
        DATABASE_URL="postgresql://hosprime:CHANGE_ME@postgres:5432/hosprime",
    )

    issues = settings.fatal_configuration_issues()

    assert any("JWT_SECRET" in issue for issue in issues)
    assert any("GEMINI_API_KEY" in issue for issue in issues)
    assert any("NEO4J_PASSWORD" in issue for issue in issues)
    assert any("DATABASE_URL" in issue for issue in issues)


def test_short_jwt_secret_is_rejected() -> None:
    issues = make_settings(JWT_SECRET="too-short").fatal_configuration_issues()
    assert "JWT_SECRET must contain at least 32 characters" in issues


def test_production_rejects_sqlite() -> None:
    warnings = make_settings(
        ENVIRONMENT="production",
        DATABASE_URL="sqlite:///./hosprime.db",
    ).security_warnings()
    assert "SQLite is not permitted in production" in warnings


def test_compose_uses_required_environment_substitution() -> None:
    compose = (REPOSITORY_ROOT / "docker-compose.yml").read_text(encoding="utf-8")

    required_variables = (
        "POSTGRES_PASSWORD",
        "DATABASE_URL",
        "POSTGRES_URL",
        "NEO4J_PASSWORD",
        "GEMINI_API_KEY",
        "JWT_SECRET",
    )
    for variable in required_variables:
        assert f"${{{variable}:?" in compose

    forbidden_literals = (
        "postgrespassword",
        "neo4jpassword",
        "hosprime-super-secret-key-enterprise",
    )
    lowered = compose.lower()
    for literal in forbidden_literals:
        assert literal not in lowered


def test_real_env_files_remain_ignored() -> None:
    gitignore = (REPOSITORY_ROOT / ".gitignore").read_text(encoding="utf-8")
    ignored_paths = {line.strip() for line in gitignore.splitlines()}
    assert ".env" in ignored_paths
    assert "backend/.env" in ignored_paths
