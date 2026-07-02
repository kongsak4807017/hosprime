import { useState, useEffect } from 'react';
import { ThumbsUp, ThumbsDown, Shield, Wallet, Award, Activity, Settings, Info } from 'lucide-react';
import { api, QueryLogResponse } from '../../lib/api';

interface AgentConfig {
  id: number;
  name: string;
  role: string;
  status: string;
  is_active: boolean;
  temperature: number;
  token_quota: number;
  token_used: number;
  token_balance: number;
  token_rewarded: number;
}

interface AgentLogItem {
  id: number;
  agent_id: string;
  task_type: string;
  input_data: any;
  output_data: any;
  status: string;
  created_at: string;
}

export function LogsTab() {
  const [activeSubTab, setActiveSubTab] = useState<'user' | 'agent' | 'governance'>('user');
  
  // Tab 1: User Query Logs
  const [userLogs, setUserLogs] = useState<QueryLogResponse[]>([]);
  const [loadingUserLogs, setLoadingUserLogs] = useState(false);

  // Tab 2: All AI Agent Logs
  const [agentLogs, setAgentLogs] = useState<AgentLogItem[]>([]);
  const [loadingAgentLogs, setLoadingAgentLogs] = useState(false);
  const [selectedAgentLog, setSelectedAgentLog] = useState<AgentLogItem | null>(null);

  // Tab 3: Governance Agent Configs (Loaded from DB)
  const [agentsList, setAgentsList] = useState<AgentConfig[]>([]);
  const [loadingAgents, setLoadingAgents] = useState(false);
  const [selectedAgentForQuota, setSelectedAgentForQuota] = useState<string | null>(null);
  const [newQuotaValue, setNewQuotaValue] = useState<number>(100000);

  const fetchUserLogs = async () => {
    setLoadingUserLogs(true);
    try {
      const data = await api.getQueryLogs();
      setUserLogs(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoadingUserLogs(false);
    }
  };

  const fetchAgentLogs = async () => {
    setLoadingAgentLogs(true);
    try {
      const data = await api.getAgentLogs();
      setAgentLogs(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoadingAgentLogs(false);
    }
  };

  const fetchAgents = async () => {
    setLoadingAgents(true);
    try {
      const data = await api.getAgents();
      setAgentsList(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoadingAgents(false);
    }
  };

  useEffect(() => {
    fetchUserLogs();
    fetchAgentLogs();
    fetchAgents();
  }, []);

  // Governance Handlers
  const handleToggleAgent = async (role: string, currentStatus: boolean) => {
    try {
      await api.updateAgent(role, { is_active: !currentStatus });
      fetchAgents();
    } catch (e) {
      alert("ปรับเปลี่ยนสถานะการทำงานล้มเหลว: " + e);
    }
  };

  const handleTempChange = async (role: string, val: number) => {
    try {
      // อัปเดตใน state เพื่อให้เลื่อนได้อย่างลื่นไหล ไม่สะดุด
      setAgentsList(prev => prev.map(a => a.role === role ? { ...a, temperature: val } : a));
      await api.updateAgent(role, { temperature: val });
    } catch (e) {
      console.error("แก้ไขความสร้างสรรค์ขัดข้อง:", e);
    }
  };

  const handleUpdateQuota = async () => {
    if (!selectedAgentForQuota) return;
    try {
      await api.updateAgent(selectedAgentForQuota, { token_quota: newQuotaValue });
      setSelectedAgentForQuota(null);
      fetchAgents();
      alert("ปรับปรุงโควตา Token ประจำสัปดาห์สำเร็จ!");
    } catch (e) {
      alert("ปรับปรุงโควตาล้มเหลว: " + e);
    }
  };

  return (
    <div className="max-w-7xl mx-auto space-y-6 text-white text-left animate-fade-in">
      
      {/* Tab Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h2 className="text-2xl font-bold tracking-tight font-outfit text-transparent bg-clip-text bg-gradient-to-r from-white via-slate-100 to-gold-400">
            📊 บันทึกกิจกรรมและการนิเทศการเงิน AI (Governance & Token Logs)
          </h2>
          <p className="text-slate-400 text-xs mt-1">
            ติดตามกิจกรรมของทั้ง User และ AI Twin ควบคุมพารามิเตอร์การประมวลผล ตลอดจนกำกับดูแลระบบการเงิน Token Economy ขององค์กร
          </p>
        </div>

        {/* Switcher Navigation */}
        <div className="flex bg-slate-900 p-1 rounded-2xl border border-slate-800 shrink-0">
          <button
            onClick={() => {
              setActiveSubTab('user');
              fetchUserLogs();
            }}
            className={`px-4 py-2 text-xs font-semibold rounded-xl transition-all ${
              activeSubTab === 'user' ? 'bg-slate-950 text-gold-400 border border-slate-800' : 'text-slate-400 hover:text-slate-250'
            }`}
          >
            👤 ถาม-ตอบ User (Search Logs)
          </button>
          <button
            onClick={() => {
              setActiveSubTab('agent');
              fetchAgentLogs();
            }}
            className={`px-4 py-2 text-xs font-semibold rounded-xl transition-all ${
              activeSubTab === 'agent' ? 'bg-slate-950 text-gold-400 border border-slate-800' : 'text-slate-400 hover:text-slate-250'
            }`}
          >
            ⚙️ ปฏิบัติการ AI (Agent Tasks)
          </button>
          <button
            onClick={() => {
              setActiveSubTab('governance');
              fetchAgents();
            }}
            className={`px-4 py-2 text-xs font-semibold rounded-xl transition-all ${
              activeSubTab === 'governance' ? 'bg-slate-950 text-gold-400 border border-slate-800' : 'text-slate-400 hover:text-slate-250'
            }`}
          >
            🛡️ บอร์ดนิเทศการเงิน AI (Governance)
          </button>
        </div>
      </div>

      {/* ======================================================== */}
      {/* SUBTAB 1: User Search Logs (user)                        */}
      {/* ======================================================== */}
      {activeSubTab === 'user' && (
        <div className="space-y-4 animate-fade-in">
          <div className="flex justify-between items-center px-1">
            <h3 className="text-xs font-bold text-slate-350 uppercase tracking-wider">บันทึกคำถาม RAG จากผู้ใช้ ({userLogs.length})</h3>
            <button onClick={fetchUserLogs} disabled={loadingUserLogs} className="text-gold-500 text-[10px] hover:text-gold-400">
              {loadingUserLogs ? 'กำลังรีเฟรช...' : '🔄 รีเฟรชข้อมูล'}
            </button>
          </div>

          <div className="glass rounded-2xl overflow-hidden border border-slate-850">
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse min-w-[800px]">
                <thead>
                  <tr className="bg-slate-950 border-b border-slate-850 text-slate-450 text-[10px] uppercase font-bold tracking-wider">
                    <th className="p-4 w-[25%]">ผู้ใช้ & คำถาม</th>
                    <th className="p-4 w-[40%]">คำตอบจาก Oracle RAG</th>
                    <th className="p-4">แหล่งความรู้อ้างอิง</th>
                    <th className="p-4 text-center">ความมั่นใจ</th>
                    <th className="p-4 text-right">ผลตรวจทาน</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-900/60 text-xs text-slate-300">
                  {userLogs.map((log) => (
                    <tr key={log.id} className="hover:bg-slate-900/10 transition-colors">
                      <td className="p-4 align-top break-words max-w-[200px]">
                        <p className="text-[9px] font-bold text-slate-500 uppercase font-mono">{log.user_id}</p>
                        <p className="font-semibold text-white mt-1">{log.question}</p>
                        <p className="text-[9px] text-slate-550 mt-1 font-mono">{new Date(log.created_at).toLocaleString('th-TH')}</p>
                      </td>
                      <td className="p-4 text-slate-400 align-top line-clamp-3 leading-relaxed whitespace-pre-wrap">
                        {log.answer.length > 250 ? `${log.answer.substring(0, 250)}...` : log.answer}
                      </td>
                      <td className="p-4 align-top">
                        <div className="flex flex-col gap-1 max-w-[150px]">
                          {log.sources && log.sources.slice(0, 2).map((src, i) => (
                            <span key={i} className="text-[10px] text-slate-500 truncate" title={src.document_title}>
                              - {src.document_title}
                            </span>
                          ))}
                          {log.sources && log.sources.length > 2 && (
                            <span className="text-[9px] text-gold-500 font-bold">+{log.sources.length - 2} ไฟล์อ้างอิงเพิ่ม</span>
                          )}
                        </div>
                      </td>
                      <td className="p-4 text-center align-top font-mono font-semibold text-white">
                        {(log.confidence * 100).toFixed(0)}%
                      </td>
                      <td className="p-4 text-right align-top shrink-0">
                        {log.feedback === 'positive' && (
                          <span className="inline-flex items-center gap-1 text-[9px] font-bold text-emerald-400 bg-emerald-950/30 px-2 py-0.5 rounded-full border border-emerald-900/40">
                            <ThumbsUp className="w-2.5 h-2.5" /> ตรงประเด็น
                          </span>
                        )}
                        {log.feedback === 'negative' && (
                          <span className="inline-flex items-center gap-1 text-[9px] font-bold text-rose-400 bg-rose-955/30 px-2 py-0.5 rounded-full border border-rose-900/40">
                            <ThumbsDown className="w-2.5 h-2.5" /> ไม่ตรง/มีช่องโหว่
                          </span>
                        )}
                        {!log.feedback && <span className="text-slate-600 text-[10px] font-light">ยังไม่มีผลประเมิน</span>}
                      </td>
                    </tr>
                  ))}
                  {userLogs.length === 0 && !loadingUserLogs && (
                    <tr>
                      <td colSpan={5} className="p-12 text-center text-slate-500">
                        ไม่มีประวัติการค้นหาข้อมูลในระบบ
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* ======================================================== */}
      {/* SUBTAB 2: AI Agent Logs (agent)                         */}
      {/* ======================================================== */}
      {activeSubTab === 'agent' && (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start animate-fade-in">
          
          {/* Left: Activity Table */}
          <div className="lg:col-span-8 space-y-4">
            <div className="flex justify-between items-center px-1">
              <h3 className="text-xs font-bold text-slate-350 uppercase tracking-wider">
                ประวัติงานและปฏิบัติการของ AI Agents ทั้งหมด ({agentLogs.length})
              </h3>
              <button onClick={fetchAgentLogs} disabled={loadingAgentLogs} className="text-gold-500 text-[10px] hover:text-gold-400">
                {loadingAgentLogs ? 'กำลังดึง...' : '🔄 รีเฟรชบอร์ด'}
              </button>
            </div>

            <div className="glass rounded-2xl overflow-hidden border border-slate-850">
              <div className="overflow-x-auto">
                <table className="w-full text-left border-collapse min-w-[700px]">
                  <thead>
                    <tr className="bg-slate-950 border-b border-slate-850 text-slate-450 text-[10px] uppercase font-bold tracking-wider">
                      <th className="p-4 w-[25%]">AI Agent / แผนก</th>
                      <th className="p-4">งานปฏิบัติการ (Task Type)</th>
                      <th className="p-4 text-center">ธุรกรรม Token (Cost / Earned)</th>
                      <th className="p-4 text-center">สถานะการทำงาน</th>
                      <th className="p-4 text-right">วันเวลาดำเนินงาน</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-900/60 text-xs text-slate-300">
                    {agentLogs.map((log) => {
                      // ดึงข้อมูล Token Economics จาก output_data ถ้ามี
                      let tokenDetail = null;
                      if (log.output_data) {
                        try {
                          const parsed = typeof log.output_data === 'object' ? log.output_data : JSON.parse(log.output_data);
                          if (parsed.token_economics) tokenDetail = parsed.token_economics;
                        } catch (e) {}
                      }

                      return (
                        <tr 
                          key={log.id} 
                          onClick={() => setSelectedAgentLog(log)}
                          className={`hover:bg-slate-900/20 transition-colors cursor-pointer ${
                            selectedAgentLog?.id === log.id ? 'bg-slate-900/40 border-l-4 border-gold-500' : ''
                          }`}
                        >
                          <td className="p-4 align-middle">
                            <div className="flex items-center gap-2">
                              <span className="text-md">🤖</span>
                              <div className="text-left">
                                <p className="font-bold text-white uppercase">{log.agent_id}</p>
                                <p className="text-[9px] text-slate-500 font-light">ID: #{log.id}</p>
                              </div>
                            </div>
                          </td>
                          <td className="p-4 align-middle font-mono text-slate-350 text-[11px]">
                            {log.task_type}
                          </td>
                          <td className="p-4 align-middle text-center">
                            {tokenDetail ? (
                              <div className="flex flex-col items-center gap-0.5 font-mono text-[10px]">
                                <span className="text-rose-400">🔴 -{tokenDetail.cost_tokens} Token (ใช้)</span>
                                <span className="text-emerald-400">🟢 +{tokenDetail.reward_tokens} Token (ได้)</span>
                              </div>
                            ) : (
                              <span className="text-slate-500 text-[10px] font-light">-</span>
                            )}
                          </td>
                          <td className="p-4 align-middle text-center">
                            <span className={`text-[9px] font-bold px-2.5 py-0.5 rounded-full border ${
                              log.status === 'success' || log.status === 'fallback'
                                ? 'bg-emerald-950/40 text-emerald-400 border-emerald-900/60' 
                                : 'bg-rose-955/35 text-rose-350 border-rose-900/60'
                            }`}>
                              {log.status === 'success' ? 'SUCCESS' : log.status === 'fallback' ? 'FALLBACK' : 'FAILED'}
                            </span>
                          </td>
                          <td className="p-4 align-middle text-right font-mono text-[10px] text-slate-500">
                            {new Date(log.created_at).toLocaleString('th-TH')}
                          </td>
                        </tr>
                      );
                    })}
                    {agentLogs.length === 0 && !loadingAgentLogs && (
                      <tr>
                        <td colSpan={5} className="p-12 text-center text-slate-500">
                          ไม่มีบันทึกปฏิบัติการภารกิจของ AI Agents ในประวัติ
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          {/* Right: Detailed Log Audit Inspector */}
          <div className="lg:col-span-4">
            {selectedAgentLog ? (
              <div className="bg-slate-900/20 border border-slate-850 glass p-5 rounded-2xl space-y-4 animate-fade-in">
                <div className="flex items-center justify-between pb-2 border-b border-slate-900">
                  <h4 className="text-xs font-bold text-slate-350">กล้องส่องประวัติงานและข้อมูลดิบ AI</h4>
                  <button onClick={() => setSelectedAgentLog(null)} className="text-slate-500 hover:text-white text-xs">✕ ปิด</button>
                </div>
                <div className="space-y-2 text-left text-xs">
                  <p className="font-bold text-white uppercase text-sm">🤖 {selectedAgentLog.agent_id}</p>
                  <p className="text-[10px] text-slate-500">
                    ปฏิบัติงานประเภท: <strong className="text-slate-400 font-mono">{selectedAgentLog.task_type}</strong>
                  </p>
                </div>

                {/* แสดงข้อมูล Token Transaction ด้านการเงินจำลอง ใน Inspector */}
                {(() => {
                  let tokenDetail = null;
                  if (selectedAgentLog.output_data) {
                    try {
                      const parsed = typeof selectedAgentLog.output_data === 'object' ? selectedAgentLog.output_data : JSON.parse(selectedAgentLog.output_data);
                      if (parsed.token_economics) tokenDetail = parsed.token_economics;
                    } catch (e) {}
                  }

                  if (!tokenDetail) return null;
                  return (
                    <div className="p-4 bg-slate-950 border border-slate-850/60 rounded-xl space-y-2 text-left text-xs">
                      <p className="font-bold text-gold-400 flex items-center gap-1.5">
                        <Wallet className="w-3.5 h-3.5" /> รายงานธุรกรรมบัญชี (Financial Audit)
                      </p>
                      <div className="grid grid-cols-2 gap-2 text-[10px] text-slate-300 font-mono pt-1">
                        <div>Input Tokens: <span>{tokenDetail.input_tokens}</span></div>
                        <div>Output Tokens: <span>{tokenDetail.output_tokens}</span></div>
                        <div className="text-rose-400">หักจ่ายค่าพยากรณ์: <span>-{tokenDetail.cost_tokens}</span></div>
                        <div className="text-emerald-400">รับตอบแทนมูลค่าชิ้นงาน: <span>+{tokenDetail.reward_tokens}</span></div>
                        <div className="col-span-2 pt-2 border-t border-slate-900 text-white font-bold flex justify-between">
                          <span>เครดิตสะสมในกระเป๋า:</span>
                          <span className="text-gold-400">{tokenDetail.new_balance_tokens} Tokens</span>
                        </div>
                      </div>
                    </div>
                  );
                })()}

                <div className="space-y-3 pt-1">
                  {/* Input Data */}
                  <div className="space-y-1">
                    <p className="text-[10px] text-slate-550 uppercase tracking-wider font-bold">ข้อมูลพารามิเตอร์ส่งเข้าระบบ (Input Data):</p>
                    <pre className="p-3 bg-slate-950 border border-slate-850 rounded-xl text-[10px] text-slate-400 overflow-x-auto max-h-[120px] font-mono leading-relaxed text-left">
                      {typeof selectedAgentLog.input_data === 'object' 
                        ? JSON.stringify(selectedAgentLog.input_data, null, 2) 
                        : selectedAgentLog.input_data}
                    </pre>
                  </div>

                  {/* Output Data */}
                  <div className="space-y-1">
                    <p className="text-[10px] text-slate-550 uppercase tracking-wider font-bold">ผลผลิตชิ้นงานสำเร็จโดย AI (Output Data):</p>
                    <pre className="p-3 bg-slate-955 border border-slate-850 rounded-xl text-[10px] text-gold-400/90 overflow-y-auto max-h-[160px] font-mono leading-relaxed text-left whitespace-pre-wrap">
                      {(() => {
                        let text = "";
                        if (selectedAgentLog.output_data) {
                          if (typeof selectedAgentLog.output_data === 'object') {
                            text = selectedAgentLog.output_data.response || JSON.stringify(selectedAgentLog.output_data, null, 2);
                          } else {
                            try {
                              const parsed = JSON.parse(selectedAgentLog.output_data);
                              text = parsed.response || selectedAgentLog.output_data;
                            } catch (e) {
                              text = selectedAgentLog.output_data;
                            }
                          }
                        }
                        return text;
                      })()}
                    </pre>
                  </div>
                </div>
              </div>
            ) : (
              <div className="bg-slate-955/20 border border-slate-850 glass p-10 rounded-2xl flex flex-col items-center justify-center text-center text-slate-500 min-h-[300px]">
                <Shield className="w-10 h-10 text-slate-800 mb-4 animate-bounce" />
                <p className="text-xs">กรุณาเลือกบรรทัดรายการความเคลื่อนไหวจากตารางงานด้านซ้าย เพื่อทำการตรวจสอบส่องข้อมูลส่งเข้า (Input), ผลสัมฤทธิ์ (Output) และประวัติบัญชีเงิน Token ของ AI ฝ่ายย่อย</p>
              </div>
            )}
          </div>

        </div>
      )}

      {/* ======================================================== */}
      {/* SUBTAB 3: AI Agents Governance Board (governance)       */}
      {/* ======================================================== */}
      {activeSubTab === 'governance' && (
        <div className="space-y-6 animate-fade-in">
          
          <div className="p-5 bg-slate-900/20 border border-slate-850 glass rounded-2xl text-left space-y-2 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
            <div className="space-y-1">
              <h3 className="text-sm font-bold text-white font-outfit flex items-center gap-2">
                <Shield className="w-4 h-4 text-gold-400 animate-pulse" /> บอร์ดควบคุมและนิเทศการเงิน AI (AI Governance & Token Economy)
              </h3>
              <p className="text-xs text-slate-400 leading-relaxed font-light">
                คุณสามารถเปิด/ปิดการทำงานของแต่ละ AI Twin ปรับเปลี่ยนอุณหภูมิความสร้างสรรค์ ควบคุมเครดิตโควตาประจำสัปดาห์ และตรวจวิเคราะห์สภาพคล่องทางการเงินของโลกทวินในภาพรวม
              </p>
            </div>
            <button onClick={fetchAgents} disabled={loadingAgents} className="shrink-0 py-2 px-4 bg-slate-950 border border-slate-800 text-xs text-gold-400 hover:text-gold-300 font-semibold rounded-xl">
              {loadingAgents ? 'กำลังรีโหลด...' : '🔄 รีโหลดข้อมูลการเงิน'}
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {agentsList.map((agent) => {
              const nameMap: Record<string, string> = {
                "pho": "PHO Chief Twin (สสจ.)",
                "cfo": "CFO Financial Twin (การคลัง)",
                "cio": "CIO Technology Twin (ระบบไอที)",
                "tb": "TB Disease Specialist (วัณโรค)",
                "pm25": "PM2.5 Crisis Specialist (ฝุ่น)",
                "disaster": "Disaster Response Twin (กู้ชีพ)",
                "legal": "Legal Advisor Twin (นิติกร)",
                "admin": "AI Agent Admin (ผู้ช่วยระบบ)"
              };

              // อัตราส่วนความคืบหน้าการใช้ Token
              const usagePercent = Math.min(100, (agent.token_used / agent.token_quota) * 100);

              return (
                <div 
                  key={agent.id} 
                  className={`p-5 rounded-2xl border transition-all flex flex-col justify-between ${
                    agent.is_active 
                      ? 'bg-slate-900/40 border-slate-850 shadow-lg' 
                      : 'bg-slate-955/70 border-slate-900 opacity-60'
                  }`}
                >
                  <div className="space-y-4">
                    
                    {/* Header: Name and Toggle */}
                    <div className="flex justify-between items-start">
                      <div className="text-left space-y-0.5">
                        <div className="flex items-center gap-1.5">
                          <span className={`w-2 h-2 rounded-full ${agent.is_active ? 'bg-green-500 animate-ping' : 'bg-slate-650'}`}></span>
                          <h4 className="text-xs font-bold text-white uppercase">{agent.role} Agent</h4>
                        </div>
                        <p className="text-[10px] text-slate-400 font-light">{nameMap[agent.role] || agent.name}</p>
                      </div>

                      <button
                        onClick={() => handleToggleAgent(agent.role, agent.is_active)}
                        className={`px-3 py-1.5 rounded-lg text-[10px] font-bold border transition-all ${
                          agent.is_active 
                            ? 'bg-emerald-950/40 hover:bg-emerald-900/30 text-emerald-400 border-emerald-900/60' 
                            : 'bg-slate-900 hover:bg-slate-800 text-slate-500 border-slate-800'
                        }`}
                      >
                        {agent.is_active ? 'ACTIVE (เปิด)' : 'INACTIVE (ปิด)'}
                      </button>
                    </div>

                    {/* Financial Dashboard section (Token Economy info) */}
                    <div className="bg-slate-950/60 border border-slate-900/50 rounded-xl p-3.5 space-y-3">
                      
                      {/* Wallet Balance */}
                      <div className="flex justify-between items-center text-xs">
                        <div className="flex items-center gap-1.5 text-slate-400">
                          <Wallet className="w-3.5 h-3.5 text-gold-500" />
                          <span>เครดิตสะสมคงเหลือ:</span>
                        </div>
                        <span className="font-bold text-gold-400 font-mono">{agent.token_balance.toLocaleString()} Tokens</span>
                      </div>

                      {/* Cumulative Reward */}
                      <div className="flex justify-between items-center text-xs border-b border-slate-900 pb-2">
                        <div className="flex items-center gap-1.5 text-slate-400">
                          <Award className="w-3.5 h-3.5 text-emerald-400" />
                          <span>รางวัลชิ้นงานสะสม:</span>
                        </div>
                        <span className="font-semibold text-emerald-400 font-mono">+{agent.token_rewarded.toLocaleString()} Tokens</span>
                      </div>

                      {/* Weekly Token Quota Usage Progress */}
                      <div className="space-y-1 text-left pt-1">
                        <div className="flex justify-between text-[9px] text-slate-400">
                          <span>โควตาประจำสัปดาห์:</span>
                          <span className="font-mono">{agent.token_used.toLocaleString()} / {agent.token_quota.toLocaleString()} Tokens ({usagePercent.toFixed(0)}%)</span>
                        </div>
                        <div className="w-full bg-slate-900 h-1.5 rounded-full overflow-hidden">
                          <div 
                            className={`h-full rounded-full transition-all duration-300 ${
                              usagePercent > 85 ? 'bg-rose-500' : usagePercent > 50 ? 'bg-amber-500' : 'bg-sky-400'
                            }`}
                            style={{ width: `${usagePercent}%` }}
                          ></div>
                        </div>
                      </div>

                      {/* Modify Quota Button */}
                      {agent.is_active && (
                        <button 
                          onClick={() => {
                            setSelectedAgentForQuota(agent.role);
                            setNewQuotaValue(agent.token_quota);
                          }}
                          className="w-full py-1 text-[9px] text-slate-500 hover:text-gold-400 transition-colors flex items-center justify-center gap-1 border border-slate-900 hover:border-slate-850 rounded-lg mt-1"
                        >
                          <Settings className="w-2.5 h-2.5" /> ปรับแต่งโควตา Token
                        </button>
                      )}
                    </div>

                    {/* Temperature Slider */}
                    <div className="space-y-1.5 text-left">
                      <div className="flex justify-between text-[10px]">
                        <span className="text-slate-500 flex items-center gap-1"><Activity className="w-3 h-3" /> อุณหภูมิความสร้างสรรค์</span>
                        <strong className="text-gold-400">{agent.temperature}</strong>
                      </div>
                      <input 
                        type="range" 
                        min="0" 
                        max="1" 
                        step="0.1" 
                        value={agent.temperature} 
                        onChange={(e) => handleTempChange(agent.role, parseFloat(e.target.value))}
                        disabled={!agent.is_active}
                        className="w-full accent-gold-500 bg-slate-950 h-1 rounded-full border-0 cursor-pointer disabled:opacity-30"
                      />
                      <div className="flex justify-between text-[9px] text-slate-600">
                        <span>เป็นทางการ / แม่นยำ</span>
                        <span>อิสระ / ความคิดสร้างสรรค์</span>
                      </div>
                    </div>

                  </div>
                </div>
              );
            })}
          </div>

          {/* Quota Settings Modal */}
          {selectedAgentForQuota && (
            <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
              <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 max-w-sm w-full space-y-4 text-left animate-scale-up">
                <div>
                  <h4 className="text-sm font-bold text-white uppercase">⚙️ ปรับเครดิตโควตา AI ({selectedAgentForQuota})</h4>
                  <p className="text-[10px] text-slate-400 mt-1">กำหนดลิมิตจำนวนการส่งและดึง Token ของเอเจนต์ตัวนี้ประจำสัปดาห์</p>
                </div>
                <div className="space-y-2">
                  <label className="text-[10px] text-slate-550 font-bold block">ระบุจำนวน Token (ต่อสัปดาห์):</label>
                  <input 
                    type="number"
                    value={newQuotaValue}
                    onChange={(e) => setNewQuotaValue(parseInt(e.target.value) || 0)}
                    className="w-full bg-slate-955 border border-slate-800 focus:border-gold-500/50 rounded-xl py-2 px-3 text-xs font-mono text-white outline-none"
                  />
                  <div className="p-3 bg-slate-950 border border-slate-850/60 rounded-lg text-[9px] text-slate-500 leading-relaxed flex gap-1.5">
                    <Info className="w-3.5 h-3.5 text-gold-400 shrink-0" />
                    <span>หากเครดิตใช้งานเกินโควตาประจำสัปดาห์ ระบบนิเทศการเงิน AI จะปิดใช้งานเอเจนต์นี้โดยอัตโนมัติเพื่อป้องกันค่าใช้จ่ายบานปลาย</span>
                  </div>
                </div>
                <div className="flex gap-2">
                  <button 
                    onClick={() => setSelectedAgentForQuota(null)}
                    className="flex-1 py-2 bg-slate-950 text-slate-400 text-xs font-bold rounded-xl border border-slate-850 hover:bg-slate-900"
                  >
                    ยกเลิก
                  </button>
                  <button 
                    onClick={handleUpdateQuota}
                    className="flex-1 py-2 bg-gradient-to-r from-gold-600 to-amber-700 hover:from-gold-500 hover:to-amber-600 text-slate-950 text-xs font-bold rounded-xl"
                  >
                    อัปเดตเครดิต
                  </button>
                </div>
              </div>
            </div>
          )}

        </div>
      )}

    </div>
  );
}
