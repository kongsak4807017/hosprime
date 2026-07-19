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

    assert "!/^[[:space:]]*(#|$)/ && /CHANGE_ME/" in shell
    assert "$_ -notmatch '^\\s*(#|$)' -and $_ -match 'CHANGE_ME'" in powershell
    assert "(^|=)CHANGE_ME" not in shell
    assert "(^|=)CHANGE_ME" not in powershell


def test_shell_bootstrap_invokes_healthcheck_through_bash() -> None:
    shell = read("scripts/bootstrap.sh")
    assert 'bash "$ROOT_DIR/scripts/healthcheck.sh"' in shell
    assert '"$ROOT_DIR/scripts/healthcheck.sh"\n' not in shell


def test_all_deploy_commands_bind_to_one_explicit_compose_project() -> None:
    shell_bootstrap = read("scripts/bootstrap.sh")
    shell_health = read("scripts/healthcheck.sh")
    powershell_bootstrap = read("scripts/bootstrap.ps1")
    powershell_health = read("scripts/healthcheck.ps1")

    for content in (shell_bootstrap, shell_health):
        assert 'PROJECT_NAME="${HOSPRIME_COMPOSE_PROJECT_NAME:-hosprime}"' in content
        assert 'docker compose --project-name "$PROJECT_NAME" --env-file "$ENV_FILE"' in content
        assert '^[a-z0-9][a-z0-9_-]*$' in content

    for content in (powershell_bootstrap, powershell_health):
        assert '[string]$ProjectName = $env:HOSPRIME_COMPOSE_PROJECT_NAME' in content
        assert "if ([string]::IsNullOrWhiteSpace($ProjectName)) { $ProjectName = 'hosprime' }" in content
        assert 'docker compose --project-name $ProjectName --env-file $EnvFile' in content
        assert '^[a-z0-9][a-z0-9_-]*$' in content

    assert 'HOSPRIME_COMPOSE_PROJECT_NAME="$PROJECT_NAME" bash' in shell_bootstrap
    assert "-ProjectName $ProjectName" in powershell_bootstrap


def test_environment_path_is_normalized_before_scripts_change_directory() -> None:
    shell_bootstrap = read("scripts/bootstrap.sh")
    shell_health = read("scripts/healthcheck.sh")
    powershell_bootstrap = read("scripts/bootstrap.ps1")
    powershell_health = read("scripts/healthcheck.ps1")

    for content in (shell_bootstrap, shell_health):
        assert 'ENV_FILE_INPUT="${HOSPRIME_ENV_FILE:-$ROOT_DIR/.env}"' in content
        assert "os.path.abspath(sys.argv[1])" in content
        assert 'cd "$ROOT_DIR"' in content
        assert content.index("os.path.abspath(sys.argv[1])") < content.index('cd "$ROOT_DIR"')
        assert '[[ ! -L "$ENV_FILE" ]]' in content

    for content in (powershell_bootstrap, powershell_health):
        assert "[System.IO.Path]::IsPathRooted($EnvFile)" in content
        assert "$EnvFile = [System.IO.Path]::GetFullPath($EnvFile)" in content
        assert "if ($item.LinkType)" in content
        assert content.index("[System.IO.Path]::GetFullPath($EnvFile)") < content.index("Push-Location $RootDir")


def test_healthcheck_ports_are_integer_and_bounded() -> None:
    shell = read("scripts/healthcheck.sh")
    powershell = read("scripts/healthcheck.ps1")

    assert "validate_port BACKEND_PORT" in shell
    assert "validate_port FRONTEND_PORT" in shell
    assert '[[ "$value" =~ ^[0-9]+$ ]]' in shell
    assert "10#$value >= 1 && 10#$value <= 65535" in shell

    assert "Assert-Port 'BACKEND_PORT'" in powershell
    assert "Assert-Port 'FRONTEND_PORT'" in powershell
    assert "[int]::TryParse" in powershell
    assert "$port -lt 1 -or $port -gt 65535" in powershell


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


def test_healthchecks_require_docker_health_for_all_five_services() -> None:
    shell = read("scripts/healthcheck.sh")
    powershell = read("scripts/healthcheck.ps1")

    for content in (shell, powershell):
        assert "docker inspect" in content
        assert "State.Health.Status" in content
        assert "healthy" in content
        assert "ps --status running --services" not in content

    assert "for service in postgres redis neo4j backend frontend; do" in shell
    assert "foreach ($service in @('postgres', 'redis', 'neo4j', 'backend', 'frontend'))" in powershell


def test_healthchecks_require_full_readiness_not_degraded_state() -> None:
    shell = read("scripts/healthcheck.sh")
    powershell = read("scripts/healthcheck.ps1")
    assert 'ready.get("status") != "ready"' in shell
    assert "$ready.status -ne 'ready'" in powershell
    assert '"degraded"' not in shell
    assert "'degraded'" not in powershell


def test_shell_http_probes_have_bounded_timeouts() -> None:
    shell = read("scripts/healthcheck.sh")
    assert "--connect-timeout" in shell
    assert "--max-time" in shell
    assert "HOSPRIME_HTTP_CONNECT_TIMEOUT_SECONDS" in shell
    assert "HOSPRIME_HTTP_MAX_TIME_SECONDS" in shell


def test_compose_does_not_use_global_fixed_container_names() -> None:
    compose = read("docker-compose.yml")
    assert "container_name:" not in compose
    for service in ("postgres", "redis", "neo4j", "backend", "frontend"):
        assert f"  {service}:" in compose


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
