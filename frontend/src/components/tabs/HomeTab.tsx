import { FileText, ShieldCheck, History, ArrowRight } from 'lucide-react';
import { DocumentResponse } from '../../lib/api';

interface HomeTabProps {
  handleTabChange: (tab: any) => void;
  stats: { totalDocs: number; pendingDocs: number; totalQueries: number };
  catalog: DocumentResponse[];
}

export function HomeTab({ handleTabChange, stats, catalog }: HomeTabProps) {
  const suggestedQuestions = [
    "PM2.5 ปีที่แล้วจังหวัดทำอะไรบ้าง",
    "TB active case finding มีแนวทางอะไร",
    "NCD remission มีเอกสารหรือโครงการอะไรแล้ว",
    "น้ำท่วมครั้งก่อนเรามีมาตรการอะไร",
    "Digital Health platform ควรเริ่มจากอะไร"
  ];

  return (
    <div className="max-w-5xl mx-auto space-y-8 animate-fade-in">
      {/* Welcome Hero */}
      <div className="space-y-3">
        <span className="text-xs font-semibold tracking-widest text-gold-500 uppercase">Health Organization OS</span>
        <h2 className="text-4xl font-extrabold tracking-tight text-white font-outfit">Preserving Organizational Intelligence</h2>
        <p className="text-slate-400 max-w-2xl text-sm leading-relaxed">
          ยินดีต้อนรับสู่ <span className="text-white font-semibold">HosPrime Knowledge Oracle</span> แพลตฟอร์มสืบค้นความรู้เชิงปัญญาประดิษฐ์ระดับองค์กร 
          เปลี่ยนคลังความรู้ที่กระจัดกระจายให้กลายมาเป็นความจำร่วมของหน่วยงานสาธารณสุข
        </p>
      </div>

      {/* Statistics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="glass p-6 rounded-2xl flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-brand-800/80 flex items-center justify-center text-brand-300">
            <FileText className="w-5 h-5" />
          </div>
          <div>
            <p className="text-xs text-slate-400">เอกสารในระบบ</p>
            <p className="text-2xl font-bold font-outfit text-white">{stats.totalDocs} ฉบับ</p>
          </div>
        </div>

        <div className="glass p-6 rounded-2xl flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-amber-950/80 flex items-center justify-center text-amber-400 border border-amber-800/40">
            <ShieldCheck className="w-5 h-5" />
          </div>
          <div>
            <p className="text-xs text-slate-400">รอแอดมินอนุมัติ</p>
            <p className="text-2xl font-bold font-outfit text-white">{stats.pendingDocs} ฉบับ</p>
          </div>
        </div>

        <div className="glass p-6 rounded-2xl flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-emerald-950/80 flex items-center justify-center text-emerald-400 border border-emerald-800/40">
            <History className="w-5 h-5" />
          </div>
          <div>
            <p className="text-xs text-slate-400">คำถามทั้งหมด</p>
            <p className="text-2xl font-bold font-outfit text-white">{stats.totalQueries} คิวรี</p>
          </div>
        </div>
      </div>

      {/* Suggested Questions Grid */}
      <div className="space-y-4">
        <h3 className="text-sm font-semibold tracking-wider text-slate-300 uppercase">คำถามแนะนำสำหรับผู้บริหาร (Executive Demo)</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {suggestedQuestions.map((q, i) => (
            <button
              key={i}
              onClick={() => {
                localStorage.setItem("hosprime_temp_question", q);
                handleTabChange('ask');
              }}
              className="glass p-4 rounded-xl text-left text-sm hover:border-gold-500/40 hover:bg-slate-800/20 transition-all duration-200 flex items-center justify-between group"
            >
              <span className="text-slate-300 group-hover:text-white font-medium">{q}</span>
              <ArrowRight className="w-4 h-4 text-slate-500 group-hover:text-gold-500 transition-colors duration-200" />
            </button>
          ))}
        </div>
      </div>

      {/* Recent Activity / Documents */}
      <div className="glass p-6 rounded-2xl space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-semibold text-slate-200">เอกสารคลังความรู้ล่าสุด</h3>
          <button onClick={() => handleTabChange('catalog')} className="text-xs text-gold-500 hover:underline flex items-center gap-1">
            ดูทั้งหมด <ArrowRight className="w-3 h-3" />
          </button>
        </div>
        <div className="divide-y divide-slate-800/60">
          {catalog.slice(0, 4).map((doc) => (
            <div key={doc.id} className="py-3 flex items-center justify-between">
              <div className="flex items-center gap-3">
                <FileText className="w-4 h-4 text-slate-400" />
                <div>
                  <p className="text-sm font-medium text-slate-200">{doc.title}</p>
                  <p className="text-[10px] text-slate-500">
                    แผนก: {doc.department || 'N/A'} | โปรแกรม: {doc.program || 'N/A'} | ปี: {doc.year || 'N/A'}
                  </p>
                </div>
              </div>
              <span className={`text-[10px] px-2 py-0.5 rounded-full ${
                doc.status === 'processed' ? 'bg-emerald-950 text-emerald-400 border border-emerald-800/40' : 'bg-amber-950 text-amber-400 border border-amber-800/40'
              }`}>
                {doc.status}
              </span>
            </div>
          ))}
          {catalog.length === 0 && (
            <p className="text-xs text-slate-500 py-4 text-center">ยังไม่มีข้อมูลเอกสารในระบบ</p>
          )}
        </div>
      </div>
    </div>
  );
}
