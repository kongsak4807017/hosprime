#!/usr/bin/env python3
"""Fail closed when tracked files or a Git diff contain likely credentials.

The scanner is dependency-free so it can run locally and in CI before application
packages are installed. Findings are always fully redacted. Historical credentials
that may already exist still require explicit owner-led revocation or rotation; this
scanner prevents new exposure and supports a manual full-tree audit.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence


@dataclass(frozen=True)
class Rule:
    name: str
    pattern: re.Pattern[str]


@dataclass(frozen=True)
class Finding:
    path: str
    line: int
    rule: str
    redacted: str


HIGH_CONFIDENCE_RULES: tuple[Rule, ...] = (
    Rule("private-key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----")),
    Rule("github-token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b")),
    Rule("openai-key", re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{20,}\b")),
    Rule("google-api-key", re.compile(r"\bAIza[0-9A-Za-z_-]{30,}\b")),
    Rule("aws-access-key", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
    Rule("slack-token", re.compile(r"\bxox[baprs]-[0-9A-Za-z-]{20,}\b")),
)

CREDENTIAL_KEY_TERM = (
    r"(?:password|passwd|pwd|secret|token|api[_-]?key|private[_-]?key)"
)
ASSIGNMENT_RE = re.compile(
    rf"(?ix)"
    rf"[\"']?[a-z0-9_.-]*{CREDENTIAL_KEY_TERM}[a-z0-9_.-]*[\"']?"
    rf"\s*(?::|=)\s*"
    r"(?:(?P<env>\$\{[^}\r\n]+\})"
    rf"|\"(?P<double>[^\"\r\n]+)\""
    rf"|'(?P<single>[^'\r\n]+)'"
    rf"|(?P<bare>[^\s\"'#,;}}{{\]\r\n]+))"
)
URI_USERINFO_RE = re.compile(
    r"(?i)\b[a-z][a-z0-9+.-]{1,31}://"
    r"(?P<username>[^/\s:@]+):(?P<password>[^@\s/]+)@(?P<host>[^/\s]+)"
)

SAFE_VALUE_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"(?i)^(?:change[_-]?me|changeme)(?:[_-][a-z0-9_-]+)?$"),
    re.compile(r"(?i)^(?:example|sample|dummy|fake|placeholder)(?:[_-][a-z0-9_-]+)?$"),
    re.compile(r"(?i)^(?:ci|test)[_-][a-z0-9_-]*not[_-]for[_-]production$"),
    re.compile(r"(?i)^(?:null|none|nil|~)$"),
    # Allow only direct references and required-value assertions. Compose default
    # and alternate forms (for example ${NAME:-literal} or ${NAME:+literal}) can
    # embed fixed credentials and must therefore be reported.
    re.compile(r"^\$\{[A-Za-z_][A-Za-z0-9_]*(?:(?::)?\?[^}]*)?\}$"),
    re.compile(r"(?i)^\$env:[A-Za-z_][A-Za-z0-9_]*$"),
    re.compile(r"(?i)^getenv\([^)]{1,200}\)$"),
)

TEXT_SUFFIXES = {
    "",
    ".conf",
    ".env",
    ".ini",
    ".js",
    ".json",
    ".jsx",
    ".md",
    ".ps1",
    ".py",
    ".sh",
    ".toml",
    ".ts",
    ".tsx",
    ".txt",
    ".yaml",
    ".yml",
}

MAX_FILE_BYTES = 2_000_000


def run_git(*args: str) -> bytes:
    """Run Git without allowing untrusted command output into security evidence.

    Git stderr can contain repository-controlled path text, configured helper output,
    or credential-bearing values. The scanner therefore reports only the executable
    name and numeric exit status. Callers retain the original exception as no public
    evidence because subprocess output is intentionally withheld.
    """

    completed = subprocess.run(
        ["git", *args],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            f"git command failed with exit status {completed.returncode}"
        )
    return completed.stdout


def decode_utf8(data: bytes, source: str) -> str:
    """Decode scanner input strictly so malformed bytes cannot hide credentials."""

    try:
        return data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise RuntimeError(
            f"{source} is not valid UTF-8 and cannot be safely scanned"
        ) from exc


def redact(_value: str) -> str:
    """Return a constant marker without disclosing any original character."""

    return "<redacted>"


def assignment_is_safe(value: str) -> bool:
    """Allow only explicit, whole-value placeholders or environment references.

    Substring matching is intentionally prohibited: a real credential containing
    words such as ``example`` or ``test`` must still be reported. CI or test
    literals are allowed only when the complete value explicitly ends with a
    ``not-for-production`` marker. Environment substitutions are safe only when
    they are direct references or required-value assertions; fallback and alternate
    values may contain fixed credentials and are rejected.
    """

    compact = value.strip()
    return any(pattern.fullmatch(compact) for pattern in SAFE_VALUE_PATTERNS)


def assignment_value(match: re.Match[str]) -> str:
    """Return the value from an environment, quoted or unquoted assignment."""

    for group_name in ("env", "double", "single", "bare"):
        candidate = match.group(group_name)
        if candidate is not None:
            return candidate
    raise ValueError("credential assignment did not contain a value")


def scan_line(path: str, number: int, line: str) -> list[Finding]:
    findings: list[Finding] = []
    for rule in HIGH_CONFIDENCE_RULES:
        for match in rule.pattern.finditer(line):
            findings.append(Finding(path, number, rule.name, redact(match.group(0))))

    for match in URI_USERINFO_RE.finditer(line):
        userinfo_value = match.group("password")
        if not assignment_is_safe(userinfo_value):
            findings.append(
                Finding(path, number, "credential-uri-userinfo", redact(userinfo_value))
            )

    for match in ASSIGNMENT_RE.finditer(line):
        candidate = assignment_value(match)
        if not assignment_is_safe(candidate):
            findings.append(
                Finding(path, number, "credential-assignment", redact(candidate))
            )
    return findings


def scan_text(path: str, text: str) -> list[Finding]:
    findings: list[Finding] = []
    for number, line in enumerate(text.splitlines(), start=1):
        findings.extend(scan_line(path, number, line))
    return findings


def should_scan(path: Path) -> bool:
    if path.name.startswith(".env"):
        return True
    return path.suffix.lower() in TEXT_SUFFIXES


def tracked_paths() -> list[Path]:
    raw = run_git("ls-files", "-z")
    return [Path(item.decode("utf-8")) for item in raw.split(b"\0") if item]


def scan_tracked_files(paths: Iterable[Path]) -> list[Finding]:
    """Scan candidate tracked text files and fail closed on unsafe input.

    Candidate configuration and source files must never be silently skipped because
    they are symlinks, oversized, contain NUL bytes, or contain malformed UTF-8.
    Following a tracked symlink could read outside the checkout, while a dangling
    symlink could bypass scanning entirely, so both conditions are explicit errors.
    """

    findings: list[Finding] = []
    for path in paths:
        if not should_scan(path):
            continue
        if path.is_symlink():
            raise RuntimeError(
                f"tracked text path is a symbolic link and cannot be safely scanned: {path}"
            )
        if not path.is_file():
            raise RuntimeError(f"tracked text path is not a regular file: {path}")
        try:
            file_size = path.stat().st_size
            if file_size > MAX_FILE_BYTES:
                raise RuntimeError(
                    f"tracked text file exceeds {MAX_FILE_BYTES} byte scan limit: {path}"
                )
            data = path.read_bytes()
        except OSError as exc:
            raise RuntimeError(f"cannot read tracked file {path}: {exc}") from exc
        if b"\0" in data:
            raise RuntimeError(
                f"tracked text file contains NUL bytes and cannot be safely scanned: {path}"
            )
        text = decode_utf8(data, f"tracked text file {path}")
        findings.extend(scan_text(path.as_posix(), text))
    return findings


def validate_git_range(git_range: str) -> str:
    """Reject revision ranges that Git could interpret as command-line options.

    The range is passed to ``git diff`` before the path separator, so a leading
    hyphen could override safety flags such as ``--no-ext-diff``. Control
    characters are rejected to keep errors and evidence structurally trustworthy.
    """

    if not git_range or git_range.startswith("-"):
        raise RuntimeError("Git revision range is empty or option-like")
    if any(ord(character) < 32 or ord(character) == 127 for character in git_range):
        raise RuntimeError("Git revision range contains unsafe control characters")
    return git_range


def scan_added_diff(git_range: str) -> list[Finding]:
    """Scan added lines without executing repository-configured diff helpers.

    ``--no-ext-diff`` and ``--no-textconv`` keep this security gate data-only. A
    local or repository-associated diff driver must never execute code as a side
    effect of inspecting a pull request or push range. The revision range is
    validated so it cannot be interpreted as a later Git option that re-enables a
    disabled helper.
    """

    validated_range = validate_git_range(git_range)
    raw_diff = run_git(
        "diff",
        "--unified=0",
        "--no-color",
        "--no-ext-diff",
        "--no-textconv",
        validated_range,
        "--",
    )
    diff = decode_utf8(raw_diff, f"git diff {validated_range}")
    findings: list[Finding] = []
    current_path = "<diff>"
    new_line = 0
    for raw_line in diff.splitlines():
        if raw_line.startswith("+++ b/"):
            current_path = raw_line[6:]
            continue
        if raw_line.startswith("@@"):
            match = re.search(r"\+(\d+)", raw_line)
            new_line = int(match.group(1)) if match else 0
            continue
        if raw_line.startswith("+") and not raw_line.startswith("+++"):
            findings.extend(scan_line(current_path, new_line, raw_line[1:]))
            new_line += 1
        elif not raw_line.startswith("-"):
            new_line += 1
    return findings


def deduplicate(findings: Sequence[Finding]) -> list[Finding]:
    return sorted(
        set(findings),
        key=lambda item: (item.path, item.line, item.rule, item.redacted),
    )


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--git-range",
        help="Also scan added lines in a Git revision range, for example origin/main...HEAD.",
    )
    parser.add_argument(
        "--diff-only",
        action="store_true",
        help="Scan only added lines in --git-range, not the complete tracked tree.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    if args.diff_only and not args.git_range:
        print("ERROR: --diff-only requires --git-range", file=sys.stderr)
        return 2

    try:
        findings: list[Finding] = []
        if not args.diff_only:
            findings.extend(scan_tracked_files(tracked_paths()))
        if args.git_range:
            findings.extend(scan_added_diff(args.git_range))
    except RuntimeError as exc:
        print(f"SECRET SCAN ERROR: {exc}", file=sys.stderr)
        return 2

    unique = deduplicate(findings)
    if unique:
        print("SECRET SCAN FAILED: possible credentials detected (values redacted).")
        for finding in unique:
            print(
                f"{finding.path}:{finding.line}: {finding.rule}: {finding.redacted}"
            )
        print("Remove the value from Git and rotate/revoke it through the accountable owner.")
        return 1

    print("SECRET SCAN PASSED: no likely credentials found in the selected scope.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())