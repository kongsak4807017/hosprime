#!/usr/bin/env python3
"""Controlled M0 secret-scan entrypoint with current high-confidence patterns.

Validate the complete tracked Git path snapshot before importing the scanner. This
preserves the fail-closed path boundary while extending the core dependency-free
scanner with current credential formats used in developer workflows.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Sequence

import secret_scan_entry


MODERN_HIGH_CONFIDENCE_RULE_SPECS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "github-fine-grained-pat",
        re.compile(r"\bgithub_pat_[A-Za-z0-9_]{50,}\b"),
    ),
    (
        "gitlab-token",
        re.compile(
            r"\b(?:glpat|gloas|gldt|glrt|glrtr|glcbt|glptt|glft|glimt|glagent|glwt|glsoat|glffct)-[A-Za-z0-9_-]{20,}\b"
        ),
    ),
    (
        "stripe-live-secret-key",
        re.compile(r"\bsk_live_[A-Za-z0-9]{24,}\b"),
    ),
    (
        "encrypted-private-key",
        re.compile(r"-----BEGIN ENCRYPTED PRIVATE KEY-----"),
    ),
)


def install_modern_rules() -> None:
    """Install each modern rule once after the path-validation boundary."""

    import secret_scan

    existing_names = {rule.name for rule in secret_scan.HIGH_CONFIDENCE_RULES}
    additions = tuple(
        secret_scan.Rule(name, pattern)
        for name, pattern in MODERN_HIGH_CONFIDENCE_RULE_SPECS
        if name not in existing_names
    )
    secret_scan.HIGH_CONFIDENCE_RULES += additions


def install_secure_reader() -> None:
    """Install parent-component-pinned reads after tracked-path validation."""

    import secret_scan
    import secret_scan_secure_io

    secret_scan_secure_io.install_component_pinned_reader(secret_scan)


def main(argv: Sequence[str] | None = None) -> int:
    try:
        validated_paths = secret_scan_entry.validate_tracked_paths()
    except RuntimeError:
        print(secret_scan_entry.GENERIC_SCAN_ERROR, file=sys.stderr)
        return 2

    # Import and extend the scanner only after the complete Git path snapshot has
    # passed strict UTF-8, control-character and repository-boundary validation.
    import secret_scan

    install_modern_rules()
    install_secure_reader()
    secret_scan.tracked_paths = lambda: [Path(path) for path in validated_paths]

    effective_argv = list(sys.argv[1:] if argv is None else argv)
    original_argv = sys.argv
    try:
        sys.argv = [original_argv[0], *effective_argv]
        return secret_scan_entry.run_scanner_safely(secret_scan.main)
    finally:
        sys.argv = original_argv


if __name__ == "__main__":
    raise SystemExit(main())
