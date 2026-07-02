import { useState, useEffect } from 'react';
import { api } from '../../lib/api';

export function AIWorkflowsTab() {
  const [loading, setLoading] = useState(false);
  const [apiResult, setApiResult] = useState<any>(null);

  const checkStatus = async () => {
    setLoading(true);
    setApiResult(null);
    try {
      const data = await api.getLatestWorkflowStatus();
      setApiResult(data);
    } catch (e) {
      setApiResult({ error: "ไม่สามารถสืบค้นสถานะเวิร์กโฟลว์หลังบ้านได้" });
    } finally {
      setLoading(false);
    }
  };

  const handleWorkflowSimulate = async () => {
    setLoading(true);
    setApiResult(null);
    try {
      const data = await api.triggerWorkflow("เชียงราย", "วิกฤต", "50,000");
      setApiResult(data.data || data);
    } catch (e) {
      setApiResult({ error: "การประสานงาน AI Workflow ขัดข้อง" });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    checkStatus();
  }, []);

  return (
    <div className="max-w-5xl mx-auto space-y-6 animate-fade-in">
      <div>
        <h2 className="text-2xl font-bold tracking-tight text-white font-outfit">เวิร์กโฟลว์หลังบ้านอัตโนมัติ (AI Workflows)</h2>
        <p className="text-slate-400 text-xs">ควบคุมการรันงาน Backoffice และการประสานงานประมวลผลผ่าน Temporal Engine ร่วมกับมนุษย์อนุมัติ</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-5 gap-6 items-start">
        <div className="md:col-span-3 space-y-6">
          <div className="grid grid-cols-2 gap-3">
            <button
              onClick={checkStatus}
              disabled={loading}
              className="py-2.5 border border-slate-800 bg-slate-950/40 hover:bg-slate-900/30 text-xs font-semibold rounded-xl text-slate-300 transition-colors"
            >
              สืบค้นสถานะเวิร์กโฟลว์ล่าสุดจาก SQLite
            </button>
            <button
              onClick={handleWorkflowSimulate}
              disabled={loading}
              className="py-2.5 bg-gradient-to-r from-brand-700 to-brand-600 hover:from-brand-650 hover:to-gold-500 text-white text-xs font-semibold rounded-xl transition-all"
            >
              {loading ? "กำลังเปิดรัน..." : "กระตุ้นการทำงานเวิร์กโฟลว์ฝุ่นละออง PM2.5"}
            </button>
          </div>

          {/* Timeline View */}
          {apiResult && apiResult.steps && (
            <div className="p-6 bg-slate-900/50 border border-slate-800 rounded-2xl space-y-5 animate-fade-in text-xs">
              <div className="flex justify-between items-center pb-3 border-b border-slate-800">
                <div>
                  <h4 className="font-bold text-white">เวิร์กโฟลว์รัน ID: #{apiResult.workflow_id}</h4>
                  <p className="text-[10px] text-slate-500 font-mono">ประเภท: {apiResult.workflow_name}</p>
                </div>
                <span className={`text-[10px] px-2.5 py-0.5 rounded-full font-bold ${
                  apiResult.status === 'COMPLETED' ? 'bg-emerald-950 text-emerald-400 border border-emerald-800/40' : 'bg-amber-950 text-amber-400 border border-amber-805/30 animate-pulse'
                }`}>
                  {apiResult.status}
                </span>
              </div>

              {/* Steps Visual */}
              <div className="space-y-4 relative pl-4 border-l border-slate-800 ml-2">
                {apiResult.steps.map((st: any, i: number) => (
                  <div key={i} className="relative space-y-1">
                    <span className={`absolute left-[-21px] top-1 w-2.5 h-2.5 rounded-full border-2 ${
                      st.status === 'completed'
                        ? 'bg-emerald-500 border-slate-950'
                        : st.status === 'pending_human_approval'
                        ? 'bg-amber-500 border-slate-950'
                        : 'bg-slate-700 border-slate-950'
                    }`}></span>
                    {st.status === 'pending_human_approval' && (
                      <span className="absolute left-[-21px] top-1 w-2.5 h-2.5 rounded-full bg-amber-500 border-2 border-slate-950 animate-ping"></span>
                    )}
                    <p className={`text-xs font-semibold ${st.status === 'completed' ? 'text-slate-300' : st.status === 'pending_human_approval' ? 'text-amber-400 font-bold' : 'text-slate-500'}`}>
                      {st.step}
                    </p>
                    <p className="text-[9px] text-slate-500 uppercase font-mono">
                      สถานะ: {st.status.replace(/_/g, ' ')}
                    </p>
                  </div>
                ))}
              </div>

              {/* Action Pending */}
              {apiResult.current_step && apiResult.status === 'RUNNING' && (
                <div className="p-4 bg-slate-950 border border-slate-850 rounded-xl space-y-3 mt-4">
                  <p className="text-[10px] text-slate-400 font-semibold">ขั้นตอนปัจจุบันที่ต้องยืนยันข้อมูล (Human-in-the-loop):</p>
                  <p className="text-xs text-white italic font-light">"{apiResult.current_step}"</p>
                  <div className="flex gap-2 justify-end pt-1">
                    <button 
                      onClick={async () => {
                        setLoading(true);
                        try {
                          await api.approveWorkflow(apiResult.workflow_id);
                          alert("อนุมัติขั้นตอนเวิร์กโฟลว์เรียบร้อยแล้ว!");
                          checkStatus();
                        } catch (e) {
                          alert("ไม่สามารถอนุมัติเวิร์กโฟลว์ได้");
                        } finally {
                          setLoading(false);
                        }
                      }} 
                      disabled={loading}
                      className="px-3 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white rounded text-[10px] font-semibold transition-colors disabled:opacity-50 disabled:pointer-events-none"
                    >
                      {loading ? "กำลังบันทึก..." : "ยืนยันคำสั่ง (Approve Action)"}
                    </button>
                  </div>
                </div>
              )}
            </div>
          )}

          {apiResult && apiResult.error && (
            <div className="p-4 bg-rose-950/20 border border-rose-800/40 rounded-xl text-rose-350 text-xs">
              {apiResult.error}
            </div>
          )}
        </div>

        <div className="md:col-span-2 space-y-6">
          <div className="glass p-6 rounded-2xl space-y-4">
            <h4 className="text-xs font-bold text-slate-200 uppercase tracking-wider">เวิร์กโฟลว์อัตโนมัติ</h4>
            <p className="text-xs text-slate-400 leading-relaxed font-light">
              ประสานงานข้ามเครื่องมือผ่านเอเจนต์และตรวจสอบภัยพิบัติสุขภาพร่วมกันอย่างเป็นระบบ และเชื่อมต่อกระบวนการมนุษย์อนุมัติ (Human-in-the-loop)
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
