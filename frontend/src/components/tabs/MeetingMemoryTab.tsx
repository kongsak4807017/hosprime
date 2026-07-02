import { useState, useEffect, useRef } from 'react';
import { api } from '../../lib/api';

export function MeetingMemoryTab() {
  const [loading, setLoading] = useState(false);
  const [meetings, setMeetings] = useState<any[]>([]);
  const [selectedMeeting, setSelectedMeeting] = useState<any>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  // Audio Upload Form State
  const [showAddMeeting, setShowAddMeeting] = useState(false);
  const [audioTitle, setAudioTitle] = useState('');
  const [audioFile, setAudioFile] = useState<File | null>(null);
  const [uploadingAudio, setUploadingAudio] = useState(false);

  // Document Upload State
  const [docFile, setDocFile] = useState<File | null>(null);
  const [uploadingDoc, setUploadingDoc] = useState(false);

  // Chat State
  const [chatInput, setChatInput] = useState('');
  const [chatLogs, setChatLogs] = useState<Record<number, { role: 'user' | 'assistant', text: string }[]>>({});
  const [chatLoading, setChatLoading] = useState(false);

  // Sub-tab state for selected meeting workspace
  const [workspaceTab, setWorkspaceTab] = useState<'summary' | 'chat'>('summary');
  
  const chatEndRef = useRef<HTMLDivElement>(null);

  const fetchMeetings = async () => {
    setLoading(true);
    setErrorMessage(null);
    try {
      const data = await api.getMeetings();
      if (Array.isArray(data)) {
        setMeetings(data);
        // Sync selected meeting details if already selected
        if (selectedMeeting) {
          const updated = data.find((m: any) => m.id === selectedMeeting.id);
          if (updated) setSelectedMeeting(updated);
        }
      }
    } catch (e) {
      setErrorMessage("ไม่สามารถเชื่อมต่อ API ประวัติประชุมได้ กรุณาเปิดรัน Backend Server");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMeetings();
  }, []);

  useEffect(() => {
    // Scroll chat to bottom when log updates
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [chatLogs, selectedMeeting, workspaceTab]);

  const extractAttachedDocs = (transcript: string | null) => {
    if (!transcript) return [];
    const regex = /\[เอกสารแนบประกอบการประชุม: ([^\]]+)\]/g;
    const docs = [];
    let match;
    while ((match = regex.exec(transcript)) !== null) {
      docs.push(match[1]);
    }
    return docs;
  };

  const handleUploadAudio = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!audioFile || !audioTitle.trim()) {
      alert('กรุณากรอกชื่อหัวข้อประชุมและเลือกไฟล์เสียง');
      return;
    }
    setUploadingAudio(true);
    try {
      const formData = new FormData();
      formData.append('file', audioFile);
      formData.append('title', audioTitle);
      
      const token = localStorage.getItem('hosprime_token');
      const headers: Record<string, string> = {};
      if (token) headers['Authorization'] = `Bearer ${token}`;

      const res = await fetch(`${((import.meta as any).env?.VITE_API_BASE_URL) || 'http://localhost:8000/api'}/meetings/upload-audio`, {
        method: 'POST',
        headers,
        body: formData
      });
      
      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || 'เกิดข้อผิดพลาดในการวิเคราะห์ไฟล์เสียงประชุม');
      }

      setAudioFile(null);
      setAudioTitle('');
      setShowAddMeeting(false);
      await fetchMeetings();
      alert('อัปโหลดไฟล์เสียงและถอดความสรุปมติลง SQLite เรียบร้อยแล้ว!');
    } catch (err: any) {
      alert(err.message || 'เกิดข้อผิดพลาดในการเชื่อมต่อ');
    } finally {
      setUploadingAudio(false);
    }
  };

  const handleUploadDoc = async () => {
    if (!selectedMeeting || !docFile) return;
    setUploadingDoc(true);
    try {
      await api.uploadMeetingDocument(selectedMeeting.id, docFile);
      setDocFile(null);
      
      // Refresh data
      await fetchMeetings();
      
      alert('อัปโหลดและสกัดเนื้อหาเอกสารแนบประมวลผล RAG สำเร็จ!');
    } catch (err: any) {
      alert(err.message || 'ไม่สามารถอัปโหลดเอกสารประกอบได้');
    } finally {
      setUploadingDoc(false);
    }
  };

  const handleAskMeeting = async () => {
    if (!selectedMeeting || !chatInput.trim()) return;
    const meetingId = selectedMeeting.id;
    const userMsg = chatInput;
    setChatInput('');
    setChatLoading(true);

    const currentLogs = chatLogs[meetingId] || [];
    setChatLogs({
      ...chatLogs,
      [meetingId]: [...currentLogs, { role: 'user', text: userMsg }]
    });

    try {
      const res = await api.askMeetingOracle(meetingId, userMsg);
      setChatLogs(prev => ({
        ...prev,
        [meetingId]: [...(prev[meetingId] || []), { role: 'assistant', text: res.response }]
      }));
    } catch (err: any) {
      setChatLogs(prev => ({
        ...prev,
        [meetingId]: [...(prev[meetingId] || []), { role: 'assistant', text: `ขออภัย เกิดข้อผิดพลาด RAG: ${err.message}` }]
      }));
    } finally {
      setChatLoading(false);
    }
  };

  const selectedAttachedDocs = selectedMeeting ? extractAttachedDocs(selectedMeeting.transcript) : [];
  const currentChatLogs = selectedMeeting ? (chatLogs[selectedMeeting.id] || []) : [];

  return (
    <div className="max-w-7xl mx-auto space-y-6 animate-fade-in text-white">
      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h2 className="text-2xl font-bold tracking-tight font-outfit text-transparent bg-clip-text bg-gradient-to-r from-white via-slate-100 to-gold-400">
            🎙️ ความทรงจำที่ประชุม (Meeting Memory)
          </h2>
          <p className="text-slate-400 text-xs mt-1">
            เครื่องมือสกัดเสียงบันทึกการประชุม สรุปมติ ติดตามสั่งงาน และแนบเอกสารเพื่อคุยวิเคราะห์ RAG เฉพาะบริบทการประชุมสไตล์ NotebookLM
          </p>
        </div>
        <button
          onClick={() => setShowAddMeeting(!showAddMeeting)}
          className="px-4 py-2 bg-gradient-to-r from-gold-600 to-amber-700 hover:from-gold-500 hover:to-amber-600 border border-gold-500/20 text-xs font-semibold rounded-xl transition-all shadow-lg flex items-center gap-2"
        >
          {showAddMeeting ? '✕ ปิดฟอร์ม' : '＋ บันทึกประชุมใหม่ (ไฟล์เสียง)'}
        </button>
      </div>

      {/* Error Message */}
      {errorMessage && (
        <div className="p-4 bg-rose-950/30 border border-rose-800/40 rounded-2xl text-rose-300 text-xs">
          ⚠️ {errorMessage}
        </div>
      )}

      {/* Audio Upload Form panel */}
      {showAddMeeting && (
        <form onSubmit={handleUploadAudio} className="p-6 border border-slate-800 rounded-2xl bg-slate-900/40 glass space-y-4 max-w-xl animate-slide-down">
          <h3 className="text-sm font-semibold text-gold-400">📝 อัปโหลดไฟล์บันทึกเสียงประชุม สสจ.</h3>
          <div className="space-y-3">
            <div>
              <label className="block text-[11px] text-slate-400 mb-1">หัวข้อ/ชื่อบันทึกประชุม</label>
              <input
                type="text"
                value={audioTitle}
                onChange={(e) => setAudioTitle(e.target.value)}
                placeholder="เช่น การประชุมคณะกรรมการ PHEOC ครั้งที่ 3/2569"
                required
                className="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-xs text-white placeholder-slate-600 focus:outline-none focus:border-gold-500/50"
              />
            </div>
            <div>
              <label className="block text-[11px] text-slate-400 mb-1">ไฟล์เสียงบันทึก (MP3, WAV, M4A)</label>
              <input
                type="file"
                accept="audio/*"
                onChange={(e) => setAudioFile(e.target.files?.[0] || null)}
                required
                className="w-full text-xs text-slate-400 file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-[11px] file:font-semibold file:bg-slate-800 file:text-slate-350 hover:file:bg-slate-700 file:cursor-pointer"
              />
            </div>
          </div>
          <div className="flex gap-2 justify-end pt-2">
            <button
              type="button"
              onClick={() => setShowAddMeeting(false)}
              className="px-4 py-2 bg-slate-950 border border-slate-800 hover:bg-slate-900 rounded-xl text-xs text-slate-400"
            >
              ยกเลิก
            </button>
            <button
              type="submit"
              disabled={uploadingAudio}
              className="px-5 py-2 bg-gold-600 hover:bg-gold-500 text-xs font-semibold rounded-xl text-slate-950 disabled:opacity-50 transition-all flex items-center gap-2"
            >
              {uploadingAudio ? (
                <>
                  <svg className="animate-spin h-3 w-3 text-slate-950" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                  </svg>
                  กำลังถอดรหัสเสียงและวิเคราะห์โดย Agent...
                </>
              ) : 'เริ่มถอดความวิเคราะห์'}
            </button>
          </div>
        </form>
      )}

      {/* Main Workspace Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Left Column: Meeting Selection List */}
        <div className="lg:col-span-4 space-y-4">
          <div className="flex justify-between items-center px-1">
            <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider">รายการประชุมย้อนหลัง ({meetings.length})</h4>
            <button 
              onClick={fetchMeetings} 
              className="text-[10px] text-gold-500 hover:text-gold-400 font-medium"
              disabled={loading}
            >
              {loading ? "รีเฟรช..." : "🔄 รีเฟรชรายการ"}
            </button>
          </div>

          <div className="space-y-3 max-h-[600px] overflow-y-auto pr-1">
            {meetings.map((meet) => {
              const docs = extractAttachedDocs(meet.transcript);
              const isSelected = selectedMeeting?.id === meet.id;
              return (
                <div
                  key={meet.id}
                  onClick={() => {
                    setSelectedMeeting(meet);
                    setWorkspaceTab('summary');
                  }}
                  className={`p-4 rounded-2xl border transition-all cursor-pointer text-left space-y-2.5 ${
                    isSelected
                      ? 'bg-slate-900 border-gold-500/60 shadow-lg shadow-gold-500/5'
                      : 'bg-slate-950/60 border-slate-900 hover:border-slate-800 hover:bg-slate-900/30'
                  }`}
                >
                  <div className="flex justify-between items-start gap-2">
                    <h5 className="text-xs font-bold text-slate-100 line-clamp-1">{meet.title}</h5>
                    <span className="text-[9px] text-slate-500 font-mono shrink-0">{meet.date || '2026-06-16'}</span>
                  </div>
                  <p className="text-[11px] text-slate-400 line-clamp-2 font-light">
                    {meet.summary || 'ไม่มีบทสรุปการประชุม'}
                  </p>
                  <div className="flex items-center gap-3 text-[10px] text-slate-500 pt-1 border-t border-slate-900">
                    <span className="flex items-center gap-1">
                      📁 เอกสารแนบ: <strong className="text-slate-350">{docs.length}</strong>
                    </span>
                    <span className="flex items-center gap-1">
                      📋 งานสั่งการ: <strong className="text-slate-350">{meet.action_items?.length || 0}</strong>
                    </span>
                  </div>
                </div>
              );
            })}

            {meetings.length === 0 && !loading && (
              <div className="p-8 border border-slate-900 rounded-2xl text-center text-slate-500 text-xs">
                ไม่มีบันทึกประชุมในระบบ SQLite<br/>กดสุ่มสร้างหรืออัปโหลดไฟล์เสียงด้านบน
              </div>
            )}
          </div>
        </div>

        {/* Right Column: Selected Meeting RAG Workspace (NotebookLM Console) */}
        <div className="lg:col-span-8">
          {selectedMeeting ? (
            <div className="border border-slate-850 rounded-3xl bg-slate-900/20 glass overflow-hidden flex flex-col min-h-[550px]">
              
              {/* Workspace Header & Sub-Tabs */}
              <div className="p-5 bg-slate-950/80 border-b border-slate-850 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-[9px] uppercase tracking-widest text-gold-500 font-bold bg-gold-950/60 border border-gold-900 px-2.5 py-0.5 rounded-full">NotebookLM Active</span>
                    <span className="text-[10px] font-mono text-slate-500">ID: #{selectedMeeting.id}</span>
                  </div>
                  <h3 className="text-sm font-bold text-white mt-1.5">{selectedMeeting.title}</h3>
                </div>
                
                {/* Switch Workspace Tabs */}
                <div className="flex bg-slate-900 p-1 rounded-xl border border-slate-800 shrink-0">
                  <button
                    onClick={() => setWorkspaceTab('summary')}
                    className={`px-4 py-1.5 text-xs font-semibold rounded-lg transition-all ${
                      workspaceTab === 'summary'
                        ? 'bg-slate-950 text-gold-400 border border-slate-800'
                        : 'text-slate-400 hover:text-slate-200'
                    }`}
                  >
                    📋 สรุปสั่งการ
                  </button>
                  <button
                    onClick={() => setWorkspaceTab('chat')}
                    className={`px-4 py-1.5 text-xs font-semibold rounded-lg transition-all flex items-center gap-1.5 ${
                      workspaceTab === 'chat'
                        ? 'bg-slate-950 text-gold-400 border border-slate-800'
                        : 'text-slate-400 hover:text-slate-200'
                    }`}
                  >
                    💬 แชทเจาะลึก 
                    {selectedAttachedDocs.length > 0 && (
                      <span className="w-1.5 h-1.5 bg-green-500 rounded-full animate-pulse"></span>
                    )}
                  </button>
                </div>
              </div>

              {/* Tab Content 1: Summary & Action Items */}
              {workspaceTab === 'summary' && (
                <div className="p-6 space-y-6 flex-1 overflow-y-auto max-h-[500px]">
                  
                  {/* Detailed Summary */}
                  <div className="space-y-2">
                    <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider">มติการประชุมและข้อสรุป</h4>
                    <div className="p-4 bg-slate-950/40 border border-slate-850 rounded-2xl">
                      <p className="text-xs text-slate-300 leading-relaxed font-light whitespace-pre-wrap">
                        {selectedMeeting.summary || 'ไม่มีสรุปบันทึก'}
                      </p>
                    </div>
                  </div>

                  {/* Attached Documents */}
                  <div className="space-y-3">
                    <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center justify-between">
                      <span>เอกสารประกอบการประชุม ({selectedAttachedDocs.length})</span>
                      <span className="text-[10px] text-slate-500 font-light font-sans normal-case">สำหรับเป็นข้อมูลเสริมของ RAG</span>
                    </h4>
                    
                    {selectedAttachedDocs.length > 0 ? (
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                        {selectedAttachedDocs.map((docName, idx) => (
                          <div key={idx} className="flex items-center gap-2 p-3 bg-slate-950/50 border border-slate-850 rounded-xl text-xs text-slate-300">
                            <span className="text-slate-400">📄</span>
                            <span className="truncate font-light flex-1">{docName}</span>
                            <span className="text-[9px] text-emerald-500 font-bold bg-emerald-950/40 px-2 py-0.5 rounded border border-emerald-900/40 shrink-0">สกัด RAG แล้ว</span>
                          </div>
                        ))}
                      </div>
                    ) : (
                      <p className="text-[11px] text-slate-550 italic">ยังไม่มีการเพิ่มเอกสารประกอบการประชุมแบบ RAG สำหรับการแชทเจาะลึกเฉพาะทาง</p>
                    )}

                    {/* Document Upload Input zone */}
                    <div className="p-4 border border-dashed border-slate-800 hover:border-slate-700 bg-slate-950/20 rounded-2xl flex flex-col sm:flex-row items-center justify-between gap-4 transition-all">
                      <div className="flex items-center gap-3">
                        <span className="text-xl">📥</span>
                        <div className="text-left">
                          <p className="text-xs font-semibold text-slate-200">แนบเอกสารเพิ่ม (PDF / TXT / DOCX / MD)</p>
                          <p className="text-[10px] text-slate-500">ข้อมูลจะสกัดเข้า RAG ใช้อ้างอิงการตอบคำถามแชท</p>
                        </div>
                      </div>
                      <div className="flex gap-2 w-full sm:w-auto">
                        <input
                          type="file"
                          accept=".pdf,.txt,.docx,.md"
                          onChange={(e) => setDocFile(e.target.files?.[0] || null)}
                          className="hidden"
                          id="meeting-doc-upload"
                        />
                        <label
                          htmlFor="meeting-doc-upload"
                          className="px-3 py-2 bg-slate-900 border border-slate-800 hover:bg-slate-800 text-[11px] font-medium rounded-xl cursor-pointer text-slate-300 text-center flex-1 sm:flex-initial"
                        >
                          {docFile ? `เลือกแล้ว: ${docFile.name.slice(0, 15)}...` : '📂 เลือกไฟล์'}
                        </label>
                        <button
                          onClick={handleUploadDoc}
                          disabled={!docFile || uploadingDoc}
                          className="px-4 py-2 bg-gold-600 hover:bg-gold-500 text-xs font-semibold rounded-xl text-slate-950 disabled:opacity-40 transition-all shrink-0 flex-1 sm:flex-initial text-center"
                        >
                          {uploadingDoc ? 'กำลังวิเคราะห์...' : '🚀 แนบไฟล์'}
                        </button>
                      </div>
                    </div>
                  </div>

                  {/* Action Items List */}
                  <div className="space-y-3">
                    <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider">รายการสิ่งที่จะต้องปฏิบัติ (Action Items)</h4>
                    {selectedMeeting.action_items && selectedMeeting.action_items.length > 0 ? (
                      <div className="grid grid-cols-1 gap-2.5">
                        {selectedMeeting.action_items.map((item: any, idx: number) => (
                          <div key={idx} className="flex items-start gap-3 p-4 bg-slate-950/30 border border-slate-850 rounded-2xl text-xs">
                            <div className={`mt-0.5 w-4 h-4 rounded-full flex items-center justify-center border text-[9px] font-bold ${
                              item.status === 'completed' 
                                ? 'bg-emerald-950 border-emerald-800 text-emerald-400' 
                                : 'bg-amber-950 border-amber-800 text-amber-400'
                            }`}>
                              {item.status === 'completed' ? '✓' : '⏰'}
                            </div>
                            <div className="flex-1 space-y-1">
                              <div className="flex justify-between items-start gap-4">
                                <p className="text-slate-200 font-semibold leading-snug">{item.task}</p>
                                <span className={`text-[9px] px-2 py-0.5 rounded-full uppercase font-bold border ${
                                  item.status === 'completed'
                                    ? 'bg-emerald-950/40 text-emerald-400 border-emerald-900/60'
                                    : 'bg-amber-950/40 text-amber-400 border-amber-900/60'
                                }`}>
                                  {item.status === 'completed' ? 'เสร็จสิ้น' : 'รอการดำเนินงาน'}
                                </span>
                              </div>
                              <div className="flex items-center gap-4 text-[10px] text-slate-500 pt-0.5">
                                <span>ผู้รับผิดชอบ: <strong className="text-slate-400">{item.assignee}</strong></span>
                                <span>กำหนดส่ง: <strong className="text-slate-400 font-mono">{item.due_date}</strong></span>
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    ) : (
                      <p className="text-xs text-slate-500 italic py-2">ไม่มีการมอบหมายงานสั่งการในการประชุมครั้งนี้</p>
                    )}
                  </div>

                </div>
              )}

              {/* Tab Content 2: Chat with Meeting (NotebookLM style) */}
              {workspaceTab === 'chat' && (
                <div className="flex-1 flex flex-col bg-slate-950/40">
                  
                  {/* Chat Area Info panel */}
                  <div className="px-5 py-2.5 bg-slate-950/90 border-b border-slate-900 text-[10px] text-slate-400 flex justify-between items-center shrink-0">
                    <span>📚 ถามหาข้อมูลภายในบันทึกและเอกสารแนบของการประชุมนี้เท่านั้น</span>
                    <span>เอกสาร RAG: <strong>{selectedAttachedDocs.length} ฉบับ</strong></span>
                  </div>

                  {/* Messages Scroll Box */}
                  <div className="flex-1 p-5 overflow-y-auto space-y-4 max-h-[360px] min-h-[300px]">
                    
                    {/* Welcome message */}
                    <div className="flex gap-3">
                      <div className="w-7 h-7 rounded-full bg-gold-950 border border-gold-900 flex items-center justify-center text-xs shadow">
                        🤖
                      </div>
                      <div className="p-3.5 bg-slate-900/80 border border-slate-850 rounded-2xl rounded-tl-none max-w-[85%] text-left text-xs leading-relaxed font-light text-slate-200">
                        ยินดีต้อนรับสู่กล่องวิเคราะห์การประชุม สไตล์ NotebookLM! <br/>
                        คุณสามารถถามเจาะลึกคำสั่งการ นโยบาย หรือรายละเอียดที่มีอยู่ในเอกสารแนบของการประชุม <strong>"{selectedMeeting.title}"</strong> ได้ทันทีครับ
                      </div>
                    </div>

                    {/* Chat Logs */}
                    {currentChatLogs.map((msg, index) => {
                      const isUser = msg.role === 'user';
                      return (
                        <div key={index} className={`flex gap-3 ${isUser ? 'justify-end' : 'justify-start'}`}>
                          {!isUser && (
                            <div className="w-7 h-7 rounded-full bg-gold-950 border border-gold-900 flex items-center justify-center text-xs shadow shrink-0">
                              🤖
                            </div>
                          )}
                          <div className={`p-3.5 rounded-2xl text-left text-xs leading-relaxed max-w-[85%] font-light whitespace-pre-wrap ${
                            isUser
                              ? 'bg-gradient-to-r from-gold-600 to-amber-700 text-slate-950 font-medium rounded-tr-none'
                              : 'bg-slate-900/80 border border-slate-850 text-slate-200 rounded-tl-none'
                          }`}>
                            {msg.text}
                          </div>
                          {isUser && (
                            <div className="w-7 h-7 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center text-[10px] font-bold text-slate-300 shrink-0">
                              ME
                            </div>
                          )}
                        </div>
                      );
                    })}

                    {/* Chat loader */}
                    {chatLoading && (
                      <div className="flex gap-3 animate-pulse">
                        <div className="w-7 h-7 rounded-full bg-gold-950 border border-gold-900 flex items-center justify-center text-xs shrink-0">
                          ⌛
                        </div>
                        <div className="p-3.5 bg-slate-900/60 border border-slate-850 rounded-2xl rounded-tl-none text-left text-xs text-slate-400">
                          กำลังประมวลผล RAG อ้างอิงเนื้อหาเอกสารประชุม...
                        </div>
                      </div>
                    )}
                    
                    <div ref={chatEndRef} />
                  </div>

                  {/* Message Input box */}
                  <div className="p-4 bg-slate-950/80 border-t border-slate-900 flex gap-2 shrink-0">
                    <input
                      type="text"
                      value={chatInput}
                      onChange={(e) => setChatInput(e.target.value)}
                      onKeyDown={(e) => {
                        if (e.key === 'Enter') handleAskMeeting();
                      }}
                      placeholder={`พิมพ์คำถามเกี่ยวกับ "${selectedMeeting.title}"...`}
                      disabled={chatLoading}
                      className="flex-1 bg-slate-900 border border-slate-850 rounded-xl px-4 py-2.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-gold-500/50"
                    />
                    <button
                      onClick={handleAskMeeting}
                      disabled={chatLoading || !chatInput.trim()}
                      className="px-5 py-2.5 bg-gold-600 hover:bg-gold-500 disabled:opacity-40 text-xs font-semibold rounded-xl text-slate-950 transition-all shadow-md shrink-0"
                    >
                      ส่งถาม
                    </button>
                  </div>

                </div>
              )}

            </div>
          ) : (
            // Workspace Blank Placeholder
            <div className="border border-dashed border-slate-800 rounded-3xl p-12 text-center bg-slate-950/20 glass h-full flex flex-col items-center justify-center space-y-4">
              <div className="w-16 h-16 rounded-full bg-slate-900/60 border border-slate-800 flex items-center justify-center text-2xl text-slate-500 animate-bounce">
                📖
              </div>
              <div className="max-w-md">
                <h4 className="text-sm font-semibold text-slate-300">เข้าสู่ระบบความจำประชุมเจาะลึก (Meeting Workspace)</h4>
                <p className="text-xs text-slate-500 leading-relaxed mt-2 font-light">
                  กรุณาเลือกรายการการประชุมทางเมนูด้านซ้าย เพื่อเรียกดูบันทึก สรุปคำสั่งการ หรือเปิดแชทถามตอบ RAG อ้างอิงเอกสารแนบการประชุมอย่างเจาะลึก 100%
                </p>
              </div>
            </div>
          )}
        </div>

      </div>
    </div>
  );
}
