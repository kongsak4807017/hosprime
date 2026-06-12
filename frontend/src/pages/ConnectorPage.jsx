import { useEffect, useRef, useState } from "react";
import { Database, FileSpreadsheet, HardDrive, Loader2, Plus, ScanSearch, Trash2, Upload, ShieldAlert } from "lucide-react";
import { toast } from "sonner";
import api, { formatApiError } from "@/lib/api";
import { formatThaiDateTime } from "@/lib/helpers";
import {
  Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle,
} from "@/components/ui/dialog";

const inputCls =
  "w-full border border-[#E1E5E2] bg-white rounded-lg px-3 py-2 text-sm focus:border-[#1E3F33] focus:ring-1 focus:ring-[#1E3F33] focus:outline-none";

const TYPE_META = {
  internal: { label: "ฐานข้อมูลภายใน", icon: HardDrive, badge: "bg-[#1E3F33]/10 text-[#1E3F33]" },
  mongodb: { label: "MongoDB ภายนอก (HIS)", icon: Database, badge: "bg-[#2E77D0]/10 text-[#2E77D0]" },
  file: { label: "ไฟล์ข้อมูล", icon: FileSpreadsheet, badge: "bg-[#CC5A3A]/10 text-[#CC5A3A]" },
};

export default function ConnectorPage() {
  const [sources, setSources] = useState([]);
  const [addOpen, setAddOpen] = useState(false);
  const [form, setForm] = useState({ name: "", connection_string: "", db_name: "" });
  const [scanningId, setScanningId] = useState(null);
  const [scan, setScan] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [expandedCol, setExpandedCol] = useState(null);
  const fileRef = useRef(null);

  const fetchSources = () => api.get("/connector/sources").then((r) => setSources(r.data));
  useEffect(() => { fetchSources(); }, []);

  const addSource = async (e) => {
    e.preventDefault();
    setSaving(true);
    try {
      await api.post("/connector/sources", form);
      toast.success("เพิ่มแหล่งข้อมูลสำเร็จ");
      setAddOpen(false);
      setForm({ name: "", connection_string: "", db_name: "" });
      fetchSources();
    } catch (err) { toast.error(formatApiError(err)); } finally { setSaving(false); }
  };

  const uploadFile = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setUploading(true);
    try {
      const fd = new FormData();
      fd.append("file", file);
      await api.post("/connector/upload", fd, { headers: { "Content-Type": "multipart/form-data" } });
      toast.success(`อัปโหลด ${file.name} สำเร็จ`);
      fetchSources();
    } catch (err) { toast.error(formatApiError(err)); } finally {
      setUploading(false);
      if (fileRef.current) fileRef.current.value = "";
    }
  };

  const runScan = async (source) => {
    setScanningId(source.id);
    setScan(null);
    try {
      const { data } = await api.post(`/connector/sources/${source.id}/scan`, null, { timeout: 180000 });
      setScan(data);
      toast.success(`สแกน "${source.name}" สำเร็จ`);
      fetchSources();
    } catch (err) { toast.error(formatApiError(err)); } finally { setScanningId(null); }
  };

  const viewLastScan = async (source) => {
    try {
      const { data } = await api.get(`/connector/sources/${source.id}/scan`);
      setScan(data);
    } catch (err) { toast.error(formatApiError(err)); }
  };

  const deleteSource = async (source) => {
    if (!window.confirm(`ยืนยันการลบแหล่งข้อมูล "${source.name}"?`)) return;
    try {
      await api.delete(`/connector/sources/${source.id}`);
      toast.success("ลบแหล่งข้อมูลสำเร็จ");
      if (scan?.source_id === source.id) setScan(null);
      fetchSources();
    } catch (err) { toast.error(formatApiError(err)); }
  };

  return (
    <div className="space-y-6" data-testid="connector-page">
      <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
        <div>
          <div className="text-xs font-semibold uppercase tracking-[0.2em] text-[#546E62] mb-1">Data Connector & Governance Agent</div>
          <h1 className="font-heading text-3xl md:text-4xl font-medium tracking-tight text-[#0F1F19]">เชื่อมต่อ & สแกนข้อมูล</h1>
          <p className="text-[#546E62] mt-2 text-sm max-w-2xl">
            One-click scan ตรวจจับโครงสร้างฐานข้อมูล HIS เดิม, ระบุข้อมูลส่วนบุคคล (PDPA) และให้ AI แนะนำการ mapping เข้าระบบ + การสร้าง Knowledge Graph
          </p>
        </div>
        <div className="flex gap-2">
          <input ref={fileRef} type="file" accept=".csv,.xlsx,.xls" onChange={uploadFile} className="hidden" data-testid="file-upload-input" />
          <button onClick={() => fileRef.current?.click()} disabled={uploading} data-testid="upload-file-btn" className="inline-flex items-center gap-2 border border-[#E1E5E2] bg-white text-[#0F1F19] hover:bg-[#F2F0EB] rounded-lg px-4 py-2.5 text-sm font-medium transition-colors disabled:opacity-60">
            {uploading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Upload className="w-4 h-4" />} อัปโหลด CSV/Excel
          </button>
          <button onClick={() => setAddOpen(true)} data-testid="add-source-btn" className="inline-flex items-center gap-2 bg-[#1E3F33] text-white hover:bg-[#2C5A48] rounded-lg px-4 py-2.5 text-sm font-medium transition-colors">
            <Plus className="w-4 h-4" /> เชื่อม MongoDB ภายนอก
          </button>
        </div>
      </div>

      {/* Sources */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
        {sources.map((s) => {
          const meta = TYPE_META[s.type] || TYPE_META.internal;
          const Icon = meta.icon;
          return (
            <div key={s.id} className="bg-white border border-[#E1E5E2] rounded-lg p-5 shadow-sm" data-testid="source-card">
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center gap-3">
                  <div className="w-9 h-9 rounded-lg bg-[#F2F0EB] flex items-center justify-center">
                    <Icon className="w-4 h-4 text-[#1E3F33]" />
                  </div>
                  <div>
                    <div className="font-medium text-sm text-[#0F1F19]">{s.name}</div>
                    <span className={`text-[10px] rounded-full px-2 py-0.5 ${meta.badge}`}>{meta.label}</span>
                  </div>
                </div>
                {s.type !== "internal" && (
                  <button onClick={() => deleteSource(s)} className="p-1.5 text-[#D34228] hover:bg-[#D34228]/10 rounded-lg" data-testid="delete-source-btn">
                    <Trash2 className="w-3.5 h-3.5" />
                  </button>
                )}
              </div>
              <div className="text-xs text-[#546E62] mb-4">
                {s.last_scan_at ? `สแกนล่าสุด: ${formatThaiDateTime(s.last_scan_at)}` : "ยังไม่เคยสแกน"}
                {s.type === "file" && s.row_count != null && ` • ${s.row_count.toLocaleString()} แถว`}
              </div>
              <div className="flex gap-2">
                <button
                  onClick={() => runScan(s)}
                  disabled={scanningId !== null}
                  data-testid="scan-source-btn"
                  className="flex-1 inline-flex items-center justify-center gap-2 bg-[#1E3F33] text-white hover:bg-[#2C5A48] rounded-lg px-3 py-2 text-sm font-medium transition-colors disabled:opacity-60"
                >
                  {scanningId === s.id ? <Loader2 className="w-4 h-4 animate-spin" /> : <ScanSearch className="w-4 h-4" />}
                  {scanningId === s.id ? "กำลังสแกน + วิเคราะห์ AI..." : "One-Click Scan"}
                </button>
                {s.last_scan_at && (
                  <button onClick={() => viewLastScan(s)} data-testid="view-scan-btn" className="border border-[#E1E5E2] bg-white rounded-lg px-3 py-2 text-sm hover:bg-[#F2F0EB]">
                    ผลล่าสุด
                  </button>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* Scan results */}
      {scan && (
        <div className="space-y-4" data-testid="scan-results">
          <div className="flex items-center gap-3 flex-wrap">
            <h2 className="font-heading text-xl font-medium text-[#0F1F19]">ผลการสแกน: {scan.source_name}</h2>
            <span className="text-xs text-[#546E62]">{formatThaiDateTime(scan.scanned_at)} โดย {scan.scanned_by}</span>
          </div>
          <div className="grid grid-cols-3 gap-4">
            <div className="bg-white border border-[#E1E5E2] rounded-lg p-4 text-center">
              <div className="font-heading text-2xl font-semibold text-[#1E3F33]" data-testid="scan-collections-count">{scan.total_collections}</div>
              <div className="text-xs text-[#546E62]">Collections/ตาราง</div>
            </div>
            <div className="bg-white border border-[#E1E5E2] rounded-lg p-4 text-center">
              <div className="font-heading text-2xl font-semibold text-[#1E3F33]">{scan.total_records.toLocaleString()}</div>
              <div className="text-xs text-[#546E62]">Records ทั้งหมด</div>
            </div>
            <div className="bg-white border border-[#D34228]/30 rounded-lg p-4 text-center">
              <div className="font-heading text-2xl font-semibold text-[#D34228]" data-testid="scan-pii-count">{scan.pii_field_count}</div>
              <div className="text-xs text-[#546E62]">ฟิลด์ PII (PDPA)</div>
            </div>
          </div>

          {/* AI Analysis */}
          <div className="bg-white border border-[#E1E5E2] rounded-lg p-5 shadow-sm" data-testid="ai-analysis-panel">
            <h3 className="font-heading text-lg font-medium text-[#0F1F19] mb-3 flex items-center gap-2">
              <ShieldAlert className="w-5 h-5 text-[#1E3F33]" /> AI Governance & Mapping Suggestion
            </h3>
            {scan.ai_success ? (
              <div className="text-sm text-[#0F1F19] whitespace-pre-wrap leading-relaxed">{scan.ai_analysis}</div>
            ) : (
              <div className="text-sm text-[#D34228] bg-[#D34228]/5 border border-[#D34228]/20 rounded-lg p-3">
                AI วิเคราะห์ไม่สำเร็จ: {scan.ai_error || "ไม่ทราบสาเหตุ"} — ตรวจสอบการตั้งค่า AI ที่เมนู "ตั้งค่า AI"
              </div>
            )}
          </div>

          {/* Collections detail */}
          <div className="bg-white border border-[#E1E5E2] rounded-lg shadow-sm divide-y divide-[#E1E5E2]">
            {scan.collections.map((c) => (
              <div key={c.name}>
                <button
                  onClick={() => setExpandedCol(expandedCol === c.name ? null : c.name)}
                  className="w-full flex items-center justify-between px-5 py-3 hover:bg-[#F2F0EB]/50 text-left"
                  data-testid={`collection-row-${c.name}`}
                >
                  <div className="flex items-center gap-3">
                    <span className="font-mono text-sm font-semibold text-[#1E3F33]">{c.name}</span>
                    {c.is_system && <span className="text-[10px] bg-[#E1E5E2] text-[#546E62] rounded-full px-2 py-0.5">system</span>}
                  </div>
                  <div className="flex items-center gap-4 text-xs text-[#546E62]">
                    <span>{c.count.toLocaleString()} records</span>
                    <span>{c.fields.length} fields</span>
                    {c.fields.some((f) => f.is_pii) && (
                      <span className="bg-[#D34228]/10 text-[#D34228] rounded-full px-2 py-0.5">PII {c.fields.filter((f) => f.is_pii).length}</span>
                    )}
                  </div>
                </button>
                {expandedCol === c.name && (
                  <div className="px-5 pb-4 overflow-x-auto">
                    <table className="w-full text-xs">
                      <thead>
                        <tr className="text-left text-[#546E62] border-b border-[#E1E5E2]">
                          <th className="py-2 pr-4">ฟิลด์</th><th className="py-2 pr-4">ชนิดข้อมูล</th>
                          <th className="py-2 pr-4">Fill Rate</th><th className="py-2">PDPA/PII</th>
                        </tr>
                      </thead>
                      <tbody>
                        {c.fields.map((f) => (
                          <tr key={f.name} className="border-b border-[#E1E5E2]/50 last:border-0">
                            <td className="py-1.5 pr-4 font-mono">{f.name}</td>
                            <td className="py-1.5 pr-4">{f.types.join(", ")}</td>
                            <td className="py-1.5 pr-4">
                              <span className={f.fill_rate < 50 ? "text-[#D34228]" : "text-[#327A59]"}>{f.fill_rate}%</span>
                            </td>
                            <td className="py-1.5">
                              {f.is_pii ? <span className="bg-[#D34228]/10 text-[#D34228] rounded-full px-2 py-0.5">{f.pii_reason}</span> : "-"}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Add MongoDB dialog */}
      <Dialog open={addOpen} onOpenChange={setAddOpen}>
        <DialogContent className="max-w-md">
          <DialogHeader>
            <DialogTitle className="font-heading">เชื่อมต่อ MongoDB ภายนอก (HIS เดิม)</DialogTitle>
            <DialogDescription>ระบุ connection string ของฐานข้อมูล HIS ที่ต้องการสแกน</DialogDescription>
          </DialogHeader>
          <form onSubmit={addSource} className="space-y-3" data-testid="add-source-form">
            <div>
              <label className="text-xs text-[#546E62]">ชื่อแหล่งข้อมูล *</label>
              <input required value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} placeholder="เช่น HIS โรงพยาบาลเดิม" className={inputCls} data-testid="source-name-input" />
            </div>
            <div>
              <label className="text-xs text-[#546E62]">Connection String *</label>
              <input required value={form.connection_string} onChange={(e) => setForm({ ...form, connection_string: e.target.value })} placeholder="mongodb://user:pass@host:27017" className={inputCls} data-testid="source-connstr-input" />
            </div>
            <div>
              <label className="text-xs text-[#546E62]">ชื่อ Database *</label>
              <input required value={form.db_name} onChange={(e) => setForm({ ...form, db_name: e.target.value })} placeholder="เช่น his_db" className={inputCls} data-testid="source-dbname-input" />
            </div>
            <button type="submit" disabled={saving} data-testid="source-submit-btn" className="w-full bg-[#1E3F33] text-white hover:bg-[#2C5A48] rounded-lg py-2.5 font-medium transition-colors disabled:opacity-60">
              เพิ่มแหล่งข้อมูล
            </button>
          </form>
        </DialogContent>
      </Dialog>
    </div>
  );
}
