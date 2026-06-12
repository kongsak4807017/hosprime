import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Users, CalendarClock, CheckCircle2, Stethoscope, ArrowRight } from "lucide-react";
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from "recharts";
import api from "@/lib/api";
import { useAuth } from "@/context/AuthContext";
import { STATUS_LABELS, STATUS_BADGES, GENDER_LABELS } from "@/lib/constants";
import { calcAge, formatThaiDate } from "@/lib/helpers";

const KpiCard = ({ icon: Icon, label, value, sub, testId }) => (
  <div className="bg-white border border-[#E1E5E2] rounded-lg p-5 shadow-sm" data-testid={testId}>
    <div className="flex items-center justify-between mb-3">
      <span className="text-xs font-semibold uppercase tracking-[0.15em] text-[#546E62]">{label}</span>
      <div className="w-8 h-8 rounded-lg bg-[#F2F0EB] flex items-center justify-center">
        <Icon className="w-4 h-4 text-[#1E3F33]" />
      </div>
    </div>
    <div className="font-heading text-3xl font-medium text-[#0F1F19]">{value}</div>
    {sub && <div className="text-xs text-[#546E62] mt-1">{sub}</div>}
  </div>
);

export default function DashboardPage() {
  const { user } = useAuth();
  const [stats, setStats] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    if (user?.role === "patient") return;
    api
      .get("/dashboard/stats")
      .then((res) => setStats(res.data))
      .catch(() => setError("ไม่สามารถโหลดข้อมูลแดชบอร์ดได้"));
  }, [user]);

  if (user?.role === "patient") {
    return (
      <div className="max-w-2xl" data-testid="patient-portal-placeholder">
        <h1 className="font-heading text-3xl font-medium text-[#0F1F19] mb-2">สวัสดี, {user.full_name}</h1>
        <div className="bg-white border border-[#E1E5E2] rounded-lg p-8 mt-6 text-center">
          <p className="text-[#546E62]">พอร์ทัลผู้ป่วย (ดูประวัติ จองนัดหมาย ผลแล็บ) จะเปิดใช้งานในเฟสถัดไป</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6" data-testid="dashboard-page">
      <div>
        <div className="text-xs font-semibold uppercase tracking-[0.2em] text-[#546E62] mb-1">ภาพรวมโรงพยาบาล</div>
        <h1 className="font-heading text-3xl md:text-4xl font-medium tracking-tight text-[#0F1F19]">แดชบอร์ด</h1>
      </div>

      {error && <div className="bg-[#D34228]/10 text-[#D34228] rounded-lg px-4 py-3 text-sm">{error}</div>}

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6">
        <KpiCard icon={Users} label="ผู้ป่วยทั้งหมด" value={stats?.total_patients ?? "–"} sub={`ใหม่เดือนนี้ ${stats?.new_patients_this_month ?? 0} ราย`} testId="kpi-total-patients" />
        <KpiCard icon={CalendarClock} label="นัดหมายวันนี้" value={stats?.appointments_today ?? "–"} sub={`รอตรวจ ${(stats?.appointments_today ?? 0) - (stats?.completed_today ?? 0)} ราย`} testId="kpi-appointments-today" />
        <KpiCard icon={CheckCircle2} label="ตรวจเสร็จวันนี้" value={stats?.completed_today ?? "–"} testId="kpi-completed-today" />
        <KpiCard icon={Stethoscope} label="แพทย์ในระบบ" value={stats?.total_doctors ?? "–"} testId="kpi-total-doctors" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 md:gap-6">
        {/* Trend chart */}
        <div className="lg:col-span-2 bg-white border border-[#E1E5E2] rounded-lg p-5 shadow-sm" data-testid="appointments-trend-chart">
          <h3 className="font-heading text-lg font-medium text-[#0F1F19] mb-4">แนวโน้มนัดหมาย 7 วันล่าสุด</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={stats?.appointments_trend || []}>
                <defs>
                  <linearGradient id="trendFill" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#1E3F33" stopOpacity={0.25} />
                    <stop offset="100%" stopColor="#1E3F33" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#E1E5E2" vertical={false} />
                <XAxis
                  dataKey="date"
                  tickFormatter={(d) => new Date(d).toLocaleDateString("th-TH", { day: "numeric", month: "short" })}
                  tick={{ fontSize: 12, fill: "#546E62" }}
                  axisLine={false}
                  tickLine={false}
                />
                <YAxis allowDecimals={false} tick={{ fontSize: 12, fill: "#546E62" }} axisLine={false} tickLine={false} width={28} />
                <Tooltip
                  labelFormatter={(d) => formatThaiDate(d)}
                  formatter={(v) => [`${v} นัดหมาย`, ""]}
                  contentStyle={{ borderRadius: 8, border: "1px solid #E1E5E2", fontFamily: "inherit" }}
                />
                <Area type="monotone" dataKey="count" stroke="#1E3F33" strokeWidth={2} fill="url(#trendFill)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Upcoming appointments */}
        <div className="bg-white border border-[#E1E5E2] rounded-lg p-5 shadow-sm" data-testid="upcoming-appointments">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-heading text-lg font-medium text-[#0F1F19]">คิววันนี้</h3>
            <Link to="/appointments" className="text-xs text-[#1E3F33] font-medium flex items-center gap-1 hover:underline">
              ดูทั้งหมด <ArrowRight className="w-3 h-3" />
            </Link>
          </div>
          <div className="space-y-3">
            {(stats?.upcoming_appointments || []).length === 0 && (
              <p className="text-sm text-[#546E62]">ไม่มีนัดหมายที่รอดำเนินการวันนี้</p>
            )}
            {(stats?.upcoming_appointments || []).map((apt) => (
              <div key={apt.id} className="flex items-center gap-3 border-b border-[#E1E5E2] last:border-0 pb-3 last:pb-0">
                <div className="font-mono text-sm font-semibold text-[#1E3F33] w-12">{apt.appointment_time}</div>
                <div className="min-w-0 flex-1">
                  <div className="text-sm font-medium text-[#0F1F19] truncate">{apt.patient_name}</div>
                  <div className="text-xs text-[#546E62] truncate">{apt.doctor_name}</div>
                </div>
                <span className={`text-[10px] rounded-full px-2 py-0.5 whitespace-nowrap ${STATUS_BADGES[apt.status]}`}>
                  {STATUS_LABELS[apt.status]}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Recent patients */}
      <div className="bg-white border border-[#E1E5E2] rounded-lg shadow-sm" data-testid="recent-patients">
        <div className="flex items-center justify-between p-5 pb-3">
          <h3 className="font-heading text-lg font-medium text-[#0F1F19]">ผู้ป่วยลงทะเบียนล่าสุด</h3>
          <Link to="/patients" className="text-xs text-[#1E3F33] font-medium flex items-center gap-1 hover:underline">
            ดูทั้งหมด <ArrowRight className="w-3 h-3" />
          </Link>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left text-xs uppercase tracking-wider text-[#546E62] border-b border-[#E1E5E2]">
                <th className="px-5 py-2 font-semibold">รหัสผู้ป่วย</th>
                <th className="px-5 py-2 font-semibold">ชื่อ-นามสกุล</th>
                <th className="px-5 py-2 font-semibold">เพศ</th>
                <th className="px-5 py-2 font-semibold">อายุ</th>
                <th className="px-5 py-2 font-semibold">กรุ๊ปเลือด</th>
                <th className="px-5 py-2 font-semibold">โทรศัพท์</th>
              </tr>
            </thead>
            <tbody>
              {(stats?.recent_patients || []).map((p) => (
                <tr key={p.id} className="border-b border-[#E1E5E2] last:border-0 hover:bg-[#F2F0EB]/50 transition-colors">
                  <td className="px-5 py-3 font-mono text-xs text-[#1E3F33]">
                    <Link to={`/patients/${p.id}`} className="hover:underline">{p.patient_number}</Link>
                  </td>
                  <td className="px-5 py-3 font-medium">{p.first_name} {p.last_name}</td>
                  <td className="px-5 py-3">{GENDER_LABELS[p.gender] || p.gender}</td>
                  <td className="px-5 py-3">{calcAge(p.date_of_birth)} ปี</td>
                  <td className="px-5 py-3">{p.blood_type || "-"}</td>
                  <td className="px-5 py-3">{p.phone}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
