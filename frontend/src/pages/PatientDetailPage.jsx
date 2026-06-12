import { useCallback, useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { ArrowLeft, Pencil, Plus, AlertTriangle, Phone, ShieldCheck, Trash2 } from "lucide-react";
import { toast } from "sonner";
import api, { formatApiError } from "@/lib/api";
import { useAuth } from "@/context/AuthContext";
import { GENDER_LABELS, MARITAL_LABELS, STATUS_LABELS, STATUS_BADGES } from "@/lib/constants";
import { calcAge, formatThaiDate, formatThaiDateTime } from "@/lib/helpers";
import {
  Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger,
} from "@/components/ui/dialog";

const inputCls =
  "w-full border border-[#E1E5E2] bg-white rounded-lg px-3 py-2 text-sm focus:border-[#1E3F33] focus:ring-1 focus:ring-[#1E3F33] focus:outline-none";

const Card = ({ title, children, action }) => (
  <div className="bg-white border border-[#E1E5E2] rounded-lg p-5 shadow-sm">
    <div className="flex items-center justify-between mb-4">
      <h3 className="font-heading text-lg font-medium text-[#0F1F19]">{title}</h3>
      {action}
    </div>
    {children}
  </div>
);

const InfoRow = ({ label, value }) => (
  <div className="flex justify-between py-1.5 border-b border-[#E1E5E2]/60 last:border-0">
    <span className="text-sm text-[#546E62]">{label}</span>
    <span className="text-sm font-medium text-[#0F1F19] text-right">{value || "-"}</span>
  </div>
);

const CAN_WRITE = ["admin", "doctor", "nurse"];

export default function PatientDetailPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [patient, setPatient] = useState(null);
  const [appointments, setAppointments] = useState([]);
  const [vitalsOpen, setVitalsOpen] = useState(false);
  const [vitals, setVitals] = useState({ temperature: "", bp_systolic: "", bp_diastolic: "", heart_rate: "", respiratory_rate: "", weight: "", height: "" });
  const [saving, setSaving] = useState(false);

  const load = useCallback(() => {
    api.get(`/patients/${id}`).then((res) => setPatient(res.data)).catch(() => {
      toast.error("ไม่พบข้อมูลผู้ป่วย");
      navigate("/patients");
    });
    api.get("/appointments", { params: { patient_id: id, limit: 50 } }).then((res) => setAppointments(res.data.items));
  }, [id, navigate]);

  useEffect(() => { load(); }, [load]);

  const submitVitals = async (e) => {
    e.preventDefault();
    setSaving(true);
    try {
      const payload = Object.fromEntries(
        Object.entries(vitals).filter(([, v]) => v !== "").map(([k, v]) => [k, Number(v)])
      );
      await api.post(`/patients/${id}/vitals`, payload);
      toast.success("บันทึกสัญญาณชีพสำเร็จ");
      setVitalsOpen(false);
      setVitals({ temperature: "", bp_systolic: "", bp_diastolic: "", heart_rate: "", respiratory_rate: "", weight: "", height: "" });
      load();
    } catch (err) {
      toast.error(formatApiError(err));
    } finally {
      setSaving(false);
    }
  };

  const deletePatient = async () => {
    if (!window.confirm("ยืนยันการลบข้อมูลผู้ป่วยรายนี้?")) return;
    try {
      await api.delete(`/patients/${id}`);
      toast.success("ลบข้อมูลผู้ป่วยสำเร็จ");
      navigate("/patients");
    } catch (err) {
      toast.error(formatApiError(err));
    }
  };

  if (!patient) return <div className="text-[#546E62]">กำลังโหลด...</div>;

  const canWrite = CAN_WRITE.includes(user?.role);
  const sortedVitals = [...(patient.vitals || [])].sort((a, b) => (b.recorded_at > a.recorded_at ? 1 : -1));

  return (
    <div className="space-y-6" data-testid="patient-detail-page">
      <div>
        <Link to="/patients" className="inline-flex items-center gap-1 text-sm text-[#546E62] hover:text-[#1E3F33] mb-2">
          <ArrowLeft className="w-4 h-4" /> รายชื่อผู้ป่วย
        </Link>
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="flex items-center gap-4">
            <div className="w-14 h-14 rounded-full bg-[#1E3F33] text-white flex items-center justify-center text-xl font-heading font-medium">
              {patient.first_name?.charAt(0)}
            </div>
            <div>
              <h1 className="font-heading text-2xl md:text-3xl font-medium tracking-tight text-[#0F1F19]" data-testid="patient-detail-name">
                {patient.first_name} {patient.last_name}
              </h1>
              <div className="flex flex-wrap items-center gap-3 text-sm text-[#546E62] mt-1">
                <span className="font-mono text-[#1E3F33] font-semibold">{patient.patient_number}</span>
                <span>{GENDER_LABELS[patient.gender]}</span>
                <span>{calcAge(patient.date_of_birth)} ปี</span>
                {patient.blood_type && (
                  <span className="bg-[#CC5A3A]/10 text-[#CC5A3A] rounded-full px-2.5 py-0.5 text-xs font-semibold">
                    เลือด {patient.blood_type}
                  </span>
                )}
              </div>
            </div>
          </div>
          {canWrite && (
            <div className="flex gap-2">
              <Link
                to={`/patients/${id}/edit`}
                data-testid="edit-patient-btn"
                className="inline-flex items-center gap-2 bg-[#1E3F33] text-white hover:bg-[#2C5A48] rounded-lg px-4 py-2 text-sm font-medium transition-colors"
              >
                <Pencil className="w-4 h-4" /> แก้ไขข้อมูล
              </Link>
              {user?.role === "admin" && (
                <button onClick={deletePatient} data-testid="delete-patient-btn" className="inline-flex items-center gap-2 border border-[#D34228]/30 text-[#D34228] hover:bg-[#D34228]/5 rounded-lg px-4 py-2 text-sm font-medium transition-colors">
                  <Trash2 className="w-4 h-4" /> ลบ
                </button>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Allergy alert */}
      {patient.allergies?.length > 0 && (
        <div className="bg-[#D34228]/10 border border-[#D34228]/30 rounded-lg p-4 flex items-start gap-3" data-testid="allergy-alert">
          <AlertTriangle className="w-5 h-5 text-[#D34228] mt-0.5" />
          <div>
            <div className="font-semibold text-[#D34228] text-sm">ประวัติแพ้ยา/สารก่อภูมิแพ้</div>
            <div className="text-sm text-[#0F1F19] mt-1">
              {patient.allergies.map((a, i) => (
                <span key={i} className="inline-block mr-3">
                  <strong>{a.allergen}</strong>
                  {a.severity && ` (${a.severity})`}
                  {a.reaction && ` — ${a.reaction}`}
                </span>
              ))}
            </div>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-12 gap-4 md:gap-6">
        {/* Left column */}
        <div className="md:col-span-4 space-y-4 md:space-y-6">
          <Card title="ข้อมูลส่วนตัว">
            <InfoRow label="วันเกิด" value={formatThaiDate(patient.date_of_birth)} />
            <InfoRow label="เลขบัตรประชาชน" value={patient.national_id} />
            <InfoRow label="สถานภาพ" value={MARITAL_LABELS[patient.marital_status]} />
            <InfoRow label="อาชีพ" value={patient.occupation} />
            <InfoRow label="สัญชาติ" value={patient.nationality} />
          </Card>
          <Card title="ข้อมูลติดต่อ">
            <InfoRow label="โทรศัพท์" value={patient.phone} />
            <InfoRow label="อีเมล" value={patient.email} />
            <InfoRow label="จังหวัด" value={patient.address?.state} />
            <InfoRow label="ที่อยู่" value={[patient.address?.street, patient.address?.city].filter(Boolean).join(" ")} />
          </Card>
          <Card title="ผู้ติดต่อฉุกเฉิน">
            {patient.emergency_contact?.name ? (
              <>
                <InfoRow label="ชื่อ" value={patient.emergency_contact.name} />
                <InfoRow label="ความสัมพันธ์" value={patient.emergency_contact.relationship} />
                <InfoRow label="โทรศัพท์" value={patient.emergency_contact.phone} />
              </>
            ) : (
              <p className="text-sm text-[#546E62] flex items-center gap-2"><Phone className="w-4 h-4" /> ไม่มีข้อมูล</p>
            )}
          </Card>
          <Card title="สิทธิการรักษา">
            {patient.insurance?.provider ? (
              <>
                <InfoRow label="สิทธิ" value={patient.insurance.provider} />
                <InfoRow label="เลขกรมธรรม์" value={patient.insurance.policy_number} />
                <InfoRow label="ความคุ้มครอง" value={patient.insurance.coverage_type} />
              </>
            ) : (
              <p className="text-sm text-[#546E62] flex items-center gap-2"><ShieldCheck className="w-4 h-4" /> ไม่มีข้อมูล</p>
            )}
          </Card>
        </div>

        {/* Right column */}
        <div className="md:col-span-8 space-y-4 md:space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 md:gap-6">
            <Card title="โรคประจำตัว">
              {patient.chronic_conditions?.length > 0 ? (
                <ul className="space-y-2">
                  {patient.chronic_conditions.map((c, i) => (
                    <li key={i} className="flex justify-between items-center text-sm border-b border-[#E1E5E2]/60 last:border-0 pb-2 last:pb-0">
                      <span className="font-medium text-[#0F1F19]">{c.condition}</span>
                      <span className="text-xs text-[#546E62]">{c.diagnosed_date ? formatThaiDate(c.diagnosed_date) : ""}</span>
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="text-sm text-[#546E62]">ไม่มีโรคประจำตัว</p>
              )}
            </Card>
            <Card title="ยาที่ใช้ประจำ">
              {patient.current_medications?.length > 0 ? (
                <ul className="space-y-2">
                  {patient.current_medications.map((m, i) => (
                    <li key={i} className="text-sm border-b border-[#E1E5E2]/60 last:border-0 pb-2 last:pb-0">
                      <span className="font-medium text-[#0F1F19]">{m.drug_name}</span>
                      <span className="text-xs text-[#546E62] ml-2">{m.dosage} • {m.frequency}</span>
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="text-sm text-[#546E62]">ไม่มียาประจำ</p>
              )}
            </Card>
          </div>

          {/* Vitals */}
          <Card
            title="สัญญาณชีพ (Vital Signs)"
            action={
              canWrite && (
                <Dialog open={vitalsOpen} onOpenChange={setVitalsOpen}>
                  <DialogTrigger asChild>
                    <button data-testid="add-vitals-btn" className="inline-flex items-center gap-1.5 text-sm bg-[#1E3F33] text-white hover:bg-[#2C5A48] rounded-lg px-3 py-1.5 font-medium transition-colors">
                      <Plus className="w-3.5 h-3.5" /> บันทึกสัญญาณชีพ
                    </button>
                  </DialogTrigger>
                  <DialogContent>
                    <DialogHeader>
                      <DialogTitle className="font-heading">บันทึกสัญญาณชีพ</DialogTitle>
                      <DialogDescription>กรอกค่าที่วัดได้ ช่องที่ไม่ได้วัดเว้นว่างได้</DialogDescription>
                    </DialogHeader>
                    <form onSubmit={submitVitals} className="grid grid-cols-2 gap-3" data-testid="vitals-form">
                      <div>
                        <label className="text-xs text-[#546E62]">อุณหภูมิ (°C)</label>
                        <input type="number" step="0.1" value={vitals.temperature} onChange={(e) => setVitals({ ...vitals, temperature: e.target.value })} className={inputCls} data-testid="vitals-temperature-input" />
                      </div>
                      <div>
                        <label className="text-xs text-[#546E62]">ชีพจร (ครั้ง/นาที)</label>
                        <input type="number" value={vitals.heart_rate} onChange={(e) => setVitals({ ...vitals, heart_rate: e.target.value })} className={inputCls} data-testid="vitals-heartrate-input" />
                      </div>
                      <div>
                        <label className="text-xs text-[#546E62]">ความดันตัวบน (mmHg)</label>
                        <input type="number" value={vitals.bp_systolic} onChange={(e) => setVitals({ ...vitals, bp_systolic: e.target.value })} className={inputCls} data-testid="vitals-bpsys-input" />
                      </div>
                      <div>
                        <label className="text-xs text-[#546E62]">ความดันตัวล่าง (mmHg)</label>
                        <input type="number" value={vitals.bp_diastolic} onChange={(e) => setVitals({ ...vitals, bp_diastolic: e.target.value })} className={inputCls} data-testid="vitals-bpdia-input" />
                      </div>
                      <div>
                        <label className="text-xs text-[#546E62]">อัตราหายใจ (ครั้ง/นาที)</label>
                        <input type="number" value={vitals.respiratory_rate} onChange={(e) => setVitals({ ...vitals, respiratory_rate: e.target.value })} className={inputCls} />
                      </div>
                      <div>
                        <label className="text-xs text-[#546E62]">น้ำหนัก (กก.)</label>
                        <input type="number" step="0.1" value={vitals.weight} onChange={(e) => setVitals({ ...vitals, weight: e.target.value })} className={inputCls} />
                      </div>
                      <div>
                        <label className="text-xs text-[#546E62]">ส่วนสูง (ซม.)</label>
                        <input type="number" step="0.1" value={vitals.height} onChange={(e) => setVitals({ ...vitals, height: e.target.value })} className={inputCls} />
                      </div>
                      <div className="col-span-2 mt-2">
                        <button type="submit" disabled={saving} data-testid="vitals-submit-btn" className="w-full bg-[#1E3F33] text-white hover:bg-[#2C5A48] rounded-lg py-2.5 font-medium transition-colors disabled:opacity-60">
                          บันทึก
                        </button>
                      </div>
                    </form>
                  </DialogContent>
                </Dialog>
              )
            }
          >
            {sortedVitals.length > 0 ? (
              <div className="overflow-x-auto">
                <table className="w-full text-sm" data-testid="vitals-table">
                  <thead>
                    <tr className="text-left text-xs uppercase tracking-wider text-[#546E62] border-b border-[#E1E5E2]">
                      <th className="py-2 pr-3 font-semibold">วันที่</th>
                      <th className="py-2 pr-3 font-semibold">อุณหภูมิ</th>
                      <th className="py-2 pr-3 font-semibold">ความดัน</th>
                      <th className="py-2 pr-3 font-semibold">ชีพจร</th>
                      <th className="py-2 pr-3 font-semibold">น้ำหนัก</th>
                      <th className="py-2 pr-3 font-semibold">ผู้บันทึก</th>
                    </tr>
                  </thead>
                  <tbody>
                    {sortedVitals.map((v) => (
                      <tr key={v.id} className="border-b border-[#E1E5E2]/60 last:border-0">
                        <td className="py-2 pr-3 text-xs text-[#546E62]">{formatThaiDateTime(v.recorded_at)}</td>
                        <td className="py-2 pr-3">{v.temperature ? `${v.temperature}°C` : "-"}</td>
                        <td className="py-2 pr-3">{v.bp_systolic ? `${v.bp_systolic}/${v.bp_diastolic}` : "-"}</td>
                        <td className="py-2 pr-3">{v.heart_rate || "-"}</td>
                        <td className="py-2 pr-3">{v.weight ? `${v.weight} กก.` : "-"}</td>
                        <td className="py-2 pr-3 text-xs">{v.recorded_by}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <p className="text-sm text-[#546E62]">ยังไม่มีการบันทึกสัญญาณชีพ</p>
            )}
          </Card>

          {/* Appointments history */}
          <Card title="ประวัตินัดหมาย">
            {appointments.length > 0 ? (
              <div className="space-y-3" data-testid="patient-appointments">
                {appointments.map((apt) => (
                  <div key={apt.id} className="flex items-center gap-3 border-b border-[#E1E5E2]/60 last:border-0 pb-3 last:pb-0">
                    <div className="text-center w-16">
                      <div className="text-xs text-[#546E62]">{formatThaiDate(apt.appointment_date)}</div>
                      <div className="font-mono text-sm font-semibold text-[#1E3F33]">{apt.appointment_time}</div>
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="text-sm font-medium text-[#0F1F19] truncate">{apt.reason || "ตรวจรักษา"}</div>
                      <div className="text-xs text-[#546E62]">{apt.doctor_name} • {apt.department}</div>
                    </div>
                    <span className={`text-[10px] rounded-full px-2 py-0.5 whitespace-nowrap ${STATUS_BADGES[apt.status]}`}>
                      {STATUS_LABELS[apt.status]}
                    </span>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-sm text-[#546E62]">ไม่มีประวัตินัดหมาย</p>
            )}
          </Card>
        </div>
      </div>
    </div>
  );
}
