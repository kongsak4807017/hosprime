#!/usr/bin/env python3
"""Run the complete HosPrime repository-native secret gate in one process.

This command mirrors the executable security workflow without depending on a
particular shell. It is intended for local exact-commit receipts and CI. The
optional ``--git-range`` value enables the added-diff gate after the complete
tracked-tree gate succeeds.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Mapping, Sequence

ROOT = Path(__file__).resolve().parents[1]
GENERIC_FAILURE = "SECRET GATE ERROR: verification did not complete successfully"
PASS_MESSAGE = "SECRET GATE PASS: tests, artifact gate, tracked tree and requested diff completed"
EXACT_GIT_RANGE_RE = re.compile(
    r"(?P<base>[0-9a-fA-F]{40})\.\.\.(?P<head>[0-9a-fA-F]{40})"
)


def exact_commits_from_range(git_range: str) -> tuple[str, str] | None:
    """Return normalized base/head SHAs or reject a non-exact range."""

    match = EXACT_GIT_RANGE_RE.fullmatch(git_range)
    if match is None:
        return None
    return match.group("base").lower(), match.group("head").lower()


def expected_head_from_range(git_range: str) -> str | None:
    """Return the normalized exact head SHA or reject a non-exact range."""

    commits = exact_commits_from_range(git_range)
    return commits[1] if commits is not None else None


def sanitized_git_environment(
    source: Mapping[str, str] | None = None,
) -> dict[str, str] | None:
    """Return an environment that cannot redirect Git-backed security work.

    Git repository-selection and object-store variables such as ``GIT_DIR``,
    ``GIT_WORK_TREE`` and ``GIT_OBJECT_DIRECTORY`` override ``cwd`` and can make
    HEAD/status/ancestry probes or scanner-owned Git commands describe a different
    repository from the files that the security commands execute. Configuration-
    injection variables can also alter local Git behavior. The receipt requires
    none of these variables, so every inherited ``GIT_*`` key is removed.

    ``None`` is returned when no sanitization is required so ordinary subprocess
    call signatures remain stable and the child inherits the normal environment.
    """

    inherited = os.environ if source is None else source
    if not any(key.upper().startswith("GIT_") for key in inherited):
        return None
    return {
        key: value
        for key, value in inherited.items()
        if not key.upper().startswith("GIT_")
    }


def _run_git_probe(arguments: Sequence[str]) -> subprocess.CompletedProcess[str] | None:
    """Run a non-disclosing Git probe from the repository root."""

    kwargs: dict[str, object] = {
        "cwd": ROOT,
        "check": False,
        "capture_output": True,
        "text": True,
    }
    environment = sanitized_git_environment()
    if environment is not None:
        kwargs["env"] = environment
    try:
        return subprocess.run(["git", *arguments], **kwargs)
    except OSError:
        return None


def _git_probe_succeeded(arguments: Sequence[str]) -> bool:
    """Require a silent successful Git probe without forwarding repository output."""

    completed = _run_git_probe(arguments)
    return (
        completed is not None
        and completed.returncode == 0
        and completed.stdout == ""
        and completed.stderr == ""
    )


def checkout_matches_expected_head(expected_head: str) -> bool:
    """Verify that the current checkout is the exact range head without leaking Git output."""

    completed = _run_git_probe(["rev-parse", "--verify", "HEAD"])
    return (
        completed is not None
        and completed.returncode == 0
        and completed.stdout.strip().lower() == expected_head
        and not completed.stderr
    )


def exact_range_is_valid(base_sha: str, head_sha: str) -> bool:
    """Require real commit objects and a base that is an ancestor of the exact head.

    Merely accepting two 40-hex values is insufficient for an accountable receipt:
    a missing object, unrelated commit, or reversed range can change the meaning of
    an added-diff scan. All probes are captured and must complete silently.
    """

    return (
        _git_probe_succeeded(["cat-file", "-e", f"{base_sha}^{{commit}}"])
        and _git_probe_succeeded(["cat-file", "-e", f"{head_sha}^{{commit}}"])
        and _git_probe_succeeded(
            ["merge-base", "--is-ancestor", base_sha, head_sha]
        )
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
    """Run every gate with the same repository-selection isolation as provenance probes."""

    environment = sanitized_git_environment()
    for command in commands:
        kwargs: dict[str, object] = {
            "cwd": ROOT,
            "check": False,
        }
        if environment is not None:
            kwargs["env"] = environment
        try:
            completed = subprocess.run(list(command), **kwargs)
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
        commits = exact_commits_from_range(args.git_range)
        if commits is None:
            print(GENERIC_FAILURE, file=sys.stderr)
            return 2
        base_sha, expected_head = commits
        if (
            not checkout_matches_expected_head(expected_head)
            or not exact_range_is_valid(base_sha, expected_head)
        ):
            print(GENERIC_FAILURE, file=sys.stderr)
            return 2
    if not checkout_is_pristine():
        print(GENERIC_FAILURE, file=sys.stderr)
        return 2
    return run_commands(build_commands(args.git_range))


if __name__ == "__main__":
    raise SystemExit(main())
