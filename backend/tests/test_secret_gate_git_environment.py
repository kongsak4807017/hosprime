import os
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


class SecretGateGitEnvironmentTests(unittest.TestCase):
    def test_no_git_environment_returns_inherit_marker(self) -> None:
        source = {"PATH": "/usr/bin", "HOME": "/tmp/home"}

        self.assertIsNone(verify_secret_gate.sanitized_git_environment(source))

    def test_every_git_prefixed_variable_is_removed(self) -> None:
        source = {
            "PATH": "/usr/bin",
            "HOME": "/tmp/home",
            "GIT_DIR": "/tmp/alternate/.git",
            "GIT_WORK_TREE": "/tmp/alternate",
            "GIT_INDEX_FILE": "/tmp/alternate-index",
            "GIT_OBJECT_DIRECTORY": "/tmp/objects",
            "GIT_ALTERNATE_OBJECT_DIRECTORIES": "/tmp/alternate-objects",
            "GIT_CONFIG_COUNT": "1",
            "GIT_CONFIG_KEY_0": "core.fsmonitor",
            "GIT_CONFIG_VALUE_0": "malicious-helper",
            "git_lowercase_probe": "remove-case-insensitively",
        }

        sanitized = verify_secret_gate.sanitized_git_environment(source)

        self.assertIsNotNone(sanitized)
        assert sanitized is not None
        self.assertEqual(sanitized, {"PATH": "/usr/bin", "HOME": "/tmp/home"})
        self.assertFalse(any(key.upper().startswith("GIT_") for key in sanitized))

    @patch.object(verify_secret_gate.subprocess, "run")
    def test_git_probe_uses_sanitized_environment_when_redirectors_exist(self, run) -> None:
        run.return_value = subprocess.CompletedProcess([], 0, stdout="", stderr="")
        inherited = {
            "PATH": os.environ.get("PATH", ""),
            "GIT_DIR": "/tmp/alternate/.git",
            "GIT_WORK_TREE": "/tmp/alternate",
            "GIT_CONFIG_COUNT": "1",
            "GIT_CONFIG_KEY_0": "core.fsmonitor",
            "GIT_CONFIG_VALUE_0": "malicious-helper",
        }

        with patch.object(verify_secret_gate.os, "environ", inherited):
            result = verify_secret_gate._run_git_probe(["status", "--porcelain=v1"])

        self.assertEqual(result.returncode, 0)
        call = run.call_args
        self.assertEqual(call.args[0], ["git", "status", "--porcelain=v1"])
        self.assertEqual(call.kwargs["cwd"], ROOT)
        self.assertEqual(call.kwargs["env"], {"PATH": inherited["PATH"]})
        self.assertFalse(
            any(key.upper().startswith("GIT_") for key in call.kwargs["env"])
        )

    @patch.object(verify_secret_gate.subprocess, "run")
    def test_git_probe_keeps_existing_call_contract_without_redirectors(self, run) -> None:
        run.return_value = subprocess.CompletedProcess([], 0, stdout="", stderr="")

        with patch.object(verify_secret_gate.os, "environ", {"PATH": "/usr/bin"}):
            verify_secret_gate._run_git_probe(["status", "--porcelain=v1"])

        self.assertNotIn("env", run.call_args.kwargs)


if __name__ == "__main__":
    unittest.main()
