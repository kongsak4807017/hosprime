import sys
import unittest
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODULE_NAME = "hosprime_secret_scan"
SPEC = spec_from_file_location(MODULE_NAME, ROOT / "scripts" / "secret_scan.py")
assert SPEC and SPEC.loader
secret_scan = module_from_spec(SPEC)
sys.modules[MODULE_NAME] = secret_scan
SPEC.loader.exec_module(secret_scan)


class SecretScanTests(unittest.TestCase):
    def test_high_confidence_provider_key_is_detected_and_redacted(self) -> None:
        value = "sk-" + "proj-" + "abcdefghijklmnopqrstuvwxyz" + "123456"
        line = "OPENAI_" + "API_KEY=" + repr(value)
        findings = secret_scan.scan_text("config.py", line)

        self.assertTrue(any(item.rule == "openai-key" for item in findings))
        self.assertTrue(all(value not in item.redacted for item in findings))
        self.assertTrue(any("…" in item.redacted for item in findings))

    def test_private_key_header_is_detected(self) -> None:
        header = "-----BEGIN " + "PRIVATE KEY-----"
        footer = "-----END " + "PRIVATE KEY-----"
        findings = secret_scan.scan_text(
            "private.pem", "\n".join((header, "material", footer))
        )
        self.assertTrue(any(item.rule == "private-key" for item in findings))

    def test_literal_credential_assignment_is_detected(self) -> None:
        name = "admin_" + "password"
        value = "Correct" + "Horse" + "Battery" + "Staple"
        findings = secret_scan.scan_text("settings.yml", f"{name}: {value}")
        self.assertTrue(any(item.rule == "credential-assignment" for item in findings))

    def test_prefixed_environment_variable_names_are_detected(self) -> None:
        text = "\n".join(
            (
                "POSTGRES_PASSWORD=production-database-password",
                "BOOTSTRAP_ADMIN_PASSWORD=production-admin-password",
                "SERVICE_API_KEY=production-provider-key",
            )
        )
        findings = secret_scan.scan_text("settings.env", text)
        self.assertEqual(
            sum(item.rule == "credential-assignment" for item in findings), 3
        )

    def test_quoted_json_and_yaml_assignments_are_detected(self) -> None:
        text = "\n".join(
            (
                '"database_password": "quoted value with spaces"',
                "'service_token': 'another quoted credential value'",
            )
        )
        findings = secret_scan.scan_text("settings.json", text)
        self.assertEqual(
            sum(item.rule == "credential-assignment" for item in findings), 2
        )

    def test_safe_placeholders_and_ci_values_are_allowed(self) -> None:
        text = "\n".join(
            (
                "POSTGRES_PASSWORD=CHANGE_ME_POSTGRES_PASSWORD",
                "JWT_SECRET=${JWT_SECRET:?Set JWT_SECRET in .env}",
                "BOOTSTRAP_ADMIN_PASSWORD=ci-admin-password-not-for-production",
                "API_KEY=example-provider-key",
            )
        )
        self.assertEqual(secret_scan.scan_text(".env.example", text), [])

    def test_safe_marker_substrings_do_not_hide_real_credentials(self) -> None:
        text = "\n".join(
            (
                "PASSWORD=production-example-credential-123",
                "TOKEN=real-test-token-material-456",
                "API_KEY=prefix-secret_key-production-789",
            )
        )
        findings = secret_scan.scan_text("settings.env", text)
        self.assertEqual(
            sum(item.rule == "credential-assignment" for item in findings), 3
        )

    def test_environment_references_must_match_the_whole_value(self) -> None:
        self.assertEqual(
            secret_scan.scan_text(".env.example", "JWT_SECRET=${JWT_SECRET}"), []
        )
        findings = secret_scan.scan_text(
            "settings.env", "JWT_SECRET=prefix-${JWT_SECRET}-suffix"
        )
        self.assertTrue(any(item.rule == "credential-assignment" for item in findings))

    def test_deduplicate_returns_deterministic_unique_findings(self) -> None:
        finding = secret_scan.Finding(
            "a.env", 3, "credential-assignment", "abc…xyz"
        )
        self.assertEqual(secret_scan.deduplicate([finding, finding]), [finding])

    def test_diff_only_requires_a_git_range(self) -> None:
        self.assertEqual(secret_scan.main(["--diff-only"]), 2)


if __name__ == "__main__":
    unittest.main()
