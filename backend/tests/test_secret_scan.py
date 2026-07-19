import sys
import tempfile
import unittest
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODULE_NAME = "hosprime_secret_scan"
SPEC = spec_from_file_location(MODULE_NAME, ROOT / "scripts" / "secret_scan.py")
assert SPEC and SPEC.loader
scanner_module = module_from_spec(SPEC)
sys.modules[MODULE_NAME] = scanner_module
SPEC.loader.exec_module(scanner_module)


class SecretScanTests(unittest.TestCase):
    def test_high_confidence_provider_key_is_detected_and_fully_redacted(self) -> None:
        value = "sk-" + "proj-" + "abcdefghijklmnopqrstuvwxyz" + "123456"
        line = "OPENAI_" + "API_KEY=" + repr(value)
        findings = scanner_module.scan_text("config.py", line)

        self.assertTrue(any(item.rule == "openai-key" for item in findings))
        self.assertTrue(all(item.redacted == "<redacted>" for item in findings))
        self.assertTrue(all(value[:3] not in item.redacted for item in findings))
        self.assertTrue(all(value[-3:] not in item.redacted for item in findings))

    def test_private_key_header_is_detected_without_disclosure(self) -> None:
        header = "-----BEGIN " + "PRIVATE KEY-----"
        footer = "-----END " + "PRIVATE KEY-----"
        findings = scanner_module.scan_text(
            "private.pem", "\n".join((header, "material", footer))
        )
        self.assertTrue(any(item.rule == "private-key" for item in findings))
        self.assertTrue(all(item.redacted == "<redacted>" for item in findings))

    def test_encrypted_private_key_header_is_detected_in_ordinary_text(self) -> None:
        header = "-----BEGIN " + "ENCRYPTED PRIVATE KEY-----"
        findings = scanner_module.scan_text(
            "notes.md", "\n".join(("diagnostic excerpt", header, "synthetic-fixture"))
        )

        encrypted = [item for item in findings if item.rule == "encrypted-private-key"]
        self.assertEqual(len(encrypted), 1)
        self.assertEqual(encrypted[0].line, 2)
        self.assertEqual(encrypted[0].redacted, "<redacted>")
        self.assertNotIn("ENCRYPTED", encrypted[0].redacted)

    def test_literal_credential_assignment_is_detected(self) -> None:
        name = "admin_" + "password"
        value = "Correct" + "Horse" + "Battery" + "Staple"
        findings = scanner_module.scan_text("settings.yml", f"{name}: {value}")
        self.assertTrue(any(item.rule == "credential-assignment" for item in findings))

    def test_short_literal_credentials_are_detected(self) -> None:
        key = "PASS" + "WORD"
        lines = (f"{key}=abc", f'"{key}": "1234"', f"'{key}': 'xy'")
        findings = scanner_module.scan_text("settings.yml", "\n".join(lines))
        self.assertEqual(
            sum(item.rule == "credential-assignment" for item in findings), 3
        )
        self.assertTrue(all(item.redacted == "<redacted>" for item in findings))

    def test_prefixed_environment_variable_names_are_detected(self) -> None:
        field_name = "PASS" + "WORD"
        provider_field = "API_" + "KEY"
        text = "\n".join(
            (
                f"POSTGRES_{field_name}=production-database-password",
                f"BOOTSTRAP_ADMIN_{field_name}=production-admin-password",
                f"SERVICE_{provider_field}=production-provider-key",
            )
        )
        findings = scanner_module.scan_text("settings.env", text)
        self.assertEqual(
            sum(item.rule == "credential-assignment" for item in findings), 3
        )

    def test_quoted_json_and_yaml_assignments_are_detected(self) -> None:
        field_name = "pass" + "word"
        field_c = "to" + "ken"
        text = "\n".join(
            (
                f'"database_{field_name}": "quoted value with spaces"',
                f"'service_{field_c}': 'another quoted credential value'",
            )
        )
        findings = scanner_module.scan_text("settings.json", text)
        self.assertEqual(
            sum(item.rule == "credential-assignment" for item in findings), 2
        )

    def test_safe_placeholders_explicit_nonproduction_values_and_empty_literals_are_allowed(self) -> None:
        field_name = "PASS" + "WORD"
        field_b = "SEC" + "RET"
        provider_field = "API_" + "KEY"
        env_name = "JWT_" + "SECRET"
        text = "\n".join(
            (
                f"POSTGRES_{field_name}=CHANGE_ME_POSTGRES_PASSWORD",
                f"JWT_{field_b}=${{{env_name}:?Set the required value in .env}}",
                f"BOOTSTRAP_ADMIN_{field_name}=ci-admin-password-not-for-production",
                f"{provider_field}=example-provider-key",
                f"OPTIONAL_{field_b}=null",
                f"EMPTY_{field_b}=",
            )
        )
        self.assertEqual(scanner_module.scan_text(".env.example", text), [])

    def test_ambiguous_ci_and_test_literals_are_not_allowlisted(self) -> None:
        field_name = "PASS" + "WORD"
        field_b = "SEC" + "RET"
        text = "\n".join(
            (
                f"ADMIN_{field_name}=test-password",
                f"JWT_{field_b}=ci-secret",
                f"DATABASE_{field_name}=test-local-only",
            )
        )
        findings = scanner_module.scan_text("settings.env", text)
        self.assertEqual(
            sum(item.rule == "credential-assignment" for item in findings), 3
        )

    def test_safe_marker_substrings_do_not_hide_real_credentials(self) -> None:
        field_name = "PASS" + "WORD"
        field_c = "TO" + "KEN"
        provider_field = "API_" + "KEY"
        text = "\n".join(
            (
                f"{field_name}=production-example-credential-123",
                f"{field_c}=real-test-token-material-456",
                f"{provider_field}=prefix-secret_key-production-789",
            )
        )
        findings = scanner_module.scan_text("settings.env", text)
        self.assertEqual(
            sum(item.rule == "credential-assignment" for item in findings), 3
        )

    def test_environment_references_must_match_the_whole_value(self) -> None:
        field_b = "SEC" + "RET"
        env_name = "JWT_" + "SECRET"
        self.assertEqual(
            scanner_module.scan_text(
                ".env.example", f"JWT_{field_b}=${{{env_name}}}"
            ),
            [],
        )
        findings = scanner_module.scan_text(
            "settings.env", f"JWT_{field_b}=prefix-${{{env_name}}}-suffix"
        )
        self.assertTrue(any(item.rule == "credential-assignment" for item in findings))

    def test_connection_uri_literal_password_is_detected_and_fully_redacted(self) -> None:
        scheme = "postgres" + "ql"
        literal_value = "literal" + "-database-credential"
        uri = f"{scheme}://app:{literal_value}@database:5432/app"
        findings = scanner_module.scan_text("settings.env", "DATABASE_URL=" + uri)

        uri_findings = [
            item for item in findings if item.rule == "credential-uri-userinfo"
        ]
        self.assertEqual(len(uri_findings), 1)
        self.assertEqual(uri_findings[0].redacted, "<redacted>")
        self.assertNotIn(literal_value[:3], uri_findings[0].redacted)
        self.assertNotIn(literal_value[-3:], uri_findings[0].redacted)

    def test_connection_uri_environment_reference_is_allowed(self) -> None:
        scheme = "postgres" + "ql"
        uri = f"{scheme}://app:${{POSTGRES_PASSWORD}}@database:5432/app"
        self.assertEqual(
            scanner_module.scan_text(".env.example", "DATABASE_URL=" + uri), []
        )

    def test_candidate_text_file_with_nul_bytes_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "settings.env"
            path.write_bytes(b"ADMIN_PASSWORD=abc\x00hidden")
            with self.assertRaisesRegex(RuntimeError, "contains NUL bytes"):
                scanner_module.scan_tracked_files([path])

    def test_oversized_candidate_text_file_fails_closed_without_path_disclosure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "credential-bearing-name.env"
            path.write_bytes(b"x" * (scanner_module.MAX_FILE_BYTES + 1))
            with self.assertRaisesRegex(RuntimeError, "could not be safely read") as raised:
                scanner_module.scan_tracked_files([path])
            self.assertNotIn(path.name, str(raised.exception))

    def test_deduplicate_returns_deterministic_unique_findings(self) -> None:
        finding = scanner_module.Finding(
            "a.env", 3, "credential-assignment", "<redacted>"
        )
        self.assertEqual(scanner_module.deduplicate([finding, finding]), [finding])

    def test_diff_only_requires_a_git_range(self) -> None:
        self.assertEqual(scanner_module.main(["--diff-only"]), 2)


if __name__ == "__main__":
    unittest.main()
