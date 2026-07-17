import sys
import tempfile
import unittest
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
MODULE_NAME = "hosprime_secret_scan_encoding"
SPEC = spec_from_file_location(MODULE_NAME, ROOT / "scripts" / "secret_scan.py")
assert SPEC and SPEC.loader
scanner_module = module_from_spec(SPEC)
sys.modules[MODULE_NAME] = scanner_module
SPEC.loader.exec_module(scanner_module)


class SecretScanEncodingTests(unittest.TestCase):
    def test_invalid_utf8_tracked_text_file_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "settings.env"
            path.write_bytes(b"ADMIN_PASSWORD=abc\xffhidden")

            with self.assertRaisesRegex(RuntimeError, "not valid UTF-8"):
                scanner_module.scan_tracked_files([path])

    def test_invalid_utf8_git_diff_fails_closed(self) -> None:
        malformed_diff = (
            b"diff --git a/settings.env b/settings.env\n"
            b"--- a/settings.env\n"
            b"+++ b/settings.env\n"
            b"@@ -0,0 +1 @@\n"
            b"+ADMIN_PASSWORD=abc\xffhidden\n"
        )

        with patch.object(scanner_module, "run_git", return_value=malformed_diff):
            with self.assertRaisesRegex(RuntimeError, "not valid UTF-8"):
                scanner_module.scan_added_diff("base...head")

    def test_valid_utf8_diff_still_detects_and_fully_redacts(self) -> None:
        valid_diff = (
            b"diff --git a/settings.env b/settings.env\n"
            b"--- a/settings.env\n"
            b"+++ b/settings.env\n"
            b"@@ -0,0 +1 @@\n"
            b"+ADMIN_PASSWORD=synthetic-value\n"
        )

        with patch.object(scanner_module, "run_git", return_value=valid_diff):
            findings = scanner_module.scan_added_diff("base...head")

        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].rule, "credential-assignment")
        self.assertEqual(findings[0].redacted, "<redacted>")


if __name__ == "__main__":
    unittest.main()
