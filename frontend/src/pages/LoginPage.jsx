import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { HeartPulse, Loader2 } from "lucide-react";
import { useAuth } from "@/context/AuthContext";
import { formatApiError } from "@/lib/api";

const LOGIN_BG =
  "https://images.unsplash.com/photo-1719934398679-d764c1410770?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NjA1NTJ8MHwxfHNlYXJjaHwyfHxob3NwaXRhbCUyMGFyY2hpdGVjdHVyZSUyMGJ1aWxkaW5nJTIwbW9kZXJufGVufDB8fHx8MTc4MTI3NTI5NXww&ixlib=rb-4.1.0&q=85";

export default function LoginPage() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await login(email, password);
      navigate("/");
    } catch (err) {
      setError(formatApiError(err));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex bg-[#F9F9F8]">
      {/* Form side */}
      <div className="w-full lg:w-[45%] flex flex-col justify-center px-8 md:px-16 xl:px-24 py-12">
        <div className="flex items-center gap-3 mb-12">
          <div className="w-11 h-11 rounded-xl bg-[#1E3F33] flex items-center justify-center">
            <HeartPulse className="w-6 h-6 text-white" />
          </div>
          <div>
            <div className="font-heading font-semibold text-2xl text-[#0F1F19] leading-none">HosPRIME</div>
            <div className="text-[10px] uppercase tracking-[0.25em] text-[#546E62] mt-1">
              Hospital Intelligent Management
            </div>
          </div>
        </div>

        <h1 className="font-heading text-3xl md:text-4xl font-medium tracking-tight text-[#0F1F19] mb-2">
          เข้าสู่ระบบ
        </h1>
        <p className="text-[#546E62] mb-8">ระบบบริหารจัดการโรงพยาบาลอัจฉริยะ</p>

        <form onSubmit={handleSubmit} className="space-y-5" data-testid="login-form">
          <div>
            <label className="block text-sm font-medium text-[#0F1F19] mb-1.5">อีเมล</label>
            <input
              type="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="name@hosprime.com"
              data-testid="login-email-input"
              className="w-full border border-[#E1E5E2] bg-white rounded-lg px-4 py-2.5 text-[#0F1F19] placeholder:text-[#546E62]/60 focus:border-[#1E3F33] focus:ring-1 focus:ring-[#1E3F33] focus:outline-none transition-all"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-[#0F1F19] mb-1.5">รหัสผ่าน</label>
            <input
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              data-testid="login-password-input"
              className="w-full border border-[#E1E5E2] bg-white rounded-lg px-4 py-2.5 text-[#0F1F19] placeholder:text-[#546E62]/60 focus:border-[#1E3F33] focus:ring-1 focus:ring-[#1E3F33] focus:outline-none transition-all"
            />
          </div>

          {error && (
            <div
              className="bg-[#D34228]/10 border border-[#D34228]/30 text-[#D34228] text-sm rounded-lg px-4 py-3"
              data-testid="login-error"
            >
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            data-testid="login-submit-btn"
            className="w-full bg-[#1E3F33] text-white hover:bg-[#2C5A48] rounded-lg px-6 py-3 font-medium transition-colors focus:ring-2 focus:ring-[#4A6B5D] focus:outline-none disabled:opacity-60 flex items-center justify-center gap-2"
          >
            {loading && <Loader2 className="w-4 h-4 animate-spin" />}
            เข้าสู่ระบบ
          </button>
        </form>

        <div className="mt-8 bg-[#F2F0EB] border border-[#E1E5E2] rounded-lg p-4 text-xs text-[#546E62]" data-testid="demo-credentials">
          <div className="font-semibold text-[#0F1F19] mb-1.5">บัญชีทดสอบ (Demo)</div>
          <div>ผู้ดูแลระบบ: admin@hosprime.com / Admin@1234</div>
          <div>แพทย์: doctor@hosprime.com / Test@1234</div>
          <div>พยาบาล: nurse@hosprime.com / Test@1234</div>
        </div>
      </div>

      {/* Image side */}
      <div className="hidden lg:block lg:w-[55%] relative">
        <img src={LOGIN_BG} alt="HosPRIME Hospital" className="absolute inset-0 w-full h-full object-cover" />
        <div className="absolute inset-0 bg-gradient-to-t from-[#1E3F33]/90 via-[#1E3F33]/30 to-transparent" />
        <div className="absolute bottom-0 left-0 right-0 p-12 text-white">
          <h2 className="font-heading text-3xl font-medium mb-3">ยกระดับการดูแลผู้ป่วยด้วยระบบอัจฉริยะ</h2>
          <p className="text-white/80 max-w-lg">
            บริหารจัดการข้อมูลผู้ป่วย นัดหมาย เภสัชกรรม ห้องปฏิบัติการ และการเงิน ครบในระบบเดียว
            พร้อม AI ผู้ช่วยทางการแพทย์
          </p>
        </div>
      </div>
    </div>
  );
}
