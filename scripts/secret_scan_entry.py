#!/usr/bin/env python3
"""Fail-closed entrypoint for the HosPrime repository secret scanner.

Git permits filenames that are not valid UTF-8 or that contain terminal control
characters. Validate the complete tracked-path list before importing and running
the scanner so malformed paths cannot produce an uncontrolled traceback, forge CI
output, or evade the repository security gate.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Sequence


def run_git_ls_files() -> bytes:
    completed = subprocess.run(
        ["git", "ls-files", "-z"],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if completed.returncode != 0:
        message = completed.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"git ls-files -z failed: {message}")
    return completed.stdout


def validate_tracked_path_bytes(raw: bytes) -> list[str]:
    """Return safe repository-relative paths or fail closed.

    Error messages intentionally contain no undecodable filename bytes or control
    characters from the Git index.
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

        if any(ord(character) < 32 or ord(character) == 127 for character in path):
            raise RuntimeError(
                "Git index contains a tracked path with control characters"
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
