import { useState, useEffect } from 'react';
import { 
  Compass, HelpCircle, UploadCloud, Database, ShieldCheck, 
  FileText, History, Layers, Users, Activity
} from 'lucide-react';
import { api, DocumentResponse, UserResponse } from './lib/api';
import { ThemeSwitcher } from './components/ThemeSwitcher';
import { Login } from './components/Login';

// Import Tab Components
import { HomeTab } from './components/tabs/HomeTab';
import { AskTab } from './components/tabs/AskTab';
import { UploadTab } from './components/tabs/UploadTab';
import { CatalogTab } from './components/tabs/CatalogTab';
import { AdminTab } from './components/tabs/AdminTab';
import { LogsTab } from './components/tabs/LogsTab';
import { MeetingMemoryTab } from './components/tabs/MeetingMemoryTab';
import { ExecutiveTwinTab } from './components/tabs/ExecutiveTwinTab';
import { GraphBrainTab } from './components/tabs/GraphBrainTab';
import { AIWorkflowsTab } from './components/tabs/AIWorkflowsTab';

export default function App() {
  const [currentUser, setCurrentUser] = useState<UserResponse | null>(api.getCurrentUser());
  const [activeTab, setActiveTab] = useState<'home' | 'ask' | 'upload' | 'catalog' | 'admin' | 'logs' | 'meetings' | 'twins' | 'graph' | 'workflows'>('home');
  const [stats, setStats] = useState({ totalDocs: 0, pendingDocs: 0, totalQueries: 0 });
  const [catalog, setCatalog] = useState<DocumentResponse[]>([]);

  // โหลดสถิติพื้นฐาน
  const fetchStats = async () => {
    try {
      const docs = await api.getCatalog();
      const pending = await api.getPendingDocuments();
      const logs = await api.getQueryLogs();
      setStats({
        totalDocs: docs.length,
        pendingDocs: pending.length,
        totalQueries: logs.length
      });
      setCatalog(docs);
    } catch (e) {
      console.error("Failed to fetch statistics", e);
    }
  };

  useEffect(() => {
    if (!currentUser) return;
    fetchStats();
    const interval = setInterval(fetchStats, 10000); // อัปเดตทุก 10 วินาที
    return () => clearInterval(interval);
  }, [currentUser]);

  // ฟังก์ชันสลับแท็บ
  const handleTabChange = (tab: 'home' | 'ask' | 'upload' | 'catalog' | 'admin' | 'logs' | 'meetings' | 'twins' | 'graph' | 'workflows') => {
    setActiveTab(tab);
    fetchStats();
  };

  if (!currentUser) {
    return <Login onLoginSuccess={(user) => setCurrentUser(user)} />;
  }

  return (
    <div className="flex h-screen bg-slate-950 text-slate-100 font-sans overflow-hidden">
      {/* Sidebar Navigation */}
      <aside className="w-72 bg-slate-900 border-r border-slate-800 flex flex-col justify-between z-10">
        <div className="overflow-y-auto flex-1 select-none">
          {/* Brand Logo Header */}
          <div className="p-6 border-b border-slate-800/60 flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-brand-600 to-gold-500 flex items-center justify-center shadow-lg shadow-brand-900/30">
              <span className="text-xl font-bold text-slate-950">👑</span>
            </div>
            <div>
              <h1 className="text-lg font-bold tracking-tight text-white font-outfit">HosPrime</h1>
              <p className="text-xs text-slate-400 font-outfit font-light">Health Organization OS</p>
            </div>
          </div>

          {/* Navigation Links */}
          <div className="p-4 space-y-4">
            {/* Section 1: RAG Knowledge Oracle */}
            <div className="space-y-1">
              <p className="px-4 text-[10px] font-bold text-slate-500 uppercase tracking-wider mb-2">คลังปัญญาองค์กร (RAG Oracle)</p>
              
              <button 
                onClick={() => handleTabChange('home')}
                className={`w-full flex items-center gap-3 px-4 py-2.5 rounded-xl text-xs font-medium transition-all duration-200 ${
                  activeTab === 'home' 
                    ? 'bg-gradient-to-r from-brand-800 to-brand-700/50 text-white border-l-4 border-gold-500 pl-3' 
                    : 'text-slate-400 hover:text-white hover:bg-slate-800/40'
                }`}
              >
                <Compass className="w-3.5 h-3.5" />
                <span>ภาพรวม (Home)</span>
              </button>

              <button 
                onClick={() => handleTabChange('ask')}
                className={`w-full flex items-center gap-3 px-4 py-2.5 rounded-xl text-xs font-medium transition-all duration-200 ${
                  activeTab === 'ask' 
                    ? 'bg-gradient-to-r from-brand-800 to-brand-700/50 text-white border-l-4 border-gold-500 pl-3' 
                    : 'text-slate-400 hover:text-white hover:bg-slate-800/40'
                }`}
              >
                <HelpCircle className="w-3.5 h-3.5" />
                <span>คลังปัญญา & ระดมสมอง (Ask & Collab)</span>
              </button>

              <button 
                onClick={() => handleTabChange('upload')}
                className={`w-full flex items-center gap-3 px-4 py-2.5 rounded-xl text-xs font-medium transition-all duration-200 ${
                  activeTab === 'upload' 
                    ? 'bg-gradient-to-r from-brand-800 to-brand-700/50 text-white border-l-4 border-gold-500 pl-3' 
                    : 'text-slate-400 hover:text-white hover:bg-slate-800/40'
                }`}
              >
                <UploadCloud className="w-3.5 h-3.5" />
                <span>อัปโหลดเอกสาร (Upload)</span>
              </button>

              <button 
                onClick={() => handleTabChange('catalog')}
                className={`w-full flex items-center gap-3 px-4 py-2.5 rounded-xl text-xs font-medium transition-all duration-200 ${
                  activeTab === 'catalog' 
                    ? 'bg-gradient-to-r from-brand-800 to-brand-700/50 text-white border-l-4 border-gold-500 pl-3' 
                    : 'text-slate-400 hover:text-white hover:bg-slate-800/40'
                }`}
              >
                <Database className="w-3.5 h-3.5" />
                <span>คลังความรู้ (Catalog)</span>
              </button>

              <button 
                onClick={() => handleTabChange('admin')}
                className={`w-full flex items-center justify-between px-4 py-2.5 rounded-xl text-xs font-medium transition-all duration-200 ${
                  activeTab === 'admin' 
                    ? 'bg-gradient-to-r from-brand-800 to-brand-700/50 text-white border-l-4 border-gold-500 pl-3' 
                    : 'text-slate-400 hover:text-white hover:bg-slate-800/40'
                }`}
              >
                <div className="flex items-center gap-3">
                  <ShieldCheck className="w-3.5 h-3.5" />
                  <span>แอดมินตรวจทาน (Review)</span>
                </div>
                {stats.pendingDocs > 0 && (
                  <span className="bg-amber-600/90 text-white text-[9px] font-bold px-1.5 py-0.5 rounded-full">
                    {stats.pendingDocs}
                  </span>
                )}
              </button>

              <button 
                onClick={() => handleTabChange('logs')}
                className={`w-full flex items-center gap-3 px-4 py-2.5 rounded-xl text-xs font-medium transition-all duration-200 ${
                  activeTab === 'logs' 
                    ? 'bg-gradient-to-r from-brand-800 to-brand-700/50 text-white border-l-4 border-gold-500 pl-3' 
                    : 'text-slate-400 hover:text-white hover:bg-slate-800/40'
                }`}
              >
                <History className="w-3.5 h-3.5" />
                <span>กำกับดูแล & กิจกรรม (Governance & Logs)</span>
              </button>
            </div>

            {/* Section 2: HODT Twin Operating System */}
            <div className="space-y-1 border-t border-slate-800/60 pt-3">
              <p className="px-4 text-[10px] font-bold text-slate-500 uppercase tracking-wider mb-2">ระบบบริหารดิจิทัล (HODT Twin OS)</p>

              <button 
                onClick={() => handleTabChange('meetings')}
                className={`w-full flex items-center gap-3 px-4 py-2.5 rounded-xl text-xs font-medium transition-all duration-200 ${
                  activeTab === 'meetings' 
                    ? 'bg-gradient-to-r from-brand-800 to-brand-700/50 text-white border-l-4 border-gold-500 pl-3' 
                    : 'text-slate-400 hover:text-white hover:bg-slate-800/40'
                }`}
              >
                <FileText className="w-3.5 h-3.5 text-indigo-400" />
                <span>ความทรงจำที่ประชุม (Meeting)</span>
              </button>

              <button 
                onClick={() => handleTabChange('twins')}
                className={`w-full flex items-center gap-3 px-4 py-2.5 rounded-xl text-xs font-medium transition-all duration-200 ${
                  activeTab === 'twins' 
                    ? 'bg-gradient-to-r from-brand-800 to-brand-700/50 text-white border-l-4 border-gold-500 pl-3' 
                    : 'text-slate-400 hover:text-white hover:bg-slate-800/40'
                }`}
              >
                <Users className="w-3.5 h-3.5 text-amber-400" />
                <span>ห้องทำงานจำลอง (Workspace Twin)</span>
              </button>

              <button 
                onClick={() => handleTabChange('graph')}
                className={`w-full flex items-center gap-3 px-4 py-2.5 rounded-xl text-xs font-medium transition-all duration-200 ${
                  activeTab === 'graph' 
                    ? 'bg-gradient-to-r from-brand-800 to-brand-700/50 text-white border-l-4 border-gold-500 pl-3' 
                    : 'text-slate-400 hover:text-white hover:bg-slate-800/40'
                }`}
              >
                <Layers className="w-3.5 h-3.5 text-emerald-400" />
                <span>โครงข่ายสมองจังหวัด (Graph)</span>
              </button>

              <button 
                onClick={() => handleTabChange('workflows')}
                className={`w-full flex items-center gap-3 px-4 py-2.5 rounded-xl text-xs font-medium transition-all duration-200 ${
                  activeTab === 'workflows' 
                    ? 'bg-gradient-to-r from-brand-800 to-brand-700/50 text-white border-l-4 border-gold-500 pl-3' 
                    : 'text-slate-400 hover:text-white hover:bg-slate-800/40'
                }`}
              >
                <Activity className="w-3.5 h-3.5 text-rose-400" />
                <span>เวิร์กโฟลว์หลังบ้าน (Workflows)</span>
              </button>
            </div>
          </div>
        </div>

        {/* Workspace Info Footer */}
        <div className="p-6 border-t border-slate-800/60 space-y-3">
          <div className="flex items-center justify-between p-3 bg-slate-950/40 rounded-xl border border-slate-800">
            <div className="flex items-center gap-2.5 min-w-0">
              <div className="w-7 h-7 rounded-lg bg-gold-500/15 flex-shrink-0 flex items-center justify-center border border-gold-500/20">
                <span className="text-xs font-bold text-gold-400">
                  {currentUser?.username.substring(0, 2).toUpperCase()}
                </span>
              </div>
              <div className="min-w-0">
                <p className="text-xs font-bold text-white truncate">{currentUser?.username}</p>
                <p className="text-[9px] text-slate-400 truncate">{currentUser?.department || 'ไม่ระบุฝ่าย'}</p>
              </div>
            </div>
            <span className="bg-gold-950/50 text-gold-400 border border-gold-800/40 text-[9px] font-semibold px-2 py-0.5 rounded-md uppercase tracking-wider flex-shrink-0">
              {currentUser?.role}
            </span>
          </div>
          
          <button
            onClick={() => {
              api.logout();
              setCurrentUser(null);
            }}
            className="w-full py-2 rounded-xl border border-slate-800 hover:border-red-900/40 hover:bg-red-950/15 text-xs text-slate-400 hover:text-red-400 active:scale-[0.98] transition-all duration-150 font-medium"
          >
            ออกจากระบบ (Logout)
          </button>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 flex flex-col min-w-0 bg-slate-950 relative overflow-hidden">
        {/* Background gradient lights */}
        <div className="absolute top-[-20%] left-[-10%] w-[50%] h-[50%] bg-brand-900/10 rounded-full blur-[120px] pointer-events-none"></div>
        <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-gold-600/5 rounded-full blur-[100px] pointer-events-none"></div>

        {/* Top Header bar with ThemeSwitcher */}
        <header className="h-16 border-b border-slate-900 flex items-center justify-end px-8 gap-4 z-10">
          <ThemeSwitcher />
        </header>

        {/* Main Tab Render */}
        <div className="flex-1 overflow-y-auto p-8 z-10">
          {activeTab === 'home' && <HomeTab handleTabChange={handleTabChange} stats={stats} catalog={catalog} />}
          {activeTab === 'ask' && <AskTab />}
          {activeTab === 'upload' && <UploadTab onIngested={fetchStats} />}
          {activeTab === 'catalog' && <CatalogTab />}
          {activeTab === 'admin' && <AdminTab onApproved={fetchStats} />}
          {activeTab === 'logs' && <LogsTab />}
          {activeTab === 'meetings' && <MeetingMemoryTab />}
          {activeTab === 'twins' && <ExecutiveTwinTab />}
          {activeTab === 'graph' && <GraphBrainTab />}
          {activeTab === 'workflows' && <AIWorkflowsTab />}
        </div>
      </main>
    </div>
  );
}
