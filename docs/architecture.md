# สถาปัตยกรรมระบบ (Architecture Specification)
## HosPrime Milestone 1: Knowledge Oracle MVP

สถาปัตยกรรมของ HosPrime ถูกออกแบบโดยเน้นการทำ **Local-First RAG & Sovereign AI** เพื่อเก็บรักษาความปลอดภัยของข้อมูลในองค์กรและรองรับการขยายตัวสู่ระบบอัจฉริยะแบบกระจายศูนย์ (Federated Intelligence) ในระดับจังหวัดและประเทศ

---

## 📊 แผนภาพการไหลของข้อมูล (RAG Data Flow Diagram)

```mermaid
graph TD
    %% 1. Ingestion Pipeline
    subgraph Ingestion Pipeline (ระบบนำเข้าความรู้)
        A[อัปโหลดไฟล์เอกสาร PDF/DOCX/TXT/MD] --> B[KnowledgeIngestionAgent]
        B --> C[DocumentParser - สกัด Text รายหน้า]
        C --> D[DocumentClassificationAgent - แยกประเภท SOP/Policy/Report]
        C --> E[MetadataAgent - ตรวจจับ ปี/แผนก/ความปลอดภัย]
        E -->|สกัดเอนทิตี/บทบาท| F[(SQLite: Entity Relations)]
        C --> G[ChunkingAgent - แบ่งท่อนข้อความ 800 ตัวอักษร]
        G --> H[EmbeddingAgent - คำนวณ Vector ด้วย text-embedding-004]
        H --> I[(SQLite: Document & Chunk Vector)]
    end

    %% 2. Retrieval & RAG Pipeline
    subgraph Retrieval & RAG Pipeline (ระบบสืบค้นและตอบคำถาม)
        J[ผู้ใช้ป้อนคำถามภาษาไทย/อังกฤษ] --> K[RetrievalAgent - ดึงเวกเตอร์คำถาม]
        K -->|เปรียบเทียบ Cosine Similarity| I
        I -->|ส่งคืน Chunks ที่คล้ายกัน| L[RerankingAgent - ปรับน้ำหนักตามแฟ้มงาน]
        L --> M[AnswerGenerationAgent - สังเคราะห์ RAG ด้วย gemini-1.5-flash]
        M -->|วิเคราะห์หลักฐานและจัดโครงสร้าง| N[CitationAgent - แมปหมายเลขแหล่งอ้างอิง]
        N --> O[ส่งผลลัพธ์คำตอบที่มีความน่าเชื่อถือสูงและโปร่งใส]
    end

    %% 3. Feedback Loop
    subgraph Feedback Loop
        O --> P[ผู้ใช้ส่ง Thumbs Up / Down]
        P --> Q[FeedbackLearningAgent]
        Q -->|บันทึกประเมินเพื่อจูน Rerank| R[(SQLite: Query & Feedback Log)]
    end
```

---

## ⚙️ หน้าที่ของ Agents ทั้ง 10 ตัวใน Milestone 1

1. **`KnowledgeIngestionAgent`**: ประสานงานกระบวนการอัปโหลด นำเข้าไฟล์ และเรียกใช้ Parser
2. **`DocumentClassificationAgent`**: แยกประเภทของเอกสาร (SOP, Policy, Report, Meeting Notes) และกำหนดระดับความมั่นใจของการแยกแยะ
3. **`MetadataAgent`**: ตรวจหาเมตาดาตาสำคัญ (ปี, เจ้าของ, แผนก, โปรแกรมงาน) และวิเคราะห์ความสัมพันธ์เชิงบทบาทและสายงานเบื้องต้น (HODT Relations)
4. **`ChunkingAgent`**: แบ่งท่อนข้อความขนาด ~800 ตัวอักษรโดยรักษาโครงสร้างคำพูดไม่ให้ประโยคขาดออกจากกัน
5. **`EmbeddingAgent`**: เชื่อมโยง Gemini API นำ Chunk ไปสร้าง Vector Embedding ขนาด 768 มิติ
6. **`RetrievalAgent`**: ค้นหา Chunk ที่มีค่า Cosine Similarity สูงสุดกับคำถามผู้ใช้งาน
7. **`RerankingAgent`**: กรองข้อมูลและคำนวณปรับคะแนนความเกี่ยวข้อง โดยเพิ่มน้ำหนักในกรณีที่เมตาดาตาของเอกสาร (เช่น โปรแกรมงานหรือแผนก) ตรงกับคีย์เวิร์ดในคำถามของผู้ใช้
8. **`AnswerGenerationAgent`**: สร้างคำตอบ RAG ในรูปแบบ Executive Summary, Key findings, Evidence, Caution/limitation และ Recommended next step โดยอยู่บนกฎเกณฑ์ **"ห้ามปั้นแต่งข้อมูลเด็ดขาด (No evidence -> no answer)"**
9. **`CitationAgent`**: ทำแผนผังและจับคู่เนื้อหาคำตอบไปยังแหล่งอ้างอิงรายชิ้นส่วน และรายงานค่าความเชื่อมั่นโดยเฉลี่ย
10. **`FeedbackLearningAgent`**: จัดเก็บประวัติการส่งความเห็นของผู้ใช้ลงใน Query logs เพื่อช่วยประเมินการทำงาน RAG ในอนาคต
