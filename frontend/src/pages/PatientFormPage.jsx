import { useEffect, useState } from "react";
import { useNavigate, useParams, Link } from "react-router-dom";
import { ArrowLeft, Plus, Trash2, Loader2 } from "lucide-react";
import { toast } from "sonner";
import api, { formatApiError } from "@/lib/api";
import { BLOOD_TYPES } from "@/lib/constants";

const inputCls =
  "w-full border border-[#E1E5E2] bg-white rounded-lg px-4 py-2.5 text-sm text-[#0F1F19] placeholder:text-[#546E62]/60 focus:border-[#1E3F33] focus:ring-1 focus:ring-[#1E3F33] focus:outline-none transition-all";

const Field = ({ label, required, children }) => (
  <div>
    <label className="block text-sm font-medium text-[#0F1F19] mb-1.5">
      {label} {required && <span className="text-[#D34228]">*</span>}
    </label>
    {children}
  </div>
);

const Section = ({ title, children }) => (
  <div className="bg-white border border-[#E1E5E2] rounded-lg p-6 shadow-sm">
    <h3 className="font-heading text-lg font-medium text-[#0F1F19] mb-5">{title}</h3>
    {children}
  </div>
);

const EMPTY = {
  first_name: "", last_name: "", date_of_birth: "", gender: "male", national_id: "",
  blood_type: "", marital_status: "", occupation: "", nationality: "ไทย",
  phone: "", email: "",
  address: { street: "", city: "", state: "", postal_code: "" },
  emergency_contact: { name: "", relationship: "", phone: "" },
  insurance: { provider: "", policy_number: "", coverage_type: "" },
  allergies: [], chronic_conditions: [], current_medications: [], notes: "",
};

export default function PatientFormPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const isEdit = Boolean(id);
  const [form, setForm] = useState(EMPTY);
  const [saving, setSaving] = useState(false);
  const [loading, setLoading] = useState(isEdit);

  useEffect(() => {
    if (!isEdit) return;
    api.get(`/patients/${id}`).then((res) => {
      const p = res.data;
      setForm({ ...EMPTY, ...p, address: { ...EMPTY.address, ...p.address }, emergency_contact: { ...EMPTY.emergency_contact, ...p.emergency_contact }, insurance: { ...EMPTY.insurance, ...p.insurance } });
      setLoading(false);
    }).catch(() => { toast.error("ไม่พบข้อมูลผู้ป่วย"); navigate("/patients"); });
  }, [id, isEdit, navigate]);

  const set = (key, value) => setForm((f) => ({ ...f, [key]: value }));
  const setNested = (group, key, value) => setForm((f) => ({ ...f, [group]: { ...f[group], [key]: value } }));

  const addItem = (key, item) => setForm((f) => ({ ...f, [key]: [...f[key], item] }));
  const removeItem = (key, idx) => setForm((f) => ({ ...f, [key]: f[key].filter((_, i) => i !== idx) }));
  const setItem = (key, idx, field, value) =>
    setForm((f) => ({ ...f, [key]: f[key].map((it, i) => (i === idx ? { ...it, [field]: value } : it)) }));

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    try {
      const payload = { ...form };
      delete payload.id; delete payload.patient_number; delete payload.vitals;
      delete payload.created_at; delete payload.updated_at; delete payload.created_by; delete payload.is_active;
      if (isEdit) {
        await api.put(`/patients/${id}`, payload);
        toast.success("บันทึกข้อมูลผู้ป่วยสำเร็จ");
        navigate(`/patients/${id}`);
      } else {
        const { data } = await api.post("/patients", payload);
        toast.success(`ลงทะเบียนผู้ป่วยสำเร็จ (${data.patient_number})`);
        navigate(`/patients/${data.id}`);
      }
    } catch (err) {
      toast.error(formatApiError(err));
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <div className="text-[#546E62]">กำลังโหลด...</div>;

  return (
    <div className="max-w-4xl space-y-6" data-testid="patient-form-page">
      <div>
        <Link to={isEdit ? `/patients/${id}` : "/patients"} className="inline-flex items-center gap-1 text-sm text-[#546E62] hover:text-[#1E3F33] mb-2">
          <ArrowLeft className="w-4 h-4" /> กลับ
        </Link>
        <h1 className="font-heading text-3xl font-medium tracking-tight text-[#0F1F19]">
          {isEdit ? "แก้ไขข้อมูลผู้ป่วย" : "ลงทะเบียนผู้ป่วยใหม่"}
        </h1>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        <Section title="ข้อมูลส่วนตัว">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Field label="ชื่อ" required>
              <input required value={form.first_name} onChange={(e) => set("first_name", e.target.value)} className={inputCls} data-testid="patient-firstname-input" />
            </Field>
            <Field label="นามสกุล" required>
              <input required value={form.last_name} onChange={(e) => set("last_name", e.target.value)} className={inputCls} data-testid="patient-lastname-input" />
            </Field>
            <Field label="วันเกิด" required>
              <input type="date" required value={form.date_of_birth} onChange={(e) => set("date_of_birth", e.target.value)} className={inputCls} data-testid="patient-dob-input" />
            </Field>
            <Field label="เพศ" required>
              <select value={form.gender} onChange={(e) => set("gender", e.target.value)} className={inputCls} data-testid="patient-gender-select">
                <option value="male">ชาย</option>
                <option value="female">หญิง</option>
                <option value="other">อื่นๆ</option>
              </select>
            </Field>
            <Field label="เลขบัตรประชาชน">
              <input value={form.national_id} onChange={(e) => set("national_id", e.target.value)} maxLength={13} className={inputCls} data-testid="patient-nationalid-input" />
            </Field>
            <Field label="กรุ๊ปเลือด">
              <select value={form.blood_type} onChange={(e) => set("blood_type", e.target.value)} className={inputCls} data-testid="patient-bloodtype-select">
                <option value="">ไม่ระบุ</option>
                {BLOOD_TYPES.map((b) => <option key={b} value={b}>{b}</option>)}
              </select>
            </Field>
            <Field label="สถานภาพ">
              <select value={form.marital_status} onChange={(e) => set("marital_status", e.target.value)} className={inputCls}>
                <option value="">ไม่ระบุ</option>
                <option value="single">โสด</option>
                <option value="married">สมรส</option>
                <option value="divorced">หย่าร้าง</option>
                <option value="widowed">หม้าย</option>
              </select>
            </Field>
            <Field label="อาชีพ">
              <input value={form.occupation} onChange={(e) => set("occupation", e.target.value)} className={inputCls} />
            </Field>
          </div>
        </Section>

        <Section title="ข้อมูลติดต่อ">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Field label="เบอร์โทรศัพท์" required>
              <input required value={form.phone} onChange={(e) => set("phone", e.target.value)} className={inputCls} data-testid="patient-phone-input" />
            </Field>
            <Field label="อีเมล">
              <input type="email" value={form.email} onChange={(e) => set("email", e.target.value)} className={inputCls} />
            </Field>
            <Field label="ที่อยู่">
              <input value={form.address.street} onChange={(e) => setNested("address", "street", e.target.value)} className={inputCls} />
            </Field>
            <Field label="อำเภอ/เขต">
              <input value={form.address.city} onChange={(e) => setNested("address", "city", e.target.value)} className={inputCls} />
            </Field>
            <Field label="จังหวัด">
              <input value={form.address.state} onChange={(e) => setNested("address", "state", e.target.value)} className={inputCls} />
            </Field>
            <Field label="รหัสไปรษณีย์">
              <input value={form.address.postal_code} onChange={(e) => setNested("address", "postal_code", e.target.value)} className={inputCls} />
            </Field>
          </div>
        </Section>

        <Section title="ผู้ติดต่อฉุกเฉิน">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Field label="ชื่อ-นามสกุล">
              <input value={form.emergency_contact.name} onChange={(e) => setNested("emergency_contact", "name", e.target.value)} className={inputCls} />
            </Field>
            <Field label="ความสัมพันธ์">
              <input value={form.emergency_contact.relationship} onChange={(e) => setNested("emergency_contact", "relationship", e.target.value)} className={inputCls} />
            </Field>
            <Field label="เบอร์โทรศัพท์">
              <input value={form.emergency_contact.phone} onChange={(e) => setNested("emergency_contact", "phone", e.target.value)} className={inputCls} />
            </Field>
          </div>
        </Section>

        <Section title="สิทธิการรักษา / ประกัน">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Field label="สิทธิ/บริษัทประกัน">
              <input value={form.insurance.provider} onChange={(e) => setNested("insurance", "provider", e.target.value)} placeholder="เช่น สิทธิบัตรทอง, ประกันสังคม" className={inputCls} />
            </Field>
            <Field label="เลขกรมธรรม์">
              <input value={form.insurance.policy_number} onChange={(e) => setNested("insurance", "policy_number", e.target.value)} className={inputCls} />
            </Field>
            <Field label="ประเภทความคุ้มครอง">
              <input value={form.insurance.coverage_type} onChange={(e) => setNested("insurance", "coverage_type", e.target.value)} className={inputCls} />
            </Field>
          </div>
        </Section>

        <Section title="ประวัติการแพ้ยา/สารก่อภูมิแพ้">
          <div className="space-y-3">
            {form.allergies.map((a, i) => (
              <div key={i} className="grid grid-cols-1 md:grid-cols-[1fr,1fr,1fr,auto] gap-3 items-start">
                <input value={a.allergen} onChange={(e) => setItem("allergies", i, "allergen", e.target.value)} placeholder="สารที่แพ้ เช่น Penicillin" className={inputCls} data-testid={`allergy-allergen-${i}`} />
                <select value={a.severity} onChange={(e) => setItem("allergies", i, "severity", e.target.value)} className={inputCls}>
                  <option value="">ความรุนแรง</option>
                  <option value="เล็กน้อย">เล็กน้อย</option>
                  <option value="ปานกลาง">ปานกลาง</option>
                  <option value="รุนแรง">รุนแรง</option>
                </select>
                <input value={a.reaction} onChange={(e) => setItem("allergies", i, "reaction", e.target.value)} placeholder="อาการที่เกิด" className={inputCls} />
                <button type="button" onClick={() => removeItem("allergies", i)} className="p-2.5 text-[#D34228] hover:bg-[#D34228]/10 rounded-lg">
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            ))}
            <button type="button" onClick={() => addItem("allergies", { allergen: "", severity: "", reaction: "" })} data-testid="add-allergy-btn" className="inline-flex items-center gap-2 text-sm text-[#1E3F33] font-medium hover:underline">
              <Plus className="w-4 h-4" /> เพิ่มรายการแพ้ยา
            </button>
          </div>
        </Section>

        <Section title="โรคประจำตัว">
          <div className="space-y-3">
            {form.chronic_conditions.map((c, i) => (
              <div key={i} className="grid grid-cols-1 md:grid-cols-[1fr,1fr,auto] gap-3 items-start">
                <input value={c.condition} onChange={(e) => setItem("chronic_conditions", i, "condition", e.target.value)} placeholder="โรค เช่น เบาหวาน" className={inputCls} />
                <input type="date" value={c.diagnosed_date} onChange={(e) => setItem("chronic_conditions", i, "diagnosed_date", e.target.value)} className={inputCls} />
                <button type="button" onClick={() => removeItem("chronic_conditions", i)} className="p-2.5 text-[#D34228] hover:bg-[#D34228]/10 rounded-lg">
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            ))}
            <button type="button" onClick={() => addItem("chronic_conditions", { condition: "", diagnosed_date: "", status: "active" })} className="inline-flex items-center gap-2 text-sm text-[#1E3F33] font-medium hover:underline">
              <Plus className="w-4 h-4" /> เพิ่มโรคประจำตัว
            </button>
          </div>
        </Section>

        <Section title="ยาที่ใช้ประจำ">
          <div className="space-y-3">
            {form.current_medications.map((m, i) => (
              <div key={i} className="grid grid-cols-1 md:grid-cols-[1fr,1fr,1fr,auto] gap-3 items-start">
                <input value={m.drug_name} onChange={(e) => setItem("current_medications", i, "drug_name", e.target.value)} placeholder="ชื่อยา" className={inputCls} />
                <input value={m.dosage} onChange={(e) => setItem("current_medications", i, "dosage", e.target.value)} placeholder="ขนาดยา เช่น 500 mg" className={inputCls} />
                <input value={m.frequency} onChange={(e) => setItem("current_medications", i, "frequency", e.target.value)} placeholder="ความถี่ เช่น วันละ 2 ครั้ง" className={inputCls} />
                <button type="button" onClick={() => removeItem("current_medications", i)} className="p-2.5 text-[#D34228] hover:bg-[#D34228]/10 rounded-lg">
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            ))}
            <button type="button" onClick={() => addItem("current_medications", { drug_name: "", dosage: "", frequency: "" })} className="inline-flex items-center gap-2 text-sm text-[#1E3F33] font-medium hover:underline">
              <Plus className="w-4 h-4" /> เพิ่มยาประจำ
            </button>
          </div>
        </Section>

        <Section title="หมายเหตุ">
          <textarea value={form.notes} onChange={(e) => set("notes", e.target.value)} rows={3} className={inputCls} placeholder="บันทึกเพิ่มเติม..." />
        </Section>

        <div className="flex gap-3">
          <button type="submit" disabled={saving} data-testid="patient-form-submit-btn" className="bg-[#1E3F33] text-white hover:bg-[#2C5A48] rounded-lg px-8 py-3 font-medium transition-colors disabled:opacity-60 inline-flex items-center gap-2">
            {saving && <Loader2 className="w-4 h-4 animate-spin" />}
            {isEdit ? "บันทึกการแก้ไข" : "ลงทะเบียนผู้ป่วย"}
          </button>
          <Link to={isEdit ? `/patients/${id}` : "/patients"} className="bg-[#F2F0EB] text-[#0F1F19] hover:bg-[#E1E5E2] rounded-lg px-8 py-3 font-medium transition-colors border border-[#E1E5E2]">
            ยกเลิก
          </Link>
        </div>
      </form>
    </div>
  );
}
