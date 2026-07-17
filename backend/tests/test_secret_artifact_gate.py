from __future__ import annotations

import importlib.util
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

SPEC = importlib.util.spec_from_file_location(
    "secret_artifact_gate", SCRIPTS_DIR / "secret_artifact_gate.py"
)
assert SPEC and SPEC.loader
secret_artifact_gate = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(secret_artifact_gate)


class SecretArtifactGateTests(unittest.TestCase):
    def test_sensitive_text_suffixes_and_basenames_are_selected(self) -> None:
        text_files, forbidden = secret_artifact_gate.sensitive_paths(
            [
                "certs/service.pem",
                "config/app.properties",
                "home/.npmrc",
                "ssh/id_ed25519",
                "profiles/credentials",
                "notes/readme.md",
            ]
        )
        self.assertEqual(
            [path.as_posix() for path in text_files],
            [
                "certs/service.pem",
                "config/app.properties",
                "home/.npmrc",
                "ssh/id_ed25519",
                "profiles/credentials",
            ],
        )
        self.assertEqual(forbidden, [])

    def test_binary_credential_stores_are_rejected_without_path_disclosure(self) -> None:
        with mock.patch.object(
            secret_artifact_gate.secret_scan_entry,
            "validate_tracked_paths",
            return_value=["private/identifying-name.p12"],
        ):
            with mock.patch("builtins.print") as output:
                result = secret_artifact_gate.main()
        self.assertEqual(result, 1)
        rendered = " ".join(
            str(argument)
            for call in output.call_args_list
            for argument in call.args
        )
        self.assertIn("tracked binary credential store detected", rendered)
        self.assertNotIn("identifying-name", rendered)
        self.assertNotIn(".p12", rendered)

    def test_pem_private_key_is_detected_with_constant_redaction(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            previous = Path.cwd()
            os.chdir(directory)
            try:
                path = Path("service.pem")
                path.write_text(
                    "-----BEGIN PRIVATE KEY-----\nsynthetic-fixture\n",
                    encoding="utf-8",
                )
                findings = secret_artifact_gate.scan_sensitive_text_files([path])
            finally:
                os.chdir(previous)
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].rule, "private-key")
        self.assertEqual(findings[0].redacted, "<redacted>")

    def test_extensionless_private_key_is_detected_with_constant_redaction(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            previous = Path.cwd()
            os.chdir(directory)
            try:
                path = Path("id_rsa")
                path.write_text(
                    "-----BEGIN PRIVATE KEY-----\nsynthetic-extensionless-fixture\n",
                    encoding="utf-8",
                )
                findings = secret_artifact_gate.scan_sensitive_text_files([path])
            finally:
                os.chdir(previous)
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0].rule, "private-key")
        self.assertEqual(findings[0].redacted, "<redacted>")

    def test_authentication_dotfile_literal_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            previous = Path.cwd()
            os.chdir(directory)
            try:
                path = Path(".npmrc")
                field = "auth" + "Token"
                path.write_text(
                    f"//registry.invalid/:_{field}=synthetic-not-a-real-value\n",
                    encoding="utf-8",
                )
                findings = secret_artifact_gate.scan_sensitive_text_files([path])
            finally:
                os.chdir(previous)
        self.assertTrue(findings)
        self.assertTrue(all(item.redacted == "<redacted>" for item in findings))

    def test_sensitive_text_nul_bytes_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            previous = Path.cwd()
            os.chdir(directory)
            try:
                path = Path("service.key")
                path.write_bytes(b"prefix\0suffix")
                with self.assertRaisesRegex(RuntimeError, "contains NUL bytes"):
                    secret_artifact_gate.scan_sensitive_text_files([path])
            finally:
                os.chdir(previous)

    def test_safe_public_pem_text_passes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            previous = Path.cwd()
            os.chdir(directory)
            try:
                path = Path("public.pem")
                path.write_text(
                    "-----BEGIN CERTIFICATE-----\nsynthetic-public-fixture\n",
                    encoding="utf-8",
                )
                findings = secret_artifact_gate.scan_sensitive_text_files([path])
            finally:
                os.chdir(previous)
        self.assertEqual(findings, [])


if __name__ == "__main__":
    unittest.main()
