from pathlib import Path

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
