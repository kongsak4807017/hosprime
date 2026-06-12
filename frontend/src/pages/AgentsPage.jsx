import { useEffect, useRef, useState } from "react";
import {
  Banknote, Bot, Building2, FlaskConical, HeartPulse, Loader2, Pill, Plus, Send, Stethoscope, Trash2,
} from "lucide-react";
import { toast } from "sonner";
import api, { formatApiError } from "@/lib/api";
import { formatThaiDateTime } from "@/lib/helpers";

const ICONS = { building: Building2, stethoscope: Stethoscope, heart: HeartPulse, pill: Pill, flask: FlaskConical, banknote: Banknote };

export default function AgentsPage() {
  const [agents, setAgents] = useState([]);
  const [active, setActive] = useState(null);
  const [sessions, setSessions] = useState([]);
  const [sessionId, setSessionId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [sending, setSending] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    api.get("/agents").then((r) => setAgents(r.data));
  }, []);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, sending]);

  const selectAgent = async (agent) => {
    setActive(agent);
    setSessionId(null);
    setMessages([]);
    const { data } = await api.get(`/agents/${agent.key}/sessions`);
    setSessions(data);
  };

  const openSession = async (sid) => {
    const { data } = await api.get(`/agents/sessions/${sid}/messages`);
    setSessionId(sid);
    setMessages(data.messages);
  };

  const newChat = () => {
    setSessionId(null);
    setMessages([]);
  };

  const deleteSession = async (sid, e) => {
    e.stopPropagation();
    if (!window.confirm("ลบบทสนทนานี้?")) return;
    await api.delete(`/agents/sessions/${sid}`);
    setSessions((s) => s.filter((x) => x.id !== sid));
    if (sessionId === sid) newChat();
  };

  const send = async (e) => {
    e.preventDefault();
    const text = input.trim();
    if (!text || sending || !active) return;
    setInput("");
    setMessages((m) => [...m, { role: "user", content: text, created_at: new Date().toISOString() }]);
    setSending(true);
    try {
      const { data } = await api.post(`/agents/${active.key}/chat`, { message: text, session_id: sessionId }, { timeout: 150000 });
      setMessages((m) => [...m, { role: "assistant", content: data.reply, created_at: new Date().toISOString() }]);
      if (!sessionId) {
        setSessionId(data.session_id);
        const { data: s } = await api.get(`/agents/${active.key}/sessions`);
        setSessions(s);
      }
    } catch (err) {
      toast.error(formatApiError(err));
      setMessages((m) => m.slice(0, -1));
      setInput(text);
    } finally { setSending(false); }
  };

  return (
    <div className="space-y-6" data-testid="agents-page">
      <div>
        <div className="text-xs font-semibold uppercase tracking-[0.2em] text-[#546E62] mb-1">Digital Twin Agents</div>
        <h1 className="font-heading text-3xl md:text-4xl font-medium tracking-tight text-[#0F1F19]">หัวหน้างานดิจิทัล</h1>
        <p className="text-[#546E62] mt-2 text-sm max-w-2xl">
          AI ผู้เชี่ยวชาญเฉพาะทางประจำตำแหน่งหัวหน้างาน 6 ตำแหน่ง — เห็นข้อมูล real-time ของแผนกตัวเอง พร้อมให้คำปรึกษาเชิงปฏิบัติ
        </p>
      </div>

      {/* Agent cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 xl:grid-cols-6 gap-3">
        {agents.map((a) => {
          const Icon = ICONS[a.icon] || Bot;
          const isActive = active?.key === a.key;
          return (
            <button
              key={a.key}
              onClick={() => selectAgent(a)}
              data-testid={`agent-card-${a.key}`}
              className={`text-left border rounded-lg p-4 transition-all ${isActive ? "border-[#1E3F33] bg-[#1E3F33] text-white shadow-md" : "border-[#E1E5E2] bg-white hover:border-[#4A6B5D] hover:shadow-sm"}`}
            >
              <div className={`w-9 h-9 rounded-lg flex items-center justify-center mb-2 ${isActive ? "bg-white/15" : "bg-[#F2F0EB]"}`}>
                <Icon className={`w-4 h-4 ${isActive ? "text-white" : "text-[#1E3F33]"}`} />
              </div>
              <div className="text-sm font-medium leading-tight">{a.name}</div>
              <div className={`text-[10px] mt-1 ${isActive ? "text-white/70" : "text-[#546E62]"}`}>{a.name_en}</div>
            </button>
          );
        })}
      </div>

      {/* Chat area */}
      {active ? (
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-4">
          {/* Sessions */}
          <div className="bg-white border border-[#E1E5E2] rounded-lg shadow-sm p-3 lg:h-[560px] overflow-y-auto" data-testid="sessions-panel">
            <button onClick={newChat} data-testid="new-chat-btn" className="w-full inline-flex items-center justify-center gap-2 bg-[#1E3F33] text-white hover:bg-[#2C5A48] rounded-lg py-2 text-sm font-medium transition-colors mb-3">
              <Plus className="w-4 h-4" /> บทสนทนาใหม่
            </button>
            {sessions.length === 0 && <p className="text-xs text-[#546E62] text-center py-4">ยังไม่มีประวัติการสนทนา</p>}
            <div className="space-y-1">
              {sessions.map((s) => (
                <div
                  key={s.id}
                  onClick={() => openSession(s.id)}
                  data-testid="session-item"
                  className={`group flex items-center justify-between gap-2 rounded-lg px-3 py-2 text-sm cursor-pointer transition-colors ${sessionId === s.id ? "bg-[#1E3F33]/10 text-[#1E3F33] font-medium" : "hover:bg-[#F2F0EB] text-[#0F1F19]"}`}
                >
                  <div className="min-w-0">
                    <div className="truncate">{s.title}</div>
                    <div className="text-[10px] text-[#546E62]">{formatThaiDateTime(s.updated_at)}</div>
                  </div>
                  <button onClick={(e) => deleteSession(s.id, e)} className="opacity-0 group-hover:opacity-100 p-1 text-[#D34228] hover:bg-[#D34228]/10 rounded">
                    <Trash2 className="w-3 h-3" />
                  </button>
                </div>
              ))}
            </div>
          </div>

          {/* Messages */}
          <div className="lg:col-span-3 bg-white border border-[#E1E5E2] rounded-lg shadow-sm flex flex-col h-[560px]" data-testid="chat-panel">
            <div className="border-b border-[#E1E5E2] px-5 py-3">
              <div className="font-heading font-medium text-[#0F1F19]">{active.name}</div>
              <div className="text-xs text-[#546E62]">{active.description}</div>
            </div>
            <div className="flex-1 overflow-y-auto p-5 space-y-4">
              {messages.length === 0 && !sending && (
                <div className="text-center text-[#546E62] text-sm py-12">
                  <Bot className="w-10 h-10 mx-auto mb-3 text-[#4A6B5D]" />
                  เริ่มถาม {active.name} ได้เลย — Agent เห็นข้อมูล real-time ของแผนกอยู่แล้ว
                </div>
              )}
              {messages.map((m, i) => (
                <div key={i} className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}>
                  <div
                    className={`max-w-[80%] rounded-2xl px-4 py-3 text-sm whitespace-pre-wrap leading-relaxed ${m.role === "user" ? "bg-[#1E3F33] text-white rounded-br-sm" : "bg-[#F2F0EB] text-[#0F1F19] rounded-bl-sm"}`}
                    data-testid={m.role === "user" ? "user-message" : "assistant-message"}
                  >
                    {m.content}
                  </div>
                </div>
              ))}
              {sending && (
                <div className="flex justify-start">
                  <div className="bg-[#F2F0EB] rounded-2xl rounded-bl-sm px-4 py-3 text-sm text-[#546E62] inline-flex items-center gap-2" data-testid="agent-thinking">
                    <Loader2 className="w-4 h-4 animate-spin" /> กำลังวิเคราะห์ข้อมูล...
                  </div>
                </div>
              )}
              <div ref={bottomRef} />
            </div>
            <form onSubmit={send} className="border-t border-[#E1E5E2] p-3 flex gap-2">
              <input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder={`ถาม${active.name}...`}
                data-testid="agent-chat-input"
                className="flex-1 border border-[#E1E5E2] bg-white rounded-lg px-4 py-2.5 text-sm focus:border-[#1E3F33] focus:ring-1 focus:ring-[#1E3F33] focus:outline-none"
              />
              <button type="submit" disabled={sending || !input.trim()} data-testid="agent-send-btn" className="inline-flex items-center gap-2 bg-[#1E3F33] text-white hover:bg-[#2C5A48] rounded-lg px-5 py-2.5 text-sm font-medium transition-colors disabled:opacity-50">
                <Send className="w-4 h-4" />
              </button>
            </form>
          </div>
        </div>
      ) : (
        <div className="bg-[#F2F0EB] border border-[#E1E5E2] rounded-lg p-10 text-center text-[#546E62]" data-testid="agents-placeholder">
          เลือกหัวหน้างานด้านบนเพื่อเริ่มสนทนา
        </div>
      )}
    </div>
  );
}
