import os
import sys
import tempfile
import unittest
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

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

            with self.assertRaisesRegex(RuntimeError, "symbolic link"):
                scanner_module.scan_tracked_files([tracked_link])

    def test_dangling_candidate_symlink_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            tracked_link = root / "settings.env"
            self.create_symlink(root / "missing.env", tracked_link)

            with self.assertRaisesRegex(RuntimeError, "symbolic link"):
                scanner_module.scan_tracked_files([tracked_link])

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
