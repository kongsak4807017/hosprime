from pathlib import Path
import hashlib
import yaml

TEMPLATE = Path("docs/testing/M0_3_TRIAL_READINESS_RECORD_TEMPLATE.yml")


def test_template_parses_and_is_fail_closed():
    text = TEMPLATE.read_text(encoding="utf-8")
    data = yaml.safe_load(text)

    assert isinstance(data, dict)

    core_gates = [
        "gate_1_authorization",
        "gate_2_executor_delegation",
        "gate_3_participant_consent",
        "gate_4_acceptance_authority",
        "gate_5_runtime_environment",
        "gate_6_repository_and_fixture",
        "gate_7_synthetic_scope_acknowledgement",
        "gate_8_audit_and_evidence_package",
    ]

    assert all(gate in data for gate in core_gates)
    assert all(data[gate]["state"] == "MISSING" for gate in core_gates)
    assert data["record_control"]["lifecycle_state"] == "DRAFT"
    assert data["derived_readiness"]["trial_ready"] is False
    assert data["derived_readiness"]["default_fail_closed"] is True
    assert len(data["derived_readiness"]["gate_validity"]) == 8
    assert all(value is False for value in data["derived_readiness"]["gate_validity"].values())
    assert all(value is False for value in data["derived_readiness"]["explicit_non_claims"].values())

    scope = data["scope_boundary"]
    assert scope["real_personal_staff_patient_or_confidential_data_allowed"] is False
    assert scope["high_impact_action_allowed"] is False
    assert scope["organizational_memory_promotion_allowed"] is False
    assert scope["rag_activation_allowed"] is False
    assert scope["fixture_mutation_allowed"] is False

    gate_6 = data["gate_6_repository_and_fixture"]
    assert gate_6["mutable_branch_or_tag_used_as_authority"] is False
    assert gate_6["expected_inventory_count"] == len(gate_6["expected_inventory"]) == 5

    stop = data["stop_conditions"]
    required_stops = [
        "stop_if_any_core_gate_not_complete",
        "stop_if_evidence_reference_missing",
        "stop_if_authorization_expired_or_revoked",
        "stop_if_consent_missing_or_withdrawn",
        "stop_if_repository_sha_missing_or_mutable",
        "stop_if_fixture_integrity_fails",
        "stop_if_role_conflict_unresolved",
        "stop_if_retention_authority_unassigned",
        "stop_if_prohibited_data_or_action_detected",
    ]
    assert all(stop[name] is True for name in required_stops)

    # Receipt-friendly deterministic fingerprint for the exact tested artifact.
    assert len(hashlib.sha256(text.encode("utf-8")).hexdigest()) == 64
