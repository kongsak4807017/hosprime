import { useCallback, useEffect, useState } from "react";
import { Plus, Search, FlaskConical } from "lucide-react";
import { toast } from "sonner";
import api, { formatApiError } from "@/lib/api";
import { useAuth } from "@/context/AuthContext";
import {
  LAB_STATUS_LABELS, LAB_STATUS_BADGES, LAB_PRIORITY_LABELS, LAB_PRIORITY_BADGES,
} from "@/lib/constants";
import { formatTHB, formatThaiDateTime } from "@/lib/helpers";
import {
  Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle,
} from "@/components/ui/dialog";

const inputCls =
  "w-full border border-[#E1E5E2] bg-white rounded-lg px-3 py-2 text-sm focus:border-[#1E3F33] focus:ring-1 focus:ring-[#1E3F33] focus:outline-none";

const ORDER_ROLES = ["admin", "doctor"];
const COLLECT_ROLES = ["admin", "lab_technician", "nurse"];
const RESULT_ROLES = ["admin", "lab_technician"];

export default function LabPage() {
  const { user } = useAuth();
  const [data, setData] = useState({ items: [], total: 0 });
  const [status, setStatus] = useState("");
  const [search, setSearch] = useState("");
  const [catalog, setCatalog] = useState([]);
  const [patients, setPatients] = useState([]);
  const [orderOpen, setOrderOpen] = useState(false);
  const [orderForm, setOrderForm] = useState({ patient_id: "", test_type: "", priority: "routine", clinical_notes: "" });
  const [resultItem, setResultItem] = useState(null);
  const [resultValues, setResultValues] = useState({});
  const [interpretation, setInterpretation] = useState("");
  const [viewItem, setViewItem] = useState(null);
  const [saving, setSaving] = useState(false);

  const fetch_ = useCallback(() => {
    api.get("/lab/tests", { params: { status, search, limit: 30 } }).then((r) => setData(r.data));
  }, [status, search]);

  useEffect(() => { const t = setTimeout(fetch_, search ? 350 : 0); return () => clearTimeout(t); }, [fetch_, search]);

  useEffect(() => {
    api.get("/lab/catalog").then((r) => setCatalog(r.data));
  }, []);

  useEffect(() => {
    if (!orderOpen) return;
    api.get("/patients", { params: { limit: 100 } }).then((r) => setPatients(r.data.items));
  }, [orderOpen]);

  const selectedTest = catalog.find((t) => t.test_type === orderForm.test_type);
  const resultCatalog = catalog.find((t) => t.test_type === resultItem?.test_type);

  const submitOrder = async (e) => {
    e.preventDefault();
    setSaving(true);
    try {
      await api.post("/lab/tests", orderForm);
      toast.success("สั่งตรวจสำเร็จ");
      setOrderOpen(false);
      setOrderForm({ patient_id: "", test_type: "", priority: "routine", clinical_notes: "" });
      fetch_();
    } catch (err) { toast.error(formatApiError(err)); } finally { setSaving(false); }
  };

  const collect = async (id) => {
    try {
      await api.post(`/lab/tests/${id}/collect`);
      toast.success("บันทึกการเก็บตัวอย่างสำเร็จ");
      fetch_();
    } catch (err) { toast.error(formatApiError(err)); }
  };

  const cancel = async (id) => {
    if (!window.confirm("ยืนยันการยกเลิกรายการตรวจนี้?")) return;
    try {
      await api.post(`/lab/tests/${id}/cancel`);
      toast.success("ยกเลิกรายการตรวจสำเร็จ");
      fetch_();
    } catch (err) { toast.error(formatApiError(err)); }
  };

  const openResults = (t) => {
    setResultItem(t);
    setResultValues({});
    setInterpretation("");
  };

  const submitResults = async (e) => {
    e.preventDefault();
    setSaving(true);
    try {
      const parameters = (resultCatalog?.parameters || []).map((p) => ({
        name: p.name,
        value: String(resultValues[p.name] ?? ""),
      })).filter((p) => p.value !== "");
      if (parameters.length === 0) {
        toast.error("กรุณากรอกผลอย่างน้อย 1 ค่า");
        setSaving(false);
        return;
      }
      await api.post(`/lab/tests/${resultItem.id}/results`, { parameters, interpretation });
      toast.success("บันทึกผลตรวจสำเร็จ");
      setResultItem(null);
      fetch_();
    } catch (err) { toast.error(formatApiError(err)); } finally { setSaving(false); }
  };

  return (
    <div className="space-y-6" data-testid="lab-page">
      <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
        <div>
          <div className="text-xs font-semibold uppercase tracking-[0.2em] text-[#546E62] mb-1">ห้องปฏิบัติการ</div>
          <h1 className="font-heading text-3xl md:text-4xl font-medium tracking-tight text-[#0F1F19]">
            รายการตรวจแล็บ <span className="text-[#546E62] text-xl font-normal">({data.total} รายการ)</span>
          </h1>
        </div>
        {ORDER_ROLES.includes(user?.role) && (
          <button onClick={() => setOrderOpen(true)} data-testid="order-lab-btn" className="inline-flex items-center gap-2 bg-[#1E3F33] text-white hover:bg-[#2C5A48] rounded-lg px-5 py-2.5 font-medium transition-colors">
            <Plus className="w-4 h-4" /> สั่งตรวจใหม่
          </button>
        )}
      </div>

      <div className="flex flex-col md:flex-row gap-3">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[#546E62]" />
          <input value={search} onChange={(e) => setSearch(e.target.value)} placeholder="ค้นหาเลขที่ตรวจ, ชื่อผู้ป่วย, ชนิดการตรวจ..." data-testid="lab-search-input" className={`${inputCls} pl-10 py-2.5`} />
        </div>
        <select value={status} onChange={(e) => setStatus(e.target.value)} data-testid="lab-status-filter" className="border border-[#E1E5E2] bg-white rounded-lg px-4 py-2.5 text-sm focus:outline-none">
          <option value="">สถานะทั้งหมด</option>
          {Object.entries(LAB_STATUS_LABELS).map(([k, v]) => <option key={k} value={k}>{v}</option>)}
        </select>
      </div>

      <div className="bg-white border border-[#E1E5E2] rounded-lg shadow-sm overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="text-left text-xs uppercase tracking-wider text-[#546E62] border-b border-[#E1E5E2] bg-[#F2F0EB]/50">
              <th className="px-4 py-3 font-semibold">เลขที่</th>
              <th className="px-4 py-3 font-semibold">ผู้ป่วย</th>
              <th className="px-4 py-3 font-semibold">รายการตรวจ</th>
              <th className="px-4 py-3 font-semibold">แพทย์ผู้สั่ง</th>
              <th className="px-4 py-3 font-semibold">ความเร่งด่วน</th>
              <th className="px-4 py-3 font-semibold">สั่งเมื่อ</th>
              <th className="px-4 py-3 font-semibold">สถานะ</th>
              <th className="px-4 py-3 font-semibold">จัดการ</th>
            </tr>
          </thead>
          <tbody>
            {data.items.length === 0 && <tr><td colSpan={8} className="px-4 py-8 text-center text-[#546E62]" data-testid="lab-empty">ไม่พบรายการตรวจ</td></tr>}
            {data.items.map((t) => (
              <tr key={t.id} data-testid="lab-row" className="border-b border-[#E1E5E2] last:border-0 hover:bg-[#F2F0EB]/50">
                <td className="px-4 py-3 font-mono text-xs text-[#1E3F33] font-semibold">{t.test_number}</td>
                <td className="px-4 py-3">
                  <div className="font-medium">{t.patient_name}</div>
                  <div className="text-xs text-[#546E62] font-mono">{t.patient_number}</div>
                </td>
                <td className="px-4 py-3">{t.test_type}</td>
                <td className="px-4 py-3">{t.doctor_name}</td>
                <td className="px-4 py-3"><span className={`text-xs rounded-full px-2.5 py-1 font-medium ${LAB_PRIORITY_BADGES[t.priority]}`}>{LAB_PRIORITY_LABELS[t.priority]}</span></td>
                <td className="px-4 py-3 text-xs text-[#546E62]">{formatThaiDateTime(t.ordered_at)}</td>
                <td className="px-4 py-3">
                  <span className={`text-xs rounded-full px-2.5 py-1 font-medium ${LAB_STATUS_BADGES[t.status]}`} data-testid={`lab-status-${t.status}`}>
                    {LAB_STATUS_LABELS[t.status]}
                    {t.results?.has_abnormal && " ⚠"}
                  </span>
                </td>
                <td className="px-4 py-3">
                  <div className="flex gap-2">
                    {t.status === "ordered" && COLLECT_ROLES.includes(user?.role) && (
                      <button onClick={() => collect(t.id)} data-testid="collect-sample-btn" className="text-xs bg-[#4A6B5D] text-white rounded-lg px-2.5 py-1 hover:bg-[#2C5A48]">เก็บตัวอย่าง</button>
                    )}
                    {(t.status === "sample_collected" || t.status === "in_progress") && RESULT_ROLES.includes(user?.role) && (
                      <button onClick={() => openResults(t)} data-testid="enter-results-btn" className="text-xs bg-[#1E3F33] text-white rounded-lg px-2.5 py-1 hover:bg-[#2C5A48]">บันทึกผล</button>
                    )}
                    {t.status === "completed" && (
                      <button onClick={() => setViewItem(t)} data-testid="view-results-btn" className="text-xs border border-[#327A59]/30 text-[#327A59] rounded-lg px-2.5 py-1 hover:bg-[#327A59]/5">ดูผล</button>
                    )}
                    {["ordered", "sample_collected"].includes(t.status) && ORDER_ROLES.includes(user?.role) && (
                      <button onClick={() => cancel(t.id)} className="text-xs border border-[#D34228]/30 text-[#D34228] rounded-lg px-2.5 py-1 hover:bg-[#D34228]/5">ยกเลิก</button>
                    )}
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Order dialog */}
      <Dialog open={orderOpen} onOpenChange={setOrderOpen}>
        <DialogContent className="max-w-lg">
          <DialogHeader>
            <DialogTitle className="font-heading">สั่งตรวจแล็บใหม่</DialogTitle>
            <DialogDescription>เลือกผู้ป่วยและรายการตรวจ</DialogDescription>
          </DialogHeader>
          <form onSubmit={submitOrder} className="space-y-3" data-testid="lab-order-form">
            <div>
              <label className="text-xs text-[#546E62]">ผู้ป่วย *</label>
              <select required value={orderForm.patient_id} onChange={(e) => setOrderForm({ ...orderForm, patient_id: e.target.value })} className={inputCls} data-testid="lab-patient-select">
                <option value="">เลือกผู้ป่วย</option>
                {patients.map((p) => <option key={p.id} value={p.id}>{`${p.patient_number} — ${p.first_name} ${p.last_name}`}</option>)}
              </select>
            </div>
            <div>
              <label className="text-xs text-[#546E62]">รายการตรวจ *</label>
              <select required value={orderForm.test_type} onChange={(e) => setOrderForm({ ...orderForm, test_type: e.target.value })} className={inputCls} data-testid="lab-testtype-select">
                <option value="">เลือกรายการตรวจ</option>
                {catalog.map((t) => <option key={t.test_type} value={t.test_type}>{`${t.test_type} (${t.price} บาท)`}</option>)}
              </select>
              {selectedTest && (
                <div className="mt-2 bg-[#F2F0EB] border border-[#E1E5E2] rounded-lg p-3 text-xs text-[#546E62]">
                  <div className="font-semibold text-[#0F1F19] mb-1">พารามิเตอร์ที่ตรวจ:</div>
                  {selectedTest.parameters.map((p) => (
                    <div key={p.name}>{p.name} (ค่าอ้างอิง {p.ref_min} - {p.ref_max} {p.unit})</div>
                  ))}
                </div>
              )}
            </div>
            <div>
              <label className="text-xs text-[#546E62]">ความเร่งด่วน</label>
              <select value={orderForm.priority} onChange={(e) => setOrderForm({ ...orderForm, priority: e.target.value })} className={inputCls} data-testid="lab-priority-select">
                {Object.entries(LAB_PRIORITY_LABELS).map(([k, v]) => <option key={k} value={k}>{v}</option>)}
              </select>
            </div>
            <div>
              <label className="text-xs text-[#546E62]">ข้อมูลทางคลินิก</label>
              <textarea rows={2} value={orderForm.clinical_notes} onChange={(e) => setOrderForm({ ...orderForm, clinical_notes: e.target.value })} className={inputCls} data-testid="lab-notes-input" />
            </div>
            <button type="submit" disabled={saving} data-testid="lab-order-submit-btn" className="w-full bg-[#1E3F33] text-white hover:bg-[#2C5A48] rounded-lg py-2.5 font-medium transition-colors disabled:opacity-60">
              {saving ? "กำลังบันทึก..." : "ยืนยันสั่งตรวจ"}
            </button>
          </form>
        </DialogContent>
      </Dialog>

      {/* Results entry dialog */}
      <Dialog open={!!resultItem} onOpenChange={(o) => !o && setResultItem(null)}>
        <DialogContent className="max-w-lg max-h-[85vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle className="font-heading">บันทึกผล: {resultItem?.test_type}</DialogTitle>
            <DialogDescription>{resultItem?.test_number} • {resultItem?.patient_name}</DialogDescription>
          </DialogHeader>
          <form onSubmit={submitResults} className="space-y-3" data-testid="lab-results-form">
            {(resultCatalog?.parameters || []).map((p) => (
              <div key={p.name} className="grid grid-cols-[1fr,120px] gap-3 items-center">
                <div>
                  <div className="text-sm font-medium">{p.name}</div>
                  <div className="text-xs text-[#546E62]">ค่าอ้างอิง {p.ref_min} - {p.ref_max} {p.unit}</div>
                </div>
                <input
                  type="text"
                  value={resultValues[p.name] ?? ""}
                  onChange={(e) => setResultValues({ ...resultValues, [p.name]: e.target.value })}
                  placeholder="ค่าที่วัดได้"
                  className={inputCls}
                  data-testid={`result-input-${p.name.replace(/[^a-zA-Z0-9]/g, "")}`}
                />
              </div>
            ))}
            <div>
              <label className="text-xs text-[#546E62]">การแปลผล/ความเห็น</label>
              <textarea rows={2} value={interpretation} onChange={(e) => setInterpretation(e.target.value)} className={inputCls} data-testid="result-interpretation-input" />
            </div>
            <button type="submit" disabled={saving} data-testid="lab-results-submit-btn" className="w-full bg-[#1E3F33] text-white hover:bg-[#2C5A48] rounded-lg py-2.5 font-medium transition-colors disabled:opacity-60">
              {saving ? "กำลังบันทึก..." : "บันทึกผลตรวจ"}
            </button>
          </form>
        </DialogContent>
      </Dialog>

      {/* View results dialog */}
      <Dialog open={!!viewItem} onOpenChange={(o) => !o && setViewItem(null)}>
        <DialogContent className="max-w-lg">
          <DialogHeader>
            <DialogTitle className="font-heading flex items-center gap-2">
              <FlaskConical className="w-5 h-5 text-[#1E3F33]" /> ผลตรวจ: {viewItem?.test_type}
            </DialogTitle>
            <DialogDescription>{viewItem?.test_number} • {viewItem?.patient_name}</DialogDescription>
          </DialogHeader>
          {viewItem?.results && (
            <div className="space-y-3" data-testid="lab-results-view">
              <table className="w-full text-sm border border-[#E1E5E2] rounded-lg overflow-hidden">
                <thead>
                  <tr className="bg-[#F2F0EB] text-left text-xs text-[#546E62]">
                    <th className="px-3 py-2">พารามิเตอร์</th>
                    <th className="px-3 py-2">ผล</th>
                    <th className="px-3 py-2">ค่าอ้างอิง</th>
                  </tr>
                </thead>
                <tbody>
                  {viewItem.results.parameters.map((p, i) => (
                    <tr key={i} className="border-t border-[#E1E5E2]">
                      <td className="px-3 py-2 font-medium">{p.name}</td>
                      <td className={`px-3 py-2 font-semibold ${p.is_abnormal ? "text-[#D34228]" : "text-[#327A59]"}`}>
                        {p.value} {p.unit}
                        {p.is_abnormal && <span className="ml-1 text-[10px] bg-[#D34228]/10 rounded-full px-2 py-0.5" data-testid="abnormal-flag">ผิดปกติ</span>}
                      </td>
                      <td className="px-3 py-2 text-xs text-[#546E62]">{p.reference_range}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
              {viewItem.results.interpretation && (
                <div className="bg-[#F2F0EB] border border-[#E1E5E2] rounded-lg p-3 text-sm">
                  <div className="text-xs font-semibold text-[#546E62] mb-1">การแปลผล</div>
                  {viewItem.results.interpretation}
                </div>
              )}
              <div className="text-xs text-[#546E62]">
                ตรวจโดย {viewItem.performed_by} • {formatThaiDateTime(viewItem.performed_at)} • ค่าตรวจ {formatTHB(viewItem.price)}
              </div>
            </div>
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
}
