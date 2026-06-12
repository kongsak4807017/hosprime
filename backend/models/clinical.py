from typing import List, Optional

from pydantic import BaseModel, Field

# ---------- Pharmacy ----------

class Batch(BaseModel):
    batch_number: str
    expiry_date: str
    quantity: int = 0


class DrugCreate(BaseModel):
    name: str
    generic_name: Optional[str] = ""
    category: str
    dosage_form: str = "Tablet"
    strength: Optional[str] = ""
    unit: Optional[str] = "เม็ด"
    quantity_in_stock: int = 0
    reorder_level: int = 0
    location: Optional[str] = ""
    cost_price: float = 0
    selling_price: float = 0
    batches: List[Batch] = []
    storage_conditions: Optional[str] = ""


class DrugUpdate(BaseModel):
    name: Optional[str] = None
    generic_name: Optional[str] = None
    category: Optional[str] = None
    dosage_form: Optional[str] = None
    strength: Optional[str] = None
    unit: Optional[str] = None
    reorder_level: Optional[int] = None
    location: Optional[str] = None
    cost_price: Optional[float] = None
    selling_price: Optional[float] = None
    storage_conditions: Optional[str] = None


class StockAdjust(BaseModel):
    quantity_change: int
    batch_number: Optional[str] = ""
    expiry_date: Optional[str] = ""
    note: Optional[str] = ""


class PrescriptionMedication(BaseModel):
    drug_id: str
    dosage: Optional[str] = ""
    frequency: Optional[str] = ""
    duration_days: int = 0
    quantity: int = Field(gt=0)
    instructions: Optional[str] = ""


class PrescriptionCreate(BaseModel):
    patient_id: str
    medications: List[PrescriptionMedication] = Field(min_length=1)
    diagnosis: Optional[str] = ""
    notes: Optional[str] = ""


# ---------- Laboratory ----------

class LabOrderCreate(BaseModel):
    patient_id: str
    test_type: str
    priority: str = "routine"
    clinical_notes: Optional[str] = ""


class LabResultValue(BaseModel):
    name: str
    value: str


class LabResultsSubmit(BaseModel):
    parameters: List[LabResultValue] = Field(min_length=1)
    interpretation: Optional[str] = ""
    notes: Optional[str] = ""


# ---------- Billing ----------

class InvoiceLineItem(BaseModel):
    item_type: str = "other"
    description: str
    quantity: int = Field(default=1, gt=0)
    unit_price: float = Field(ge=0)


class InvoiceCreate(BaseModel):
    patient_id: str
    line_items: List[InvoiceLineItem] = Field(min_length=1)
    discount: float = 0
    tax: float = 0
    due_date: Optional[str] = ""
    notes: Optional[str] = ""


class PaymentCreate(BaseModel):
    amount: float = Field(gt=0)
    method: str = "cash"
    reference: Optional[str] = ""


class ClaimCreate(BaseModel):
    provider: str
    claim_amount: float = Field(gt=0)


class ClaimUpdate(BaseModel):
    status: str
    approved_amount: float = 0
