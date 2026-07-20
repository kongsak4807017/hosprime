import sys
import unittest
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODULE_NAME = "hosprime_secret_scan_env_defaults"
SPEC = spec_from_file_location(MODULE_NAME, ROOT / "scripts" / "secret_scan.py")
assert SPEC and SPEC.loader
scanner_module = module_from_spec(SPEC)
sys.modules[MODULE_NAME] = scanner_module
SPEC.loader.exec_module(scanner_module)


class SecretScanEnvironmentDefaultTests(unittest.TestCase):
    def test_required_environment_references_remain_allowed(self) -> None:
        credential_key = "JWT_" + "SECRET"
        safe_values = (
            "${JWT_SECRET}",
            "${JWT_SECRET?Set JWT_SECRET}",
            "${JWT_SECRET:?Set JWT_SECRET in .env}",
        )

        for value in safe_values:
            with self.subTest(value=value):
                self.assertEqual(
                    scanner_module.scan_text(
                        ".env.example", f"{credential_key}={value}"
                    ),
                    [],
                )

    def test_compose_fixed_defaults_are_detected_and_fully_redacted(self) -> None:
        credential_key = "ADMIN_" + "PASSWORD"
        unsafe_values = (
            "${ADMIN_PASSWORD-default-password}",
            "${ADMIN_PASSWORD:-default-password}",
            "${ADMIN_PASSWORD+alternate-password}",
            "${ADMIN_PASSWORD:+alternate-password}",
        )

        for value in unsafe_values:
            with self.subTest(value=value):
                findings = scanner_module.scan_text(
                    "docker-compose.yml", f"{credential_key}={value}"
                )
                assignments = [
                    item for item in findings if item.rule == "credential-assignment"
                ]
                self.assertEqual(len(assignments), 1)
                self.assertEqual(assignments[0].redacted, "<redacted>")
                self.assertNotIn("password", assignments[0].redacted)

    def test_uri_password_with_fixed_environment_default_is_detected(self) -> None:
        uri = (
            "postgresql://app:${POSTGRES_PASSWORD:-default-password}"
            "@database:5432/app"
        )
        findings = scanner_module.scan_text(
            "docker-compose.yml", "DATABASE_URL=" + uri
        )

        uri_findings = [
            item for item in findings if item.rule == "credential-uri-userinfo"
        ]
        self.assertEqual(len(uri_findings), 1)
        self.assertEqual(uri_findings[0].redacted, "<redacted>")


if __name__ == "__main__":
    unittest.main()
