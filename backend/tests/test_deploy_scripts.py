from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_required_cross_platform_scripts_exist() -> None:
    for path in (
        "scripts/bootstrap.sh",
        "scripts/bootstrap.ps1",
        "scripts/healthcheck.sh",
        "scripts/healthcheck.ps1",
    ):
        assert (ROOT / path).is_file(), path


def test_bootstrap_scripts_fail_closed_on_placeholders_and_wait_for_health() -> None:
    shell = read("scripts/bootstrap.sh")
    powershell = read("scripts/bootstrap.ps1")
    for content in (shell, powershell):
        assert "CHANGE_ME" in content
        assert "compose" in content
        assert "--wait" in content
        assert "healthcheck" in content
        assert "down --volumes" not in content


def test_healthchecks_verify_all_services_and_public_endpoints() -> None:
    required = ("postgres", "redis", "neo4j", "backend", "frontend")
    for path in ("scripts/healthcheck.sh", "scripts/healthcheck.ps1"):
        content = read(path)
        for service in required:
            assert service in content
        assert "/health/live" in content
        assert "/health/ready" in content
        assert "database_dialect" in content
        assert "FRONTEND_PORT" in content


def test_healthchecks_require_full_readiness_not_degraded_state() -> None:
    shell = read("scripts/healthcheck.sh")
    powershell = read("scripts/healthcheck.ps1")
    assert 'ready.get("status") != "ready"' in shell
    assert "$ready.status -ne 'ready'" in powershell
    assert '"degraded"' not in shell
    assert "'degraded'" not in powershell


def test_scripts_do_not_echo_or_generate_credentials() -> None:
    forbidden = (
        "POSTGRES_PASSWORD=",
        "NEO4J_PASSWORD=",
        "JWT_SECRET=",
        "GEMINI_API_KEY=",
        "BOOTSTRAP_ADMIN_PASSWORD=",
    )
    for path in (
        "scripts/bootstrap.sh",
        "scripts/bootstrap.ps1",
        "scripts/healthcheck.sh",
        "scripts/healthcheck.ps1",
    ):
        content = read(path)
        for value in forbidden:
            assert value not in content
