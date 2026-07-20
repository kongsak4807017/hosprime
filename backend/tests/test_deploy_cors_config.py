from pathlib import Path

import pytest

from backend.app.core.cors import (
    CorsConfigurationError,
    redact_cors_error,
    validate_local_m0_cors_origins,
)

ROOT = Path(__file__).resolve().parents[2]


def test_default_frontend_port_accepts_both_loopback_origins() -> None:
    origins = validate_local_m0_cors_origins(
        '["http://localhost","http://127.0.0.1"]',
        80,
    )

    assert origins == ["http://127.0.0.1", "http://localhost"]


def test_custom_frontend_port_requires_both_matching_loopback_origins() -> None:
    origins = validate_local_m0_cors_origins(
        '["http://localhost:18080","http://127.0.0.1:18080"]',
        18080,
    )

    assert origins == ["http://127.0.0.1:18080", "http://localhost:18080"]


@pytest.mark.parametrize(
    "raw_value,frontend_port",
    (
        ('["*"]', 80),
        ('["https://localhost"]', 80),
        ('["http://0.0.0.0"]', 80),
        ('["http://localhost:18080"]', 18080),
        ('["http://localhost","http://127.0.0.1"]', 18080),
        ('["http://user:password@localhost"]', 80),
        ('["http://localhost/path","http://127.0.0.1"]', 80),
        ('["http://localhost?token=value","http://127.0.0.1"]', 80),
        ('["http://localhost#fragment","http://127.0.0.1"]', 80),
        ('["http://localhost","http://localhost"]', 80),
        (
            '["http://localhost","http://localhost:80","http://127.0.0.1"]',
            80,
        ),
        (
            '["http://localhost","http://localhost/","http://127.0.0.1"]',
            80,
        ),
        (
            '["http://localhost:18080","http://localhost:18080/",'
            '"http://127.0.0.1:18080"]',
            18080,
        ),
    ),
)
def test_unsafe_or_inconsistent_origins_are_rejected(
    raw_value: str,
    frontend_port: int,
) -> None:
    with pytest.raises(CorsConfigurationError):
        validate_local_m0_cors_origins(raw_value, frontend_port)


def test_comma_separated_origins_are_supported_for_operator_compatibility() -> None:
    origins = validate_local_m0_cors_origins(
        "http://localhost:18080,http://127.0.0.1:18080",
        18080,
    )

    assert origins == ["http://127.0.0.1:18080", "http://localhost:18080"]


def test_error_evidence_is_fixed_and_does_not_echo_rejected_origin() -> None:
    rejected = "http://user:synthetic-secret@external.invalid:4444"
    try:
        validate_local_m0_cors_origins(f'["{rejected}"]', 80)
    except CorsConfigurationError as exc:
        evidence = redact_cors_error(exc)
    else:  # pragma: no cover - protects the non-disclosure assertion itself
        raise AssertionError("unsafe origin unexpectedly accepted")

    assert evidence == "CORS_ORIGINS is unsafe or inconsistent with FRONTEND_PORT"
    assert rejected not in evidence
    assert "synthetic-secret" not in evidence
    assert "external.invalid" not in evidence


def test_compose_passes_frontend_port_to_backend_runtime_gate() -> None:
    compose = (ROOT / "docker-compose.yml").read_text(encoding="utf-8")

    assert "CORS_ORIGINS: ${CORS_ORIGINS:" in compose
    assert "FRONTEND_PORT: ${FRONTEND_PORT:-80}" in compose


def test_backend_uses_validated_origins_and_fixed_error_message() -> None:
    main = (ROOT / "backend/app/main.py").read_text(encoding="utf-8")

    assert "validate_local_m0_cors_origins(raw_origins, frontend_port)" in main
    assert "raise RuntimeError(redact_cors_error(exc)) from exc" in main
    assert "allow_origins=allowed_origins" in main
