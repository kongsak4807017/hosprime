"""
HosPRIME Phase 3 Backend Tests
Covers: AI Settings, Data Connector, Knowledge Graph, Digital Twin Agents
NOTE: LLM calls are real (Emergent Universal Key) - keep tests minimal.
"""
import io
import os
import time
import uuid

import pytest
import requests

BASE_URL = os.environ.get("REACT_APP_BACKEND_URL", "http://localhost:8001").rstrip("/")
API = f"{BASE_URL}/api"

ADMIN = {"email": "admin@hosprime.com", "password": "Admin@1234"}
DOCTOR = {"email": "doctor@hosprime.com", "password": "Test@1234"}
DOCTOR2 = {"email": "doctor2@hosprime.com", "password": "Test@1234"}
NURSE = {"email": "nurse@hosprime.com", "password": "Test@1234"}

MONGO_DBNAME = os.environ.get("DB_NAME", "test_database")


def _login(creds):
    s = requests.Session()
    r = s.post(f"{API}/auth/login", json=creds, timeout=15)
    assert r.status_code == 200, f"login {creds['email']} -> {r.status_code} {r.text}"
    s.headers.update({"Authorization": f"Bearer {r.json()['access_token']}"})
    return s


@pytest.fixture(scope="module")
def admin_s():
    return _login(ADMIN)


@pytest.fixture(scope="module")
def doctor_s():
    return _login(DOCTOR)


@pytest.fixture(scope="module")
def doctor2_s():
    return _login(DOCTOR2)


@pytest.fixture(scope="module")
def nurse_s():
    return _login(NURSE)


# ---------- AI Settings ----------
class TestAISettings:
    def test_get_settings_admin(self, admin_s):
        r = admin_s.get(f"{API}/ai/settings", timeout=10)
        assert r.status_code == 200, r.text
        d = r.json()
        assert d["provider"] == "emergent"
        assert d["model"] == "gpt-5.2"
        assert isinstance(d["available_models"], dict)
        assert "openai" in d["available_models"]
        # api_key should be masked
        assert d["api_key"].startswith("••••") or d["api_key"] == ""

    def test_doctor_forbidden(self, doctor_s):
        assert doctor_s.get(f"{API}/ai/settings", timeout=10).status_code == 403
        assert doctor_s.put(f"{API}/ai/settings", json={
            "provider": "emergent", "llm_provider": "openai", "model": "gpt-5.2"
        }, timeout=10).status_code == 403
        assert doctor_s.post(f"{API}/ai/settings/test", timeout=10).status_code == 403

    def test_invalid_provider_400(self, admin_s):
        r = admin_s.put(f"{API}/ai/settings", json={
            "provider": "azure", "model": "gpt-5.2"
        }, timeout=10)
        assert r.status_code == 400

    def test_custom_without_base_url_400(self, admin_s):
        r = admin_s.put(f"{API}/ai/settings", json={
            "provider": "custom", "model": "local-model", "base_url": ""
        }, timeout=10)
        assert r.status_code == 400

    def test_test_connection_llm_call(self, admin_s):
        """LLM CALL - takes ~5-20s"""
        r = admin_s.post(f"{API}/ai/settings/test", timeout=60)
        assert r.status_code == 200, r.text
        d = r.json()
        assert d["success"] is True, d
        assert "reply" in d and len(d["reply"]) > 0

    def test_restore_settings(self, admin_s):
        """Ensure settings restored to emergent/openai/gpt-5.2 at end"""
        r = admin_s.put(f"{API}/ai/settings", json={
            "provider": "emergent", "llm_provider": "openai", "model": "gpt-5.2"
        }, timeout=10)
        assert r.status_code == 200
        assert r.json()["provider"] == "emergent"
        assert r.json()["model"] == "gpt-5.2"


# ---------- Data Connector ----------
class TestDataConnector:
    internal_id = None
    external_id = None
    file_id = None

    def test_list_sources_auto_creates_internal(self, admin_s):
        r = admin_s.get(f"{API}/connector/sources", timeout=10)
        assert r.status_code == 200
        sources = r.json()
        internals = [s for s in sources if s["type"] == "internal"]
        assert len(internals) >= 1
        assert "HosPRIME" in internals[0]["name"]
        TestDataConnector.internal_id = internals[0]["id"]

    def test_doctor_forbidden(self, doctor_s):
        assert doctor_s.get(f"{API}/connector/sources", timeout=10).status_code == 403

    def test_add_external_mongo_source(self, admin_s):
        r = admin_s.post(f"{API}/connector/sources", json={
            "name": f"TEST_External_{uuid.uuid4().hex[:6]}",
            "connection_string": "mongodb://localhost:27017",
            "db_name": MONGO_DBNAME,
        }, timeout=10)
        assert r.status_code == 201, r.text
        d = r.json()
        assert d["type"] == "mongodb"
        # connection_string should be masked
        assert "••••" in d["connection_string"]
        TestDataConnector.external_id = d["id"]

    def test_scan_internal_source(self, admin_s):
        """LLM CALL - allow 90s"""
        assert TestDataConnector.internal_id
        r = admin_s.post(f"{API}/connector/sources/{TestDataConnector.internal_id}/scan", timeout=120)
        assert r.status_code == 200, r.text
        d = r.json()
        assert d["total_records"] > 0
        assert d["total_collections"] > 0
        assert d["pii_field_count"] > 0
        assert len(d["collections"]) > 0
        # verify field structure
        for col in d["collections"]:
            assert "name" in col and "count" in col and "fields" in col
            for f in col["fields"]:
                assert "name" in f and "types" in f and "fill_rate" in f and "is_pii" in f
        # AI analysis
        assert d["ai_success"] is True, f"ai_error: {d.get('ai_error')}"
        analysis = d["ai_analysis"]
        assert "Mapping" in analysis or "PDPA" in analysis or "mapping" in analysis.lower()

    def test_scan_external_mongo(self, admin_s):
        """External mongo source - should work since pointing to same local DB"""
        assert TestDataConnector.external_id
        r = admin_s.post(f"{API}/connector/sources/{TestDataConnector.external_id}/scan", timeout=120)
        assert r.status_code == 200, r.text
        d = r.json()
        assert d["total_records"] > 0

    def test_get_latest_scan(self, admin_s):
        r = admin_s.get(f"{API}/connector/sources/{TestDataConnector.internal_id}/scan", timeout=10)
        assert r.status_code == 200
        assert r.json()["source_id"] == TestDataConnector.internal_id

    def test_upload_csv_with_pii(self, admin_s):
        csv = (
            "national_id,first_name,last_name,phone,email,age\n"
            "1234567890123,สมชาย,ใจดี,0812345678,a@x.com,40\n"
            "1234567890124,สมหญิง,รักดี,0898765432,b@x.com,35\n"
        )
        files = {"file": ("TEST_patients.csv", io.BytesIO(csv.encode("utf-8")), "text/csv")}
        # Use a fresh session without Content-Type header for multipart
        s = requests.Session()
        rlogin = s.post(f"{API}/auth/login", json=ADMIN, timeout=15)
        s.headers.update({"Authorization": f"Bearer {rlogin.json()['access_token']}"})
        r = s.post(f"{API}/connector/upload", files=files, timeout=20)
        assert r.status_code == 201, r.text
        d = r.json()
        assert d["type"] == "file"
        assert d["row_count"] == 2
        TestDataConnector.file_id = d["id"]

        # Now scan file - LLM call
        r2 = admin_s.post(f"{API}/connector/sources/{TestDataConnector.file_id}/scan", timeout=120)
        assert r2.status_code == 200, r2.text
        scan = r2.json()
        pii_fields = [f for c in scan["collections"] for f in c["fields"] if f["is_pii"]]
        pii_names = {f["name"] for f in pii_fields}
        assert "national_id" in pii_names or "phone" in pii_names or "email" in pii_names, pii_names

    def test_delete_internal_400(self, admin_s):
        r = admin_s.delete(f"{API}/connector/sources/{TestDataConnector.internal_id}", timeout=10)
        assert r.status_code == 400

    def test_delete_external_works(self, admin_s):
        r = admin_s.delete(f"{API}/connector/sources/{TestDataConnector.external_id}", timeout=10)
        assert r.status_code == 200
        # cleanup file source too
        if TestDataConnector.file_id:
            admin_s.delete(f"{API}/connector/sources/{TestDataConnector.file_id}", timeout=10)


# ---------- Knowledge Graph ----------
class TestKnowledgeGraph:
    sample_patient_key = None

    def test_nurse_cannot_build(self, nurse_s):
        r = nurse_s.post(f"{API}/graph/build", timeout=10)
        assert r.status_code == 403

    def test_build_graph(self, admin_s):
        r = admin_s.post(f"{API}/graph/build", timeout=60)
        assert r.status_code == 200, r.text
        d = r.json()
        assert d["node_count"] > 30, d
        assert d["edge_count"] > 30, d
        types = d["nodes_by_type"]
        for required in ["patient", "doctor", "drug", "condition", "allergen", "labtest", "department"]:
            assert required in types, f"missing node type: {required}"

    def test_get_graph_nurse_allowed(self, nurse_s):
        r = nurse_s.get(f"{API}/graph", timeout=15)
        assert r.status_code == 200
        d = r.json()
        assert "nodes" in d and "edges" in d and "node_types" in d
        assert len(d["nodes"]) > 0

    def test_get_graph_filtered(self, admin_s):
        r = admin_s.get(f"{API}/graph", params={"node_type": "drug"}, timeout=15)
        assert r.status_code == 200
        d = r.json()
        # filtered nodes include drugs + their neighbors
        drug_nodes = [n for n in d["nodes"] if n["type"] == "drug"]
        assert len(drug_nodes) > 0

    def test_graph_stats(self, admin_s):
        r = admin_s.get(f"{API}/graph/stats", timeout=10)
        assert r.status_code == 200
        d = r.json()
        assert "nodes_by_type" in d and "edges_by_type" in d and "node_types" in d

    def test_node_neighbors(self, admin_s):
        # find a patient node
        r = admin_s.get(f"{API}/graph", params={"node_type": "patient", "limit": 5}, timeout=15)
        patient_nodes = [n for n in r.json()["nodes"] if n["type"] == "patient"]
        assert patient_nodes, "no patient nodes"
        key = patient_nodes[0]["key"]
        TestKnowledgeGraph.sample_patient_key = key
        r2 = admin_s.get(f"{API}/graph/node/{key}/neighbors", timeout=15)
        assert r2.status_code == 200, r2.text
        d = r2.json()
        assert d["node"]["key"] == key
        assert "edges" in d and "neighbors" in d

    def test_query_graph_llm(self, doctor_s):
        """LLM CALL - allow 60s. Should reference สมชาย (Penicillin allergy patient)"""
        r = doctor_s.post(f"{API}/graph/query", json={
            "question": "ผู้ป่วยคนไหนแพ้ Penicillin"
        }, timeout=120)
        assert r.status_code == 200, r.text
        d = r.json()
        assert "answer" in d and len(d["answer"]) > 0
        # We accept any reasonable Thai answer; ideally mentions สมชาย or Penicillin
        # Soft check - log but don't fail if name not present
        ans = d["answer"]
        assert "Penicillin" in ans or "เพนิ" in ans or "สมชาย" in ans or "แพ้" in ans, f"Unexpected: {ans[:300]}"


# ---------- Digital Twin Agents ----------
class TestAgents:
    session_id = None

    def test_list_agents(self, admin_s):
        r = admin_s.get(f"{API}/agents", timeout=10)
        assert r.status_code == 200
        d = r.json()
        keys = {a["key"] for a in d}
        for k in ["director", "cmo", "head_nurse", "head_pharmacy", "head_lab", "head_finance"]:
            assert k in keys, f"missing agent: {k}"
        assert len(d) == 6

    def test_chat_invalid_agent_404(self, admin_s):
        r = admin_s.post(f"{API}/agents/nonexistent/chat", json={"message": "hi"}, timeout=10)
        assert r.status_code == 404

    def test_chat_empty_message_400(self, admin_s):
        r = admin_s.post(f"{API}/agents/head_pharmacy/chat", json={"message": "   "}, timeout=10)
        assert r.status_code == 400

    def test_first_message_llm(self, admin_s):
        """LLM CALL - allow 90s"""
        r = admin_s.post(f"{API}/agents/head_pharmacy/chat", json={
            "message": "มียาอะไรใกล้หมดสต็อกบ้าง"
        }, timeout=120)
        assert r.status_code == 200, r.text
        d = r.json()
        assert "session_id" in d and "reply" in d
        assert len(d["reply"]) > 10
        # Soft check: Amlodipine is low_stock in seed
        # Just ensure reply mentions a drug-related Thai context
        TestAgents.session_id = d["session_id"]

    def test_multi_turn_with_same_session(self, admin_s):
        """LLM CALL - second message in same session"""
        assert TestAgents.session_id
        r = admin_s.post(f"{API}/agents/head_pharmacy/chat", json={
            "message": "แล้วควรสั่งซื้อเพิ่มเท่าไหร่",
            "session_id": TestAgents.session_id,
        }, timeout=120)
        assert r.status_code == 200, r.text
        d = r.json()
        assert d["session_id"] == TestAgents.session_id

    def test_list_sessions(self, admin_s):
        r = admin_s.get(f"{API}/agents/head_pharmacy/sessions", timeout=10)
        assert r.status_code == 200
        sessions = r.json()
        assert any(s["id"] == TestAgents.session_id for s in sessions)

    def test_get_messages(self, admin_s):
        r = admin_s.get(f"{API}/agents/sessions/{TestAgents.session_id}/messages", timeout=10)
        assert r.status_code == 200
        d = r.json()
        assert len(d["messages"]) == 4
        roles = [m["role"] for m in d["messages"]]
        assert roles == ["user", "assistant", "user", "assistant"]

    def test_doctor_cannot_access_admin_session(self, doctor_s):
        r = doctor_s.get(f"{API}/agents/sessions/{TestAgents.session_id}/messages", timeout=10)
        assert r.status_code == 404

    def test_doctor_cannot_chat_in_admin_session(self, doctor_s):
        r = doctor_s.post(f"{API}/agents/head_pharmacy/chat", json={
            "message": "hi", "session_id": TestAgents.session_id
        }, timeout=15)
        assert r.status_code == 404

    def test_delete_session(self, admin_s):
        r = admin_s.delete(f"{API}/agents/sessions/{TestAgents.session_id}", timeout=10)
        assert r.status_code == 200
        # session gone
        r2 = admin_s.get(f"{API}/agents/sessions/{TestAgents.session_id}/messages", timeout=10)
        assert r2.status_code == 404
