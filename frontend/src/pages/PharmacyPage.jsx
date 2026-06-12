import { useCallback, useEffect, useState } from "react";
import { Plus, Search, Trash2, PackagePlus, AlertTriangle, CalendarX2 } from "lucide-react";
import { toast } from "sonner";
import api, { formatApiError } from "@/lib/api";
import { useAuth } from "@/context/AuthContext";
import {
  PRESCRIPTION_STATUS_LABELS, PRESCRIPTION_STATUS_BADGES, DRUG_CATEGORIES,
} from "@/lib/constants";
import { formatTHB, formatThaiDate, formatThaiDateTime, isExpiringSoon } from "@/lib/helpers";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle,
} from "@/components/ui/dialog";

const inputCls =
  "w-full border border-[#E1E5E2] bg-white rounded-lg px-3 py-2 text-sm focus:border-[#1E3F33] focus:ring-1 focus:ring-[#1E3F33] focus:outline-none";

const PRESCRIBE_ROLES = ["admin", "doctor"];
const DISPENSE_ROLES = ["admin", "pharmacist"];
const DRUG_WRITE_ROLES = ["admin", "pharmacist"];

const thCls = "px-4 py-3 font-semibold";
const theadCls = "text-left text-xs uppercase tracking-wider text-[#546E62] border-b border-[#E1E5E2] bg-[#F2F0EB]/50";

// ============ Prescriptions Tab ============
function PrescriptionsTab() {
  const { user } = useAuth();
  const [data, setData] = useState({ items: [], total: 0 });
  const [status, setStatus] = useState("");
  const [search, setSearch] = useState("");
  const [createOpen, setCreateOpen] = useState(false);
  const [viewItem, setViewItem] = useState(null);
  const [patients, setPatients] = useState([]);
  const [drugs, setDrugs] = useState([]);
  const [form, setForm] = useState({ patient_id: "", diagnosis: "", notes: "", medications: [{ drug_id: "", dosage: "", frequency: "", duration_days: "", quantity: "" }] });
  const [saving, setSaving] = useState(false);

  const fetch_ = useCallback(() => {
    api.get("/pharmacy/prescriptions", { params: { status, search, limit: 30 } }).then((r) => setData(r.data));
  }, [status, search]);

  useEffect(() => { const t = setTimeout(fetch_, search ? 350 : 0); return () => clearTimeout(t); }, [fetch_, search]);

  useEffect(() => {
    if (!createOpen) return;
    api.get("/patients", { params: { limit: 100 } }).then((r) => setPatients(r.data.items));
    api.get("/pharmacy/drugs", { params: { limit: 100 } }).then((r) => setDrugs(r.data.items));
  }, [createOpen]);

  const setMed = (i, field, val) => setForm((f) => ({ ...f, medications: f.medications.map((m, idx) => (idx === i ? { ...m, [field]: val } : m)) }));

  const submit = async (e) => {
    e.preventDefault();
    setSaving(true);
    try {
      const payload = {
        ...form,
        medications: form.medications.map((m) => ({ ...m, duration_days: Number(m.duration_days) || 0, quantity: Number(m.quantity) })),
      };
      await api.post("/pharmacy/prescriptions", payload);
      toast.success("สั่งยาสำเร็จ");
      setCreateOpen(false);
      setForm({ patient_id: "", diagnosis: "", notes: "", medications: [{ drug_id: "", dosage: "", frequency: "", duration_days: "", quantity: "" }] });
      fetch_();
    } catch (err) { toast.error(formatApiError(err)); } finally { setSaving(false); }
  };

  const dispense = async (id) => {
    try {
      await api.post(`/pharmacy/prescriptions/${id}/dispense`);
      toast.success("จ่ายยาสำเร็จ ตัดสต็อกเรียบร้อย");
      fetch_();
    } catch (err) { toast.error(formatApiError(err)); }
  };

  const cancel = async (id) => {
    if (!window.confirm("ยืนยันการยกเลิกใบสั่งยานี้?")) return;
    try {
      await api.post(`/pharmacy/prescriptions/${id}/cancel`);
      toast.success("ยกเลิกใบสั่งยาสำเร็จ");
      fetch_();
    } catch (err) { toast.error(formatApiError(err)); }
  };

  return (
    <div className="space-y-4">
      <div className="flex flex-col md:flex-row gap-3">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[#546E62]" />
          <input value={search} onChange={(e) => setSearch(e.target.value)} placeholder="ค้นหาใบสั่งยา, ชื่อผู้ป่วย..." data-testid="prescription-search-input" className={`${inputCls} pl-10`} />
        </div>
        <select value={status} onChange={(e) => setStatus(e.target.value)} data-testid="prescription-status-filter" className="border border-[#E1E5E2] bg-white rounded-lg px-4 py-2 text-sm focus:outline-none">
          <option value="">สถานะทั้งหมด</option>
          {Object.entries(PRESCRIPTION_STATUS_LABELS).map(([k, v]) => <option key={k} value={k}>{v}</option>)}
        </select>
        {PRESCRIBE_ROLES.includes(user?.role) && (
          <button onClick={() => setCreateOpen(true)} data-testid="create-prescription-btn" className="inline-flex items-center gap-2 bg-[#1E3F33] text-white hover:bg-[#2C5A48] rounded-lg px-4 py-2 text-sm font-medium transition-colors">
            <Plus className="w-4 h-4" /> สั่งยาใหม่
          </button>
        )}
      </div>

      <div className="bg-white border border-[#E1E5E2] rounded-lg shadow-sm overflow-x-auto">
        <table className="w-full text-sm">
          <thead><tr className={theadCls}>
            <th className={thCls}>เลขที่</th><th className={thCls}>ผู้ป่วย</th><th className={thCls}>แพทย์</th>
            <th className={thCls}>การวินิจฉัย</th><th className={thCls}>รายการยา</th><th className={thCls}>สถานะ</th><th className={thCls}>จัดการ</th>
          </tr></thead>
          <tbody>
            {data.items.length === 0 && <tr><td colSpan={7} className="px-4 py-8 text-center text-[#546E62]" data-testid="prescriptions-empty">ไม่พบใบสั่งยา</td></tr>}
            {data.items.map((p) => (
              <tr key={p.id} data-testid="prescription-row" className="border-b border-[#E1E5E2] last:border-0 hover:bg-[#F2F0EB]/50">
                <td className="px-4 py-3 font-mono text-xs text-[#1E3F33] font-semibold">{p.prescription_number}</td>
                <td className="px-4 py-3 font-medium">{p.patient_name}</td>
                <td className="px-4 py-3">{p.doctor_name}</td>
                <td className="px-4 py-3 max-w-[180px] truncate text-[#546E62]">{p.diagnosis || "-"}</td>
                <td className="px-4 py-3">{p.medications.length} รายการ</td>
                <td className="px-4 py-3"><span className={`text-xs rounded-full px-2.5 py-1 font-medium ${PRESCRIPTION_STATUS_BADGES[p.status]}`}>{PRESCRIPTION_STATUS_LABELS[p.status]}</span></td>
                <td className="px-4 py-3">
                  <div className="flex gap-2">
                    <button onClick={() => setViewItem(p)} data-testid="view-prescription-btn" className="text-xs border border-[#E1E5E2] rounded-lg px-2.5 py-1 bg-white hover:bg-[#F2F0EB]">ดู</button>
                    {p.status === "active" && DISPENSE_ROLES.includes(user?.role) && (
                      <button onClick={() => dispense(p.id)} data-testid="dispense-btn" className="text-xs bg-[#1E3F33] text-white rounded-lg px-2.5 py-1 hover:bg-[#2C5A48]">จ่ายยา</button>
                    )}
                    {p.status === "active" && PRESCRIBE_ROLES.includes(user?.role) && (
                      <button onClick={() => cancel(p.id)} className="text-xs border border-[#D34228]/30 text-[#D34228] rounded-lg px-2.5 py-1 hover:bg-[#D34228]/5">ยกเลิก</button>
                    )}
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Create prescription dialog */}
      <Dialog open={createOpen} onOpenChange={setCreateOpen}>
        <DialogContent className="max-w-2xl max-h-[85vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle className="font-heading">สั่งยาใหม่</DialogTitle>
            <DialogDescription>เลือกผู้ป่วยและรายการยาจากคลัง</DialogDescription>
          </DialogHeader>
          <form onSubmit={submit} className="space-y-3" data-testid="prescription-form">
            <div>
              <label className="text-xs text-[#546E62]">ผู้ป่วย *</label>
              <select required value={form.patient_id} onChange={(e) => setForm({ ...form, patient_id: e.target.value })} className={inputCls} data-testid="prescription-patient-select">
                <option value="">เลือกผู้ป่วย</option>
                {patients.map((p) => <option key={p.id} value={p.id}>{`${p.patient_number} — ${p.first_name} ${p.last_name}`}</option>)}
              </select>
            </div>
            <div>
              <label className="text-xs text-[#546E62]">การวินิจฉัย</label>
              <input value={form.diagnosis} onChange={(e) => setForm({ ...form, diagnosis: e.target.value })} className={inputCls} data-testid="prescription-diagnosis-input" />
            </div>
            <div className="space-y-3">
              <label className="text-xs font-semibold text-[#0F1F19]">รายการยา *</label>
              {form.medications.map((m, i) => (
                <div key={i} className="border border-[#E1E5E2] rounded-lg p-3 space-y-2 bg-[#F9F9F8]">
                  <div className="flex gap-2">
                    <select required value={m.drug_id} onChange={(e) => setMed(i, "drug_id", e.target.value)} className={inputCls} data-testid={`prescription-drug-select-${i}`}>
                      <option value="">เลือกยา</option>
                      {drugs.map((d) => <option key={d.id} value={d.id}>{`${d.name} (คงเหลือ ${d.quantity_in_stock})`}</option>)}
                    </select>
                    {form.medications.length > 1 && (
                      <button type="button" onClick={() => setForm((f) => ({ ...f, medications: f.medications.filter((_, idx) => idx !== i) }))} className="p-2 text-[#D34228] hover:bg-[#D34228]/10 rounded-lg"><Trash2 className="w-4 h-4" /></button>
                    )}
                  </div>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
                    <input value={m.dosage} onChange={(e) => setMed(i, "dosage", e.target.value)} placeholder="ขนาด เช่น 1 เม็ด" className={inputCls} />
                    <input value={m.frequency} onChange={(e) => setMed(i, "frequency", e.target.value)} placeholder="วันละ 2 ครั้ง" className={inputCls} />
                    <input type="number" min="0" value={m.duration_days} onChange={(e) => setMed(i, "duration_days", e.target.value)} placeholder="จำนวนวัน" className={inputCls} />
                    <input type="number" min="1" required value={m.quantity} onChange={(e) => setMed(i, "quantity", e.target.value)} placeholder="จำนวน *" className={inputCls} data-testid={`prescription-quantity-input-${i}`} />
                  </div>
                </div>
              ))}
              <button type="button" onClick={() => setForm((f) => ({ ...f, medications: [...f.medications, { drug_id: "", dosage: "", frequency: "", duration_days: "", quantity: "" }] }))} className="inline-flex items-center gap-2 text-sm text-[#1E3F33] font-medium hover:underline">
                <Plus className="w-4 h-4" /> เพิ่มรายการยา
              </button>
            </div>
            <div>
              <label className="text-xs text-[#546E62]">หมายเหตุ</label>
              <textarea rows={2} value={form.notes} onChange={(e) => setForm({ ...form, notes: e.target.value })} className={inputCls} />
            </div>
            <button type="submit" disabled={saving} data-testid="prescription-submit-btn" className="w-full bg-[#1E3F33] text-white hover:bg-[#2C5A48] rounded-lg py-2.5 font-medium transition-colors disabled:opacity-60">
              {saving ? "กำลังบันทึก..." : "ยืนยันสั่งยา"}
            </button>
          </form>
        </DialogContent>
      </Dialog>

      {/* View prescription dialog */}
      <Dialog open={!!viewItem} onOpenChange={(o) => !o && setViewItem(null)}>
        <DialogContent className="max-w-lg">
          <DialogHeader>
            <DialogTitle className="font-heading">{viewItem?.prescription_number}</DialogTitle>
            <DialogDescription>{viewItem?.patient_name} • {viewItem?.doctor_name}</DialogDescription>
          </DialogHeader>
          {viewItem && (
            <div className="space-y-3 text-sm" data-testid="prescription-detail">
              <div><span className="text-[#546E62]">การวินิจฉัย:</span> <span className="font-medium">{viewItem.diagnosis || "-"}</span></div>
              <div className="border border-[#E1E5E2] rounded-lg divide-y divide-[#E1E5E2]">
                {viewItem.medications.map((m, i) => (
                  <div key={i} className="p-3">
                    <div className="font-medium">{m.drug_name}</div>
                    <div className="text-xs text-[#546E62]">{m.dosage} • {m.frequency} {m.duration_days ? `• ${m.duration_days} วัน` : ""} • จำนวน {m.quantity} {m.instructions && `• ${m.instructions}`}</div>
                  </div>
                ))}
              </div>
              <div className="flex justify-between text-xs text-[#546E62]">
                <span>สั่งเมื่อ {formatThaiDateTime(viewItem.issued_at)}</span>
                {viewItem.dispensed_by_name && <span>จ่ายโดย {viewItem.dispensed_by_name}</span>}
              </div>
            </div>
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
}

// ============ Drugs (Inventory) Tab ============
const EMPTY_DRUG = { name: "", generic_name: "", category: "ยาแก้ปวด", dosage_form: "Tablet", strength: "", unit: "เม็ด", quantity_in_stock: "", reorder_level: "", location: "", cost_price: "", selling_price: "" };

function DrugsTab() {
  const { user } = useAuth();
  const [data, setData] = useState({ items: [], total: 0 });
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("");
  const [lowStock, setLowStock] = useState(false);
  const [formOpen, setFormOpen] = useState(false);
  const [editId, setEditId] = useState(null);
  const [form, setForm] = useState(EMPTY_DRUG);
  const [stockItem, setStockItem] = useState(null);
  const [stockForm, setStockForm] = useState({ quantity_change: "", batch_number: "", expiry_date: "", note: "" });
  const [saving, setSaving] = useState(false);

  const canWrite = DRUG_WRITE_ROLES.includes(user?.role);

  const fetch_ = useCallback(() => {
    api.get("/pharmacy/drugs", { params: { search, category, low_stock: lowStock, limit: 50 } }).then((r) => setData(r.data));
  }, [search, category, lowStock]);

  useEffect(() => { const t = setTimeout(fetch_, search ? 350 : 0); return () => clearTimeout(t); }, [fetch_, search]);

  const openCreate = () => { setEditId(null); setForm(EMPTY_DRUG); setFormOpen(true); };
  const openEdit = (d) => {
    setEditId(d.id);
    setForm({ name: d.name, generic_name: d.generic_name, category: d.category, dosage_form: d.dosage_form, strength: d.strength, unit: d.unit, quantity_in_stock: d.quantity_in_stock, reorder_level: d.reorder_level, location: d.location, cost_price: d.cost_price, selling_price: d.selling_price });
    setFormOpen(true);
  };

  const submit = async (e) => {
    e.preventDefault();
    setSaving(true);
    try {
      const payload = {
        ...form,
        quantity_in_stock: Number(form.quantity_in_stock) || 0,
        reorder_level: Number(form.reorder_level) || 0,
        cost_price: Number(form.cost_price) || 0,
        selling_price: Number(form.selling_price) || 0,
      };
      if (editId) {
        delete payload.quantity_in_stock;
        await api.put(`/pharmacy/drugs/${editId}`, payload);
        toast.success("แก้ไขข้อมูลยาสำเร็จ");
      } else {
        await api.post("/pharmacy/drugs", payload);
        toast.success("เพิ่มยาใหม่สำเร็จ");
      }
      setFormOpen(false);
      fetch_();
    } catch (err) { toast.error(formatApiError(err)); } finally { setSaving(false); }
  };

  const submitStock = async (e) => {
    e.preventDefault();
    setSaving(true);
    try {
      await api.post(`/pharmacy/drugs/${stockItem.id}/stock`, { ...stockForm, quantity_change: Number(stockForm.quantity_change) });
      toast.success("ปรับสต็อกสำเร็จ");
      setStockItem(null);
      setStockForm({ quantity_change: "", batch_number: "", expiry_date: "", note: "" });
      fetch_();
    } catch (err) { toast.error(formatApiError(err)); } finally { setSaving(false); }
  };

  const nearestExpiry = (d) => {
    const dates = (d.batches || []).filter((b) => b.expiry_date && b.quantity > 0).map((b) => b.expiry_date).sort();
    return dates[0] || "";
  };

  return (
    <div className="space-y-4">
      <div className="flex flex-col md:flex-row gap-3">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[#546E62]" />
          <input value={search} onChange={(e) => setSearch(e.target.value)} placeholder="ค้นหายา, รหัสยา..." data-testid="drug-search-input" className={`${inputCls} pl-10`} />
        </div>
        <select value={category} onChange={(e) => setCategory(e.target.value)} className="border border-[#E1E5E2] bg-white rounded-lg px-4 py-2 text-sm focus:outline-none" data-testid="drug-category-filter">
          <option value="">หมวดยาทั้งหมด</option>
          {DRUG_CATEGORIES.map((c) => <option key={c} value={c}>{c}</option>)}
        </select>
        <label className="flex items-center gap-2 text-sm text-[#0F1F19] border border-[#E1E5E2] bg-white rounded-lg px-4 py-2 cursor-pointer">
          <input type="checkbox" checked={lowStock} onChange={(e) => setLowStock(e.target.checked)} data-testid="drug-lowstock-filter" />
          ใกล้หมดสต็อก
        </label>
        {canWrite && (
          <button onClick={openCreate} data-testid="add-drug-btn" className="inline-flex items-center gap-2 bg-[#1E3F33] text-white hover:bg-[#2C5A48] rounded-lg px-4 py-2 text-sm font-medium transition-colors">
            <Plus className="w-4 h-4" /> เพิ่มยาใหม่
          </button>
        )}
      </div>

      <div className="bg-white border border-[#E1E5E2] rounded-lg shadow-sm overflow-x-auto">
        <table className="w-full text-sm">
          <thead><tr className={theadCls}>
            <th className={thCls}>รหัส</th><th className={thCls}>ชื่อยา</th><th className={thCls}>หมวด</th>
            <th className={thCls}>รูปแบบ</th><th className={thCls}>คงเหลือ</th><th className={thCls}>หมดอายุใกล้สุด</th>
            <th className={thCls}>ราคาขาย</th>{canWrite && <th className={thCls}>จัดการ</th>}
          </tr></thead>
          <tbody>
            {data.items.length === 0 && <tr><td colSpan={8} className="px-4 py-8 text-center text-[#546E62]">ไม่พบรายการยา</td></tr>}
            {data.items.map((d) => {
              const low = d.quantity_in_stock <= d.reorder_level;
              const exp = nearestExpiry(d);
              return (
                <tr key={d.id} data-testid="drug-row" className="border-b border-[#E1E5E2] last:border-0 hover:bg-[#F2F0EB]/50">
                  <td className="px-4 py-3 font-mono text-xs text-[#1E3F33] font-semibold">{d.drug_code}</td>
                  <td className="px-4 py-3">
                    <div className="font-medium">{d.name}</div>
                    <div className="text-xs text-[#546E62]">{d.generic_name}</div>
                  </td>
                  <td className="px-4 py-3">{d.category}</td>
                  <td className="px-4 py-3 text-xs">{d.dosage_form} {d.strength}</td>
                  <td className="px-4 py-3">
                    <span className={`font-semibold ${low ? "text-[#D34228]" : "text-[#0F1F19]"}`}>{d.quantity_in_stock.toLocaleString()}</span>
                    {low && <span className="ml-2 text-[10px] bg-[#D34228]/10 text-[#D34228] rounded-full px-2 py-0.5" data-testid="lowstock-badge">ใกล้หมด</span>}
                  </td>
                  <td className="px-4 py-3">
                    {exp ? (
                      <span className={isExpiringSoon(exp) ? "text-[#D34228] font-medium" : "text-[#546E62]"}>
                        {formatThaiDate(exp)}
                        {isExpiringSoon(exp) && <span className="ml-1 text-[10px] bg-[#E5A732]/15 text-[#9c7016] rounded-full px-2 py-0.5">ใกล้หมดอายุ</span>}
                      </span>
                    ) : "-"}
                  </td>
                  <td className="px-4 py-3">{formatTHB(d.selling_price)}</td>
                  {canWrite && (
                    <td className="px-4 py-3">
                      <div className="flex gap-2">
                        <button onClick={() => openEdit(d)} data-testid="edit-drug-btn" className="text-xs border border-[#E1E5E2] rounded-lg px-2.5 py-1 bg-white hover:bg-[#F2F0EB]">แก้ไข</button>
                        <button onClick={() => setStockItem(d)} data-testid="adjust-stock-btn" className="text-xs bg-[#4A6B5D] text-white rounded-lg px-2.5 py-1 hover:bg-[#2C5A48] inline-flex items-center gap-1"><PackagePlus className="w-3 h-3" /> สต็อก</button>
                      </div>
                    </td>
                  )}
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {/* Drug form dialog */}
      <Dialog open={formOpen} onOpenChange={setFormOpen}>
        <DialogContent className="max-w-lg max-h-[85vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle className="font-heading">{editId ? "แก้ไขข้อมูลยา" : "เพิ่มยาใหม่"}</DialogTitle>
            <DialogDescription>ข้อมูลยาในคลังเภสัชกรรม</DialogDescription>
          </DialogHeader>
          <form onSubmit={submit} className="grid grid-cols-2 gap-3" data-testid="drug-form">
            <div className="col-span-2">
              <label className="text-xs text-[#546E62]">ชื่อยา *</label>
              <input required value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} className={inputCls} data-testid="drug-name-input" />
            </div>
            <div>
              <label className="text-xs text-[#546E62]">ชื่อสามัญ</label>
              <input value={form.generic_name} onChange={(e) => setForm({ ...form, generic_name: e.target.value })} className={inputCls} />
            </div>
            <div>
              <label className="text-xs text-[#546E62]">หมวดยา *</label>
              <select value={form.category} onChange={(e) => setForm({ ...form, category: e.target.value })} className={inputCls}>
                {DRUG_CATEGORIES.map((c) => <option key={c} value={c}>{c}</option>)}
              </select>
            </div>
            <div>
              <label className="text-xs text-[#546E62]">รูปแบบ</label>
              <select value={form.dosage_form} onChange={(e) => setForm({ ...form, dosage_form: e.target.value })} className={inputCls}>
                {["Tablet", "Capsule", "Syrup", "Injection", "Cream", "Inhaler"].map((f) => <option key={f} value={f}>{f}</option>)}
              </select>
            </div>
            <div>
              <label className="text-xs text-[#546E62]">ความแรง</label>
              <input value={form.strength} onChange={(e) => setForm({ ...form, strength: e.target.value })} placeholder="เช่น 500 mg" className={inputCls} />
            </div>
            {!editId && (
              <div>
                <label className="text-xs text-[#546E62]">จำนวนเริ่มต้น</label>
                <input type="number" min="0" value={form.quantity_in_stock} onChange={(e) => setForm({ ...form, quantity_in_stock: e.target.value })} className={inputCls} data-testid="drug-stock-input" />
              </div>
            )}
            <div>
              <label className="text-xs text-[#546E62]">จุดสั่งซื้อ (Reorder)</label>
              <input type="number" min="0" value={form.reorder_level} onChange={(e) => setForm({ ...form, reorder_level: e.target.value })} className={inputCls} />
            </div>
            <div>
              <label className="text-xs text-[#546E62]">ราคาทุน (บาท)</label>
              <input type="number" min="0" step="0.01" value={form.cost_price} onChange={(e) => setForm({ ...form, cost_price: e.target.value })} className={inputCls} />
            </div>
            <div>
              <label className="text-xs text-[#546E62]">ราคาขาย (บาท)</label>
              <input type="number" min="0" step="0.01" value={form.selling_price} onChange={(e) => setForm({ ...form, selling_price: e.target.value })} className={inputCls} />
            </div>
            <div>
              <label className="text-xs text-[#546E62]">ตำแหน่งจัดเก็บ</label>
              <input value={form.location} onChange={(e) => setForm({ ...form, location: e.target.value })} className={inputCls} />
            </div>
            <div className="col-span-2">
              <button type="submit" disabled={saving} data-testid="drug-submit-btn" className="w-full bg-[#1E3F33] text-white hover:bg-[#2C5A48] rounded-lg py-2.5 font-medium transition-colors disabled:opacity-60">
                {saving ? "กำลังบันทึก..." : "บันทึก"}
              </button>
            </div>
          </form>
        </DialogContent>
      </Dialog>

      {/* Stock adjust dialog */}
      <Dialog open={!!stockItem} onOpenChange={(o) => !o && setStockItem(null)}>
        <DialogContent className="max-w-md">
          <DialogHeader>
            <DialogTitle className="font-heading">ปรับสต็อก: {stockItem?.name}</DialogTitle>
            <DialogDescription>คงเหลือปัจจุบัน {stockItem?.quantity_in_stock?.toLocaleString()} {stockItem?.unit}</DialogDescription>
          </DialogHeader>
          <form onSubmit={submitStock} className="space-y-3" data-testid="stock-form">
            <div>
              <label className="text-xs text-[#546E62]">จำนวน (+ รับเข้า / - เบิกออก) *</label>
              <input type="number" required value={stockForm.quantity_change} onChange={(e) => setStockForm({ ...stockForm, quantity_change: e.target.value })} placeholder="เช่น 500 หรือ -50" className={inputCls} data-testid="stock-quantity-input" />
            </div>
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="text-xs text-[#546E62]">เลข Batch (กรณีรับเข้า)</label>
                <input value={stockForm.batch_number} onChange={(e) => setStockForm({ ...stockForm, batch_number: e.target.value })} className={inputCls} />
              </div>
              <div>
                <label className="text-xs text-[#546E62]">วันหมดอายุ</label>
                <input type="date" value={stockForm.expiry_date} onChange={(e) => setStockForm({ ...stockForm, expiry_date: e.target.value })} className={inputCls} />
              </div>
            </div>
            <div>
              <label className="text-xs text-[#546E62]">หมายเหตุ</label>
              <input value={stockForm.note} onChange={(e) => setStockForm({ ...stockForm, note: e.target.value })} className={inputCls} />
            </div>
            <button type="submit" disabled={saving} data-testid="stock-submit-btn" className="w-full bg-[#1E3F33] text-white hover:bg-[#2C5A48] rounded-lg py-2.5 font-medium transition-colors disabled:opacity-60">
              ยืนยันปรับสต็อก
            </button>
          </form>
        </DialogContent>
      </Dialog>
    </div>
  );
}

// ============ Alerts Tab ============
function AlertsTab() {
  const [alerts, setAlerts] = useState({ low_stock: [], expiring: [], horizon_days: 90 });

  useEffect(() => {
    api.get("/pharmacy/alerts").then((r) => setAlerts(r.data));
  }, []);

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 md:gap-6">
      <div className="bg-white border border-[#E1E5E2] rounded-lg p-5 shadow-sm" data-testid="lowstock-alerts">
        <h3 className="font-heading text-lg font-medium text-[#0F1F19] mb-4 flex items-center gap-2">
          <AlertTriangle className="w-5 h-5 text-[#D34228]" /> ยาใกล้หมดสต็อก ({alerts.low_stock.length})
        </h3>
        {alerts.low_stock.length === 0 && <p className="text-sm text-[#546E62]">ไม่มียาใกล้หมดสต็อก</p>}
        <div className="space-y-2">
          {alerts.low_stock.map((d) => (
            <div key={d.id} className="flex items-center justify-between border border-[#D34228]/20 bg-[#D34228]/5 rounded-lg p-3">
              <div>
                <div className="text-sm font-medium">{d.name}</div>
                <div className="text-xs text-[#546E62]">{d.drug_code} • จุดสั่งซื้อ {d.reorder_level}</div>
              </div>
              <div className="text-right">
                <div className="text-lg font-heading font-semibold text-[#D34228]">{d.quantity_in_stock}</div>
                <div className="text-[10px] text-[#546E62]">คงเหลือ</div>
              </div>
            </div>
          ))}
        </div>
      </div>
      <div className="bg-white border border-[#E1E5E2] rounded-lg p-5 shadow-sm" data-testid="expiring-alerts">
        <h3 className="font-heading text-lg font-medium text-[#0F1F19] mb-4 flex items-center gap-2">
          <CalendarX2 className="w-5 h-5 text-[#E5A732]" /> ยาใกล้หมดอายุภายใน {alerts.horizon_days} วัน ({alerts.expiring.length})
        </h3>
        {alerts.expiring.length === 0 && <p className="text-sm text-[#546E62]">ไม่มียาใกล้หมดอายุ</p>}
        <div className="space-y-2">
          {alerts.expiring.map((d) => {
            const batches = (d.batches || []).filter((b) => isExpiringSoon(b.expiry_date, alerts.horizon_days) && b.quantity > 0);
            return (
              <div key={d.id} className="border border-[#E5A732]/30 bg-[#E5A732]/5 rounded-lg p-3">
                <div className="text-sm font-medium">{d.name}</div>
                {batches.map((b, i) => (
                  <div key={i} className="text-xs text-[#546E62] mt-1">
                    Batch {b.batch_number} • {b.quantity} {d.unit} • หมดอายุ <span className="text-[#9c7016] font-semibold">{formatThaiDate(b.expiry_date)}</span>
                  </div>
                ))}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

// ============ Main Page ============
export default function PharmacyPage() {
  return (
    <div className="space-y-6" data-testid="pharmacy-page">
      <div>
        <div className="text-xs font-semibold uppercase tracking-[0.2em] text-[#546E62] mb-1">เภสัชกรรม</div>
        <h1 className="font-heading text-3xl md:text-4xl font-medium tracking-tight text-[#0F1F19]">ระบบเภสัชกรรม</h1>
      </div>
      <Tabs defaultValue="prescriptions">
        <TabsList className="bg-[#F2F0EB] border border-[#E1E5E2]">
          <TabsTrigger value="prescriptions" data-testid="tab-prescriptions">ใบสั่งยา</TabsTrigger>
          <TabsTrigger value="drugs" data-testid="tab-drugs">คลังยา</TabsTrigger>
          <TabsTrigger value="alerts" data-testid="tab-alerts">แจ้งเตือน</TabsTrigger>
        </TabsList>
        <TabsContent value="prescriptions" className="mt-4"><PrescriptionsTab /></TabsContent>
        <TabsContent value="drugs" className="mt-4"><DrugsTab /></TabsContent>
        <TabsContent value="alerts" className="mt-4"><AlertsTab /></TabsContent>
      </Tabs>
    </div>
  );
}
