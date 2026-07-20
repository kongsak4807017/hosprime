import sys
import unittest
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

SCANNER_NAME = "hosprime_putty_key_scanner"
SCANNER_SPEC = spec_from_file_location(SCANNER_NAME, SCRIPTS / "secret_scan.py")
assert SCANNER_SPEC and SCANNER_SPEC.loader
scanner = module_from_spec(SCANNER_SPEC)
sys.modules[SCANNER_NAME] = scanner
SCANNER_SPEC.loader.exec_module(scanner)

# Production modules import the scanner by its normal name only after path validation.
sys.modules["secret_scan"] = scanner
ENTRY_NAME = "hosprime_putty_key_entry"
ENTRY_SPEC = spec_from_file_location(ENTRY_NAME, SCRIPTS / "secret_scan_m0_entry.py")
assert ENTRY_SPEC and ENTRY_SPEC.loader
entry = module_from_spec(ENTRY_SPEC)
sys.modules[ENTRY_NAME] = entry
ENTRY_SPEC.loader.exec_module(entry)

ARTIFACT_NAME = "hosprime_putty_artifact_gate"
ARTIFACT_SPEC = spec_from_file_location(
    ARTIFACT_NAME, SCRIPTS / "secret_artifact_gate.py"
)
assert ARTIFACT_SPEC and ARTIFACT_SPEC.loader
artifact_gate = module_from_spec(ARTIFACT_SPEC)
sys.modules[ARTIFACT_NAME] = artifact_gate
ARTIFACT_SPEC.loader.exec_module(artifact_gate)


class PuttyPrivateKeyArtifactTests(unittest.TestCase):
    def setUp(self) -> None:
        entry.install_modern_rules()

    def test_ppk_suffix_is_selected_as_sensitive_text(self) -> None:
        text_files, forbidden_stores = artifact_gate.sensitive_paths(
            ["keys/operator.PPK", "docs/readme.md"]
        )

        self.assertEqual([path.as_posix() for path in text_files], ["keys/operator.PPK"])
        self.assertEqual(forbidden_stores, [])

    def test_putty_v2_and_v3_private_key_headers_are_detected(self) -> None:
        fixtures = (
            "PuTTY-User-Key-File-2: ssh-rsa",
            "PuTTY-User-Key-File-3: ssh-ed25519",
        )

        for header in fixtures:
            with self.subTest(header=header.split(":", 1)[0]):
                findings = scanner.scan_text("keys/operator.ppk", header)
                matching = [item for item in findings if item.rule == "putty-private-key"]
                self.assertEqual(len(matching), 1)
                self.assertEqual(matching[0].redacted, "<redacted>")
                self.assertNotIn("ssh-rsa", repr(matching[0]))
                self.assertNotIn("ssh-ed25519", repr(matching[0]))

    def test_public_key_comment_does_not_match_putty_private_key_rule(self) -> None:
        findings = scanner.scan_text(
            "keys/operator.pub",
            "Comment: PuTTY-User-Key-File-3 documentation only",
        )

        self.assertFalse(any(item.rule == "putty-private-key" for item in findings))

    def test_putty_rule_installation_is_idempotent(self) -> None:
        entry.install_modern_rules()
        entry.install_modern_rules()
        names = [rule.name for rule in scanner.HIGH_CONFIDENCE_RULES]

        self.assertEqual(names.count("putty-private-key"), 1)


if __name__ == "__main__":
    unittest.main()
