import { useState, useEffect, useRef } from 'react';
import { Search, ThumbsUp, ThumbsDown, X, Wallet } from 'lucide-react';
import { api, QueryResponse, SourceChunkInfo } from '../../lib/api';

interface AgentMessage {
  agent: string;
  avatar: string;
  roleColor: string;
  text: string;
  token_details?: {
    cost_tokens: number;
    reward_tokens: number;
    balance_tokens: number;
  };
}

export function AskTab() {
  const [activeSubTab, setActiveSubTab] = useState<'rag' | 'collab'>('rag');

  // ==========================================
  // Tab 1: Standard RAG Oracle States
  // ==========================================
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState<QueryResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [selectedSource, setSelectedSource] = useState<SourceChunkInfo | null>(null);

  // ==========================================
  // Tab 2: Multi-Agent Collaboration States
  // ==========================================
  const [collabPrompt, setCollabPrompt] = useState("ต้องการวางโครงการคัดกรองวัณโรคเชิงรุกและจัดหาหน้ากากป้องกันฝุ่น PM2.5 อำเภอแม่สาย ภายใต้งบประมาณราชการที่จำกัดและถูกต้องตามระเบียบพัสดุ");
  const [collabMessages, setCollabMessages] = useState<AgentMessage[]>([]);
  const [collabLoading, setCollabLoading] = useState(false);
  const [visibleMessageCount, setVisibleMessageCount] = useState(0);
  
  const chatEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // โหลดคำถามทางลัดจากหน้า Home
    const q = localStorage.getItem("hosprime_temp_question");
    if (q) {
      setQuestion(q);
      localStorage.removeItem("hosprime_temp_question");
      handleAsk(q);
    }
  }, []);

  useEffect(() => {
    // Auto scroll to bottom of collaboration chat
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [visibleMessageCount, collabLoading]);

  // Tab 1 Handler
  const handleAsk = async (qText?: string) => {
    const queryToSubmit = qText || question;
    if (!queryToSubmit.trim()) return;

    setLoading(true);
    setError(null);
    setResponse(null);
    setSelectedSource(null);

    try {
      const result = await api.askOracle(queryToSubmit);
      setResponse(result);
    } catch (e) {
      setError("เกิดข้อผิดพลาดในการติดต่อถามข้อมูล กรุณาลองใหม่อีกครั้ง");
    } finally {
      setLoading(false);
    }
  };

  const handleFeedback = async (type: 'positive' | 'negative') => {
    if (!response) return;
    try {
      await api.submitFeedback(response.query_log_id, type);
      alert("ขอบคุณสำหรับคำติชม เพื่อพัฒนาการสืบค้นข้อมูลในอนาคต");
    } catch (e) {
      console.error(e);
    }
  };

  // Tab 2 Handler: Multi-Agent Collaboration Real-logic & Token Economy
  const handleTriggerCollab = async () => {
    if (!collabPrompt.trim()) return;
    setCollabLoading(true);
    setCollabMessages([]);
    setVisibleMessageCount(0);

    const messagesList: AgentMessage[] = [];

    // โปรไฟล์และสีประจำแผนก
    const avatarMap: Record<string, { av: string, col: string }> = {
      "pho": { av: "👑 PHO", col: "text-amber-400 font-bold" },
      "cfo": { av: "💰 CFO", col: "text-indigo-400 font-bold" },
      "cio": { av: "💻 CIO", col: "text-teal-400 font-bold" },
      "tb": { av: "🫁 TB", col: "text-emerald-400 font-bold" },
      "pm25": { av: "😷 PM", col: "text-rose-400 font-bold" },
      "disaster": { av: "🌊 Emergency", col: "text-orange-400 font-bold" },
      "legal": { av: "⚖️ Legal", col: "text-sky-400 font-bold" },
      "admin": { av: "💼 Secretary", col: "text-slate-400 font-bold" }
    };

    try {
      // 1. ดึงรายชื่อเอเจนต์จาก DB และกรองตัวที่ Active
      const agents = await api.getAgents();
      const activeAgents = agents.filter(a => a.is_active && a.role !== 'admin');
      
      if (activeAgents.length === 0) {
        alert("ไม่มี AI ผู้เชี่ยวชาญเปิดทำงานอยู่ในขณะนี้ กรุณาเปิดใช้งานอย่างน้อย 1 แผนกในหน้าระบบกำกับดูแล AI");
        setCollabLoading(false);
        return;
      }

      // 2. เลขาส่วนตัว AI (Secretary) ออกมาประสานงานรอบแรก
      const secretaryMsg = `เจ้านายครับ ได้รับมอบหมายภารกิจ "${collabPrompt}" เรียบร้อยแล้วครับ! \nผมขออนุญาตตั้งห้องประชุมบอร์ด AI ประสานงานผู้เชี่ยวชาญจำนวน ${activeAgents.length} แผนกที่กำลังปฏิบัติการ เพื่อร่วมมือกันจัดทำแผนงานชิ้นงานชิ้นนี้ให้สมบูรณ์และคุ้มค่าที่สุดครับ`;
      
      const firstSecretary: AgentMessage = {
        agent: "Secretary AI (เลขาส่วนตัว)",
        avatar: "💼 Secretary",
        roleColor: "text-slate-400 font-bold",
        text: secretaryMsg,
        token_details: {
          cost_tokens: 150,
          reward_tokens: 0,
          balance_tokens: 45000 // จำลองยอดเงินเลขา
        }
      };
      
      messagesList.push(firstSecretary);
      setCollabMessages([...messagesList]);
      setVisibleMessageCount(1);

      // หน่วงเวลาสมจริงเล็กน้อย
      await new Promise(r => setTimeout(r, 1200));

      // 3. วนลูปคุยกับผู้เชี่ยวชาญทีละตัว
      const transcriptParts: string[] = [];
      
      for (const agent of activeAgents) {
        // อัปเดตสถานะในช่องแชทว่ากำลังรอทวินตัวนี้ประมวลผล
        const loaderMsg: AgentMessage = {
          agent: `${agent.name} (กำลังประมวลผล...)`,
          avatar: avatarMap[agent.role]?.av || "🤖 Agent",
          roleColor: "text-slate-550 animate-pulse",
          text: `กำลังเตรียมประเมินผลและคำนวณเครดิต Token...`
        };
        
        setCollabMessages([...messagesList, loaderMsg]);
        setVisibleMessageCount(messagesList.length + 1);
        await new Promise(r => setTimeout(r, 1000));

        try {
          // เรียก API ไปหาทวินจริง
          const reqBody = {
            agent_id: agent.role,
            question: `ในฐานะแผนกของคุณ กรุณาวิเคราะห์และให้คำปรึกษาสำหรับงานนี้: "${collabPrompt}" เพื่อประมวลผลร่วมกับฝ่ายอื่นๆ`
          };
          
          const token = localStorage.getItem('hosprime_token');
          const headers: Record<string, string> = { 'Content-Type': 'application/json' };
          if (token) headers['Authorization'] = `Bearer ${token}`;

          const res = await fetch(`${((import.meta as any).env?.VITE_API_BASE_URL) || 'http://localhost:8000/api'}/twins/consult`, {
            method: 'POST',
            headers,
            body: JSON.stringify(reqBody)
          });
          
          if (!res.ok) {
            const errData = await res.json().catch(() => ({}));
            throw new Error(errData.detail || "การเชื่อมต่อทวินขัดข้อง");
          }
          
          const data = await res.json();
          
          // นำคำตอบและ Token details ที่ได้บันทึกใส่ลิสต์ข้อความจริง
          const agentProfile = avatarMap[agent.role] || { av: "🤖 Agent", col: "text-gold-400 font-bold" };
          const responseMsg: AgentMessage = {
            agent: `${agent.name}`,
            avatar: agentProfile.av,
            roleColor: agentProfile.col,
            text: data.response,
            token_details: {
              cost_tokens: data.token_details?.cost_tokens || 350,
              reward_tokens: data.token_details?.reward_tokens || 525,
              balance_tokens: data.token_details?.balance_tokens || 50000
            }
          };
          
          transcriptParts.push(`${agent.name} เสนอว่า: ${data.response}`);
          messagesList.push(responseMsg);
          setCollabMessages([...messagesList]);
          setVisibleMessageCount(messagesList.length);
          
          await new Promise(r => setTimeout(r, 1500));
        } catch (err: any) {
          // หากตัวใดตัวหนึ่งล้มเหลว (เช่นโควตาหมด) ให้ข้ามหรือแสดงความล้มเหลว
          const errorMsg: AgentMessage = {
            agent: `${agent.name} (ระงับปฏิบัติการ)`,
            avatar: avatarMap[agent.role]?.av || "🤖 Agent",
            roleColor: "text-rose-500",
            text: `⚠️ ขัดข้อง: ${err.message || 'โควตา Token เกินกำหนดการตรวจสอบสารสนเทศ'}`
          };
          messagesList.push(errorMsg);
          setCollabMessages([...messagesList]);
          setVisibleMessageCount(messagesList.length);
          await new Promise(r => setTimeout(r, 1200));
        }
      }

      // 4. รอบสุดท้าย: ส่งข้อมูลกลับหาเลขา AI เพื่อเขียนสรุปและสร้างชิ้นงานสุดท้าย
      const summaryLoader: AgentMessage = {
        agent: "Secretary AI (เลขาส่วนตัว)",
        avatar: "💼 Secretary",
        roleColor: "text-slate-400 font-bold animate-pulse",
        text: `รวบรวมข้อมูลเสร็จสิ้น กำลังประสานงานและจัดทํารายงาน **ชิ้นงานบูรณาการ (Integrated Action Plan/TOR)** สำหรับส่งเจ้านาย...`
      };
      setCollabMessages([...messagesList, summaryLoader]);
      setVisibleMessageCount(messagesList.length + 1);
      await new Promise(r => setTimeout(r, 1200));

      const sysInstruction = `คุณคือระบบเลขาอัจฉริยะของสำนักงานสาธารณสุขจังหวัดเชียงราย 
หน้าที่ของคุณคือนำข้อเสนอแนะจากการประชุมระดมสมองของ AI Twins แต่ละฝ่าย มาสรุปและเขียนเรียบเรียงให้ออกมาเป็นชิ้นงานสมบูรณ์
โดยจัดทำหัวข้อดังนี้:
1. 📂 ชื่อชิ้นงานและประเภท (เช่น ร่างจดหมายราชการสั่งการ หรือ โครงการบูรณาการ)
2. 🎯 เป้าหมายนโยบายระดับจังหวัด (อิงแนวทาง PHO)
3. 💰 แผนงบประมาณและการพัสดุ (อิงแนวทาง CFO และระเบียบ Legal)
4. ⚙️ มาตรการปฏิบัติหน้างาน (อิงแนวทาง Specialist ต่างๆ)
5. 🛡️ ข้อมูลมูลค่าชิ้นงาน (ประมาณการ Token output ของชิ้นงานนี้)
กรุณาเขียนสรุปให้สวยงาม เป็นระเบียบ ชัดเจน และเป็นทางการ`;

      const reqBody = {
        agent_id: "admin", // เลขา AI
        question: `${sysInstruction}\n\nโจทย์ภารกิจเดิม: ${collabPrompt}\n\nความคิดเห็นจากบอร์ดผู้เชี่ยวชาญ:\n${transcriptParts.join("\n\n")}`
      };

      const token = localStorage.getItem('hosprime_token');
      const headers: Record<string, string> = { 'Content-Type': 'application/json' };
      if (token) headers['Authorization'] = `Bearer ${token}`;

      const res = await fetch(`${((import.meta as any).env?.VITE_API_BASE_URL) || 'http://localhost:8000/api'}/twins/consult`, {
        method: 'POST',
        headers,
        body: JSON.stringify(reqBody)
      });
      if (!res.ok) throw new Error("การสังเคราะห์ข้อมูลชิ้นงานขัดข้อง");
      const data = await res.json();

      const finalSecretary: AgentMessage = {
        agent: "Secretary AI (สรุปชิ้นงานสำเร็จ)",
        avatar: "💼 Secretary",
        roleColor: "text-gold-400 font-bold",
        text: `เจ้านายครับ! การระดมสมองหารือเสร็จสิ้นสมบูรณ์ ได้ผลผลิตออกมาเป็นชิ้นงานบูรณาการเรียบร้อยแล้วครับ:\n\n${data.response}`,
        token_details: {
          cost_tokens: data.token_details?.cost_tokens || 500,
          reward_tokens: data.token_details?.reward_tokens || 750,
          balance_tokens: data.token_details?.balance_tokens || 45000
        }
      };

      messagesList.push(finalSecretary);
      setCollabMessages([...messagesList]);
      setVisibleMessageCount(messagesList.length);
      setCollabLoading(false);

    } catch (e: any) {
      alert("การระดมสมองของ AI ขัดข้อง: " + e.message);
      setCollabLoading(false);
    }
  };

  // Text formatter helpers
  const renderFormattedAnswer = (text: string) => {
    const sections = text.split(/(?=#\s+)/);
    return (
      <div className="space-y-6">
        {sections.map((sec, i) => {
          const lines = sec.trim().split('\n');
          const title = lines[0].replace('#', '').trim();
          const body = lines.slice(1).join('\n');
          if (!title) return null;

          let titleColor = "text-white";
          let bgColor = "bg-slate-900/50";
          let borderColor = "border-slate-800";

          if (title.includes("Executive Summary") || title.includes("สรุป")) {
            bgColor = "bg-brand-900/10";
            borderColor = "border-brand-800/40";
            titleColor = "text-brand-300";
          } else if (title.includes("Findings") || title.includes("ผลลัพธ์")) {
            titleColor = "text-sky-300";
          } else if (title.includes("Evidence") || title.includes("หลักฐาน")) {
            titleColor = "text-emerald-300";
          } else if (title.includes("Caution") || title.includes("ข้อควรระวัง")) {
            bgColor = "bg-amber-950/10";
            borderColor = "border-amber-800/30";
            titleColor = "text-amber-400";
          } else if (title.includes("Next Step") || title.includes("คำแนะนำ")) {
            bgColor = "bg-indigo-950/15";
            borderColor = "border-indigo-800/30";
            titleColor = "text-indigo-400";
          }

          return (
            <div key={i} className={`p-6 rounded-2xl border ${borderColor} ${bgColor} space-y-3`}>
              <h4 className={`text-md font-bold ${titleColor} flex items-center gap-2`}>
                <span className="w-1.5 h-3 bg-current rounded-full"></span>
                {title}
              </h4>
              <div className="text-slate-300 text-sm leading-relaxed whitespace-pre-line prose max-w-none">
                {renderInlineCitations(body)}
              </div>
            </div>
          );
        })}
      </div>
    );
  };

  const renderInlineCitations = (text: string) => {
    const regex = /\[Source ID:\s*(\d+)\]/gi;
    const parts = [];
    let lastIndex = 0;
    let match;

    while ((match = regex.exec(text)) !== null) {
      const matchIndex = match.index;
      const sourceIdStr = match[1];
      const sourceId = parseInt(sourceIdStr);

      if (matchIndex > lastIndex) {
        parts.push(text.substring(lastIndex, matchIndex));
      }

      parts.push(
        <button
          key={matchIndex}
          onClick={() => {
            if (response && response.sources) {
              const source = response.sources[sourceId - 1];
              if (source) setSelectedSource(source);
            }
          }}
          className="mx-1 px-1.5 py-0.5 text-xs font-bold bg-brand-800 hover:bg-gold-500 hover:text-slate-950 text-white rounded transition-colors duration-150"
        >
          [{sourceIdStr}]
        </button>
      );
      lastIndex = regex.lastIndex;
    }

    if (lastIndex < text.length) {
      parts.push(text.substring(lastIndex));
    }

    return parts.length > 0 ? parts : text;
  };

  return (
    <div className="max-w-7xl mx-auto space-y-6 text-white text-left animate-fade-in">
      
      {/* Tab Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h2 className="text-2xl font-bold tracking-tight font-outfit text-transparent bg-clip-text bg-gradient-to-r from-white via-slate-100 to-gold-400">
            🧠 คลังปัญญาองค์กรและการระดมสมอง (Oracle Brain)
          </h2>
          <p className="text-slate-400 text-xs mt-1">
            ปรึกษาข้อมูลและคลังความรู้ RAG หรือจัดตั้งการประชุมจำลองของทีม AI Experts เพื่อร่วมกันจัดทำแผนงานชิ้นงานสำคัญ
          </p>
        </div>

        {/* Switcher Navigation */}
        <div className="flex bg-slate-900 p-1 rounded-2xl border border-slate-800 shrink-0">
          <button
            onClick={() => setActiveSubTab('rag')}
            className={`px-4 py-2 text-xs font-semibold rounded-xl transition-all ${
              activeSubTab === 'rag' ? 'bg-slate-950 text-gold-400 border border-slate-800' : 'text-slate-400 hover:text-slate-250'
            }`}
          >
            🔍 ถามความรู้ RAG (Oracle Ask)
          </button>
          <button
            onClick={() => setActiveSubTab('collab')}
            className={`px-4 py-2 text-xs font-semibold rounded-xl transition-all ${
              activeSubTab === 'collab' ? 'bg-slate-950 text-gold-400 border border-slate-800' : 'text-slate-400 hover:text-slate-250'
            }`}
          >
            🤝 ปรึกษาผู้เชี่ยวชาญ (Multi-Agent)
          </button>
        </div>
      </div>

      {/* ======================================================== */}
      {/* SUBTAB 1: Standard RAG Oracle (rag)                      */}
      {/* ======================================================== */}
      {activeSubTab === 'rag' && (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start animate-fade-in">
          {/* Left Side: Input and Answers */}
          <div className="lg:col-span-8 space-y-6">
            <div className="bg-slate-900/20 border border-slate-850 glass p-6 rounded-2xl space-y-4">
              <div className="relative">
                <input
                  type="text"
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && handleAsk()}
                  placeholder="สอบถามข้อมูล RAG จากนโยบาย คู่มือ หรือผลงานจังหวัด เช่น 'แนวทางการคัดกรองวัณโรคดื้อยามีอะไรบ้าง'..."
                  className="w-full bg-slate-950 border border-slate-850 focus:border-gold-500/50 rounded-xl py-3 pl-4 pr-12 text-xs text-white placeholder-slate-550 outline-none"
                />
                <button 
                  onClick={() => handleAsk()}
                  className="absolute right-2.5 top-2 bg-gradient-to-tr from-gold-600 to-amber-700 hover:from-gold-500 hover:to-amber-600 text-slate-950 p-2 rounded-lg transition-all"
                >
                  <Search className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>

            {error && (
              <div className="p-4 bg-rose-950/20 border border-rose-800/40 rounded-xl text-rose-300 text-xs">
                ⚠️ {error}
              </div>
            )}

            {loading && (
              <div className="bg-slate-900/20 border border-slate-850 glass p-12 rounded-2xl flex flex-col items-center justify-center space-y-4">
                <div className="w-8 h-8 border-4 border-gold-500 border-t-transparent rounded-full animate-spin"></div>
                <p className="text-xs text-slate-400">กำลังสืบค้นและสังเคราะห์คำตอบ RAG จากระบบองค์กร...</p>
              </div>
            )}

            {response && (
              <div className="space-y-6">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-semibold text-slate-405">ค่าความเชื่อมั่นในการตอบ:</span>
                    <span className={`text-[11px] font-bold px-2.5 py-0.5 rounded-full border ${
                      response.confidence > 0.7 
                        ? 'bg-emerald-955/35 text-emerald-400 border-emerald-900/60' 
                        : 'bg-amber-955/35 text-amber-400 border-amber-900/60'
                    }`}>
                      {(response.confidence * 100).toFixed(0)}% {response.confidence > 0.75 ? "น่าเชื่อถือสูง" : "ควรอ่านหลักฐานเสริม"}
                    </span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-xs text-slate-500">ช่วยระบุผลลัพธ์คำตอบ:</span>
                    <button onClick={() => handleFeedback('positive')} className="p-1.5 bg-slate-900 hover:bg-slate-800 text-slate-400 hover:text-emerald-400 rounded-lg border border-slate-850">
                      <ThumbsUp className="w-3 h-3" />
                    </button>
                    <button onClick={() => handleFeedback('negative')} className="p-1.5 bg-slate-900 hover:bg-slate-800 text-slate-400 hover:text-rose-400 rounded-lg border border-slate-855">
                      <ThumbsDown className="w-3 h-3" />
                    </button>
                  </div>
                </div>

                {renderFormattedAnswer(response.answer)}
              </div>
            )}
          </div>

          {/* Right Side: References / Sources */}
          <div className="lg:col-span-4 space-y-6">
            {response && (
              <div className="bg-slate-900/20 border border-slate-850 glass p-5 rounded-2xl space-y-4">
                <h3 className="text-xs font-bold text-slate-200 flex items-center gap-2 tracking-wider">
                  📂 แฟ้มหลักฐานการสืบค้น ({response.sources.length})
                </h3>
                <div className="space-y-2.5">
                  {response.sources.map((src, i) => (
                    <button
                      key={i}
                      onClick={() => setSelectedSource(src)}
                      className={`w-full p-4 rounded-xl text-left border transition-all ${
                        selectedSource?.chunk_id === src.chunk_id 
                          ? 'bg-slate-900 border-gold-500/50' 
                          : 'bg-slate-950/60 border-slate-900 hover:border-slate-800 hover:bg-slate-900/30'
                      }`}
                    >
                      <div className="flex items-center justify-between mb-2 text-[10px]">
                        <span className="font-bold bg-slate-950 text-slate-450 px-2 py-0.5 rounded border border-slate-850">
                          หลักฐานชิ้นที่ {i + 1}
                        </span>
                        <span className="text-slate-500 font-mono">
                          Score: {(src.score * 100).toFixed(0)}%
                        </span>
                      </div>
                      <p className="text-xs font-semibold text-white truncate">{src.document_title}</p>
                      <p className="text-[10px] text-slate-500 mt-1">
                        หน้า {src.page_number || '1'} | หมวดหมู่: {src.section_title || 'N/A'}
                      </p>
                    </button>
                  ))}
                </div>
              </div>
            )}

            {selectedSource && (
              <div className="bg-slate-900/20 border border-slate-850 glass p-5 rounded-2xl space-y-4 animate-fade-in">
                <div className="flex items-center justify-between pb-2 border-b border-slate-900">
                  <h4 className="text-xs font-bold text-slate-300">เนื้อความอ้างอิงตรงจากเอกสาร</h4>
                  <button onClick={() => setSelectedSource(null)} className="text-slate-500 hover:text-white">
                    <X className="w-3 w-3" />
                  </button>
                </div>
                <div className="space-y-1 text-left text-xs">
                  <p className="font-bold text-gold-400 truncate">{selectedSource.document_title}</p>
                  <p className="text-[10px] text-slate-500">
                    หน้าที่ {selectedSource.page_number || '1'} | หัวข้อ: {selectedSource.section_title || 'N/A'}
                  </p>
                </div>
                <div className="p-4 bg-slate-955 border border-slate-850 rounded-xl text-[11px] text-slate-350 leading-relaxed max-h-60 overflow-y-auto whitespace-pre-wrap font-light">
                  {selectedSource.chunk_text}
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* ======================================================== */}
      {/* SUBTAB 2: Multi-Agent Collaboration Panel (collab)       */}
      {/* ======================================================== */}
      {activeSubTab === 'collab' && (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start animate-fade-in">
          
          {/* Left Pane: Config & Suggestions */}
          <div className="lg:col-span-4 space-y-5">
            
            <div className="bg-slate-900/20 border border-slate-850 glass p-5 rounded-2xl text-left space-y-4">
              <div>
                <h3 className="text-xs font-bold text-gold-400 uppercase tracking-widest"> Orhcestration Console</h3>
                <p className="text-[10px] text-slate-500 mt-1">ป้อนภารกิจที่ซับซ้อนเพื่อให้เลขาส่วนตัว AI ทำการประเมินและประชุมหารือร่วมกับผู้เชี่ยวชาญทุกฝ่ายในบอร์ดผู้บริหาร</p>
              </div>

              <div className="space-y-2">
                <label className="text-[11px] text-slate-400 font-semibold block">ระบุโจทย์ภารกิจ/ชิ้นงาน *</label>
                <textarea
                  rows={4}
                  value={collabPrompt}
                  onChange={(e) => setCollabPrompt(e.target.value)}
                  placeholder="เช่น ต้องการจัดหาหน้ากากอนามัยสำหรับ อสม. และซ่อมแซมโรงไฟฟ้า รพ.สต. พื้นที่น้ำท่วมด่วน..."
                  className="w-full bg-slate-950 border border-slate-850 focus:border-gold-500/50 rounded-xl px-3 py-2 text-xs text-white outline-none resize-none font-light leading-relaxed"
                />
              </div>

              <button
                onClick={handleTriggerCollab}
                disabled={collabLoading || !collabPrompt.trim()}
                className="w-full py-2.5 bg-gradient-to-r from-gold-600 to-amber-700 hover:from-gold-500 hover:to-amber-600 disabled:opacity-40 text-slate-950 font-bold rounded-xl text-xs transition-all shadow-lg flex items-center justify-center gap-2"
              >
                {collabLoading ? (
                  <>
                    <div className="w-3.5 h-3.5 border-2 border-slate-950 border-t-transparent rounded-full animate-spin"></div>
                    <span>กำลังตั้งโต๊ะประชุมบอร์ด AI...</span>
                  </>
                ) : '🤝 เริ่มต้นการระดมสมองของ AI'}
              </button>
            </div>

            {/* Suggestions cards */}
            <div className="bg-slate-950/40 border border-slate-850 p-5 rounded-2xl text-left space-y-3">
              <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider">โจทย์งานแนะนำศึกษา</h4>
              <div className="space-y-2 text-xs">
                <button
                  onClick={() => setCollabPrompt("แผนบูรณาการความปลอดภัยความปลอดภัยเครือข่ายไอทีโรงพยาบาลอำเภอ รองรับมาตรฐาน PDPA ของสสจ. ภายใต้งบประมาณจัดซื้อจัดจ้างที่จำกัด")}
                  className="w-full p-2.5 bg-slate-900/40 hover:bg-slate-900/80 border border-slate-900 rounded-xl text-left text-[11px] text-slate-350 truncate block"
                >
                  🔒 1. การประเมินความปลอดภัยระบบและกฎหมาย PDPA
                </button>
                <button
                  onClick={() => setCollabPrompt("มาตรการเชิงรับและเชิงรุกรับมือสภาวะวิกฤตอุทกภัยแม่สาย จัดส่งชุดแพทย์เคลื่อนที่ MCATT และเวชภัณฑ์ภายใน 24 ชม.")}
                  className="w-full p-2.5 bg-slate-900/40 hover:bg-slate-900/80 border border-slate-900 rounded-xl text-left text-[11px] text-slate-350 truncate block"
                >
                  🌊 2. แผนรับมืออุทกภัยแม่สายเร่งด่วน
                </button>
                <button
                  onClick={() => setCollabPrompt("วางแผนจัดชุดรถเอกซเรย์หลวงพระราชทานเคลื่อนที่สุ่มคัดกรองวัณโรคดื้อยาในทัณฑสถานจังหวัด 100%")}
                  className="w-full p-2.5 bg-slate-900/40 hover:bg-slate-900/80 border border-slate-900 rounded-xl text-left text-[11px] text-slate-350 truncate block"
                >
                  🫁 3. รณรงค์วัณโรคคัดกรองในเรือนจำ
                </button>
              </div>
            </div>

          </div>

          {/* Right Pane: Multi-Agent Board room */}
          <div className="lg:col-span-8 bg-slate-900/20 border border-slate-850 rounded-3xl overflow-hidden glass flex flex-col min-h-[500px]">
            
            {/* Header info */}
            <div className="p-4 bg-slate-950 border-b border-slate-900 flex justify-between items-center shrink-0">
              <div className="text-left">
                <h4 className="text-xs font-bold text-white">🤝 โต๊ะประชุมระดมสมองผู้เชี่ยวชาญร่วม (AI Board Meeting)</h4>
                <p className="text-[9px] text-slate-500 mt-0.5">บอร์ดประมวลผลความคิดเห็นและรวบรวมชิ้นงานสั่งการแบบครบวงจร</p>
              </div>
              <span className="text-[9px] bg-gold-950/60 border border-gold-900 text-gold-400 font-bold px-2 py-0.5 rounded">
                Multi-Agent Active
              </span>
            </div>

            {/* Chat Messages Log */}
            <div className="flex-1 p-5 overflow-y-auto space-y-4 max-h-[420px] min-h-[350px] bg-slate-955/20">
              
              {collabMessages.slice(0, visibleMessageCount).map((msg, idx) => {
                const isFinal = idx === collabMessages.length - 1;
                return (
                  <div key={idx} className="flex gap-3 text-left animate-slide-down">
                    <div className="w-8 h-8 rounded-full bg-slate-950 border border-slate-850 flex items-center justify-center text-[10px] font-bold shadow shrink-0">
                      {msg.avatar}
                    </div>
                    <div className={`p-4 rounded-2xl rounded-tl-none text-xs leading-relaxed max-w-[85%] font-light whitespace-pre-wrap border ${
                      isFinal 
                        ? 'bg-slate-900 border-gold-500/50 text-slate-200 shadow-md shadow-gold-500/5' 
                        : 'bg-slate-950/80 border-slate-850 text-slate-300'
                    }`}>
                      <p className={`font-bold text-[10px] mb-1.5 ${msg.roleColor}`}>{msg.agent}</p>
                      <div className="whitespace-pre-wrap">{msg.text}</div>
                      
                      {msg.token_details && (
                        <div className="mt-3 pt-2 border-t border-slate-900/60 flex flex-wrap gap-x-4 gap-y-1 text-[9px] text-slate-500 font-mono items-center">
                          <span className="flex items-center gap-1 text-rose-400">
                            <span className="w-1 h-1 rounded-full bg-rose-500"></span>
                            วิเคราะห์: -{msg.token_details.cost_tokens.toLocaleString()} Tokens
                          </span>
                          {msg.token_details.reward_tokens > 0 && (
                            <span className="flex items-center gap-1 text-emerald-400">
                              <span className="w-1 h-1 rounded-full bg-emerald-500"></span>
                              รางวัลชิ้นงาน: +{msg.token_details.reward_tokens.toLocaleString()} Tokens
                            </span>
                          )}
                          <span className="flex items-center gap-1 text-gold-400 ml-auto">
                            <Wallet className="w-2.5 h-2.5 text-gold-500" />
                            กระเป๋า: {msg.token_details.balance_tokens.toLocaleString()} Tokens
                          </span>
                        </div>
                      )}
                    </div>
                  </div>
                );
              })}

              {collabLoading && visibleMessageCount < collabMessages.length && (
                <div className="flex gap-3 text-left animate-pulse">
                  <div className="w-8 h-8 rounded-full bg-slate-950 border border-slate-850 flex items-center justify-center text-xs shrink-0">💬</div>
                  <div className="p-4 bg-slate-950/40 border border-slate-850 rounded-2xl rounded-tl-none text-xs text-slate-500">
                    กำลังปรึกษาและถกเถียงทัศนะกับแผนกถัดไป...
                  </div>
                </div>
              )}

              {collabMessages.length === 0 && !collabLoading && (
                <div className="py-20 text-center text-slate-500 text-xs font-light space-y-2">
                  <span className="text-3xl block">🤝</span>
                  <p>กดปุ่ม **เริ่มต้นการระดมสมองของ AI** ทางด้านซ้าย<br/>เพื่อเชิญเลขาและผู้เชี่ยวชาญมาร่วมกันสกัดแผนงานชิ้นงานสำเร็จครับ</p>
                </div>
              )}

              <div ref={chatEndRef} />
            </div>

            {/* Chat Footer: Information */}
            <div className="p-3 bg-slate-950 border-t border-slate-900 text-[10px] text-slate-500 text-center shrink-0 font-light">
              * ข้อมูลบทสนทนาและการสั่งการจะอ้างอิงเป้าหมาย KPIs, SOP และข้อกฎหมายจัดซื้อจัดจ้างราชการของจังหวัดเชียงรายจริง
            </div>

          </div>

        </div>
      )}

    </div>
  );
}
