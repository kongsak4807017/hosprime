import io
import sys
import unittest
from contextlib import redirect_stderr
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
MODULE_NAME = "hosprime_secret_scan_entry_error_redaction"
SPEC = spec_from_file_location(MODULE_NAME, ROOT / "scripts" / "secret_scan_entry.py")
assert SPEC and SPEC.loader
entry_module = module_from_spec(SPEC)
sys.modules[MODULE_NAME] = entry_module
SPEC.loader.exec_module(entry_module)


class SecretScanEntryErrorRedactionTests(unittest.TestCase):
    def test_operational_error_withholds_path_and_os_detail(self) -> None:
        sensitive_path = "private/credential-bearing-name.env"
        sensitive_detail = "permission denied for synthetic-secret-marker"

        def failing_scanner(_argv):
            print(
                f"SECRET SCAN ERROR: cannot read tracked file {sensitive_path}: "
                f"{sensitive_detail}",
                file=sys.stderr,
            )
            return 2

        stderr = io.StringIO()
        with redirect_stderr(stderr):
            result = entry_module.run_scanner_safely(failing_scanner)

        output = stderr.getvalue()
        self.assertEqual(result, 2)
        self.assertEqual(output.strip(), entry_module.GENERIC_SCAN_ERROR)
        self.assertNotIn(sensitive_path, output)
        self.assertNotIn(sensitive_detail, output)
        self.assertNotIn("synthetic-secret-marker", output)

    def test_validated_path_failure_uses_same_generic_error(self) -> None:
        stderr = io.StringIO()
        with patch.object(
            entry_module,
            "validate_tracked_paths",
            side_effect=RuntimeError("unsafe path: synthetic-secret-marker.env"),
        ), redirect_stderr(stderr):
            result = entry_module.main([])

        output = stderr.getvalue()
        self.assertEqual(result, 2)
        self.assertEqual(output.strip(), entry_module.GENERIC_SCAN_ERROR)
        self.assertNotIn("synthetic-secret-marker", output)

    def test_non_error_scanner_stderr_is_preserved(self) -> None:
        def diagnostic_scanner(_argv):
            print("usage diagnostic", file=sys.stderr)
            return 0

        stderr = io.StringIO()
        with redirect_stderr(stderr):
            result = entry_module.run_scanner_safely(diagnostic_scanner)

        self.assertEqual(result, 0)
        self.assertEqual(stderr.getvalue(), "usage diagnostic\n")


if __name__ == "__main__":
    unittest.main()
