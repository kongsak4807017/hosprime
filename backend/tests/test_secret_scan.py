from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC = spec_from_file_location("hosprime_secret_scan", ROOT / "scripts" / "secret_scan.py")
assert SPEC and SPEC.loader
secret_scan = module_from_spec(SPEC)
SPEC.loader.exec_module(secret_scan)


def test_high_confidence_provider_key_is_detected_and_redacted() -> None:
    value = "sk-proj-abcdefghijklmnopqrstuvwxyz123456"
    findings = secret_scan.scan_text("config.py", f'OPENAI_API_KEY="{value}"')

    assert any(item.rule == "openai-key" for item in findings)
    assert all(value not in item.redacted for item in findings)
    assert any("…" in item.redacted for item in findings)


def test_private_key_header_is_detected() -> None:
    findings = secret_scan.scan_text(
        "private.pem", "-----BEGIN PRIVATE KEY-----\nmaterial\n-----END PRIVATE KEY-----"
    )
    assert any(item.rule == "private-key" for item in findings)


def test_literal_credential_assignment_is_detected() -> None:
    findings = secret_scan.scan_text(
        "settings.yml", "admin_password: CorrectHorseBatteryStaple"
    )
    assert any(item.rule == "credential-assignment" for item in findings)


def test_safe_placeholders_and_ci_values_are_allowed() -> None:
    text = "\n".join(
        (
            "POSTGRES_PASSWORD=CHANGE_ME_POSTGRES_PASSWORD",
            "JWT_SECRET=${JWT_SECRET:?Set JWT_SECRET in .env}",
            "BOOTSTRAP_ADMIN_PASSWORD=ci-admin-password-not-for-production",
            "API_KEY=example-provider-key",
        )
    )
    assert secret_scan.scan_text(".env.example", text) == []


def test_deduplicate_returns_deterministic_unique_findings() -> None:
    finding = secret_scan.Finding("a.env", 3, "credential-assignment", "abc…xyz")
    assert secret_scan.deduplicate([finding, finding]) == [finding]


def test_diff_only_requires_a_git_range() -> None:
    assert secret_scan.main(["--diff-only"]) == 2
