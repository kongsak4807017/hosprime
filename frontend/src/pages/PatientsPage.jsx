import { useCallback, useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Search, Plus, ChevronLeft, ChevronRight } from "lucide-react";
import api from "@/lib/api";
import { useAuth } from "@/context/AuthContext";
import { GENDER_LABELS, BLOOD_TYPES } from "@/lib/constants";
import { calcAge, formatThaiDate } from "@/lib/helpers";

const CAN_WRITE = ["admin", "doctor", "nurse"];

export default function PatientsPage() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [data, setData] = useState({ items: [], total: 0, page: 1, pages: 1 });
  const [search, setSearch] = useState("");
  const [gender, setGender] = useState("");
  const [bloodType, setBloodType] = useState("");
  const [page, setPage] = useState(1);
  const [loading, setLoading] = useState(true);

  const fetchPatients = useCallback(async () => {
    setLoading(true);
    try {
      const { data } = await api.get("/patients", {
        params: { search, gender, blood_type: bloodType, page, limit: 15 },
      });
      setData(data);
    } finally {
      setLoading(false);
    }
  }, [search, gender, bloodType, page]);

  useEffect(() => {
    const t = setTimeout(fetchPatients, search ? 350 : 0);
    return () => clearTimeout(t);
  }, [fetchPatients, search]);

  return (
    <div className="space-y-6" data-testid="patients-page">
      <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
        <div>
          <div className="text-xs font-semibold uppercase tracking-[0.2em] text-[#546E62] mb-1">เวชระเบียน</div>
          <h1 className="font-heading text-3xl md:text-4xl font-medium tracking-tight text-[#0F1F19]">
            ผู้ป่วย <span className="text-[#546E62] text-xl font-normal">({data.total} ราย)</span>
          </h1>
        </div>
        {CAN_WRITE.includes(user?.role) && (
          <Link
            to="/patients/new"
            data-testid="add-patient-btn"
            className="inline-flex items-center gap-2 bg-[#1E3F33] text-white hover:bg-[#2C5A48] rounded-lg px-5 py-2.5 font-medium transition-colors"
          >
            <Plus className="w-4 h-4" /> ลงทะเบียนผู้ป่วยใหม่
          </Link>
        )}
      </div>

      {/* Filters */}
      <div className="flex flex-col md:flex-row gap-3">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[#546E62]" />
          <input
            value={search}
            onChange={(e) => { setSearch(e.target.value); setPage(1); }}
            placeholder="ค้นหาด้วยชื่อ, รหัสผู้ป่วย, เบอร์โทร, เลขบัตรประชาชน..."
            data-testid="patient-search-input"
            className="w-full border border-[#E1E5E2] bg-white rounded-lg pl-10 pr-4 py-2.5 text-sm focus:border-[#1E3F33] focus:ring-1 focus:ring-[#1E3F33] focus:outline-none"
          />
        </div>
        <select
          value={gender}
          onChange={(e) => { setGender(e.target.value); setPage(1); }}
          data-testid="patient-gender-filter"
          className="border border-[#E1E5E2] bg-white rounded-lg px-4 py-2.5 text-sm focus:border-[#1E3F33] focus:outline-none"
        >
          <option value="">เพศทั้งหมด</option>
          <option value="male">ชาย</option>
          <option value="female">หญิง</option>
          <option value="other">อื่นๆ</option>
        </select>
        <select
          value={bloodType}
          onChange={(e) => { setBloodType(e.target.value); setPage(1); }}
          data-testid="patient-bloodtype-filter"
          className="border border-[#E1E5E2] bg-white rounded-lg px-4 py-2.5 text-sm focus:border-[#1E3F33] focus:outline-none"
        >
          <option value="">กรุ๊ปเลือดทั้งหมด</option>
          {BLOOD_TYPES.map((b) => <option key={b} value={b}>{b}</option>)}
        </select>
      </div>

      {/* Table */}
      <div className="bg-white border border-[#E1E5E2] rounded-lg shadow-sm overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="text-left text-xs uppercase tracking-wider text-[#546E62] border-b border-[#E1E5E2] bg-[#F2F0EB]/50">
              <th className="px-5 py-3 font-semibold">รหัสผู้ป่วย</th>
              <th className="px-5 py-3 font-semibold">ชื่อ-นามสกุล</th>
              <th className="px-5 py-3 font-semibold">เพศ</th>
              <th className="px-5 py-3 font-semibold">อายุ</th>
              <th className="px-5 py-3 font-semibold">กรุ๊ปเลือด</th>
              <th className="px-5 py-3 font-semibold">โทรศัพท์</th>
              <th className="px-5 py-3 font-semibold">แพ้ยา</th>
              <th className="px-5 py-3 font-semibold">ลงทะเบียน</th>
            </tr>
          </thead>
          <tbody>
            {loading && (
              <tr><td colSpan={8} className="px-5 py-10 text-center text-[#546E62]">กำลังโหลด...</td></tr>
            )}
            {!loading && data.items.length === 0 && (
              <tr><td colSpan={8} className="px-5 py-10 text-center text-[#546E62]" data-testid="patients-empty">ไม่พบข้อมูลผู้ป่วย</td></tr>
            )}
            {!loading && data.items.map((p) => (
              <tr
                key={p.id}
                onClick={() => navigate(`/patients/${p.id}`)}
                data-testid="patient-list-row"
                className="border-b border-[#E1E5E2] last:border-0 hover:bg-[#F2F0EB]/50 transition-colors cursor-pointer"
              >
                <td className="px-5 py-3 font-mono text-xs text-[#1E3F33] font-semibold">{p.patient_number}</td>
                <td className="px-5 py-3 font-medium">{p.first_name} {p.last_name}</td>
                <td className="px-5 py-3">{GENDER_LABELS[p.gender] || p.gender}</td>
                <td className="px-5 py-3">{calcAge(p.date_of_birth)} ปี</td>
                <td className="px-5 py-3">{p.blood_type || "-"}</td>
                <td className="px-5 py-3">{p.phone}</td>
                <td className="px-5 py-3">
                  {p.allergies?.length > 0 ? (
                    <span className="bg-[#D34228]/10 text-[#D34228] border border-[#D34228]/20 rounded-full px-2.5 py-0.5 text-xs font-medium">
                      แพ้ {p.allergies.length} รายการ
                    </span>
                  ) : (
                    <span className="text-[#546E62] text-xs">ไม่มี</span>
                  )}
                </td>
                <td className="px-5 py-3 text-xs text-[#546E62]">{formatThaiDate(p.created_at)}</td>
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
            <button
              disabled={page <= 1}
              onClick={() => setPage(page - 1)}
              data-testid="patients-prev-page"
              className="p-2 border border-[#E1E5E2] rounded-lg bg-white disabled:opacity-40 hover:bg-[#F2F0EB]"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
            <button
              disabled={page >= data.pages}
              onClick={() => setPage(page + 1)}
              data-testid="patients-next-page"
              className="p-2 border border-[#E1E5E2] rounded-lg bg-white disabled:opacity-40 hover:bg-[#F2F0EB]"
            >
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
