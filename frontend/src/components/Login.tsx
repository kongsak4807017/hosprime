import { useState } from 'react';
import { Shield, Lock, User, Eye, EyeOff } from 'lucide-react';
import { api, UserResponse } from '../lib/api';

interface LoginProps {
  onLoginSuccess: (user: UserResponse) => void;
}

export function Login({ onLoginSuccess }: LoginProps) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!username || !password) {
      setError('กรุณากรอกชื่อผู้ใช้และรหัสผ่าน');
      return;
    }

    setError(null);
    setLoading(true);

    try {
      const data = await api.login(username, password);
      onLoginSuccess(data.user);
    } catch (err: any) {
      setError(err.message || 'การเข้าสู่ระบบล้มเหลว กรุณาลองใหม่อีกครั้ง');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-950 px-4 py-12 sm:px-6 lg:px-8 relative overflow-hidden">
      {/* Background Gradients decoration */}
      <div className="absolute top-1/4 left-1/4 -translate-x-1/2 -translate-y-1/2 w-80 h-80 bg-brand-500/10 rounded-full blur-[120px] pointer-events-none" />
      <div className="absolute bottom-1/4 right-1/4 translate-x-1/2 translate-y-1/2 w-96 h-96 bg-gold-500/5 rounded-full blur-[140px] pointer-events-none" />

      <div className="w-full max-w-md space-y-8 z-10">
        <div className="flex flex-col items-center">
          {/* Logo */}
          <div className="w-16 h-16 rounded-2xl bg-gradient-to-tr from-brand-600 to-gold-500 flex items-center justify-center shadow-xl shadow-brand-900/40 mb-4 ring-2 ring-gold-500/20">
            <span className="text-3xl">👑</span>
          </div>
          <h2 className="mt-2 text-center text-3xl font-extrabold tracking-tight text-white font-outfit">
            HosPrime <span className="text-transparent bg-clip-text bg-gradient-to-r from-gold-400 to-gold-600">HODT</span>
          </h2>
          <p className="mt-2 text-center text-sm text-slate-400 font-outfit">
            Health Organization Operating System
          </p>
          <span className="mt-1 px-3 py-1 text-[10px] font-semibold text-gold-400 bg-gold-950/60 border border-gold-800/40 rounded-full uppercase tracking-wider">
            Sovereign Intranet Engine
          </span>
        </div>

        {/* Card */}
        <div className="bg-slate-900/60 backdrop-blur-xl border border-slate-800/80 rounded-2xl p-8 shadow-2xl shadow-slate-950/50">
          <form className="space-y-6" onSubmit={handleSubmit}>
            {error && (
              <div className="bg-red-950/55 border border-red-900/60 text-red-200 text-xs px-4 py-3 rounded-xl flex items-center gap-2 animate-pulse">
                <span className="w-1.5 h-1.5 rounded-full bg-red-500" />
                <span>{error}</span>
              </div>
            )}

            <div className="space-y-4">
              {/* Username field */}
              <div>
                <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1.5">
                  ชื่อผู้ใช้งาน (Username)
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-500">
                    <User className="w-4 h-4" />
                  </div>
                  <input
                    type="text"
                    required
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    placeholder="ระบุชื่อบัญชีผู้ใช้"
                    className="block w-full pl-10 pr-4 py-3 bg-slate-950/80 border border-slate-800 hover:border-slate-700 focus:border-gold-500 focus:ring-1 focus:ring-gold-500/35 rounded-xl text-sm text-white placeholder-slate-600 transition-all duration-200"
                  />
                </div>
              </div>

              {/* Password field */}
              <div>
                <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1.5">
                  รหัสผ่าน (Password)
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-500">
                    <Lock className="w-4 h-4" />
                  </div>
                  <input
                    type={showPassword ? 'text' : 'password'}
                    required
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="••••••••"
                    className="block w-full pl-10 pr-10 py-3 bg-slate-950/80 border border-slate-800 hover:border-slate-700 focus:border-gold-500 focus:ring-1 focus:ring-gold-500/35 rounded-xl text-sm text-white placeholder-slate-600 transition-all duration-200"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute inset-y-0 right-0 pr-3.5 flex items-center text-slate-500 hover:text-slate-300 transition-colors"
                  >
                    {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                  </button>
                </div>
              </div>
            </div>

            {/* Login Button */}
            <div>
              <button
                type="submit"
                disabled={loading}
                className="w-full flex justify-center items-center gap-2 py-3 px-4 border border-transparent rounded-xl text-sm font-semibold text-slate-950 bg-gradient-to-r from-gold-400 via-gold-500 to-gold-600 hover:from-gold-300 hover:to-gold-500 active:scale-[0.98] transition-all duration-150 disabled:opacity-50 disabled:pointer-events-none shadow-lg shadow-gold-500/20 font-outfit"
              >
                {loading ? (
                  <>
                    <div className="w-4 h-4 rounded-full border-2 border-slate-950 border-t-transparent animate-spin" />
                    <span>กำลังตรวจสอบสิทธิ์...</span>
                  </>
                ) : (
                  <>
                    <Shield className="w-4 h-4" />
                    <span>เข้าสู่ระบบ (Login)</span>
                  </>
                )}
              </button>
            </div>
          </form>

          {/* Tester Account Help */}
          <div className="mt-8 pt-6 border-t border-slate-800/80">
            <h4 className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-3">บัญชีทดสอบในระบบ (Local Sandbox)</h4>
            <div className="grid grid-cols-2 gap-3">
              <div className="bg-slate-950/50 p-2.5 rounded-xl border border-slate-800/40 text-[11px]">
                <div className="font-bold text-gold-400">ผู้บริหาร (Admin)</div>
                <div className="text-slate-400">User: <code className="text-white bg-slate-800 px-1 py-0.5 rounded">admin</code></div>
                <div className="text-slate-400">Pass: <code className="text-white bg-slate-800 px-1 py-0.5 rounded">admin1234</code></div>
              </div>
              <div className="bg-slate-950/50 p-2.5 rounded-xl border border-slate-800/40 text-[11px]">
                <div className="font-bold text-brand-400">เจ้าหน้าที่ (User)</div>
                <div className="text-slate-400">User: <code className="text-white bg-slate-800 px-1 py-0.5 rounded">user</code></div>
                <div className="text-slate-400">Pass: <code className="text-white bg-slate-800 px-1 py-0.5 rounded">user1234</code></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
