#!/usr/bin/env python3
"""Fail-closed entrypoint for the HosPrime repository secret scanner.

Git permits filenames that are not valid UTF-8 or that contain characters capable
of altering terminal and CI-log presentation. Validate the complete tracked-path
list before importing and running the scanner so malformed paths cannot produce an
uncontrolled traceback, forge evidence output, or evade the repository security gate.
"""

from __future__ import annotations

import hashlib
import io
import re
import subprocess
import sys
import unicodedata
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Callable, Sequence


UNSAFE_UNICODE_CATEGORIES = {"Cc", "Cf", "Zl", "Zp"}
GENERIC_SCAN_ERROR = "SECRET SCAN ERROR: selected scope could not be safely scanned"
SCAN_PASSED_MESSAGE = "SECRET SCAN PASSED: no likely credentials found in the selected scope."
SCAN_FAILED_HEADER = "SECRET SCAN FAILED: possible credentials detected (values redacted)."
SCAN_FAILED_FOOTER = (
    "Remove the value from Git and rotate/revoke it through the accountable owner."
)
FINDING_LINE_RE = re.compile(
    r"^(?P<path>.+):(?P<line>[0-9]+): (?P<rule>[a-z0-9-]+): <redacted>$"
)
WINDOWS_RESERVED_DEVICE_NAMES = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    "CONIN$",
    "CONOUT$",
    *(f"COM{number}" for number in range(1, 10)),
    *(f"LPT{number}" for number in range(1, 10)),
}
WINDOWS_FORBIDDEN_FILENAME_CHARACTERS = frozenset('<>:"|?*')


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


def windows_path_is_checkout_unsafe(path: str) -> bool:
    """Reject Git paths that cannot round-trip safely through Windows checkout.

    Linux permits names that Windows interprets as device files, alternate data
    streams, wildcard syntax, or lossy trailing-dot / trailing-space names. Reject
    those names before importing scanner code so Linux CI evidence remains valid for
    every supported M0 checkout platform.
    """

    windows_path = PureWindowsPath(path)
    for part in windows_path.parts:
        if part in {windows_path.anchor, ".", ".."}:
            continue
        if part.rstrip(" .") != part:
            return True
        if any(
            character in WINDOWS_FORBIDDEN_FILENAME_CHARACTERS
            for character in part
        ):
            return True
        device_candidate = part.split(".", 1)[0].upper()
        if device_candidate in WINDOWS_RESERVED_DEVICE_NAMES:
            return True
    return False


def path_crosses_repository_boundary(path: str) -> bool:
    """Reject paths unsafe on either POSIX or Windows checkout semantics.

    Git stores path bytes independently of the runner operating system. A path such as
    ``..\outside.env`` is an ordinary filename on POSIX but parent traversal on
    Windows, while drive-relative and root-relative Windows paths can resolve outside
    the checkout. Validate both path grammars and Windows filename rules so evidence
    produced on Linux remains a valid security boundary for every supported M0 platform.
    """

    posix_path = PurePosixPath(path)
    windows_path = PureWindowsPath(path)
    return bool(
        posix_path.anchor
        or windows_path.anchor
        or windows_path.drive
        or ".." in posix_path.parts
        or ".." in windows_path.parts
        or windows_path_is_checkout_unsafe(path)
    )


def checkout_path_identity(path: str) -> str:
    """Return a conservative identity shared by supported local checkouts.

    Windows commonly treats path components case-insensitively and accepts both slash
    directions as separators. Default macOS filesystems also compare common Unicode
    normalization variants as the same name. A Linux runner can otherwise scan two
    distinct Git paths even though another supported platform checks out only one of
    them or aliases both names. Normalize each Windows-interpreted component to NFC and
    case-fold it so such collisions fail before scanner import.
    """

    return "/".join(
        unicodedata.normalize("NFC", part).casefold()
        for part in PureWindowsPath(path).parts
    )


def validate_tracked_path_bytes(raw: bytes) -> list[str]:
    """Return safe repository-relative paths or fail closed.

    Error messages intentionally contain no undecodable filename bytes, filename text,
    control characters, bidi overrides, zero-width format controls, or Unicode line /
    paragraph separators from the Git index.
    """

    validated: list[str] = []
    checkout_identities: set[str] = set()
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

        checkout_identity = checkout_path_identity(path)
        if checkout_identity in checkout_identities:
            raise RuntimeError(
                "Git index contains tracked paths with colliding checkout identities"
            )
        checkout_identities.add(checkout_identity)
        validated.append(path)
    return validated


def validate_tracked_paths() -> list[str]:
    return validate_tracked_path_bytes(run_git_ls_files())


def path_fingerprint(path: str) -> str:
    """Return a stable non-reversible locator for repository-controlled path text."""

    return hashlib.sha256(path.encode("utf-8")).hexdigest()[:16]


def sanitize_failed_scan_stdout(output: str) -> str:
    """Allow only the scanner's fixed failure envelope and redacted findings.

    Credential values are already replaced with ``<redacted>`` by the core scanner,
    but a repository-controlled filename can itself contain a credential. Replace every
    path with a stable SHA-256 fingerprint before emitting findings to CI or terminal
    evidence. Any unexpected output shape fails closed rather than echoing untrusted text.
    """

    lines = output.splitlines()
    if len(lines) < 3 or lines[0] != SCAN_FAILED_HEADER or lines[-1] != SCAN_FAILED_FOOTER:
        raise RuntimeError("scanner failure output did not match the controlled contract")

    sanitized = [SCAN_FAILED_HEADER]
    for line in lines[1:-1]:
        match = FINDING_LINE_RE.fullmatch(line)
        if match is None:
            raise RuntimeError("scanner finding output did not match the controlled contract")
        sanitized.append(
            "path-sha256="
            f"{path_fingerprint(match.group('path'))}:"
            f"{match.group('line')}: {match.group('rule')}: <redacted>"
        )
    sanitized.append(SCAN_FAILED_FOOTER)
    return "\n".join(sanitized) + "\n"


def run_scanner_safely(scanner_main: Callable[[Sequence[str] | None], int]) -> int:
    """Run the scanner through a closed, non-disclosing evidence envelope.

    Only one exact pass message or the fixed failure envelope is allowed. Credential
    findings retain rule and line number while repository-controlled paths become
    deterministic fingerprints. Any stderr, unexpected stdout, exception, or explicit
    process exit fails closed without allowing traceback or exception text to escape.
    """

    captured_stdout = io.StringIO()
    captured_stderr = io.StringIO()
    terminated_unexpectedly = False
    with redirect_stdout(captured_stdout), redirect_stderr(captured_stderr):
        try:
            result = scanner_main(None)
        except (Exception, SystemExit):
            # The exception message, traceback context, or argparse exit output can
            # contain repository-controlled paths or values. Convert all unexpected
            # scanner termination into the same non-disclosing operational failure.
            terminated_unexpectedly = True
            result = 2

    if terminated_unexpectedly:
        print(GENERIC_SCAN_ERROR, file=sys.stderr)
        return 2

    stdout_value = captured_stdout.getvalue()
    stderr_value = captured_stderr.getvalue()

    if result == 0:
        if stderr_value or stdout_value != f"{SCAN_PASSED_MESSAGE}\n":
            print(GENERIC_SCAN_ERROR, file=sys.stderr)
            return 2
        print(SCAN_PASSED_MESSAGE)
        return 0

    if result == 1:
        if stderr_value:
            print(GENERIC_SCAN_ERROR, file=sys.stderr)
            return 2
        try:
            sanitized = sanitize_failed_scan_stdout(stdout_value)
        except RuntimeError:
            print(GENERIC_SCAN_ERROR, file=sys.stderr)
            return 2
        print(sanitized, end="")
        return 1

    print(GENERIC_SCAN_ERROR, file=sys.stderr)
    return 2


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