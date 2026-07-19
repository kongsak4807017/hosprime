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


def test_bootstrap_rejects_tracked_in_repo_environment_files() -> None:
    shell = read("scripts/bootstrap.sh")
    powershell = read("scripts/bootstrap.ps1")

    assert "assert_in_repo_env_is_ignored" in shell
    assert 'git check-ignore -q -- "$relative_path"' in shell
    assert "os.path.commonpath((root, path)) == root" in shell
    assert "Environment file inside repository must be ignored by Git" in shell
    assert shell.index("assert_in_repo_env_is_ignored") < shell.index("compose config --quiet")

    assert "Assert-InRepoEnvIsIgnored" in powershell
    assert "StartsWith($rootPrefix, [System.StringComparison]::OrdinalIgnoreCase)" in powershell
    assert "& git check-ignore -q -- $relativePath" in powershell
    assert "Environment file inside repository must be ignored by Git" in powershell
    assert powershell.index("Assert-InRepoEnvIsIgnored $EnvFile") < powershell.index("Invoke-Compose config --quiet")


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


def test_healthcheck_endpoints_use_compose_runtime_ports() -> None:
    shell = read("scripts/healthcheck.sh")
    powershell = read("scripts/healthcheck.ps1")

    assert 'BACKEND_PORT="$(published_port backend 8000)"' in shell
    assert 'FRONTEND_PORT="$(published_port frontend 80)"' in shell
    assert 'compose port "$service" "$container_port"' in shell
    assert "read_env" not in shell
    assert 'grep -E "^[[:space:]]*${key}="' not in shell
    assert '[[ "$value" =~ ^[0-9]+$ ]]' in shell
    assert "10#$value >= 1 && 10#$value <= 65535" in shell

    assert "$BackendPort = Get-PublishedPort 'backend' 8000" in powershell
    assert "$FrontendPort = Get-PublishedPort 'frontend' 80" in powershell
    assert "docker compose --project-name $ProjectName --env-file $EnvFile port" in powershell
    assert "Read-EnvValue" not in powershell
    assert "[int]::TryParse" in powershell
    assert "$port -lt 1 -or $port -gt 65535" in powershell


def test_healthcheck_runtime_port_discovery_fails_closed_on_ambiguous_bindings() -> None:
    shell = read("scripts/healthcheck.sh")
    powershell = read("scripts/healthcheck.ps1")

    assert "sort -u" in shell
    assert '[[ "$bindings" != *$\'\\n\'* ]]' in shell
    assert "No published host port" in shell
    assert "Multiple published host ports" in shell

    assert "Sort-Object -Unique" in powershell
    assert "$bindings.Count -ne 1" in powershell
    assert "Unexpected published-port binding" in powershell
    assert "Expected one published host port" in powershell


def test_healthchecks_require_runtime_loopback_bindings_for_all_published_services() -> None:
    shell = read("scripts/healthcheck.sh")
    powershell = read("scripts/healthcheck.ps1")

    shell_calls = (
        'published_port postgres 5432',
        'published_port redis 6379',
        'published_port neo4j 7474',
        'published_port neo4j 7687',
        'published_port backend 8000',
        'published_port frontend 80',
    )
    for call in shell_calls:
        assert call in shell
    assert '127\\.0\\.0\\.1:([0-9]+)' in shell
    assert "Published binding must use 127.0.0.1" in shell

    powershell_calls = (
        "Get-PublishedPort 'postgres' 5432",
        "Get-PublishedPort 'redis' 6379",
        "Get-PublishedPort 'neo4j' 7474",
        "Get-PublishedPort 'neo4j' 7687",
        "Get-PublishedPort 'backend' 8000",
        "Get-PublishedPort 'frontend' 80",
    )
    for call in powershell_calls:
        assert call in powershell
    assert "^127\\.0\\.0\\.1:(\\d+)$" in powershell
    assert "Published binding must use 127.0.0.1" in powershell


def test_healthchecks_require_unique_project_scoped_service_containers() -> None:
    shell = read("scripts/healthcheck.sh")
    powershell = read("scripts/healthcheck.ps1")

    assert 'compose ps -q "$service"' in shell
    assert '[[ "$ids" != *$\'\\n\'* ]]' in shell
    assert '[[ "$ids" =~ ^[0-9a-f]{12,64}$ ]]' in shell
    assert 'com.docker.compose.project' in shell
    assert 'com.docker.compose.service' in shell
    assert '[[ "$identity" == "$PROJECT_NAME|$service" ]]' in shell

    assert "Sort-Object -Unique" in powershell
    assert "$ids.Count -ne 1" in powershell
    assert "$ids[0] -notmatch '^[0-9a-f]{12,64}$'" in powershell
    assert 'com.docker.compose.project' in powershell
    assert 'com.docker.compose.service' in powershell
    assert '$identity -ne "${ProjectName}|${service}"' in powershell


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


def test_compose_published_ports_bind_to_loopback_by_default() -> None:
    compose = read("docker-compose.yml")
    env_example = read(".env.example")

    assert "HOSPRIME_BIND_ADDRESS=127.0.0.1" in env_example
    assert "Change this only when remote access is intentionally required" in env_example

    expected_mappings = (
        '${HOSPRIME_BIND_ADDRESS:-127.0.0.1}:${POSTGRES_PORT:-5432}:5432',
        '${HOSPRIME_BIND_ADDRESS:-127.0.0.1}:${REDIS_PORT:-6379}:6379',
        '${HOSPRIME_BIND_ADDRESS:-127.0.0.1}:${NEO4J_HTTP_PORT:-7474}:7474',
        '${HOSPRIME_BIND_ADDRESS:-127.0.0.1}:${NEO4J_BOLT_PORT:-7687}:7687',
        '${HOSPRIME_BIND_ADDRESS:-127.0.0.1}:${BACKEND_PORT:-8000}:8000',
        '${HOSPRIME_BIND_ADDRESS:-127.0.0.1}:${FRONTEND_PORT:-80}:80',
    )
    for mapping in expected_mappings:
        assert mapping in compose

    assert '- "${POSTGRES_PORT:-5432}:5432"' not in compose
    assert '- "${REDIS_PORT:-6379}:6379"' not in compose
    assert '- "${BACKEND_PORT:-8000}:8000"' not in compose
    assert '- "${FRONTEND_PORT:-80}:80"' not in compose


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
