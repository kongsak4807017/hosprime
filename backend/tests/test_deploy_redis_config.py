import os
import stat
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _run(
    args: list[str],
    cwd: Path,
    env: dict[str, str] | None = None,
    timeout: int = 30,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=cwd,
        env=env,
        text=True,
        capture_output=True,
        check=False,
        timeout=timeout,
    )


def _prepare_fixture(tmp_path: Path) -> tuple[Path, Path, Path]:
    repo = tmp_path / "repo"
    scripts = repo / "scripts"
    scripts.mkdir(parents=True)
    (scripts / "bootstrap.sh").write_text(
        (ROOT / "scripts/bootstrap.sh").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    (scripts / "healthcheck.sh").write_text("#!/usr/bin/env bash\nexit 0\n", encoding="utf-8")
    (repo / ".env.example").write_text("# fixture\n", encoding="utf-8")
    (repo / ".gitignore").write_text(".env\n", encoding="utf-8")

    docker_log = tmp_path / "docker.log"
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    docker_stub = bin_dir / "docker"
    docker_stub.write_text(
        """#!/usr/bin/env bash
set -eu
printf '%s\\n' "$*" >> "$DOCKER_LOG"
if [[ "${1:-}" == "info" ]]; then exit 0; fi
if [[ "${1:-}" == "compose" && "${2:-}" == "version" ]]; then exit 0; fi
exit 0
""",
        encoding="utf-8",
    )
    docker_stub.chmod(docker_stub.stat().st_mode | stat.S_IXUSR)

    _run(["git", "init"], repo)
    _run(["git", "config", "user.email", "test@example.invalid"], repo)
    _run(["git", "config", "user.name", "HosPrime Test"], repo)
    _run(["git", "add", "."], repo)
    committed = _run(["git", "commit", "-m", "fixture"], repo)
    assert committed.returncode == 0, committed.stderr
    return repo, bin_dir, docker_log


def _write_env(path: Path, redis_url: str) -> None:
    path.write_text(
        "\n".join(
            (
                "HOSPRIME_BIND_ADDRESS=127.0.0.1",
                "POSTGRES_DB=hosprime",
                "POSTGRES_USER=hosprime",
                "POSTGRES_PASSWORD=fixture-postgres-password",
                "POSTGRES_PORT=15432",
                "DATABASE_URL=postgresql://hosprime:fixture-postgres-password@postgres:5432/hosprime",
                "POSTGRES_URL=postgresql://hosprime:fixture-postgres-password@postgres:5432/hosprime",
                f"REDIS_URL={redis_url}",
                "REDIS_PORT=16379",
                "NEO4J_URI=bolt://neo4j:7687",
                "NEO4J_USER=neo4j",
                "NEO4J_PASSWORD=fixture-neo4j-password",
                "NEO4J_HTTP_PORT=17474",
                "NEO4J_BOLT_PORT=17687",
                "JWT_SECRET=fixture-jwt-secret-long-enough-for-validation",
                "BOOTSTRAP_ADMIN_USERNAME=admin",
                "BOOTSTRAP_ADMIN_PASSWORD=fixture-admin-password",
                "GEMINI_API_KEY=",
                "BACKEND_PORT=18000",
                "FRONTEND_PORT=18080",
            )
        )
        + "\n",
        encoding="utf-8",
    )


def _bootstrap_env(bin_dir: Path, docker_log: Path, env_file: Path) -> dict[str, str]:
    env = os.environ.copy()
    env.update(
        {
            "PATH": f"{bin_dir}{os.pathsep}{env['PATH']}",
            "DOCKER_LOG": str(docker_log),
            "HOSPRIME_ENV_FILE": str(env_file),
            "HOSPRIME_COMPOSE_PROJECT_NAME": "hosprime-test",
        }
    )
    return env


def test_shell_rejects_wrong_internal_redis_host_before_compose(tmp_path: Path) -> None:
    repo, bin_dir, docker_log = _prepare_fixture(tmp_path)
    env_file = tmp_path / "runtime.env"
    _write_env(env_file, "redis://wrong-host:6379/0")

    result = _run(
        ["bash", "scripts/bootstrap.sh", "--skip-build"],
        repo,
        _bootstrap_env(bin_dir, docker_log, env_file),
    )

    combined = result.stdout + result.stderr
    assert result.returncode == 1
    assert "Redis environment values are missing, malformed, or inconsistent" in combined
    assert "wrong-host" not in combined
    assert "config --quiet" not in docker_log.read_text(encoding="utf-8")


def test_shell_rejects_redis_credentials_query_or_fragment_before_compose(tmp_path: Path) -> None:
    invalid_urls = (
        "redis://user:password@redis:6379/0",
        "redis://redis:6379/0?ssl=true",
        "redis://redis:6379/0#fragment",
    )
    for index, redis_url in enumerate(invalid_urls):
        case_dir = tmp_path / str(index)
        case_dir.mkdir()
        repo, bin_dir, docker_log = _prepare_fixture(case_dir)
        env_file = case_dir / "runtime.env"
        _write_env(env_file, redis_url)

        result = _run(
            ["bash", "scripts/bootstrap.sh", "--skip-build"],
            repo,
            _bootstrap_env(bin_dir, docker_log, env_file),
        )

        combined = result.stdout + result.stderr
        assert result.returncode == 1
        assert "Redis environment values are missing, malformed, or inconsistent" in combined
        assert "password" not in combined
        assert "ssl=true" not in combined
        assert "fragment" not in combined
        assert "config --quiet" not in docker_log.read_text(encoding="utf-8")


def test_shell_accepts_canonical_internal_redis_url_with_custom_published_port(tmp_path: Path) -> None:
    repo, bin_dir, docker_log = _prepare_fixture(tmp_path)
    env_file = tmp_path / "runtime.env"
    _write_env(env_file, "redis://redis:6379/0")

    result = _run(
        ["bash", "scripts/bootstrap.sh", "--skip-build"],
        repo,
        _bootstrap_env(bin_dir, docker_log, env_file),
    )

    assert result.returncode == 0, result.stdout + result.stderr
    log = docker_log.read_text(encoding="utf-8")
    assert "config --quiet" in log
    assert "up --detach --wait --wait-timeout 240" in log


def test_powershell_validates_redis_url_before_compose() -> None:
    powershell = (ROOT / "scripts/bootstrap.ps1").read_text(encoding="utf-8")

    assert "function Assert-RedisConfiguration" in powershell
    assert "$uri.Scheme -ne 'redis'" in powershell
    assert "$uri.Host -ne 'redis'" in powershell
    assert "$uri.Port -ne 6379" in powershell
    assert "$uri.AbsolutePath -ne '/0'" in powershell
    assert powershell.index("Assert-RedisConfiguration $EnvFile") < powershell.index(
        "Invoke-Compose config --quiet"
    )
