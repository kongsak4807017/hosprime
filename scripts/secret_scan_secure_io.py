#!/usr/bin/env python3
"""Race-resistant tracked-file reads for the M0 credential scanner.

On platforms with ``openat``-style ``dir_fd`` support, every parent directory is
opened with ``O_NOFOLLOW`` and retained as a descriptor while the next component
is opened. This prevents a repository directory from being replaced by a symlink
between path validation and file reading. Platforms without the required APIs
retain the core scanner's final-component protection.
"""

from __future__ import annotations

import os
import stat
from pathlib import Path
from typing import Any, Callable


GENERIC_READ_ERROR = "tracked text path could not be safely read"
INSTALL_MARKER = "_hosprime_component_pinned_reader_installed"


def _supports_component_pinning() -> bool:
    return (
        hasattr(os, "O_DIRECTORY")
        and hasattr(os, "O_NOFOLLOW")
        and os.open in getattr(os, "supports_dir_fd", set())
        and os.stat in getattr(os, "supports_dir_fd", set())
        and os.stat in getattr(os, "supports_follow_symlinks", set())
    )


def _directory_flags() -> int:
    return (
        os.O_RDONLY
        | getattr(os, "O_DIRECTORY", 0)
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0)
    )


def _file_flags() -> int:
    return (
        os.O_RDONLY
        | getattr(os, "O_BINARY", 0)
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NOFOLLOW", 0)
    )


def _open_component_pinned(path: Path) -> tuple[int, os.stat_result]:
    """Open a regular file while pinning every traversed directory descriptor."""

    candidate = Path(path)
    components = list(candidate.parts)
    if candidate.is_absolute():
        anchor = candidate.anchor
        components = components[1:]
    else:
        anchor = "."

    if not components or any(component in ("", ".", "..") for component in components):
        raise RuntimeError(GENERIC_READ_ERROR)

    directory_fd = os.open(anchor, _directory_flags())
    try:
        for component in components[:-1]:
            next_fd = os.open(component, _directory_flags(), dir_fd=directory_fd)
            try:
                opened_directory = os.fstat(next_fd)
                if not stat.S_ISDIR(opened_directory.st_mode):
                    raise RuntimeError(GENERIC_READ_ERROR)
            except Exception:
                os.close(next_fd)
                raise
            os.close(directory_fd)
            directory_fd = next_fd

        filename = components[-1]
        before = os.stat(filename, dir_fd=directory_fd, follow_symlinks=False)
        if not stat.S_ISREG(before.st_mode):
            raise RuntimeError(GENERIC_READ_ERROR)

        descriptor = os.open(filename, _file_flags(), dir_fd=directory_fd)
        try:
            opened = os.fstat(descriptor)
            if not stat.S_ISREG(opened.st_mode):
                raise RuntimeError(GENERIC_READ_ERROR)
            if (before.st_dev, before.st_ino) != (opened.st_dev, opened.st_ino):
                raise RuntimeError(GENERIC_READ_ERROR)
            return descriptor, opened
        except Exception:
            os.close(descriptor)
            raise
    finally:
        os.close(directory_fd)


def _read_from_descriptor(
    descriptor: int,
    opened: os.stat_result,
    max_bytes: int,
    chunk_bytes: int,
) -> bytes:
    try:
        if opened.st_size > max_bytes:
            raise RuntimeError(GENERIC_READ_ERROR)

        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = os.read(descriptor, min(chunk_bytes, max_bytes + 1 - total))
            if not chunk:
                return b"".join(chunks)
            chunks.append(chunk)
            total += len(chunk)
            if total > max_bytes:
                raise RuntimeError(GENERIC_READ_ERROR)
    except (OSError, RuntimeError) as exc:
        raise RuntimeError(GENERIC_READ_ERROR) from exc
    finally:
        os.close(descriptor)


def install_component_pinned_reader(secret_scan: Any) -> None:
    """Install the hardened reader once without weakening unsupported platforms."""

    if getattr(secret_scan, INSTALL_MARKER, False):
        return

    original_reader: Callable[..., bytes] = secret_scan.read_regular_file_safely

    def read_regular_file_safely(
        path: Path,
        max_bytes: int = secret_scan.MAX_FILE_BYTES,
    ) -> bytes:
        if not _supports_component_pinning():
            return original_reader(path, max_bytes)
        try:
            descriptor, opened = _open_component_pinned(Path(path))
            return _read_from_descriptor(
                descriptor,
                opened,
                max_bytes,
                secret_scan.READ_CHUNK_BYTES,
            )
        except (OSError, RuntimeError) as exc:
            raise RuntimeError(GENERIC_READ_ERROR) from exc

    secret_scan.read_regular_file_safely = read_regular_file_safely
    setattr(secret_scan, INSTALL_MARKER, True)
