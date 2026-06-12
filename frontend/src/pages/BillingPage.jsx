import { useCallback, useEffect, useState } from "react";
import { Plus, Search, Trash2, Banknote, CalendarRange, AlertCircle, FileText } from "lucide-react";
import { toast } from "sonner";
import api, { formatApiError } from "@/lib/api";
import { useAuth } from "@/context/AuthContext";
import {
  INVOICE_STATUS_LABELS, INVOICE_STATUS_BADGES, PAYMENT_METHOD_LABELS,
  CLAIM_STATUS_LABELS, ITEM_TYPE_LABELS,
} from "@/lib/constants";
import { formatTHB, formatThaiDate, formatThaiDateTime } from "@/lib/helpers";
import {
  Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle,
} from "@/components/ui/dialog";

const inputCls =
  "w-full border border-[#E1E5E2] bg-white rounded-lg px-3 py-2 text-sm focus:border-[#1E3F33] focus:ring-1 focus:ring-[#1E3F33] focus:outline-none";

const BILLING_ROLES = ["admin", "finance"];

const StatCard = ({ icon: Icon, label, value, accent, testId }) => (
  <div className="bg-white border border-[#E1E5E2] rounded-lg p-5 shadow-sm" data-testid={testId}>
    <div className="flex items-center justify-between mb-2">
      <span className="text-xs font-semibold uppercase tracking-[0.15em] text-[#546E62]">{label}</span>
      <Icon className={`w-4 h-4 ${accent || "text-[#1E3F33]"}`} />
    </div>
    <div className={`font-heading text-2xl font-medium ${accent || "text-[#0F1F19]"}`}>{value}</div>
  </div>
);

const EMPTY_ITEM = { item_type: "consultation", description: "", quantity: 1, unit_price: "" };

export default function BillingPage() {
  const { user } = useAuth();
  const [stats, setStats] = useState(null);
  const [data, setData] = useState({ items: [], total: 0 });
  const [status, setStatus] = useState("");
  const [search, setSearch] = useState("");
  const [createOpen, setCreateOpen] = useState(false);
  const [patients, setPatients] = useState([]);
  const [form, setForm] = useState({ patient_id: "", discount: "", tax: "", due_date: "", notes: "", line_items: [{ ...EMPTY_ITEM }] });
  const [detail, setDetail] = useState(null);
  const [payForm, setPayForm] = useState({ amount: "", method: "cash", reference: "" });
  const [claimForm, setClaimForm] = useState({ provider: "", claim_amount: "" });
  const [claimUpdate, setClaimUpdate] = useState({ status: "approved", approved_amount: "" });
  const [saving, setSaving] = useState(false);

  const canWrite = BILLING_ROLES.includes(user?.role);

  const fetchStats = useCallback(() => {
    api.get("/billing/stats").then((r) => setStats(r.data));
  }, []);

  const fetch_ = useCallback(() => {
    api.get("/billing/invoices", { params: { status, search, limit: 30 } }).then((r) => setData(r.data));
  }, [status, search]);

  useEffect(() => { fetchStats(); }, [fetchStats]);
  useEffect(() => { const t = setTimeout(fetch_, search ? 350 : 0); return () => clearTimeout(t); }, [fetch_, search]);

  useEffect(() => {
    if (!createOpen) return;
    api.get("/patients", { params: { limit: 100 } }).then((r) => setPatients(r.data.items));
  }, [createOpen]);

  const setItem = (i, field, val) => setForm((f) => ({ ...f, line_items: f.line_items.map((it, idx) => (idx === i ? { ...it, [field]: val } : it)) }));

  const subtotal = form.line_items.reduce((s, it) => s + (Number(it.quantity) || 0) * (Number(it.unit_price) || 0), 0);
  const totalAmount = subtotal - (Number(form.discount) || 0) + (Number(form.tax) || 0);

  const refreshDetail = async (id) => {
    const { data } = await api.get(`/billing/invoices/${id}`);
    setDetail(data);
    fetch_();
    fetchStats();
  };

  const submitInvoice = async (e) => {
    e.preventDefault();
    setSaving(true);
    try {
      const payload = {
        patient_id: form.patient_id,
        discount: Number(form.discount) || 0,
        tax: Number(form.tax) || 0,
        due_date: form.due_date,
        notes: form.notes,
        line_items: form.line_items.map((it) => ({ ...it, quantity: Number(it.quantity), unit_price: Number(it.unit_price) })),
      };
      const { data } = await api.post("/billing/invoices", payload);
      toast.success(`สร้างใบแจ้งหนี้สำเร็จ (${data.invoice_number})`);
      setCreateOpen(false);
      setForm({ patient_id: "", discount: "", tax: "", due_date: "", notes: "", line_items: [{ ...EMPTY_ITEM }] });
      fetch_();
      fetchStats();
    } catch (err) { toast.error(formatApiError(err)); } finally { setSaving(false); }
  };

  const submitPayment = async (e) => {
    e.preventDefault();
    setSaving(true);
    try {
      await api.post(`/billing/invoices/${detail.id}/payments`, { ...payForm, amount: Number(payForm.amount) });
      toast.success("บันทึกการชำระเงินสำเร็จ");
      setPayForm({ amount: "", method: "cash", reference: "" });
      await refreshDetail(detail.id);
    } catch (err) { toast.error(formatApiError(err)); } finally { setSaving(false); }
  };

  const submitClaim = async (e) => {
    e.preventDefault();
    setSaving(true);
    try {
      await api.post(`/billing/invoices/${detail.id}/claim`, { ...claimForm, claim_amount: Number(claimForm.claim_amount) });
      toast.success("ยื่นเคลมประกันสำเร็จ");
      setClaimForm({ provider: "", claim_amount: "" });
      await refreshDetail(detail.id);
    } catch (err) { toast.error(formatApiError(err)); } finally { setSaving(false); }
  };

  const submitClaimUpdate = async (e) => {
    e.preventDefault();
    setSaving(true);
    try {
      await api.patch(`/billing/invoices/${detail.id}/claim`, { status: claimUpdate.status, approved_amount: Number(claimUpdate.approved_amount) || 0 });
      toast.success("อัปเดตสถานะเคลมสำเร็จ");
      await refreshDetail(detail.id);
    } catch (err) { toast.error(formatApiError(err)); } finally { setSaving(false); }
  };

  const cancelInvoice = async () => {
    if (!window.confirm("ยืนยันการยกเลิกใบแจ้งหนี้นี้?")) return;
    try {
      await api.post(`/billing/invoices/${detail.id}/cancel`);
      toast.success("ยกเลิกใบแจ้งหนี้สำเร็จ");
      await refreshDetail(detail.id);
    } catch (err) { toast.error(formatApiError(err)); }
  };

  return (
    <div className="space-y-6" data-testid="billing-page">
      <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
        <div>
          <div className="text-xs font-semibold uppercase tracking-[0.2em] text-[#546E62] mb-1">การเงิน</div>
          <h1 className="font-heading text-3xl md:text-4xl font-medium tracking-tight text-[#0F1F19]">การเงิน & บิล</h1>
        </div>
        {canWrite && (
          <button onClick={() => setCreateOpen(true)} data-testid="create-invoice-btn" className="inline-flex items-center gap-2 bg-[#1E3F33] text-white hover:bg-[#2C5A48] rounded-lg px-5 py-2.5 font-medium transition-colors">
            <Plus className="w-4 h-4" /> สร้างใบแจ้งหนี้
          </button>
        )}
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard icon={Banknote} label="รายรับวันนี้" value={formatTHB(stats?.revenue_today)} testId="stat-revenue-today" />
        <StatCard icon={CalendarRange} label="รายรับเดือนนี้" value={formatTHB(stats?.revenue_month)} testId="stat-revenue-month" />
        <StatCard icon={AlertCircle} label="ยอดค้างชำระ" value={formatTHB(stats?.outstanding)} accent="text-[#D34228]" testId="stat-outstanding" />
        <StatCard icon={FileText} label="บิลรอชำระ" value={stats?.pending_invoices ?? "–"} testId="stat-pending-invoices" />
      </div>

      <div className="flex flex-col md:flex-row gap-3">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[#546E62]" />
          <input value={search} onChange={(e) => setSearch(e.target.value)} placeholder="ค้นหาเลขที่บิล, ชื่อผู้ป่วย..." data-testid="invoice-search-input" className={`${inputCls} pl-10 py-2.5`} />
        </div>
        <select value={status} onChange={(e) => setStatus(e.target.value)} data-testid="invoice-status-filter" className="border border-[#E1E5E2] bg-white rounded-lg px-4 py-2.5 text-sm focus:outline-none">
          <option value="">สถานะทั้งหมด</option>
          {Object.entries(INVOICE_STATUS_LABELS).map(([k, v]) => <option key={k} value={k}>{v}</option>)}
        </select>
      </div>

      <div className="bg-white border border-[#E1E5E2] rounded-lg shadow-sm overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="text-left text-xs uppercase tracking-wider text-[#546E62] border-b border-[#E1E5E2] bg-[#F2F0EB]/50">
              <th className="px-4 py-3 font-semibold">เลขที่บิล</th>
              <th className="px-4 py-3 font-semibold">วันที่</th>
              <th className="px-4 py-3 font-semibold">ผู้ป่วย</th>
              <th className="px-4 py-3 font-semibold">ยอดรวม</th>
              <th className="px-4 py-3 font-semibold">ชำระแล้ว</th>
              <th className="px-4 py-3 font-semibold">ค้างชำระ</th>
              <th className="px-4 py-3 font-semibold">เคลม</th>
              <th className="px-4 py-3 font-semibold">สถานะ</th>
              <th className="px-4 py-3 font-semibold">จัดการ</th>
            </tr>
          </thead>
          <tbody>
            {data.items.length === 0 && <tr><td colSpan={9} className="px-4 py-8 text-center text-[#546E62]" data-testid="invoices-empty">ไม่พบใบแจ้งหนี้</td></tr>}
            {data.items.map((inv) => (
              <tr key={inv.id} data-testid="invoice-row" className="border-b border-[#E1E5E2] last:border-0 hover:bg-[#F2F0EB]/50">
                <td className="px-4 py-3 font-mono text-xs text-[#1E3F33] font-semibold">{inv.invoice_number}</td>
                <td className="px-4 py-3 text-xs text-[#546E62]">{formatThaiDate(inv.invoice_date)}</td>
                <td className="px-4 py-3 font-medium">{inv.patient_name}</td>
                <td className="px-4 py-3 font-semibold">{formatTHB(inv.total_amount)}</td>
                <td className="px-4 py-3 text-[#327A59]">{formatTHB(inv.paid_amount)}</td>
                <td className="px-4 py-3 text-[#D34228]">{formatTHB(inv.balance)}</td>
                <td className="px-4 py-3 text-xs">
                  {inv.insurance_claim ? CLAIM_STATUS_LABELS[inv.insurance_claim.status] : <span className="text-[#546E62]">—</span>}
                </td>
                <td className="px-4 py-3">
                  <span className={`text-xs rounded-full px-2.5 py-1 font-medium ${INVOICE_STATUS_BADGES[inv.status]}`} data-testid={`invoice-status-${inv.status}`}>
                    {INVOICE_STATUS_LABELS[inv.status]}
                  </span>
                </td>
                <td className="px-4 py-3">
                  <button onClick={() => { setDetail(inv); setPayForm({ amount: String(inv.balance || ""), method: "cash", reference: "" }); }} data-testid="view-invoice-btn" className="text-xs border border-[#E1E5E2] rounded-lg px-3 py-1.5 bg-white hover:bg-[#F2F0EB] font-medium">
                    ดู / ชำระเงิน
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Create invoice dialog */}
      <Dialog open={createOpen} onOpenChange={setCreateOpen}>
        <DialogContent className="max-w-2xl max-h-[85vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle className="font-heading">สร้างใบแจ้งหนี้</DialogTitle>
            <DialogDescription>เพิ่มรายการค่าใช้จ่ายของผู้ป่วย</DialogDescription>
          </DialogHeader>
          <form onSubmit={submitInvoice} className="space-y-3" data-testid="invoice-form">
            <div>
              <label className="text-xs text-[#546E62]">ผู้ป่วย *</label>
              <select required value={form.patient_id} onChange={(e) => setForm({ ...form, patient_id: e.target.value })} className={inputCls} data-testid="invoice-patient-select">
                <option value="">เลือกผู้ป่วย</option>
                {patients.map((p) => <option key={p.id} value={p.id}>{`${p.patient_number} — ${p.first_name} ${p.last_name}`}</option>)}
              </select>
            </div>
            <div className="space-y-2">
              <label className="text-xs font-semibold text-[#0F1F19]">รายการ *</label>
              {form.line_items.map((it, i) => (
                <div key={i} className="grid grid-cols-[110px,1fr,70px,100px,auto] gap-2 items-center">
                  <select value={it.item_type} onChange={(e) => setItem(i, "item_type", e.target.value)} className={inputCls}>
                    {Object.entries(ITEM_TYPE_LABELS).map(([k, v]) => <option key={k} value={k}>{v}</option>)}
                  </select>
                  <input required value={it.description} onChange={(e) => setItem(i, "description", e.target.value)} placeholder="รายละเอียด" className={inputCls} data-testid={`invoice-item-desc-${i}`} />
                  <input type="number" min="1" required value={it.quantity} onChange={(e) => setItem(i, "quantity", e.target.value)} className={inputCls} />
                  <input type="number" min="0" step="0.01" required value={it.unit_price} onChange={(e) => setItem(i, "unit_price", e.target.value)} placeholder="ราคา" className={inputCls} data-testid={`invoice-item-price-${i}`} />
                  {form.line_items.length > 1 ? (
                    <button type="button" onClick={() => setForm((f) => ({ ...f, line_items: f.line_items.filter((_, idx) => idx !== i) }))} className="p-2 text-[#D34228] hover:bg-[#D34228]/10 rounded-lg"><Trash2 className="w-4 h-4" /></button>
                  ) : <span />}
                </div>
              ))}
              <button type="button" onClick={() => setForm((f) => ({ ...f, line_items: [...f.line_items, { ...EMPTY_ITEM }] }))} className="inline-flex items-center gap-2 text-sm text-[#1E3F33] font-medium hover:underline">
                <Plus className="w-4 h-4" /> เพิ่มรายการ
              </button>
            </div>
            <div className="grid grid-cols-3 gap-3">
              <div>
                <label className="text-xs text-[#546E62]">ส่วนลด (บาท)</label>
                <input type="number" min="0" step="0.01" value={form.discount} onChange={(e) => setForm({ ...form, discount: e.target.value })} className={inputCls} />
              </div>
              <div>
                <label className="text-xs text-[#546E62]">ภาษี (บาท)</label>
                <input type="number" min="0" step="0.01" value={form.tax} onChange={(e) => setForm({ ...form, tax: e.target.value })} className={inputCls} />
              </div>
              <div>
                <label className="text-xs text-[#546E62]">ครบกำหนดชำระ</label>
                <input type="date" value={form.due_date} onChange={(e) => setForm({ ...form, due_date: e.target.value })} className={inputCls} />
              </div>
            </div>
            <div className="bg-[#F2F0EB] border border-[#E1E5E2] rounded-lg p-3 flex justify-between text-sm">
              <span className="text-[#546E62]">ยอดรวมสุทธิ</span>
              <span className="font-heading font-semibold text-lg text-[#1E3F33]" data-testid="invoice-total-preview">{formatTHB(totalAmount)}</span>
            </div>
            <button type="submit" disabled={saving} data-testid="invoice-submit-btn" className="w-full bg-[#1E3F33] text-white hover:bg-[#2C5A48] rounded-lg py-2.5 font-medium transition-colors disabled:opacity-60">
              {saving ? "กำลังบันทึก..." : "สร้างใบแจ้งหนี้"}
            </button>
          </form>
        </DialogContent>
      </Dialog>

      {/* Invoice detail dialog */}
      <Dialog open={!!detail} onOpenChange={(o) => !o && setDetail(null)}>
        <DialogContent className="max-w-2xl max-h-[85vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle className="font-heading flex items-center justify-between">
              <span>{detail?.invoice_number}</span>
              {detail && (
                <span className={`text-xs rounded-full px-2.5 py-1 font-medium ${INVOICE_STATUS_BADGES[detail.status]}`}>
                  {INVOICE_STATUS_LABELS[detail.status]}
                </span>
              )}
            </DialogTitle>
            <DialogDescription>{detail?.patient_name} ({detail?.patient_number}) • {detail && formatThaiDate(detail.invoice_date)}</DialogDescription>
          </DialogHeader>
          {detail && (
            <div className="space-y-4" data-testid="invoice-detail">
              {/* Line items */}
              <table className="w-full text-sm border border-[#E1E5E2] rounded-lg overflow-hidden">
                <thead>
                  <tr className="bg-[#F2F0EB] text-left text-xs text-[#546E62]">
                    <th className="px-3 py-2">ประเภท</th><th className="px-3 py-2">รายละเอียด</th>
                    <th className="px-3 py-2 text-right">จำนวน</th><th className="px-3 py-2 text-right">รวม</th>
                  </tr>
                </thead>
                <tbody>
                  {detail.line_items.map((it, i) => (
                    <tr key={i} className="border-t border-[#E1E5E2]">
                      <td className="px-3 py-2 text-xs">{ITEM_TYPE_LABELS[it.item_type] || it.item_type}</td>
                      <td className="px-3 py-2">{it.description}</td>
                      <td className="px-3 py-2 text-right">{it.quantity}</td>
                      <td className="px-3 py-2 text-right">{formatTHB(it.total)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
              <div className="flex justify-end">
                <div className="w-64 space-y-1 text-sm">
                  <div className="flex justify-between"><span className="text-[#546E62]">ยอดรวม</span><span>{formatTHB(detail.subtotal)}</span></div>
                  {detail.discount > 0 && <div className="flex justify-between"><span className="text-[#546E62]">ส่วนลด</span><span>-{formatTHB(detail.discount)}</span></div>}
                  {detail.tax > 0 && <div className="flex justify-between"><span className="text-[#546E62]">ภาษี</span><span>{formatTHB(detail.tax)}</span></div>}
                  <div className="flex justify-between font-semibold border-t border-[#E1E5E2] pt-1"><span>สุทธิ</span><span>{formatTHB(detail.total_amount)}</span></div>
                  <div className="flex justify-between text-[#327A59]"><span>ชำระแล้ว</span><span>{formatTHB(detail.paid_amount)}</span></div>
                  <div className="flex justify-between text-[#D34228] font-semibold"><span>ค้างชำระ</span><span data-testid="invoice-balance">{formatTHB(detail.balance)}</span></div>
                </div>
              </div>

              {/* Payments history */}
              {detail.payments.length > 0 && (
                <div>
                  <div className="text-xs font-semibold uppercase tracking-wider text-[#546E62] mb-2">ประวัติการชำระเงิน</div>
                  <div className="space-y-1">
                    {detail.payments.map((p) => (
                      <div key={p.id} className="flex justify-between text-sm border border-[#E1E5E2] rounded-lg px-3 py-2">
                        <span>{PAYMENT_METHOD_LABELS[p.method]} {p.reference && `(${p.reference})`} • {p.received_by}</span>
                        <span className="font-medium text-[#327A59]">{formatTHB(p.amount)}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Record payment */}
              {canWrite && detail.balance > 0 && detail.status !== "cancelled" && (
                <form onSubmit={submitPayment} className="border border-[#E1E5E2] rounded-lg p-4 bg-[#F9F9F8] space-y-3" data-testid="payment-form">
                  <div className="text-sm font-semibold">รับชำระเงิน</div>
                  <div className="grid grid-cols-3 gap-3">
                    <div>
                      <label className="text-xs text-[#546E62]">จำนวนเงิน *</label>
                      <input type="number" min="0.01" step="0.01" required value={payForm.amount} onChange={(e) => setPayForm({ ...payForm, amount: e.target.value })} className={inputCls} data-testid="payment-amount-input" />
                    </div>
                    <div>
                      <label className="text-xs text-[#546E62]">วิธีชำระ</label>
                      <select value={payForm.method} onChange={(e) => setPayForm({ ...payForm, method: e.target.value })} className={inputCls} data-testid="payment-method-select">
                        {Object.entries(PAYMENT_METHOD_LABELS).map(([k, v]) => <option key={k} value={k}>{v}</option>)}
                      </select>
                    </div>
                    <div>
                      <label className="text-xs text-[#546E62]">เลขอ้างอิง</label>
                      <input value={payForm.reference} onChange={(e) => setPayForm({ ...payForm, reference: e.target.value })} className={inputCls} />
                    </div>
                  </div>
                  <button type="submit" disabled={saving} data-testid="payment-submit-btn" className="w-full bg-[#1E3F33] text-white hover:bg-[#2C5A48] rounded-lg py-2 text-sm font-medium transition-colors disabled:opacity-60">
                    บันทึกการชำระเงิน
                  </button>
                </form>
              )}

              {/* Insurance claim */}
              <div className="border border-[#E1E5E2] rounded-lg p-4 space-y-3">
                <div className="text-sm font-semibold">เคลมประกัน</div>
                {detail.insurance_claim ? (
                  <div className="space-y-2" data-testid="claim-info">
                    <div className="text-sm">
                      <span className="font-mono text-xs text-[#1E3F33] font-semibold">{detail.insurance_claim.claim_id}</span>
                      <span className="mx-2">•</span>{detail.insurance_claim.provider}
                      <span className="mx-2">•</span>ยอดเคลม {formatTHB(detail.insurance_claim.claim_amount)}
                      <span className="mx-2">•</span>สถานะ: <span className="font-medium">{CLAIM_STATUS_LABELS[detail.insurance_claim.status]}</span>
                      {detail.insurance_claim.approved_amount > 0 && <span className="mx-2">• อนุมัติ {formatTHB(detail.insurance_claim.approved_amount)}</span>}
                    </div>
                    {canWrite && detail.insurance_claim.status === "submitted" && (
                      <form onSubmit={submitClaimUpdate} className="flex gap-2 items-end" data-testid="claim-update-form">
                        <div className="flex-1">
                          <label className="text-xs text-[#546E62]">ผลการพิจารณา</label>
                          <select value={claimUpdate.status} onChange={(e) => setClaimUpdate({ ...claimUpdate, status: e.target.value })} className={inputCls}>
                            <option value="approved">อนุมัติ</option>
                            <option value="partially_approved">อนุมัติบางส่วน</option>
                            <option value="rejected">ปฏิเสธ</option>
                          </select>
                        </div>
                        <div className="flex-1">
                          <label className="text-xs text-[#546E62]">ยอดอนุมัติ</label>
                          <input type="number" min="0" step="0.01" value={claimUpdate.approved_amount} onChange={(e) => setClaimUpdate({ ...claimUpdate, approved_amount: e.target.value })} className={inputCls} />
                        </div>
                        <button type="submit" disabled={saving} className="bg-[#4A6B5D] text-white rounded-lg px-4 py-2 text-sm hover:bg-[#2C5A48]">อัปเดต</button>
                      </form>
                    )}
                  </div>
                ) : canWrite && detail.status !== "cancelled" ? (
                  <form onSubmit={submitClaim} className="flex gap-2 items-end" data-testid="claim-form">
                    <div className="flex-1">
                      <label className="text-xs text-[#546E62]">บริษัท/สิทธิประกัน *</label>
                      <input required value={claimForm.provider} onChange={(e) => setClaimForm({ ...claimForm, provider: e.target.value })} placeholder="เช่น ประกันสังคม" className={inputCls} data-testid="claim-provider-input" />
                    </div>
                    <div className="flex-1">
                      <label className="text-xs text-[#546E62]">ยอดเคลม *</label>
                      <input type="number" min="0.01" step="0.01" required value={claimForm.claim_amount} onChange={(e) => setClaimForm({ ...claimForm, claim_amount: e.target.value })} className={inputCls} data-testid="claim-amount-input" />
                    </div>
                    <button type="submit" disabled={saving} data-testid="claim-submit-btn" className="bg-[#4A6B5D] text-white rounded-lg px-4 py-2 text-sm hover:bg-[#2C5A48]">ยื่นเคลม</button>
                  </form>
                ) : (
                  <p className="text-sm text-[#546E62]">ไม่มีการยื่นเคลม</p>
                )}
              </div>

              {canWrite && detail.status === "pending" && detail.paid_amount === 0 && (
                <button onClick={cancelInvoice} data-testid="cancel-invoice-btn" className="text-sm border border-[#D34228]/30 text-[#D34228] rounded-lg px-4 py-2 hover:bg-[#D34228]/5">
                  ยกเลิกใบแจ้งหนี้
                </button>
              )}
            </div>
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
}
