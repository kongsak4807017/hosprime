import { useState } from "react";
import { NavLink, useNavigate } from "react-router-dom";
import {
  LayoutDashboard,
  Users,
  CalendarClock,
  Pill,
  FlaskConical,
  Receipt,
  BedDouble,
  UserCog,
  Bot,
  BarChart3,
  LogOut,
  Menu,
  X,
  HeartPulse,
} from "lucide-react";
import { useAuth } from "@/context/AuthContext";
import { ROLE_LABELS } from "@/lib/constants";

const STAFF = ["admin", "doctor", "nurse", "pharmacist", "lab_technician", "finance"];

const MENU = [
  { label: "แดชบอร์ด", icon: LayoutDashboard, path: "/", roles: [...STAFF, "patient"], testId: "nav-dashboard" },
  { label: "ผู้ป่วย", icon: Users, path: "/patients", roles: STAFF, testId: "nav-patients" },
  { label: "นัดหมาย", icon: CalendarClock, path: "/appointments", roles: STAFF, testId: "nav-appointments" },
];

const COMING_SOON = [
  { label: "เภสัชกรรม", icon: Pill },
  { label: "ห้องปฏิบัติการ", icon: FlaskConical },
  { label: "การเงิน & บิล", icon: Receipt },
  { label: "เตียงผู้ป่วย", icon: BedDouble },
  { label: "บุคลากร", icon: UserCog },
  { label: "AI ผู้ช่วยแพทย์", icon: Bot },
  { label: "รายงานวิเคราะห์", icon: BarChart3 },
];

export const Layout = ({ children }) => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [open, setOpen] = useState(false);

  const handleLogout = async () => {
    await logout();
    navigate("/login");
  };

  const menuItems = MENU.filter((m) => m.roles.includes(user?.role));

  return (
    <div className="min-h-screen bg-[#F9F9F8] flex">
      {/* Sidebar */}
      <aside
        className={`fixed md:static inset-y-0 left-0 z-40 w-64 bg-[#F2F0EB] border-r border-[#E1E5E2] flex flex-col transition-transform duration-200 ${
          open ? "translate-x-0" : "-translate-x-full md:translate-x-0"
        }`}
        data-testid="sidebar"
      >
        <div className="flex items-center gap-3 px-6 py-5 border-b border-[#E1E5E2]">
          <div className="w-9 h-9 rounded-lg bg-[#1E3F33] flex items-center justify-center">
            <HeartPulse className="w-5 h-5 text-white" />
          </div>
          <div>
            <div className="font-heading font-semibold text-lg text-[#0F1F19] leading-none">HosPRIME</div>
            <div className="text-[10px] uppercase tracking-[0.2em] text-[#546E62] mt-1">Hospital System</div>
          </div>
        </div>

        <nav className="flex-1 overflow-y-auto px-3 py-4 space-y-1">
          {menuItems.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              end={item.path === "/"}
              data-testid={item.testId}
              onClick={() => setOpen(false)}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                  isActive
                    ? "bg-[#1E3F33] text-white"
                    : "text-[#0F1F19] hover:bg-[#E1E5E2]"
                }`
              }
            >
              <item.icon className="w-4 h-4" />
              {item.label}
            </NavLink>
          ))}

          <div className="pt-4 pb-1 px-3 text-[10px] font-semibold uppercase tracking-[0.2em] text-[#546E62]">
            เฟสถัดไป
          </div>
          {COMING_SOON.map((item) => (
            <div
              key={item.label}
              className="flex items-center justify-between px-3 py-2 rounded-lg text-sm text-[#546E62]/70 cursor-not-allowed"
            >
              <span className="flex items-center gap-3">
                <item.icon className="w-4 h-4" />
                {item.label}
              </span>
              <span className="text-[9px] bg-[#E1E5E2] text-[#546E62] rounded-full px-2 py-0.5">เร็วๆ นี้</span>
            </div>
          ))}
        </nav>

        <div className="border-t border-[#E1E5E2] p-4">
          <div className="flex items-center gap-3 mb-3">
            <div className="w-9 h-9 rounded-full bg-[#4A6B5D] text-white flex items-center justify-center text-sm font-semibold">
              {user?.full_name?.charAt(0) || "?"}
            </div>
            <div className="min-w-0">
              <div className="text-sm font-medium text-[#0F1F19] truncate" data-testid="user-fullname">
                {user?.full_name}
              </div>
              <div className="text-xs text-[#546E62]">{ROLE_LABELS[user?.role] || user?.role}</div>
            </div>
          </div>
          <button
            onClick={handleLogout}
            data-testid="logout-btn"
            className="w-full flex items-center justify-center gap-2 text-sm text-[#D34228] border border-[#D34228]/30 rounded-lg py-2 hover:bg-[#D34228]/5 transition-colors"
          >
            <LogOut className="w-4 h-4" />
            ออกจากระบบ
          </button>
        </div>
      </aside>

      {open && (
        <div className="fixed inset-0 bg-black/30 z-30 md:hidden" onClick={() => setOpen(false)} />
      )}

      {/* Main */}
      <div className="flex-1 flex flex-col min-w-0">
        <header className="sticky top-0 z-20 bg-[#F9F9F8]/90 backdrop-blur-md border-b border-[#E1E5E2] px-4 md:px-8 py-3 flex items-center gap-3 md:hidden">
          <button onClick={() => setOpen(!open)} data-testid="mobile-menu-btn" className="p-2">
            {open ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
          <span className="font-heading font-semibold text-[#0F1F19]">HosPRIME</span>
        </header>
        <main className="flex-1 p-4 md:p-8">{children}</main>
      </div>
    </div>
  );
};
