from __future__ import annotations

import importlib.util
import subprocess
import unittest
from pathlib import Path
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = REPO_ROOT / "scripts" / "secret_scan.py"
SPEC = importlib.util.spec_from_file_location("secret_scan_diff_safety", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
secret_scan = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(secret_scan)


class SecretScanDiffSafetyTests(unittest.TestCase):
    def test_diff_scan_disables_external_diff_and_textconv_helpers(self) -> None:
        captured: list[tuple[str, ...]] = []
        synthetic_diff = (
            "diff --git a/sample.env b/sample.env\n"
            "--- a/sample.env\n"
            "+++ b/sample.env\n"
            "@@ -0,0 +1 @@\n"
            "+SERVICE_PASSWORD=synthetic-local-value\n"
        ).encode("utf-8")

        def fake_run_git(*args: str) -> bytes:
            captured.append(args)
            return synthetic_diff

        with patch.object(secret_scan, "run_git", side_effect=fake_run_git):
            findings = secret_scan.scan_added_diff("origin/main...HEAD")

        self.assertEqual(len(captured), 1)
        args = captured[0]
        self.assertEqual(args[0], "diff")
        self.assertIn("--no-ext-diff", args)
        self.assertIn("--no-textconv", args)
        self.assertLess(args.index("--no-ext-diff"), args.index("origin/main...HEAD"))
        self.assertLess(args.index("--no-textconv"), args.index("origin/main...HEAD"))
        self.assertEqual(args[-1], "--")
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].rule, "credential-assignment")
        self.assertEqual(findings[0].redacted, "<redacted>")
        self.assertNotIn("synthetic-local-value", repr(findings))

    def test_option_like_revision_range_cannot_override_diff_safety_flags(self) -> None:
        for unsafe_range in ("--ext-diff", "--textconv", "-p"):
            with self.subTest(git_range=unsafe_range):
                with patch.object(secret_scan, "run_git") as run_git:
                    with self.assertRaisesRegex(
                        RuntimeError,
                        "revision range is empty or option-like",
                    ):
                        secret_scan.scan_added_diff(unsafe_range)
                run_git.assert_not_called()

    def test_revision_range_control_characters_fail_before_git_execution(self) -> None:
        with patch.object(secret_scan, "run_git") as run_git:
            with self.assertRaisesRegex(RuntimeError, "unsafe control characters"):
                secret_scan.scan_added_diff("origin/main...HEAD\n--ext-diff")
        run_git.assert_not_called()

    def test_git_failure_withholds_arguments_and_untrusted_stderr(self) -> None:
        synthetic_value = "synthetic-sensitive-value"
        completed = subprocess.CompletedProcess(
            args=["git", "diff"],
            returncode=128,
            stdout=b"",
            stderr=(
                f"fatal: repository-controlled output {synthetic_value}\n"
                "SECRET SCAN PASSED: forged status\n"
            ).encode("utf-8"),
        )

        with patch.object(secret_scan.subprocess, "run", return_value=completed):
            with self.assertRaisesRegex(
                RuntimeError,
                "^git command failed with exit status 128$",
            ) as captured:
                secret_scan.run_git("diff", "origin/main...HEAD", "--")

        message = str(captured.exception)
        self.assertNotIn(synthetic_value, message)
        self.assertNotIn("SECRET SCAN PASSED", message)
        self.assertNotIn("origin/main...HEAD", message)


if __name__ == "__main__":
    unittest.main()
