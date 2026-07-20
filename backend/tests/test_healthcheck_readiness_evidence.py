from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EXPECTED_CAPABILITY_WARNING = "External AI provider is not configured"


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_shell_healthcheck_requires_complete_provider_free_readiness_evidence() -> None:
    shell = read("scripts/healthcheck.sh")

    required_contracts = (
        'ready.get("status") != "ready"',
        'ready.get("database_dialect") != "postgresql"',
        'ready.get("configuration_warnings") != []',
        'ready.get("capability_warnings") != EXPECTED_CAPABILITY_WARNINGS',
        EXPECTED_CAPABILITY_WARNING,
    )
    for contract in required_contracts:
        assert contract in shell

    assert shell.index('ready.get("status") != "ready"') < shell.index(
        'ready.get("configuration_warnings") != []'
    )
    assert "Unexpected liveness response: {live}" not in shell
    assert "Backend is not fully ready: {ready}" not in shell
    assert "Expected PostgreSQL runtime: {ready}" not in shell


def test_powershell_healthcheck_requires_complete_provider_free_readiness_evidence() -> None:
    powershell = read("scripts/healthcheck.ps1")

    required_contracts = (
        "$ready.status -ne 'ready'",
        "$ready.database_dialect -ne 'postgresql'",
        "@($ready.configuration_warnings).Count -ne 0",
        "$actualCapabilityWarnings = @($ready.capability_warnings)",
        EXPECTED_CAPABILITY_WARNING,
    )
    for contract in required_contracts:
        assert contract in powershell

    assert powershell.index("$ready.status -ne 'ready'") < powershell.index(
        "@($ready.configuration_warnings).Count -ne 0"
    )
    assert "Unexpected liveness status: $($live.status)" not in powershell
    assert "Backend is not fully ready: $($ready.status)" not in powershell
    assert "Expected PostgreSQL runtime; got $($ready.database_dialect)" not in powershell


def test_healthcheck_failure_messages_do_not_serialize_readiness_payloads() -> None:
    shell = read("scripts/healthcheck.sh")
    powershell = read("scripts/healthcheck.ps1")

    for content in (shell, powershell):
        assert "Backend reported security or configuration warnings" in content
        assert "Backend provider capability evidence is incomplete or unexpected" in content
        assert "configuration_warnings=" not in content
        assert "capability_warnings=" not in content
