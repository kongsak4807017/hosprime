from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_bootstrap_requires_exact_pristine_git_source() -> None:
    shell = read("scripts/bootstrap.sh")
    powershell = read("scripts/bootstrap.ps1")

    assert "git rev-parse --verify HEAD" in shell
    assert "git status --porcelain=v1 --untracked-files=all" in shell
    assert "HosPrime checkout must be pristine before bootstrap" in shell
    assert 'HOSPRIME_EXPECTED_GIT_SHA="$SOURCE_SHA"' in shell
    assert 'export HOSPRIME_BUILD_GIT_SHA="$SOURCE_SHA"' in shell

    assert "git rev-parse --verify HEAD" in powershell
    assert "git status --porcelain=v1 --untracked-files=all" in powershell
    assert "HosPrime checkout must be pristine before bootstrap" in powershell
    assert "-ExpectedGitSha $SourceSha" in powershell
    assert "$env:HOSPRIME_BUILD_GIT_SHA = $SourceSha" in powershell


def test_health_evidence_rejects_source_commit_drift() -> None:
    shell = read("scripts/healthcheck.sh")
    powershell = read("scripts/healthcheck.ps1")

    assert 'EXPECTED_GIT_SHA="${HOSPRIME_EXPECTED_GIT_SHA:-}"' in shell
    assert '[[ -z "$EXPECTED_GIT_SHA" || "$SOURCE_SHA" == "$EXPECTED_GIT_SHA" ]]' in shell
    assert "HosPrime checkout must be pristine for health evidence" in shell
    assert "source commit: %s" in shell

    assert "[string]$ExpectedGitSha = $env:HOSPRIME_EXPECTED_GIT_SHA" in powershell
    assert "$SourceSha -ne $ExpectedGitSha" in powershell
    assert "HosPrime checkout must be pristine for health evidence" in powershell
    assert "source commit: $SourceSha" in powershell


def test_application_images_are_stamped_and_verified_against_source() -> None:
    compose = read("docker-compose.yml")
    backend_dockerfile = read("backend/Dockerfile")
    frontend_dockerfile = read("frontend/Dockerfile")
    shell = read("scripts/healthcheck.sh")
    powershell = read("scripts/healthcheck.ps1")

    assert compose.count("HOSPRIME_GIT_SHA: ${HOSPRIME_BUILD_GIT_SHA:?") == 2
    for dockerfile in (backend_dockerfile, frontend_dockerfile):
        assert "ARG HOSPRIME_GIT_SHA" in dockerfile
        assert "LABEL org.opencontainers.image.revision=$HOSPRIME_GIT_SHA" in dockerfile

    assert "container_image_id()" in shell
    assert "image_source_revision()" in shell
    assert '[[ "$revision" == "$SOURCE_SHA" ]]' in shell
    assert "org.opencontainers.image.revision" in shell

    assert "Get-ContainerImageId" in powershell
    assert "Get-ImageSourceRevision" in powershell
    assert "$revision -ne $SourceSha" in powershell
    assert "org.opencontainers.image.revision" in powershell


def test_source_provenance_does_not_print_environment_values() -> None:
    for path in (
        "scripts/bootstrap.sh",
        "scripts/bootstrap.ps1",
        "scripts/healthcheck.sh",
        "scripts/healthcheck.ps1",
    ):
        content = read(path)
        assert "git diff" not in content
        assert "git status --short --branch" not in content
        assert "cat $ENV_FILE" not in content
        assert "Get-Content -LiteralPath $EnvFile | Write-Host" not in content
