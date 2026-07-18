import sys
import unittest
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

SCANNER_NAME = "hosprime_modern_pattern_scanner"
SCANNER_SPEC = spec_from_file_location(SCANNER_NAME, SCRIPTS / "secret_scan.py")
assert SCANNER_SPEC and SCANNER_SPEC.loader
scanner = module_from_spec(SCANNER_SPEC)
sys.modules[SCANNER_NAME] = scanner
SCANNER_SPEC.loader.exec_module(scanner)

# The production entry imports `secret_scan` by its normal module name. Bind the
# isolated test module to that name before loading the extension entrypoint.
sys.modules["secret_scan"] = scanner
ENTRY_NAME = "hosprime_secret_scan_m0_entry"
ENTRY_SPEC = spec_from_file_location(ENTRY_NAME, SCRIPTS / "secret_scan_m0_entry.py")
assert ENTRY_SPEC and ENTRY_SPEC.loader
entry = module_from_spec(ENTRY_SPEC)
sys.modules[ENTRY_NAME] = entry
ENTRY_SPEC.loader.exec_module(entry)


class SecretScanModernPatternTests(unittest.TestCase):
    def setUp(self) -> None:
        entry.install_modern_rules()

    def test_github_fine_grained_pat_is_detected_and_fully_redacted(self) -> None:
        value = "github" + "_pat_" + ("A" * 60)
        findings = scanner.scan_text("settings.txt", "value=" + value)
        matching = [item for item in findings if item.rule == "github-fine-grained-pat"]

        self.assertEqual(len(matching), 1)
        self.assertEqual(matching[0].redacted, "<redacted>")
        self.assertNotIn(value[:8], repr(matching[0]))
        self.assertNotIn(value[-8:], repr(matching[0]))

    def test_encrypted_pkcs8_private_key_header_is_detected(self) -> None:
        header = "-----BEGIN " + "ENCRYPTED PRIVATE KEY-----"
        findings = scanner.scan_text("identity.pem", header)

        self.assertTrue(any(item.rule == "encrypted-private-key" for item in findings))
        self.assertTrue(all(item.redacted == "<redacted>" for item in findings))

    def test_rule_installation_is_idempotent(self) -> None:
        entry.install_modern_rules()
        entry.install_modern_rules()
        names = [rule.name for rule in scanner.HIGH_CONFIDENCE_RULES]

        self.assertEqual(names.count("github-fine-grained-pat"), 1)
        self.assertEqual(names.count("encrypted-private-key"), 1)


if __name__ == "__main__":
    unittest.main()
