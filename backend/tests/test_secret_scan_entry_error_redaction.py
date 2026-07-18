import io
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
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

    def test_unexpected_exception_is_contained_without_traceback_detail(self) -> None:
        sensitive_detail = "synthetic-secret-marker-from-exception"

        def raising_scanner(_argv):
            print("partial repository-controlled output")
            raise RuntimeError(sensitive_detail)

        stdout = io.StringIO()
        stderr = io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            result = entry_module.run_scanner_safely(raising_scanner)

        self.assertEqual(result, 2)
        self.assertEqual(stdout.getvalue(), "")
        self.assertEqual(stderr.getvalue().strip(), entry_module.GENERIC_SCAN_ERROR)
        self.assertNotIn(sensitive_detail, stderr.getvalue())
        self.assertNotIn("partial repository-controlled output", stdout.getvalue())
        self.assertNotIn("Traceback", stderr.getvalue())

    def test_system_exit_is_contained_without_argparse_output(self) -> None:
        sensitive_detail = "synthetic-secret-marker-from-argparse"

        def exiting_scanner(_argv):
            print(sensitive_detail, file=sys.stderr)
            raise SystemExit(2)

        stdout = io.StringIO()
        stderr = io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            result = entry_module.run_scanner_safely(exiting_scanner)

        self.assertEqual(result, 2)
        self.assertEqual(stdout.getvalue(), "")
        self.assertEqual(stderr.getvalue().strip(), entry_module.GENERIC_SCAN_ERROR)
        self.assertNotIn(sensitive_detail, stderr.getvalue())

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

    def test_exact_pass_message_is_preserved(self) -> None:
        def passing_scanner(_argv):
            print(entry_module.SCAN_PASSED_MESSAGE)
            return 0

        stdout = io.StringIO()
        stderr = io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            result = entry_module.run_scanner_safely(passing_scanner)

        self.assertEqual(result, 0)
        self.assertEqual(stdout.getvalue(), f"{entry_module.SCAN_PASSED_MESSAGE}\n")
        self.assertEqual(stderr.getvalue(), "")

    def test_pass_with_unexpected_output_or_stderr_fails_closed(self) -> None:
        sensitive_detail = "synthetic-secret-marker"

        def noisy_passing_scanner(_argv):
            print(entry_module.SCAN_PASSED_MESSAGE)
            print(sensitive_detail, file=sys.stderr)
            return 0

        stdout = io.StringIO()
        stderr = io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            result = entry_module.run_scanner_safely(noisy_passing_scanner)

        self.assertEqual(result, 2)
        self.assertEqual(stdout.getvalue(), "")
        self.assertEqual(stderr.getvalue().strip(), entry_module.GENERIC_SCAN_ERROR)
        self.assertNotIn(sensitive_detail, stderr.getvalue())

    def test_failed_finding_replaces_repository_path_with_fingerprint(self) -> None:
        sensitive_path = "private/synthetic-secret-marker.env"

        def finding_scanner(_argv):
            print(entry_module.SCAN_FAILED_HEADER)
            print(f"{sensitive_path}:7: credential-assignment: <redacted>")
            print(entry_module.SCAN_FAILED_FOOTER)
            return 1

        stdout = io.StringIO()
        stderr = io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            result = entry_module.run_scanner_safely(finding_scanner)

        output = stdout.getvalue()
        expected_fingerprint = entry_module.path_fingerprint(sensitive_path)
        self.assertEqual(result, 1)
        self.assertEqual(stderr.getvalue(), "")
        self.assertIn(f"path-sha256={expected_fingerprint}:7", output)
        self.assertIn("credential-assignment: <redacted>", output)
        self.assertNotIn(sensitive_path, output)
        self.assertNotIn("synthetic-secret-marker", output)

    def test_unexpected_failed_scan_output_fails_closed(self) -> None:
        sensitive_detail = "synthetic-secret-marker"

        def malformed_scanner(_argv):
            print(entry_module.SCAN_FAILED_HEADER)
            print(sensitive_detail)
            print(entry_module.SCAN_FAILED_FOOTER)
            return 1

        stdout = io.StringIO()
        stderr = io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            result = entry_module.run_scanner_safely(malformed_scanner)

        self.assertEqual(result, 2)
        self.assertEqual(stdout.getvalue(), "")
        self.assertEqual(stderr.getvalue().strip(), entry_module.GENERIC_SCAN_ERROR)
        self.assertNotIn(sensitive_detail, stderr.getvalue())

    def test_failed_scan_stderr_fails_closed(self) -> None:
        sensitive_detail = "synthetic-secret-marker"

        def noisy_finding_scanner(_argv):
            print(entry_module.SCAN_FAILED_HEADER)
            print("safe.env:3: credential-assignment: <redacted>")
            print(entry_module.SCAN_FAILED_FOOTER)
            print(sensitive_detail, file=sys.stderr)
            return 1

        stdout = io.StringIO()
        stderr = io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            result = entry_module.run_scanner_safely(noisy_finding_scanner)

        self.assertEqual(result, 2)
        self.assertEqual(stdout.getvalue(), "")
        self.assertEqual(stderr.getvalue().strip(), entry_module.GENERIC_SCAN_ERROR)
        self.assertNotIn(sensitive_detail, stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
