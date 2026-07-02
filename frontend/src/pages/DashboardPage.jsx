import ExecutiveOfficePage from "@/pages/ExecutiveOfficePage";
import { useAuth } from "@/context/AuthContext";

export default function DashboardPage() {
  const { user } = useAuth();

  if (user?.role === "patient") {
    return (
      <div className="max-w-2xl" data-testid="patient-portal-placeholder">
        <h1 className="font-heading text-3xl font-medium text-[#0F1F19] mb-2">
          สวัสดี, {user.full_name}
        </h1>
        <div className="bg-white border border-[#E1E5E2] rounded-lg p-8 mt-6 text-center">
          <p className="text-[#546E62]">
            พอร์ทัลผู้ป่วยเป็นคนละ product boundary กับ Executive Office และจะพัฒนาในระยะถัดไป
          </p>
        </div>
      </div>
    );
  }

  return <ExecutiveOfficePage />;
}
