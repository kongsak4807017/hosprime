from __future__ import annotations

import os
import shutil
import stat
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
BOOTSTRAP = ROOT / "scripts" / "bootstrap.sh"
POWERSHELL = ROOT / "scripts" / "bootstrap.ps1"
ENV_EXAMPLE = ROOT / ".env.example"


def _prepare_fixture(tmp_path: Path, overrides: dict[str, str]) -> tuple[Path, Path]:
    repo = tmp_path / "repo"
    (repo / "scripts").mkdir(parents=True)
    shutil.copy2(BOOTSTRAP, repo / "scripts" / "bootstrap.sh")
    shutil.copy2(ENV_EXAMPLE, repo / ".env.example")
    (repo / "docker-compose.yml").write_text("services: {}\n", encoding="utf-8")
    (repo / ".gitignore").write_text(".env\n", encoding="utf-8")

    values: dict[str, str] = {}
    for raw in ENV_EXAMPLE.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key] = value

    values.update(
        {
            "POSTGRES_DB": "hosprime",
            "POSTGRES_USER": "hosprime",
            "POSTGRES_PASSWORD": "synthetic-db-password",
            "DATABASE_URL": "postgresql://hosprime:synthetic-db-password@postgres:5432/hosprime",
            "POSTGRES_URL": "postgresql://hosprime:synthetic-db-password@postgres:5432/hosprime",
            "NEO4J_URI": "bolt://neo4j:7687",
            "NEO4J_USER": "neo4j",
            "NEO4J_PASSWORD": "synthetic-graph-password",
            "JWT_SECRET": "synthetic-jwt-secret-with-sufficient-length",
            "BOOTSTRAP_ADMIN_USERNAME": "admin",
            "BOOTSTRAP_ADMIN_PASSWORD": "synthetic-admin-password",
            "POSTGRES_PORT": "15432",
            "REDIS_PORT": "16379",
            "NEO4J_HTTP_PORT": "17474",
            "NEO4J_BOLT_PORT": "17687",
            "BACKEND_PORT": "18000",
            "FRONTEND_PORT": "18080",
            "HOSPRIME_BIND_ADDRESS": "127.0.0.1",
        }
    )
    values.update(overrides)
    env_file = repo / ".env"
    env_file.write_text("".join(f"{key}={value}\n" for key, value in values.items()), encoding="utf-8")
    env_file.chmod(0o600)

    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.name", "HosPrime Test"], cwd=repo, check=True)
    subprocess.run(["git", "add", "."], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-qm", "fixture"], cwd=repo, check=True)

    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    docker_log = tmp_path / "docker.log"
    docker = bin_dir / "docker"
    docker.write_text(
        "#!/usr/bin/env bash\n"
        "printf '%s\\n' \"$*\" >> \"$DOCKER_LOG\"\n"
        "case \"$*\" in\n"
        "  'info'|'compose version') exit 0 ;;\n"
        "  *'compose '*'config --quiet'*) exit 0 ;;\n"
        "  *'compose '*'up --detach --wait --wait-timeout 240'*) exit 0 ;;\n"
        "esac\n"
        "exit 0\n",
        encoding="utf-8",
    )
    docker.chmod(docker.stat().st_mode | stat.S_IXUSR)
    return repo, docker_log


def _run(repo: Path, docker_log: Path) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PATH"] = f"{docker_log.parent / 'bin'}{os.pathsep}{env['PATH']}"
    env["DOCKER_LOG"] = str(docker_log)
    env["HOSPRIME_ENV_FILE"] = str(repo / ".env")
    return subprocess.run(
        ["bash", "scripts/bootstrap.sh", "--skip-build"],
        cwd=repo,
        env=env,
        text=True,
        capture_output=True,
        timeout=30,
        check=False,
    )


@pytest.mark.parametrize(
    "overrides",
    [
        {"POSTGRES_PORT": "0"},
        {"REDIS_PORT": "65536"},
        {"BACKEND_PORT": "not-a-port"},
        {"FRONTEND_PORT": "18000"},
        {"NEO4J_HTTP_PORT": "17687"},
    ],
)
def test_shell_rejects_invalid_or_duplicate_published_ports_before_compose(
    tmp_path: Path, overrides: dict[str, str]
) -> None:
    repo, docker_log = _prepare_fixture(tmp_path, overrides)
    result = _run(repo, docker_log)

    assert result.returncode == 1
    assert "Published port values are missing, malformed, or duplicated" in result.stderr
    assert "config --quiet" not in docker_log.read_text(encoding="utf-8")
    assert "synthetic-db-password" not in result.stderr
    assert "synthetic-graph-password" not in result.stderr


def test_shell_accepts_six_unique_published_ports_and_reaches_compose(tmp_path: Path) -> None:
    repo, docker_log = _prepare_fixture(tmp_path, {})
    result = _run(repo, docker_log)

    assert result.returncode == 0, result.stderr
    log = docker_log.read_text(encoding="utf-8")
    assert "config --quiet" in log
    assert "up --detach --wait --wait-timeout 240" in log


def test_powershell_enforces_port_validation_before_compose() -> None:
    source = POWERSHELL.read_text(encoding="utf-8")

    assert "function Assert-PublishedPortConfiguration" in source
    assert "POSTGRES_PORT" in source
    assert "REDIS_PORT" in source
    assert "NEO4J_HTTP_PORT" in source
    assert "NEO4J_BOLT_PORT" in source
    assert "BACKEND_PORT" in source
    assert "FRONTEND_PORT" in source
    assert "Published port values are missing, malformed, or duplicated." in source
    assert source.index("Assert-PublishedPortConfiguration $EnvFile") < source.index(
        "$status = Invoke-Compose config --quiet"
    )
