#!/usr/bin/env python3
"""Fail-closed entrypoint for the HosPrime repository secret scanner.

Git permits filenames that are not valid UTF-8 or that contain characters capable
of altering terminal and CI-log presentation. Validate the complete tracked-path
list before importing and running the scanner so malformed paths cannot produce an
uncontrolled traceback, forge evidence output, or evade the repository security gate.
"""

from __future__ import annotations

import subprocess
import sys
import unicodedata
from pathlib import Path
from typing import Sequence


UNSAFE_UNICODE_CATEGORIES = {"Cc", "Cf", "Zl", "Zp"}


def run_git_ls_files() -> bytes:
    completed = subprocess.run(
        ["git", "ls-files", "-z"],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if completed.returncode != 0:
        # Do not echo Git stderr. A repository-controlled path may be present in the
        # message and could contain control or formatting characters.
        raise RuntimeError(
            f"git ls-files -z failed with exit status {completed.returncode}"
        )
    return completed.stdout


def validate_tracked_path_bytes(raw: bytes) -> list[str]:
    """Return safe repository-relative paths or fail closed.

    Error messages intentionally contain no undecodable filename bytes, filename text,
    control characters, bidi overrides, zero-width format controls, or Unicode line /
    paragraph separators from the Git index.
    """

    validated: list[str] = []
    for item in raw.split(b"\0"):
        if not item:
            continue
        try:
            path = item.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise RuntimeError(
                "Git index contains a tracked path that is not valid UTF-8"
            ) from exc

        if any(
            unicodedata.category(character) in UNSAFE_UNICODE_CATEGORIES
            for character in path
        ):
            raise RuntimeError(
                "Git index contains a tracked path with unsafe control or format characters"
            )

        candidate = Path(path)
        if candidate.is_absolute() or ".." in candidate.parts:
            raise RuntimeError(
                "Git index contains a tracked path outside the repository boundary"
            )
        validated.append(path)
    return validated


def validate_tracked_paths() -> list[str]:
    return validate_tracked_path_bytes(run_git_ls_files())


def main(argv: Sequence[str] | None = None) -> int:
    try:
        validate_tracked_paths()
    except RuntimeError as exc:
        print(f"SECRET SCAN ERROR: {exc}", file=sys.stderr)
        return 2

    # Import after path validation so secret_scan.tracked_paths() cannot encounter
    # malformed path bytes during the controlled workflow invocation.
    import secret_scan

    return secret_scan.main(argv or sys.argv[1:])


if __name__ == "__main__":
    raise SystemExit(main())
