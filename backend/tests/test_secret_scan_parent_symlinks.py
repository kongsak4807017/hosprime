import os
import shutil
import sys
import tempfile
import unittest
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))


def load_module(name: str, filename: str):
    spec = spec_from_file_location(name, SCRIPTS / filename)
    assert spec and spec.loader
    module = module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


scanner = load_module("hosprime_parent_symlink_scanner", "secret_scan.py")
secure_io = load_module("hosprime_parent_symlink_secure_io", "secret_scan_secure_io.py")
secure_io.install_component_pinned_reader(scanner)


@unittest.skipUnless(
    secure_io._supports_component_pinning(),
    "component-pinned openat semantics are unavailable on this platform",
)
class SecretScanParentSymlinkTests(unittest.TestCase):
    def create_symlink(self, target: Path, link: Path) -> None:
        try:
            os.symlink(target, link, target_is_directory=True)
        except (OSError, NotImplementedError) as exc:
            self.skipTest(f"directory symbolic links are unavailable: {exc}")

    def create_hard_link(self, target: Path, link: Path) -> None:
        try:
            os.link(target, link)
        except (OSError, NotImplementedError) as exc:
            self.skipTest(f"hard links are unavailable: {exc}")

    def test_parent_replaced_before_component_open_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            checkout = root / "checkout"
            managed = checkout / "managed"
            external = root / "external"
            managed.mkdir(parents=True)
            external.mkdir()
            tracked = managed / "settings.env"
            tracked.write_text("SAFE=value", encoding="utf-8")
            (external / "settings.env").write_text(
                "ADMIN_PASSWORD=synthetic-parent-swap", encoding="utf-8"
            )

            real_open = os.open
            swapped = False

            def swap_parent_then_open(path, flags, *args, **kwargs):
                nonlocal swapped
                if path == "managed" and kwargs.get("dir_fd") is not None and not swapped:
                    swapped = True
                    shutil.rmtree(managed)
                    self.create_symlink(external, managed)
                return real_open(path, flags, *args, **kwargs)

            with patch.object(os, "open", swap_parent_then_open):
                with self.assertRaisesRegex(RuntimeError, "safely read"):
                    scanner.read_regular_file_safely(tracked)

    def test_open_parent_descriptor_is_not_redirected_by_later_swap(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            checkout = root / "checkout"
            managed = checkout / "managed"
            displaced = checkout / "managed-original"
            external = root / "external"
            managed.mkdir(parents=True)
            external.mkdir()
            tracked = managed / "settings.env"
            tracked.write_text("SAFE=value", encoding="utf-8")
            (external / "settings.env").write_text(
                "ADMIN_PASSWORD=synthetic-external-value", encoding="utf-8"
            )

            real_open = os.open
            swapped = False

            def swap_after_parent_open(path, flags, *args, **kwargs):
                nonlocal swapped
                if path == "settings.env" and kwargs.get("dir_fd") is not None and not swapped:
                    swapped = True
                    managed.rename(displaced)
                    self.create_symlink(external, managed)
                return real_open(path, flags, *args, **kwargs)

            with patch.object(os, "open", swap_after_parent_open):
                data = scanner.read_regular_file_safely(tracked)

            self.assertEqual(data, b"SAFE=value")
            self.assertNotIn(b"synthetic-external-value", data)

    def test_hard_link_to_external_inode_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            checkout = root / "checkout" / "managed"
            checkout.mkdir(parents=True)
            external = root / "external.env"
            external.write_text(
                "ADMIN_PASSWORD=synthetic-external-hard-link", encoding="utf-8"
            )
            tracked = checkout / "settings.env"
            self.create_hard_link(external, tracked)

            self.assertGreater(os.stat(tracked).st_nlink, 1)
            with self.assertRaisesRegex(RuntimeError, "safely read"):
                scanner.read_regular_file_safely(tracked)

    def test_link_count_change_during_read_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            tracked = Path(directory) / "checkout" / "managed" / "settings.env"
            tracked.parent.mkdir(parents=True)
            tracked.write_text("SAFE=value", encoding="utf-8")
            alias = Path(directory) / "late-alias.env"

            real_read = os.read
            linked = False

            def add_hard_link_after_first_read(descriptor, size):
                nonlocal linked
                chunk = real_read(descriptor, size)
                if chunk and not linked:
                    linked = True
                    self.create_hard_link(tracked, alias)
                return chunk

            with patch.object(os, "read", add_hard_link_after_first_read):
                with self.assertRaisesRegex(RuntimeError, "safely read"):
                    scanner.read_regular_file_safely(tracked)

    def test_in_place_rewrite_during_read_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            tracked = Path(directory) / "checkout" / "managed" / "settings.env"
            tracked.parent.mkdir(parents=True)
            tracked.write_text("SAFE=value", encoding="utf-8")

            real_read = os.read
            rewritten = False

            def rewrite_after_first_read(descriptor, size):
                nonlocal rewritten
                chunk = real_read(descriptor, size)
                if chunk and not rewritten:
                    rewritten = True
                    tracked.write_text("RISK=value", encoding="utf-8")
                return chunk

            with patch.object(os, "read", rewrite_after_first_read):
                with self.assertRaisesRegex(RuntimeError, "safely read"):
                    scanner.read_regular_file_safely(tracked)

    def test_invalid_read_limits_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            tracked = Path(directory) / "checkout" / "managed" / "settings.env"
            tracked.parent.mkdir(parents=True)
            tracked.write_text("SAFE=value", encoding="utf-8")

            descriptor, opened = secure_io._open_component_pinned(tracked)
            with self.assertRaisesRegex(RuntimeError, "safely read"):
                secure_io._read_from_descriptor(descriptor, opened, -1, 1)

    def test_nested_regular_file_remains_scannable(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            tracked = Path(directory) / "checkout" / "managed" / "settings.env"
            tracked.parent.mkdir(parents=True)
            tracked.write_text(
                "ADMIN_PASSWORD=synthetic-not-a-real-secret", encoding="utf-8"
            )

            findings = scanner.scan_tracked_files([tracked])

            self.assertTrue(
                any(item.rule == "credential-assignment" for item in findings)
            )
            self.assertTrue(all(item.redacted == "<redacted>" for item in findings))


if __name__ == "__main__":
    unittest.main()
