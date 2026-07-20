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
        "BOOTSTRAP_ADMIN_USERNAME": "admin",
        "BOOTSTRAP_ADMIN_PASSWORD": "safe-local-admin-password",
        "ALLOW_DEMO_FALLBACKS": False,
        "ALLOW_PSEUDO_EMBEDDINGS": False,
        "SEED_DEMO_DATA": False,
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
        BOOTSTRAP_ADMIN_PASSWORD="CHANGE_ME_WITH_A_LONG_RANDOM_ADMIN_PASSWORD",
    )

    issues = settings.fatal_configuration_issues()

    assert any("JWT_SECRET" in issue for issue in issues)
    assert any("GEMINI_API_KEY" in issue for issue in issues)
    assert any("NEO4J_PASSWORD" in issue for issue in issues)
    assert any("DATABASE_URL" in issue for issue in issues)
    assert any("BOOTSTRAP_ADMIN_PASSWORD" in issue for issue in issues)


def test_short_jwt_secret_is_rejected() -> None:
    issues = make_settings(JWT_SECRET="too-short").fatal_configuration_issues()
    assert "JWT_SECRET must contain at least 32 characters" in issues


def test_bootstrap_admin_password_is_required_and_strong() -> None:
    assert "BOOTSTRAP_ADMIN_PASSWORD is not configured" in make_settings(
        BOOTSTRAP_ADMIN_PASSWORD=""
    ).fatal_configuration_issues()
    assert "BOOTSTRAP_ADMIN_PASSWORD must contain at least 12 characters" in make_settings(
        BOOTSTRAP_ADMIN_PASSWORD="short"
    ).fatal_configuration_issues()


def test_production_rejects_effective_sqlite_database() -> None:
    warnings = make_settings(
        ENVIRONMENT="production",
        DATABASE_URL="sqlite:///./hosprime.db",
        POSTGRES_URL="",
    ).security_warnings()
    assert "SQLite is not permitted in production" in warnings


def test_production_accepts_postgres_url_over_sqlite_fallback() -> None:
    settings = make_settings(
        ENVIRONMENT="production",
        DATABASE_URL="sqlite:///./hosprime.db",
        POSTGRES_URL="postgresql://hosprime:safe-local-test-password@postgres:5432/hosprime",
    )

    assert settings.effective_database_url.startswith("postgresql://")
    assert "SQLite is not permitted in production" not in settings.security_warnings()


def test_compose_uses_required_environment_substitution() -> None:
    compose = (REPOSITORY_ROOT / "docker-compose.yml").read_text(encoding="utf-8")

    required_variables = (
        "POSTGRES_PASSWORD",
        "DATABASE_URL",
        "POSTGRES_URL",
        "NEO4J_PASSWORD",
        "JWT_SECRET",
        "BOOTSTRAP_ADMIN_USERNAME",
        "BOOTSTRAP_ADMIN_PASSWORD",
    )
    for variable in required_variables:
        assert f"${{{variable}:?" in compose

    forbidden_literals = (
        "postgrespassword",
        "neo4jpassword",
        "hosprime-super-secret-key-enterprise",
        "admin1234",
        "user1234",
    )
    lowered = compose.lower()
    for literal in forbidden_literals:
        assert literal not in lowered


def test_local_m0_compose_allows_missing_external_provider_key() -> None:
    compose = (REPOSITORY_ROOT / "docker-compose.yml").read_text(encoding="utf-8")
    env_example = (REPOSITORY_ROOT / ".env.example").read_text(encoding="utf-8")

    assert "GEMINI_API_KEY: ${GEMINI_API_KEY:-}" in compose
    assert "${GEMINI_API_KEY:?" not in compose
    assert "GEMINI_API_KEY=\n" in env_example
    assert "Optional for the local M0 developer preview" in env_example
    provider_free = make_settings(GEMINI_API_KEY="")
    assert provider_free.fatal_configuration_issues() == []
    assert "GEMINI_API_KEY is not configured" not in provider_free.security_warnings()
    assert "External AI provider is not configured" in provider_free.capability_warnings()


def test_ci_runtime_credentials_are_generated_per_run() -> None:
    workflow = (
        REPOSITORY_ROOT / ".github" / "workflows" / "m0-secure-runtime-test.yml"
    ).read_text(encoding="utf-8")

    assert "import secrets" in workflow
    assert "secrets.token_urlsafe(32)" in workflow
    assert "secrets.token_urlsafe(48)" in workflow
    assert 'quote(postgres_password, safe="")' in workflow
    assert 'Path(".env").write_text' in workflow
    assert "chmod 600 .env" in workflow
    assert '"GEMINI_API_KEY": ""' in workflow
    assert "provider_key =" not in workflow

    forbidden_fixed_credentials = (
        "ci-postgres-password-not-for-production",
        "ci-neo4j-password-not-for-production",
        "ci-provider-key-not-for-production",
        "ci-only-jwt-secret-with-more-than-thirty-two-characters",
        "ci-admin-password-not-for-production",
    )
    for credential in forbidden_fixed_credentials:
        assert credential not in workflow


def test_compose_requires_frontend_health_before_readiness() -> None:
    compose = (REPOSITORY_ROOT / "docker-compose.yml").read_text(encoding="utf-8")
    frontend = compose.split("\n  frontend:\n", 1)[1].split("\nvolumes:\n", 1)[0]

    assert "healthcheck:" in frontend
    assert '["CMD", "wget", "--quiet", "--spider", "http://127.0.0.1/"]' in frontend
    assert "CMD-SHELL" not in frontend
    assert "http://localhost/" not in frontend
    assert "interval: 15s" in frontend
    assert "timeout: 5s" in frontend
    assert "retries: 10" in frontend
    assert "start_period: 10s" in frontend


def test_deploy_bootstrap_is_idempotent_and_non_destructive() -> None:
    dockerfile = (REPOSITORY_ROOT / "backend" / "Dockerfile").read_text(encoding="utf-8")
    bootstrap = (
        REPOSITORY_ROOT / "backend" / "app" / "db" / "safe_bootstrap.py"
    ).read_text(encoding="utf-8")

    assert "backend.app.db.safe_bootstrap" in dockerfile
    assert "drop_all" not in bootstrap
    assert "create_all" in bootstrap
    assert "BOOTSTRAP_ADMIN_PASSWORD" in bootstrap
    assert "admin1234" not in bootstrap
    assert "user1234" not in bootstrap


def test_real_env_files_remain_ignored() -> None:
    gitignore = (REPOSITORY_ROOT / ".gitignore").read_text(encoding="utf-8")
    ignored_paths = {line.strip() for line in gitignore.splitlines()}
    assert ".env" in ignored_paths
    assert "backend/.env" in ignored_paths
