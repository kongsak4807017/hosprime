import { useCallback, useEffect, useRef, useState } from "react";
import ForceGraph2D from "react-force-graph-2d";
import { Loader2, RefreshCw, Send, Sparkles, X } from "lucide-react";
import { toast } from "sonner";
import api, { formatApiError } from "@/lib/api";
import { useAuth } from "@/context/AuthContext";
import { formatThaiDateTime } from "@/lib/helpers";

const BUILD_ROLES = ["admin", "doctor"];

export default function GraphPage() {
  const { user } = useAuth();
  const [graph, setGraph] = useState({ nodes: [], edges: [], meta: null, node_types: {} });
  const [typeFilter, setTypeFilter] = useState("");
  const [building, setBuilding] = useState(false);
  const [selected, setSelected] = useState(null);
  const [question, setQuestion] = useState("");
  const [asking, setAsking] = useState(false);
  const [answer, setAnswer] = useState(null);
  const containerRef = useRef(null);
  const [width, setWidth] = useState(800);

  const fetchGraph = useCallback(() => {
    api.get("/graph", { params: typeFilter ? { node_type: typeFilter } : {} }).then((r) => setGraph(r.data));
  }, [typeFilter]);

  useEffect(() => { fetchGraph(); }, [fetchGraph]);

  useEffect(() => {
    const update = () => containerRef.current && setWidth(containerRef.current.offsetWidth);
    update();
    window.addEventListener("resize", update);
    return () => window.removeEventListener("resize", update);
  }, []);

  const build = async () => {
    setBuilding(true);
    try {
      const { data } = await api.post("/graph/build");
      toast.success(`สร้างกราฟสำเร็จ: ${data.node_count} โหนด, ${data.edge_count} ความสัมพันธ์`);
      fetchGraph();
    } catch (err) { toast.error(formatApiError(err)); } finally { setBuilding(false); }
  };

  const ask = async (e) => {
    e.preventDefault();
    if (!question.trim()) return;
    setAsking(true);
    setAnswer(null);
    try {
      const { data } = await api.post("/graph/query", { question }, { timeout: 120000 });
      setAnswer(data);
    } catch (err) { toast.error(formatApiError(err)); } finally { setAsking(false); }
  };

  const onNodeClick = async (node) => {
    try {
      const { data } = await api.get(`/graph/node/${encodeURIComponent(node.id)}/neighbors`);
      setSelected(data);
    } catch (err) { toast.error(formatApiError(err)); }
  };

  const nodeTypes = graph.node_types || {};
  const graphData = {
    nodes: graph.nodes.map((n) => ({ id: n.key, name: n.label, type: n.type, color: nodeTypes[n.type]?.color || "#546E62", props: n.props })),
    links: graph.edges.map((e) => ({ source: e.source, target: e.target, label: e.label, weight: e.weight })),
  };

  return (
    <div className="space-y-6" data-testid="graph-page">
      <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
        <div>
          <div className="text-xs font-semibold uppercase tracking-[0.2em] text-[#546E62] mb-1">Knowledge Graph ระดับหน่วยงาน</div>
          <h1 className="font-heading text-3xl md:text-4xl font-medium tracking-tight text-[#0F1F19]">กราฟความรู้ทางการแพทย์</h1>
          {graph.meta && (
            <p className="text-xs text-[#546E62] mt-1">
              สร้างล่าสุด {formatThaiDateTime(graph.meta.built_at)} โดย {graph.meta.built_by} • {graph.meta.node_count} โหนด / {graph.meta.edge_count} ความสัมพันธ์
            </p>
          )}
        </div>
        {BUILD_ROLES.includes(user?.role) && (
          <button onClick={build} disabled={building} data-testid="build-graph-btn" className="inline-flex items-center gap-2 bg-[#1E3F33] text-white hover:bg-[#2C5A48] rounded-lg px-5 py-2.5 font-medium transition-colors disabled:opacity-60">
            {building ? <Loader2 className="w-4 h-4 animate-spin" /> : <RefreshCw className="w-4 h-4" />}
            {building ? "กำลังสร้างกราฟ..." : "สร้าง/อัปเดตกราฟ"}
          </button>
        )}
      </div>

      {/* AI Query */}
      <div className="bg-white border border-[#E1E5E2] rounded-lg p-5 shadow-sm space-y-3" data-testid="graph-query-panel">
        <div className="flex items-center gap-2 text-sm font-semibold text-[#0F1F19]">
          <Sparkles className="w-4 h-4 text-[#CC5A3A]" /> ถามกราฟด้วยภาษาไทย (AI)
        </div>
        <form onSubmit={ask} className="flex gap-2">
          <input
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder='เช่น "ผู้ป่วยคนไหนแพ้ Penicillin บ้าง", "ยาที่วิชัยใช้มีตัวไหนตีกันไหม"'
            data-testid="graph-question-input"
            className="flex-1 border border-[#E1E5E2] bg-white rounded-lg px-4 py-2.5 text-sm focus:border-[#1E3F33] focus:ring-1 focus:ring-[#1E3F33] focus:outline-none"
          />
          <button type="submit" disabled={asking} data-testid="graph-ask-btn" className="inline-flex items-center gap-2 bg-[#1E3F33] text-white hover:bg-[#2C5A48] rounded-lg px-5 py-2.5 text-sm font-medium transition-colors disabled:opacity-60">
            {asking ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />} ถาม
          </button>
        </form>
        {answer && (
          <div className="bg-[#F2F0EB] border border-[#E1E5E2] rounded-lg p-4 text-sm whitespace-pre-wrap leading-relaxed" data-testid="graph-answer">
            {answer.answer}
          </div>
        )}
      </div>

      {/* Filters */}
      <div className="flex flex-wrap gap-2">
        <button
          onClick={() => setTypeFilter("")}
          className={`text-xs rounded-full px-3 py-1.5 border transition-colors ${!typeFilter ? "bg-[#1E3F33] text-white border-[#1E3F33]" : "bg-white border-[#E1E5E2] text-[#546E62] hover:bg-[#F2F0EB]"}`}
          data-testid="filter-all"
        >
          ทั้งหมด ({graph.nodes.length})
        </button>
        {Object.entries(nodeTypes).map(([key, meta]) => (
          <button
            key={key}
            onClick={() => setTypeFilter(typeFilter === key ? "" : key)}
            className={`text-xs rounded-full px-3 py-1.5 border transition-colors inline-flex items-center gap-1.5 ${typeFilter === key ? "bg-[#1E3F33] text-white border-[#1E3F33]" : "bg-white border-[#E1E5E2] text-[#546E62] hover:bg-[#F2F0EB]"}`}
            data-testid={`filter-${key}`}
          >
            <span className="w-2.5 h-2.5 rounded-full" style={{ background: meta.color }} />
            {meta.label}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        {/* Graph canvas */}
        <div ref={containerRef} className={`bg-white border border-[#E1E5E2] rounded-lg shadow-sm overflow-hidden relative ${selected ? "lg:col-span-2" : "lg:col-span-3"}`} data-testid="graph-canvas">
          {graph.nodes.length === 0 ? (
            <div className="h-[560px] flex flex-col items-center justify-center text-[#546E62] gap-3">
              <p>ยังไม่มีกราฟ — กดปุ่ม "สร้าง/อัปเดตกราฟ" เพื่อสร้างจากข้อมูลโรงพยาบาล</p>
            </div>
          ) : (
            <ForceGraph2D
              graphData={graphData}
              width={selected ? Math.max(300, width - 0) : width}
              height={560}
              backgroundColor="#FDFDFC"
              nodeLabel={(n) => `${n.name} (${nodeTypes[n.type]?.label || n.type})`}
              nodeColor={(n) => n.color}
              nodeRelSize={5}
              linkColor={() => "#C8CFC9"}
              linkWidth={(l) => Math.min(3, l.weight)}
              linkDirectionalArrowLength={3}
              linkDirectionalArrowRelPos={1}
              linkLabel={(l) => l.label}
              onNodeClick={onNodeClick}
              nodeCanvasObjectMode={() => "after"}
              nodeCanvasObject={(node, ctx, globalScale) => {
                if (globalScale < 1.2) return;
                const label = node.name.length > 18 ? node.name.slice(0, 18) + "…" : node.name;
                ctx.font = `${10 / globalScale}px IBM Plex Sans Thai, sans-serif`;
                ctx.textAlign = "center";
                ctx.textBaseline = "top";
                ctx.fillStyle = "#546E62";
                ctx.fillText(label, node.x, node.y + 6);
              }}
            />
          )}
        </div>

        {/* Node detail panel */}
        {selected && (
          <div className="bg-white border border-[#E1E5E2] rounded-lg p-5 shadow-sm h-[560px] overflow-y-auto" data-testid="node-detail-panel">
            <div className="flex items-start justify-between mb-3">
              <div>
                <span className="text-[10px] uppercase tracking-wider rounded-full px-2 py-0.5" style={{ background: `${nodeTypes[selected.node.type]?.color}20`, color: nodeTypes[selected.node.type]?.color }}>
                  {nodeTypes[selected.node.type]?.label || selected.node.type}
                </span>
                <h3 className="font-heading text-lg font-medium text-[#0F1F19] mt-1">{selected.node.label}</h3>
              </div>
              <button onClick={() => setSelected(null)} className="p-1 hover:bg-[#F2F0EB] rounded"><X className="w-4 h-4" /></button>
            </div>
            {Object.entries(selected.node.props || {}).filter(([, v]) => v).map(([k, v]) => (
              <div key={k} className="text-xs text-[#546E62] mb-1">{k}: <span className="text-[#0F1F19] font-medium">{String(v)}</span></div>
            ))}
            <div className="text-xs font-semibold uppercase tracking-wider text-[#546E62] mt-4 mb-2">
              ความสัมพันธ์ ({selected.edges.length})
            </div>
            <div className="space-y-2">
              {selected.edges.map((e) => {
                const isOut = e.source === selected.node.key;
                const otherKey = isOut ? e.target : e.source;
                const other = selected.neighbors.find((n) => n.key === otherKey);
                return (
                  <div key={e.key} className="border border-[#E1E5E2] rounded-lg p-2.5 text-sm">
                    <span className="text-xs text-[#CC5A3A] font-medium">{isOut ? "→" : "←"} {e.label}</span>
                    <div className="font-medium text-[#0F1F19]">{other?.label || otherKey}</div>
                    {e.props?.description && <div className="text-xs text-[#D34228] mt-1">⚠ {e.props.description}</div>}
                  </div>
                );
              })}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
