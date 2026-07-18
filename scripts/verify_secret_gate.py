#!/usr/bin/env python3
"""Run the complete HosPrime repository-native secret gate in one process.

This command mirrors the executable security workflow without depending on a
particular shell. It is intended for local exact-commit receipts and CI. The
optional ``--git-range`` value enables the added-diff gate after the complete
tracked-tree gate succeeds.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Sequence

ROOT = Path(__file__).resolve().parents[1]
GENERIC_FAILURE = "SECRET GATE ERROR: verification did not complete successfully"
PASS_MESSAGE = "SECRET GATE PASS: tests, artifact gate, tracked tree and requested diff completed"


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
        help="Optional validated Git revision range for the added-diff scan.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    return run_commands(build_commands(args.git_range))


if __name__ == "__main__":
    raise SystemExit(main())
