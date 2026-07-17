import sys
import types
import unittest
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
MODULE_NAME = "hosprime_secret_scan_entry_argv"
SPEC = spec_from_file_location(MODULE_NAME, ROOT / "scripts" / "secret_scan_entry.py")
assert SPEC and SPEC.loader
entry_module = module_from_spec(SPEC)
SPEC.loader.exec_module(entry_module)


class SecretScanEntryArgvTests(unittest.TestCase):
    def run_entry(self, supplied_argv, host_argv):
        observed = {}

        def fake_main(argv):
            observed["main_argv"] = argv
            observed["process_argv"] = list(sys.argv)
            observed["paths"] = [path.as_posix() for path in fake_scanner.tracked_paths()]
            return 0

        fake_scanner = types.SimpleNamespace(main=fake_main, tracked_paths=lambda: [])
        original_argv = sys.argv
        with patch.object(entry_module, "validate_tracked_paths", return_value=["README.md", "vault/บุคคล.md"]):
            with patch.dict(sys.modules, {"secret_scan": fake_scanner}):
                try:
                    sys.argv = list(host_argv)
                    result = entry_module.main(supplied_argv)
                finally:
                    restored = list(sys.argv)
                    sys.argv = original_argv

        return result, observed, restored

    def test_explicit_empty_arguments_do_not_inherit_host_arguments(self) -> None:
        result, observed, restored = self.run_entry([], ["unittest", "--failfast"])

        self.assertEqual(result, 0)
        self.assertIsNone(observed["main_argv"])
        self.assertEqual(observed["process_argv"], ["unittest"])
        self.assertEqual(observed["paths"], ["README.md", "vault/บุคคล.md"])
        self.assertEqual(restored, ["unittest", "--failfast"])

    def test_explicit_scanner_arguments_are_forwarded_exactly(self) -> None:
        supplied = ["--git-range", "origin/main...HEAD", "--diff-only"]
        result, observed, restored = self.run_entry(supplied, ["pytest", "-q"])

        self.assertEqual(result, 0)
        self.assertIsNone(observed["main_argv"])
        self.assertEqual(observed["process_argv"], ["pytest", *supplied])
        self.assertEqual(restored, ["pytest", "-q"])


if __name__ == "__main__":
    unittest.main()
