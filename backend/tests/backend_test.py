"""
HosPRIME Backend Tests
Covers: Auth, RBAC, Patients CRUD, Appointments, Dashboard
"""
import os
import uuid
from datetime import datetime, timedelta, timezone

import pytest
import requests

BASE_URL = os.environ.get("REACT_APP_BACKEND_URL", "https://production-ready-195.preview.emergentagent.com").rstrip("/")
API = f"{BASE_URL}/api"

ADMIN = {"email": "admin@hosprime.com", "password": "Admin@1234"}
DOCTOR = {"email": "doctor@hosprime.com", "password": "Test@1234"}
NURSE = {"email": "nurse@hosprime.com", "password": "Test@1234"}
FINANCE = {"email": "finance@hosprime.com", "password": "Test@1234"}


def _login(creds):
    s = requests.Session()
    r = s.post(f"{API}/auth/login", json=creds, timeout=15)
    assert r.status_code == 200, f"login failed for {creds['email']}: {r.status_code} {r.text}"
    return s, r.json().get("access_token")


@pytest.fixture(scope="session")
def admin_sess():
    s, t = _login(ADMIN)
    s.headers.update({"Authorization": f"Bearer {t}"})
    return s


@pytest.fixture(scope="session")
def doctor_sess():
    s, t = _login(DOCTOR)
    s.headers.update({"Authorization": f"Bearer {t}"})
    return s


@pytest.fixture(scope="session")
def nurse_sess():
    s, t = _login(NURSE)
    s.headers.update({"Authorization": f"Bearer {t}"})
    return s


@pytest.fixture(scope="session")
def finance_sess():
    s, t = _login(FINANCE)
    s.headers.update({"Authorization": f"Bearer {t}"})
    return s


# ---------------- AUTH ----------------
class TestAuth:
    def test_root(self):
        r = requests.get(f"{API}/", timeout=10)
        assert r.status_code == 200
        assert r.json().get("status") == "operational"

    def test_login_sets_cookies(self):
        s = requests.Session()
        r = s.post(f"{API}/auth/login", json=ADMIN, timeout=10)
        assert r.status_code == 200
        body = r.json()
        assert body["email"] == ADMIN["email"]
        assert body["role"] == "admin"
        assert "access_token" in body
        assert "password_hash" not in body
        # cookies
        cookie_names = {c.name for c in s.cookies}
        assert "access_token" in cookie_names
        assert "refresh_token" in cookie_names

    def test_me_with_cookie(self):
        s = requests.Session()
        s.post(f"{API}/auth/login", json=ADMIN, timeout=10)
        r = s.get(f"{API}/auth/me", timeout=10)
        assert r.status_code == 200
        assert r.json()["email"] == ADMIN["email"]

    def test_login_wrong_password_returns_thai_401(self):
        # use a unique email to avoid lockout impact on real users
        r = requests.post(f"{API}/auth/login", json={"email": "nonexistent_test@hosprime.com", "password": "wrong"}, timeout=10)
        assert r.status_code == 401
        # Thai error
        assert "อีเมล" in r.json().get("detail", "") or "รหัสผ่าน" in r.json().get("detail", "")

    def test_refresh_token(self):
        s = requests.Session()
        s.post(f"{API}/auth/login", json=ADMIN, timeout=10)
        old_access = s.cookies.get("access_token")
        r = s.post(f"{API}/auth/refresh", timeout=10)
        assert r.status_code == 200
        new_access = s.cookies.get("access_token")
        assert new_access and new_access != old_access

    def test_logout_clears_cookies(self):
        s = requests.Session()
        s.post(f"{API}/auth/login", json=ADMIN, timeout=10)
        r = s.post(f"{API}/auth/logout", timeout=10)
        assert r.status_code == 200
        # after logout, me should 401
        r2 = s.get(f"{API}/auth/me", timeout=10)
        assert r2.status_code == 401


# ---------------- RBAC ----------------
class TestRBAC:
    def test_admin_can_register(self, admin_sess):
        email = f"test_{uuid.uuid4().hex[:8]}@hosprime.com"
        r = admin_sess.post(f"{API}/auth/register", json={
            "email": email, "password": "Pass@1234",
            "full_name": "Test Staff", "role": "nurse"
        }, timeout=10)
        assert r.status_code == 201
        data = r.json()
        assert data["email"] == email
        assert data["role"] == "nurse"
        # duplicate -> 409
        r2 = admin_sess.post(f"{API}/auth/register", json={
            "email": email, "password": "Pass@1234",
            "full_name": "Dup", "role": "nurse"
        }, timeout=10)
        assert r2.status_code == 409

    def test_admin_invalid_role(self, admin_sess):
        r = admin_sess.post(f"{API}/auth/register", json={
            "email": f"x_{uuid.uuid4().hex[:6]}@hosprime.com",
            "password": "Pass@1234", "full_name": "X", "role": "superuser"
        }, timeout=10)
        assert r.status_code == 400

    def test_doctor_cannot_register(self, doctor_sess):
        r = doctor_sess.post(f"{API}/auth/register", json={
            "email": "abc@hosprime.com", "password": "Pass@1234",
            "full_name": "X", "role": "nurse"
        }, timeout=10)
        assert r.status_code == 403

    def test_doctor_cannot_list_users(self, doctor_sess):
        r = doctor_sess.get(f"{API}/auth/users", timeout=10)
        assert r.status_code == 403

    def test_finance_can_list_patients(self, finance_sess):
        r = finance_sess.get(f"{API}/patients", timeout=10)
        assert r.status_code == 200

    def test_finance_cannot_create_patient(self, finance_sess):
        r = finance_sess.post(f"{API}/patients", json={
            "first_name": "TEST", "last_name": "Finance",
            "date_of_birth": "1990-01-01", "gender": "male", "phone": "081"
        }, timeout=10)
        assert r.status_code == 403


# ---------------- PATIENTS ----------------
class TestPatients:
    created_id = None

    def test_create_patient_full(self, admin_sess):
        payload = {
            "first_name": "TEST_ทดสอบ",
            "last_name": f"สกุล_{uuid.uuid4().hex[:6]}",
            "date_of_birth": "1990-05-20", "gender": "male",
            "phone": "081-000-0001", "blood_type": "A+",
            "address": {"street": "1/1", "city": "กรุงเทพ", "state": "กทม", "postal_code": "10110"},
            "emergency_contact": {"name": "EMR", "relationship": "พี่ชาย", "phone": "082"},
            "insurance": {"provider": "สปสช.", "policy_number": "X1", "coverage_type": "ทั่วหน้า"},
            "allergies": [{"allergen": "Penicillin", "severity": "รุนแรง", "reaction": "ผื่น"}]
        }
        r = admin_sess.post(f"{API}/patients", json=payload, timeout=15)
        assert r.status_code == 201, r.text
        data = r.json()
        assert data["patient_number"].startswith("PAT-")
        assert len(data["allergies"]) == 1
        assert data["address"]["city"] == "กรุงเทพ"
        TestPatients.created_id = data["id"]

        # GET verify persistence
        r2 = admin_sess.get(f"{API}/patients/{data['id']}", timeout=10)
        assert r2.status_code == 200
        assert r2.json()["first_name"] == "TEST_ทดสอบ"

    def test_list_with_thai_search(self, admin_sess):
        r = admin_sess.get(f"{API}/patients", params={"search": "สมชาย"}, timeout=10)
        assert r.status_code == 200
        items = r.json()["items"]
        assert any(it["first_name"] == "สมชาย" for it in items)

    def test_list_gender_filter(self, admin_sess):
        r = admin_sess.get(f"{API}/patients", params={"gender": "female"}, timeout=10)
        assert r.status_code == 200
        for it in r.json()["items"]:
            assert it["gender"] == "female"

    def test_list_blood_type_filter(self, admin_sess):
        r = admin_sess.get(f"{API}/patients", params={"blood_type": "O+"}, timeout=10)
        assert r.status_code == 200
        for it in r.json()["items"]:
            assert it["blood_type"] == "O+"

    def test_update_patient(self, admin_sess):
        assert TestPatients.created_id
        r = admin_sess.put(f"{API}/patients/{TestPatients.created_id}",
                            json={"occupation": "วิศวกร"}, timeout=10)
        assert r.status_code == 200
        assert r.json()["occupation"] == "วิศวกร"

    def test_add_vitals(self, admin_sess):
        assert TestPatients.created_id
        r = admin_sess.post(f"{API}/patients/{TestPatients.created_id}/vitals",
                             json={"temperature": 37.2, "bp_systolic": 120, "bp_diastolic": 80,
                                   "heart_rate": 72, "weight": 70.0, "height": 175.0}, timeout=10)
        assert r.status_code == 201
        # verify on GET
        r2 = admin_sess.get(f"{API}/patients/{TestPatients.created_id}", timeout=10)
        assert len(r2.json()["vitals"]) >= 1

    def test_nurse_cannot_delete(self, nurse_sess):
        assert TestPatients.created_id
        r = nurse_sess.delete(f"{API}/patients/{TestPatients.created_id}", timeout=10)
        assert r.status_code == 403

    def test_admin_soft_delete(self, admin_sess):
        assert TestPatients.created_id
        r = admin_sess.delete(f"{API}/patients/{TestPatients.created_id}", timeout=10)
        assert r.status_code == 200
        # not in list
        r2 = admin_sess.get(f"{API}/patients", params={"search": TestPatients.created_id}, timeout=10)
        ids = [it["id"] for it in r2.json()["items"]]
        assert TestPatients.created_id not in ids


# ---------------- APPOINTMENTS ----------------
class TestAppointments:
    apt_id = None

    def test_list_doctors(self, admin_sess):
        r = admin_sess.get(f"{API}/appointments/doctors", timeout=10)
        assert r.status_code == 200
        doctors = r.json()
        assert len(doctors) >= 2

    def test_create_appointment(self, admin_sess):
        # pick a patient and doctor
        patients = admin_sess.get(f"{API}/patients", timeout=10).json()["items"]
        doctors = admin_sess.get(f"{API}/appointments/doctors", timeout=10).json()
        assert patients and doctors
        future = (datetime.now(timezone.utc) + timedelta(days=14)).strftime("%Y-%m-%d")
        payload = {
            "patient_id": patients[0]["id"],
            "doctor_id": doctors[0]["id"],
            "department": doctors[0].get("department", ""),
            "appointment_date": future,
            "appointment_time": "10:00",
            "reason": "TEST appointment"
        }
        r = admin_sess.post(f"{API}/appointments", json=payload, timeout=10)
        assert r.status_code == 201, r.text
        data = r.json()
        assert data["appointment_number"].startswith("APT-")
        assert data["patient_name"]
        assert data["doctor_name"]
        assert data["status"] == "scheduled"
        TestAppointments.apt_id = data["id"]
        TestAppointments._payload = payload

    def test_double_booking_conflict(self, admin_sess):
        # repost same payload
        r = admin_sess.post(f"{API}/appointments", json=TestAppointments._payload, timeout=10)
        assert r.status_code == 409

    def test_list_filter_by_status(self, admin_sess):
        r = admin_sess.get(f"{API}/appointments", params={"status": "scheduled"}, timeout=10)
        assert r.status_code == 200
        for it in r.json()["items"]:
            assert it["status"] == "scheduled"

    def test_status_workflow(self, admin_sess):
        aid = TestAppointments.apt_id
        for s in ["checked_in", "in_progress", "completed"]:
            r = admin_sess.patch(f"{API}/appointments/{aid}/status", json={"status": s}, timeout=10)
            assert r.status_code == 200, f"{s} -> {r.text}"
            assert r.json()["status"] == s

    def test_invalid_status_rejected(self, admin_sess):
        r = admin_sess.patch(f"{API}/appointments/{TestAppointments.apt_id}/status",
                              json={"status": "bogus"}, timeout=10)
        assert r.status_code == 400


# ---------------- DASHBOARD ----------------
class TestDashboard:
    def test_dashboard_stats(self, admin_sess):
        r = admin_sess.get(f"{API}/dashboard/stats", timeout=10)
        assert r.status_code == 200
        data = r.json()
        for k in ["total_patients", "appointments_today", "appointments_trend",
                   "upcoming_appointments", "recent_patients"]:
            assert k in data
        assert isinstance(data["appointments_trend"], list)
        assert len(data["appointments_trend"]) == 7
