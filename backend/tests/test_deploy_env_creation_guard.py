import os
import shutil
import stat
import subprocess
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_shell_checks_git_ignore_before_creating_runtime_env() -> None:
    script = read("scripts/bootstrap.sh")
    guard_call = "assert_in_repo_env_is_ignored"
    creation_gate = 'if [[ ! -e "$ENV_FILE" ]]; then'
    copy_call = 'cp .env.example "$ENV_FILE"'

    # The invocation after source/provenance validation must precede both the
    # missing-file branch and the first write to the selected runtime path.
    invocation = script.index(guard_call, script.index('export HOSPRIME_BUILD_GIT_SHA="$SOURCE_SHA"'))
    assert invocation < script.index(creation_gate)
    assert invocation < script.index(copy_call)
    assert 'git check-ignore -q -- "$relative_path"' in script


def test_powershell_checks_git_ignore_before_creating_runtime_env() -> None:
    script = read("scripts/bootstrap.ps1")
    guard_call = "Assert-InRepoEnvIsIgnored $EnvFile"
    creation_gate = "if (-not (Test-Path -LiteralPath $EnvFile)) {"
    copy_call = "Copy-Item -LiteralPath (Join-Path $RootDir '.env.example') -Destination $EnvFile"

    invocation = script.index(guard_call, script.index("$env:HOSPRIME_BUILD_GIT_SHA = $SourceSha"))
    assert invocation < script.index(creation_gate)
    assert invocation < script.index(copy_call)
    assert "& git check-ignore -q -- $relativePath" in script


def test_external_runtime_env_paths_remain_supported() -> None:
    shell = read("scripts/bootstrap.sh")
    powershell = read("scripts/bootstrap.ps1")

    # Both guards are conditional on repository containment; external paths
    # do not run git check-ignore and continue to the normal creation flow.
    assert "if not inside:\n    raise SystemExit(1)" in shell
    assert "if ($Path.StartsWith($rootPrefix, [System.StringComparison]::OrdinalIgnoreCase))" in powershell


def _run(command: list[str], *, cwd: Path, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def _prepare_shell_fixture(tmp_path: Path, *, ignored_path: str | None = None) -> tuple[Path, dict[str, str], Path]:
    if os.name == "nt":
        pytest.skip("POSIX bootstrap execution contract")
    for command in ("bash", "git", "python3"):
        if shutil.which(command) is None:
            pytest.skip(f"required command unavailable: {command}")

    repo = tmp_path / "repo"
    scripts = repo / "scripts"
    scripts.mkdir(parents=True)
    shutil.copy2(ROOT / "scripts" / "bootstrap.sh", scripts / "bootstrap.sh")
    shutil.copy2(ROOT / ".env.example", repo / ".env.example")

    if ignored_path is not None:
        (repo / ".gitignore").write_text(f"/{ignored_path}\n", encoding="utf-8")

    assert _run(["git", "init", "-q"], cwd=repo).returncode == 0
    assert _run(["git", "config", "user.name", "HosPrime Test"], cwd=repo).returncode == 0
    assert _run(["git", "config", "user.email", "test@example.invalid"], cwd=repo).returncode == 0
    assert _run(["git", "add", "."], cwd=repo).returncode == 0
    commit = _run(["git", "commit", "-qm", "fixture"], cwd=repo)
    assert commit.returncode == 0, commit.stderr

    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    docker_log = tmp_path / "docker.log"
    docker_stub = bin_dir / "docker"
    docker_stub.write_text(
        "#!/usr/bin/env sh\n"
        "printf '%s\\n' \"$*\" >> \"$HOSPRIME_TEST_DOCKER_LOG\"\n"
        "exit 0\n",
        encoding="utf-8",
    )
    docker_stub.chmod(docker_stub.stat().st_mode | stat.S_IXUSR)

    env = os.environ.copy()
    env["PATH"] = f"{bin_dir}{os.pathsep}{env.get('PATH', '')}"
    env["HOSPRIME_TEST_DOCKER_LOG"] = str(docker_log)
    env["HOSPRIME_COMPOSE_PROJECT_NAME"] = "hosprime-test"
    return repo, env, docker_log


def test_shell_creates_new_ignored_in_repo_env_before_stopping_for_configuration(tmp_path: Path) -> None:
    target_name = "runtime.env"
    repo, env, docker_log = _prepare_shell_fixture(tmp_path, ignored_path=target_name)
    target = repo / target_name
    env["HOSPRIME_ENV_FILE"] = str(target)

    result = _run(["bash", "scripts/bootstrap.sh"], cwd=repo, env=env)

    assert result.returncode == 2
    assert target.is_file()
    assert stat.S_IMODE(target.stat().st_mode) == 0o600
    assert "Replace every CHANGE_ME value" in result.stdout
    docker_calls = docker_log.read_text(encoding="utf-8").splitlines()
    assert docker_calls == ["info", "compose version"]


def test_shell_rejects_new_nonignored_in_repo_env_before_any_write_or_compose(tmp_path: Path) -> None:
    repo, env, docker_log = _prepare_shell_fixture(tmp_path)
    target = repo / "runtime.env"
    env["HOSPRIME_ENV_FILE"] = str(target)

    result = _run(["bash", "scripts/bootstrap.sh"], cwd=repo, env=env)

    assert result.returncode == 1
    assert not target.exists()
    assert "must be ignored by Git" in result.stderr
    docker_calls = docker_log.read_text(encoding="utf-8").splitlines()
    assert docker_calls == ["info", "compose version"]
    assert not any(call.startswith("compose config") for call in docker_calls)


def test_shell_creates_new_external_env_with_owner_only_permissions(tmp_path: Path) -> None:
    repo, env, docker_log = _prepare_shell_fixture(tmp_path)
    external_dir = tmp_path / "external"
    external_dir.mkdir()
    target = external_dir / "runtime.env"
    env["HOSPRIME_ENV_FILE"] = str(target)

    result = _run(["bash", "scripts/bootstrap.sh"], cwd=repo, env=env)

    assert result.returncode == 2
    assert target.is_file()
    assert stat.S_IMODE(target.stat().st_mode) == 0o600
    docker_calls = docker_log.read_text(encoding="utf-8").splitlines()
    assert docker_calls == ["info", "compose version"]
