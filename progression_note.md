# Progression Note: HosPrime Milestone 1 - Knowledge Oracle MVP

เอกสารนี้บันทึกสถานะการพัฒนาระบบ HosPrime Milestone 1 เพื่อให้ผู้พัฒนาหรือ AI Agent ตัวอื่นสามารถทำงานต่อร่วมกับระบบ KIMI CLI หรือเครืองมือสั่งการอื่นๆ ได้อย่างราบรื่น

---

## 1. สถานะปัจจุบัน (สิ่งที่ได้ดำเนินการไปแล้ว)
ขณะนี้ได้ทำการออกแบบและเขียนโครงสร้างพื้นฐานระบบหลังบ้าน (Backend Skeleton & Database Models) รวมถึงระบบ RAG Pipeline เสร็จสิ้นแล้ว โดยมีโครงสร้างไฟล์จริงดังนี้:

### โครงสร้างระบบหลังบ้าน (Backend):
- **`backend/.env`**: เก็บค่า Configuration เช่น Gemini API Key และ SQLite DB URL
- **`backend/requirements.txt`**: กำหนดชุดไลบรารีที่จำเป็น (FastAPI, SQLAlchemy, google-generativeai, pypdf, python-docx, etc.)
- **`backend/app/main.py`**: ตั้งค่า FastAPI หลัก, จัดการ CORS, เชื่อมต่อ Router และสั่งเตรียมสร้างตารางข้อมูล SQLite
- **`backend/app/core/config.py`**: ตัวแปรและสภาพแวดล้อมระบบพร้อมฟังก์ชันตรวจสอบความพร้อมของโฟลเดอร์เก็บข้อมูล
- **`backend/app/db/session.py`**: ตัวเชื่อมต่อ SQLite Database
- **`backend/app/db/models.py`**: โมเดล SQL ประกอบด้วยตารางเอกสาร (`Document`), ท่อนความรู้ (`DocumentChunk`), ประวัติถามตอบ (`QueryLog`), ประวัติการทำงานเอเจนต์ (`AgentLog`) และตารางความสัมพันธ์เชิง HODT (`EntityRelation`)
- **`backend/app/schemas/schemas.py`**: Pydantic models สำหรับใช้รับส่งและตรวจสอบข้อมูลผ่าน API
- **`backend/app/services/document_parser.py`**: ระบบเปิดอ่านและสกัดข้อความจริงจากไฟล์ PDF, DOCX, TXT และ MD
- **`backend/app/services/gemini_service.py`**: บริการเรียกใช้งานโมเดล Gemini (`gemini-1.5-flash` สำหรับ RAG/QA และ `text-embedding-004` สำหรับ Embedding) พร้อมระบบ **Fallback/Mock Mode สำหรับทดสอบออฟไลน์**
- **`backend/app/agents/agents.py`**: รวมศูนย์การทำงานของ AI Agent Services ทั้ง 10 ตัว (Ingestion, Classification, Metadata, Chunking, Embedding, Retrieval, Reranking, AnswerGen, Citation, Feedback)
- **`backend/app/api/endpoints/`**: API endpoints ครบถ้วน (documents.py สำหรับจัดการไฟล์, oracle.py สำหรับการสืบค้น RAG, admin.py สำหรับอนุมัติเอกสาร)
- **`backend/app/api/router.py`**: ตัวจัดการเส้นทาง API หลัก
- **`backend/app/db/bootstrap.py`**: สคริปต์สแกนเอกสารทดสอบในระบบ ล้างฐานข้อมูล และประมวลผล RAG Pipeline เข้าสู่คลังความรู้พร้อมใช้งานเดโม

### คลังข้อมูลเดโม (Demo Dataset):
สร้างไฟล์ Markdown (.md) จำลองข้อมูลตามสถานการณ์และคำถามเดโม 20 คำถามครบทั้ง 5 ด้านในโฟลเดอร์ `demo_data/`:
1. `pm25_actionplan_2568.md` - แผนควบคุมฝุ่นละออง PM2.5, การแจกจ่ายหน้ากาก N95
2. `tb_active_case_finding.md` - แนวทาง Active Case Finding ของวัณโรคและประชากรข้ามชาติ
3. `ncd_remission_guideline.md` - เกณฑ์และการประเมินผลโครงการ NCD Remission
4. `flood_disaster_plan.md` - แผนประสานงานช่วยเหลือผู้ป่วยติดเตียงและภัยพิบัติอุทกภัย
5. `digital_health_roadmap.md` - แผนสุขภาพดิจิทัล การเชื่อมต่อ FHIR gateway และบุคลากรไอที

---

## 2. สิ่งที่ต้องดำเนินการในขั้นถัดไป (สำหรับ AI Agent ตัวอื่นหรือนักพัฒนา)

### งานหลังบ้าน (Backend Tasks):
1. **การติดตั้ง Dependencies และเริ่มระบบ**:
   - รันคำสั่งติดตั้งแพ็กเกจ: `pip install -r backend/requirements.txt`
   - รันคำสั่งบู้ตสแตรปข้อมูลเดโมเข้า SQLite: `python backend/app/db/bootstrap.py` (หรือเปลี่ยนการเรียกใช้ python module ให้เหมาะสม)
   - เริ่มรันเซอร์เวอร์หลังบ้าน: `uvicorn backend.app.main:app --reload`
2. **การทดสอบความถูกต้องของ API**:
   - เข้าตรวจสอบ API Swagger ที่ `http://localhost:8000/docs` เพื่อทดลองเล่น API ทั้งสามส่วน

### งานหน้าบ้าน (Frontend Tasks):
จำเป็นต้องสร้างส่วนติดต่อผู้ใช้ด้วย React + TypeScript + Tailwind CSS ในโฟลเดอร์ `frontend/`:
1. **เตรียมโครงสร้างโปรเจกต์ React**:
   - ใช้ Vite ในการเริ่มต้นระบบ React + TypeScript: `npm create vite@latest frontend -- --template react-ts`
   - ติดตั้งและตั้งค่า Tailwind CSS และ Lucide-React สำหรับไอคอน
2. **การออกแบบและหน้าจอ (Pages & Components)**:
   - **`App.tsx` & Router**: กำหนด Route ไปยัง 6 หน้าตามความต้องการของ UX:
     - **Home**: ทางลัดด่วน ค้นหาเบื้องต้น และคำแนะนำ 20 คำถาม
     - **Ask Oracle**: หน้า RAG หลัก มีช่องกรอกคำถาม, แสดงโครงสร้างคำตอบ (Summary, Findings, Evidence, Caution, Recommendation, Sources) และมี Citation panel แถบด้านข้างสำหรับแสดงเอกสารฉบับเต็มเมื่อคลิกที่ตัวอ้างอิง
     - **Upload Knowledge**: ลากวางไฟล์ กรอก Metadata
     - **Knowledge Catalog**: ตารางสืบค้นและคัดกรองเอกสาร คาร์ดสถานะประมวลผล
     - **Admin Review**: สำหรับแอดมินอนุมัติเอกสารที่อัปโหลด แก้ไขและบันทึกข้อมูลเมตาดาตา
     - **Query Logs**: ประวัติการสอบถามและบันทึกฟีดแบค (Thumbs Up/Down)
3. **การเชื่อมต่อกับ Backend**:
   - พัฒนาโมดูล `frontend/src/lib/api.ts` เพื่อเชื่อมต่อ HTTP request ไปยัง FastAPI ที่รันอยู่บนพอร์ต 8000
