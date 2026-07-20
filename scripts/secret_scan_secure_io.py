#!/usr/bin/env python3
"""Race-resistant tracked-file reads for the M0 credential scanner.

On platforms with ``openat``-style ``dir_fd`` support, every parent directory is
opened relative to a pinned descriptor and its pre-open identity is compared with
the opened descriptor. Relative tracked paths are resolved from a checkout-root
descriptor captured when the hardened reader is installed, so a later process-wide
working-directory change cannot redirect a validated scan. Platforms without the
required APIs retain the core scanner's final-component protection.
"""

from __future__ import annotations

import os
import stat
from pathlib import Path
from typing import Any, Callable


GENERIC_READ_ERROR = "tracked text path could not be safely read"
INSTALL_MARKER = "_hosprime_component_pinned_reader_installed"
ROOT_FD_MARKER = "_hosprime_component_pinned_root_fd"
ROOT_IDENTITY_MARKER = "_hosprime_component_pinned_root_identity"


def _detect_component_pinning_support() -> bool:
    return (
        hasattr(os, "O_DIRECTORY")
        and hasattr(os, "O_NOFOLLOW")
        and os.open in getattr(os, "supports_dir_fd", set())
        and os.stat in getattr(os, "supports_dir_fd", set())
        and os.stat in getattr(os, "supports_follow_symlinks", set())
    )


# Detect once at import time. Tests and security instrumentation may intercept
# ``os.open`` later; that must not silently downgrade the hardened reader.
COMPONENT_PINNING_SUPPORTED = _detect_component_pinning_support()


def _supports_component_pinning() -> bool:
    return COMPONENT_PINNING_SUPPORTED


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


def _same_identity(before: os.stat_result, opened: os.stat_result) -> bool:
    return (before.st_dev, before.st_ino) == (opened.st_dev, opened.st_ino)


def _directory_identity(metadata: os.stat_result) -> tuple[int, int, int]:
    """Return the immutable trust identity for a pinned checkout directory."""

    return metadata.st_dev, metadata.st_ino, metadata.st_mode


def _is_single_link_regular(metadata: os.stat_result) -> bool:
    """Require an ordinary file with one filesystem name.

    A tracked path replaced with a hard link can otherwise reference an inode whose
    content is controlled outside the checkout while still passing regular-file,
    symlink, and inode-stability checks. Git checkouts do not require hard-linked
    working-tree files, so the security gate fails closed when ``st_nlink`` is not 1.
    """

    return stat.S_ISREG(metadata.st_mode) and metadata.st_nlink == 1


def _snapshot_identity(metadata: os.stat_result) -> tuple[int, int, int, int, int, int, int]:
    """Return fields that must remain stable for one trustworthy file read."""

    return (
        metadata.st_dev,
        metadata.st_ino,
        metadata.st_mode,
        metadata.st_nlink,
        metadata.st_size,
        getattr(metadata, "st_mtime_ns", int(metadata.st_mtime * 1_000_000_000)),
        getattr(metadata, "st_ctime_ns", int(metadata.st_ctime * 1_000_000_000)),
    )


def _validated_relative_components(path: Path) -> list[str]:
    candidate = Path(path)
    if candidate.is_absolute():
        raise RuntimeError(GENERIC_READ_ERROR)
    components = list(candidate.parts)
    if not components or any(component in ("", ".", "..") for component in components):
        raise RuntimeError(GENERIC_READ_ERROR)
    return components


def _open_components(directory_fd: int, components: list[str]) -> tuple[int, os.stat_result]:
    """Open validated components relative to an owned directory descriptor."""

    try:
        for component in components[:-1]:
            before_directory = os.stat(
                component,
                dir_fd=directory_fd,
                follow_symlinks=False,
            )
            if not stat.S_ISDIR(before_directory.st_mode):
                raise RuntimeError(GENERIC_READ_ERROR)

            next_fd = os.open(component, _directory_flags(), dir_fd=directory_fd)
            try:
                opened_directory = os.fstat(next_fd)
                if not stat.S_ISDIR(opened_directory.st_mode):
                    raise RuntimeError(GENERIC_READ_ERROR)
                if not _same_identity(before_directory, opened_directory):
                    raise RuntimeError(GENERIC_READ_ERROR)
            except Exception:
                os.close(next_fd)
                raise
            os.close(directory_fd)
            directory_fd = next_fd

        filename = components[-1]
        before = os.stat(filename, dir_fd=directory_fd, follow_symlinks=False)
        if not _is_single_link_regular(before):
            raise RuntimeError(GENERIC_READ_ERROR)

        descriptor = os.open(filename, _file_flags(), dir_fd=directory_fd)
        try:
            opened = os.fstat(descriptor)
            if not _is_single_link_regular(opened):
                raise RuntimeError(GENERIC_READ_ERROR)
            if not _same_identity(before, opened):
                raise RuntimeError(GENERIC_READ_ERROR)
            return descriptor, opened
        except Exception:
            os.close(descriptor)
            raise
    finally:
        os.close(directory_fd)


def _open_component_pinned_at(
    root_fd: int,
    expected_root_identity: tuple[int, int, int],
    path: Path,
) -> tuple[int, os.stat_result]:
    """Open a repository-relative file from a verified pinned checkout root."""

    components = _validated_relative_components(Path(path))
    try:
        owned_root_fd = os.dup(root_fd)
        opened_root = os.fstat(owned_root_fd)
        if (
            not stat.S_ISDIR(opened_root.st_mode)
            or _directory_identity(opened_root) != expected_root_identity
        ):
            raise RuntimeError(GENERIC_READ_ERROR)
    except (OSError, RuntimeError) as exc:
        if "owned_root_fd" in locals():
            os.close(owned_root_fd)
        raise RuntimeError(GENERIC_READ_ERROR) from exc
    return _open_components(owned_root_fd, components)


def _open_component_pinned(path: Path) -> tuple[int, os.stat_result]:
    """Open an absolute or current-directory-relative regular file safely."""

    candidate = Path(path)
    if candidate.is_absolute():
        anchor = candidate.anchor
        components = list(candidate.parts)[1:]
        if not components or any(component in ("", ".", "..") for component in components):
            raise RuntimeError(GENERIC_READ_ERROR)
        directory_fd = os.open(anchor, _directory_flags())
        return _open_components(directory_fd, components)

    directory_fd = os.open(".", _directory_flags())
    return _open_components(directory_fd, _validated_relative_components(candidate))


def _read_from_descriptor(
    descriptor: int,
    opened: os.stat_result,
    max_bytes: int,
    chunk_bytes: int,
) -> bytes:
    try:
        if (
            max_bytes < 0
            or chunk_bytes <= 0
            or opened.st_size > max_bytes
            or not _is_single_link_regular(opened)
        ):
            raise RuntimeError(GENERIC_READ_ERROR)

        initial_snapshot = _snapshot_identity(opened)
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = os.read(descriptor, min(chunk_bytes, max_bytes + 1 - total))
            if not chunk:
                final_metadata = os.fstat(descriptor)
                if (
                    not _is_single_link_regular(final_metadata)
                    or _snapshot_identity(final_metadata) != initial_snapshot
                ):
                    raise RuntimeError(GENERIC_READ_ERROR)
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
    """Install the hardened reader once and pin its repository trust root."""

    if getattr(secret_scan, INSTALL_MARKER, False):
        return

    original_reader: Callable[..., bytes] = secret_scan.read_regular_file_safely
    root_fd: int | None = None
    if COMPONENT_PINNING_SUPPORTED:
        try:
            root_fd = os.open(".", _directory_flags())
            root_metadata = os.fstat(root_fd)
            if not stat.S_ISDIR(root_metadata.st_mode):
                raise RuntimeError(GENERIC_READ_ERROR)
            root_identity = _directory_identity(root_metadata)
        except (OSError, RuntimeError) as exc:
            if root_fd is not None:
                os.close(root_fd)
            raise RuntimeError(GENERIC_READ_ERROR) from exc
        setattr(secret_scan, ROOT_FD_MARKER, root_fd)
        setattr(secret_scan, ROOT_IDENTITY_MARKER, root_identity)

    def read_regular_file_safely(
        path: Path,
        max_bytes: int = secret_scan.MAX_FILE_BYTES,
    ) -> bytes:
        if not COMPONENT_PINNING_SUPPORTED:
            return original_reader(path, max_bytes)
        try:
            candidate = Path(path)
            if candidate.is_absolute():
                descriptor, opened = _open_component_pinned(candidate)
            else:
                pinned_root_fd = getattr(secret_scan, ROOT_FD_MARKER, None)
                pinned_root_identity = getattr(secret_scan, ROOT_IDENTITY_MARKER, None)
                if not isinstance(pinned_root_fd, int) or not (
                    isinstance(pinned_root_identity, tuple)
                    and len(pinned_root_identity) == 3
                    and all(isinstance(value, int) for value in pinned_root_identity)
                ):
                    raise RuntimeError(GENERIC_READ_ERROR)
                descriptor, opened = _open_component_pinned_at(
                    pinned_root_fd,
                    pinned_root_identity,
                    candidate,
                )
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
