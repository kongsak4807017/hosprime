import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import verify_secret_gate

BASE_SHA = "1" * 40
HEAD_SHA = "2" * 40


class VerifySecretGateTests(unittest.TestCase):
    def test_build_commands_runs_complete_gate_in_order(self) -> None:
        commands = verify_secret_gate.build_commands("base...head")

        self.assertEqual(commands[0][1:4], ["-m", "unittest", "discover"])
        self.assertEqual(commands[1][1:], ["scripts/secret_artifact_gate.py"])
        self.assertEqual(commands[2][1:], ["scripts/secret_scan_m0_entry.py"])
        self.assertEqual(
            commands[3][1:],
            [
                "scripts/secret_scan_m0_entry.py",
                "--git-range",
                "base...head",
                "--diff-only",
            ],
        )
        self.assertTrue(all(command[0] == sys.executable for command in commands))

    def test_no_range_omits_only_diff_scan(self) -> None:
        commands = verify_secret_gate.build_commands(None)

        self.assertEqual(len(commands), 3)
        self.assertFalse(any("--diff-only" in command for command in commands))

    @patch.object(verify_secret_gate.subprocess, "run")
    def test_success_runs_all_commands_from_repository_root(self, run) -> None:
        run.return_value = subprocess.CompletedProcess([], 0)
        commands = [["python", "first"], ["python", "second"]]

        with patch("builtins.print") as emit:
            status = verify_secret_gate.run_commands(commands)

        self.assertEqual(status, 0)
        self.assertEqual(run.call_count, 2)
        self.assertTrue(all(call.kwargs["cwd"] == ROOT for call in run.call_args_list))
        emit.assert_called_once_with(verify_secret_gate.PASS_MESSAGE)

    @patch.object(verify_secret_gate.subprocess, "run")
    def test_failure_stops_without_running_later_gate(self, run) -> None:
        run.side_effect = [
            subprocess.CompletedProcess([], 0),
            subprocess.CompletedProcess([], 7),
        ]

        status = verify_secret_gate.run_commands(
            [["python", "first"], ["python", "second"], ["python", "third"]]
        )

        self.assertEqual(status, 7)
        self.assertEqual(run.call_count, 2)

    @patch.object(verify_secret_gate.subprocess, "run", side_effect=OSError("detail"))
    def test_spawn_failure_is_generic_and_fail_closed(self, run) -> None:
        with patch("builtins.print") as emit:
            status = verify_secret_gate.run_commands([["python", "first"]])

        self.assertEqual(status, 2)
        emit.assert_called_once_with(verify_secret_gate.GENERIC_FAILURE, file=sys.stderr)

    def test_malformed_range_fails_before_any_gate(self) -> None:
        with (
            patch.object(verify_secret_gate, "run_commands") as run_commands,
            patch("builtins.print") as emit,
        ):
            status = verify_secret_gate.main(["--git-range", "main...HEAD"])

        self.assertEqual(status, 2)
        run_commands.assert_not_called()
        emit.assert_called_once_with(verify_secret_gate.GENERIC_FAILURE, file=sys.stderr)

    @patch.object(verify_secret_gate.subprocess, "run")
    def test_range_head_must_match_checkout_head(self, run) -> None:
        run.return_value = subprocess.CompletedProcess(
            [], 0, stdout=("3" * 40) + "\n", stderr=""
        )

        with (
            patch.object(verify_secret_gate, "run_commands") as run_commands,
            patch("builtins.print") as emit,
        ):
            status = verify_secret_gate.main(
                ["--git-range", f"{BASE_SHA}...{HEAD_SHA}"]
            )

        self.assertEqual(status, 2)
        run_commands.assert_not_called()
        emit.assert_called_once_with(verify_secret_gate.GENERIC_FAILURE, file=sys.stderr)

    @patch.object(verify_secret_gate.subprocess, "run")
    def test_matching_exact_head_allows_gate_from_pristine_checkout(self, run) -> None:
        run.return_value = subprocess.CompletedProcess(
            [], 0, stdout=HEAD_SHA + "\n", stderr=""
        )

        with (
            patch.object(verify_secret_gate, "checkout_is_pristine", return_value=True),
            patch.object(verify_secret_gate, "run_commands", return_value=0) as run_commands,
        ):
            status = verify_secret_gate.main(
                ["--git-range", f"{BASE_SHA}...{HEAD_SHA}"]
            )

        self.assertEqual(status, 0)
        run_commands.assert_called_once_with(
            verify_secret_gate.build_commands(f"{BASE_SHA}...{HEAD_SHA}")
        )
        run.assert_called_once_with(
            ["git", "rev-parse", "--verify", "HEAD"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )

    @patch.object(verify_secret_gate.subprocess, "run")
    def test_pristine_checkout_requires_empty_porcelain_status(self, run) -> None:
        run.return_value = subprocess.CompletedProcess([], 0, stdout="", stderr="")

        self.assertTrue(verify_secret_gate.checkout_is_pristine())
        run.assert_called_once_with(
            ["git", "status", "--porcelain=v1", "--untracked-files=all"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )

    def test_tracked_staged_and_untracked_changes_are_rejected(self) -> None:
        dirty_outputs = (
            " M scripts/verify_secret_gate.py\n",
            "M  scripts/verify_secret_gate.py\n",
            "?? injected_module.py\n",
        )
        for status_output in dirty_outputs:
            with self.subTest(status_output=status_output):
                completed = subprocess.CompletedProcess(
                    [], 0, stdout=status_output, stderr=""
                )
                with patch.object(
                    verify_secret_gate, "_run_git_probe", return_value=completed
                ):
                    self.assertFalse(verify_secret_gate.checkout_is_pristine())

    def test_dirty_checkout_fails_before_any_security_gate(self) -> None:
        with (
            patch.object(verify_secret_gate, "checkout_is_pristine", return_value=False),
            patch.object(verify_secret_gate, "run_commands") as run_commands,
            patch("builtins.print") as emit,
        ):
            status = verify_secret_gate.main([])

        self.assertEqual(status, 2)
        run_commands.assert_not_called()
        emit.assert_called_once_with(verify_secret_gate.GENERIC_FAILURE, file=sys.stderr)

    def test_git_probe_error_or_stderr_fails_closed(self) -> None:
        cases = (
            None,
            subprocess.CompletedProcess([], 1, stdout="", stderr="detail"),
            subprocess.CompletedProcess([], 0, stdout="", stderr="detail"),
        )
        for completed in cases:
            with self.subTest(completed=completed):
                with patch.object(
                    verify_secret_gate, "_run_git_probe", return_value=completed
                ):
                    self.assertFalse(verify_secret_gate.checkout_is_pristine())


if __name__ == "__main__":
    unittest.main()
