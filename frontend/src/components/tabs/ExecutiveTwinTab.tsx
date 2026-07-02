import { useState, useEffect } from 'react';
import { api } from '../../lib/api';

interface TaskItem {
  id: string;
  type: string;
  urgency: 'high' | 'medium';
  title: string;
  description: string;
}

export function ExecutiveTwinTab() {
  const [loading, setLoading] = useState(false);
  const [agentsList, setAgentsList] = useState<any[]>([]);
  const [selectedAgentRole, setSelectedAgentRole] = useState<string>('executive');
  
  // Navigation tabs (Office Workspace vs Agent Marketplace)
  const [activeTab, setActiveTab] = useState<'office' | 'marketplace'>('office');
  
  // Dashboard & Simulation States inside office
  const [activeWorkspaceTab, setActiveWorkspaceTab] = useState<'draft' | 'consult' | 'board' | 'simulator' | 'orchestrator' | 'monitor'>('draft');
  const [monitorLogs, setMonitorLogs] = useState<any[]>([]);
  const [activeTelemetry, setActiveTelemetry] = useState<Record<string, { cpu: number, mem: number, load: number }>>({});
  const [agentBrains, setAgentBrains] = useState<Record<string, string>>({});
  const [smallTalkLogs, setSmallTalkLogs] = useState<any[]>([]);
  const [flowActive, setFlowActive] = useState(false);
  const [flowStep, setFlowStep] = useState(0);

  // จำลองการรัน Flow แบบ n8n-style
  const handleRunFlowSimulation = () => {
    if (flowActive) return;
    setFlowActive(true);
    setFlowStep(1);
    
    setTimeout(() => setFlowStep(2), 1500);
    setTimeout(() => setFlowStep(3), 3000);
    setTimeout(() => setFlowStep(4), 4500);
    setTimeout(() => setFlowStep(5), 6000);
    setTimeout(() => {
      setFlowActive(false);
      setFlowStep(0);
      alert("🎉 ประมวลผล Workflow สำเร็จ! ดึงข้อมูล RAG ตรวจสอบ PDPA และร่างรายงานส่งสั่งการ PHO เรียบร้อยแล้ว");
    }, 7500);
  };
  const [draftResult, setDraftResult] = useState<any>(null);

  // What-If Simulation States
  const [opdLoad, setOpdLoad] = useState<number>(1.0);
  const [icuBeds, setIcuBeds] = useState<number>(12);
  const [staffFte, setStaffFte] = useState<number>(1.0);
  const [simResult, setSimResult] = useState<any>(null);
  const [simLoading, setSimLoading] = useState<boolean>(false);

  // Master Orchestrator States
  const [goalInput, setGoalInput] = useState<string>('วิเคราะห์อัตราครองเตียงที่พุ่งสูง และประเมินร่วมกับระเบียบส่งต่อระดับจังหวัดเพื่อเสนอมาตรการแก้ไข');
  const [orchestrationResult, setOrchestrationResult] = useState<any>(null);
  const [orchestrationLoading, setOrchestrationLoading] = useState<boolean>(false);
  const [emergencyActive, setEmergencyActive] = useState<boolean>(false);

  // Data Lineage Modal/Panel States
    const [lineageTarget, setLineageTarget] = useState<string | null>(null);

  // Helper function to return dynamic activity of agents in the simulation office
  const getAgentActivity = (role: string) => {
    if (emergencyActive) {
      return { text: "🚨 ระงับชั่วคราว (Suspended)", status: "suspended" };
    }

    // ค้นหา log ล่าสุดของตำแหน่งนี้ใน Autonomous Logs
    const latest = monitorLogs.find(l => l.sender === role);

    if (role === 'executive') {
      if (orchestrationLoading) return { text: "⚙️ กำลังประมวลนโยบายและสั่งการข้ามฝ่าย...", status: "busy" };
      return { text: latest ? latest.text : "🟢 สแตนด์บาย | พร้อมรับข้อสั่งการระดับสูง", status: latest ? "busy" : "idle" };
    }
    if (role === 'cos') {
      if (orchestrationLoading) return { text: "⚙️ กำลังแตกย่อยเป้าหมายเป็นโครงการ...", status: "busy" };
      return { text: latest ? latest.text : "🟢 สแตนด์บาย | เฝ้าระวังกิจกรรมประสานงานหลัก", status: latest ? "busy" : "idle" };
    }
    if (role === 'analyst') {
      if (orchestrationLoading) return { text: "⚙️ กำลังรันแผนประเมิน MOPH OKRs...", status: "busy" };
      return { text: latest ? latest.text : "🟢 สแตนด์บาย | อัปเดตตัวชี้วัดรายสัปดาห์", status: latest ? "busy" : "idle" };
    }
    if (role === 'knowledge') {
      if (orchestrationLoading) return { text: "📚 กำลังดึงคู่มือระเบียบ SOP (RAG 3072D)...", status: "busy" };
      if (chatLoading && selectedAgentRole === 'knowledge') return { text: "📚 กำลังตรวจสอบมาตรฐาน SOP ในคลังความรู้...", status: "busy" };
      return { text: latest ? latest.text : "🟢 สแตนด์บาย | ตรวจสอบระเบียบปฏิบัติราชการ", status: latest ? "busy" : "idle" };
    }
    if (role === 'report') {
      if (loading) return { text: "✍ กำลังร่างหนังสือสั่งการจังหวัดตราครุฑ...", status: "busy" };
      if (orchestrationLoading) return { text: "✍ กำลังเรียบเรียงสรุปรายงานผู้บริหาร...", status: "busy" };
      return { text: latest ? latest.text : "🟢 สแตนด์บาย | จัดเตรียมสำนวนและเล่มรายงาน", status: latest ? "busy" : "idle" };
    }
    if (role === 'coo') {
      if (simLoading) return { text: "🔮 กำลังจำลองสถิติคิวบริการและอัตราครองเตียง...", status: "busy" };
      return { text: latest ? latest.text : "🟢 สแตนด์บาย | ติดตามคิวผู้ป่วยนอกและทรัพยากรเตียง", status: latest ? "busy" : "idle" };
    }
    if (role === 'cfo') {
      if (simLoading) return { text: "💰 กำลังประเมินผลกระทบวินัยการเงินการคลัง...", status: "busy" };
      return { text: latest ? latest.text : "🟢 สแตนด์บาย | ตรวจสอบอัตราเบิกจ่ายและเคลมรายได้", status: latest ? "busy" : "idle" };
    }
    if (role === 'meeting') {
      return { text: latest ? latest.text : "🟢 สแตนด์บาย | รอดึงข้อมูลมติที่ประชุมและ Action Items", status: latest ? "busy" : "idle" };
    }
    if (role === 'provincial') {
      return { text: latest ? latest.text : "🟢 สแตนด์บาย | ติดตามโครงข่าย refer และภัยพิบัติตำบล", status: latest ? "busy" : "idle" };
    }
    if (role === 'datagov') {
      if (orchestrationLoading || chatLoading) return { text: "🔒 กำลังตรวจสอบ PDPA และสิทธิ์ EHR Access...", status: "busy" };
      return { text: latest ? latest.text : "🟢 สแตนด์บาย | ตรวจทานความปลอดภัยและมาตรฐานข้อมูล", status: latest ? "busy" : "idle" };
    }

    // AI จัดการข้อมูลหลังบ้าน
    if (role === 'db_monitor') {
      if (simLoading) return { text: "⚡ กำลังสอบทานทราฟฟิกข้อมูลบริการ OPD/ICU...", status: "busy" };
      return { text: latest ? latest.text : "🟢 สแตนด์บาย | บำรุงรักษา SQLite Data Layer", status: latest ? "busy" : "idle" };
    }
    if (role === 'rag_optimizer') {
      if (orchestrationLoading) return { text: "🧠 กำลังประมวลผล Vector Embeddings 3072 มิติ...", status: "busy" };
      return { text: latest ? latest.text : "🟢 สแตนด์บาย | ปรับแต่งดัชนีคลังความรู้ RAG", status: latest ? "busy" : "idle" };
    }
    if (role === 'security_officer') {
      if (emergencyActive) return { text: "🚨 ระบบความมั่นคงสารสนเทศถูกปิดชั่วคราว", status: "suspended" };
      return { text: latest ? latest.text : "🟢 สแตนด์บาย | เฝ้าระวัง Cyber-Attack และ Ransomware", status: latest ? "busy" : "idle" };
    }

    return { text: latest ? latest.text : "🟢 ออนไลน์ | สแตนด์บายปฏิบัติงาน", status: latest ? "busy" : "idle" };
  };
  
  // Helper to render office desks in floor plan
  const renderDesk = (role: string) => {
    const detailsMap: Record<string, { shortName: string, icon: string }> = {
      executive: { shortName: "ผู้อำนวยการดิจิทัล", icon: "👔" },
      cos: { shortName: "หัวหน้าสำนักงาน", icon: "📋" },
      analyst: { shortName: "ฝ่ายยุทธศาสตร์", icon: "📊" },
      knowledge: { shortName: "ผู้ช่วยคลังปัญญา", icon: "📚" },
      report: { shortName: "ผู้ร่างเอกสาร", icon: "✍" },
      meeting: { shortName: "ผู้จดสรุปประชุม", icon: "🎙️" },
      coo: { shortName: "ฝ่ายบริการแพทย์", icon: "🏥" },
      cfo: { shortName: "ฝ่ายบริหารการเงิน", icon: "💰" },
      provincial: { shortName: "ประสานจังหวัด", icon: "🗺️" },
      datagov: { shortName: "ธรรมภิบาลข้อมูล", icon: "🔒" },
      db_monitor: { shortName: "Log Intel", icon: "⚡" },
      rag_optimizer: { shortName: "RAG Opt (3072D)", icon: "🧠" },
      security_officer: { shortName: "ผู้คุมความปลอดภัย", icon: "🛡️" }
    };

    const meta = detailsMap[role] || { shortName: role.toUpperCase(), icon: "👤" };
    const stats = activeTelemetry[role] || { cpu: 2, mem: 60, load: 0 };
    const act = getAgentActivity(role);
    const isSelected = selectedAgentRole === role;
    const model = agentBrains[role] || "GPT-4o";

    return (
      <div 
        onClick={() => setSelectedAgentRole(role)}
        className={`p-2.5 rounded-xl border text-left cursor-pointer transition-all duration-150 relative overflow-hidden group ${
          isSelected 
            ? 'bg-slate-900 border-gold-500/50 text-white ring-1 ring-gold-500/20 shadow-md' 
            : 'bg-slate-950/80 border-slate-900 hover:bg-slate-900/40 hover:border-slate-800 text-slate-400'
        }`}
        title={`${meta.shortName} | Model: ${model} | Status: ${act.status.toUpperCase()}`}
      >
        {isSelected && (
          <div className="absolute top-0 left-0 bottom-0 w-0.5 bg-gold-400"></div>
        )}
        {act.status === 'busy' && (
          <div className="absolute inset-0 bg-amber-500/5 animate-pulse pointer-events-none"></div>
        )}
        {emergencyActive && (
          <div className="absolute inset-0 bg-red-950/20 pointer-events-none"></div>
        )}
        
        <div className="flex justify-between items-center gap-1">
          <span className="truncate block font-bold text-[9.5px] text-slate-200">{meta.icon} {meta.shortName}</span>
          <span className={`w-1.5 h-1.5 rounded-full ${
            emergencyActive 
              ? 'bg-red-500 animate-pulse' 
              : act.status === 'busy' 
              ? 'bg-amber-500 animate-pulse' 
              : 'bg-emerald-500'
          }`} />
        </div>
        
        <div className="flex justify-between items-center text-[8px] font-mono text-slate-500 mt-1">
          <span>{stats.cpu}% CPU</span>
          <span className="text-[7.5px] text-slate-500 truncate max-w-[50%]">{model}</span>
        </div>
      </div>
    );
  };

    // Letter drafting form states
  const [letterType, setLetterType] = useState('บันทึกข้อความสั่งการจังหวัด (Official Order)');
  const [letterSubject, setLetterSubject] = useState('มาตรการคัดกรองวัณโรคเชิงรุกในกลุ่มเปราะบาง (เรือนจำและพื้นที่ดอนสูง)');
  const [letterDetail, setLetterDetail] = useState('มอบหมายให้กลุ่มงานควบคุมโรคประสานงานหน่วยงานที่เกี่ยวข้องและจัดชุดรถเอกซเรย์เคลื่อนที่พระราชทานลงพื้นที่สแกน 100% ภายใน 30 วัน');
  const [confidentiality, setConfidentiality] = useState('Internal');

  // Consultation Chat States
  const [chatInput, setChatInput] = useState('');
  const [chatLogs, setChatLogs] = useState<Record<string, { role: 'user' | 'assistant', text: string }[]>>({});
  const [chatLoading, setChatLoading] = useState(false);

  // AI Analytics State
  const [kpiAnalysis, setKpiAnalysis] = useState<string | null>(null);
  const [analyzingKpi, setAnalyzingKpi] = useState(false);

  // Marketplace Installation States
  const [installingPack, setInstallingPack] = useState<string | null>(null);

  // Fetch agents on mount and tab changes
  const fetchAgents = async () => {
    try {
      const data = await api.getAgents();
      const activeOnly = data.filter((a: any) => a.is_active);
      setAgentsList(activeOnly);
      
      // ซิงก์สมองของแต่ละตัวจาก DB เข้าสู่ local state ของหน้าบ้าน
      const dbBrains: Record<string, string> = {};
      data.forEach((agent: any) => {
        if (agent.role && agent.model_name) {
          dbBrains[agent.role] = agent.model_name;
        }
      });
      setAgentBrains(prev => ({ ...prev, ...dbBrains }));

      // หากไม่มีเอเจนต์ตัวใดเลยที่ active ถือว่าระบบกำลังโดนระงับฉุกเฉิน
      if (data.length > 0 && activeOnly.length === 0) {
        setEmergencyActive(true);
      } else {
        setEmergencyActive(false);
      }
    } catch (err) {
      console.error('Failed to fetch agents', err);
    }
  };

  // Run simulation
  const handleRunSimulation = async () => {
    setSimLoading(true);
    setSimResult(null);
    try {
      const data = await api.simulateTwinMetrics(opdLoad, icuBeds, staffFte);
      setSimResult(data.metrics);
    } catch (e: any) {
      alert(`การจำลองสถานการณ์ขัดข้อง: ${e.message}`);
    } finally {
      setSimLoading(false);
    }
  };

  // Run Orchestrator flow
  const handleRunOrchestrator = async () => {
    if (!goalInput.trim()) return;
    setOrchestrationLoading(true);
    setOrchestrationResult(null);
    try {
      const data = await api.orchestrateEnterpriseFlow(goalInput);
      setOrchestrationResult(data);
    } catch (e: any) {
      alert(`ระบบ Master Orchestrator ขัดข้อง: ${e.message}`);
    } finally {
      setOrchestrationLoading(false);
    }
  };

  // Trigger Emergency Stop (disable all agents)
  const handleEmergencyStop = async () => {
    if (!window.confirm('🚨 คุณต้องการกดสั่งระงับระบบปฏิบัติการ AI ทั้งหมดเพื่อความมั่นคงและปลอดภัยของระบบสารสนเทศองค์กรทันทีหรือไม่?')) {
      return;
    }
    setLoading(true);
    try {
      const allAgents = await api.getAgents();
      const updatePromises = allAgents.map((agent: any) => 
        api.updateAgent(agent.role, { is_active: false })
      );
      await Promise.all(updatePromises);
      setEmergencyActive(true);
      alert('⚠️ ระบบความมั่นคงสารสนเทศ: ทำการสั่งปิดการทำงานของ AI Agents ทั้งหมดสำเร็จแล้ว!');
      await fetchAgents();
    } catch (e: any) {
      alert(`ความพยายามปิดการสั่งงานฉุกเฉินล้มเหลว: ${e.message}`);
    } finally {
      setLoading(false);
    }
  };

  // Reactivate system (Re-enable agents)
  const handleReactivateSystem = async () => {
    setLoading(true);
    try {
      const allAgents = await api.getAgents();
      const defaultRoles = ['executive', 'cos', 'analyst', 'knowledge', 'report', 'meeting', 'datagov', 'cfo', 'coo', 'provincial'];
      const updatePromises = allAgents
        .filter((agent: any) => defaultRoles.includes(agent.role))
        .map((agent: any) => api.updateAgent(agent.role, { is_active: true }));
      await Promise.all(updatePromises);
      setEmergencyActive(false);
      alert('🟢 เปิดระบบการทำงานของ AI Assistants เริ่มต้น 10 ตำแหน่ง เรียบร้อยแล้ว!');
      await fetchAgents();
    } catch (e: any) {
      alert(`ไม่สามารถกู้คืนระบบได้: ${e.message}`);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAgents();
    
    // ตั้งค่าโมเดลสมองเริ่มต้นสำหรับตำแหน่งงานต่างๆ
    const defaultBrains: any = {};
    const allRoles = ['executive', 'cos', 'analyst', 'knowledge', 'report', 'meeting', 'datagov', 'cfo', 'coo', 'provincial', 'db_monitor', 'rag_optimizer', 'security_officer'];
    allRoles.forEach(r => {
      if (['executive', 'cos'].includes(r)) defaultBrains[r] = 'Claude 3.5 Sonnet';
      else if (['analyst', 'provincial', 'cfo'].includes(r)) defaultBrains[r] = 'Gemini 1.5 Pro';
      else if (['rag_optimizer', 'db_monitor'].includes(r)) defaultBrains[r] = 'DeepSeek R1';
      else defaultBrains[r] = 'GPT-4o';
    });
    setAgentBrains(defaultBrains);

    // ตั้งค่าบทสนทนาจำลองหลังบ้านเริ่มต้น
    setSmallTalkLogs([
      { sender: "cos", text: "ดึงรายงาน MOPH KPIs ความพร้อมระบบ refer เตียงแล้ว ดำเนินการประสาน COO ด่วนครับ", time: "02:30:12" },
      { sender: "analyst", text: "รับทราบครับ กำลังสอบทานตัวชี้วัดความครอบคลุมวัณโรคในทัณฑสถานและส่งรายงานเสนอ PHO", time: "02:32:05" },
      { sender: "datagov", text: "สแกนทราฟฟิกข้อมูลเวชระเบียน EHR ข้ามเครือข่าย ปลอดภัย PDPA และสอดคล้อง 100%", time: "02:35:44" }
    ]);
  }, []);

  // เริ่มต้นตั้งค่า Telemetry และจำลองการทำงานอัตโนมัติ (Autonomous Simulation Loop)
  useEffect(() => {
    // โหลดประวัติกิจกรรมเริ่มต้น
    const initialLogs = [
      { timestamp: new Date().toLocaleTimeString(), sender: "system", text: "ระบบสำนักงานจำลองเริ่มต้นปฏิบัติการ (Virtual Office Engine Initialized)" },
      { timestamp: new Date().toLocaleTimeString(), sender: "datagov", text: "ตรวจทานความสอดคล้องมาตรฐานข้อมูล PDPA และ EHR Access Token สำเร็จ" },
      { timestamp: new Date().toLocaleTimeString(), sender: "db_monitor", text: "ตรวจสอบระบบฐานข้อมูลจำลอง SQLite Data Layer: สถานะปกติ, Latency 42ms" },
      { timestamp: new Date().toLocaleTimeString(), sender: "rag_optimizer", text: "เริ่มการประมวลผล Chunking ข้อมูล และปรับแต่ง Vector Index ขนาด 3072 มิติ" }
    ];
    setMonitorLogs(initialLogs);

    // จำลอง Telemetry และพลังงานสำหรับฝ่ายต่าง ๆ
    const roles = ['executive', 'cos', 'analyst', 'knowledge', 'report', 'meeting', 'datagov', 'cfo', 'coo', 'provincial', 'db_monitor', 'rag_optimizer', 'security_officer'];
    const initTelemetry: any = {};
    roles.forEach(r => {
      initTelemetry[r] = {
        cpu: Math.floor(Math.random() * 8 + 2),
        mem: Math.floor(Math.random() * 25 + 55),
        load: Math.floor(Math.random() * 3 + 1)
      };
    });
    setActiveTelemetry(initTelemetry);

    // รันการทำงานแบบ Autonomous ทุกๆ 6 วินาที
    const interval = setInterval(() => {
      if (emergencyActive) return; // หากสั่งการฉุกเฉิน จะหยุดกิจกรรมทั้งหมด

      const activeRoles = roles.filter(r => r !== 'executive'); // ผู้อำนวยการจะทำงานตามข้อสั่งการใหญ่
      const randomRole = activeRoles[Math.floor(Math.random() * activeRoles.length)];

      const activities: Record<string, string[]> = {
        cos: [
          "ตรวจสอบความสอดคล้องของโครงการประสานกำลังพลกับ MOPH KPIs",
          "ประสานงานฝ่ายยุทธศาสตร์เพื่อนำเข้าเป้าหมาย OKRs ชุดใหม่",
          "ตรวจทานผลประเมินวินัยการเงินเพื่อส่งต่อให้แก่ CFO พิจารณา"
        ],
        analyst: [
          "วิเคราะห์ผลกระทบอัตราส่งต่อ refer ผู้ป่วยระดับอำเภอดอยสูง",
          "ร่างแผนกลยุทธ์จำลองป้องกันโรค NCD Remission ระดับจังหวัด",
          "สอบทานรายงานสถานการณ์การเบิกจ่ายงบดำเนินการของแต่ละแผนก"
        ],
        knowledge: [
          "ดึงคู่มือ SOP-REF-03 แนวทางคัดแยกความเร่งด่วนผู้ป่วยนอก (Triage)",
          "ตรวจสอบข้อกฎหมายกรมบัญชีกลางเกี่ยวกับงบภัยพิบัติน้ำท่วมและหมอกควัน",
          "เพิ่มเนื้อหาคู่มือปฏิบัติงานควบคุมวัณโรคเชิงรุกเข้าสู่ Vector DB"
        ],
        report: [
          "เรียบเรียงสำนวนตราครุฑหนังสือสั่งการจัดส่งเครื่องกรองอากาศ",
          "จัดพิมพ์ตารางข้อมูลผู้ครองเตียงวิกฤต ICU เสนอ PHO ลงนาม",
          "ตรวจทานและจัดหน้าเล่มรายงานข้อพิจารณาความคุ้มค่าโครงการ"
        ],
        meeting: [
          "ถอดความสรุปวาระการประชุมทบทวนมาตรการรับมืออุทกภัยดินสไลด์",
          "สกัดรายการ Action Items มอบหมายงานให้แก่กลุ่มงานสิ่งแวดล้อม",
          "จัดพิมพ์บันทึกการประชุมสรุปยอดประชากรกลุ่มเสี่ยงวัณโรคเชิงรุก"
        ],
        datagov: [
          "ทำความสะอาดข้อมูล (Data Anonymization) เพื่อการแลกเปลี่ยนสถิติสุขภาพ",
          "วิเคราะห์ความปลอดภัยในการรับส่งข้อมูลผ่านเครือข่ายจำลอง FHIR Gateway",
          "ให้การรับรองความถูกต้องมาตรฐานฟิลด์ข้อมูลเวชระเบียน EHR"
        ],
        cfo: [
          "ตรวจสอบอัตราความเร็วการเบิกจ่ายงบประมาณสะสม (Budget Burn Rate)",
          "ประเมินกระแสเงินสดสำรองและวิเคราะห์วินัยการคลังของโรงพยาบาล",
          "คำนวณความคุ้มค่าและความเป็นไปได้ทางการเงินในแผนจัดสรรงบพิเศษ"
        ],
        coo: [
          "จำลองสถิติเวลารอคอยเฉลี่ยแผนก OPD และเสนอเปิดใช้ Telemedicine",
          "สแกนสัดส่วนอัตราครองเตียงผู้ป่วย ICU และเตรียมเกณฑ์ Bed turnover",
          "ตรวจสอบระบบการนัดหมายและการคัดกรองจัดระดับความสำคัญคนไข้"
        ],
        provincial: [
          "รวบรวมแผนบริหารและพัสดุภัยพิบัติต่างๆ เพื่อจัดทำ Governor Brief",
          "คำนวณสถิติตำแหน่งจุดความร้อนฝุ่นละออง PM2.5 จากระบบข้อมูล GIS",
          "เฝ้าระวังประสิทธิภาพReferral System และประสานเครือข่ายสภากาชาด"
        ],
        db_monitor: [
          "สแกน Latency ของระบบฐานข้อมูลประมวลผล SQLite Data Layer",
          "ทำความสะอาดล็อกธุรกรรมเก่าเพื่อเพิ่มประสิทธิภาพการประมวลผล",
          "ตรวจสอบ Uptime เซิร์ฟเวอร์จำลอง และทดสอบประสิทธิภาพการเขียนข้อมูล"
        ],
        rag_optimizer: [
          "ประมวลผลจัดกลุ่ม Vector Embeddings 3072 มิติ เพื่อความเร็วสืบค้น",
          "จัดทำดัชนีคีย์เวิร์ดความรู้การควบคุมโรคติดต่อและวิบัติภัยธรรมชาติ",
          "จูนพารามิเตอร์ Re-ranking เพื่อลดระยะเวลาส่งออกข้อมูล RAG"
        ],
        security_officer: [
          "ตรวจจับช่องโหว่พอร์ตเครือข่ายและสแกนกิจกรรมบุกรุกจำลอง",
          "ตรวจสอบสถานะการทำงานของไฟร์วอลล์และเกตเวย์ความมั่นคงทางไอที",
          "ประเมินความปลอดภัยของเซสชันที่เชื่อมต่อไปยังระบบสารสนเทศภายนอก"
        ]
      };

      const possibleTasks = activities[randomRole] || ["กำลังดำเนินการตรวจสอบภารกิจตามมาตรฐาน"];
      const selectedTaskText = possibleTasks[Math.floor(Math.random() * possibleTasks.length)];

      // บันทึกกิจกรรมลงใน Monitor Logs
      setMonitorLogs(prev => [
        {
          timestamp: new Date().toLocaleTimeString(),
          sender: randomRole,
          text: selectedTaskText
        },
        ...prev.slice(0, 49) // เก็บ 50 รายการล่าสุด
      ]);

      // สุ่มจำลองบทสนทนาระหว่างคู่ตำแหน่งงาน (AI Small Talk)
      const talkPairs = [
        { from: 'cfo', to: 'coo', text: 'ข้อมูลอัตราการครองเตียง ICU พุ่งขึ้นถึง 91% จำเป็นต้องพิจารณาแผนครองเตียงเสริมหรือไม่ครับ?' },
        { from: 'coo', to: 'report', text: 'ฝากร่างหนังสือด่วนที่สุดขออนุมัติขยายเวลาระบบ Telemedicine เพื่อบรรเทาคิวคนไข้ OPD ครับ' },
        { from: 'rag_optimizer', to: 'datagov', text: 'ดำเนินการจัดดัชนี Vector SOP (3072 มิติ) เรียบร้อยแล้ว ขอความเห็นชอบความปลอดภัยข้อมูลด้าน PDPA ด้วยครับ' },
        { from: 'datagov', to: 'security_officer', text: 'สอบทานบันทึกการเรียกใช้ FHIR Gateway แล้ว ไม่พบสิ่งผิดปกติ ปลอดภัย PDPA 100%' },
        { from: 'provincial', to: 'cos', text: 'สรุป Governor Brief เรื่องแผนรับมือดินสไลด์และกำลังพล MCATT ประจำอำเภอดอยสูง เสนอ PHO แล้วครับ' },
        { from: 'analyst', to: 'knowledge', text: 'รบกวนช่วยดึงคู่มือระเบียบ SOP เรื่องการจ่ายเวชภัณฑ์ภัยพิบัติฉุกเฉินมาแนบประกอบเล่มโครงการด้วยครับ' }
      ];

      if (Math.random() > 0.4) {
        const pair = talkPairs[Math.floor(Math.random() * talkPairs.length)];
        setSmallTalkLogs(prev => [
          { sender: pair.from, text: `ส่งข้อความคุยกับ @${pair.to.toUpperCase()}: "${pair.text}"`, time: new Date().toLocaleTimeString() },
          ...prev.slice(0, 19)
        ]);
      }

      // อัปเดต Telemetry ของตำแหน่งนั้นๆ (จำลองการกินไฟ / ข้อมูล)
      setActiveTelemetry(prev => {
        const current = prev[randomRole] || { cpu: 2, mem: 60, load: 0 };
        return {
          ...prev,
          [randomRole]: {
            cpu: Math.floor(Math.random() * 45 + 30), // ทำงานใช้ CPU สูงขึ้น
            mem: Math.min(99, Math.floor(current.mem + (Math.random() * 6 - 3))),
            load: current.load + 1
          }
        };
      });

      // ค่อยๆ ลดสถานะ CPU ลงเมื่อเสร็จสิ้น
      setTimeout(() => {
        setActiveTelemetry(prev => {
          const updated = { ...prev };
          if (updated[randomRole]) {
            updated[randomRole] = {
              ...updated[randomRole],
              cpu: Math.floor(Math.random() * 8 + 2) // ลดกลับสู่ปกติ
            };
          }
          return updated;
        });
      }, 3000);

    }, 6000);

    return () => clearInterval(interval);
  }, [emergencyActive, monitorLogs]);

  // Role Metadata DB (Simulated Office Context)
  const roleDb: Record<string, any> = {
    executive: {
      name: "Executive (Digital CEO)",
      title: "ผู้ช่วยบริหารและติดตามความเสี่ยงเชิงยุทธศาสตร์",
      department: "สำนักงานผู้อำนวยการ (Executive Office)",
      kpis: [
        { label: "ความสำเร็จแผนยุทธศาสตร์องค์กร (Strategy Progress)", value: 87, target: 90, unit: "%" },
        { label: "ระดับการบรรลุตัวชี้วัด KPIs ภาพรวม (Overall KPIs)", value: 92, target: 95, unit: "%" },
        { label: "ดัชนีความเสี่ยงการบริการสาธารณสุข (Health Risk Index)", value: 1.8, target: 2.0, unit: "%" }
      ],
      tasks: [
        { id: "exec-1", type: "วิเคราะห์เชิงกลยุทธ์", urgency: "high", title: "จัดเตรียม Daily Brief สรุปความพร้อมระบบสาธารณสุขวันนี้", description: "รายงานสรุปเตียงผู้ป่วยหนักและแนวโน้มค่าฝุ่นละอองที่เริ่มพุ่งสูงขึ้นเพื่อเสนอแนวทางลดความหนาแน่นผู้ป่วย" },
        { id: "exec-2", type: "วิเคราะห์ KPIs", urgency: "medium", title: "ประเมินตัวชี้วัดความคุ้มค่าโครงการจัดตั้ง Clean Rooms ใน รพ.สต.", description: "ความสำเร็จของโครงการเปรียบเทียบกับงบประมาณสนับสนุนที่ใช้ไปเพื่อลดอัตราป่วยโรคทางเดินหายใจ" }
      ],
      plans: [
        "จัดทำ Executive Dashboard รายสัปดาห์เสนอผู้บริหารระดับจังหวัด",
        "ทบทวนแผนกลยุทธ์เพื่อปรับปรุงการเข้าถึงบริการระดับตำบล"
      ],
      obstacles: [
        "ข้อมูลสถานการณ์เตียงในเครือข่ายยังมีจุดหน่วงเวลาในการรายงาน 12 ชั่วโมง",
        "งบดำเนินงานสำรองฉุกเฉินมีจำกัดเนื่องจากสิ้นไตรมาส"
      ]
    },
    cos: {
      name: "Chief of Staff (ผู้จัดการสำนักงาน)",
      title: "ผู้ประสานการทำงานและแจกจ่ายงานเอเจนต์",
      department: "สำนักงานประสานการบริหาร (Chief of Staff Office)",
      kpis: [
        { label: "อัตราความเร็วการแตกงานเป็น Tasks (Task Breakdown Speed)", value: 98, target: 95, unit: "%" },
        { label: "ความสำเร็จโครงการระดับสำนักงาน (Project Success Rate)", value: 85, target: 90, unit: "%" }
      ],
      tasks: [
        { id: "cos-1", type: "แตกย่อยแผนงาน", urgency: "high", title: "แปลงข้อสั่งการลดความเสี่ยงวัณโรคในเรือนจำเป็น Tasks ย่อย", description: "แบ่งงานให้ทีมควบคุมโรคสกัด SOP และให้ทีมพัสดุเตรียมเสนอจัดหารถเอกซเรย์ดิจิทัล" },
        { id: "cos-2", type: "จัดลำดับงาน", urgency: "medium", title: "ประสานงาน ฝ่ายวิเคราะห์ยุทธศาสตร์ ดึงแผน MOPH KPI ล่าสุด", description: "จัดระเบียบงานยุทธศาสตร์เข้าสู่วารสารเฝ้าติดตามประจำรอบครึ่งปี" }
      ],
      plans: [
        "สร้าง Logic Model ของแต่ละโครงการสาธารณสุขและระบุตัวเอเจนต์ผู้รับผิดชอบ",
        "ติดตามและประเมินผลสัมฤทธิ์ของชิ้นงานที่เอเจนต์ผู้รับมอบหมายทำสำเร็จ"
      ],
      obstacles: [
        "การส่งมอบชิ้นงานของเอเจนต์ล่าช้ากว่าเป้าเมื่อ Weekly Quota ต่ำ",
        "การทับซ้อนกันของประเด็นงานข้ามกลุ่มงาน"
      ]
    },
    analyst: {
      name: "Analyst (ฝ่ายวิเคราะห์ยุทธศาสตร์)",
      title: "ผู้วิเคราะห์นโยบาย ยุทธศาสตร์ และ MOPH KPIs",
      department: "กลุ่มงานยุทธศาสตร์และแผนงาน (Strategy & Analysis)",
      kpis: [
        { label: "ความถูกต้องแผนยุทธศาสตร์ (Strategic Accuracy)", value: 95, target: 98, unit: "%" },
        { label: "ความสอดคล้องนโยบาย สธ. (MOPH Alignment)", value: 100, target: 100, unit: "%" }
      ],
      tasks: [
        { id: "analyst-1", type: "วิเคราะห์นโยบาย", urgency: "high", title: "วิเคราะห์ความสอดคล้องข้อเสนอโครงการกับนโยบายสุขภาพดิจิทัล สธ.", description: "ตรวจเช็คว่าแผนงานจัดหา FHIR Gateway สอดรับกับแนวทางยกระดับระบบไอทีหลักประกันสุขภาพถ้วนหน้าหรือไม่" },
        { id: "analyst-2", type: "ทบทวนแผน OKR", urgency: "medium", title: "สรุปเป้าหมาย OKR ด้านคลินิกโรคเรื้อรังสงบ (NCD Remission)", description: "วางแผนสัดส่วนผู้ป่วยหยุดยาเบาหวานเปรียบเทียบกับเกณฑ์ MOPH KPI ล่าสุด" }
      ],
      plans: [
        "ทบทวนรายงานความคุ้มค่าโครงการตามกรอบ PMQA หมวด 4",
        "ศึกษาผลกระทบเชิงนโยบายของการกระจายอำนาจสู่ท้องถิ่นด้านสาธารณสุข"
      ],
      obstacles: [
        "ตัวชี้วัดกระทรวงสาธารณสุขมีการอัปเดตและเปลี่ยนแปลงเป็นระยะทุกรอบไตรมาส",
        "การขาดแคลนข้อมูลประเมินความพึงพอใจในระบบปฐมภูมิ"
      ]
    },
    knowledge: {
      name: "Knowledge (ผู้ช่วยคลังปัญญา)",
      title: "ผู้สืบค้น SOP และระเบียบปฏิบัติราชการสาธารณสุข",
      department: "ศูนย์จัดการความรู้และปัญญาองค์กร (Knowledge Hub)",
      kpis: [
        { label: "สถิติการสืบค้นความรู้สำเร็จ (Knowledge Retrieval)", value: 98, target: 95, unit: "%" },
        { label: "ความครอบคลุม SOP ในระบบ (SOP Coverage)", value: 89, target: 90, unit: "%" }
      ],
      tasks: [
        { id: "knowledge-1", type: "สืบค้นข้อมูล SOP", urgency: "high", title: "ค้นหาแนวทางปฏิบัติ (SOP) ในการกู้ภัยและจัดหาเวชภัณฑ์เมื่อเกิดน้ำท่วม", description: "ต้องการดึงกฎเกณฑ์แนวทางการตอบสนองเหตุวิบัติฉุกเฉินและบทบาท MCATT ทันที" },
        { id: "knowledge-2", type: "ระเบียบจัดซื้อจัดจ้าง", urgency: "medium", title: "ตรวจระเบียบพัสดุกรมบัญชีกลางเรื่องการจัดซื้อจัดจ้างแบบเร่งด่วนพิเศษ", description: "สืบค้นเงื่อนไขการอนุมัติวงเงินจัดหาเครื่องกรองอากาศและหน้ากาก N95 ในสภาวะวิกฤตฝุ่น" }
      ],
      plans: [
        "นำเข้าคู่มือควบคุมโรคและ SOP สาธารณสุขฉุกเฉินเพิ่มเติมเข้าคลังความรู้ RAG",
        "จัดกลุ่มดัชนีความรู้ (Indexing) เพื่ออำนวยความสะดวกในการค้นคืนข้อมูลด่วน"
      ],
      obstacles: [
        "ไฟล์ PDF ระเบียบกระทรวงเดิมเป็นภาพสแกนที่ไม่มีการทำ OCR ทำให้ดึงความรู้ขัดข้อง",
        "เอกสาร SOP โครงสร้างงานเดิมบางแผนกไม่มีการบันทึกเป็นลายลักษณ์อักษร"
      ]
    },
    report: {
      name: "Report (ผู้ร่างเล่มรายงาน)",
      title: "ผู้เขียนเอกสาร รายงานวิชาการ และร่างจดหมายราชการตราครุฑ",
      department: "กลุ่มงานธุรการและสารบรรณ (Administrative Report Office)",
      kpis: [
        { label: "ความถูกต้องตามระเบียบสารบรรณ (Drafting Quality)", value: 97, target: 98, unit: "%" },
        { label: "อัตราความเร็วการเขียนรายงาน (Report Generation Rate)", value: 94, target: 90, unit: "%" }
      ],
      tasks: [
        { id: "report-1", type: "ร่างจดหมายราชการ", urgency: "high", title: "ร่างบันทึกข้อความสั่งการจัดสรรพัสดุและงบประมาณเพื่อเฝ้าระวังฝุ่น PM2.5", description: "จัดทำร่างตราครุฑเสนอ PHO อนุมัติจัดหาหน้ากาก N95 และห้องลดฝุ่นในอำเภอขอบชายแดน" },
        { id: "report-2", type: "จัดเตรียมรายงาน", urgency: "medium", title: "จัดโครงร่างสรุปรายงานสถานการณ์ผู้ป่วยวัณโรครายสัปดาห์", description: "รวบรวมประเด็นสแกนวัณโรคทัณฑสถานและสถิติยอดผู้ป่วยเข้าสู่ระบบส่งตรวจเสมหะ" }
      ],
      plans: [
        "พัฒนารูปแบบเทมเพลตจดหมายราชการให้รองรับหนังสือภายนอกและคำสั่งจังหวัดอย่างสมบูรณ์",
        "ปรับปรุงการแปลและตรวจคำผิดภาษาไทยเพื่อรักษามาตรฐานธุรการขั้นสูง"
      ],
      obstacles: [
        "โครงเนื้อหาเดิมที่ผู้ใช้พิมพ์มีรายละเอียดสั้นเกินไป ทำให้ AI ต้องใช้น้ำหนักจินตนาการเพิ่ม",
        "สำนวนระดับนโยบายบางประเภทต้องสอดแทรกระเบียบกฎหมายประกอบซึ่งรายงานต้องดึงข้อมูลเสริม"
      ]
    },
    meeting: {
      name: "Meeting (ผู้ถอดสรุปประชุม)",
      title: "ผู้ถอดความสรุปวาระประชุมและ Action Items",
      department: "หน่วยจัดการบันทึกและจดหมายการประชุม (Meeting Memory Dept)",
      kpis: [
        { label: "ความถูกต้องถอดความเสียง (Transcription Accuracy)", value: 92, target: 95, unit: "%" },
        { label: "ความรวดเร็วการสกัด Action Items (Action Items Extraction)", value: 98, target: 95, unit: "%" }
      ],
      tasks: [
        { id: "meeting-1", type: "ถอดสรุปบันทึก", urgency: "high", title: "สรุปการประชุมคณะกรรมการประเมินภัยน้ำท่วมและทีมกู้ชีพสาธารณสุข", description: "ถอดเสียงวาระจัดเตรียมยาสามัญและทีม MCATT สู่จุดพักพิงเพื่อรายงานต่อที่ประชุมใหญ่" },
        { id: "meeting-2", type: "สกัด Action Items", urgency: "medium", title: "จัดเก็บงานติดตามการกินยา DOTS จากประเด็นคัดกรองวัณโรค", description: "สกัดข้อมูลหน้าที่และเป้าหมายมอบหมายให้กลุ่มงานควบคุมโรคติดตามผลลัพธ์การกินยา" }
      ],
      plans: [
        "ขยายความสามารถ RAG เฉพาะห้องประชุม (NotebookLM-style RAG) เพื่อให้แชทอ้างอิงเอกสารแนบได้ 100%",
        "อัปเกรดโมเดลสัญจรเสียง Whisper ให้ตอบรับสำเนียงท้องถิ่นระดับอำเภอ"
      ],
      obstacles: [
        "เสียงสะท้อนและสัญญาณแทรกภายในห้องประชุมทำให้การถอดความช่วงคำศัพท์การแพทย์เพี้ยน",
        "ระยะเวลาประชุมที่ยาวนานกว่า 3 ชั่วโมงทำให้ใช้เวลาประมวลผล RAG สูงขึ้น"
      ]
    },
    datagov: {
      name: "Data Governance (ธรรมภิบาลข้อมูล)",
      title: "ผู้คุ้มครองมาตรฐานข้อมูล ความปลอดภัย และกฎหมาย PDPA",
      department: "หน่วยควบคุมความมั่นคงข้อมูลสารสนเทศ (Data Governance & Cyber Security)",
      kpis: [
        { label: "ดัชนีผ่านการตรวจทาน PDPA (PDPA Audit Score)", value: 100, target: 100, unit: "%" },
        { label: "ความถูกต้องของชุดข้อมูลหลัก (Data Quality Index)", value: 96, target: 95, unit: "%" }
      ],
      tasks: [
        { id: "datagov-1", type: "ความมั่นคงปลอดภัย", urgency: "high", title: "ตรวจสอบมาตรฐานความปลอดภัย FHIR Gateway และการเข้าถึง EHR", description: "วิเคราะห์พฤติกรรมการเรียกใช้ API ข้ามเครือข่าย ป้องกันข้อมูลรั่วไหลและจำกัดสิทธิ์แอดมิน" },
        { id: "datagov-2", type: "ตรวจทานมาตรฐานข้อมูล", urgency: "medium", title: "จัดแนวทางจัดกลุ่ม Master Data สถิติโรคระบาดข้ามพรมแดน", description: "กำกับพอร์ตแลกเปลี่ยนสถิติโรคติดต่อไม่ให้ระบุข้อมูลที่เชื่อมโยงถึงตัวตนบุคคลจริง" }
      ],
      plans: [
        "จัดซ้อมแผนกู้ระบบข้อมูลสาธารณสุขฉุกเฉินและซ้อมป้องกันแรนซัมแวร์ในโรงพยาบาล",
        "พัฒนาเครื่องมือลบข้อมูลระบุตัวตน (Anonymization Tool) อัตโนมัติในฐานข้อมูลเดโม"
      ],
      obstacles: [
        "การส่งข้อมูลสุขภาพระดับตำบลบางแห่งยังใช้วิธีแนบไฟล์ตารางซึ่งขัดต่อนโยบายความปลอดภัย",
        "บุคลากรหน้างานยังส่งรหัสผ่านแชร์กันในกลุ่มงานจัดบริการคิว"
      ]
    },
    cfo: {
      name: "CFO (ฝ่ายการคลัง)",
      title: "ผู้บริหารแผนการเงิน งบประมาณ และความคุ้มค่าโครงการ",
      department: "กลุ่มงานการเงินและงบประมาณ (Finance & Budget Division)",
      kpis: [
        { label: "อัตราการเบิกจ่ายงบประมาณสะสม (Budget Burn Rate)", value: 84, target: 100, unit: "%" },
        { label: "ดัชนีประเมินวินัยการคลัง (Fiscal Health Index)", value: 4.8, target: 5.0, unit: "คะแนน" }
      ],
      tasks: [
        { id: "cfo-1", type: "พิจารณางบประมาณ", urgency: "high", title: "ขออนุมัติเบิกจ่ายงบพิเศษโครงการจัดซื้อหน้ากาก N95 บรรเทาภัยหมอกควัน", description: "วงเงินจัดพัสดุด่วน 1.2 ล้านบาท เพื่อกระจายสู่ประชากรเสี่ยง ตรวจทานความคุ้มค่าก่อนชง PHO" },
        { id: "cfo-2", type: "วิเคราะห์งบลงทุน", urgency: "medium", title: "ประเมินค่าซ่อมบำรุงเซิร์ฟเวอร์ไอทีและระบบคลาวด์ประจำปีงบประมาณ", description: "เปรียบเทียบสัดส่วนงบแผ่นดินกับงบกองทุนประกันสุขภาพเพื่อวางกรอบงบประมาณไตรมาสถัดไป" }
      ],
      plans: [
        "ควบคุมงบประมาณค่าใช้สอย Token และการหักจ่ายเครดิตของเอเจนต์ในโลกทวิน",
        "จัดทำแผนรายงานพยากรณ์กระแสเงินสดและหนี้ค้างชำระของโรงพยาบาลในสังกัด"
      ],
      obstacles: [
        "ระเบียบการเบิกเงินช่วยเหลือภัยพิบัติบางส่วนมีความเข้มงวดและล่าช้าจากหน่วยงานพัสดุส่วนกลาง",
        "โรงพยาบาลชุมชนบางแห่งส่งยอดรายงานการเงินล่าช้าเนื่องจากขาดบุคลากรการบัญชี"
      ]
    },
    coo: {
      name: "COO (ฝ่ายปฏิบัติการบริการ)",
      title: "ผู้บริหารการดำเนินงาน จัดระบบคิวเตียง และประสิทธิภาพโรงพยาบาล",
      department: "กลุ่มงานอำนวยการและปฏิบัติการแพทย์ (Hospital Operations)",
      kpis: [
        { label: "ประสิทธิภาพจัดการเตียงคนไข้ (Bed Utilization)", value: 91, target: 90, unit: "%" },
        { label: "ระยะเวลารอคอยเฉลี่ย OPD (Average OPD Waiting Time)", value: 34, target: 30, unit: "นาที" }
      ],
      tasks: [
        { id: "coo-1", type: "บริหารคิวบริการ", urgency: "high", title: "ทบทวนแผนจัดการเวชระเบียนและระบบคิวผู้ป่วยนอกกรณีคลินิกหนาแน่น", description: "แก้ปัญหาคิวล้นในคลินิก NCD ช่วงเช้าวันอังคารและพิจารณาขยายสู่ระบบเทเลเมดิซีน" },
        { id: "coo-2", type: "จัดการเตียงรักษา", urgency: "medium", title: "ประเมินความเร็วการ Bed turnover ในหอผู้ป่วยวิกฤตและโรคปอด", description: "วิเคราะห์อัตราการครองเตียงของผู้รับวัณโรคและโรคฝุ่น PM2.5 ที่เข้าพักรักษาตัวยาวนาน" }
      ],
      plans: [
        "วางระบบ Standard Gateway เพื่อซิงก์ข้อมูลคิวเตียงว่างระดับโรงพยาบาลในเครือข่าย",
        "จัดอบรมแผนก Triage ในการคัดกรองความเร่งด่วนของระดับผู้ป่วยอุบัติเหตุฉุกเฉิน"
      ],
      obstacles: [
        "การส่งต่อผู้ป่วยจากปฐมภูมิมาทุติยภูมิมีความหนาแน่นในช่วงต้นสัปดาห์สูงกว่าปกติ",
        "เตียงหอผู้ป่วยหนัก (ICU) มีการจองคิวล่วงหน้ายาวนานและค่อนข้างขาดแคลน"
      ]
    },
    provincial: {
      name: "Provincial Brain (มันสมองจังหวัด)",
      title: "ผู้บริหารเครือข่ายส่งต่อระดับจังหวัด และจัดสรุปเสนอผู้ว่าฯ",
      department: "ศูนย์ข้อมูลและประสานงานสาธารณสุขจังหวัด (Provincial Health Intelligence)",
      kpis: [
        { label: "อัตราส่งต่อผู้ป่วยสำเร็จ (Referral System Success)", value: 99, target: 100, unit: "%" },
        { label: "ความพร้อมตอบสนองแผนเผชิญเหตุ (Crisis Response Uptime)", value: 100, target: 100, unit: "%" }
      ],
      tasks: [
        { id: "provincial-1", type: "สรุปผู้บริหารจังหวัด", urgency: "high", title: "จัดทำ Governor Briefing สรุปแผนรับมืออุทกภัยดินสไลด์และดินถล่มเชียงราย", description: "รวบรวมแผนการโยกย้ายเตียง รพ.สต. และกำลังพลทีมแพทย์เคลื่อนที่ MCATT เสนอลงนามสั่งการผู้ว่าราชการจังหวัด" },
        { id: "provincial-2", type: "ปรับสมดุลพัสดุ", urgency: "medium", title: "ประสานงานโอนย้ายเครื่องกรองอากาศและหน้ากากจากคลังกลางสู่ตำบลดอยสูง", description: "คำนวณสถิติและวิเคราะห์พื้นที่ความเสี่ยงของจุดความร้อนเพื่อกระจายหน้ากาก N95 ได้ครอบคลุมเป้าหมาย" }
      ],
      plans: [
        "พัฒนา Knowledge Graph ความสัมพันธ์ระบบสารสนเทศสุขภาพทั้งจังหวัด",
        "จัดสรรโควตางบและกําลังคนแพทย์สนามให้เหมาะสมตามระดับวิกฤตภัยพิบัติสิ่งแวดล้อม"
      ],
      obstacles: [
        "ข้อมูลเครือข่ายส่งต่อของสถานพยาบาลระดับอำเภอบางแห่งไม่มีการอัปเดตช่องทางติดต่อสำรอง",
        "การบูรณาการงบภัยพิบัติข้ามกระทรวง (สธ. ร่วมกับ มหาดไทย) ขาดจุดเชื่อมโยงข้อมูลกลาง"
      ]
    },
    db_monitor: {
      name: "วิเคราะห์การเก็บล็อก (Log Intelligence)",
      title: "ระบบตรวจสอบความเสถียรของฐานข้อมูลและทราฟฟิกสารสนเทศ",
      department: "กลุ่มงานสถาปัตยกรรมข้อมูล (Data Infrastructure Division)",
      kpis: [
        { label: "ความเสถียรของฐานข้อมูล (Database Uptime)", value: 99.98, target: 99.9, unit: "%" },
        { label: "ความเร็วการประมวลผล Query (Average Query Time)", value: 45, target: 80, unit: "ms" }
      ],
      tasks: [
        { id: "db-1", type: "ตรวจสอบระบบ", urgency: "high", title: "วิเคราะห์ทราฟฟิกข้อมูลบริการ OPD/ICU ในระดับ SQLite Data Layer", description: "ตรวจเช็คการเขียน/อ่านฐานข้อมูลจำลองว่าทำงานขัดข้องหรือไม่ในช่วงเวลาที่มีการเรียกใช้ข้อมูลสูง" }
      ],
      plans: [
        "ย้ายข้อมูลประวัติเก่าเข้าสู่ออฟไลน์ Archive เพื่อเพิ่มความเร็วของระบบ",
        "ทำระบบสำรองข้อมูลอัตโนมัติรายชั่วโมงในสภาวะจำลองภัยพิบัติ"
      ],
      obstacles: [
        "มีจำนวน Log สะสมปริมาณมากจากการรัน Simulation ต่อเนื่อง",
        "การเชื่อมต่อเครือข่ายจำลองกับภายนอกบางจุดมี Latency สูงกว่าปกติ"
      ]
    },
    rag_optimizer: {
      name: "ผู้ช่วย RAG Optimizer (3072D Vector)",
      title: "ระบบจัดดัชนีและเพิ่มความเร็วในการสืบค้นคลังความรู้องค์กร",
      department: "กลุ่มงานเทคโนโลยีสารสนเทศและการสื่อสาร (IT & RAG Services)",
      kpis: [
        { label: "ความแม่นยำในการจับคู่เนื้อหา (Retrieval Precision)", value: 97.5, target: 95, unit: "%" },
        { label: "มิติตัวชี้วัดเวกเตอร์ (Vector Dimension)", value: 3072, target: 3072, unit: "มิติ" }
      ],
      tasks: [
        { id: "rag-1", type: "อัปเกรดโมเดล", urgency: "high", title: "ปรับแต่งดัชนีคลังความรู้สำหรับการจำลอง SOP ด้านระบาดวิทยา", description: "วิเคราะห์ประสิทธิภาพการทำ Chunking และ Overlap เพื่อป้องกันการดึงเนื้อหากฎหมายปนกัน" }
      ],
      plans: [
        "เพิ่มการจัดทำ Re-ranking (Cross-encoder) ในการค้นหาระเบียบสั่งการ",
        "จัดเก็บความรู้การประเมินสถานการณ์น้ำท่วมปีล่าสุดเป็น Vector DB ชุดใหม่"
      ],
      obstacles: [
        "ข้อมูลระเบียบกระทรวงบางเล่มมีโครงสร้างตารางที่ประมวลผลและแปลงเป็น Vector ได้ยาก",
        "ปริมาณหน่วยความจำสะสมของโมเดลฝังตัวอักษรสูงขึ้นตามจำนวนเอกสาร"
      ]
    },
    security_officer: {
      name: "ผู้คุมความปลอดภัย (Cyber Security)",
      title: "ระบบป้องกันภัยคุกคามสารสนเทศและเฝ้าระวังความมั่นคงปลอดภัย",
      department: "หน่วยควบคุมความมั่นคงข้อมูลสารสนเทศ (Data Governance & Cyber Security)",
      kpis: [
        { label: "การตอบรับภัยคุกคาม Cyber-Attack (Intrusion Detection)", value: 100, target: 100, unit: "%" },
        { label: "อัตราความเสี่ยงระบบสารสนเทศ (Risk Mitigation)", value: 0.05, target: 0.1, unit: "%" }
      ],
      tasks: [
        { id: "sec-1", type: "เฝ้าระวังความปลอดภัย", urgency: "high", title: "ตรวจสอบความปลอดภัยการรับส่งข้อมูลตามมาตรฐาน PDPA", description: "ตรวจจับและป้องกันการสแกนหาช่องโหว่พอร์ตภายนอกและการเรียกใช้ข้อมูลเวชระเบียนที่ผิดปกติ" }
      ],
      plans: [
        "เปิดใช้ระบบ Multi-factor Authentication จำลองสำหรับผู้ใช้งานระบบบริหารจัดการ",
        "จัดทำแผนรายงานการละเมิดความมั่นคงสารสนเทศรายงานต่อ PHO"
      ],
      obstacles: [
        "ผู้ใช้งานบางส่วนยังใช้รหัสผ่านแบบคาดเดาง่าย (Weak Passwords)",
        "ความปลอดภัยของ API Gateway ขาเข้าจากระบบภายนอกจำเป็นต้องอัปเดต Certificate"
      ]
    }
  };

  // Get current active agent metadata or generate dynamic fallback for installed marketplace agents
  const currentRoleData = roleDb[selectedAgentRole] || {
    name: `${selectedAgentRole.toUpperCase()} (ผู้ช่วยวิเคราะห์เฉพาะทาง)`,
    title: `ผู้ดูแลระบบเฉพาะทางจาก Marketplace`,
    department: `หน่วยงานดิจิทัลจำลอง (Virtual Digital Suite)`,
    kpis: [
      { label: "สถิติวิเคราะห์งานเสร็จสิ้น (Task Completion Score)", value: 95, target: 90, unit: "%" },
      { label: "ความถูกต้องประมวลผล SOP (SOP Accuracy)", value: 98, target: 95, unit: "%" }
    ],
    tasks: [
      { id: `${selectedAgentRole}-task-1`, type: "คำสั่งปฏิบัติการ", urgency: "high", title: `วิเคราะห์ประเด็นจำลองสำหรับระบบสนับสนุนของ ${selectedAgentRole}`, description: `จัดเตรียมข้อสั่งการและการประมวล SOP ตามขอบเขตความเชี่ยวชาญเพื่อเสนอรายงาน` }
    ],
    plans: [
      `ให้การสนับสนุนการทำ RAG ค้นหาข้อมูลเชิงลึกเฉพาะตำแหน่ง`,
      `เฝ้าระวังตัวชี้วัดความสำเร็จของกลุ่มโครงการเสริม`
    ],
    obstacles: [
      `ข้อมูลประวัติการทำงานในฐานข้อมูลองค์กรยังมีจำนวนจำกัด`,
      `โควตาเครดิตการประมวลผล Token รายสัปดาห์`
    ]
  };

  // Select a task from the inbox and populate forms
  const handleSelectTask = (task: TaskItem) => {
    setLetterSubject(`ข้อสั่งการด่วนเรื่อง: ${task.title}`);
    setLetterDetail(`แนวทางการปฏิบัติงานสั่งการ: \nสืบเนื่องจาก ${task.description} \n\nสั่งการให้ส่วนงานที่เกี่ยวข้องดำเนินมาตรการเร่งด่วน รายงานผลกลับมายังฝ่ายบริหารภายใน 7 วัน`);
    setActiveWorkspaceTab('draft');
    
    // Populate consult input
    setChatInput(`ในฐานะ ${currentRoleData.name} ขอความเห็นและข้อมูลอ้างอิงของระเบียบเพื่อรับมือหรือแก้ไขปัญหา: "${task.title}" รายละเอียดคือ "${task.description}"`);
    alert(`ดึงงาน "${task.title}" เข้าเครื่องมือทำงานของ ${currentRoleData.name} แล้ว!`);
  };

  // 📄 Draft Official Letter Handler
  const handleDraftSimulate = async () => {
    setLoading(true);
    setDraftResult(null);
    try {
      const prompt = `ประเภทหนังสือราชการ: ${letterType}\nเรื่อง: ${letterSubject}\nรายละเอียดและข้อสั่งการหลัก: ${letterDetail}\nระดับความลับ: ${confidentiality}\nผู้ลงนาม/ตำแหน่ง: ${currentRoleData.title}`;
      const data = await api.draftTwinLetter(prompt);
      setDraftResult(data);
    } catch (e) {
      setDraftResult({ error: "การจำลองร่างจดหมายราชการขัดข้อง" });
    } finally {
      setLoading(false);
    }
  };

  // 💬 Chat with selected agent handler
  const handleConsultTwin = async () => {
    if (!chatInput.trim()) return;
    const question = chatInput;
    setChatInput('');
    setChatLoading(true);

    const currentLogs = chatLogs[selectedAgentRole] || [];
    setChatLogs({
      ...chatLogs,
      [selectedAgentRole]: [...currentLogs, { role: 'user', text: question }]
    });

    try {
      const token = localStorage.getItem('hosprime_token');
      const headers: Record<string, string> = { 'Content-Type': 'application/json' };
      if (token) headers['Authorization'] = `Bearer ${token}`;

      const res = await fetch(`${((import.meta as any).env?.VITE_API_BASE_URL) || 'http://localhost:8000/api'}/twins/consult`, {
        method: 'POST',
        headers,
        body: JSON.stringify({ agent_id: selectedAgentRole, question })
      });
      
      if (!res.ok) throw new Error('เกิดข้อผิดพลาดในการหารือเอเจนต์ AI');
      const data = await res.json();

      setChatLogs(prev => ({
        ...prev,
        [selectedAgentRole]: [...(prev[selectedAgentRole] || []), { role: 'assistant', text: data.response }]
      }));
    } catch (e: any) {
      setChatLogs(prev => ({
        ...prev,
        [selectedAgentRole]: [...(prev[selectedAgentRole] || []), { role: 'assistant', text: `ขออภัยการโต้ตอบขัดข้อง: ${e.message}` }]
      }));
    } finally {
      setChatLoading(false);
    }
  };

  // 📊 Analyze KPIs with selected Agent
  const handleAnalyzeKPIs = async () => {
    setAnalyzingKpi(true);
    setKpiAnalysis(null);
    try {
      const kpisText = currentRoleData.kpis.map((k: any) => `- ${k.label}: ปัจจุบัน ${k.value}${k.unit} (เป้าหมาย ${k.target}${k.unit})`).join('\n');
      const question = `วิเคราะห์และรายงานปัญหา แผนการดำเนินงาน และให้ข้อเสนอแนะเชิงกลยุทธ์จากตัวชี้วัด KPIs ล่าสุดเหล่านี้ด้วยครับ:\n${kpisText}\n\nแนบประเด็นแผนงาน: ${currentRoleData.plans.join(', ')}\nอุปสรรค: ${currentRoleData.obstacles.join(', ')}`;
      
      const token = localStorage.getItem('hosprime_token');
      const headers: Record<string, string> = { 'Content-Type': 'application/json' };
      if (token) headers['Authorization'] = `Bearer ${token}`;

      const res = await fetch(`${((import.meta as any).env?.VITE_API_BASE_URL) || 'http://localhost:8000/api'}/twins/consult`, {
        method: 'POST',
        headers,
        body: JSON.stringify({ agent_id: selectedAgentRole, question })
      });
      if (!res.ok) throw new Error('AI วิเคราะห์ล้มเหลว');
      const data = await res.json();
      setKpiAnalysis(data.response);
    } catch (e: any) {
      setKpiAnalysis(`เกิดข้อผิดพลาดในการวิเคราะห์ตัวชี้วัด: ${e.message}`);
    } finally {
      setAnalyzingKpi(false);
    }
  };

  // 🛒 Handle Install Agent Pack
  const handleInstallPack = async (packId: string) => {
    setInstallingPack(packId);
    try {
      const res = await api.installAgentPack(packId);
      alert(`🎉 ติดตั้งแพ็กเกจ ${packId.toUpperCase()} สำเร็จ!\nได้ติดตั้งผู้ช่วยเอเจนต์เพิ่มจำนวน ${res.installed_count} ตัว เรียบร้อยแล้ว`);
      await fetchAgents(); // Reload active agents list
    } catch (e: any) {
      alert(`ขออภัยการติดตั้งขัดข้อง: ${e.message}`);
    } finally {
      setInstallingPack(null);
    }
  };

  useEffect(() => {
    // Automatically adjust defaults when changing selected agent
    if (selectedAgentRole === 'executive') {
      setLetterSubject('มาตรการคัดกรองวัณโรคเชิงรุกในกลุ่มเปราะบาง (เรือนจำและพื้นที่ดอนสูง)');
      setLetterDetail('มอบหมายให้กลุ่มงานควบคุมโรคประสานงานหน่วยงานที่เกี่ยวข้องและจัดชุดรถเอกซเรย์เคลื่อนที่พระราชทานลงพื้นที่สแกน 100% ภายใน 30 วัน');
    } else if (selectedAgentRole === 'cfo') {
      setLetterSubject('รายงานการเร่งรัดติดตามการเบิกจ่ายงบประมาณไตรมาสสุดท้าย');
      setLetterDetail('แจ้งหัวหน้ากลุ่มงานทุกฝ่ายตรวจสอบการเบิกจ่ายงบดำเนินการและงบลงทุน ให้ดำเนินการส่งเอกสารพัสดุและเบิกจ่ายให้ทันตามกรอบเวลาของกระทรวงการคลัง');
    } else if (selectedAgentRole === 'cos') {
      setLetterSubject('รายงานการติดตามการทำงานโครงการประสานอัตรากำลังปฐมภูมิ');
      setLetterDetail('ประสาน COO ตรวจสอบอัตราผู้รอคิวบริการ OPD และให้ผู้ชำนาญการดึง SOP การคัดกรองจำแนกระดับความเร่งด่วนตามระบบสากลมาแนบประกอบ');
    } else {
      setLetterSubject(`ร่างหนังสือราชการฝ่ายปฏิบัติการสำหรับ ${selectedAgentRole.toUpperCase()}`);
      setLetterDetail(`เนื้อหา: มอบหมายสั่งการและแนวทางปฏิบัติงานตามกรอบภารกิจความรับผิดชอบของฝ่าย ${selectedAgentRole}`);
    }
    setDraftResult(null);
    setKpiAnalysis(null);
  }, [selectedAgentRole]);

  const currentChatLogs = chatLogs[selectedAgentRole] || [];

  // Define Packs for Marketplace rendering
  const marketplacePacks = [
    {
      id: "ncd",
      name: "NCD Center Pack",
      badge: "Chronic Care",
      desc: "ระบบบริหารจัดการและป้องกันโรคไม่ติดต่อเรื้อรัง (เบาหวาน, ความดันโลหิตสูง, โรคไตเรื้อรัง, โรคอ้วน, ไขมันในเลือดสูง, NCD Remission, Lifestyle Medicine)",
      agentsCount: 7,
      isInstalled: agentsList.some(a => a.role === 'diabetes')
    },
    {
      id: "tb",
      name: "Communicable Disease Center Pack",
      badge: "Infectious Care",
      desc: "ระบบควบคุมและเฝ้าระวังโรคติดต่อสำคัญเชิงรุกข้ามพรมแดนและพื้นที่ทัณฑสถาน (วัณโรค, HIV, โรคติดต่อทางเพศ, ไข้เลือดออก, มาลาเรีย, ไข้หวัดใหญ่, โควิด)",
      agentsCount: 7,
      isInstalled: agentsList.some(a => a.role === 'tb_disease')
    },
    {
      id: "pheoc",
      name: "PHEOC & Disaster Pack",
      badge: "Emergency Care",
      desc: "ศูนย์สั่งการและรับมืออุทกภัย ดินถล่ม แผ่นดินไหว วิกฤตฝุ่นละออง PM2.5 และทีมประเมินฟื้นฟูสุขภาพจิต MCATT ใน 72 ชั่วโมง",
      agentsCount: 7,
      isInstalled: agentsList.some(a => a.role === 'pheoc_cmd')
    },
    {
      id: "finance",
      name: "Finance & Procurement Pack",
      badge: "Hospital Finance",
      desc: "ระบบวิเคราะห์การคลังโรงพยาบาล บริหารรายรับ-รายจ่าย คาดการณ์ดัชนีวินัยการคลัง ตรวจสอบสิทธิเบิกจ่าย และจัดซื้อพัสดุภาครัฐตามระเบียบ",
      agentsCount: 10,
      isInstalled: agentsList.some(a => a.role === 'revenue_mgr')
    },
    {
      id: "hr",
      name: "HR & Productivity Pack",
      badge: "Hospital HR",
      desc: "ระบบจัดหาอัตรากำลังพล ตรวจสอบสิทธิ์คุณวุฒิ การประเมินสมรรถนะ อบรมทักษะ และติดตามภาวะความล้าทางจิตใจ (Burnout) ของแพทย์และพยาบาล",
      agentsCount: 8,
      isInstalled: agentsList.some(a => a.role === 'recruitment')
    }
  ];

  return (
    <div className="max-w-7xl mx-auto space-y-6 text-white text-left animate-fade-in">
      
      {/* Top Header & Tab switcher */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h2 className="text-2xl font-bold tracking-tight font-outfit text-transparent bg-clip-text bg-gradient-to-r from-white via-slate-100 to-gold-400">
            🏢 ระบบสำนักงานจำลองเสมือนและเครื่องมือประมวลผลข้อมูล (Virtual Simulation Office & Digital Tools)
          </h2>
          <p className="text-slate-400 text-xs mt-1">
            ประสานงานกับทีมผู้ช่วย AI สั่งร่างเอกสารราชการ หารือระบบคู่มือ SOP หรือเลือกติดตั้งแพ็กเกจเอเจนต์เฉพาะทางจาก Marketplace
          </p>
        </div>

        {/* Workspace Toggle Buttons */}
        <div className="flex bg-slate-900/60 p-1.5 rounded-2xl border border-slate-800 glass shrink-0">
          <button
            onClick={() => setActiveTab('office')}
            className={`px-4 py-2 text-xs font-bold rounded-xl transition-all flex items-center gap-2 ${
              activeTab === 'office' ? 'bg-gradient-to-r from-gold-600 to-amber-700 text-slate-950 shadow-md' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            🏢 ห้องทำงานสั่งการ AI
          </button>
          <button
            onClick={() => setActiveTab('marketplace')}
            className={`px-4 py-2 text-xs font-bold rounded-xl transition-all flex items-center gap-2 ${
              activeTab === 'marketplace' ? 'bg-gradient-to-r from-gold-600 to-amber-700 text-slate-950 shadow-md' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            🛒 ตลาดผู้ช่วย AI (Marketplace)
          </button>
        </div>
      </div>

      {activeTab === 'marketplace' ? (
        /* Agent Marketplace UI Layout */
        <div className="space-y-6">
          <div className="p-6 bg-slate-955/40 border border-slate-850 rounded-3xl glass text-left space-y-2">
            <h3 className="text-lg font-bold text-gold-400">🛒 ตลาดเครื่องมือประมวลผลข้อมูลองค์กร (Digital Tools & Intelligence Marketplace)</h3>
            <p className="text-xs text-slate-400 font-light leading-relaxed">
              เลือกติดตั้งกลุ่มผู้ช่วยปัญญาประดิษฐ์เพื่อตอบโจทย์งานสาธารณสุขและระบาดวิทยาเฉพาะทาง เมื่อทำการเปิดใช้ระบบ เครื่องมือประมวลผลและ AI เบื้องหลังจะทำงานในโครงสร้างข้อมูลองค์กรอัตโนมัติ ทำให้สามารถจำลองและประมวลผลผ่านบอร์ดบริหารได้ทันที
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {marketplacePacks.map((pack) => (
              <div
                key={pack.id}
                className="p-5 bg-gradient-to-br from-slate-950/80 to-slate-900/60 border border-slate-850 hover:border-slate-700 rounded-3xl relative overflow-hidden flex flex-col justify-between transition-all duration-200 group shadow-lg"
              >
                <div className="absolute top-0 right-0 w-28 h-28 bg-gold-500/5 rounded-full blur-2xl group-hover:bg-gold-500/10 transition-all"></div>
                <div className="space-y-4 text-left">
                  <div className="flex justify-between items-center">
                    <span className="text-[9px] uppercase tracking-widest font-bold bg-slate-900 border border-slate-800 text-gold-500 px-2.5 py-0.5 rounded-full">
                      {pack.badge}
                    </span>
                    <span className="text-[10px] text-slate-500 font-medium">เครื่องมือ {pack.agentsCount} รายการ</span>
                  </div>
                  
                  <h4 className="text-base font-bold text-white mt-1 group-hover:text-gold-400 transition-colors">{pack.name}</h4>
                  <p className="text-xs text-slate-400 leading-relaxed font-light mt-1.5 min-h-[70px]">{pack.desc}</p>
                </div>

                <div className="pt-5 border-t border-slate-900 mt-5 flex justify-between items-center">
                  <span className="text-xs font-bold text-gold-400">สิทธิ์พัสดุ: ฟรี</span>
                  
                  {pack.isInstalled ? (
                    <span className="px-4 py-2 bg-emerald-950/40 border border-emerald-900 text-emerald-400 text-xs font-semibold rounded-xl flex items-center gap-1.5">
                      ✓ ติดตั้งเรียบร้อย
                    </span>
                  ) : (
                    <button
                      onClick={() => handleInstallPack(pack.id)}
                      disabled={installingPack !== null}
                      className="px-4.5 py-2 bg-slate-900 border border-slate-800 hover:bg-gold-600 hover:text-slate-950 disabled:opacity-40 text-xs font-bold rounded-xl transition-all duration-150 active:scale-[0.98]"
                    >
                      {installingPack === pack.id ? "กำลังติดตั้ง..." : "📥 ติดตั้งแพ็กเกจ"}
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      ) : (
        /* Office Workspace Split layout */
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
          
          {/* Left Sidebar: Active AI Assistants list */}
          <div className="lg:col-span-4 space-y-5">
            
            {/* Active Profile Info */}
            <div className="p-4 bg-gradient-to-br from-slate-955 to-slate-900 border border-slate-850 rounded-2xl text-left space-y-1 relative overflow-hidden shadow">
              <div className="flex items-center gap-2.5">
                <span className="text-lg">👤</span>
                <div>
                  <h3 className="text-xs font-bold text-white uppercase tracking-wider">บทบาทผู้สั่งการหลัก</h3>
                  <p className="text-[11px] text-gold-400">ผู้บริหารและผู้อำนวยการหน่วยงาน</p>
                </div>
              </div>
            </div>

            {/* 🏢 Simulation Office: จำลองสถานการณ์การทำงานระดับสำนักงานเสมือน */}
            <div className="p-4 bg-slate-950/40 border border-slate-850 rounded-2xl glass space-y-4">
              <div className="border-b border-slate-900 pb-2">
                <h4 className="text-xs font-bold text-gold-400 uppercase tracking-widest flex items-center gap-1.5">
                  🏢 Simulation Office (สำนักงานจำลองเสมือน)
                </h4>
                <p className="text-[10px] text-slate-400 font-light mt-0.5">สถานะความเคลื่อนไหวของเอเจนต์และการจัดการข้อมูลองค์กร</p>
              </div>

              {/* หมวดหมู่ 1: ฝ่ายปฏิบัติการและบริหาร (Administrative & Services AI) */}
              <div className="space-y-2.5">
                <span className="text-[10px] uppercase tracking-wider font-bold text-slate-300 block border-l-2 border-gold-500 pl-2">
                  💼 ฝ่ายปฏิบัติการและบริหาร
                </span>
                
                <div className="space-y-1.5 max-h-[220px] overflow-y-auto pr-1">
                  {/* โหลดเอเจนต์ปฏิบัติการจาก DB */}
                  {agentsList
                    .filter((a: any) => ['executive', 'cos', 'analyst', 'report', 'coo', 'cfo', 'meeting', 'provincial'].includes(a.role))
                    .map((agent) => {
                      const isSelected = selectedAgentRole === agent.role;
                      const act = getAgentActivity(agent.role);
                      return (
                        <div
                          key={agent.id}
                          onClick={() => setSelectedAgentRole(agent.role)}
                          className={`p-2.5 rounded-xl text-left cursor-pointer transition-all duration-150 relative overflow-hidden border ${
                            isSelected 
                              ? 'bg-slate-900 border-gold-500/50 text-white shadow-md' 
                              : 'bg-slate-950/60 border-slate-900/60 hover:bg-slate-900/30 hover:border-slate-850 text-slate-400'
                          }`}
                        >
                          {isSelected && (
                            <div className="absolute top-0 left-0 bottom-0 w-0.5 bg-gradient-to-b from-gold-500 to-amber-700"></div>
                          )}
                          <div className="flex justify-between items-center">
                            <span className={`text-[11px] font-bold ${isSelected ? 'text-gold-400' : 'text-slate-300'}`}>{agent.name}</span>
                            <span className={`text-[8px] uppercase tracking-wider px-1.5 py-0.2 rounded font-bold ${
                              emergencyActive
                                ? 'bg-red-950/40 border border-red-900 text-red-500'
                                : act.status === 'busy'
                                ? 'bg-amber-950/40 border border-amber-900 text-amber-500'
                                : 'bg-emerald-950/40 border border-emerald-900 text-emerald-500'
                            }`}>
                              {emergencyActive ? 'SUSPENDED' : act.status.toUpperCase()}
                            </span>
                          </div>
                          
                          {/* รายละเอียดกิจกรรมการทำงาน */}
                          <p className="text-[10px] text-slate-400 mt-1 font-light truncate leading-relaxed">
                            {act.text}
                          </p>
                        </div>
                      );
                    })}
                </div>
              </div>

              {/* หมวดหมู่ 2: ฝ่ายโครงสร้างข้อมูลและวิศวกรรม (Data & Security Infrastructure AI) */}
              <div className="space-y-2.5 pt-1">
                <span className="text-[10px] uppercase tracking-wider font-bold text-slate-300 block border-l-2 border-amber-600 pl-2">
                  🔒 ฝ่ายโครงสร้างข้อมูลและวิศวกรรม
                </span>

                <div className="space-y-1.5 max-h-[180px] overflow-y-auto pr-1">
                  {/* แสดง AI หลังบ้านที่เฝ้าดูแลระบบข้อมูล */}
                  {[
                    { name: "ธรรมาภิบาลข้อมูล (Data Governance)", role: "datagov" },
                    { name: "วิเคราะห์การเก็บล็อก (Log Intelligence AI)", role: "db_monitor" },
                    { name: "ผู้ช่วย RAG Optimizer (3072D Vector)", role: "rag_optimizer" },
                    { name: "ผู้คุมความปลอดภัย (Cyber Security AI)", role: "security_officer" }
                  ].map((infAgent) => {
                    const isSelected = selectedAgentRole === infAgent.role;
                    const act = getAgentActivity(infAgent.role);
                    return (
                      <div
                        key={infAgent.role}
                        onClick={() => setSelectedAgentRole(infAgent.role)}
                        className={`p-2.5 rounded-xl text-left cursor-pointer transition-all duration-150 relative overflow-hidden border ${
                          isSelected 
                            ? 'bg-slate-900 border-gold-500/50 text-white shadow-md' 
                            : 'bg-slate-950/60 border-slate-900/60 hover:bg-slate-900/30 hover:border-slate-855 text-slate-450'
                        }`}
                      >
                        {isSelected && (
                          <div className="absolute top-0 left-0 bottom-0 w-0.5 bg-gradient-to-b from-amber-600 to-orange-700"></div>
                        )}
                        <div className="flex justify-between items-center">
                          <span className={`text-[11px] font-bold ${isSelected ? 'text-amber-400' : 'text-slate-300'}`}>{infAgent.name}</span>
                          <span className={`text-[8px] uppercase tracking-wider px-1.5 py-0.2 rounded font-bold ${
                            emergencyActive
                              ? 'bg-red-950/40 border border-red-900 text-red-500'
                              : act.status === 'busy'
                              ? 'bg-amber-950/40 border border-amber-900 text-amber-500 animate-pulse'
                              : 'bg-indigo-950/40 border border-indigo-900 text-indigo-400'
                          }`}>
                            {emergencyActive ? 'SUSPENDED' : 'INFRA'}
                          </span>
                        </div>
                        
                        {/* รายละเอียดกิจกรรมหลังบ้าน */}
                        <p className="text-[10px] text-slate-400 mt-1 font-light truncate leading-relaxed">
                          {act.text}
                        </p>
                      </div>
                    );
                  })}
                </div>
              </div>

            </div>
            
            {/* KPIs Tracker Section */}
            <div className="p-5 bg-slate-950/40 border border-slate-850 rounded-2xl glass space-y-4">
              <div className="flex justify-between items-center pb-2 border-b border-slate-900">
                <h4 className="text-xs font-bold text-slate-355 uppercase tracking-wider flex items-center gap-1.5">
                  📊 ดัชนี KPIs ประจำตำแหน่ง/ฝ่าย {currentRoleData.name}
                </h4>
                <button
                  onClick={handleAnalyzeKPIs}
                  disabled={analyzingKpi}
                  className="text-[10px] text-gold-500 hover:text-gold-400 font-medium"
                >
                  {analyzingKpi ? 'กำลังประมวลผล...' : '🔍 ให้ AI วิเคราะห์เชิงลึก'}
                </button>
              </div>

              {/* AI KPI analysis result show */}
              {kpiAnalysis && (
                <div className="p-4 bg-slate-900/60 border border-slate-850 rounded-xl text-left text-[11px] leading-relaxed text-slate-300 space-y-2 max-h-[160px] overflow-y-auto font-light animate-slide-down">
                  <p className="font-bold text-gold-400">💡 รายงานความคุ้มค่าและข้อสั่งการของ AI:</p>
                  <div className="whitespace-pre-wrap">{kpiAnalysis}</div>
                </div>
              )}

              <div className="space-y-3">
                {currentRoleData.kpis.map((kpi: any, idx: number) => {
                  const percent = Math.min(100, (kpi.value / kpi.target) * 100);
                  const isSuccess = kpi.value >= kpi.target;
                  return (
                    <div key={idx} className="space-y-1">
                      <div className="flex justify-between text-[11px] font-light">
                        <span className="text-slate-300">{kpi.label}</span>
                        <span>
                          <strong className={isSuccess ? 'text-emerald-400' : 'text-amber-500'}>
                            {kpi.value}
                          </strong>
                          <span className="text-slate-500"> / {kpi.target} {kpi.unit}</span>
                        </span>
                      </div>
                      {/* Progress Bar */}
                      <div className="w-full bg-slate-900 h-1 rounded-full overflow-hidden border border-slate-955">
                        <div 
                          className={`h-full rounded-full transition-all duration-500 ${
                            isSuccess ? 'bg-gradient-to-r from-emerald-600 to-green-500' : 'bg-gradient-to-r from-amber-600 to-yellow-500'
                          }`} 
                          style={{ width: `${percent}%` }}
                        ></div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Inbox: Tasks & Orders */}
            <div className="p-5 bg-slate-950/40 border border-slate-850 rounded-2xl glass space-y-3.5">
              <h4 className="text-xs font-bold text-slate-350 uppercase tracking-wider border-b border-slate-900 pb-2 flex items-center gap-1.5">
                📬 กล่องรับงานสั่งการเข้ามาใหม่
              </h4>
              <div className="space-y-2.5">
                {currentRoleData.tasks.map((task: TaskItem) => (
                  <div
                    key={task.id}
                    onClick={() => handleSelectTask(task)}
                    className="p-3.5 bg-slate-950/60 hover:bg-slate-900/60 border border-slate-900 hover:border-slate-800 rounded-xl text-left cursor-pointer transition-all duration-150 relative overflow-hidden group"
                  >
                    <div className="absolute top-0 left-0 bottom-0 w-1 bg-rose-600"></div>
                    <div className="flex justify-between items-start gap-3">
                      <span className="text-[9px] uppercase tracking-wider font-bold text-rose-500 bg-rose-950/40 px-1.5 py-0.5 rounded border border-rose-900/40">
                        {task.type}
                      </span>
                      <span className="text-[10px] text-slate-500 group-hover:text-gold-500 transition-colors font-semibold">คลิกมอบงาน AI ➔</span>
                    </div>
                    <p className="text-xs font-bold text-white mt-1.5 line-clamp-1">{task.title}</p>
                    <p className="text-[10px] text-slate-400 font-light mt-1 line-clamp-2 leading-relaxed">{task.description}</p>
                  </div>
                ))}
              </div>
            </div>

          </div>

          {/* Right Side: Simulator Work Tools */}
          <div className="lg:col-span-8 space-y-6">
            
            {/* Tools Workspace Navigation */}
            <div className="border border-slate-850 rounded-3xl bg-slate-900/20 glass overflow-hidden flex flex-col min-h-[500px]">
              
              {/* Header & Subtabs */}
              <div className="p-5 bg-slate-950/80 border-b border-slate-850 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 text-left">
                <div>
                  <span className="text-[9px] uppercase tracking-widest text-gold-500 font-bold bg-gold-950/60 border border-gold-900 px-2.5 py-0.5 rounded-full">
                    Virtual Simulation Workspace
                  </span>
                  <h3 className="text-sm font-bold text-white mt-1.5">ประสานการสั่งงานผู้ช่วย: <span className="text-gold-400">{currentRoleData.name}</span></h3>
                </div>

                {/* Workspace Navigation buttons */}
                <div className="flex flex-wrap items-center bg-slate-900 p-1 rounded-xl border border-slate-800 shrink-0 gap-1">
                  <button
                    onClick={() => setActiveWorkspaceTab('draft')}
                    className={`px-3 py-1.5 text-xs font-semibold rounded-lg transition-all ${
                      activeWorkspaceTab === 'draft' ? 'bg-slate-950 text-gold-400 border border-slate-800' : 'text-slate-400 hover:text-slate-200'
                    }`}
                  >
                    📄 ร่างหนังสือราชการ
                  </button>
                  <button
                    onClick={() => setActiveWorkspaceTab('consult')}
                    className={`px-3 py-1.5 text-xs font-semibold rounded-lg transition-all ${
                      activeWorkspaceTab === 'consult' ? 'bg-slate-950 text-gold-400 border border-slate-800' : 'text-slate-400 hover:text-slate-200'
                    }`}
                  >
                    💬 แชทหารือ
                  </button>
                  <button
                    onClick={() => setActiveWorkspaceTab('board')}
                    className={`px-3 py-1.5 text-xs font-semibold rounded-lg transition-all ${
                      activeWorkspaceTab === 'board' ? 'bg-slate-950 text-gold-400 border border-slate-800' : 'text-slate-400 hover:text-slate-200'
                    }`}
                  >
                    ⚠️ แผนงาน
                  </button>
                  <button
                    onClick={() => setActiveWorkspaceTab('simulator')}
                    className={`px-3 py-1.5 text-xs font-semibold rounded-lg transition-all ${
                      activeWorkspaceTab === 'simulator' ? 'bg-slate-950 text-gold-400 border border-slate-800' : 'text-slate-400 hover:text-slate-200'
                    }`}
                  >
                    📊 What-If Simulator
                  </button>
                  <button
                    onClick={() => setActiveWorkspaceTab('orchestrator')}
                    className={`px-3 py-1.5 text-xs font-semibold rounded-lg transition-all ${
                      activeWorkspaceTab === 'orchestrator' ? 'bg-slate-950 text-gold-400 border border-slate-800' : 'text-slate-400 hover:text-slate-200'
                    }`}
                  >
                    ⚡ ศูนย์สั่งการรวม
                  </button>
                  <button
                    onClick={() => setActiveWorkspaceTab('monitor')}
                    className={`px-3 py-1.5 text-xs font-semibold rounded-lg transition-all ${
                      activeWorkspaceTab === 'monitor' ? 'bg-slate-950 text-gold-400 border border-slate-800' : 'text-slate-400 hover:text-slate-200'
                    }`}
                  >
                    📈 เฝ้าระวัง & มอนิเตอร์
                  </button>

                  {/* Emergency Stop Toggle in Toolbar */}
                  {emergencyActive ? (
                    <button
                      onClick={handleReactivateSystem}
                      className="ml-2 px-2.5 py-1.5 bg-emerald-950/60 hover:bg-emerald-900 border border-emerald-800 text-emerald-400 text-[10px] font-bold rounded-lg transition-all animate-pulse"
                    >
                      🟢 กู้คืนระบบ AI
                    </button>
                  ) : (
                    <button
                      onClick={handleEmergencyStop}
                      className="ml-2 px-2.5 py-1.5 bg-red-950/60 hover:bg-red-900 border border-red-800 text-red-400 text-[10px] font-bold rounded-lg transition-all"
                    >
                      🚨 Emergency Stop
                    </button>
                  )}
                </div>
              </div>

              {/* Tab 1: Official Letter Draft Room */}
              {activeWorkspaceTab === 'draft' && (
                <div className="p-6 space-y-6 flex-1 overflow-y-auto max-h-[550px]">
                  
                  {/* Form fields */}
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-left">
                    <div className="space-y-1.5">
                      <label className="text-[11px] text-slate-400 font-medium">ประเภทหนังสือราชการ</label>
                      <select
                        value={letterType}
                        onChange={(e) => setLetterType(e.target.value)}
                        className="w-full bg-slate-950 border border-slate-850 focus:border-gold-500/50 rounded-xl px-3 py-2.5 text-xs text-white outline-none cursor-pointer"
                      >
                        <option value="บันทึกข้อความสั่งการจังหวัด (Official Order)">บันทึกข้อความสั่งการจังหวัด (Official Order)</option>
                        <option value="หนังสือหารือระเบียบ/ข้อกฎหมาย (Legal Consultation Request)">หนังสือหารือระเบียบ/ข้อกฎหมาย (Legal Request)</option>
                        <option value="หนังสือรายงานสถานการณ์ฉุกเฉิน (Emergency Situation Report)">หนังสือรายงานสถานการณ์ฉุกเฉิน (Emergency Report)</option>
                        <option value="หนังสืออนุมัติโครงการและงบประมาณ (Project & Budget Approval)">หนังสืออนุมัติโครงการและงบประมาณ (Budget Approval)</option>
                      </select>
                    </div>
                    
                    <div className="space-y-1.5">
                      <label className="text-[11px] text-slate-400 font-medium">ระดับชั้นความลับ</label>
                      <select
                        value={confidentiality}
                        onChange={(e) => setConfidentiality(e.target.value)}
                        className="w-full bg-slate-950 border border-slate-850 focus:border-gold-500/50 rounded-xl px-3 py-2.5 text-xs text-white outline-none cursor-pointer"
                      >
                        <option value="Public">Public (เปิดเผยทั่วไป)</option>
                        <option value="Internal">Internal (ใช้ภายในหน่วยงาน)</option>
                        <option value="Confidential">Confidential (เอกสารลับความมั่นคงการแพทย์)</option>
                      </select>
                    </div>

                    <div className="space-y-1.5 sm:col-span-2">
                      <label className="text-[11px] text-slate-400 font-medium">หัวเรื่องหนังสือราชการ</label>
                      <input
                        type="text"
                        value={letterSubject}
                        onChange={(e) => setLetterSubject(e.target.value)}
                        placeholder="เช่น มอบหมายสั่งการจัดหาพัสดุและตั้งวอร์รูม PM2.5..."
                        className="w-full bg-slate-950 border border-slate-850 focus:border-gold-500/50 rounded-xl px-4 py-2.5 text-xs text-white outline-none"
                      />
                    </div>

                    <div className="space-y-1.5 sm:col-span-2">
                      <label className="text-[11px] text-slate-400 font-medium">รายละเอียดเนื้อหาและแนวทางการตัดสินใจข้อสั่งการ *</label>
                      <textarea
                        rows={4}
                        value={letterDetail}
                        onChange={(e) => setLetterDetail(e.target.value)}
                        placeholder="กรอกรายละเอียดเพื่อให้เอเจนต์นำไปประมวลสรุป เรียงเรียงเป็นสำนวนจดหมายราชการตราครุฑทางการไทยอย่างประณีต..."
                        className="w-full bg-slate-955 border border-slate-850 focus:border-gold-500/50 rounded-xl px-4 py-2.5 text-xs text-white outline-none resize-none font-light"
                      />
                    </div>
                  </div>

                  {/* Submit button */}
                  <div className="flex justify-end border-t border-slate-900 pt-4">
                    <button
                      onClick={handleDraftSimulate}
                      disabled={loading || !letterSubject.trim() || !letterDetail.trim()}
                      className="px-5 py-2.5 bg-gradient-to-r from-gold-600 to-amber-700 hover:from-gold-500 hover:to-amber-600 disabled:opacity-40 text-slate-950 font-bold rounded-xl text-xs transition-all shadow-lg active:scale-[0.98] flex items-center gap-2"
                    >
                      {loading ? (
                        <>
                          <div className="w-3.5 h-3.5 border-2 border-slate-950 border-t-transparent rounded-full animate-spin"></div>
                          <span>กำลังแต่งเรียบเรียงสำนวนราชการตราครุฑ...</span>
                        </>
                      ) : (
                        <>📝 <span>ส่งให้เอเจนต์ AI ร่างหนังสือราชการ</span></>
                      )}
                    </button>
                  </div>

                  {/* Draft Result: Premium Garuda Paper style */}
                  {draftResult && draftResult.draft_content && (
                    <div className="border border-amber-900/40 bg-amber-50/95 text-slate-900 p-8 rounded-2xl shadow-2xl space-y-6 font-serif max-h-[400px] overflow-y-auto animate-fade-in relative text-left">
                      <div className="absolute top-4 right-4 text-[9px] uppercase tracking-wider font-sans font-bold bg-amber-200/60 border border-amber-300 px-2 py-0.5 rounded text-amber-800">
                        HosPrime AI Copy
                      </div>
                      
                      {/* Official Letterhead Header */}
                      <div className="flex flex-col items-center text-center space-y-2 border-b border-slate-900/10 pb-4">
                        <span className="text-4xl text-amber-800">🦅</span>
                        <h4 className="text-sm font-bold uppercase tracking-wider font-sans text-amber-900">บันทึกข้อความ</h4>
                        <p className="text-[10px] text-slate-600 font-sans font-semibold">สำนักงานสาธารณสุขจังหวัดเชียงราย กระทรวงสาธารณสุข</p>
                      </div>
                      
                      {/* Meta Fields */}
                      <div className="grid grid-cols-2 gap-y-2 text-xs font-sans text-slate-700 border-b border-slate-900/5 pb-4">
                        <div><strong className="text-slate-900">ส่วนราชการ:</strong> {currentRoleData.department}</div>
                        <div><strong className="text-slate-900">ที่:</strong> ชร ๐๐๓๒/พิเศษ.{Math.floor(Math.random() * 900 + 100)}</div>
                        <div><strong className="text-slate-900">วันที่:</strong> ๑๖ มิถุนายน ๒๕๖๙</div>
                        <div><strong className="text-slate-900">ระดับความลับ:</strong> {confidentiality === 'Public' ? 'เปิดเผยทั่วไป' : confidentiality === 'Internal' ? 'ภายในหน่วยงาน' : 'ลับที่สุด'}</div>
                        <div className="col-span-2 border-t border-slate-900/5 pt-2">
                          <strong className="text-slate-900 text-sm">เรื่อง:</strong> <span className="text-slate-800 font-semibold">{letterSubject}</span>
                        </div>
                      </div>

                      {/* Content Body */}
                      <pre className="text-xs leading-relaxed whitespace-pre-wrap font-sans font-light text-slate-800 px-2 bg-transparent select-text">
                        {draftResult.draft_content}
                      </pre>
                      
                      {/* Official Sign-off */}
                      <div className="flex flex-col items-end pt-4 border-t border-slate-900/5 font-sans">
                        <div className="text-center w-60">
                          <p className="text-[10px] italic text-slate-500 mb-5">(ลายมือชื่อดิจิทัลและแสตมป์จาก AI)</p>
                          <p className="text-xs font-bold text-slate-955 border-b border-slate-900/10 pb-1">{currentRoleData.name}</p>
                          <p className="text-[10px] text-slate-700 mt-1">{currentRoleData.title}</p>
                          <p className="text-[8px] text-slate-500 font-mono mt-1">HosPrime AI Office Security Hash Verified</p>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              )}

              {/* Tab 2: Consult/Chat with selected agent */}
              {activeWorkspaceTab === 'consult' && (
                <div className="flex-1 flex flex-col bg-slate-950/40">
                  <div className="px-5 py-2.5 bg-slate-950/90 border-b border-slate-900 text-[10px] text-slate-450 flex justify-between items-center shrink-0">
                    <span>💬 แชทหารือ SOP ข้อมูลกฎระเบียบราชการ และแนวทางปัญญาประดิษฐ์เพื่อช่วยการบริหาร</span>
                    <span>ผู้เชี่ยวชาญ: <strong>{currentRoleData.name}</strong></span>
                  </div>

                  {/* Messages scroll area */}
                  <div className="flex-1 p-5 overflow-y-auto space-y-4 max-h-[380px] min-h-[300px]">
                    
                    {/* Default greeting */}
                    <div className="flex gap-3 text-left">
                      <div className="w-7 h-7 rounded-full bg-gold-950 border border-gold-900 flex items-center justify-center text-xs shadow-md shrink-0">🤖</div>
                      <div className="p-3.5 bg-slate-900/80 border border-slate-850 rounded-2xl rounded-tl-none max-w-[85%] text-xs leading-relaxed font-light text-slate-200">
                        สวัสดีครับ ผมคือระบบผู้ช่วยบริหารอัจฉริยะองค์กร ในฐานะ **{currentRoleData.name}** <br/>
                        พร้อมช่วยคุณประเมิน SOP ค้นหากฎระเบียบสาธารณสุข ตรวจวินัยงบประมาณการคลัง ตรวจแผน MOPH KPIs หรือจัดเตรียมเล่มรายงานสรุปตามวาระงานที่คุณมอบหมายครับ
                      </div>
                    </div>

                    {/* Logs list */}
                    {currentChatLogs.map((msg, index) => {
                      const isUser = msg.role === 'user';
                      return (
                        <div key={index} className={`flex gap-3 ${isUser ? 'justify-end' : 'justify-start'}`}>
                          {!isUser && (
                            <div className="w-7 h-7 rounded-full bg-gold-950 border border-gold-900 flex items-center justify-center text-xs shadow-md shrink-0">🤖</div>
                          )}
                          <div className={`p-3.5 rounded-2xl text-left text-xs leading-relaxed max-w-[85%] font-light whitespace-pre-wrap ${
                            isUser
                              ? 'bg-gradient-to-r from-gold-600 to-amber-700 text-slate-950 font-medium rounded-tr-none shadow'
                              : 'bg-slate-900/80 border border-slate-850 text-slate-200 rounded-tl-none'
                          }`}>
                            {msg.text}
                          </div>
                          {isUser && (
                            <div className="w-7 h-7 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center text-[10px] font-bold shrink-0">ME</div>
                          )}
                        </div>
                      );
                    })}

                    {chatLoading && (
                      <div className="flex gap-3 animate-pulse text-left">
                        <div className="w-7 h-7 rounded-full bg-gold-950 border border-gold-900 flex items-center justify-center text-xs shrink-0">⏳</div>
                        <div className="p-3.5 bg-slate-900/50 border border-slate-850 rounded-2xl rounded-tl-none text-xs text-slate-500">
                          กำลังสืบค้น SOP และเรียบเรียงข้อมูลความเห็นประมวลผล...
                        </div>
                      </div>
                    )}

                  </div>

                  {/* Prompt input */}
                  <div className="p-4 bg-slate-950/85 border-t border-slate-900 flex gap-2 shrink-0">
                    <input
                      type="text"
                      value={chatInput}
                      onChange={(e) => setChatInput(e.target.value)}
                      onKeyDown={(e) => {
                        if (e.key === 'Enter') handleConsultTwin();
                      }}
                      placeholder={`ถามคำถาม หรือมอบหมายงานให้กับ ${currentRoleData.name}...`}
                      disabled={chatLoading}
                      className="flex-1 bg-slate-900 border border-slate-850 rounded-xl px-4 py-2.5 text-xs text-white placeholder-slate-550 focus:outline-none focus:border-gold-500/50"
                    />
                    <button
                      onClick={handleConsultTwin}
                      disabled={chatLoading || !chatInput.trim()}
                      className="px-5 py-2.5 bg-gold-600 hover:bg-gold-500 disabled:opacity-40 text-xs font-semibold rounded-xl text-slate-950 transition-all shrink-0"
                    >
                      ส่งข้อความ
                    </button>
                  </div>
                </div>
              )}

              {/* Tab 3: Plans & Obstacles Board */}
              {activeWorkspaceTab === 'board' && (
                <div className="p-6 space-y-6 flex-1 overflow-y-auto max-h-[550px] text-left">
                  
                  {/* แผงอธิบาย Workflow Builder */}
                  <div className="p-4.5 bg-slate-955/60 border border-slate-850 rounded-2xl flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 relative overflow-hidden">
                    <div className="absolute top-0 right-0 w-24 h-24 bg-gold-500/5 rounded-full blur-2xl"></div>
                    <div>
                      <h4 className="text-xs font-bold text-gold-400 uppercase tracking-wider mb-1 flex items-center gap-2">
                        🔀 แผงผังกระบวนงานทำงาน (n8n-style Workflow Builder)
                      </h4>
                      <p className="text-[11px] text-slate-400 font-light leading-relaxed">
                        แสดงลำดับขั้นตอนการทำงานและการเชื่อมต่อข้อมูล RAG (3072 มิติ) ของตำแหน่งงานรายฝ่าย โดยมีจุดควบคุมเชื่อมโยงและสามารถกดรันตรวจสอบเพื่อประเมินความสอดคล้องนโยบาย
                      </p>
                    </div>

                    <button
                      onClick={handleRunFlowSimulation}
                      disabled={flowActive}
                      className="px-4.5 py-2 bg-gradient-to-r from-emerald-600 to-green-600 hover:from-emerald-500 hover:to-green-500 text-slate-950 font-bold rounded-xl text-xs transition-all active:scale-[0.98] shrink-0"
                    >
                      {flowActive ? '⚙️ กำลังรันประมวลผล Flow...' : '▶️ ทดสอบรัน Workflow'}
                    </button>
                  </div>

                  {/* 🔀 n8n-style Graph Canvas */}
                  <div className="p-6 bg-slate-955 border border-slate-850 rounded-3xl relative overflow-hidden min-h-[200px] shadow-inner flex items-center justify-center">
                    {/* SVG Connections Lines */}
                    <div className="absolute inset-0 w-full h-full pointer-events-none hidden md:block">
                      <svg className="w-full h-full">
                        {/* Static lines */}
                        <path d="M 80,100 H 220" stroke="#1e293b" strokeWidth="2.5" fill="none" />
                        <path d="M 285,100 H 425" stroke="#1e293b" strokeWidth="2.5" fill="none" />
                        <path d="M 490,100 H 630" stroke="#1e293b" strokeWidth="2.5" fill="none" />
                        <path d="M 695,100 H 835" stroke="#1e293b" strokeWidth="2.5" fill="none" />
                        
                        {/* Dynamic Glowing lines on simulation run */}
                        {flowActive && flowStep >= 1 && (
                          <path d="M 80,100 H 220" stroke="#f59e0b" strokeWidth="2.5" strokeDasharray="6, 4" className="animate-[dash_1s_linear_infinite]" fill="none" />
                        )}
                        {flowActive && flowStep >= 2 && (
                          <path d="M 285,100 H 425" stroke="#10b981" strokeWidth="2.5" strokeDasharray="6, 4" className="animate-[dash_1s_linear_infinite]" fill="none" />
                        )}
                        {flowActive && flowStep >= 3 && (
                          <path d="M 490,100 H 630" stroke="#3b82f6" strokeWidth="2.5" strokeDasharray="6, 4" className="animate-[dash_1s_linear_infinite]" fill="none" />
                        )}
                        {flowActive && flowStep >= 4 && (
                          <path d="M 695,100 H 835" stroke="#8b5cf6" strokeWidth="2.5" strokeDasharray="6, 4" className="animate-[dash_1s_linear_infinite]" fill="none" />
                        )}
                      </svg>
                    </div>

                    {/* Nodes Row Layout */}
                    <div className="flex flex-col md:flex-row items-center md:justify-between w-full z-10 gap-6 md:gap-2">
                      
                      {/* Node 1 */}
                      <div className={`p-3 rounded-2xl border bg-slate-950/90 text-center w-36 relative transition-all duration-150 ${
                        flowActive && flowStep === 1 ? 'border-amber-500 shadow-md ring-1 ring-amber-500/10' : 'border-slate-850'
                      }`}>
                        <span className="text-sm block">👔</span>
                        <span className="text-[10px] font-bold text-white block mt-1">1. สั่งยุทธศาสตร์</span>
                        <span className="text-[8px] text-slate-500 block">Executive CEO</span>
                      </div>

                      {/* Node 2 */}
                      <div className={`p-3 rounded-2xl border bg-slate-950/90 text-center w-36 relative transition-all duration-150 ${
                        flowActive && flowStep === 2 ? 'border-emerald-500 shadow-md ring-1 ring-emerald-500/10' : 'border-slate-850'
                      }`}>
                        <span className="text-sm block">📚</span>
                        <span className="text-[10px] font-bold text-white block mt-1">2. สืบค้นคู่มือ SOP</span>
                        <span className="text-[8px] text-slate-500 block">Knowledge RAG</span>
                      </div>

                      {/* Node 3 */}
                      <div className={`p-3 rounded-2xl border bg-slate-950/90 text-center w-36 relative transition-all duration-150 ${
                        flowActive && flowStep === 3 ? 'border-blue-500 shadow-md ring-1 ring-blue-500/10' : 'border-slate-850'
                      }`}>
                        <span className="text-sm block">🔒</span>
                        <span className="text-[10px] font-bold text-white block mt-1">3. ตรวจสอบ PDPA</span>
                        <span className="text-[8px] text-slate-500 block">Data Governance</span>
                      </div>

                      {/* Node 4 */}
                      <div className={`p-3 rounded-2xl border bg-slate-950/90 text-center w-36 relative transition-all duration-150 ${
                        flowActive && flowStep === 4 ? 'border-violet-500 shadow-md ring-1 ring-violet-500/10' : 'border-slate-850'
                      }`}>
                        <span className="text-sm block">✍</span>
                        <span className="text-[10px] font-bold text-white block mt-1">4. ร่างหนังสือราชการ</span>
                        <span className="text-[8px] text-slate-500 block">Report Writer</span>
                      </div>

                      {/* Node 5 */}
                      <div className={`p-3 rounded-2xl border bg-slate-950/90 text-center w-36 relative transition-all duration-150 ${
                        flowActive && flowStep === 5 ? 'border-pink-500 shadow-md ring-1 ring-pink-500/10' : 'border-slate-850'
                      }`}>
                        <span className="text-sm block">✒️</span>
                        <span className="text-[10px] font-bold text-white block mt-1">5. ลงนามส่งนโยบาย</span>
                        <span className="text-[8px] text-slate-500 block">PHO Approval</span>
                      </div>

                    </div>
                  </div>

                  {/* 🛠️ Tools Hub & Connected MCP Servers */}
                  <div className="space-y-3 pt-2">
                    <h5 className="text-[11px] font-bold text-slate-300 uppercase tracking-widest flex items-center gap-1.5 border-b border-slate-900 pb-2">
                      🧰 Tools Hub (ระบบเชื่อมต่อเครื่องมือประมวลผลข้อมูลองค์กร)
                    </h5>

                    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
                      {/* Tool 1 */}
                      <div className="p-3.5 bg-slate-950/50 border border-slate-900 rounded-2xl text-left space-y-1">
                        <div className="flex justify-between items-center">
                          <span className="text-[10px] font-bold text-white">📊 MOPH HDC Connector</span>
                          <span className="w-1.5 h-1.5 bg-emerald-500 rounded-full"></span>
                        </div>
                        <p className="text-[8px] text-slate-500 font-light leading-relaxed">ซิงก์ข้อมูลคิวเตียงว่างและสถิติคนไข้ OPD ระดับอำเภอ</p>
                        <span className="text-[8px] font-mono text-slate-600 block pt-1">ENDPOINT: /api/hdc/sync</span>
                      </div>

                      {/* Tool 2 */}
                      <div className="p-3.5 bg-slate-950/50 border border-slate-900 rounded-2xl text-left space-y-1">
                        <div className="flex justify-between items-center">
                          <span className="text-[10px] font-bold text-white">🗺️ GIS Environment API</span>
                          <span className="w-1.5 h-1.5 bg-emerald-500 rounded-full"></span>
                        </div>
                        <p className="text-[8px] text-slate-500 font-light leading-relaxed">ดึงแผนที่จุดความร้อน (Hotspots) และปริมาณฝุ่นละออง PM2.5</p>
                        <span className="text-[8px] font-mono text-slate-600 block pt-1">ENDPOINT: /api/gis/pm25</span>
                      </div>

                      {/* Tool 3 */}
                      <div className="p-3.5 bg-slate-950/50 border border-slate-900 rounded-2xl text-left space-y-1">
                        <div className="flex justify-between items-center">
                          <span className="text-[10px] font-bold text-white">📚 SOP Vector Database</span>
                          <span className="w-1.5 h-1.5 bg-emerald-500 rounded-full"></span>
                        </div>
                        <p className="text-[8px] text-slate-500 font-light leading-relaxed">คลังข้อมูลและเอกสารระเบียบสาธารณสุขฉบับอัปเดต</p>
                        <span className="text-[8px] font-mono text-slate-600 block pt-1">DATABASES: sqlite_vector</span>
                      </div>

                      {/* Tool 4 */}
                      <div className="p-3.5 bg-slate-950/50 border border-slate-900 rounded-2xl text-left space-y-1">
                        <div className="flex justify-between items-center">
                          <span className="text-[10px] font-bold text-white">🏥 Referral FHIR Gateway</span>
                          <span className="w-1.5 h-1.5 bg-emerald-500 rounded-full"></span>
                        </div>
                        <p className="text-[8px] text-slate-500 font-light leading-relaxed">ตัวกลางรับส่งเวชระเบียน EHR ปลอดภัยตามมาตรฐานสากล</p>
                        <span className="text-[8px] font-mono text-slate-600 block pt-1">STANDARDS: FHIR v4</span>
                      </div>
                    </div>
                  </div>

                  {/* แผงแสดงแผนและอุปสรรคย่อยด้านล่าง */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-1">
                    <div className="p-4 bg-slate-900/40 border border-slate-850 rounded-2xl">
                      <span className="text-[10px] uppercase tracking-wider font-bold text-emerald-400 block mb-2 border-b border-slate-950 pb-1.5">💼 แผนงานหลักที่ต้องประเมิน (Plans)</span>
                      <ul className="space-y-1.5 text-[10px] text-slate-350 font-light pl-2">
                        {currentRoleData.plans.map((plan: string, i: number) => (
                          <li key={i} className="list-disc leading-relaxed">{plan}</li>
                        ))}
                      </ul>
                    </div>
                    <div className="p-4 bg-slate-900/40 border border-slate-850 rounded-2xl">
                      <span className="text-[10px] uppercase tracking-wider font-bold text-rose-400 block mb-2 border-b border-slate-950 pb-1.5">⚠️ ปัญหาและประเด็นกีดขวาง (Obstacles)</span>
                      <ul className="space-y-1.5 text-[10px] text-slate-355 font-light pl-2">
                        {currentRoleData.obstacles.map((obs: string, i: number) => (
                          <li key={i} className="list-disc leading-relaxed">{obs}</li>
                        ))}
                      </ul>
                    </div>
                  </div>

                </div>
              )}

              {/* Tab 4: What-If Simulation Panel */}              {/* Tab 4: What-If Simulation Panel */}
              {activeWorkspaceTab === 'simulator' && (
                <div className="p-6 space-y-6 flex-1 overflow-y-auto max-h-[550px] text-left">
                  <div className="p-4.5 bg-slate-955/60 border border-slate-850 rounded-2xl relative overflow-hidden">
                    <div className="absolute top-0 right-0 w-24 h-24 bg-amber-500/5 rounded-full blur-2xl"></div>
                    <h4 className="text-xs font-bold text-gold-400 uppercase tracking-wider mb-1.5 flex items-center gap-2">
                      📊 ระบบจำลองและคาดการณ์สถานการณ์บริการและอัตราเตียง (What-If Operations Simulator)
                    </h4>
                    <p className="text-[11px] text-slate-400 font-light leading-relaxed">
                      ปรับแต่งปริมาณความหนาแน่นของผู้รับบริการ จำนวนทรัพยากรเตียง ICU และอัตรากำลังคนปฏิบัติงานหน้างาน เพื่อคาดการณ์เวลาคอยคิวและอัตราครองเตียงล่วงหน้าก่อนสั่งการจริงในจดหมายทางการ
                    </p>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {/* Controls Column */}
                    <div className="p-5 bg-slate-955/40 border border-slate-850 rounded-2xl space-y-5">
                      <h5 className="text-[11px] font-bold text-slate-300 uppercase tracking-wider border-b border-slate-900 pb-2">
                        🎛️ เลื่อนปรับตัวแปรระบบบริการ
                      </h5>
                      
                      {/* OPD Load */}
                      <div className="space-y-2">
                        <div className="flex justify-between text-xs">
                          <span className="text-slate-400">ปริมาณผู้ป่วยนอก OPD Load (Factor)</span>
                          <span className="text-gold-400 font-bold">{opdLoad.toFixed(1)}x</span>
                        </div>
                        <input
                          type="range"
                          min="0.5"
                          max="3.0"
                          step="0.1"
                          value={opdLoad}
                          onChange={(e) => setOpdLoad(parseFloat(e.target.value))}
                          className="w-full accent-gold-500 bg-slate-900 h-1.5 rounded-lg appearance-none cursor-pointer"
                        />
                        <div className="flex justify-between text-[9px] text-slate-500 font-light">
                          <span>เบาบาง (0.5x)</span>
                          <span>ปกติ (1.0x)</span>
                          <span>หนาแน่นมาก (2.0x)</span>
                          <span>วิกฤตล้นระบบ (3.0x)</span>
                        </div>
                      </div>

                      {/* ICU Beds */}
                      <div className="space-y-2">
                        <div className="flex justify-between text-xs">
                          <span className="text-slate-400">ความจุเตียงหอผู้ป่วยวิกฤต ICU (เตียงว่าง)</span>
                          <span className="text-gold-400 font-bold">{icuBeds} เตียง</span>
                        </div>
                        <input
                          type="range"
                          min="5"
                          max="30"
                          step="1"
                          value={icuBeds}
                          onChange={(e) => setIcuBeds(parseInt(e.target.value))}
                          className="w-full accent-gold-500 bg-slate-900 h-1.5 rounded-lg appearance-none cursor-pointer"
                        />
                        <div className="flex justify-between text-[9px] text-slate-500 font-light">
                          <span>วิกฤตเตียงขาด (5 เตียง)</span>
                          <span>มาตรฐาน (12 เตียง)</span>
                          <span>จัดกำลังเสริมสูงสุด (30 เตียง)</span>
                        </div>
                      </div>

                      {/* Staff FTE */}
                      <div className="space-y-2">
                        <div className="flex justify-between text-xs">
                          <span className="text-slate-400">อัตรากำลังคนหน้างาน Staff FTE (Ratio)</span>
                          <span className="text-gold-400 font-bold">{Math.floor(staffFte * 100)}%</span>
                        </div>
                        <input
                          type="range"
                          min="0.4"
                          max="2.0"
                          step="0.1"
                          value={staffFte}
                          onChange={(e) => setStaffFte(parseFloat(e.target.value))}
                          className="w-full accent-gold-500 bg-slate-900 h-1.5 rounded-lg appearance-none cursor-pointer"
                        />
                        <div className="flex justify-between text-[9px] text-slate-500 font-light">
                          <span>ขาดแคลนมาก (40%)</span>
                          <span>สมบูรณ์ตามเกณฑ์ (100%)</span>
                          <span>จัดเวรเสริมฉุกเฉิน (200%)</span>
                        </div>
                      </div>

                      <button
                        onClick={handleRunSimulation}
                        disabled={simLoading || emergencyActive}
                        className="w-full py-2.5 bg-gradient-to-r from-gold-600 to-amber-700 hover:from-gold-500 hover:to-amber-600 disabled:opacity-40 text-slate-950 font-bold rounded-xl text-xs transition-all shadow-md active:scale-[0.98] flex items-center justify-center gap-2"
                      >
                        {simLoading ? '⏳ กำลังคำนวณแบบจำลอง...' : '🔮 รันโมเดลจำลองสถานการณ์'}
                      </button>
                    </div>

                    {/* Results Column */}
                    <div className="p-5 bg-slate-955/40 border border-slate-850 rounded-2xl flex flex-col justify-between min-h-[300px]">
                      <div>
                        <h5 className="text-[11px] font-bold text-slate-300 uppercase tracking-wider border-b border-slate-900 pb-2 mb-4">
                          🎯 ผลลัพธ์การพยากรณ์จุดคอขวด
                        </h5>

                        {simResult ? (
                          <div className="space-y-4 animate-fade-in">
                            <div className="grid grid-cols-2 gap-4">
                              <div className="p-3 bg-slate-900/60 border border-slate-850 rounded-xl text-left">
                                <span className="text-[9px] text-slate-500 font-semibold block">เวลาคอยเฉลี่ย OPD</span>
                                <strong className={`text-lg font-bold block mt-1 ${simResult.opd_waiting_time > 40 ? 'text-amber-500' : 'text-emerald-400'}`}>
                                  {simResult.opd_waiting_time} นาที
                                </strong>
                                <span className="text-[8px] text-slate-500 block font-light mt-0.5">
                                  {simResult.opd_waiting_time > 40 ? '⚠️ ช้าเกินเกณฑ์มาตรฐาน 30 นาที' : '🟢 อยู่ในเกณฑ์มาตรฐาน'}
                                </span>
                              </div>

                              <div className="p-3 bg-slate-900/60 border border-slate-850 rounded-xl text-left">
                                <span className="text-[9px] text-slate-500 font-semibold block">อัตราครองเตียงวิกฤต ICU</span>
                                <strong className={`text-lg font-bold block mt-1 ${simResult.bed_occupancy > 95 ? 'text-rose-500 font-black' : 'text-emerald-400'}`}>
                                  {simResult.bed_occupancy}%
                                </strong>
                                <span className="text-[8px] text-slate-500 block font-light mt-0.5">
                                  {simResult.bed_occupancy > 95 ? '🚨 เตียงไอซียูเต็มขีดจำกัด!' : '🟢 ความจุเตียงเพียงพอ'}
                                </span>
                              </div>
                            </div>

                            <div className="p-3 bg-slate-900/80 border border-slate-850 rounded-xl text-left">
                              <span className="text-[9px] text-slate-500 font-bold block uppercase tracking-wider">สถานะจุดคอขวดองค์กร</span>
                              <div className="flex items-center gap-2 mt-1">
                                <span className={`text-xs px-2 py-0.5 rounded-full font-bold border ${
                                  simResult.bottleneck === 'ปกติ' 
                                    ? 'bg-emerald-950/40 border-emerald-900 text-emerald-400' 
                                    : 'bg-amber-950/40 border-amber-900 text-amber-500'
                                }`}>
                                  ⚠️ {simResult.bottleneck}
                                </span>
                              </div>
                            </div>

                            <div className="p-4 bg-slate-900/40 border border-slate-850 rounded-xl text-left text-xs font-light text-slate-300 relative">
                              <span className="font-bold text-gold-400 block mb-1">💡 คำแนะนำเชิงปฏิบัติการโดย AI:</span>
                              <p className="leading-relaxed text-[11px]">{simResult.recommendation}</p>

                              {/* Trigger Lineage View */}
                              <button
                                onClick={() => setLineageTarget(lineageTarget === 'sim' ? null : 'sim')}
                                className="mt-3 text-[10px] text-gold-500 hover:text-gold-400 font-bold flex items-center gap-1"
                              >
                                🔍 {lineageTarget === 'sim' ? 'ซ่อนแหล่งข้อมูลอ้างอิง' : 'แสดงแหล่งข้อมูลอ้างอิง (Data Lineage)'}
                              </button>
                            </div>
                          </div>
                        ) : (
                          <div className="h-44 border border-dashed border-slate-800 rounded-xl flex items-center justify-center text-xs text-slate-500 font-light">
                            กดปุ่ม "รันโมเดลจำลองสถานการณ์" ด้านซ้ายเพื่อรับค่าประเมิน
                          </div>
                        )}
                      </div>

                      <div className="text-[10px] text-slate-500 font-light pt-2">
                        * พยากรณ์โดยอิงการคำนวณระดับหน่วยบริการของกระทรวงสาธารณสุข
                      </div>
                    </div>
                  </div>

                  {/* Lineage expansion box */}
                  {lineageTarget === 'sim' && simResult && (
                    <div className="p-4 bg-slate-955 border border-gold-500/20 rounded-2xl text-left space-y-2.5 animate-slide-down shadow-xl relative overflow-hidden">
                      <div className="absolute top-0 right-0 w-24 h-24 bg-gold-500/5 rounded-full blur-2xl"></div>
                      <h5 className="text-xs font-bold text-gold-400 uppercase tracking-widest border-b border-slate-900 pb-1.5 flex items-center gap-1.5">
                        📂 แหล่งข้อมูลอ้างอิงและธรรมภิบาลข้อมูล (Data Lineage & Contracts)
                      </h5>
                      <div className="space-y-1.5 text-[11px] text-slate-300 leading-relaxed font-light">
                        <p>• <strong>สูตรคำนวณ Waiting Time (OPD-WT-01):</strong> <code className="text-amber-500">MAX(10, INT(30 * OPD_Load * (1.3 - Staff_FTE)))</code> ประมวลผลจาก Log กิจกรรมการคิวผู้ป่วยนอก</p>
                        <p>• <strong>สูตรคำนวณ Bed Occupancy (ICU-BO-02):</strong> <code className="text-amber-500">MIN(100, MAX(10, INT(85 * OPD_Load - (ICU_Beds - 12) * 1.5)))</code> สังเคราะห์จากยอดผู้ป่วยหนักไอซียูในเครือข่าย คปสอ.</p>
                        <p>• <strong>แหล่งฐานข้อมูล (Database Provenance):</strong> ฐานข้อมูลกลาง MOPH HDC สสจ.เชียงราย (ตาราง <code className="text-slate-400">opd_service_log</code> และ <code className="text-slate-400">ipd_ward_occupancy</code>)</p>
                        <p>• <strong>SOP คู่มือปฏิบัติงาน (Standard SOP):</strong> นิยามตัวชี้วัดกระทรวงสาธารณสุขฉบับปรับปรุง 2568 หมวดบริหารงานโรงพยาบาลปฐมภูมิ-ทุติยภูมิ</p>
                      </div>
                    </div>
                  )}
                </div>
              )}

              {/* Tab 6: System & Activity Monitor */}
              {activeWorkspaceTab === 'monitor' && (
                <div className="p-6 space-y-6 flex-1 overflow-y-auto max-h-[550px] text-left">
                  
                  {/* แสงสว่างผังห้องตามเวลาท้องถิ่นจริง */}
                  {(() => {
                    const currentHour = new Date().getHours();
                    let bgGradient = "from-slate-950 to-slate-900"; 
                    let lightStatus = "Night Mode (ไฟนีออนจำลองปฏิบัติงานล่วงเวลา)";
                    if (currentHour >= 6 && currentHour < 17) {
                      bgGradient = "from-slate-900 to-slate-800"; 
                      lightStatus = "Day Mode (ระบบแสงสว่างประหยัดพลังงานกลางวัน)";
                    } else if (currentHour >= 17 && currentHour < 19) {
                      bgGradient = "from-slate-950 via-amber-950/20 to-slate-900"; 
                      lightStatus = "Golden Hour (ระบบแสงโพล้เพล้ยามเย็น)";
                    }
                    
                    return (
                      <>
                        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 border-b border-slate-900 pb-3">
                          <div>
                            <h4 className="text-xs font-bold text-gold-400 uppercase tracking-widest flex items-center gap-1.5">
                              📈 ระบบเฝ้าระวังสถานะและมอนิเตอร์ความเคลื่อนไหว (Virtual Office Telemetry)
                            </h4>
                            <p className="text-[10px] text-slate-400 font-light mt-0.5">การตรวจสอบทราฟฟิกข้อมูล, CPU/Memory และการคุ้มครอง PDPA เรียบร้อย</p>
                          </div>
                          
                          <div className="flex gap-2">
                            <span className={`px-2.5 py-0.5 text-[9px] rounded-full border font-bold ${
                              emergencyActive 
                                ? 'bg-red-950/40 border-red-900 text-red-500 animate-pulse' 
                                : 'bg-emerald-950/40 border-emerald-900 text-emerald-400'
                            }`}>
                              {emergencyActive ? '⚠️ EMERGENCY SUSPENDED' : '🟢 RUNNING AUTONOMOUS LOOP'}
                            </span>
                          </div>
                        </div>

                        {/* 🏢 Interactive Floor Plan Map (2D Grid Layout) */}
                        <div className={`p-5 bg-gradient-to-br ${bgGradient} border border-slate-850 rounded-3xl space-y-4 relative shadow-2xl overflow-hidden`}>
                          <div className="absolute top-2 right-3 text-[9px] font-mono text-slate-500 bg-slate-955/90 px-2 py-0.5 rounded border border-slate-900/60">
                            💡 {lightStatus}
                          </div>
                          <h5 className="text-[10px] font-bold text-slate-300 uppercase tracking-widest border-b border-slate-900/60 pb-1.5 flex items-center gap-1.5">
                            🗺️ Interactive Floor Plan (ผังห้องจำลองปฏิบัติราชการเสมือนจริง)
                          </h5>
                          
                          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                            {/* Director Suite (ห้องผู้บริหาร) */}
                            <div className="p-3 bg-slate-950/50 border border-slate-900/70 rounded-2xl relative">
                              <div className="absolute top-1 right-2 text-[7px] uppercase tracking-wider text-slate-600 font-bold">Director Suite</div>
                              <h6 className="text-[9px] font-bold text-gold-500/80 mb-2">👔 สำนักงานผู้อำนวยการ</h6>
                              <div className="grid grid-cols-2 gap-2">
                                {['executive', 'cos'].map(r => renderDesk(r))}
                              </div>
                            </div>

                            {/* Operations & Finance Wing (กลุ่มบริหารบริการและการเงิน) */}
                            <div className="p-3 bg-slate-950/50 border border-slate-900/70 rounded-2xl relative">
                              <div className="absolute top-1 right-2 text-[7px] uppercase tracking-wider text-slate-600 font-bold">Operations & Finance</div>
                              <h6 className="text-[9px] font-bold text-gold-500/80 mb-2">💼 ฝ่ายปฏิบัติการและบริหารการคลัง</h6>
                              <div className="grid grid-cols-2 gap-2">
                                {['coo', 'cfo', 'analyst', 'report', 'meeting'].map(r => renderDesk(r))}
                              </div>
                            </div>

                            {/* Intelligence Suite */}
                            <div className="p-3 bg-slate-950/50 border border-slate-900/70 rounded-2xl relative">
                              <div className="absolute top-1 right-2 text-[7px] uppercase tracking-wider text-slate-600 font-bold">Intelligence Suite</div>
                              <h6 className="text-[9px] font-bold text-gold-500/80 mb-2">🧠 ศูนย์จัดการความรู้และเครือข่ายส่งต่อ</h6>
                              <div className="grid grid-cols-2 gap-2">
                                {['knowledge', 'provincial'].map(r => renderDesk(r))}
                              </div>
                            </div>

                            {/* Data & Cyber Security */}
                            <div className="p-3 bg-slate-950/50 border border-slate-900/70 rounded-2xl relative">
                              <div className="absolute top-1 right-2 text-[7px] uppercase tracking-wider text-slate-600 font-bold">Data & Cyber Security</div>
                              <h6 className="text-[9px] font-bold text-gold-500/80 mb-2">🔒 ฝ่ายสถาปัตยกรรมข้อมูลและความปลอดภัย</h6>
                              <div className="grid grid-cols-2 gap-2">
                                {['datagov', 'db_monitor', 'rag_optimizer', 'security_officer'].map(r => renderDesk(r))}
                              </div>
                            </div>
                          </div>
                        </div>

                        {/* Swappable Brains Selector & Costs */}
                        <div className="p-5 bg-slate-950/40 border border-slate-850 rounded-2xl glass space-y-4">
                          <div className="flex justify-between items-center border-b border-slate-900 pb-2">
                            <h5 className="text-[11px] font-bold text-gold-400 uppercase tracking-widest flex items-center gap-1.5">
                              🧠 Swappable Brains & Token Costs (ระบบจัดสรรสมองผู้ช่วยและงบประมาณ)
                            </h5>
                            <span className="text-[9px] text-slate-500 font-medium">จำลองประมวลผล Token</span>
                          </div>

                          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                            <div className="space-y-1.5 text-left">
                              <label className="text-[10px] text-slate-400">ปรับเปลี่ยนโมเดลสมองประมวลผลสำหรับ: <strong className="text-white">{(selectedAgentRole || "").toUpperCase()}</strong></label>
                              <select
                                value={agentBrains[selectedAgentRole] || "GPT-4o"}
                                onChange={async (e) => {
                                  const newModel = e.target.value;
                                  setAgentBrains(prev => ({ ...prev, [selectedAgentRole]: newModel }));
                                  setMonitorLogs(prev => [
                                    { timestamp: new Date().toLocaleTimeString(), sender: "system", text: `เปลี่ยนโมเดลสมองของ @${selectedAgentRole.toUpperCase()} เป็น ${newModel} สำเร็จ` },
                                    ...prev
                                  ]);
                                  
                                  // ส่งอัปเดตโมเดลในฐานข้อมูลหลังบ้านจริงๆ!
                                  try {
                                    await api.updateAgent(selectedAgentRole, { model_name: newModel });
                                    await fetchAgents(); // reload state
                                  } catch (err) {
                                    console.error("Failed to sync model_name to backend:", err);
                                  }
                                }}
                                className="w-full bg-slate-950 border border-slate-850 focus:border-gold-500/50 rounded-xl px-3 py-2 text-xs text-white outline-none cursor-pointer"
                              >
                                <option value="Claude 3.5 Sonnet">🧠 Claude 3.5 Sonnet (ฉลาดกลยุทธ์)</option>
                                <option value="Gemini 1.5 Pro">🧠 Gemini 1.5 Pro (ประมวลผลขอบเขตกว้าง)</option>
                                <option value="DeepSeek R1">🧠 DeepSeek R1 (คิดวิเคราะห์ตรรกะซับซ้อน)</option>
                                <option value="GPT-4o">🧠 GPT-4o (รวดเร็ว, มาตรฐานสากล)</option>
                              </select>
                            </div>

                            <div className="p-3 bg-slate-900/40 border border-slate-850 rounded-xl flex flex-col justify-between text-left">
                              <span className="text-[9px] text-slate-500 font-semibold uppercase block">งบประมวลผลสะสมในระบบ</span>
                              <strong className="text-base font-bold text-amber-500 block mt-1">
                                ฿{(monitorLogs.length * 0.42 + 25.5).toFixed(2)} บาท
                              </strong>
                              <span className="text-[8px] text-slate-500 block font-light">อิงอัตรา Token จำลองรายตำแหน่ง</span>
                            </div>

                            <div className="p-3 bg-slate-900/40 border border-slate-850 rounded-xl text-[9px] leading-relaxed text-slate-400 space-y-0.5 text-left">
                              <span className="text-slate-500 font-bold block uppercase text-[8px] mb-0.5">โครงสร้างสมองในสำนักงาน</span>
                              <div>• Claude 3.5 Sonnet: <span className="text-slate-200">2 ฝ่ายหลัก</span></div>
                              <div>• Gemini 1.5 Pro: <span className="text-slate-200">3 ฝ่ายยุทธศาสตร์</span></div>
                              <div>• DeepSeek / GPT: <span className="text-slate-200">8 ฝ่ายหลังบ้าน</span></div>
                            </div>
                          </div>
                        </div>

                        {/* AI Small Talk & Backchannel Chat log */}
                        <div className="p-5 bg-slate-955/40 border border-slate-850 rounded-2xl glass space-y-3">
                          <h5 className="text-[11px] font-bold text-gold-400 uppercase tracking-widest border-b border-slate-900 pb-2 flex items-center gap-1.5">
                            💬 AI Small Talk & Backchannel Chat (บทสนทนาจำลองการประสานงานภายใน)
                          </h5>
                          <div className="bg-slate-950 border border-slate-900 rounded-xl p-3.5 space-y-2 max-h-[140px] overflow-y-auto pr-1 text-[11px]">
                            {smallTalkLogs.map((talk, idx) => {
                              const iconMap: any = {
                                cfo: "💰", coo: "🏥", datagov: "🔒", security_officer: "🛡️",
                                analyst: "📊", cos: "📋", knowledge: "📚", report: "✍", provincial: "🗺️", meeting: "🎙️"
                              };
                              const icon = iconMap[talk.sender] || "👤";
                              return (
                                <div key={idx} className="flex gap-2 last:border-b-0 border-b border-slate-900/40 pb-1.5 text-slate-350 leading-relaxed font-light animate-fade-in">
                                  <span className="text-slate-500 font-mono text-[9px]">[{talk.time}]</span>
                                  <strong className="text-slate-300 font-semibold shrink-0">{icon} @{talk.sender.toUpperCase()}:</strong>
                                  <span>{talk.text}</span>
                                </div>
                              );
                            })}
                          </div>
                        </div>
                      </>
                    );
                  })()}

                  {/* Terminal Log Stream & RAG Infrastructure telemetry */}
                  <div className="grid grid-cols-1 md:grid-cols-12 gap-6 pt-2">
                    
                    {/* Log Terminal Screen (8 cols) */}
                    <div className="md:col-span-8 space-y-2.5">
                      <div className="flex justify-between items-center">
                        <span className="text-[10px] uppercase tracking-wider font-bold text-slate-300 flex items-center gap-1.5">
                          💻 Live System Activity Log Stream (ประวัติกิจกรรมเรียลไทม์)
                        </span>
                        <button 
                          onClick={() => setMonitorLogs([])}
                          className="text-[9px] text-slate-500 hover:text-slate-300 font-medium"
                        >
                          ล้างหน้าต่าง Log
                        </button>
                      </div>

                      <div className="bg-slate-955 border border-slate-850 rounded-2xl p-4 font-mono text-[10px] leading-relaxed text-slate-350 min-h-[220px] max-h-[260px] overflow-y-auto space-y-2 custom-scrollbar relative text-left shadow-inner">
                        <div className="absolute top-2 right-3 text-[8px] text-slate-600 bg-slate-900 px-2 py-0.5 rounded border border-slate-850">
                          AUTO-SCROLLING
                        </div>
                        {monitorLogs.length === 0 ? (
                          <div className="text-slate-600 text-center py-12">ไม่มีล็อกใหม่เกิดขึ้น รอการประมวลผลอัตโนมัติถัดไป...</div>
                        ) : (
                          monitorLogs.map((log, i) => (
                            <div key={i} className="border-b border-slate-900/60 pb-1.5 last:border-b-0 animate-fade-in flex items-start gap-2.5">
                              <span className="text-slate-500 font-light shrink-0">[{log.timestamp}]</span>
                              <span className="text-gold-500 font-bold shrink-0">@{log.sender.toUpperCase()}</span>
                              <span className="text-slate-300 font-light leading-relaxed">{log.text}</span>
                            </div>
                          ))
                        )}
                      </div>
                    </div>

                    {/* Data / Infrastructure Status (4 cols) */}
                    <div className="md:col-span-4 space-y-4">
                      <span className="text-[10px] uppercase tracking-wider font-bold text-slate-300 block">
                        ⚙️ Infrastructure Status (สถานะระบบวิศวกรรม)
                      </span>

                      <div className="p-4 bg-slate-950/60 border border-slate-850 rounded-2xl glass space-y-3">
                        <div className="space-y-1">
                          <div className="flex justify-between text-[10px]">
                            <span className="text-slate-400">RAG Vector DB (3072D)</span>
                            <span className="text-emerald-400 font-bold">OPTIMIZED</span>
                          </div>
                          <div className="w-full bg-slate-900 h-1.5 rounded-full overflow-hidden border border-slate-850">
                            <div className="h-full bg-emerald-500 rounded-full" style={{ width: '92%' }}></div>
                          </div>
                          <span className="text-[8px] text-slate-500 block">ดัชนีพร้อมใช้: 28,450 chunks | มิติเวกเตอร์: 3,072</span>
                        </div>

                        <div className="space-y-1 pt-1">
                          <div className="flex justify-between text-[10px]">
                            <span className="text-slate-400">SQLite Uptime</span>
                            <span className="text-emerald-400 font-bold">99.98%</span>
                          </div>
                          <div className="w-full bg-slate-900 h-1.5 rounded-full overflow-hidden border border-slate-850">
                            <div className="h-full bg-emerald-500 rounded-full" style={{ width: '99%' }}></div>
                          </div>
                          <span className="text-[8px] text-slate-500 block">ทราฟฟิกเฉลี่ย: 12 qps | Query Latency: 42ms</span>
                        </div>

                        <div className="space-y-1 pt-1">
                          <div className="flex justify-between text-[10px]">
                            <span className="text-slate-400">PDPA Compliance Status</span>
                            <span className="text-emerald-400 font-bold">100% SECURE</span>
                          </div>
                          <div className="w-full bg-slate-900 h-1.5 rounded-full overflow-hidden border border-slate-850">
                            <div className="h-full bg-emerald-500 rounded-full" style={{ width: '100%' }}></div>
                          </div>
                          <span className="text-[8px] text-slate-500 block">ตรวจสอบสิทธิ์ EHR: 1,402 ครั้ง (ไม่มีการรั่วไหล)</span>
                        </div>
                      </div>
                    </div>

                  </div>

                  {/* Selected Job Description Detail panel */}
                  {selectedAgentRole && roleDb[selectedAgentRole] && (
                    <div className="p-4 bg-slate-900/60 border border-slate-850 rounded-2xl text-left space-y-2 animate-fade-in">
                      <div className="flex justify-between items-center border-b border-slate-950 pb-2">
                        <span className="text-xs font-bold text-gold-400">📋 Job Description: {roleDb[selectedAgentRole].name}</span>
                        <span className="text-[10px] text-slate-400 font-medium">สังกัด: {roleDb[selectedAgentRole].department}</span>
                      </div>
                      <div className="text-[11px] leading-relaxed text-slate-300 font-light space-y-2">
                        <p><strong>บทบาทภารกิจ (Routine Role):</strong> {roleDb[selectedAgentRole].title}</p>
                        <p><strong>แผนการดำเนินงานแบบอัตโนมัติ (SOP Plans):</strong></p>
                        <ul className="list-disc pl-4 space-y-1">
                          {roleDb[selectedAgentRole].plans.map((p: string, idx: number) => (
                            <li key={idx}>{p}</li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  )}

                </div>
              )}

              {/* Tab 5: Master Orchestrator (Command Center) */}              {/* Tab 5: Master Orchestrator (Command Center) */}
              {activeWorkspaceTab === 'orchestrator' && (
                <div className="p-6 space-y-6 flex-1 overflow-y-auto max-h-[550px] text-left">
                  
                  {/* Blocked state if Emergency Stop is active */}
                  {emergencyActive ? (
                    <div className="p-8 bg-red-950/40 border border-red-800 rounded-3xl text-center space-y-4 animate-fade-in">
                      <span className="text-4xl block">🚨</span>
                      <h4 className="text-base font-bold text-red-400">ระบบปัญญาประดิษฐ์ถูกระงับการสั่งการชั่วคราว (AI Office Suspended)</h4>
                      <p className="text-xs text-slate-400 max-w-md mx-auto leading-relaxed font-light">
                        ทีมผู้ช่วยปัญญาประดิษฐ์ทั้งหมดได้รับการระงับตามโปรโตคอล Emergency Stop เพื่อป้องกันช่องโหว่ความมั่นคงข้อมูลและการบุกรุกความมั่นคงทางไซเบอร์
                      </p>
                      <button
                        onClick={handleReactivateSystem}
                        className="px-5 py-2.5 bg-emerald-600 hover:bg-emerald-500 text-slate-950 font-bold rounded-xl text-xs transition-all active:scale-[0.98]"
                      >
                        🟢 ปลดล็อกโปรโตคอลและกู้ระบบ AI
                      </button>
                    </div>
                  ) : (
                    <>
                      {/* Strategic Goal Goal-Centric Command */}
                      <div className="p-5 bg-slate-955/40 border border-slate-850 rounded-2xl space-y-3.5">
                        <div className="flex justify-between items-center border-b border-slate-900 pb-2">
                          <h4 className="text-xs font-bold text-gold-400 uppercase tracking-wider flex items-center gap-1.5">
                            ⚡ สั่งการเป้าหมายระดับยุทธศาสตร์องค์กร (Goal-Centric Command)
                          </h4>
                          <span className="text-[9px] text-slate-500 font-medium">Orchestrator-Worker Pattern</span>
                        </div>

                        <div className="space-y-2">
                          <label className="text-[10px] text-slate-400">ระบุเป้าหมายระดับสูงของคุณ:</label>
                          <textarea
                            rows={3}
                            value={goalInput}
                            onChange={(e) => setGoalInput(e.target.value)}
                            placeholder="ระบุเป้าหมายงาน เช่น วิเคราะห์ความเสี่ยงการคลังและหนี้สินร่วมกับการสืบคู่มือพัสดุและให้เขียนเล่มรายงานข้อสั่งการ..."
                            className="w-full bg-slate-950 border border-slate-850 focus:border-gold-500/50 rounded-xl px-4 py-2.5 text-xs text-white outline-none resize-none font-light leading-relaxed"
                          />
                        </div>

                        {/* Quick Targets / Presets */}
                        <div className="flex flex-wrap gap-2 pt-1 text-[10px] items-center">
                          <span className="text-slate-500 font-medium">เป้าหมายแนะนำ:</span>
                          <button
                            onClick={() => setGoalInput('วิเคราะห์สาเหตุคิวล้นแผนกผู้ป่วยนอก (OPD) พร้อมตรวจสอบมาตรฐาน SOP การแพทย์ทางไกล และเสนอแนวทางร่างหนังสือสั่งการเพื่อแก้ปัญหาระยะยาว')}
                            className="px-2.5 py-1 bg-slate-900 border border-slate-800 hover:border-gold-500 text-slate-350 rounded-lg transition-all text-left"
                          >
                            🚨 แก้คิว OPD ล้น
                          </button>
                          <button
                            onClick={() => setGoalInput('ประเมินความเสี่ยงทางการคลังและอัตราเบิกจ่ายงบประมาณที่ล่าช้า ในฝ่ายการคลังโรงพยาบาล ตรวจสอบระเบียบกรมบัญชีกลางและจัดสร้างเล่มรายงาน')}
                            className="px-2.5 py-1 bg-slate-900 border border-slate-800 hover:border-gold-500 text-slate-350 rounded-lg transition-all text-left"
                          >
                            💰 เร่งด่วนจัดซื้อ & การคลัง
                          </button>
                        </div>

                        <div className="flex justify-end pt-2">
                          <button
                            onClick={handleRunOrchestrator}
                            disabled={orchestrationLoading || !goalInput.trim()}
                            className="px-5 py-2.5 bg-gradient-to-r from-gold-600 to-amber-700 hover:from-gold-500 hover:to-amber-600 disabled:opacity-40 text-slate-950 font-bold rounded-xl text-xs transition-all shadow-md active:scale-[0.98] flex items-center gap-1.5"
                          >
                            {orchestrationLoading ? (
                              <>
                                <div className="w-3.5 h-3.5 border-2 border-slate-955 border-t-transparent rounded-full animate-spin"></div>
                                <span>กำลังประสานวิเคราะห์ข้ามฝ่าย...</span>
                              </>
                            ) : (
                              <>⚡ เริ่มการประสานงานข้ามฝ่าย</>
                            )}
                          </button>
                        </div>
                      </div>

                      {/* Orchestrator Kanban Board */}
                      {orchestrationResult && (
                        <div className="space-y-6 animate-fade-in">
                          <h4 className="text-xs font-bold text-slate-300 uppercase tracking-widest border-b border-slate-900 pb-2">
                            📋 แดชบอร์ดติดตามงาน Command Center (Kanban-Style)
                          </h4>

                          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                            {/* Column 1: Tasks Decomposed */}
                            <div className="p-4 bg-slate-955/40 border border-slate-850 rounded-2xl space-y-3">
                              <h5 className="text-[10px] font-bold text-gold-500 uppercase tracking-wider border-b border-slate-900 pb-1.5 flex justify-between items-center">
                                <span>1. แตกงานย่อย (Queued)</span>
                                <span className="px-1.5 py-0.2 bg-slate-900 text-[8px] text-slate-400 rounded">3 Tasks</span>
                              </h5>
                              <div className="space-y-2.5 max-h-[220px] overflow-y-auto pr-1">
                                {orchestrationResult.tasks?.map((task: any, idx: number) => (
                                  <div key={idx} className="p-2.5 bg-slate-900/60 border border-slate-850 rounded-xl text-left text-[11px] relative overflow-hidden">
                                    <span className="absolute top-0 right-0 px-1.5 py-0.2 bg-gold-950/60 border-l border-b border-gold-900 text-[8px] text-gold-400 rounded-bl font-semibold uppercase">
                                      {task.assigned_to}
                                    </span>
                                    <p className="font-bold text-white">ขั้นที่ {task.step}</p>
                                    <p className="text-slate-450 font-light mt-1 text-[10px] leading-relaxed">{task.instruction}</p>
                                  </div>
                                ))}
                              </div>
                            </div>

                            {/* Column 2: Agent Processing */}
                            <div className="p-4 bg-slate-955/40 border border-slate-850 rounded-2xl space-y-3">
                              <h5 className="text-[10px] font-bold text-emerald-500 uppercase tracking-wider border-b border-slate-900 pb-1.5 flex justify-between items-center">
                                <span>2. ประมวลผล (In Progress)</span>
                                <span className="px-1.5 py-0.2 bg-emerald-955/40 text-[8px] border border-emerald-900 text-emerald-400 rounded">Done</span>
                              </h5>
                              <div className="space-y-2.5 max-h-[220px] overflow-y-auto pr-1">
                                {orchestrationResult.results?.map((res: any, idx: number) => (
                                  <div key={idx} className="p-2.5 bg-slate-900/60 border border-emerald-900/30 rounded-xl text-left text-[11px] flex justify-between items-center">
                                    <div>
                                      <span className="font-bold text-emerald-400 block">{res.agent_name}</span>
                                      <span className="text-[9px] text-slate-500 font-light">รันงานขั้นที่ {res.step} สำเร็จ</span>
                                    </div>
                                    <span className="text-[10px] text-emerald-500">✓ เสร็จสิ้น</span>
                                  </div>
                                ))}
                              </div>
                            </div>

                            {/* Column 3: Outputs & Data Lineage */}
                            <div className="p-4 bg-slate-955/40 border border-slate-850 rounded-2xl space-y-3">
                              <h5 className="text-[10px] font-bold text-slate-305 uppercase tracking-wider border-b border-slate-900 pb-1.5 flex justify-between items-center">
                                <span>3. วิเคราะห์ความถูกต้อง (Needs Review)</span>
                                <span className="px-1.5 py-0.2 bg-slate-900 text-[8px] text-slate-400 rounded">Lineage</span>
                              </h5>
                              <div className="space-y-2.5 max-h-[220px] overflow-y-auto pr-1">
                                {orchestrationResult.results?.map((res: any, idx: number) => (
                                  <div key={idx} className="p-2.5 bg-slate-900/60 border border-slate-855 rounded-xl text-left text-[11px]">
                                    <span className="font-bold text-white block truncate">{res.agent_name} Report</span>
                                    <p className="text-slate-450 text-[10px] font-light mt-0.5 line-clamp-2">{res.result}</p>
                                    
                                    <button
                                      onClick={() => setLineageTarget(lineageTarget === `task-${res.step}` ? null : `task-${res.step}`)}
                                      className="text-[9px] text-gold-500 hover:text-gold-400 font-bold block mt-1.5"
                                    >
                                      📂 {lineageTarget === `task-${res.step}` ? 'ซ่อนการโยงเส้น' : 'ดูที่มาข้อมูล (Data Lineage)'}
                                    </button>

                                    {lineageTarget === `task-${res.step}` && (
                                      <div className="mt-2 p-2 bg-slate-955 border border-gold-500/20 rounded-lg text-[9px] text-slate-300 leading-relaxed font-light animate-slide-down">
                                        <p className="font-bold text-gold-400 mb-0.5">Lineage Source:</p>
                                        {res.assigned_to === 'analyst' && <p>• อิงเกณฑ์ Balanced Scorecard กระทรวงสาธารณสุข หมวด 3 ตัวชี้วัดระบบส่งต่อจังหวัด</p>}
                                        {res.assigned_to === 'knowledge' && <p>• สืบค้นคู่มือ SOP รหัส SOP-REF-03: ระเบียบจัดการเตียงว่างและการประสาน คปสอ.</p>}
                                        {res.assigned_to === 'report' && <p>• อ้างอิงข้อเขียนโดยใช้สำนวนจดหมายราชการตราครุฑ หมวดหนังสือสั่งการจังหวัด</p>}
                                        <p>• ตารางระบบ: <code className="text-amber-500">twins_agent_log_id: {idx + 101}</code></p>
                                      </div>
                                    )}
                                  </div>
                                ))}
                              </div>
                            </div>
                          </div>

                          {/* Final synthesis report card */}
                          <div className="p-6 bg-gradient-to-br from-slate-900 to-slate-955 border border-gold-500/30 rounded-3xl relative overflow-hidden shadow-2xl space-y-4">
                            <div className="absolute top-0 right-0 w-32 h-32 bg-gold-500/5 rounded-full blur-3xl"></div>
                            
                            <div className="flex justify-between items-center border-b border-slate-800 pb-3">
                              <div>
                                <span className="text-[9px] uppercase tracking-widest text-gold-500 font-bold">Executive Brain Summary</span>
                                <h5 className="text-sm font-bold text-white mt-1">📝 สรุปรายงานยุทธศาสตร์สุดท้าย (Human-in-the-Loop)</h5>
                              </div>
                              <span className="text-[10px] text-slate-400 bg-slate-955 px-2.5 py-0.5 rounded-full border border-slate-850">สไตล์: ทางการ, เน้นตัวเลข</span>
                            </div>

                            <div className="prose prose-invert prose-xs max-h-[350px] overflow-y-auto pr-1.5 text-xs leading-relaxed text-slate-300 font-light whitespace-pre-wrap select-text text-left">
                              {orchestrationResult.final_report}
                            </div>

                            <div className="flex justify-end gap-3 pt-3 border-t border-slate-900">
                              <button
                                onClick={() => {
                                  alert('✓ รายงานได้รับการอนุมัติและลงนามอิเล็กทรอนิกส์ เสนอเข้าสู่ระบบแฟ้มสั่งการจังหวัดสำเร็จ!');
                                  setLetterSubject(`ข้อสั่งการเรื่อง: ${orchestrationResult.goal}`);
                                  setLetterDetail(orchestrationResult.final_report);
                                  setActiveWorkspaceTab('draft');
                                }}
                                className="px-4 py-2 bg-gradient-to-r from-gold-600 to-amber-700 hover:from-gold-500 hover:to-amber-600 text-slate-950 font-bold rounded-xl text-xs transition-all active:scale-[0.98]"
                              >
                                ✍ ลงนามอนุมัติ (Approve)
                              </button>
                            </div>
                          </div>
                        </div>
                      )}
                    </>
                  )}

                </div>
              )}

            </div>

          </div>

        </div>
      )}
    </div>
  );
}
