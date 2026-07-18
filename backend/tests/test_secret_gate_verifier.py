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


if __name__ == "__main__":
    unittest.main()
