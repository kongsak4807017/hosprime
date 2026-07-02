import { useState, useEffect } from 'react';
import { api } from '../../lib/api';

export function GraphBrainTab() {
  const [loading, setLoading] = useState(false);
  const [apiResult, setApiResult] = useState<any>(null);
  const [selectedNode, setSelectedNode] = useState<any>(null);

  const fetchGraph = async () => {
    setLoading(true);
    setApiResult(null);
    setSelectedNode(null);
    try {
      const data = await api.getGraphNetwork();
      setApiResult(data);
    } catch (e) {
      setApiResult({ error: "ไม่สามารถติดต่อฐานข้อมูลความสัมพันธ์ได้" });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchGraph();
  }, []);

  const getNodeColor = (type: string) => {
    switch (type) {
      case 'Organization': return '#10b981'; // emerald
      case 'Department': return '#0ea5e9'; // sky
      case 'Role': return '#f59e0b'; // amber
      case 'Program': return '#f43f5e'; // rose
      default: return '#6366f1'; // indigo
    }
  };

  const getNodeIcon = (type: string) => {
    switch (type) {
      case 'Organization': return '🏢';
      case 'Department': return '👥';
      case 'Role': return '👑';
      case 'Program': return '📂';
      default: return '📄';
    }
  };

  return (
    <div className="max-w-5xl mx-auto space-y-6 animate-fade-in">
      <div>
        <h2 className="text-2xl font-bold tracking-tight text-white font-outfit">โครงข่ายสมองระดับจังหวัด (Graph Brain)</h2>
        <p className="text-slate-400 text-xs">โครงข่ายเชื่อมโยงใยแมงมุมแสดงความสัมพันธ์ระหว่าง คน แผนก นโยบาย และเป้าหมาย KPIs จากตารางฐานข้อมูล SQLite HODT</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-5 gap-6 items-start">
        <div className="md:col-span-3 space-y-6">
          <div className="flex gap-2">
            <button
              onClick={fetchGraph}
              disabled={loading}
              className="px-5 py-2.5 bg-slate-900 border border-slate-800 hover:border-gold-500/50 hover:bg-slate-800/20 text-xs font-semibold rounded-lg text-slate-200 transition-all flex-1"
            >
              {loading ? "กำลังโหลดโครงข่าย..." : "รีโหลดแผนผังความสัมพันธ์จาก SQLite DB"}
            </button>
          </div>

          {/* SVG Visualizer */}
          {apiResult && apiResult.nodes && (
            <div className="relative w-full border border-slate-800 bg-slate-950/80 rounded-2xl p-4 overflow-hidden shadow-2xl flex flex-col items-center">
              <svg width="100%" height="360" viewBox="0 0 560 360" className="max-w-full">
                <defs>
                  <marker id="arrow" viewBox="0 0 10 10" refX="22" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                    <path d="M 0 0 L 10 5 L 0 10 z" fill="#cbd5e1" opacity="0.4" />
                  </marker>
                </defs>

                {/* Draw links */}
                {apiResult.links && apiResult.links.map((link: any, i: number) => {
                  const getPos = (nodeId: string) => {
                    const idx = apiResult.nodes.findIndex((n: any) => n.id === nodeId);
                    if (idx === -1) return { x: 280, y: 180 };
                    const angle = (idx / apiResult.nodes.length) * 2 * Math.PI;
                    const offset = (idx % 2 === 0) ? 0.95 : 1.1;
                    return {
                      x: 280 + 130 * Math.cos(angle) * offset,
                      y: 180 + 130 * Math.sin(angle) * offset
                    };
                  };
                  const srcPos = getPos(link.source);
                  const tgtPos = getPos(link.target);
                  return (
                    <g key={`link-${i}`}>
                      <line
                        x1={srcPos.x}
                        y1={srcPos.y}
                        x2={tgtPos.x}
                        y2={tgtPos.y}
                        stroke="#475569"
                        strokeWidth="1.5"
                        strokeDasharray="4 2"
                        opacity="0.6"
                        markerEnd="url(#arrow)"
                      />
                      <text
                        x={(srcPos.x + tgtPos.x) / 2}
                        y={(srcPos.y + tgtPos.y) / 2 - 5}
                        fill="#94a3b8"
                        fontSize="8"
                        textAnchor="middle"
                        className="select-none font-mono"
                      >
                        {link.type}
                      </text>
                    </g>
                  );
                })}

                {/* Draw nodes */}
                {apiResult.nodes.map((node: any, idx: number) => {
                  const angle = (idx / apiResult.nodes.length) * 2 * Math.PI;
                  const offset = (idx % 2 === 0) ? 0.95 : 1.1;
                  const x = 280 + 130 * Math.cos(angle) * offset;
                  const y = 180 + 130 * Math.sin(angle) * offset;
                  const color = getNodeColor(node.type);
                  return (
                    <g 
                      key={`node-${idx}`} 
                      className="cursor-pointer group"
                      onClick={() => setSelectedNode(node)}
                    >
                      <circle
                        cx={x}
                        cy={y}
                        r="16"
                        fill={color}
                        className="transition-all duration-300 group-hover:scale-125 group-hover:stroke-gold-400 group-hover:stroke-2"
                        stroke={selectedNode?.id === node.id ? "#e2e8f0" : "#0f172a"}
                        strokeWidth="2"
                      />
                      <circle
                        cx={x}
                        cy={y}
                        r="20"
                        fill="none"
                        stroke={color}
                        strokeWidth="1"
                        opacity="0.2"
                        className="animate-ping"
                        style={{ animationDuration: '4s' }}
                      />
                      <text
                        x={x}
                        y={y + 30}
                        fill="#f8fafc"
                        fontSize="9"
                        fontWeight="600"
                        textAnchor="middle"
                        className="select-none drop-shadow"
                      >
                        {node.id}
                      </text>
                      <text
                        x={x}
                        y={y + 4}
                        fill="#0f172a"
                        fontSize="10"
                        fontWeight="bold"
                        textAnchor="middle"
                        className="select-none"
                      >
                        {getNodeIcon(node.type)}
                      </text>
                    </g>
                  );
                })}
              </svg>

              {/* Legend */}
              <div className="flex flex-wrap gap-4 mt-3 justify-center text-[10px] text-slate-400 select-none">
                <div className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full bg-emerald-500"></span> องค์กร (Org)</div>
                <div className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full bg-sky-500"></span> ฝ่ายงาน (Dept)</div>
                <div className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full bg-amber-500"></span> บทบาท (Role)</div>
                <div className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full bg-rose-500"></span> แฟ้มงาน (Prog)</div>
                <div className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full bg-indigo-500"></span> โครงการ/อื่นๆ</div>
              </div>

              {/* Node Detail Drawer */}
              {selectedNode && (
                <div className="w-full mt-4 p-4 bg-slate-900 border border-slate-800 rounded-xl space-y-2 animate-fade-in">
                  <div className="flex justify-between items-center pb-2 border-b border-slate-800">
                    <h4 className="text-xs font-bold text-white flex items-center gap-2">
                      <span className="w-2 h-2 rounded-full" style={{ backgroundColor: getNodeColor(selectedNode.type) }}></span>
                      {selectedNode.id}
                    </h4>
                    <span className="text-[9px] uppercase font-mono px-2 py-0.5 bg-slate-950 text-slate-400 rounded">
                      Type: {selectedNode.type}
                    </span>
                  </div>
                  <p className="text-[11px] text-slate-400 leading-relaxed font-light">
                    Node ความสัมพันธ์เชิงสืบสวนระดับองค์กร (HODT Graph) เพื่อหาตัวเชื่อมระหว่างบทบาท นโยบาย และหน่วยรับผิดชอบ
                  </p>
                </div>
              )}
            </div>
          )}

          {apiResult && apiResult.error && (
            <div className="p-4 bg-rose-950/20 border border-rose-800/40 rounded-xl text-rose-355 text-xs">
              {apiResult.error}
            </div>
          )}
        </div>

        <div className="md:col-span-2 space-y-6">
          <div className="glass p-6 rounded-2xl space-y-4">
            <h4 className="text-xs font-bold text-slate-200 uppercase tracking-wider">ความสัมพันธ์เชิง HODT</h4>
            <p className="text-xs text-slate-400 leading-relaxed font-light">
              เปลี่ยนข้อมูลคลังเอกสารแบนๆ ให้กลายเป็นความรู้เชิงกราฟ เพื่อให้เอเจนต์หลังบ้านทำความเข้าใจสายการบริหารและประเมินผลกระทบข้ามฝ่ายงานได้อย่างชาญฉลาด
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
