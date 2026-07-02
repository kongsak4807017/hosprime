import { useState, useEffect, useRef } from 'react';
import { Check, X, Shield } from 'lucide-react';
import { api, DocumentResponse } from '../../lib/api';

interface AdminTabProps {
  onApproved: () => void;
}

export function AdminTab({ onApproved }: AdminTabProps) {
  // Main Sub-Tab State
  const [activeSubTab, setActiveSubTab] = useState<'docs' | 'twins' | 'agent'>('docs');

  // ==========================================
  // Tab 1: Documents Review & Migration States
  // ==========================================
  const [pendingDocs, setPendingDocs] = useState<DocumentResponse[]>([]);
  const [loading, setLoading] = useState(false);
  const [selectedDoc, setSelectedDoc] = useState<DocumentResponse | null>(null);
  
  // Metadata fields
  const [title, setTitle] = useState("");
  const [docType, setDocType] = useState("");
  const [dept, setDept] = useState("");
  const [prog, setProg] = useState("");
  const [year, setYear] = useState("");
  const [owner, setOwner] = useState("");

  // One-Click Migration States
  const [dbMigration, setDbMigration] = useState(true);
  const [postgresUrl, setPostgresUrl] = useState("postgresql://postgres:postgres@localhost:5432/hosprime");
  const [graphMigration, setGraphMigration] = useState(true);
  const [neo4jUri, setNeo4jUri] = useState("bolt://localhost:7687");
  const [neo4jUser, setNeo4jUser] = useState("neo4j");
  const [neo4jPassword, setNeo4jPassword] = useState("");
  
  const [migrating, setMigrating] = useState(false);
  const [migrationResult, setMigrationResult] = useState<any>(null);
  const [migrationError, setMigrationError] = useState<string | null>(null);

  // ==========================================
  // Tab 2: Executive Twin CRUD States
  // ==========================================
  const [activeCrud, setActiveCrud] = useState<'person' | 'role' | 'org'>('person');
  const [orgs, setOrgs] = useState<any[]>([]);
  const [roles, setRoles] = useState<any[]>([]);
  const [persons, setPersons] = useState<any[]>([]);
  const [loadingTwins, setLoadingTwins] = useState(false);

  // Org Form
  const [newOrgName, setNewOrgName] = useState("");
  const [newOrgDesc, setNewOrgDesc] = useState("");
  const [creatingOrg, setCreatingOrg] = useState(false);

  // Role Form
  const [newRoleTitle, setNewRoleTitle] = useState("");
  const [newRoleOrgId, setNewRoleOrgId] = useState<number | "">("");
  const [creatingRole, setCreatingRole] = useState(false);

  // Person Form
  const [newPersonName, setNewPersonName] = useState("");
  const [newPersonEmail, setNewPersonEmail] = useState("");
  const [newPersonRoleIds, setNewPersonRoleIds] = useState<number[]>([]);
  const [creatingPerson, setCreatingPerson] = useState(false);

  // ==========================================
  // Tab 3: AI Agent Admin States
  // ==========================================
  const [agentSummary, setAgentSummary] = useState<any>(null);
  const [loadingSummary, setLoadingSummary] = useState(false);
  const [adminChatInput, setAdminChatInput] = useState("");
  const [adminChatLogs, setAdminChatLogs] = useState<{ role: 'user' | 'assistant', text: string }[]>([]);
  const [adminChatLoading, setAdminChatLoading] = useState(false);
  
  const adminChatEndRef = useRef<HTMLDivElement>(null);

  // ==========================================
  // Loaders & Fetchers
  // ==========================================
  const fetchPending = async () => {
    setLoading(true);
    try {
      const data = await api.getPendingDocuments();
      setPendingDocs(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const fetchTwinsData = async () => {
    setLoadingTwins(true);
    try {
      const orgData = await api.getOrganizations();
      const roleData = await api.getRoles();
      const personData = await api.getPersons();
      setOrgs(orgData);
      setRoles(roleData);
      setPersons(personData);
    } catch (e) {
      console.error("Error fetching twins CRUD data:", e);
    } finally {
      setLoadingTwins(false);
    }
  };

  const fetchAgentSummary = async () => {
    setLoadingSummary(true);
    try {
      const data = await api.getAdminAgentSummary();
      setAgentSummary(data);
    } catch (e) {
      console.error("Error fetching agent summary:", e);
    } finally {
      setLoadingSummary(false);
    }
  };

  useEffect(() => {
    fetchPending();
    fetchTwinsData();
  }, []);

  useEffect(() => {
    if (activeSubTab === 'agent') {
      fetchAgentSummary();
    }
  }, [activeSubTab]);

  useEffect(() => {
    if (adminChatEndRef.current) {
      adminChatEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [adminChatLogs]);

  // ==========================================
  // Tab 1 Event Handlers
  // ==========================================
  const handleSelectDoc = (doc: DocumentResponse) => {
    setSelectedDoc(doc);
    setTitle(doc.title);
    setDocType(doc.document_type || "Report");
    setDept(doc.department || "");
    setProg(doc.program || "General");
    setYear(doc.year || "");
    setOwner(doc.owner || "");
  };

  const handleAction = async (action: 'approve' | 'reject') => {
    if (!selectedDoc) return;
    try {
      const meta = action === 'approve' ? {
        title,
        document_type: docType,
        department: dept,
        program: prog,
        year,
        owner
      } : undefined;

      await api.reviewDocument(selectedDoc.id, action, meta);
      alert(action === 'approve' ? "อนุมัติข้อมูลเอกสารเข้าระบบ RAG สำเร็จ" : "ปฏิเสธเอกสารเรียบร้อย");
      setSelectedDoc(null);
      fetchPending();
      onApproved();
    } catch (e) {
      alert("ล้มเหลวในการตรวจทานเอกสาร");
    }
  };

  const handleMigrateSubmit = async () => {
    if (!confirm("คุณแน่ใจหรือไม่ที่จะเริ่มขั้นตอนการย้ายข้อมูลระบบ? \n* ขั้นตอนนี้จะสร้างตารางและเขียนทับข้อมูลในฐานข้อมูลปลายทาง")) return;
    
    setMigrating(true);
    setMigrationError(null);
    setMigrationResult(null);
    
    try {
      const result = await api.migrateSystem({
        db_migration: dbMigration,
        postgres_url: dbMigration ? postgresUrl : undefined,
        graph_migration: graphMigration,
        neo4j_uri: graphMigration ? neo4jUri : undefined,
        neo4j_user: graphMigration ? neo4jUser : undefined,
        neo4j_password: graphMigration ? neo4jPassword : undefined,
      });
      setMigrationResult(result);
    } catch (e: any) {
      setMigrationError(e.message || "เกิดข้อผิดพลาดขัดข้องในการรันขั้นตอน Migration");
    } finally {
      setMigrating(false);
    }
  };

  // ==========================================
  // Tab 2 Event Handlers
  // ==========================================
  const handleCreateOrg = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newOrgName.trim()) return;
    setCreatingOrg(true);
    try {
      await api.createOrganization({ name: newOrgName, description: newOrgDesc });
      setNewOrgName("");
      setNewOrgDesc("");
      await fetchTwinsData();
      alert("สร้างองค์กรสำเร็จ");
    } catch (e: any) {
      alert(e.message || "ล้มเหลวในการสร้างองค์กร");
    } finally {
      setCreatingOrg(false);
    }
  };

  const handleDeleteOrg = async (id: number) => {
    if (!confirm("คุณแน่ใจที่จะลบองค์กรนี้? การลบนี้อาจส่งผลต่อบทบาทที่ผูกอยู่")) return;
    try {
      await api.deleteOrganization(id);
      await fetchTwinsData();
      alert("ลบองค์กรสำเร็จ");
    } catch (e: any) {
      alert(e.message || "ล้มเหลวในการลบองค์กร");
    }
  };

  const handleCreateRole = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newRoleTitle.trim() || newRoleOrgId === "") {
      alert("กรุณากรอกชื่อบทบาทและเลือกองค์กร");
      return;
    }
    setCreatingRole(true);
    try {
      await api.createRole({ title: newRoleTitle, organization_id: Number(newRoleOrgId) });
      setNewRoleTitle("");
      setNewRoleOrgId("");
      await fetchTwinsData();
      alert("สร้างบทบาทสำเร็จ");
    } catch (e: any) {
      alert(e.message || "ล้มเหลวในการสร้างบทบาท");
    } finally {
      setCreatingRole(false);
    }
  };

  const handleDeleteRole = async (id: number) => {
    if (!confirm("คุณแน่ใจที่จะลบบทบาทนี้?")) return;
    try {
      await api.deleteRole(id);
      await fetchTwinsData();
      alert("ลบบทบาทสำเร็จ");
    } catch (e: any) {
      alert(e.message || "ล้มเหลวในการลบบทบาท");
    }
  };

  const handleCreatePerson = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newPersonName.trim()) {
      alert("กรุณากรอกชื่อบุคคล");
      return;
    }
    setCreatingPerson(true);
    try {
      await api.createPerson({
        full_name: newPersonName,
        email: newPersonEmail || undefined,
        role_ids: newPersonRoleIds.length > 0 ? newPersonRoleIds : undefined
      });
      setNewPersonName("");
      setNewPersonEmail("");
      setNewPersonRoleIds([]);
      await fetchTwinsData();
      alert("ลงทะเบียนบุคคลสำเร็จ");
    } catch (e: any) {
      alert(e.message || "ล้มเหลวในการลงทะเบียนบุคคล");
    } finally {
      setCreatingPerson(false);
    }
  };

  const handleDeletePerson = async (id: number) => {
    if (!confirm("คุณแน่ใจที่จะลบบุคคลนี้?")) return;
    try {
      await api.deletePerson(id);
      await fetchTwinsData();
      alert("ลบบุคคลสำเร็จ");
    } catch (e: any) {
      alert(e.message || "ล้มเหลวในการลบบุคคล");
    }
  };

  const handleToggleRoleSelection = (roleId: number) => {
    setNewPersonRoleIds(prev => 
      prev.includes(roleId) ? prev.filter(id => id !== roleId) : [...prev, roleId]
    );
  };

  // ==========================================
  // Tab 3 Event Handlers
  // ==========================================
  const handleAskAdminAgent = async () => {
    if (!adminChatInput.trim()) return;
    const question = adminChatInput;
    setAdminChatInput("");
    setAdminChatLoading(true);
    
    setAdminChatLogs(prev => [...prev, { role: 'user', text: question }]);
    
    try {
      const token = localStorage.getItem('hosprime_token');
      const headers: Record<string, string> = { 'Content-Type': 'application/json' };
      if (token) headers['Authorization'] = `Bearer ${token}`;
      
      const res = await fetch(`${((import.meta as any).env?.VITE_API_BASE_URL) || 'http://localhost:8000/api'}/twins/consult`, {
        method: 'POST',
        headers,
        body: JSON.stringify({ agent_id: 'admin', question })
      });
      
      if (!res.ok) throw new Error('การโต้ตอบกับ AI Admin ล้มเหลว');
      const data = await res.json();
      setAdminChatLogs(prev => [...prev, { role: 'assistant', text: data.response }]);
    } catch (e: any) {
      setAdminChatLogs(prev => [...prev, { role: 'assistant', text: `เกิดข้อผิดพลาดในการวิเคราะห์: ${e.message}` }]);
    } finally {
      setAdminChatLoading(false);
    }
  };

  // Organizations map to resolve organization name in Role list
  const orgMap = orgs.reduce((acc, curr) => {
    acc[curr.id] = curr.name;
    return acc;
  }, {} as Record<number, string>);

  return (
    <div className="max-w-6xl mx-auto space-y-6 text-white text-left">
      {/* Header */}
      <div>
        <h2 className="text-2xl font-bold tracking-tight font-outfit text-transparent bg-clip-text bg-gradient-to-r from-white via-slate-100 to-gold-400">
          ⚙️ แผงควบคุมระบบจัดการ (Admin Panel)
        </h2>
        <p className="text-slate-400 text-xs mt-1">
          ระบบอนุมัติเอกสารความรู้ RAG, จัดการโครงสร้างฝาแฝดผู้บริหาร (Twin CRUD) และประมวลผลความมั่นคงระบบด้วย AI Agent Admin
        </p>
      </div>

      {/* Main Switcher Navigation */}
      <div className="flex bg-slate-950/80 p-1 rounded-2xl border border-slate-900 w-fit">
        <button
          onClick={() => setActiveSubTab('docs')}
          className={`px-5 py-2.5 text-xs font-semibold rounded-xl transition-all ${
            activeSubTab === 'docs'
              ? 'bg-slate-900 text-gold-400 border border-slate-800'
              : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          🔍 ตรวจทาน RAG & ย้ายระบบ
        </button>
        <button
          onClick={() => {
            setActiveSubTab('twins');
            fetchTwinsData();
          }}
          className={`px-5 py-2.5 text-xs font-semibold rounded-xl transition-all ${
            activeSubTab === 'twins'
              ? 'bg-slate-900 text-gold-400 border border-slate-800'
              : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          👥 จัดการฝาแฝด Twin (CRUD)
        </button>
        <button
          onClick={() => setActiveSubTab('agent')}
          className={`px-5 py-2.5 text-xs font-semibold rounded-xl transition-all ${
            activeSubTab === 'agent'
              ? 'bg-slate-900 text-gold-400 border border-slate-800'
              : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          🤖 ผู้ช่วยแอดมิน AI (AI Agent Admin)
        </button>
      </div>

      {/* ======================================================== */}
      {/* SUBTAB 1: Documents Review & One-Click Migration (docs)  */}
      {/* ======================================================== */}
      {activeSubTab === 'docs' && (
        <div className="space-y-8 animate-fade-in">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 items-start">
            {/* Pending List */}
            <div className="lg:col-span-1 bg-slate-950/40 border border-slate-850 p-6 rounded-2xl space-y-4">
              <h3 className="text-xs font-bold text-slate-350 uppercase tracking-wider border-b border-slate-900 pb-2 flex justify-between">
                <span>รายการรอนุมัติ ({pendingDocs.length})</span>
                <button onClick={fetchPending} className="text-gold-500 text-[10px]">🔄 ดึงใหม่</button>
              </h3>
              <div className="space-y-2.5 max-h-[350px] overflow-y-auto pr-1">
                {pendingDocs.map((doc) => (
                  <button
                    key={doc.id}
                    onClick={() => handleSelectDoc(doc)}
                    className={`w-full p-4 rounded-xl text-left border transition-all duration-150 ${
                      selectedDoc?.id === doc.id 
                        ? 'bg-slate-900 border-gold-500/50' 
                        : 'bg-slate-950/60 border-slate-900 hover:bg-slate-900/40'
                    }`}
                  >
                    <p className="text-xs font-semibold text-white truncate">{doc.title}</p>
                    <div className="flex items-center justify-between text-[10px] text-slate-500 mt-2">
                      <span>โปรแกรม: {doc.program || 'N/A'}</span>
                      <span>ปี: {doc.year || 'N/A'}</span>
                    </div>
                  </button>
                ))}
                {pendingDocs.length === 0 && !loading && (
                  <p className="text-xs text-slate-500 text-center py-8">ไม่มีเอกสารรอการอนุมัติเข้าระบบ RAG</p>
                )}
              </div>
            </div>

            {/* Metadata Editor */}
            <div className="lg:col-span-2">
              {selectedDoc ? (
                <div className="bg-slate-900/20 border border-slate-850 glass p-8 rounded-2xl space-y-6 animate-fade-in">
                  <div className="flex justify-between items-start border-b border-slate-900 pb-4">
                    <div>
                      <h3 className="text-sm font-bold text-white">แก้ไขข้อมูลเมตาดาตาประกอบการอนุมัติ</h3>
                      <p className="text-[10px] text-slate-500 mt-1">ไฟล์ดั้งเดิม: {selectedDoc.file_path.split(/[\\/]/).pop()}</p>
                    </div>
                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => handleAction('approve')}
                        className="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-slate-950 rounded-xl text-xs font-semibold flex items-center gap-1.5 transition-all shadow"
                      >
                        <Check className="w-3.5 h-3.5" /> อนุมัติ (Approve)
                      </button>
                      <button
                        onClick={() => handleAction('reject')}
                        className="px-4 py-2 bg-rose-700 hover:bg-rose-600 text-white rounded-xl text-xs font-semibold flex items-center gap-1.5 transition-all shadow"
                      >
                        <X className="w-3.5 h-3.5" /> ปฏิเสธ (Reject)
                      </button>
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="space-y-2 col-span-2">
                      <label className="text-[11px] text-slate-400 font-medium">ชื่อเรื่อง (ดึงอัตโนมัติ)</label>
                      <input
                        type="text"
                        value={title}
                        onChange={(e) => setTitle(e.target.value)}
                        className="w-full bg-slate-950 border border-slate-850 focus:border-gold-500/50 rounded-xl px-4 py-2.5 text-xs text-white outline-none"
                      />
                    </div>

                    <div className="space-y-2">
                      <label className="text-[11px] text-slate-400 font-medium">ประเภทเอกสาร</label>
                      <select
                        value={docType}
                        onChange={(e) => setDocType(e.target.value)}
                        className="w-full bg-slate-950 border border-slate-850 focus:border-gold-500/50 rounded-xl px-4 py-2.5 text-xs text-white outline-none"
                      >
                        <option value="Policy">Policy (นโยบาย/ประกาศ)</option>
                        <option value="SOP">SOP (คู่มือปฏิบัติการ/แนวทาง)</option>
                        <option value="Meeting Notes">Meeting Notes (บันทึกประชุม)</option>
                        <option value="Report">Report (รายงานสรุปผล)</option>
                      </select>
                    </div>

                    <div className="space-y-2">
                      <label className="text-[11px] text-slate-400 font-medium">แผนก/กลุ่มงานที่เกี่ยวข้อง</label>
                      <input
                        type="text"
                        value={dept}
                        onChange={(e) => setDept(e.target.value)}
                        placeholder="เช่น กลุ่มงานควบคุมโรคติดต่อ"
                        className="w-full bg-slate-950 border border-slate-850 focus:border-gold-500/50 rounded-xl px-4 py-2.5 text-xs text-white outline-none"
                      />
                    </div>

                    <div className="space-y-2">
                      <label className="text-[11px] text-slate-400 font-medium">แฟ้มงาน/โปรแกรมงาน</label>
                      <select
                        value={prog}
                        onChange={(e) => setProg(e.target.value)}
                        className="w-full bg-slate-950 border border-slate-850 focus:border-gold-500/50 rounded-xl px-4 py-2.5 text-xs text-white outline-none"
                      >
                        <option value="PM2.5">PM2.5</option>
                        <option value="TB">TB (วัณโรค)</option>
                        <option value="NCD">NCD (เบาหวาน/ความดัน)</option>
                        <option value="Disaster">Disaster (ภัยพิบัติ/น้ำท่วม)</option>
                        <option value="Digital Health">Digital Health</option>
                        <option value="General">General (ทั่วไป)</option>
                      </select>
                    </div>

                    <div className="space-y-2">
                      <label className="text-[11px] text-slate-400 font-medium">ปีงบประมาณ</label>
                      <input
                        type="text"
                        value={year}
                        onChange={(e) => setYear(e.target.value)}
                        placeholder="เช่น 2569"
                        className="w-full bg-slate-950 border border-slate-850 focus:border-gold-500/50 rounded-xl px-4 py-2.5 text-xs text-white outline-none font-mono"
                      />
                    </div>

                    <div className="space-y-2 col-span-2">
                      <label className="text-[11px] text-slate-400 font-medium">ผู้จัดทำ/เจ้าของนโยบาย</label>
                      <input
                        type="text"
                        value={owner}
                        onChange={(e) => setOwner(e.target.value)}
                        placeholder="เช่น สสจ.เชียงราย"
                        className="w-full bg-slate-950 border border-slate-850 focus:border-gold-500/50 rounded-xl px-4 py-2.5 text-xs text-white outline-none"
                      />
                    </div>
                  </div>
                </div>
              ) : (
                <div className="bg-slate-950/20 border border-slate-850 glass p-12 rounded-2xl flex flex-col items-center justify-center text-center text-slate-500 min-h-[300px]">
                  <Shield className="w-10 h-10 text-slate-700 mb-4 animate-pulse" />
                  <p className="text-xs max-w-sm">กรุณาเลือกเอกสารที่เพิ่มเข้ามาจากด้านซ้าย เพื่อทำการตรวจสอบ แก้ไขความถูกต้องของเมตาดาตา และอนุมัติข้อมูลสกัดลง RAG</p>
                </div>
              )}
            </div>
          </div>

          {/* One-Click Migration Block */}
          <div className="bg-slate-900/20 border border-slate-850 glass p-8 rounded-2xl space-y-6">
            <div className="border-b border-slate-900 pb-4 flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-gold-600 to-amber-700 flex items-center justify-center text-slate-950 text-lg shadow-lg">
                🚀
              </div>
              <div>
                <h3 className="text-sm font-bold text-white font-outfit">ระบบย้ายฐานข้อมูลในคลิกเดียว (One-Click Migration)</h3>
                <p className="text-slate-400 text-[11px]">ย้ายข้อมูลจาก SQLite ไปยัง PostgreSQL หรือ Neo4j จริงเมื่อพร้อมขึ้นระบบการทำงานเครือข่าย Intranet</p>
              </div>
            </div>

            {migrationError && (
              <div className="p-4 bg-rose-950/30 border border-rose-800/40 rounded-xl text-rose-300 text-xs">
                ⚠️ {migrationError}
              </div>
            )}

            {migrationResult && (
              <div className="p-5 bg-emerald-950/20 border border-emerald-800/30 rounded-2xl text-xs space-y-3">
                <h4 className="font-bold text-emerald-400 flex items-center gap-1.5">
                  <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
                  การโยกย้ายข้อมูลระบบเสร็จสิ้นลุล่วง! (Migration Success)
                </h4>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-slate-350 leading-relaxed font-light">
                  {migrationResult.db_migration && migrationResult.db_migration.status === "success" && (
                    <div className="space-y-1.5 p-3 bg-slate-950/60 border border-slate-850 rounded-xl">
                      <p className="font-bold text-slate-200">📊 ฐานข้อมูล SQL (PostgreSQL):</p>
                      <p className="text-[10px] text-slate-400">{migrationResult.db_migration.message}</p>
                      <div className="mt-2 grid grid-cols-2 gap-2 text-[9px] font-mono text-slate-450 bg-slate-950 p-2 rounded">
                        {Object.entries(migrationResult.db_migration.summary || {}).map(([tbl, count]: any) => (
                          <div key={tbl} className="flex justify-between">
                            <span className="truncate">{tbl}:</span>
                            <span className="text-gold-400 font-bold">{count} rows</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                  {migrationResult.graph_migration && migrationResult.graph_migration.status === "success" && (
                    <div className="space-y-1.5 p-3 bg-slate-950/60 border border-slate-850 rounded-xl">
                      <p className="font-bold text-slate-200">🕸️ ความสัมพันธ์แบบกราฟ (Neo4j):</p>
                      <p className="text-[10px] text-slate-400">{migrationResult.graph_migration.message}</p>
                      <ul className="mt-2 text-[10px] text-slate-400 pl-4 list-disc space-y-0.5">
                        <li>นำเข้าโหนด: <strong className="text-gold-500">{migrationResult.graph_migration.nodes_processed} โหนด</strong></li>
                        <li>ความสัมพันธ์ที่สร้าง: <strong className="text-emerald-500">{migrationResult.graph_migration.relationships_created} รายการ</strong></li>
                      </ul>
                    </div>
                  )}
                </div>
              </div>
            )}

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-3 p-5 bg-slate-950/30 border border-slate-850 rounded-2xl">
                <div className="flex items-center gap-2">
                  <input 
                    type="checkbox" 
                    id="dbMigration"
                    checked={dbMigration}
                    onChange={(e) => setDbMigration(e.target.checked)}
                    className="rounded border-slate-700 bg-slate-900 text-gold-500 focus:ring-0 cursor-pointer"
                  />
                  <label htmlFor="dbMigration" className="text-xs font-bold text-slate-200 cursor-pointer">ย้ายโครงสร้างหลัก (SQLite ➔ PostgreSQL)</label>
                </div>
                {dbMigration && (
                  <div className="space-y-1.5 animate-slide-down">
                    <label className="text-[10px] text-slate-500 block">PostgreSQL Connection URL ปลายทาง</label>
                    <input 
                      type="text" 
                      value={postgresUrl}
                      onChange={(e) => setPostgresUrl(e.target.value)}
                      className="w-full bg-slate-955 border border-slate-850 focus:border-gold-500/50 rounded-xl px-3 py-2 text-xs text-slate-200 font-mono"
                    />
                  </div>
                )}
              </div>

              <div className="space-y-3 p-5 bg-slate-950/30 border border-slate-850 rounded-2xl">
                <div className="flex items-center gap-2">
                  <input 
                    type="checkbox" 
                    id="graphMigration"
                    checked={graphMigration}
                    onChange={(e) => setGraphMigration(e.target.checked)}
                    className="rounded border-slate-700 bg-slate-900 text-gold-500 focus:ring-0 cursor-pointer"
                  />
                  <label htmlFor="graphMigration" className="text-xs font-bold text-slate-200 cursor-pointer">ย้ายโครงข่ายระบบความสัมพันธ์ (SQL ➔ Neo4j Graph DB)</label>
                </div>
                {graphMigration && (
                  <div className="space-y-2.5 animate-slide-down">
                    <div className="space-y-1">
                      <label className="text-[10px] text-slate-500 block">Neo4j Connection URI</label>
                      <input 
                        type="text" 
                        value={neo4jUri}
                        onChange={(e) => setNeo4jUri(e.target.value)}
                        className="w-full bg-slate-955 border border-slate-850 focus:border-gold-500/50 rounded-xl px-3 py-2 text-xs text-slate-200 font-mono"
                      />
                    </div>
                    <div className="grid grid-cols-2 gap-3">
                      <div>
                        <label className="text-[10px] text-slate-500 block">Username</label>
                        <input 
                          type="text" 
                          value={neo4jUser}
                          onChange={(e) => setNeo4jUser(e.target.value)}
                          className="w-full bg-slate-955 border border-slate-850 focus:border-gold-500/50 rounded-xl px-3 py-2 text-xs text-slate-250"
                        />
                      </div>
                      <div>
                        <label className="text-[10px] text-slate-500 block">Password</label>
                        <input 
                          type="password" 
                          value={neo4jPassword}
                          onChange={(e) => setNeo4jPassword(e.target.value)}
                          className="w-full bg-slate-955 border border-slate-850 focus:border-gold-500/50 rounded-xl px-3 py-2 text-xs text-slate-250"
                        />
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </div>

            <button
              onClick={handleMigrateSubmit}
              disabled={migrating || (!dbMigration && !graphMigration)}
              className="w-full py-3 bg-gradient-to-r from-gold-600 to-amber-700 hover:from-gold-500 hover:to-amber-600 text-slate-950 rounded-2xl text-xs font-bold tracking-wider uppercase transition-all shadow-lg active:scale-[0.99] disabled:opacity-40"
            >
              {migrating ? '🚀 กำลังรันขั้นตอนระบบ Migration... กรุณารอสักครู่...' : '🚀 เริ่มต้นรันขั้นตอน Migration ทันที'}
            </button>
          </div>
        </div>
      )}

      {/* ======================================================== */}
      {/* SUBTAB 2: Executive Twin Management CRUD (twins)         */}
      {/* ======================================================== */}
      {activeSubTab === 'twins' && (
        <div className="space-y-6 animate-fade-in">
          
          {/* Sub-sub-tabs selection */}
          <div className="flex bg-slate-950/40 p-1 rounded-xl border border-slate-900 w-fit shrink-0">
            <button
              onClick={() => setActiveCrud('person')}
              className={`px-4 py-1.5 text-xs font-semibold rounded-lg transition-all ${
                activeCrud === 'person' ? 'bg-slate-900 text-gold-400 border border-slate-800' : 'text-slate-450 hover:text-slate-250'
              }`}
            >
              👥 จัดการบุคคล/ผู้ใช้ (Persons)
            </button>
            <button
              onClick={() => setActiveCrud('role')}
              className={`px-4 py-1.5 text-xs font-semibold rounded-lg transition-all ${
                activeCrud === 'role' ? 'bg-slate-900 text-gold-400 border border-slate-800' : 'text-slate-450 hover:text-slate-250'
              }`}
            >
              👑 จัดการบทบาท (Roles)
            </button>
            <button
              onClick={() => setActiveCrud('org')}
              className={`px-4 py-1.5 text-xs font-semibold rounded-lg transition-all ${
                activeCrud === 'org' ? 'bg-slate-900 text-gold-400 border border-slate-800' : 'text-slate-450 hover:text-slate-250'
              }`}
            >
              🏢 จัดการองค์กร (Organizations)
            </button>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
            
            {/* Left Col: CRUD Forms */}
            <div className="lg:col-span-5 bg-slate-900/20 border border-slate-850 p-6 rounded-2xl glass">
              
              {/* Person CRUD Form */}
              {activeCrud === 'person' && (
                <form onSubmit={handleCreatePerson} className="space-y-4">
                  <div>
                    <h3 className="text-xs font-bold text-gold-400 uppercase tracking-wider">👥 ลงทะเบียนบุคลากร/หัวหน้ากลุ่มงาน</h3>
                    <p className="text-[10px] text-slate-500 mt-1">เพิ่มประวัติบุคคลเพื่อนำไปผูกโยงกับบทบาททวินผู้บริหารหลักของกระทรวง</p>
                  </div>
                  
                  <div className="space-y-3 text-xs">
                    <div>
                      <label className="block text-[11px] text-slate-400 mb-1">ชื่อ-นามสกุลจริง (Full Name) *</label>
                      <input
                        type="text"
                        value={newPersonName}
                        onChange={(e) => setNewPersonName(e.target.value)}
                        placeholder="เช่น นพ.สมยศ สัตยามงคล"
                        required
                        className="w-full bg-slate-950 border border-slate-850 focus:border-gold-500/50 rounded-xl px-4 py-2.5 text-white outline-none"
                      />
                    </div>
                    <div>
                      <label className="block text-[11px] text-slate-400 mb-1">ที่อยู่อีเมล (Email Address)</label>
                      <input
                        type="email"
                        value={newPersonEmail}
                        onChange={(e) => setNewPersonEmail(e.target.value)}
                        placeholder="somyot.s@moph.mail.go.th"
                        className="w-full bg-slate-950 border border-slate-850 focus:border-gold-500/50 rounded-xl px-4 py-2.5 text-white outline-none font-mono"
                      />
                    </div>
                    <div>
                      <label className="block text-[11px] text-slate-400 mb-1">ผูกบทบาท/ตำแหน่งงานที่เปิดใช้งานในระบบ</label>
                      {roles.length > 0 ? (
                        <div className="p-3 bg-slate-950/80 border border-slate-850 rounded-xl max-h-[140px] overflow-y-auto space-y-2">
                          {roles.map((r) => (
                            <label key={r.id} className="flex items-center gap-2 cursor-pointer text-[11px] text-slate-350">
                              <input
                                type="checkbox"
                                checked={newPersonRoleIds.includes(r.id)}
                                onChange={() => handleToggleRoleSelection(r.id)}
                                className="rounded border-slate-800 bg-slate-900 text-gold-500 focus:ring-0"
                              />
                              <span>{r.title} ({orgMap[r.organization_id] || `Org #${r.organization_id}`})</span>
                            </label>
                          ))}
                        </div>
                      ) : (
                        <p className="text-[10px] text-slate-500 italic p-2 bg-slate-950/40 border border-slate-900 rounded-xl">ยังไม่มีบทบาทเปิดใช้งานในระบบขณะนี้ กรุณาไปสร้างบทบาทก่อน</p>
                      )}
                    </div>
                  </div>

                  <button
                    type="submit"
                    disabled={creatingPerson}
                    className="w-full py-2.5 bg-gold-600 hover:bg-gold-500 text-slate-950 rounded-xl text-xs font-semibold shadow transition-all mt-2"
                  >
                    {creatingPerson ? 'กำลังบันทึก...' : '＋ ลงทะเบียนบุคลากรใหม่'}
                  </button>
                </form>
              )}

              {/* Role CRUD Form */}
              {activeCrud === 'role' && (
                <form onSubmit={handleCreateRole} className="space-y-4">
                  <div>
                    <h3 className="text-xs font-bold text-gold-400 uppercase tracking-wider">👑 สร้างบทบาทฝาแฝด (Role Twin)</h3>
                    <p className="text-[10px] text-slate-500 mt-1">สร้างกรอบตำแหน่งรับผิดชอบสำหรับการสั่งการเชิงกลยุทธ์ RAG</p>
                  </div>
                  
                  <div className="space-y-3 text-xs">
                    <div>
                      <label className="block text-[11px] text-slate-400 mb-1">ชื่อตำแหน่ง/บทบาท (Role Title) *</label>
                      <input
                        type="text"
                        value={newRoleTitle}
                        onChange={(e) => setNewRoleTitle(e.target.value)}
                        placeholder="เช่น หัวหน้ากลุ่มงานควบคุมโรคติดต่อ (CDC Chief)"
                        required
                        className="w-full bg-slate-950 border border-slate-850 focus:border-gold-500/50 rounded-xl px-4 py-2.5 text-white outline-none"
                      />
                    </div>
                    <div>
                      <label className="block text-[11px] text-slate-400 mb-1">สังกัดกระทรวง/องค์กรย่อย *</label>
                      {orgs.length > 0 ? (
                        <select
                          value={newRoleOrgId}
                          onChange={(e) => setNewRoleOrgId(e.target.value === "" ? "" : Number(e.target.value))}
                          required
                          className="w-full bg-slate-950 border border-slate-850 focus:border-gold-500/50 rounded-xl px-4 py-2.5 text-white outline-none"
                        >
                          <option value="">-- กรุณาเลือกองค์กรสังกัด --</option>
                          {orgs.map((o) => (
                            <option key={o.id} value={o.id}>{o.name}</option>
                          ))}
                        </select>
                      ) : (
                        <p className="text-[10px] text-rose-400 italic bg-rose-950/20 p-2 border border-rose-900/40 rounded-xl">ยังไม่ได้สร้างองค์กร กรุณาไปเพิ่มเมนูองค์กรก่อนสร้างบทบาทครับ</p>
                      )}
                    </div>
                  </div>

                  <button
                    type="submit"
                    disabled={creatingRole || orgs.length === 0}
                    className="w-full py-2.5 bg-gold-600 hover:bg-gold-500 text-slate-950 rounded-xl text-xs font-semibold shadow transition-all mt-2"
                  >
                    {creatingRole ? 'กำลังบันทึก...' : '＋ สร้างบทบาทตำแหน่งงาน'}
                  </button>
                </form>
              )}

              {/* Organization CRUD Form */}
              {activeCrud === 'org' && (
                <form onSubmit={handleCreateOrg} className="space-y-4">
                  <div>
                    <h3 className="text-xs font-bold text-gold-400 uppercase tracking-wider">🏢 ทะเบียนองค์กร/กระทรวงสาธารณสุข</h3>
                    <p className="text-[10px] text-slate-500 mt-1">ลงทะเบียนหน่วยงานสาธารณสุขระดับกอง/กลุ่มงานภายในจังหวัด</p>
                  </div>
                  
                  <div className="space-y-3 text-xs">
                    <div>
                      <label className="block text-[11px] text-slate-400 mb-1">ชื่อหน่วยงาน (Organization Name) *</label>
                      <input
                        type="text"
                        value={newOrgName}
                        onChange={(e) => setNewOrgName(e.target.value)}
                        placeholder="เช่น สำนักงานสาธารณสุขจังหวัดเชียงราย (สสจ.เชียงราย)"
                        required
                        className="w-full bg-slate-950 border border-slate-850 focus:border-gold-500/50 rounded-xl px-4 py-2.5 text-white outline-none"
                      />
                    </div>
                    <div>
                      <label className="block text-[11px] text-slate-400 mb-1">คำอธิบาย/ภารกิจหลัก (Description)</label>
                      <textarea
                        rows={3}
                        value={newOrgDesc}
                        onChange={(e) => setNewOrgDesc(e.target.value)}
                        placeholder="เช่น รับผิดชอบบริหารระบบหลักประกันสุขภาพ ควบคุมโรคระบาด และจัดระบบการแพทย์ในระดับจังหวัดเชียงราย"
                        className="w-full bg-slate-955 border border-slate-850 focus:border-gold-500/50 rounded-xl px-4 py-2 text-white outline-none resize-none font-light"
                      />
                    </div>
                  </div>

                  <button
                    type="submit"
                    disabled={creatingOrg}
                    className="w-full py-2.5 bg-gold-600 hover:bg-gold-500 text-slate-950 rounded-xl text-xs font-semibold shadow transition-all mt-2"
                  >
                    {creatingOrg ? 'กำลังบันทึก...' : '＋ ลงทะเบียนหน่วยงาน'}
                  </button>
                </form>
              )}

            </div>

            {/* Right Col: CRUD Table/List */}
            <div className="lg:col-span-7 bg-slate-950/40 border border-slate-850 p-6 rounded-2xl space-y-4">
              <div className="flex justify-between items-center pb-2 border-b border-slate-900">
                <h3 className="text-xs font-bold text-slate-350 uppercase tracking-wider">
                  {activeCrud === 'person' && `รายการบุคลากรทั้งหมดในระบบ (${persons.length})`}
                  {activeCrud === 'role' && `รายการบทบาทฝาแฝดผู้บริหาร (${roles.length})`}
                  {activeCrud === 'org' && `รายการหน่วยงานจดทะเบียน (${orgs.length})`}
                </h3>
                <button 
                  onClick={fetchTwinsData} 
                  disabled={loadingTwins}
                  className="text-[10px] text-gold-500 hover:text-gold-400"
                >
                  {loadingTwins ? 'กำลังรีเฟรช...' : '🔄 รีเฟรชข้อมูล'}
                </button>
              </div>

              <div className="max-h-[380px] overflow-y-auto pr-1">
                {loadingTwins ? (
                  <div className="py-12 text-center text-xs text-slate-500">กำลังดึงข้อมูลระบบ Twin...</div>
                ) : (
                  <>
                    {/* Persons List */}
                    {activeCrud === 'person' && (
                      <div className="space-y-2.5">
                        {persons.map((p) => (
                          <div key={p.id} className="p-4 bg-slate-900/40 border border-slate-900 rounded-xl flex justify-between items-center gap-4 text-xs">
                            <div className="text-left space-y-1">
                              <p className="font-bold text-white text-xs">{p.full_name}</p>
                              <p className="text-[10px] text-slate-550 font-mono">{p.email || 'ไม่มีอีเมล'}</p>
                              {p.roles && p.roles.length > 0 ? (
                                <div className="flex flex-wrap gap-1 mt-1.5">
                                  {p.roles.map((r: any) => (
                                    <span key={r.id} className="text-[8px] bg-gold-950/50 border border-gold-900 text-gold-400 px-2 py-0.5 rounded font-mono">
                                      {r.title}
                                    </span>
                                  ))}
                                </div>
                              ) : (
                                <span className="text-[8px] bg-slate-950 text-slate-500 px-2 py-0.5 rounded italic">ไม่ได้ผูกบทบาททวิน</span>
                              )}
                            </div>
                            <button
                              onClick={() => handleDeletePerson(p.id)}
                              className="px-2.5 py-1.5 bg-rose-950/20 hover:bg-rose-900/30 border border-rose-900/40 rounded-lg text-[10px] text-rose-300 font-semibold transition-all"
                            >
                              ลบออก
                            </button>
                          </div>
                        ))}
                        {persons.length === 0 && (
                          <p className="text-xs text-slate-500 text-center py-8">ไม่มีข้อมูลบุคลากรในระบบ</p>
                        )}
                      </div>
                    )}

                    {/* Roles List */}
                    {activeCrud === 'role' && (
                      <div className="space-y-2.5">
                        {roles.map((r) => (
                          <div key={r.id} className="p-4 bg-slate-900/40 border border-slate-900 rounded-xl flex justify-between items-center gap-4 text-xs">
                            <div className="text-left space-y-1">
                              <p className="font-bold text-white text-xs">{r.title}</p>
                              <p className="text-[10px] text-slate-500">
                                สังกัด: <strong className="text-slate-350">{orgMap[r.organization_id] || `Organization #${r.organization_id}`}</strong>
                              </p>
                            </div>
                            <button
                              onClick={() => handleDeleteRole(r.id)}
                              className="px-2.5 py-1.5 bg-rose-950/20 hover:bg-rose-900/30 border border-rose-900/40 rounded-lg text-[10px] text-rose-300 font-semibold transition-all"
                            >
                              ลบออก
                            </button>
                          </div>
                        ))}
                        {roles.length === 0 && (
                          <p className="text-xs text-slate-500 text-center py-8">ไม่มีข้อมูลบทบาทในระบบ</p>
                        )}
                      </div>
                    )}

                    {/* Organizations List */}
                    {activeCrud === 'org' && (
                      <div className="space-y-2.5">
                        {orgs.map((o) => (
                          <div key={o.id} className="p-4 bg-slate-900/40 border border-slate-900 rounded-xl flex justify-between items-center gap-4 text-xs">
                            <div className="text-left space-y-1 max-w-[80%]">
                              <p className="font-bold text-white text-xs">{o.name}</p>
                              <p className="text-[10px] text-slate-400 font-light leading-relaxed truncate">{o.description || 'ไม่มีคำอธิบายภารกิจ'}</p>
                            </div>
                            <button
                              onClick={() => handleDeleteOrg(o.id)}
                              className="px-2.5 py-1.5 bg-rose-950/20 hover:bg-rose-900/30 border border-rose-900/40 rounded-lg text-[10px] text-rose-300 font-semibold transition-all"
                            >
                              ลบออก
                            </button>
                          </div>
                        ))}
                        {orgs.length === 0 && (
                          <p className="text-xs text-slate-500 text-center py-8">ไม่มีข้อมูลหน่วยงานในระบบ</p>
                        )}
                      </div>
                    )}
                  </>
                )}
              </div>
            </div>

          </div>
        </div>
      )}

      {/* ======================================================== */}
      {/* SUBTAB 3: AI Agent Admin Console (agent)                */}
      {/* ======================================================== */}
      {activeSubTab === 'agent' && (
        <div className="space-y-6 animate-fade-in">
          
          {/* Summary Stat Cards */}
          {agentSummary ? (
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="p-4 bg-slate-950/40 border border-slate-900 rounded-2xl text-left space-y-1.5 relative overflow-hidden">
                <div className="absolute top-0 right-0 p-3 text-xl opacity-20">📁</div>
                <p className="text-[10px] text-slate-500 uppercase tracking-widest font-semibold">เอกสาร RAG</p>
                <p className="text-xl font-bold font-outfit text-white">
                  {agentSummary.stats.rag.total_documents} <span className="text-[10px] text-slate-400 font-normal">ฉบับ</span>
                </p>
                <div className="flex gap-2 text-[9px] text-slate-450 font-light">
                  <span className="text-emerald-500 font-semibold">✓ {agentSummary.stats.rag.processed} อนุมัติ</span>
                  <span className="text-amber-500 font-semibold">⏱️ {agentSummary.stats.rag.pending_review} รอตรวจ</span>
                </div>
              </div>

              <div className="p-4 bg-slate-950/40 border border-slate-900 rounded-2xl text-left space-y-1.5 relative overflow-hidden">
                <div className="absolute top-0 right-0 p-3 text-xl opacity-20">👑</div>
                <p className="text-[10px] text-slate-500 uppercase tracking-widest font-semibold">บทบาททวิน</p>
                <p className="text-xl font-bold font-outfit text-white">
                  {agentSummary.stats.twins.total_roles} <span className="text-[10px] text-slate-400 font-normal">ตำแหน่ง</span>
                </p>
                <p className="text-[9px] text-slate-400">ผูกองค์กรอยู่ {agentSummary.stats.twins.total_organizations} แห่ง</p>
              </div>

              <div className="p-4 bg-slate-950/40 border border-slate-900 rounded-2xl text-left space-y-1.5 relative overflow-hidden">
                <div className="absolute top-0 right-0 p-3 text-xl opacity-20">👥</div>
                <p className="text-[10px] text-slate-500 uppercase tracking-widest font-semibold">ผู้ใช้งาน / Twins</p>
                <p className="text-xl font-bold font-outfit text-white">
                  {agentSummary.stats.twins.total_persons} <span className="text-[10px] text-slate-400 font-normal">บุคคล</span>
                </p>
                <p className="text-[9px] text-slate-400">เข้าถาม RAG แล้ว {agentSummary.stats.rag.total_queries} ครั้ง</p>
              </div>

              <div className="p-4 bg-slate-950/40 border border-slate-900 rounded-2xl text-left space-y-1.5 relative overflow-hidden">
                <div className="absolute top-0 right-0 p-3 text-xl opacity-20">🔄</div>
                <p className="text-[10px] text-slate-500 uppercase tracking-widest font-semibold">กระบวนงานสั่งการ</p>
                <p className="text-xl font-bold font-outfit text-white">
                  {agentSummary.stats.workflows.total_workflow_runs} <span className="text-[10px] text-slate-400 font-normal">เวิร์กโฟลว์</span>
                </p>
                <p className="text-[9px] text-emerald-400 font-semibold">ระบบพร้อมใช้งาน Intranet 100%</p>
              </div>
            </div>
          ) : (
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 animate-pulse">
              {[...Array(4)].map((_, i) => (
                <div key={i} className="h-20 bg-slate-950/40 border border-slate-900 rounded-2xl"></div>
              ))}
            </div>
          )}

          {/* AI Report & Chat console */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
            
            {/* AI Report panel */}
            <div className="lg:col-span-7 bg-slate-900/20 border border-slate-850 p-6 rounded-3xl glass flex flex-col text-left space-y-4">
              <div className="flex items-center gap-2 pb-3 border-b border-slate-850">
                <span className="text-lg">🤖</span>
                <div>
                  <h4 className="text-xs font-bold text-white uppercase tracking-wider">รายงานประเมินความปลอดภัย & ประสิทธิภาพสารสนเทศ</h4>
                  <p className="text-[9px] text-slate-500">ประมวลผลวิเคราะห์เรียลไทม์โดย AI Agent Admin</p>
                </div>
              </div>

              {loadingSummary ? (
                <div className="py-20 text-center text-xs text-slate-500 animate-pulse">
                  ⌛ กำลังรวบรวมสถิติระบบและให้ AI สรุปรายงานความมั่นคง...
                </div>
              ) : agentSummary ? (
                <div className="text-xs leading-relaxed text-slate-300 font-light whitespace-pre-wrap max-h-[400px] overflow-y-auto pr-1">
                  {agentSummary.ai_summary}
                </div>
              ) : (
                <p className="text-xs text-slate-500 text-center py-8">ไม่สามารถดึงข้อมูลรายงาน AI Admin ได้</p>
              )}
            </div>

            {/* Consultation Chat widget */}
            <div className="lg:col-span-5 bg-slate-950/40 border border-slate-850 rounded-3xl overflow-hidden flex flex-col h-[460px]">
              <div className="p-4 bg-slate-950 border-b border-slate-900 text-left shrink-0">
                <h4 className="text-xs font-bold text-gold-400">💬 ปรึกษางานกับ AI Agent Admin</h4>
                <p className="text-[9px] text-slate-500 mt-0.5">สอบถามแนวทางการจัดการความรู้ นโยบาย หรือความเสี่ยงระบบสารสนเทศ</p>
              </div>

              {/* Message history */}
              <div className="flex-1 p-4 overflow-y-auto space-y-3.5 max-h-[340px]">
                <div className="flex gap-2">
                  <div className="w-6 h-6 rounded-full bg-gold-950 border border-gold-900 flex items-center justify-center text-[10px]">🤖</div>
                  <div className="p-3 bg-slate-900/80 border border-slate-850 rounded-xl rounded-tl-none text-[11px] font-light leading-relaxed max-w-[85%] text-left">
                    สวัสดีครับ ผมคือ AI Agent Admin ประจำแพลตฟอร์ม HosPrime ยินดีให้คำแนะนำการจัดการระบบสารสนเทศ วิเคราะห์คุณภาพเอกสาร RAG หรือประเมินประสิทธิภาพโครงสร้างทวินครับ
                  </div>
                </div>

                {adminChatLogs.map((msg, idx) => {
                  const isUser = msg.role === 'user';
                  return (
                    <div key={idx} className={`flex gap-2 ${isUser ? 'justify-end' : 'justify-start'}`}>
                      {!isUser && (
                        <div className="w-6 h-6 rounded-full bg-gold-950 border border-gold-900 flex items-center justify-center text-[10px] shrink-0">🤖</div>
                      )}
                      <div className={`p-3 rounded-xl text-[11px] leading-relaxed max-w-[85%] font-light whitespace-pre-wrap ${
                        isUser 
                          ? 'bg-gradient-to-r from-gold-600 to-amber-700 text-slate-950 font-medium rounded-tr-none' 
                          : 'bg-slate-900/80 border border-slate-850 text-slate-200 rounded-tl-none'
                      }`}>
                        {msg.text}
                      </div>
                      {isUser && (
                        <div className="w-6 h-6 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center text-[9px] font-bold shrink-0">ME</div>
                      )}
                    </div>
                  );
                })}

                {adminChatLoading && (
                  <div className="flex gap-2 animate-pulse">
                    <div className="w-6 h-6 rounded-full bg-gold-950 border border-gold-900 flex items-center justify-center text-[10px]">⌛</div>
                    <div className="p-3 bg-slate-900/60 border border-slate-850 rounded-xl rounded-tl-none text-[11px] text-slate-500">
                      กำลังประมวลผลกลยุทธ์ระบบ...
                    </div>
                  </div>
                )}
                
                <div ref={adminChatEndRef} />
              </div>

              {/* Chat Input */}
              <div className="p-3 bg-slate-950/80 border-t border-slate-900 flex gap-2 shrink-0">
                <input
                  type="text"
                  value={adminChatInput}
                  onChange={(e) => setAdminChatInput(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter') handleAskAdminAgent();
                  }}
                  placeholder="พิมพ์ข้อความปรึกษาผู้ดูแลระบบ AI..."
                  disabled={adminChatLoading}
                  className="flex-1 bg-slate-900 border border-slate-850 rounded-lg px-3.5 py-2 text-xs text-white placeholder-slate-650 focus:outline-none focus:border-gold-500/50"
                />
                <button
                  onClick={handleAskAdminAgent}
                  disabled={adminChatLoading || !adminChatInput.trim()}
                  className="px-4 py-2 bg-gold-600 hover:bg-gold-500 text-slate-950 text-xs font-semibold rounded-lg shrink-0 transition-all"
                >
                  ส่ง
                </button>
              </div>
            </div>

          </div>
        </div>
      )}
    </div>
  );
}
