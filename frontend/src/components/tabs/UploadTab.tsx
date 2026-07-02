import { useState, useRef } from 'react';
import { Info, UploadCloud } from 'lucide-react';
import { api } from '../../lib/api';

interface UploadTabProps {
  onIngested: () => void;
}

export function UploadTab({ onIngested }: UploadTabProps) {
  const [file, setFile] = useState<File | null>(null);
  const [title, setTitle] = useState("");
  const [confidentiality, setConfidentiality] = useState("Internal");
  const [loading, setLoading] = useState(false);
  const [statusMsg, setStatusMsg] = useState<{ type: 'success' | 'error', text: string } | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const droppedFile = e.dataTransfer.files[0];
      setFile(droppedFile);
      setTitle(droppedFile.name.replace(/\.[^/.]+$/, ""));
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0];
      setFile(selectedFile);
      setTitle(selectedFile.name.replace(/\.[^/.]+$/, ""));
    }
  };

  const handleUploadSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;

    setLoading(true);
    setStatusMsg(null);

    try {
      await api.uploadDocument(file, title, confidentiality);
      setStatusMsg({
        type: 'success',
        text: `อัปโหลดและประมวลผลข้อมูลเอกสาร "${title}" สำเร็จ! เอกสารอยู่ระหว่างรอแอดมินอนุมัติเพื่อเข้าระบบหลักการสืบค้น`
      });
      setFile(null);
      setTitle("");
      onIngested();
    } catch (err: any) {
      setStatusMsg({
        type: 'error',
        text: err.message || "เกิดข้อผิดพลาดในการประมวลผลเอกสาร"
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      {/* Title */}
      <div>
        <h2 className="text-2xl font-bold tracking-tight text-white font-outfit">Upload Knowledge</h2>
        <p className="text-slate-400 text-xs">นำเข้าเอกสารคลังความรู้ใหม่เข้าระบบประมวลผล (PDF, DOCX, TXT, MD)</p>
      </div>

      <div className="glass p-8 rounded-2xl space-y-6">
        {statusMsg && (
          <div className={`p-4 rounded-xl text-xs flex items-start gap-2 border ${
            statusMsg.type === 'success' 
              ? 'bg-emerald-950/20 border-emerald-800/40 text-emerald-300' 
              : 'bg-rose-950/20 border-rose-800/40 text-rose-300'
          }`}>
            <Info className="w-4 h-4 flex-shrink-0 mt-0.5" />
            <span>{statusMsg.text}</span>
          </div>
        )}

        <form onSubmit={handleUploadSubmit} className="space-y-6">
          {/* File Upload Drag area */}
          <div
            onDragOver={handleDragOver}
            onDrop={handleDrop}
            onClick={() => fileInputRef.current?.click()}
            className="border-2 border-dashed border-slate-800 hover:border-gold-500/50 rounded-2xl p-12 text-center cursor-pointer transition-all duration-200 bg-slate-900/10 hover:bg-slate-900/30 flex flex-col items-center justify-center space-y-4"
          >
            <input
              type="file"
              ref={fileInputRef}
              onChange={handleFileChange}
              accept=".pdf,.docx,.txt,.md"
              className="hidden"
            />
            <div className="w-16 h-16 bg-slate-950 rounded-full flex items-center justify-center text-slate-500 border border-slate-800">
              <UploadCloud className="w-8 h-8" />
            </div>
            {file ? (
              <div>
                <p className="text-sm font-semibold text-white">{file.name}</p>
                <p className="text-[10px] text-slate-500 mt-1">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
              </div>
            ) : (
              <div>
                <p className="text-sm font-semibold text-slate-300">ลากและวางเอกสารที่นี่ หรือคลิกเพื่อเปิดหาไฟล์</p>
                <p className="text-[10px] text-slate-500 mt-1">รองรับเฉพาะ PDF, DOCX, TXT และ MD (ขนาดสูงสุด 20MB)</p>
              </div>
            )}
          </div>

          {file && (
            <div className="space-y-4 animate-fade-in">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {/* Document Title input */}
                <div className="space-y-2">
                  <label className="text-xs text-slate-400 font-medium">ชื่อเรื่องเอกสาร</label>
                  <input
                    type="text"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    required
                    className="w-full bg-slate-950 border border-slate-800 focus:border-gold-500 rounded-xl px-4 py-2.5 text-xs text-slate-100 outline-none"
                  />
                </div>

                {/* Confidentiality selection */}
                <div className="space-y-2">
                  <label className="text-xs text-slate-400 font-medium">ชั้นความลับ (Confidentiality)</label>
                  <select
                    value={confidentiality}
                    onChange={(e) => setConfidentiality(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 focus:border-gold-500 rounded-xl px-4 py-2.5 text-xs text-slate-100 outline-none"
                  >
                    <option value="Public">Public (สาธารณะ)</option>
                    <option value="Internal">Internal (ใช้เฉพาะภายใน)</option>
                    <option value="Confidential">Confidential (ความลับสูง)</option>
                  </select>
                </div>
              </div>

              {/* Submit button */}
              <button
                type="submit"
                disabled={loading}
                className="w-full py-3 bg-gradient-to-r from-brand-700 to-brand-600 hover:from-brand-600 hover:to-gold-500 text-white rounded-xl text-sm font-semibold transition-all duration-200 flex items-center justify-center gap-2"
              >
                {loading ? (
                  <>
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                    <span>กำลังวิเคราะห์และประมวลผล RAG Pipeline...</span>
                  </>
                ) : (
                  <span>วิเคราะห์และบันทึกคลังความรู้</span>
                )}
              </button>
            </div>
          )}
        </form>
      </div>
    </div>
  );
}
