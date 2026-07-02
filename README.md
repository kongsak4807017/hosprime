# HosPrime - Health Organization Operating System
## Milestone 1: Knowledge Oracle MVP

HosPrime คือระบบปฏิบัติการอัจฉริยะเพื่อการจัดการความรู้และการตัดสินใจสำหรับองค์กรสาธารณสุข (Health Organization Operating System) โดย Milestone 1 นี้เสนอ **Knowledge Oracle MVP** ที่เป็นรากฐานในการรวบรวม สืบค้น และตอบคำถามจากคลังข้อมูลในองค์กรได้อย่างแม่นยำ ป้องกันการสร้างข้อมูลเท็จ (No Hallucination) และระบุแหล่งอ้างอิงและหน้า (Citation) ได้อย่างโปร่งใส

---

## 🏗️ โครงสร้างเทคโนโลยี (Tech Stack)
- **ระบบหลังบ้าน (Backend)**: FastAPI (Python), SQLAlchemy, SQLite, Pydantic
- **ระบบหน้าบ้าน (Frontend)**: React, TypeScript, Tailwind CSS, Lucide React
- **เอ็นจิ้นปัญญาประดิษฐ์ (AI Engine)**: Google Gemini API (`gemini-1.5-flash` และ `text-embedding-004`)
- **การค้นหาเวกเตอร์ (Vector Search)**: Local-first Cosine Similarity ด้วย NumPy และ SQLite

---

## 🛠️ ขั้นตอนการติดตั้งและการเริ่มใช้งาน (Setup & Run)

### 1. การตั้งค่าระบบหลังบ้าน (Backend Setup)
1. เข้าไปยังไดเรกทอรี backend:
   ```bash
   cd backend
   ```
2. ติดตั้ง Dependencies สำหรับ Python:
   ```bash
   pip install -r requirements.txt
   ```
3. กำหนดค่า API Key:
   สร้างหรือตรวจสอบไฟล์ `.env` ในโฟลเดอร์ `backend/` และใส่ Gemini API Key:
   ```env
   GEMINI_API_KEY=AIzaSyDGql9VM_5aWG-i57xLchiueyM2GkuN9nc
   DATABASE_URL=sqlite:///./hosprime.db
   ```
4. บู้ตสแตรปเตรียมข้อมูลคลังความรู้จำลอง (บีบอัดข้อมูลเดโม 5 แฟ้มงานหลัก):
   ```bash
   python app/db/bootstrap.py
   ```
5. เริ่มใช้งาน FastAPI Server:
   ```bash
   uvicorn app.main:app --reload
   ```
   *ตรวจสอบ Swagger API ได้ที่: [http://localhost:8000/docs](http://localhost:8000/docs)*

---

### 2. การตั้งค่าระบบหน้าบ้าน (Frontend Setup)
1. เข้าไปยังไดเรกทอรี frontend:
   ```bash
   cd ../frontend
   ```
2. ติดตั้งแพ็กเกจด้วย npm:
   ```bash
   npm install
   ```
3. รันหน้าจอพัฒนาด้วย Vite:
   ```bash
   npm run dev
   ```
   *เปิดหน้าจอผ่านบราวเซอร์ได้ที่: [http://localhost:5173](http://localhost:5173)*

---

## 💡 คำแนะนำในการทดสอบเดโม (Demo Scenario)

ระบบเตรียมความรู้และข้อมูลอ้างอิงในการตอบคำถามสำคัญ 5 ด้าน รวมกว่า 20 คำถาม โดยตัวอย่างคำถามที่สามารถทดลองพิมพ์สอบถามได้ในแถบ **"ถาม Oracle (Ask Oracle)"** มีดังนี้:

### 1. หมวดฝุ่นละออง PM2.5
- *“PM2.5 ปีที่แล้วจังหวัดทำอะไรบ้าง”*
- *“มาตรการการแจกหน้ากาก N95 มีตัวเลขเท่าไหร่”*
- *“ข้อจำกัดและอุปสรรคของการรับมือฝุ่นมีอะไรบ้าง”*

### 2. หมวดวัณโรค (TB Active Case Finding)
- *“TB active case finding มีแนวทางอะไร”*
- *“การตรวจคัดกรองวัณโรคเชิงรุกใช้เทคโนโลยีอะไรบ้าง”*
- *“ปัญหาของการตรวจค้นหาผู้ป่วยวัณโรคในกลุ่มประชากรข้ามชาติคืออะไร”*

### 3. หมวด NCD Remission
- *“NCD remission มีเอกสารหรือโครงการอะไรแล้ว”*
- *“การประเมินว่าผู้ป่วยเบาหวานเข้าสู่ระยะสงบ (Remission) ดูจากเกณฑ์อะไร”*
- *“ข้อควรระวังในการทำ NCD Remission ในผู้ป่วยสูงอายุคืออะไร”*

### 4. หมวดการจัดการภัยพิบัติอุทกภัย (Disaster/Flood)
- *“น้ำท่วมครั้งก่อนเรามีมาตรการอะไร”*
- *“การเยียวยาจิตใจและบทบาททีม MCATT ในน้ำท่วมทำอย่างไร”*
- *“บทเรียนปัญหาด้านการสื่อสารในช่วงน้ำท่วมมีอะไรบ้าง”*

### 5. หมวดสุขภาพดิจิทัล (Digital Health Platform)
- *“Digital Health platform ควรเริ่มจากอะไร”*
- *“การดูแลรักษาความปลอดภัยข้อมูลผู้ป่วยในระบบสุขภาพดิจิทัลทำอย่างไร”*
- *“การแก้ไขปัญหาขาดแคลนไอทีใน รพ.สต. มีคำแนะนำอย่างไร”*

---

## 🔒 กฎการทำ RAG ของ HosPrime
- **No Evidence ➔ No Answer**: หากหลักฐานความคล้ายคลึงของประโยคต่ำเกินไป หรือไม่มีข้อมูลจริงในเอกสาร ระบบจะตอบว่า `"Evidence is insufficient from the current organizational knowledge base."` เพื่อป้องกันการปั้นแต่งข้อมูล
- **Traceable**: ทุกย่อหน้าของคำตอบระบุหมายเลขหลักฐานประกอบอย่างโปร่งใส เช่น `[Source ID: 1]` ซึ่งสามารถคลิกดูรายละเอียดของข้อความและหน้าที่ในหน้าจอ RAG ได้ทันที
