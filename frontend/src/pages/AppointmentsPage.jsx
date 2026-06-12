import { useCallback, useEffect, useState } from "react";
import { CalendarPlus, ChevronLeft, ChevronRight, Search } from "lucide-react";
import { toast } from "sonner";
import api, { formatApiError } from "@/lib/api";
import { useAuth } from "@/context/AuthContext";
import {
  STATUS_LABELS, STATUS_BADGES, NEXT_STATUSES, APPOINTMENT_TYPES, PRIORITY_LABELS,
} from "@/lib/constants";
import { formatThaiDate, todayStr } from "@/lib/helpers";
import {
  Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger,
} from "@/components/ui/dialog";
import {
  DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

const inputCls =
  "w-full border border-[#E1E5E2] bg-white rounded-lg px-3 py-2 text-sm focus:border-[#1E3F33] focus:ring-1 focus:ring-[#1E3F33] focus:outline-none";

const CAN_WRITE = ["admin", "doctor", "nurse"];

const EMPTY_FORM = {
  patient_id: "", doctor_id: "", department: "", appointment_type: "consultation",
  appointment_date: todayStr(), appointment_time: "09:00", duration_minutes: 30,
  reason: "", priority: "normal", room_number: "",
};

export default function AppointmentsPage() {
  const { user } = useAuth();
  const [data, setData] = useState({ items: [], total: 0, page: 1, pages: 1 });
  const [date, setDate] = useState(todayStr());
  const [status, setStatus] = useState("");
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(true);

  const [open, setOpen] = useState(false);
  const [form, setForm] = useState(EMPTY_FORM);
  const [patients, setPatients] = useState([]);
  const [doctors, setDoctors] = useState([]);
  const [saving, setSaving] = useState(false);

  const fetchAppointments = useCallback(async () => {
    setLoading(true);
    try {
      const { data } = await api.get("/appointments", {
        params: { date, status, search, page, limit: 15 },
      });
      setData(data);
    } finally {
      setLoading(false);
    }
  }, [date, status, search, page]);

  useEffect(() => {
    const t = setTimeout(fetchAppointments, search ? 350 : 0);
    return () => clearTimeout(t);
  }, [fetchAppointments, search]);

  useEffect(() => {
    if (!open) return;
    api.get("/patients", { params: { limit: 100 } }).then((res) => setPatients(res.data.items));
    api.get("/appointments/doctors").then((res) => setDoctors(res.data));
  }, [open]);

  const set = (key, value) => setForm((f) => ({ ...f, [key]: value }));

  const handleDoctorChange = (doctorId) => {
    const doc = doctors.find((d) => d.id === doctorId);
    setForm((f) => ({ ...f, doctor_id: doctorId, department: doc?.department || f.department }));
  };

  const submit = async (e) => {
    e.preventDefault();
    setSaving(true);
    try {
      await api.post("/appointments", { ...form, duration_minutes: Number(form.duration_minutes) });
      toast.success("จองนัดหมายสำเร็จ");
      setOpen(false);
      setForm(EMPTY_FORM);
      fetchAppointments();
    } catch (err) {
      toast.error(formatApiError(err));
    } finally {
      setSaving(false);
    }
  };

  const changeStatus = async (id, newStatus) => {
    try {
      await api.patch(`/appointments/${id}/status`, { status: newStatus });
      toast.success(`เปลี่ยนสถานะเป็น "${STATUS_LABELS[newStatus]}" สำเร็จ`);
      fetchAppointments();
    } catch (err) {
      toast.error(formatApiError(err));
    }
  };

  const canWrite = CAN_WRITE.includes(user?.role);

  return (
    <div className="space-y-6" data-testid="appointments-page">
      <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
        <div>
          <div className="text-xs font-semibold uppercase tracking-[0.2em] text-[#546E62] mb-1">ตารางนัด</div>
          <h1 className="font-heading text-3xl md:text-4xl font-medium tracking-tight text-[#0F1F19]">
            นัดหมาย <span className="text-[#546E62] text-xl font-normal">({data.total} รายการ)</span>
          </h1>
        </div>
        {canWrite && (
          <Dialog open={open} onOpenChange={setOpen}>
            <DialogTrigger asChild>
              <button
                data-testid="appointment-book-btn"
                className="inline-flex items-center gap-2 bg-[#1E3F33] text-white hover:bg-[#2C5A48] rounded-lg px-5 py-2.5 font-medium transition-colors"
              >
                <CalendarPlus className="w-4 h-4" /> จองนัดหมายใหม่
              </button>
            </DialogTrigger>
            <DialogContent className="max-w-lg">
              <DialogHeader>
                <DialogTitle className="font-heading">จองนัดหมายใหม่</DialogTitle>
                <DialogDescription>เลือกผู้ป่วย แพทย์ และเวลานัดหมาย</DialogDescription>
              </DialogHeader>
              <form onSubmit={submit} className="space-y-3" data-testid="appointment-form">
                <div>
                  <label className="text-xs text-[#546E62]">ผู้ป่วย *</label>
                  <select required value={form.patient_id} onChange={(e) => set("patient_id", e.target.value)} className={inputCls} data-testid="appointment-patient-select">
                    <option value="">เลือกผู้ป่วย</option>
                    {patients.map((p) => (
                      <option key={p.id} value={p.id}>{`${p.patient_number} — ${p.first_name} ${p.last_name}`}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="text-xs text-[#546E62]">แพทย์ *</label>
                  <select required value={form.doctor_id} onChange={(e) => handleDoctorChange(e.target.value)} className={inputCls} data-testid="appointment-doctor-select">
                    <option value="">เลือกแพทย์</option>
                    {doctors.map((d) => (
                      <option key={d.id} value={d.id}>{`${d.full_name} (${d.department})`}</option>
                    ))}
                  </select>
                </div>
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="text-xs text-[#546E62]">วันที่ *</label>
                    <input type="date" required value={form.appointment_date} onChange={(e) => set("appointment_date", e.target.value)} className={inputCls} data-testid="appointment-date-input" />
                  </div>
                  <div>
                    <label className="text-xs text-[#546E62]">เวลา *</label>
                    <input type="time" required value={form.appointment_time} onChange={(e) => set("appointment_time", e.target.value)} className={inputCls} data-testid="appointment-time-input" />
                  </div>
                  <div>
                    <label className="text-xs text-[#546E62]">ประเภท</label>
                    <select value={form.appointment_type} onChange={(e) => set("appointment_type", e.target.value)} className={inputCls}>
                      {Object.entries(APPOINTMENT_TYPES).map(([k, v]) => <option key={k} value={k}>{v}</option>)}
                    </select>
                  </div>
                  <div>
                    <label className="text-xs text-[#546E62]">ความเร่งด่วน</label>
                    <select value={form.priority} onChange={(e) => set("priority", e.target.value)} className={inputCls}>
                      {Object.entries(PRIORITY_LABELS).map(([k, v]) => <option key={k} value={k}>{v}</option>)}
                    </select>
                  </div>
                </div>
                <div>
                  <label className="text-xs text-[#546E62]">อาการ/เหตุผลที่มาพบแพทย์</label>
                  <textarea rows={2} value={form.reason} onChange={(e) => set("reason", e.target.value)} className={inputCls} data-testid="appointment-reason-input" />
                </div>
                <button type="submit" disabled={saving} data-testid="appointment-submit-btn" className="w-full bg-[#1E3F33] text-white hover:bg-[#2C5A48] rounded-lg py-2.5 font-medium transition-colors disabled:opacity-60">
                  {saving ? "กำลังบันทึก..." : "ยืนยันการจอง"}
                </button>
              </form>
            </DialogContent>
          </Dialog>
        )}
      </div>

      {/* Filters */}
      <div className="flex flex-col md:flex-row gap-3">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[#546E62]" />
          <input
            value={search}
            onChange={(e) => { setSearch(e.target.value); setPage(1); }}
            placeholder="ค้นหาด้วยชื่อผู้ป่วย, รหัสนัดหมาย, ชื่อแพทย์..."
            data-testid="appointment-search-input"
            className="w-full border border-[#E1E5E2] bg-white rounded-lg pl-10 pr-4 py-2.5 text-sm focus:border-[#1E3F33] focus:ring-1 focus:ring-[#1E3F33] focus:outline-none"
          />
        </div>
        <input
          type="date"
          value={date}
          onChange={(e) => { setDate(e.target.value); setPage(1); }}
          data-testid="appointment-date-filter"
          className="border border-[#E1E5E2] bg-white rounded-lg px-4 py-2.5 text-sm focus:border-[#1E3F33] focus:outline-none"
        />
        <button
          onClick={() => { setDate(""); setPage(1); }}
          className="border border-[#E1E5E2] bg-white text-[#546E62] rounded-lg px-4 py-2.5 text-sm hover:bg-[#F2F0EB]"
          data-testid="appointment-alldates-btn"
        >
          ทุกวัน
        </button>
        <select
          value={status}
          onChange={(e) => { setStatus(e.target.value); setPage(1); }}
          data-testid="appointment-status-filter"
          className="border border-[#E1E5E2] bg-white rounded-lg px-4 py-2.5 text-sm focus:border-[#1E3F33] focus:outline-none"
        >
          <option value="">สถานะทั้งหมด</option>
          {Object.entries(STATUS_LABELS).map(([k, v]) => <option key={k} value={k}>{v}</option>)}
        </select>
      </div>

      {/* Table */}
      <div className="bg-white border border-[#E1E5E2] rounded-lg shadow-sm overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="text-left text-xs uppercase tracking-wider text-[#546E62] border-b border-[#E1E5E2] bg-[#F2F0EB]/50">
              <th className="px-5 py-3 font-semibold">รหัสนัด</th>
              <th className="px-5 py-3 font-semibold">วันที่ / เวลา</th>
              <th className="px-5 py-3 font-semibold">ผู้ป่วย</th>
              <th className="px-5 py-3 font-semibold">แพทย์</th>
              <th className="px-5 py-3 font-semibold">แผนก</th>
              <th className="px-5 py-3 font-semibold">อาการ</th>
              <th className="px-5 py-3 font-semibold">สถานะ</th>
              {canWrite && <th className="px-5 py-3 font-semibold">จัดการ</th>}
            </tr>
          </thead>
          <tbody>
            {loading && (
              <tr><td colSpan={8} className="px-5 py-10 text-center text-[#546E62]">กำลังโหลด...</td></tr>
            )}
            {!loading && data.items.length === 0 && (
              <tr><td colSpan={8} className="px-5 py-10 text-center text-[#546E62]" data-testid="appointments-empty">ไม่พบนัดหมาย</td></tr>
            )}
            {!loading && data.items.map((apt) => (
              <tr key={apt.id} data-testid="appointment-list-row" className="border-b border-[#E1E5E2] last:border-0 hover:bg-[#F2F0EB]/50 transition-colors">
                <td className="px-5 py-3 font-mono text-xs text-[#1E3F33] font-semibold">{apt.appointment_number}</td>
                <td className="px-5 py-3">
                  <div className="text-xs text-[#546E62]">{formatThaiDate(apt.appointment_date)}</div>
                  <div className="font-mono font-semibold">{apt.appointment_time}</div>
                </td>
                <td className="px-5 py-3">
                  <div className="font-medium">{apt.patient_name}</div>
                  <div className="text-xs text-[#546E62] font-mono">{apt.patient_number}</div>
                </td>
                <td className="px-5 py-3">{apt.doctor_name}</td>
                <td className="px-5 py-3">{apt.department}</td>
                <td className="px-5 py-3 max-w-[200px] truncate text-[#546E62]">{apt.reason || "-"}</td>
                <td className="px-5 py-3">
                  <span className={`text-xs rounded-full px-2.5 py-1 whitespace-nowrap font-medium ${STATUS_BADGES[apt.status]}`} data-testid={`appointment-status-${apt.status}`}>
                    {STATUS_LABELS[apt.status]}
                  </span>
                </td>
                {canWrite && (
                  <td className="px-5 py-3">
                    {NEXT_STATUSES[apt.status]?.length > 0 ? (
                      <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                          <button className="text-xs border border-[#E1E5E2] rounded-lg px-3 py-1.5 bg-white hover:bg-[#F2F0EB] font-medium" data-testid="appointment-action-btn">
                            เปลี่ยนสถานะ
                          </button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent align="end">
                          {NEXT_STATUSES[apt.status].map((s) => (
                            <DropdownMenuItem key={s} onClick={() => changeStatus(apt.id, s)} data-testid={`status-option-${s}`}>
                              {STATUS_LABELS[s]}
                            </DropdownMenuItem>
                          ))}
                        </DropdownMenuContent>
                      </DropdownMenu>
                    ) : (
                      <span className="text-xs text-[#546E62]">—</span>
                    )}
                  </td>
                )}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      {data.pages > 1 && (
        <div className="flex items-center justify-between">
          <span className="text-sm text-[#546E62]">หน้า {data.page} จาก {data.pages}</span>
          <div className="flex gap-2">
            <button disabled={page <= 1} onClick={() => setPage(page - 1)} className="p-2 border border-[#E1E5E2] rounded-lg bg-white disabled:opacity-40 hover:bg-[#F2F0EB]">
              <ChevronLeft className="w-4 h-4" />
            </button>
            <button disabled={page >= data.pages} onClick={() => setPage(page + 1)} className="p-2 border border-[#E1E5E2] rounded-lg bg-white disabled:opacity-40 hover:bg-[#F2F0EB]">
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
