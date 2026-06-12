import { useEffect, useState } from "react";
import { Cpu, Loader2, CheckCircle2, XCircle } from "lucide-react";
import { toast } from "sonner";
import api, { formatApiError } from "@/lib/api";

const inputCls =
  "w-full border border-[#E1E5E2] bg-white rounded-lg px-3 py-2 text-sm focus:border-[#1E3F33] focus:ring-1 focus:ring-[#1E3F33] focus:outline-none";

export default function AISettingsPage() {
  const [settings, setSettings] = useState(null);
  const [models, setModels] = useState({});
  const [apiKey, setApiKey] = useState("");
  const [saving, setSaving] = useState(false);
  const [testing, setTesting] = useState(false);
  const [testResult, setTestResult] = useState(null);

  useEffect(() => {
    api.get("/ai/settings").then((r) => {
      setSettings(r.data);
      setModels(r.data.available_models || {});
    });
  }, []);

  const set = (key, value) => setSettings((s) => ({ ...s, [key]: value }));

  const save = async () => {
    setSaving(true);
    try {
      const payload = {
        provider: settings.provider,
        llm_provider: settings.llm_provider,
        model: settings.model,
        base_url: settings.base_url,
      };
      if (apiKey) payload.api_key = apiKey;
      const { data } = await api.put("/ai/settings", payload);
      setSettings(data);
      setApiKey("");
      toast.success("บันทึกการตั้งค่า AI สำเร็จ");
    } catch (err) { toast.error(formatApiError(err)); } finally { setSaving(false); }
  };

  const test = async () => {
    setTesting(true);
    setTestResult(null);
    try {
      const { data } = await api.post("/ai/settings/test");
      setTestResult(data);
    } catch (err) {
      setTestResult({ success: false, error: formatApiError(err) });
    } finally { setTesting(false); }
  };

  if (!settings) return <div className="text-[#546E62]">กำลังโหลด...</div>;

  return (
    <div className="max-w-2xl space-y-6" data-testid="ai-settings-page">
      <div>
        <div className="text-xs font-semibold uppercase tracking-[0.2em] text-[#546E62] mb-1">ระบบ AI</div>
        <h1 className="font-heading text-3xl md:text-4xl font-medium tracking-tight text-[#0F1F19]">ตั้งค่า AI Engine</h1>
        <p className="text-[#546E62] mt-2 text-sm">เลือกผู้ให้บริการ AI สำหรับ Digital Twin Agents, Knowledge Graph และ Data Connector</p>
      </div>

      <div className="bg-white border border-[#E1E5E2] rounded-lg p-6 shadow-sm space-y-5">
        <div className="space-y-3">
          <label className="text-sm font-semibold text-[#0F1F19]">ผู้ให้บริการ AI</label>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            <button
              onClick={() => set("provider", "emergent")}
              data-testid="provider-emergent-btn"
              className={`text-left border rounded-lg p-4 transition-colors ${settings.provider === "emergent" ? "border-[#1E3F33] bg-[#1E3F33]/5 ring-1 ring-[#1E3F33]" : "border-[#E1E5E2] hover:bg-[#F2F0EB]"}`}
            >
              <div className="font-medium text-sm flex items-center gap-2"><Cpu className="w-4 h-4 text-[#1E3F33]" /> Emergent Universal Key</div>
              <div className="text-xs text-[#546E62] mt-1">ใช้ key กลางที่ติดตั้งแล้ว — เลือกได้ทั้ง OpenAI / Claude / Gemini ไม่ต้องใส่ key เพิ่ม</div>
            </button>
            <button
              onClick={() => set("provider", "custom")}
              data-testid="provider-custom-btn"
              className={`text-left border rounded-lg p-4 transition-colors ${settings.provider === "custom" ? "border-[#1E3F33] bg-[#1E3F33]/5 ring-1 ring-[#1E3F33]" : "border-[#E1E5E2] hover:bg-[#F2F0EB]"}`}
            >
              <div className="font-medium text-sm flex items-center gap-2"><Cpu className="w-4 h-4 text-[#CC5A3A]" /> Custom / Local AI</div>
              <div className="text-xs text-[#546E62] mt-1">เชื่อม endpoint แบบ OpenAI-compatible เช่น OpenAI, Ollama (local), LM Studio, vLLM, OpenRouter</div>
            </button>
          </div>
        </div>

        {settings.provider === "emergent" ? (
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="text-xs text-[#546E62]">ค่าย AI</label>
              <select
                value={settings.llm_provider}
                onChange={(e) => {
                  const p = e.target.value;
                  setSettings((s) => ({ ...s, llm_provider: p, model: (models[p] || [])[0] || "" }));
                }}
                className={inputCls}
                data-testid="llm-provider-select"
              >
                <option value="openai">OpenAI</option>
                <option value="anthropic">Anthropic (Claude)</option>
                <option value="gemini">Google (Gemini)</option>
              </select>
            </div>
            <div>
              <label className="text-xs text-[#546E62]">โมเดล</label>
              <select value={settings.model} onChange={(e) => set("model", e.target.value)} className={inputCls} data-testid="model-select">
                {(models[settings.llm_provider] || []).map((m) => <option key={m} value={m}>{m}</option>)}
              </select>
            </div>
          </div>
        ) : (
          <div className="space-y-3">
            <div>
              <label className="text-xs text-[#546E62]">Base URL (OpenAI-compatible) *</label>
              <input value={settings.base_url} onChange={(e) => set("base_url", e.target.value)} placeholder="เช่น http://localhost:11434/v1 หรือ https://api.openai.com/v1" className={inputCls} data-testid="base-url-input" />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="text-xs text-[#546E62]">API Key {settings.api_key_set && <span className="text-[#327A59]">(ตั้งค่าแล้ว {settings.api_key})</span>}</label>
                <input type="password" value={apiKey} onChange={(e) => setApiKey(e.target.value)} placeholder={settings.api_key_set ? "เว้นว่างเพื่อใช้ key เดิม" : "sk-... (เว้นว่างได้สำหรับ local)"} className={inputCls} data-testid="api-key-input" />
              </div>
              <div>
                <label className="text-xs text-[#546E62]">ชื่อโมเดล *</label>
                <input value={settings.model} onChange={(e) => set("model", e.target.value)} placeholder="เช่น llama3.1, gpt-4o" className={inputCls} data-testid="custom-model-input" />
              </div>
            </div>
          </div>
        )}

        <div className="flex gap-3 pt-2">
          <button onClick={save} disabled={saving} data-testid="ai-settings-save-btn" className="bg-[#1E3F33] text-white hover:bg-[#2C5A48] rounded-lg px-6 py-2.5 font-medium transition-colors disabled:opacity-60 inline-flex items-center gap-2">
            {saving && <Loader2 className="w-4 h-4 animate-spin" />} บันทึกการตั้งค่า
          </button>
          <button onClick={test} disabled={testing} data-testid="ai-settings-test-btn" className="border border-[#E1E5E2] bg-white text-[#0F1F19] hover:bg-[#F2F0EB] rounded-lg px-6 py-2.5 font-medium transition-colors disabled:opacity-60 inline-flex items-center gap-2">
            {testing && <Loader2 className="w-4 h-4 animate-spin" />} ทดสอบการเชื่อมต่อ
          </button>
        </div>

        {testResult && (
          <div className={`rounded-lg p-4 text-sm flex items-start gap-2 ${testResult.success ? "bg-[#327A59]/10 border border-[#327A59]/30 text-[#327A59]" : "bg-[#D34228]/10 border border-[#D34228]/30 text-[#D34228]"}`} data-testid="ai-test-result">
            {testResult.success ? <CheckCircle2 className="w-4 h-4 mt-0.5" /> : <XCircle className="w-4 h-4 mt-0.5" />}
            <span className="whitespace-pre-wrap">{testResult.success ? testResult.reply : testResult.error}</span>
          </div>
        )}
      </div>
    </div>
  );
}
