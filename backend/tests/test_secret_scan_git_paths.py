import contextlib
import io
import sys
import unittest
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
MODULE_NAME = "hosprime_secret_scan_entry"
SPEC = spec_from_file_location(MODULE_NAME, ROOT / "scripts" / "secret_scan_entry.py")
assert SPEC and SPEC.loader
entry_module = module_from_spec(SPEC)
sys.modules[MODULE_NAME] = entry_module
SPEC.loader.exec_module(entry_module)


class SecretScanGitPathTests(unittest.TestCase):
    def test_invalid_utf8_tracked_path_fails_closed_without_echoing_bytes(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "not valid UTF-8") as context:
            entry_module.validate_tracked_path_bytes(b"safe.env\0bad-\xff.env\0")

        self.assertNotIn("bad", str(context.exception))
        self.assertNotIn("\\xff", str(context.exception))

    def test_control_character_tracked_path_fails_closed_without_echoing_path(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "unsafe control or format") as context:
            entry_module.validate_tracked_path_bytes(
                b"safe.env\0forged\nSECRET SCAN PASSED.env\0"
            )

        self.assertNotIn("forged", str(context.exception))
        self.assertNotIn("SECRET SCAN PASSED", str(context.exception))

    def test_unicode_bidi_override_path_fails_closed_without_echoing_path(self) -> None:
        unsafe_path = "safe/visible\u202egnp.exe.env"
        with self.assertRaisesRegex(RuntimeError, "unsafe control or format") as context:
            entry_module.validate_tracked_path_bytes(
                f"safe.env\0{unsafe_path}\0".encode("utf-8")
            )

        self.assertNotIn("visible", str(context.exception))
        self.assertNotIn("exe", str(context.exception))

    def test_unicode_line_separator_path_fails_closed(self) -> None:
        unsafe_path = "forged\u2028SECRET SCAN PASSED.env"
        with self.assertRaisesRegex(RuntimeError, "unsafe control or format") as context:
            entry_module.validate_tracked_path_bytes(unsafe_path.encode("utf-8") + b"\0")

        self.assertNotIn("SECRET SCAN PASSED", str(context.exception))

    def test_parent_traversal_path_fails_closed(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "outside the repository boundary"):
            entry_module.validate_tracked_path_bytes(b"../outside.env\0")

    def test_valid_utf8_repository_paths_are_returned(self) -> None:
        self.assertEqual(
            entry_module.validate_tracked_path_bytes(
                "settings.env\0docs/คู่มือ.md\0".encode("utf-8")
            ),
            ["settings.env", "docs/คู่มือ.md"],
        )

    def test_git_failure_does_not_echo_untrusted_stderr(self) -> None:
        forged_stderr = b"fatal: forged\nSECRET SCAN PASSED\n"
        completed = SimpleNamespace(returncode=128, stdout=b"", stderr=forged_stderr)
        with patch.object(entry_module.subprocess, "run", return_value=completed):
            with self.assertRaisesRegex(RuntimeError, "exit status 128") as context:
                entry_module.run_git_ls_files()

        message = str(context.exception)
        self.assertNotIn("forged", message)
        self.assertNotIn("SECRET SCAN PASSED", message)

    def test_main_returns_controlled_error_before_importing_scanner(self) -> None:
        stderr = io.StringIO()
        with patch.object(
            entry_module,
            "validate_tracked_paths",
            side_effect=RuntimeError(
                "Git index contains a tracked path with unsafe control or format characters"
            ),
        ):
            with contextlib.redirect_stderr(stderr):
                exit_code = entry_module.main([])

        self.assertEqual(exit_code, 2)
        self.assertIn("SECRET SCAN ERROR", stderr.getvalue())
        self.assertNotIn("Traceback", stderr.getvalue())

    def test_main_pins_scanner_to_exact_validated_path_snapshot(self) -> None:
        observed: dict[str, object] = {}

        def scanner_main(argv: list[str]) -> int:
            observed["argv"] = argv
            observed["paths"] = fake_scanner.tracked_paths()
            return 0

        fake_scanner = SimpleNamespace(main=scanner_main)
        validated = ["settings.env", "docs/คู่มือ.md"]
        with patch.object(entry_module, "validate_tracked_paths", return_value=validated):
            with patch.dict(sys.modules, {"secret_scan": fake_scanner}):
                exit_code = entry_module.main(["--git-range", "base...head"])

        self.assertEqual(exit_code, 0)
        self.assertEqual(observed["argv"], ["--git-range", "base...head"])
        self.assertEqual(
            observed["paths"],
            [Path("settings.env"), Path("docs/คู่มือ.md")],
        )

    def test_explicit_empty_arguments_do_not_inherit_host_process_arguments(self) -> None:
        observed: dict[str, object] = {}

        def scanner_main(argv: list[str]) -> int:
            observed["argv"] = argv
            return 0

        fake_scanner = SimpleNamespace(main=scanner_main)
        with patch.object(entry_module, "validate_tracked_paths", return_value=["safe.env"]):
            with patch.dict(sys.modules, {"secret_scan": fake_scanner}):
                with patch.object(sys, "argv", ["unittest", "--unexpected-host-flag"]):
                    exit_code = entry_module.main([])

        self.assertEqual(exit_code, 0)
        self.assertEqual(observed["argv"], [])


if __name__ == "__main__":
    unittest.main()
