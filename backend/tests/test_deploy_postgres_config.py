import os
import stat
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _run(args: list[str], cwd: Path, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=cwd,
        env=env,
        text=True,
        capture_output=True,
        check=False,
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


def _write_env(path: Path, password: str, url_password: str) -> None:
    path.write_text(
        "\n".join(
            (
                "POSTGRES_DB=hosprime",
                "POSTGRES_USER=hosprime",
                f"POSTGRES_PASSWORD={password}",
                f"DATABASE_URL=postgresql://hosprime:{url_password}@postgres:5432/hosprime",
                f"POSTGRES_URL=postgresql://hosprime:{url_password}@postgres:5432/hosprime",
                "NEO4J_USER=neo4j",
                "NEO4J_PASSWORD=fixture-neo4j-password",
                "JWT_SECRET=fixture-jwt-secret-long-enough-for-validation",
                "BOOTSTRAP_ADMIN_USERNAME=admin",
                "BOOTSTRAP_ADMIN_PASSWORD=fixture-admin-password",
                "GEMINI_API_KEY=",
            )
        )
        + "\n",
        encoding="utf-8",
    )


def test_shell_rejects_inconsistent_postgres_credentials_before_compose(tmp_path: Path) -> None:
    repo, bin_dir, docker_log = _prepare_fixture(tmp_path)
    env_file = tmp_path / "runtime.env"
    _write_env(env_file, "correct-password", "different-password")

    env = os.environ.copy()
    env.update(
        {
            "PATH": f"{bin_dir}{os.pathsep}{env['PATH']}",
            "DOCKER_LOG": str(docker_log),
            "HOSPRIME_ENV_FILE": str(env_file),
            "HOSPRIME_COMPOSE_PROJECT_NAME": "hosprime-test",
        }
    )
    result = _run(["bash", "scripts/bootstrap.sh", "--skip-build"], repo, env)

    assert result.returncode == 1
    combined = result.stdout + result.stderr
    assert "PostgreSQL environment values are missing, malformed, or inconsistent" in combined
    assert "correct-password" not in combined
    assert "different-password" not in combined
    assert "config --quiet" not in docker_log.read_text(encoding="utf-8")


def test_shell_accepts_url_encoded_postgres_password_and_runs_compose(tmp_path: Path) -> None:
    repo, bin_dir, docker_log = _prepare_fixture(tmp_path)
    env_file = tmp_path / "runtime.env"
    _write_env(env_file, "correct:password@value", "correct%3Apassword%40value")

    env = os.environ.copy()
    env.update(
        {
            "PATH": f"{bin_dir}{os.pathsep}{env['PATH']}",
            "DOCKER_LOG": str(docker_log),
            "HOSPRIME_ENV_FILE": str(env_file),
            "HOSPRIME_COMPOSE_PROJECT_NAME": "hosprime-test",
        }
    )
    result = _run(["bash", "scripts/bootstrap.sh", "--skip-build"], repo, env)

    assert result.returncode == 0, result.stdout + result.stderr
    log = docker_log.read_text(encoding="utf-8")
    assert "config --quiet" in log
    assert "up --detach --wait --wait-timeout 240" in log


def test_powershell_validates_postgres_urls_before_compose() -> None:
    powershell = (ROOT / "scripts/bootstrap.ps1").read_text(encoding="utf-8")

    assert "function Assert-PostgresConfiguration" in powershell
    assert "[System.Uri]::TryCreate" in powershell
    assert "[System.Uri]::UnescapeDataString" in powershell
    assert "POSTGRES_PASSWORD" in powershell
    assert powershell.index("Assert-PostgresConfiguration $EnvFile") < powershell.index(
        "Invoke-Compose config --quiet"
    )
