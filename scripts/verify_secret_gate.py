#!/usr/bin/env python3
"""Run the complete HosPrime repository-native secret gate in one process.

This command mirrors the executable security workflow without depending on a
particular shell. It is intended for local exact-commit receipts and CI. The
optional ``--git-range`` value enables the added-diff gate after the complete
tracked-tree gate succeeds.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path
from typing import Sequence

ROOT = Path(__file__).resolve().parents[1]
GENERIC_FAILURE = "SECRET GATE ERROR: verification did not complete successfully"
PASS_MESSAGE = "SECRET GATE PASS: tests, artifact gate, tracked tree and requested diff completed"
EXACT_GIT_RANGE_RE = re.compile(
    r"(?P<base>[0-9a-fA-F]{40})\.\.\.(?P<head>[0-9a-fA-F]{40})"
)


def expected_head_from_range(git_range: str) -> str | None:
    """Return the normalized exact head SHA or reject a non-exact range."""

    match = EXACT_GIT_RANGE_RE.fullmatch(git_range)
    return match.group("head").lower() if match else None


def _run_git_probe(arguments: Sequence[str]) -> subprocess.CompletedProcess[str] | None:
    """Run a non-disclosing Git probe from the repository root."""

    try:
        return subprocess.run(
            ["git", *arguments],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError:
        return None


def checkout_matches_expected_head(expected_head: str) -> bool:
    """Verify that the current checkout is the exact range head without leaking Git output."""

    completed = _run_git_probe(["rev-parse", "--verify", "HEAD"])
    return (
        completed is not None
        and completed.returncode == 0
        and completed.stdout.strip().lower() == expected_head
        and not completed.stderr
    )


def checkout_is_pristine() -> bool:
    """Require the receipt to execute only committed files from the selected checkout.

    Tracked modifications, staged changes and untracked files can change imported
    Python modules, test discovery or scanner inputs without changing ``HEAD``.
    Ignored runtime files remain excluded by Git's normal status semantics.
    """

    completed = _run_git_probe(
        ["status", "--porcelain=v1", "--untracked-files=all"]
    )
    return (
        completed is not None
        and completed.returncode == 0
        and completed.stdout == ""
        and completed.stderr == ""
    )


def build_commands(git_range: str | None) -> list[list[str]]:
    python = sys.executable
    commands = [
        [
            python,
            "-m",
            "unittest",
            "discover",
            "-v",
            "-s",
            "backend/tests",
            "-p",
            "test_secret*.py",
        ],
        [python, "scripts/secret_artifact_gate.py"],
        [python, "scripts/secret_scan_m0_entry.py"],
    ]
    if git_range is not None:
        commands.append(
            [
                python,
                "scripts/secret_scan_m0_entry.py",
                "--git-range",
                git_range,
                "--diff-only",
            ]
        )
    return commands


def run_commands(commands: Sequence[Sequence[str]]) -> int:
    for command in commands:
        try:
            completed = subprocess.run(
                list(command),
                cwd=ROOT,
                check=False,
            )
        except OSError:
            print(GENERIC_FAILURE, file=sys.stderr)
            return 2
        if completed.returncode != 0:
            return completed.returncode if completed.returncode > 0 else 2
    print(PASS_MESSAGE)
    return 0


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the complete HosPrime repository-native secret gate."
    )
    parser.add_argument(
        "--git-range",
        help="Optional exact <40-hex-base>...<40-hex-head> range for the added-diff scan.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    if args.git_range is not None:
        expected_head = expected_head_from_range(args.git_range)
        if expected_head is None or not checkout_matches_expected_head(expected_head):
            print(GENERIC_FAILURE, file=sys.stderr)
            return 2
    if not checkout_is_pristine():
        print(GENERIC_FAILURE, file=sys.stderr)
        return 2
    return run_commands(build_commands(args.git_range))


if __name__ == "__main__":
    raise SystemExit(main())
