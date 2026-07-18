#!/usr/bin/env python3
"""Fail-closed entrypoint for the HosPrime repository secret scanner.

Git permits filenames that are not valid UTF-8 or that contain characters capable
of altering terminal and CI-log presentation. Validate the complete tracked-path
list before importing and running the scanner so malformed paths cannot produce an
uncontrolled traceback, forge evidence output, or evade the repository security gate.
"""

from __future__ import annotations

import io
import subprocess
import sys
import unicodedata
from contextlib import redirect_stderr
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Callable, Sequence


UNSAFE_UNICODE_CATEGORIES = {"Cc", "Cf", "Zl", "Zp"}
GENERIC_SCAN_ERROR = "SECRET SCAN ERROR: selected scope could not be safely scanned"


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


def path_crosses_repository_boundary(path: str) -> bool:
    """Reject paths unsafe on either POSIX or Windows checkout semantics.

    Git stores path bytes independently of the runner operating system. A path such as
    ``..\\outside.env`` is an ordinary filename on POSIX but parent traversal on
    Windows, while drive-relative and root-relative Windows paths can resolve outside
    the checkout. Validate both path grammars so evidence produced on Linux remains a
    valid security boundary for every supported M0 platform.
    """

    posix_path = PurePosixPath(path)
    windows_path = PureWindowsPath(path)
    return bool(
        posix_path.anchor
        or windows_path.anchor
        or windows_path.drive
        or ".." in posix_path.parts
        or ".." in windows_path.parts
    )


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

        if path_crosses_repository_boundary(path):
            raise RuntimeError(
                "Git index contains a tracked path outside the repository boundary"
            )
        validated.append(path)
    return validated


def validate_tracked_paths() -> list[str]:
    return validate_tracked_path_bytes(run_git_ls_files())


def run_scanner_safely(scanner_main: Callable[[Sequence[str] | None], int]) -> int:
    """Run the scanner while withholding repository-controlled error details.

    Findings remain observable on stdout and fully redacted by ``secret_scan``. For an
    operational error (exit 2), however, the underlying scanner may include a tracked
    path or operating-system exception in stderr. The controlled entrypoint suppresses
    that untrusted detail and emits one stable, non-disclosing error message instead.
    """

    captured_stderr = io.StringIO()
    with redirect_stderr(captured_stderr):
        result = scanner_main(None)
    if result == 2:
        print(GENERIC_SCAN_ERROR, file=sys.stderr)
    elif captured_stderr.getvalue():
        # Preserve non-operational diagnostics such as argparse usage errors only when
        # the scanner did not classify the run as an unsafe-scope error.
        print(captured_stderr.getvalue(), end="", file=sys.stderr)
    return result


def main(argv: Sequence[str] | None = None) -> int:
    try:
        validated_paths = validate_tracked_paths()
    except RuntimeError:
        print(GENERIC_SCAN_ERROR, file=sys.stderr)
        return 2

    # Import only after validation, then pin the scanner to the exact validated path
    # snapshot. Without this handoff the scanner would execute a second `git ls-files`
    # call, creating a time-of-check/time-of-use gap where the index could change after
    # validation or malformed path bytes could be reintroduced.
    import secret_scan

    secret_scan.tracked_paths = lambda: [Path(path) for path in validated_paths]

    # The scanner's direct main function currently uses a truthiness fallback for argv,
    # so passing [] would make it consume unrelated host-process arguments. Isolate the
    # process argv explicitly and call main(None), which preserves both an intentional
    # empty list (default full-tree scan) and any explicitly supplied scanner options.
    effective_argv = list(sys.argv[1:] if argv is None else argv)
    original_argv = sys.argv
    try:
        sys.argv = [original_argv[0], *effective_argv]
        return run_scanner_safely(secret_scan.main)
    finally:
        sys.argv = original_argv


if __name__ == "__main__":
    raise SystemExit(main())
