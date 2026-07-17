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
        validated_paths = validate_tracked_paths()
    except RuntimeError as exc:
        print(f"SECRET SCAN ERROR: {exc}", file=sys.stderr)
        return 2

    # Import only after validation, then pin the scanner to the exact validated path
    # snapshot. Without this handoff the scanner would execute a second `git ls-files`
    # call, creating a time-of-check/time-of-use gap where the index could change after
    # validation or malformed path bytes could be reintroduced.
    import secret_scan

    secret_scan.tracked_paths = lambda: [Path(path) for path in validated_paths]

    # An explicitly supplied empty argument sequence means "run the default full-tree
    # scan". Using truthiness here would accidentally substitute unrelated host-process
    # arguments (for example unittest or an embedding tool), changing scanner scope or
    # causing an argument-parse failure. Only None delegates to the process command line.
    effective_argv = list(sys.argv[1:] if argv is None else argv)
    return secret_scan.main(effective_argv)


if __name__ == "__main__":
    raise SystemExit(main())
