#!/usr/bin/env python3
"""Controlled M0 secret-scan entrypoint with current high-confidence patterns.

The core scanner remains dependency-free and owns traversal, redaction, Git-path
validation and diff safety. This entrypoint installs additional high-confidence
patterns for credential formats that are common in current developer workflows,
then delegates to the existing controlled entrypoint.
"""

from __future__ import annotations

import re
from typing import Sequence

import secret_scan
import secret_scan_entry


MODERN_HIGH_CONFIDENCE_RULES: tuple[secret_scan.Rule, ...] = (
    secret_scan.Rule(
        "github-fine-grained-pat",
        re.compile(r"\bgithub_pat_[A-Za-z0-9_]{50,}\b"),
    ),
    secret_scan.Rule(
        "encrypted-private-key",
        re.compile(r"-----BEGIN ENCRYPTED PRIVATE KEY-----"),
    ),
)


def install_modern_rules() -> None:
    """Install each rule once so repeated programmatic calls stay deterministic."""

    existing_names = {rule.name for rule in secret_scan.HIGH_CONFIDENCE_RULES}
    additions = tuple(
        rule for rule in MODERN_HIGH_CONFIDENCE_RULES if rule.name not in existing_names
    )
    secret_scan.HIGH_CONFIDENCE_RULES += additions


def main(argv: Sequence[str] | None = None) -> int:
    install_modern_rules()
    return secret_scan_entry.main(argv)


if __name__ == "__main__":
    raise SystemExit(main())
