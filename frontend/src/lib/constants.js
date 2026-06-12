export const ROLE_LABELS = {
  admin: "ผู้ดูแลระบบ",
  doctor: "แพทย์",
  nurse: "พยาบาล",
  pharmacist: "เภสัชกร",
  lab_technician: "นักเทคนิคการแพทย์",
  finance: "การเงิน",
  patient: "ผู้ป่วย",
};

export const STATUS_LABELS = {
  scheduled: "นัดหมายแล้ว",
  confirmed: "ยืนยันแล้ว",
  checked_in: "เช็คอินแล้ว",
  in_progress: "กำลังตรวจ",
  completed: "เสร็จสิ้น",
  cancelled: "ยกเลิก",
  no_show: "ไม่มาตามนัด",
};

export const STATUS_BADGES = {
  scheduled: "bg-[#E5A732]/10 text-[#9c7016] border border-[#E5A732]/30",
  confirmed: "bg-[#4A6B5D]/10 text-[#4A6B5D] border border-[#4A6B5D]/30",
  checked_in: "bg-[#4A6B5D]/15 text-[#2C5A48] border border-[#4A6B5D]/30",
  in_progress: "bg-[#2E77D0]/10 text-[#2E77D0] border border-[#2E77D0]/30",
  completed: "bg-[#327A59]/10 text-[#327A59] border border-[#327A59]/30",
  cancelled: "bg-[#D34228]/10 text-[#D34228] border border-[#D34228]/30",
  no_show: "bg-gray-200 text-gray-600 border border-gray-300",
};

export const NEXT_STATUSES = {
  scheduled: ["confirmed", "checked_in", "cancelled", "no_show"],
  confirmed: ["checked_in", "cancelled", "no_show"],
  checked_in: ["in_progress", "cancelled"],
  in_progress: ["completed"],
  completed: [],
  cancelled: [],
  no_show: [],
};

export const GENDER_LABELS = { male: "ชาย", female: "หญิง", other: "อื่นๆ" };

export const BLOOD_TYPES = ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"];

export const DEPARTMENTS = [
  "อายุรกรรม",
  "ศัลยกรรม",
  "กุมารเวชกรรม",
  "สูติ-นรีเวชกรรม",
  "ออร์โธปิดิกส์",
  "ฉุกเฉิน",
  "จักษุวิทยา",
  "ทันตกรรม",
];

export const APPOINTMENT_TYPES = {
  consultation: "ตรวจรักษา",
  follow_up: "ติดตามอาการ",
  emergency: "ฉุกเฉิน",
  procedure: "หัตถการ",
};

export const PRIORITY_LABELS = {
  normal: "ปกติ",
  urgent: "เร่งด่วน",
  emergency: "ฉุกเฉิน",
};

export const MARITAL_LABELS = {
  single: "โสด",
  married: "สมรส",
  divorced: "หย่าร้าง",
  widowed: "หม้าย",
};

// ---------- Phase 2: Clinical ----------

export const PRESCRIPTION_STATUS_LABELS = {
  active: "รอจ่ายยา",
  dispensed: "จ่ายยาแล้ว",
  cancelled: "ยกเลิก",
};

export const PRESCRIPTION_STATUS_BADGES = {
  active: "bg-[#E5A732]/10 text-[#9c7016] border border-[#E5A732]/30",
  dispensed: "bg-[#327A59]/10 text-[#327A59] border border-[#327A59]/30",
  cancelled: "bg-[#D34228]/10 text-[#D34228] border border-[#D34228]/30",
};

export const LAB_STATUS_LABELS = {
  ordered: "สั่งตรวจแล้ว",
  sample_collected: "เก็บตัวอย่างแล้ว",
  in_progress: "กำลังตรวจ",
  completed: "ผลออกแล้ว",
  cancelled: "ยกเลิก",
};

export const LAB_STATUS_BADGES = {
  ordered: "bg-[#E5A732]/10 text-[#9c7016] border border-[#E5A732]/30",
  sample_collected: "bg-[#4A6B5D]/15 text-[#2C5A48] border border-[#4A6B5D]/30",
  in_progress: "bg-[#2E77D0]/10 text-[#2E77D0] border border-[#2E77D0]/30",
  completed: "bg-[#327A59]/10 text-[#327A59] border border-[#327A59]/30",
  cancelled: "bg-[#D34228]/10 text-[#D34228] border border-[#D34228]/30",
};

export const LAB_PRIORITY_LABELS = { routine: "ปกติ", urgent: "เร่งด่วน", stat: "STAT" };

export const LAB_PRIORITY_BADGES = {
  routine: "bg-[#F2F0EB] text-[#546E62] border border-[#E1E5E2]",
  urgent: "bg-[#E5A732]/10 text-[#9c7016] border border-[#E5A732]/30",
  stat: "bg-[#D34228]/10 text-[#D34228] border border-[#D34228]/30",
};

export const INVOICE_STATUS_LABELS = {
  pending: "รอชำระ",
  partially_paid: "ชำระบางส่วน",
  paid: "ชำระแล้ว",
  cancelled: "ยกเลิก",
};

export const INVOICE_STATUS_BADGES = {
  pending: "bg-[#E5A732]/10 text-[#9c7016] border border-[#E5A732]/30",
  partially_paid: "bg-[#2E77D0]/10 text-[#2E77D0] border border-[#2E77D0]/30",
  paid: "bg-[#327A59]/10 text-[#327A59] border border-[#327A59]/30",
  cancelled: "bg-[#D34228]/10 text-[#D34228] border border-[#D34228]/30",
};

export const PAYMENT_METHOD_LABELS = {
  cash: "เงินสด",
  card: "บัตรเครดิต/เดบิต",
  transfer: "โอนเงิน",
  insurance: "ประกัน/สิทธิ",
};

export const CLAIM_STATUS_LABELS = {
  submitted: "ยื่นเคลมแล้ว",
  approved: "อนุมัติ",
  rejected: "ปฏิเสธ",
  partially_approved: "อนุมัติบางส่วน",
};

export const ITEM_TYPE_LABELS = {
  consultation: "ค่าตรวจรักษา",
  procedure: "หัตถการ",
  lab: "ค่าแล็บ",
  pharmacy: "ค่ายา",
  bed: "ค่าห้อง/เตียง",
  other: "อื่นๆ",
};

export const DRUG_CATEGORIES = [
  "ยาแก้ปวด",
  "ยาปฏิชีวนะ",
  "ยาเบาหวาน",
  "ยาความดัน",
  "ยาลดไขมัน",
  "ยาโรคหัวใจ",
  "ยาแก้แพ้",
  "ยาระบบทางเดินอาหาร",
  "วิตามิน",
  "อื่นๆ",
];
