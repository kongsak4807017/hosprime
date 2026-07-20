import os
import sys
import tempfile
import unittest
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
MODULE_NAME = "hosprime_secret_scan_symlinks"
SPEC = spec_from_file_location(MODULE_NAME, ROOT / "scripts" / "secret_scan.py")
assert SPEC and SPEC.loader
scanner_module = module_from_spec(SPEC)
sys.modules[MODULE_NAME] = scanner_module
SPEC.loader.exec_module(scanner_module)


class SecretScanSymlinkTests(unittest.TestCase):
    def create_symlink(self, target: Path, link: Path) -> None:
        try:
            os.symlink(target, link)
        except (OSError, NotImplementedError) as exc:
            self.skipTest(f"symbolic links are unavailable in this environment: {exc}")

    def test_candidate_symlink_to_external_file_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            external = root / "external.env"
            external.write_text("ADMIN_PASSWORD=synthetic-not-a-real-secret", encoding="utf-8")
            checkout = root / "checkout"
            checkout.mkdir()
            tracked_link = checkout / "settings.env"
            self.create_symlink(external, tracked_link)

            with self.assertRaisesRegex(RuntimeError, "safely read"):
                scanner_module.scan_tracked_files([tracked_link])

    def test_dangling_candidate_symlink_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            tracked_link = root / "settings.env"
            self.create_symlink(root / "missing.env", tracked_link)

            with self.assertRaisesRegex(RuntimeError, "safely read"):
                scanner_module.scan_tracked_files([tracked_link])

    def test_regular_file_swapped_to_symlink_during_open_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            tracked = root / "settings.env"
            external = root / "external.env"
            tracked.write_text("SAFE=value", encoding="utf-8")
            external.write_text(
                "ADMIN_PASSWORD=synthetic-race-secret", encoding="utf-8"
            )

            real_open = os.open
            swapped = False

            def swap_then_open(path, flags, *args, **kwargs):
                nonlocal swapped
                if Path(path) == tracked and not swapped:
                    swapped = True
                    tracked.unlink()
                    self.create_symlink(external, tracked)
                return real_open(path, flags, *args, **kwargs)

            with patch.object(os, "open", swap_then_open):
                with self.assertRaisesRegex(RuntimeError, "safely read"):
                    scanner_module.scan_tracked_files([tracked])

    def test_regular_candidate_file_is_still_scanned(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "settings.env"
            path.write_text("ADMIN_PASSWORD=synthetic-not-a-real-secret", encoding="utf-8")

            findings = scanner_module.scan_tracked_files([path])

            self.assertTrue(
                any(item.rule == "credential-assignment" for item in findings)
            )
            self.assertTrue(all(item.redacted == "<redacted>" for item in findings))


if __name__ == "__main__":
    unittest.main()
