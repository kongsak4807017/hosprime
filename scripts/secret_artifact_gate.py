#!/usr/bin/env python3
"""Fail closed on tracked credential artifacts outside the normal text suffix set.

The main secret scanner intentionally limits ordinary text scanning to known source and
configuration suffixes. This companion gate closes the resulting blind spot for common
credential containers, extensionless private keys, authentication dotfiles and sensitive
text formats without printing file contents or credential values.
"""

from __future__ import annotations

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

FORBIDDEN_CREDENTIAL_STORE_SUFFIXES = {
    ".jks",
    ".kdbx",
    ".keystore",
    ".p12",
    ".pfx",
}


def _load_scanner() -> Any:
    """Load the scanner and current M0 rules after path validation.

    Keeping this import lazy preserves the same validation-before-import boundary used by
    the controlled full-tree entrypoint. Installing the M0 rules here also prevents the
    sensitive-artifact gate from missing formats such as encrypted PKCS#8 private keys.
    """

    import secret_scan
    import secret_scan_m0_entry

    secret_scan_m0_entry.install_modern_rules()
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
    """Scan sensitive text formats using the same fail-closed input controls."""

    secret_scan = _load_scanner()
    findings: list[Any] = []
    for path in paths:
        if path.is_symlink():
            raise RuntimeError("tracked sensitive text artifact is a symbolic link")
        if not path.is_file():
            raise RuntimeError("tracked sensitive text artifact is not a regular file")
        try:
            size = path.stat().st_size
            if size > secret_scan.MAX_FILE_BYTES:
                raise RuntimeError("tracked sensitive text artifact exceeds scan limit")
            data = path.read_bytes()
        except OSError as exc:
            raise RuntimeError("cannot read tracked sensitive text artifact") from exc
        if b"\0" in data:
            raise RuntimeError("tracked sensitive text artifact contains NUL bytes")
        text = secret_scan.decode_utf8(data, "tracked sensitive text artifact")
        findings.extend(secret_scan.scan_text(path.as_posix(), text))
    return findings


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
    except RuntimeError:
        print(
            "SECRET ARTIFACT GATE ERROR: selected scope could not be safely scanned",
            file=sys.stderr,
        )
        return 2

    if findings:
        print(
            "SECRET ARTIFACT GATE FAILED: possible credentials detected in a sensitive "
            "text artifact (values redacted)."
        )
        for finding in findings:
            print(
                f"{finding.path}:{finding.line}: {finding.rule}: {finding.redacted}"
            )
        return 1

    print("SECRET ARTIFACT GATE PASSED: no prohibited credential artifacts found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
