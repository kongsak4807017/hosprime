"""
HosPRIME Phase 2 Backend Tests
Covers: Pharmacy (drugs/prescriptions), Laboratory (catalog/orders/results), Billing (invoices/payments/claims)
"""
import os
import uuid

import pytest
import requests

BASE_URL = os.environ.get("REACT_APP_BACKEND_URL", "").rstrip("/")
API = f"{BASE_URL}/api"

ADMIN = {"email": "admin@hosprime.com", "password": "Admin@1234"}
DOCTOR = {"email": "doctor@hosprime.com", "password": "Test@1234"}
NURSE = {"email": "nurse@hosprime.com", "password": "Test@1234"}
PHARMACIST = {"email": "pharmacist@hosprime.com", "password": "Test@1234"}
LAB_TECH = {"email": "lab@hosprime.com", "password": "Test@1234"}
FINANCE = {"email": "finance@hosprime.com", "password": "Test@1234"}


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
def nurse_s():
    return _login(NURSE)


@pytest.fixture(scope="module")
def pharmacist_s():
    return _login(PHARMACIST)


@pytest.fixture(scope="module")
def lab_s():
    return _login(LAB_TECH)


@pytest.fixture(scope="module")
def finance_s():
    return _login(FINANCE)


@pytest.fixture(scope="module")
def some_patient_id(admin_s):
    r = admin_s.get(f"{API}/patients", timeout=10)
    items = r.json()["items"]
    assert items, "no patients seeded"
    return items[0]["id"]


# ---------- Pharmacy: Drugs ----------
class TestPharmacyDrugs:
    drug_id = None

    def test_list_drugs_seeded(self, admin_s):
        r = admin_s.get(f"{API}/pharmacy/drugs", timeout=10)
        assert r.status_code == 200
        data = r.json()
        assert data["total"] >= 10
        # ensure no _id leaked
        for item in data["items"]:
            assert "_id" not in item

    def test_list_drugs_low_stock_filter(self, admin_s):
        r = admin_s.get(f"{API}/pharmacy/drugs", params={"low_stock": "true"}, timeout=10)
        assert r.status_code == 200
        items = r.json()["items"]
        # Amlodipine in seed should be in low_stock list
        names = [it["name"] for it in items]
        assert any("Amlodipine" in n for n in names), f"Amlodipine not in low_stock list: {names}"
        for it in items:
            assert it["quantity_in_stock"] <= it["reorder_level"]

    def test_drug_search(self, admin_s):
        r = admin_s.get(f"{API}/pharmacy/drugs", params={"search": "Amox"}, timeout=10)
        assert r.status_code == 200
        items = r.json()["items"]
        assert any("Amox" in it["name"] or "Amox" in it.get("generic_name", "") for it in items)

    def test_doctor_cannot_create_drug(self, doctor_s):
        r = doctor_s.post(f"{API}/pharmacy/drugs", json={
            "name": "TEST_Drug_NoAuth", "category": "antibiotic",
            "quantity_in_stock": 10, "reorder_level": 5,
            "cost_price": 1, "selling_price": 2,
        }, timeout=10)
        assert r.status_code == 403

    def test_pharmacist_creates_drug(self, pharmacist_s):
        suffix = uuid.uuid4().hex[:6]
        r = pharmacist_s.post(f"{API}/pharmacy/drugs", json={
            "name": f"TEST_Paracetamol_{suffix}",
            "generic_name": "Paracetamol",
            "category": "analgesic",
            "dosage_form": "Tablet",
            "strength": "500mg",
            "unit": "เม็ด",
            "quantity_in_stock": 500,
            "reorder_level": 100,
            "cost_price": 0.5,
            "selling_price": 1.0,
        }, timeout=10)
        assert r.status_code == 201, r.text
        d = r.json()
        assert d["drug_code"].startswith("DRG-")
        assert d["is_active"] is True
        assert "_id" not in d
        TestPharmacyDrugs.drug_id = d["id"]

    def test_admin_updates_drug(self, admin_s):
        assert TestPharmacyDrugs.drug_id
        r = admin_s.put(f"{API}/pharmacy/drugs/{TestPharmacyDrugs.drug_id}",
                         json={"reorder_level": 200}, timeout=10)
        assert r.status_code == 200
        assert r.json()["reorder_level"] == 200

    def test_stock_adjust_positive_with_batch(self, pharmacist_s):
        assert TestPharmacyDrugs.drug_id
        r = pharmacist_s.post(f"{API}/pharmacy/drugs/{TestPharmacyDrugs.drug_id}/stock", json={
            "quantity_change": 50,
            "batch_number": f"B-{uuid.uuid4().hex[:6]}",
            "expiry_date": "2027-12-31",
            "note": "TEST restock",
        }, timeout=10)
        assert r.status_code == 200
        d = r.json()
        assert d["quantity_in_stock"] == 550
        assert any(b["batch_number"].startswith("B-") for b in d["batches"])

    def test_stock_adjust_negative_beyond_stock(self, pharmacist_s):
        assert TestPharmacyDrugs.drug_id
        r = pharmacist_s.post(f"{API}/pharmacy/drugs/{TestPharmacyDrugs.drug_id}/stock", json={
            "quantity_change": -10_000, "note": "TEST",
        }, timeout=10)
        assert r.status_code == 400
        assert "สต็อก" in r.json()["detail"]

    def test_alerts(self, admin_s):
        r = admin_s.get(f"{API}/pharmacy/alerts", timeout=10)
        assert r.status_code == 200
        data = r.json()
        assert "low_stock" in data and "expiring" in data
        # Amlodipine should be in low_stock
        ls_names = [it["name"] for it in data["low_stock"]]
        assert any("Amlodipine" in n for n in ls_names), ls_names


# ---------- Pharmacy: Prescriptions ----------
class TestPrescriptions:
    pres_id = None
    drug_id = None
    initial_stock = None

    @pytest.fixture(autouse=True)
    def _pickdrug(self, admin_s):
        if TestPrescriptions.drug_id is None:
            r = admin_s.get(f"{API}/pharmacy/drugs",
                            params={"search": "Paracetamol"}, timeout=10)
            items = r.json()["items"]
            # pick a drug with reasonable stock (>10)
            drug = next((d for d in items if d["quantity_in_stock"] > 10), items[0])
            TestPrescriptions.drug_id = drug["id"]
            TestPrescriptions.initial_stock = drug["quantity_in_stock"]

    def test_pharmacist_cannot_create_prescription(self, pharmacist_s):
        r = pharmacist_s.post(f"{API}/pharmacy/prescriptions", json={
            "patient_id": "any",
            "medications": [{"drug_id": "any", "quantity": 1}],
        }, timeout=10)
        assert r.status_code == 403

    def test_doctor_creates_prescription(self, doctor_s, some_patient_id):
        r = doctor_s.post(f"{API}/pharmacy/prescriptions", json={
            "patient_id": some_patient_id,
            "medications": [{
                "drug_id": TestPrescriptions.drug_id,
                "dosage": "1x500mg",
                "frequency": "ทุก 6 ชม.",
                "duration_days": 3,
                "quantity": 5,
                "instructions": "หลังอาหาร",
            }],
            "diagnosis": "TEST headache",
        }, timeout=10)
        assert r.status_code == 201, r.text
        p = r.json()
        assert p["prescription_number"].startswith("PRE-")
        assert p["status"] == "active"
        assert p["medications"][0]["drug_name"]  # denormalized
        TestPrescriptions.pres_id = p["id"]

    def test_pharmacist_dispenses(self, pharmacist_s, admin_s):
        assert TestPrescriptions.pres_id
        # capture stock before
        r0 = admin_s.get(f"{API}/pharmacy/drugs/{TestPrescriptions.drug_id}", timeout=10)
        before = r0.json()["quantity_in_stock"]
        r = pharmacist_s.post(f"{API}/pharmacy/prescriptions/{TestPrescriptions.pres_id}/dispense", timeout=10)
        assert r.status_code == 200, r.text
        d = r.json()
        assert d["status"] == "dispensed"
        assert d["dispensed_by_name"]
        # verify stock decremented by 5
        r2 = admin_s.get(f"{API}/pharmacy/drugs/{TestPrescriptions.drug_id}", timeout=10)
        assert r2.json()["quantity_in_stock"] == before - 5

    def test_dispense_already_dispensed_returns_400(self, pharmacist_s):
        r = pharmacist_s.post(f"{API}/pharmacy/prescriptions/{TestPrescriptions.pres_id}/dispense", timeout=10)
        assert r.status_code == 400

    def test_dispense_exceeds_stock(self, doctor_s, pharmacist_s, some_patient_id, admin_s):
        # create prescription with huge quantity
        r0 = admin_s.get(f"{API}/pharmacy/drugs/{TestPrescriptions.drug_id}", timeout=10)
        cur = r0.json()["quantity_in_stock"]
        r = doctor_s.post(f"{API}/pharmacy/prescriptions", json={
            "patient_id": some_patient_id,
            "medications": [{"drug_id": TestPrescriptions.drug_id, "quantity": cur + 1000}],
        }, timeout=10)
        assert r.status_code == 201
        pres_id = r.json()["id"]
        r2 = pharmacist_s.post(f"{API}/pharmacy/prescriptions/{pres_id}/dispense", timeout=10)
        assert r2.status_code == 400
        assert "ไม่เพียงพอ" in r2.json()["detail"]

    def test_cancel_only_active(self, doctor_s, some_patient_id):
        r = doctor_s.post(f"{API}/pharmacy/prescriptions", json={
            "patient_id": some_patient_id,
            "medications": [{"drug_id": TestPrescriptions.drug_id, "quantity": 1}],
        }, timeout=10)
        assert r.status_code == 201
        pres_id = r.json()["id"]
        r2 = doctor_s.post(f"{API}/pharmacy/prescriptions/{pres_id}/cancel", timeout=10)
        assert r2.status_code == 200
        assert r2.json()["status"] == "cancelled"
        r3 = doctor_s.post(f"{API}/pharmacy/prescriptions/{pres_id}/cancel", timeout=10)
        assert r3.status_code == 400


# ---------- Lab ----------
class TestLab:
    test_id = None

    def test_catalog(self, admin_s):
        r = admin_s.get(f"{API}/lab/catalog", timeout=10)
        assert r.status_code == 200
        data = r.json()
        assert len(data) == 8
        cbc = next((t for t in data if t["test_type"].startswith("CBC")), None)
        assert cbc and any(p["name"] == "Hemoglobin" for p in cbc["parameters"])

    def test_doctor_orders_test(self, doctor_s, some_patient_id):
        r = doctor_s.post(f"{API}/lab/tests", json={
            "patient_id": some_patient_id,
            "test_type": "CBC (Complete Blood Count)",
            "priority": "routine",
            "clinical_notes": "TEST",
        }, timeout=10)
        assert r.status_code == 201, r.text
        t = r.json()
        assert t["test_number"].startswith("LAB-")
        assert t["status"] == "ordered"
        TestLab.test_id = t["id"]

    def test_nurse_cannot_order(self, nurse_s, some_patient_id):
        r = nurse_s.post(f"{API}/lab/tests", json={
            "patient_id": some_patient_id,
            "test_type": "CBC (Complete Blood Count)",
        }, timeout=10)
        assert r.status_code == 403

    def test_lab_collect_sample(self, lab_s):
        assert TestLab.test_id
        r = lab_s.post(f"{API}/lab/tests/{TestLab.test_id}/collect", timeout=10)
        assert r.status_code == 200, r.text
        t = r.json()
        assert t["status"] == "sample_collected"
        assert t["sample"]["sample_id"].startswith("SMP-")

    def test_collect_twice_400(self, lab_s):
        r = lab_s.post(f"{API}/lab/tests/{TestLab.test_id}/collect", timeout=10)
        assert r.status_code == 400

    def test_submit_results_with_abnormal(self, lab_s):
        assert TestLab.test_id
        r = lab_s.post(f"{API}/lab/tests/{TestLab.test_id}/results", json={
            "parameters": [
                {"name": "WBC", "value": "7.0"},
                {"name": "RBC", "value": "5.0"},
                {"name": "Hemoglobin", "value": "8"},      # < 12 abnormal
                {"name": "Hematocrit", "value": "40"},
                {"name": "Platelets", "value": "200"},
            ],
            "interpretation": "TEST anemia",
        }, timeout=10)
        assert r.status_code == 200, r.text
        t = r.json()
        assert t["status"] == "completed"
        params = {p["name"]: p for p in t["results"]["parameters"]}
        assert params["Hemoglobin"]["is_abnormal"] is True
        assert params["WBC"]["is_abnormal"] is False
        assert t["results"]["has_abnormal"] is True

    def test_results_on_ordered_400(self, doctor_s, lab_s, some_patient_id):
        r = doctor_s.post(f"{API}/lab/tests", json={
            "patient_id": some_patient_id,
            "test_type": "FBS (Fasting Blood Sugar)",
        }, timeout=10)
        tid = r.json()["id"]
        r2 = lab_s.post(f"{API}/lab/tests/{tid}/results", json={
            "parameters": [{"name": "Glucose", "value": "90"}],
        }, timeout=10)
        assert r2.status_code == 400

    def test_cancel_completed_rejected(self, doctor_s):
        assert TestLab.test_id
        r = doctor_s.post(f"{API}/lab/tests/{TestLab.test_id}/cancel", timeout=10)
        assert r.status_code == 400


# ---------- Billing ----------
class TestBilling:
    inv_id = None
    inv_id_for_claim = None

    def test_doctor_cannot_create_invoice(self, doctor_s, some_patient_id):
        r = doctor_s.post(f"{API}/billing/invoices", json={
            "patient_id": some_patient_id,
            "line_items": [{"description": "X", "quantity": 1, "unit_price": 100}],
        }, timeout=10)
        assert r.status_code == 403

    def test_finance_creates_invoice(self, finance_s, some_patient_id):
        r = finance_s.post(f"{API}/billing/invoices", json={
            "patient_id": some_patient_id,
            "line_items": [
                {"item_type": "consult", "description": "ค่าตรวจ", "quantity": 1, "unit_price": 500},
                {"item_type": "drug", "description": "ยา", "quantity": 2, "unit_price": 100},
            ],
            "discount": 0, "tax": 0,
        }, timeout=10)
        assert r.status_code == 201, r.text
        inv = r.json()
        assert inv["invoice_number"].startswith("INV-")
        assert inv["status"] == "pending"
        assert inv["subtotal"] == 700.0
        assert inv["total_amount"] == 700.0
        assert inv["balance"] == 700.0
        # line item totals computed server-side
        line_totals = [li["total"] for li in inv["line_items"]]
        assert line_totals == [500.0, 200.0]
        TestBilling.inv_id = inv["id"]

    def test_partial_payment(self, finance_s):
        assert TestBilling.inv_id
        r = finance_s.post(f"{API}/billing/invoices/{TestBilling.inv_id}/payments",
                           json={"amount": 300, "method": "cash"}, timeout=10)
        assert r.status_code == 200, r.text
        d = r.json()
        assert d["status"] == "partially_paid"
        assert d["paid_amount"] == 300.0
        assert d["balance"] == 400.0

    def test_pay_full_balance(self, finance_s):
        r = finance_s.post(f"{API}/billing/invoices/{TestBilling.inv_id}/payments",
                           json={"amount": 400, "method": "card"}, timeout=10)
        assert r.status_code == 200, r.text
        d = r.json()
        assert d["status"] == "paid"
        assert d["balance"] == 0.0

    def test_payment_on_paid_400(self, finance_s):
        r = finance_s.post(f"{API}/billing/invoices/{TestBilling.inv_id}/payments",
                           json={"amount": 10, "method": "cash"}, timeout=10)
        assert r.status_code == 400

    def test_overpay_400(self, finance_s, some_patient_id):
        r = finance_s.post(f"{API}/billing/invoices", json={
            "patient_id": some_patient_id,
            "line_items": [{"description": "X", "quantity": 1, "unit_price": 100}],
        }, timeout=10)
        inv_id = r.json()["id"]
        r2 = finance_s.post(f"{API}/billing/invoices/{inv_id}/payments",
                            json={"amount": 200, "method": "cash"}, timeout=10)
        assert r2.status_code == 400
        assert "ค้างชำระ" in r2.json()["detail"] or "เกิน" in r2.json()["detail"]

    def test_claim_flow(self, finance_s, some_patient_id):
        r = finance_s.post(f"{API}/billing/invoices", json={
            "patient_id": some_patient_id,
            "line_items": [{"description": "Y", "quantity": 1, "unit_price": 1000}],
        }, timeout=10)
        inv_id = r.json()["id"]
        TestBilling.inv_id_for_claim = inv_id

        # submit claim
        r2 = finance_s.post(f"{API}/billing/invoices/{inv_id}/claim",
                            json={"provider": "TEST_Insurance", "claim_amount": 800}, timeout=10)
        assert r2.status_code == 200
        d = r2.json()
        assert d["insurance_claim"]["status"] == "submitted"
        assert d["insurance_claim"]["claim_id"].startswith("CLM-")

        # duplicate claim 400
        r3 = finance_s.post(f"{API}/billing/invoices/{inv_id}/claim",
                            json={"provider": "X", "claim_amount": 100}, timeout=10)
        assert r3.status_code == 400

        # update claim to approved
        r4 = finance_s.patch(f"{API}/billing/invoices/{inv_id}/claim",
                              json={"status": "approved", "approved_amount": 750}, timeout=10)
        assert r4.status_code == 200
        assert r4.json()["insurance_claim"]["status"] == "approved"
        assert r4.json()["insurance_claim"]["approved_amount"] == 750.0

    def test_cancel_only_pending_no_payments(self, finance_s, some_patient_id):
        # cancel paid invoice -> 400
        r = finance_s.post(f"{API}/billing/invoices/{TestBilling.inv_id}/cancel", timeout=10)
        assert r.status_code == 400

        # cancel partially_paid -> 400
        r2 = finance_s.post(f"{API}/billing/invoices", json={
            "patient_id": some_patient_id,
            "line_items": [{"description": "Z", "quantity": 1, "unit_price": 500}],
        }, timeout=10)
        inv_id = r2.json()["id"]
        finance_s.post(f"{API}/billing/invoices/{inv_id}/payments",
                       json={"amount": 100, "method": "cash"}, timeout=10)
        r3 = finance_s.post(f"{API}/billing/invoices/{inv_id}/cancel", timeout=10)
        assert r3.status_code == 400

        # cancel pending with no payment -> 200
        r4 = finance_s.post(f"{API}/billing/invoices", json={
            "patient_id": some_patient_id,
            "line_items": [{"description": "W", "quantity": 1, "unit_price": 50}],
        }, timeout=10)
        cancel_id = r4.json()["id"]
        r5 = finance_s.post(f"{API}/billing/invoices/{cancel_id}/cancel", timeout=10)
        assert r5.status_code == 200
        assert r5.json()["status"] == "cancelled"

    def test_stats_changes_after_payment(self, finance_s, some_patient_id):
        before = finance_s.get(f"{API}/billing/stats", timeout=10).json()
        for k in ["revenue_today", "revenue_month", "outstanding", "pending_invoices"]:
            assert k in before
        # create invoice and pay
        r = finance_s.post(f"{API}/billing/invoices", json={
            "patient_id": some_patient_id,
            "line_items": [{"description": "STATS_TEST", "quantity": 1, "unit_price": 123}],
        }, timeout=10)
        inv_id = r.json()["id"]
        finance_s.post(f"{API}/billing/invoices/{inv_id}/payments",
                       json={"amount": 123, "method": "cash"}, timeout=10)
        after = finance_s.get(f"{API}/billing/stats", timeout=10).json()
        assert after["revenue_today"] >= before["revenue_today"] + 123 - 0.01
