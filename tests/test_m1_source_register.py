from pathlib import Path

REGISTER_PATH = Path(__file__).resolve().parents[1] / "data" / "source_register" / "m1_source_register.yml"

REQUIRED_FIELDS = {
    "source_id",
    "knowledge_pack",
    "source_title",
    "source_type",
    "organization",
    "owner_role",
    "owner_person",
    "file_or_system_location",
    "version",
    "checksum",
    "checksum_pending_reason",
    "classification",
    "access_policy",
    "allowed_roles",
    "lifecycle_state",
    "review_status",
    "reviewer",
    "decision_date",
    "review_date",
    "next_review_date",
    "parsing_status",
    "quality_status",
    "approval_status",
    "active_rag_index",
    "limitation_note",
}

ALLOWED_SEED_STATES = {"DISCOVERED", "QUARANTINED"}
EXPECTED_PACKS = {
    "PM2.5 and Environmental Health",
    "Tuberculosis and Communicable Disease Control",
    "NCD and Chronic Care Service Model",
    "Disaster, EOC and Public Health Emergency Operations",
    "Digital Health, Data Governance and AI Workflow",
}


def _load_seed_records():
    """Minimal YAML subset reader for the controlled seed-register shape.

    This avoids adding a runtime dependency only to validate the initial seed file.
    It intentionally supports the simple top-level `records:` list used by
    data/source_register/m1_source_register.yml.
    """
    text = REGISTER_PATH.read_text(encoding="utf-8")
    assert "records:" in text, "source register must contain a records list"

    records = []
    current = None
    current_list_key = None
    in_records = False

    for raw_line in text.splitlines():
        if raw_line.strip() == "records:":
            in_records = True
            continue
        if not in_records:
            continue
        if raw_line.startswith("  - "):
            if current:
                records.append(current)
            current = {}
            current_list_key = None
            key, value = raw_line[4:].split(":", 1)
            current[key.strip()] = _clean_scalar(value)
            continue
        if current is None:
            continue
        if raw_line.startswith("    ") and not raw_line.startswith("      - ") and ":" in raw_line:
            key, value = raw_line.strip().split(":", 1)
            key = key.strip()
            value = value.strip()
            if value == "":
                current[key] = []
                current_list_key = key
            else:
                current[key] = _clean_scalar(value)
                current_list_key = None
            continue
        if raw_line.startswith("      - ") and current_list_key:
            current[current_list_key].append(raw_line.strip()[2:].strip())

    if current:
        records.append(current)
    return records


def _clean_scalar(value):
    value = value.strip()
    if value == "null":
        return None
    if value == "false":
        return False
    if value == "true":
        return True
    return value


def test_register_file_exists():
    assert REGISTER_PATH.exists(), "M1 source register file must exist before ingestion build proceeds"


def test_seed_register_contains_five_priority_knowledge_packs():
    records = _load_seed_records()
    assert len(records) == 5
    assert {record["knowledge_pack"] for record in records} == EXPECTED_PACKS


def test_seed_records_have_required_metadata_fields():
    for record in _load_seed_records():
        missing = REQUIRED_FIELDS - set(record)
        assert not missing, f"{record.get('source_id', 'unknown')} missing fields: {sorted(missing)}"


def test_seed_records_are_not_approved_or_indexed():
    for record in _load_seed_records():
        assert record["lifecycle_state"] in ALLOWED_SEED_STATES
        assert record["approval_status"] == "not_approved"
        assert record["active_rag_index"] is False
        assert record["review_status"] == "not_reviewed"
        assert record["decision_date"] is None


def test_restricted_sources_have_role_scoped_access_policy():
    for record in _load_seed_records():
        if record["classification"] == "restricted_internal":
            assert record["access_policy"] == "role_scoped_restricted"
            assert isinstance(record["allowed_roles"], list)
            assert "knowledge_reviewer" in record["allowed_roles"]
