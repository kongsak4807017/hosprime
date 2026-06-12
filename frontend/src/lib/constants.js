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
