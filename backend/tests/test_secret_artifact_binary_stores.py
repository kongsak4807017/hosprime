from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

SPEC = importlib.util.spec_from_file_location(
    "secret_artifact_gate_binary_stores",
    SCRIPTS_DIR / "secret_artifact_gate.py",
)
assert SPEC and SPEC.loader
secret_artifact_gate = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(secret_artifact_gate)


class SecretArtifactBinaryStoreTests(unittest.TestCase):
    def test_common_binary_credential_store_suffixes_are_forbidden(self) -> None:
        paths = [
            "private/service.p12",
            "private/service.pfx",
            "private/service.pkcs12",
            "private/service.jks",
            "private/service.keystore",
            "private/service.bks",
            "private/service.bcfks",
            "private/service.kdb",
            "private/service.kdbx",
        ]

        text_files, forbidden = secret_artifact_gate.sensitive_paths(paths)

        self.assertEqual(text_files, [])
        self.assertEqual([path.as_posix() for path in forbidden], paths)

    def test_new_binary_store_suffixes_fail_closed_without_path_disclosure(self) -> None:
        sensitive_paths = [
            "private/identifying-name.pkcs12",
            "private/identifying-name.bks",
            "private/identifying-name.bcfks",
            "private/identifying-name.kdb",
        ]
        with mock.patch.object(
            secret_artifact_gate.secret_scan_entry,
            "validate_tracked_paths",
            return_value=sensitive_paths,
        ), mock.patch("builtins.print") as output:
            result = secret_artifact_gate.main()

        self.assertEqual(result, 1)
        rendered = "\n".join(
            str(argument)
            for call in output.call_args_list
            for argument in call.args
        )
        self.assertIn("tracked binary credential store detected", rendered)
        self.assertNotIn("identifying-name", rendered)
        self.assertNotIn(".pkcs12", rendered)
        self.assertNotIn(".bks", rendered)
        self.assertNotIn(".bcfks", rendered)
        self.assertNotIn(".kdb", rendered)


if __name__ == "__main__":
    unittest.main()
