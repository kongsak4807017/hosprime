from __future__ import annotations

import json
from collections.abc import Iterable
from urllib.parse import urlsplit


class CorsConfigurationError(ValueError):
    """Raised when local M0 CORS configuration is unsafe or inconsistent."""


def _parse_origins(raw_value: str) -> list[str]:
    value = raw_value.strip()
    if not value:
        raise CorsConfigurationError("CORS origins are required for the local M0 preview")

    try:
        decoded = json.loads(value)
    except json.JSONDecodeError:
        decoded = [item.strip() for item in value.split(",") if item.strip()]

    if not isinstance(decoded, list) or not decoded:
        raise CorsConfigurationError("CORS origins must be a non-empty list")
    if any(not isinstance(origin, str) or not origin.strip() for origin in decoded):
        raise CorsConfigurationError("CORS origins must contain only non-empty strings")
    if len(decoded) != len(set(decoded)):
        raise CorsConfigurationError("CORS origins must not contain duplicates")
    return decoded


def _canonical_local_origin(host: str, port: int) -> str:
    suffix = "" if port == 80 else f":{port}"
    return f"http://{host}{suffix}"


def expected_local_origins(frontend_port: int) -> frozenset[str]:
    if isinstance(frontend_port, bool) or not isinstance(frontend_port, int):
        raise CorsConfigurationError("Frontend port must be an integer")
    if not 1 <= frontend_port <= 65535:
        raise CorsConfigurationError("Frontend port must be between 1 and 65535")
    return frozenset(
        {
            _canonical_local_origin("localhost", frontend_port),
            _canonical_local_origin("127.0.0.1", frontend_port),
        }
    )


def validate_local_m0_cors_origins(
    raw_value: str,
    frontend_port: int,
) -> list[str]:
    """Return validated origins for the loopback-only M0 developer preview.

    The browser origin must match the actual published frontend port. Wildcards,
    credentials, paths, query strings, fragments, HTTPS, and non-loopback hosts
    are rejected so a healthy backend cannot mask an unusable or overexposed UI.
    Multiple textual spellings of the same effective origin are rejected as
    duplicates so the configured allow-list has one unambiguous representation.
    """

    origins = _parse_origins(raw_value)
    expected = expected_local_origins(frontend_port)

    normalized: set[str] = set()
    for origin in origins:
        try:
            parsed = urlsplit(origin)
            parsed_port = parsed.port
        except ValueError as exc:
            raise CorsConfigurationError("CORS origin is malformed") from exc

        if (
            parsed.scheme != "http"
            or parsed.hostname not in {"localhost", "127.0.0.1"}
            or parsed.username is not None
            or parsed.password is not None
            or parsed.path not in {"", "/"}
            or parsed.query
            or parsed.fragment
        ):
            raise CorsConfigurationError("CORS origin is outside the local M0 boundary")

        effective_port = parsed_port if parsed_port is not None else 80
        canonical_origin = _canonical_local_origin(parsed.hostname, effective_port)
        if canonical_origin in normalized:
            raise CorsConfigurationError("CORS origins must not contain equivalent duplicates")
        normalized.add(canonical_origin)

    if normalized != expected:
        raise CorsConfigurationError(
            "CORS origins must match both loopback frontend origins and the published frontend port"
        )

    return sorted(normalized)


def redact_cors_error(_: BaseException) -> str:
    """Return a fixed non-sensitive message for runtime and deployment evidence."""

    return "CORS_ORIGINS is unsafe or inconsistent with FRONTEND_PORT"
