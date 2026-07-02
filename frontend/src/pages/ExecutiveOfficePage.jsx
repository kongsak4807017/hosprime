import { useEffect, useMemo, useState } from "react";
import { Brain, BriefcaseBusiness, ChartNoAxesCombined, Crown, FileOutput, Loader2, RefreshCw, Send, ShieldAlert } from "lucide-react";
import { toast } from "sonner";
import api, { formatApiError } from "@/lib/api";

const ICONS = {
  executive: Crown,
  planner: BriefcaseBusiness,
  analyst: ChartNoAxesCombined,
  knowledge: Brain,
  action: FileOutput,
};

const PROMPTS = {
  executive: "วันนี้ผู้บริหารควรให้ความสำคัญกับเรื่องใดมากที่สุด",
  planner: "สร้างแผนลด waiting time พร้อม owner timeline และ KPI",
  analyst: "วิเคราะห์ข้อมูลปัจจุบันและระบุความผิดปกติที่ควรตรวจสอบ",
  knowledge: "สรุปองค์ความรู้และเอกสารที่เกี่ยวข้อง พร้อมข้อจำกัดของหลักฐาน",
  action: "ร่างบันทึกข้อความจากข้อสั่งการนี้ และระบุจุดที่ต้องให้คนอนุมัติ",
};

function Metric({ label, value }) {
  return (
    <div className="rounded-xl border border-[#E1E5E2] bg-white p-4 shadow-sm">
      <div className="text-xs uppercase tracking-[0.12em] text-[#546E62]">{label}</div>
      <div className="mt-2 font-heading text-2xl font-semibold text-[#0F1F19]">{value}</div>
    </div>
  );
}

export default function ExecutiveOfficePage() {
  const [agents, setAgents] = useState([]);
  const [brief, setBrief] = useState(null);
  const [activeKey, setActiveKey] = useState("executive");
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [sessionId, setSessionId] = useState(null);
  const [loading, setLoading] = useState(true);
  const [sending, setSending] = useState(false);

  const active = useMemo(() => agents.find((item) => item.key === activeKey), [agents, activeKey]);

  const load = async () => {
    setLoading(true);
    try {
      const [agentRes, briefRes] = await Promise.all([
        api.get("/executive-office/agents"),
        api.get("/executive-office/brief"),
      ]);
      setAgents(agentRes.data);
      setBrief(briefRes.data);
    } catch (error) {
      toast.error(formatApiError(error));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { load(); }, []);

  const chooseAgent = (key) => {
    setActiveKey(key);
    setMessages([]);
    setSessionId(null);
    setInput("");
  };

  const send = async (event) => {
    event.preventDefault();
    const text = input.trim();
    if (!text || sending) return;
    setInput("");
    setMessages((items) => [...items, { role: "user", content: text }]);
    setSending(true);
    try {
      const { data } = await api.post("/executive-office/chat", {
        agent_key: activeKey,
        message: text,
        session_id: sessionId,
      }, { timeout: 150000 });
      setSessionId(data.session_id);
      setMessages((items) => [...items, {
        role: "assistant",
        content: data.reply,
        evidence: data.evidence || [],
        confidence: data.confidence,
        approvalRequired: data.approval_required,
      }]);
    } catch (error) {
      toast.error(formatApiError(error));
      setMessages((items) => items.slice(0, -1));
      setInput(text);
    } finally {
      setSending(false);
    }
  };

  const metrics = brief?.metrics || {};

  return (
    <div className="space-y-6" data-testid="executive-office-page">
      <div className="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
        <div>
          <div className="text-xs font-semibold uppercase tracking-[0.2em] text-[#546E62]">HosPrime AI Agent Office v2</div>
          <h1 className="mt-1 font-heading text-4xl font-medium text-[#0F1F19]">Executive Office</h1>
          <p className="mt-2 max-w-3xl text-sm text-[#546E62]">Core Office 5 บทบาทสำหรับงานบริหาร วางแผน วิเคราะห์ องค์ความรู้ และการผลิตชิ้นงาน</p>
        </div>
        <button onClick={load} disabled={loading} className="inline-flex items-center gap-2 rounded-lg border border-[#1E3F33] px-4 py-2 text-sm text-[#1E3F33] disabled:opacity-50">
          <RefreshCw className={`h-4 w-4 ${loading ? "animate-spin" : ""}`} /> อัปเดต
        </button>
      </div>

      <div className="flex gap-3 rounded-xl border border-amber-200 bg-amber-50 p-4 text-sm text-amber-950">
        <ShieldAlert className="h-5 w-5 shrink-0" />
        <div><strong>Prototype boundary:</strong> ตัวชี้วัดยังมาจาก operational collections เดิม ยังไม่ใช่ Management Data Mart ที่ผ่าน Data Governance เต็มรูปแบบ</div>
      </div>

      <div className="grid grid-cols-2 gap-3 md:grid-cols-3 xl:grid-cols-6">
        <Metric label="ผู้ป่วย" value={metrics.patients ?? "—"} />
        <Metric label="นัดวันนี้" value={metrics.appointments_today ?? "—"} />
        <Metric label="เสร็จแล้ว" value={metrics.completed_today ?? "—"} />
        <Metric label="แล็บค้าง" value={metrics.pending_labs ?? "—"} />
        <Metric label="ยาใกล้หมด" value={metrics.low_stock_items ?? "—"} />
        <Metric label="ลูกหนี้" value={metrics.outstanding_amount != null ? `${Number(metrics.outstanding_amount).toLocaleString()} ฿` : "—"} />
      </div>

      <div className="grid gap-3 md:grid-cols-5">
        {agents.map((agent) => {
          const Icon = ICONS[agent.key] || Brain;
          const selected = agent.key === activeKey;
          return (
            <button key={agent.key} onClick={() => chooseAgent(agent.key)} className={`rounded-xl border p-4 text-left ${selected ? "border-[#1E3F33] bg-[#1E3F33] text-white" : "border-[#E1E5E2] bg-white text-[#0F1F19]"}`}>
              <Icon className="h-5 w-5" />
              <div className="mt-3 text-sm font-semibold">{agent.name_th}</div>
              <div className={`mt-1 text-xs ${selected ? "text-white/70" : "text-[#546E62]"}`}>{agent.role}</div>
            </button>
          );
        })}
      </div>

      <div className="grid gap-5 xl:grid-cols-[300px_minmax(0,1fr)]">
        <aside className="space-y-4">
          <div className="rounded-xl border border-[#E1E5E2] bg-white p-5">
            <div className="text-xs uppercase tracking-[0.16em] text-[#546E62]">Active role</div>
            <div className="mt-2 font-heading text-xl text-[#0F1F19]">{active?.name_th || "กำลังโหลด"}</div>
            <p className="mt-2 text-sm leading-relaxed text-[#546E62]">{active?.mission}</p>
            <button onClick={() => setInput(PROMPTS[activeKey] || "")} className="mt-4 w-full rounded-lg border border-[#E1E5E2] px-3 py-2 text-left text-xs text-[#546E62] hover:border-[#4A6B5D]">
              {PROMPTS[activeKey] || "เริ่มสนทนา"}
            </button>
          </div>

          {brief?.risks?.length > 0 && (
            <div className="rounded-xl border border-[#E1E5E2] bg-white p-5">
              <div className="text-sm font-semibold text-[#0F1F19]">Risk radar</div>
              <div className="mt-3 space-y-2">
                {brief.risks.map((risk) => <div key={risk.key} className="rounded-lg bg-[#F9F9F8] p-3 text-xs"><b className="mr-2 text-[#D34228]">{risk.severity}</b>{risk.title}</div>)}
              </div>
            </div>
          )}
        </aside>

        <section className="flex min-h-[600px] flex-col overflow-hidden rounded-xl border border-[#E1E5E2] bg-white">
          <div className="border-b border-[#E1E5E2] px-5 py-4">
            <div className="font-heading text-lg text-[#0F1F19]">ทำงานร่วมกับ {active?.name_th}</div>
            <div className="mt-1 text-xs text-[#546E62]">คำตอบต้องแสดงหลักฐาน ความมั่นใจ และจุดอนุมัติของมนุษย์</div>
          </div>

          <div className="flex-1 space-y-4 overflow-y-auto p-5">
            {messages.length === 0 && !sending && <div className="py-20 text-center text-sm text-[#546E62]"><Brain className="mx-auto mb-3 h-10 w-10 text-[#4A6B5D]" />ระบุปัญหา เป้าหมาย ข้อจำกัด และผลลัพธ์ที่ต้องการ</div>}
            {messages.map((message, index) => (
              <div key={index} className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}>
                <div className={`max-w-[88%] rounded-2xl px-4 py-3 text-sm ${message.role === "user" ? "bg-[#1E3F33] text-white" : "bg-[#F2F0EB] text-[#0F1F19]"}`}>
                  <div className="whitespace-pre-wrap leading-relaxed">{message.content}</div>
                  {message.role === "assistant" && <div className="mt-3 border-t border-[#D8DDD9] pt-3 text-xs text-[#546E62]">
                    <div>Confidence: <b>{message.confidence || "not rated"}</b></div>
                    {message.approvalRequired && <div className="mt-1 font-semibold text-amber-700">ต้องให้ผู้มีอำนาจตรวจและอนุมัติก่อนดำเนินการ</div>}
                    {message.evidence?.length > 0 && <div className="mt-2">Evidence: {message.evidence.map((item) => item.label).join(" • ")}</div>}
                  </div>}
                </div>
              </div>
            ))}
            {sending && <div className="inline-flex items-center gap-2 rounded-xl bg-[#F2F0EB] px-4 py-3 text-sm text-[#546E62]"><Loader2 className="h-4 w-4 animate-spin" />กำลังวิเคราะห์...</div>}
          </div>

          <form onSubmit={send} className="flex gap-2 border-t border-[#E1E5E2] p-4">
            <textarea value={input} onChange={(event) => setInput(event.target.value)} rows={2} placeholder="พิมพ์โจทย์งาน..." className="flex-1 resize-none rounded-lg border border-[#E1E5E2] px-4 py-3 text-sm focus:border-[#1E3F33] focus:outline-none" />
            <button type="submit" disabled={sending || !input.trim()} className="rounded-lg bg-[#1E3F33] px-5 text-white disabled:opacity-50" aria-label="ส่งข้อความ"><Send className="h-4 w-4" /></button>
          </form>
        </section>
      </div>
    </div>
  );
}
