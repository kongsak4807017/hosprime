#!/usr/bin/env python3
"""Fail closed on tracked credential artifacts outside the normal text suffix set.

The main secret scanner intentionally limits ordinary text scanning to known source and
configuration suffixes. This companion gate closes the resulting blind spot for common
credential containers, extensionless private keys, authentication dotfiles and sensitive
text formats without printing file contents, credential values or repository paths.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any, Iterable

import secret_scan_entry


SENSITIVE_TEXT_SUFFIXES = {
    ".cfg",
    ".config",
    ".credentials",
    ".key",
    ".pem",
    ".ppk",
    ".properties",
    ".sql",
    ".xml",
}

# These files commonly hold literal credentials or private-key material but have no
# useful suffix for the ordinary source/configuration scanner to select.
SENSITIVE_TEXT_BASENAMES = {
    ".git-credentials",
    ".netrc",
    ".npmrc",
    ".pypirc",
    "credentials",
    "id_dsa",
    "id_ecdsa",
    "id_ed25519",
    "id_rsa",
}

# Binary credential stores cannot be safely inspected by the dependency-free text
# scanner. Reject them by extension instead of permitting opaque key material in Git.
FORBIDDEN_CREDENTIAL_STORE_SUFFIXES = {
    ".bcfks",
    ".bks",
    ".jks",
    ".kdb",
    ".kdbx",
    ".keystore",
    ".p12",
    ".pfx",
    ".pkcs12",
}
FINDING_RULE_RE = re.compile(r"^[a-z0-9-]+$")


def _load_scanner() -> Any:
    """Load the scanner, current M0 rules, and hardened reader after validation."""

    import secret_scan
    import secret_scan_m0_entry

    secret_scan_m0_entry.install_modern_rules()
    secret_scan_m0_entry.install_secure_reader()
    return secret_scan


def sensitive_paths(paths: Iterable[str]) -> tuple[list[Path], list[Path]]:
    """Partition tracked paths into sensitive text files and forbidden stores."""

    text_files: list[Path] = []
    forbidden_stores: list[Path] = []
    for raw_path in paths:
        path = Path(raw_path)
        suffix = path.suffix.lower()
        basename = path.name.lower()
        if suffix in FORBIDDEN_CREDENTIAL_STORE_SUFFIXES:
            forbidden_stores.append(path)
        elif suffix in SENSITIVE_TEXT_SUFFIXES or basename in SENSITIVE_TEXT_BASENAMES:
            text_files.append(path)
    return text_files, forbidden_stores


def scan_sensitive_text_files(paths: Iterable[Path]) -> list[Any]:
    """Scan sensitive text formats through the shared race-resistant reader."""

    secret_scan = _load_scanner()
    findings: list[Any] = []
    for path in paths:
        data = secret_scan.read_regular_file_safely(path)
        if b"\0" in data:
            raise RuntimeError("tracked sensitive text artifact contains NUL bytes")
        text = secret_scan.decode_utf8(data, "tracked sensitive text artifact")
        findings.extend(secret_scan.scan_text(path.as_posix(), text))
    return findings


def format_finding(finding: Any) -> str:
    """Render one finding through a closed, non-disclosing evidence contract."""

    path = finding.path
    line = finding.line
    rule = finding.rule
    redacted = finding.redacted
    if not isinstance(path, str) or not path:
        raise ValueError("finding path did not match the controlled contract")
    if type(line) is not int or line < 1:
        raise ValueError("finding line did not match the controlled contract")
    if not isinstance(rule, str) or FINDING_RULE_RE.fullmatch(rule) is None:
        raise ValueError("finding rule did not match the controlled contract")
    if redacted != "<redacted>":
        raise ValueError("finding redaction did not match the controlled contract")

    return (
        f"path-sha256={secret_scan_entry.path_fingerprint(path)}:"
        f"{line}: {rule}: <redacted>"
    )


def main() -> int:
    try:
        # Validate the complete Git path snapshot before importing scanner code. This
        # prevents malformed or presentation-control filenames from reaching either the
        # core scanner or the modern-rule extension layer.
        tracked = secret_scan_entry.validate_tracked_paths()
        text_files, forbidden_stores = sensitive_paths(tracked)
        if forbidden_stores:
            print(
                "SECRET ARTIFACT GATE FAILED: tracked binary credential store detected "
                "(path and contents withheld).",
                file=sys.stderr,
            )
            return 1
        secret_scan = _load_scanner()
        findings = secret_scan.deduplicate(scan_sensitive_text_files(text_files))
    except (AttributeError, RuntimeError, TypeError, ValueError):
        print(
            "SECRET ARTIFACT GATE ERROR: selected scope could not be safely scanned",
            file=sys.stderr,
        )
        return 2

    if findings:
        try:
            rendered_findings = [format_finding(finding) for finding in findings]
        except (AttributeError, TypeError, ValueError):
            print(
                "SECRET ARTIFACT GATE ERROR: selected scope could not be safely scanned",
                file=sys.stderr,
            )
            return 2
        print(
            "SECRET ARTIFACT GATE FAILED: possible credentials detected in a sensitive "
            "text artifact (values redacted)."
        )
        for rendered in rendered_findings:
            print(rendered)
        return 1

    print("SECRET ARTIFACT GATE PASSED: no prohibited credential artifacts found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
