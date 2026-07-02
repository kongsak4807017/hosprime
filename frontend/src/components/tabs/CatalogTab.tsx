import { useState, useEffect } from 'react';
import { Search, Layers, Trash2, Users } from 'lucide-react';
import { api, DocumentResponse, EntityRelationResponse } from '../../lib/api';

export function CatalogTab() {
  const [catalog, setCatalog] = useState<DocumentResponse[]>([]);
  const [loading, setLoading] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedDocRelations, setSelectedDocRelations] = useState<EntityRelationResponse[]>([]);
  const [selectedDocId, setSelectedDocId] = useState<number | null>(null);

  const fetchCatalog = async () => {
    setLoading(true);
    try {
      const data = await api.getCatalog();
      setCatalog(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCatalog();
  }, []);

  const handleDelete = async (id: number) => {
    if (!confirm("คุณต้องการลบเอกสารนี้และดัชนี RAG ทั้งหมดใช่หรือไม่?")) return;
    try {
      await api.deleteDocument(id);
      fetchCatalog();
      if (selectedDocId === id) {
        setSelectedDocId(null);
        setSelectedDocRelations([]);
      }
    } catch (e) {
      alert("ไม่สามารถลบเอกสารได้");
    }
  };

  const handleViewRelations = async (docId: number) => {
    if (selectedDocId === docId) {
      // ปิดถ้ารายการซ้ำ
      setSelectedDocId(null);
      setSelectedDocRelations([]);
      return;
    }

    try {
      const data = await api.getDocumentRelations(docId);
      setSelectedDocRelations(data);
      setSelectedDocId(docId);
    } catch (e) {
      alert("ไม่สามารถดึงข้อมูลความสัมพันธ์เชิงลึกได้");
    }
  };

  // กรองตารางด้วยคำค้นหา
  const filteredCatalog = catalog.filter(doc => 
    doc.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    (doc.program && doc.program.toLowerCase().includes(searchTerm.toLowerCase())) ||
    (doc.department && doc.department.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      {/* Title */}
      <div>
        <h2 className="text-2xl font-bold tracking-tight text-white font-outfit">Knowledge Catalog</h2>
        <p className="text-slate-400 text-xs">รายการคลังความรู้ เมตาดาตา และระบบสกัดความสัมพันธ์ HODT Node</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 items-start">
        {/* Document List Table */}
        <div className="lg:col-span-2 space-y-4">
          <div className="glass p-4 rounded-xl flex items-center gap-2">
            <Search className="w-4 h-4 text-slate-500" />
            <input
              type="text"
              placeholder="ค้นหาเอกสารตามชื่อเรื่อง แผนก หรือแฟ้มงาน..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full bg-transparent border-none outline-none text-xs text-slate-200 placeholder-slate-500"
            />
          </div>

          <div className="glass rounded-2xl overflow-hidden border border-slate-800">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-slate-900/70 border-b border-slate-800 text-slate-400 text-[10px] uppercase font-bold tracking-wider">
                  <th className="p-4">ชื่อเรื่องเอกสาร</th>
                  <th className="p-4">หมวดหมู่/แฟ้มงาน</th>
                  <th className="p-4">ปี</th>
                  <th className="p-4 text-center">สถานะ RAG</th>
                  <th className="p-4 text-right">การจัดการ</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 text-xs text-slate-300">
                {filteredCatalog.map((doc) => (
                  <tr key={doc.id} className="hover:bg-slate-900/20 transition-colors">
                    <td className="p-4 font-semibold text-white max-w-[200px] truncate">{doc.title}</td>
                    <td className="p-4">
                      <div className="flex flex-col">
                        <span className="text-[10px] text-slate-500">ประเภท: {doc.document_type || 'N/A'}</span>
                        <span>โปรแกรม: {doc.program || 'N/A'}</span>
                      </div>
                    </td>
                    <td className="p-4 font-outfit">{doc.year || 'N/A'}</td>
                    <td className="p-4 text-center">
                      <span className={`inline-block text-[9px] font-bold px-2 py-0.5 rounded-full ${
                        doc.status === 'processed' 
                          ? 'bg-emerald-950 text-emerald-400 border border-emerald-800/40' 
                          : doc.status === 'failed'
                          ? 'bg-rose-950 text-rose-400 border border-rose-800/40'
                          : 'bg-amber-950 text-amber-400 border border-amber-800/40'
                      }`}>
                        {doc.status}
                      </span>
                    </td>
                    <td className="p-4 text-right space-x-2">
                      <button
                        onClick={() => handleViewRelations(doc.id)}
                        className="p-1.5 bg-slate-900 hover:bg-slate-800 text-slate-400 hover:text-gold-500 rounded transition-colors"
                        title="ดูความสัมพันธ์โครงสร้างองค์กร"
                      >
                        <Layers className="w-3.5 h-3.5" />
                      </button>
                      <button
                        onClick={() => handleDelete(doc.id)}
                        className="p-1.5 bg-slate-900 hover:bg-rose-950 text-slate-400 hover:text-rose-500 rounded transition-colors"
                        title="ลบเอกสาร"
                      >
                        <Trash2 className="w-3.5 h-3.5" />
                      </button>
                    </td>
                  </tr>
                ))}
                {filteredCatalog.length === 0 && !loading && (
                  <tr>
                    <td colSpan={5} className="p-8 text-center text-slate-500">
                      ไม่พบเอกสารในคลังความรู้
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>

        {/* Right Side: HODT Entity & Relation Graph Node list */}
        <div className="space-y-6">
          <div className="glass p-6 rounded-2xl space-y-4">
            <h3 className="text-sm font-semibold text-slate-200 flex items-center gap-2">
              <Users className="w-4 h-4 text-gold-500" />
              โครงสร้างความสัมพันธ์ (HODT Relations)
            </h3>
            {selectedDocId ? (
              <div className="space-y-3">
                <p className="text-[10px] text-slate-400">
                  ความสัมพันธ์เชิงบทบาทและสายบังคับบัญชาที่ AI สกัดจากเอกสารนี้ เพื่อสร้างความรอบรู้ระดับโครงสร้าง (Organization Memory)
                </p>
                <div className="space-y-2 max-h-96 overflow-y-auto pr-1">
                  {selectedDocRelations.map((rel) => (
                    <div key={rel.id} className="p-3 bg-slate-900/50 border border-slate-800 rounded-xl text-xs space-y-1">
                      <div className="flex items-center justify-between text-[10px] text-slate-500 mb-1">
                        <span>{rel.source_type || 'Node'} ➔ {rel.target_type || 'Node'}</span>
                      </div>
                      <div className="flex flex-wrap items-center gap-1.5">
                        <span className="font-semibold text-white bg-brand-900/20 px-1.5 py-0.5 rounded border border-brand-800/30">
                          {rel.source_node}
                        </span>
                        <span className="text-gold-500 italic text-[10px]">
                          -{rel.relation_type}-&gt;
                        </span>
                        <span className="font-semibold text-white bg-slate-950 px-1.5 py-0.5 rounded border border-slate-800">
                          {rel.target_node}
                        </span>
                      </div>
                    </div>
                  ))}
                  {selectedDocRelations.length === 0 && (
                    <p className="text-xs text-slate-500 text-center py-6">ไม่พบการระบุเอนทิตีที่ซับซ้อนในเอกสารนี้</p>
                  )}
                </div>
              </div>
            ) : (
              <div className="p-6 text-center text-slate-600 border border-dashed border-slate-800 rounded-xl text-xs">
                เลือกคลิกที่รูปปุ่มความสัมพันธ์ <Layers className="w-3.5 h-3.5 inline mx-1" /> ในตาราง เพื่อจำลองความสัมพันธ์ระดับสายงาน (Role/Org Network) ของเอกสาร
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
