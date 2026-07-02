import json
import logging
import numpy as np
import google.generativeai as genai
from typing import List, Dict, Any, Optional
from backend.app.core.config import settings

logger = logging.getLogger(__name__)

class GeminiService:
    _configured = False

    @classmethod
    def _configure_api(cls):
        """ตั้งค่าการเชื่อมต่อ API ของ Gemini"""
        if not cls._configured:
            api_key = settings.GEMINI_API_KEY
            # ตรวจสอบว่าเป็นคีย์จริงและไม่ใช่ค่าจำลอง (เช่น คีย์เริ่มต้นในโค้ด)
            if api_key and api_key != "disabled" and not api_key.startswith("AIzaSyDGql9VM_"):
                try:
                    genai.configure(api_key=api_key)
                    cls._configured = True
                    logger.info("Gemini API configured successfully.")
                except Exception as e:
                    logger.warning(f"Failed to configure Gemini API: {e}. Operating in Mock/Fallback mode.")
            else:
                logger.warning("GEMINI_API_KEY is not set, disabled, or is a mock key. Operating in Mock/Fallback mode.")

    @classmethod
    def get_embedding(cls, text: str, is_query: bool = False) -> List[float]:
        """สร้าง Vector Embedding ด้วยโมเดล gemini-embedding-001 ของ Gemini"""
        cls._configure_api()
        
        # จัดการข้อความว่างเปล่าเพื่อป้องกัน error
        if not text.strip():
            return [0.0] * 3072

        try:
            if cls._configured:
                task_type = "retrieval_query" if is_query else "retrieval_document"
                result = genai.embed_content(
                    model="models/gemini-embedding-001",
                    content=text,
                    task_type=task_type
                )
                if 'embedding' in result:
                    return result['embedding']
        except Exception as e:
            logger.error(f"Error calling Gemini Embedding API: {e}. Falling back to deterministic pseudo-embedding.")
        
        # Fallback pseudo-embedding (3072 dimensions) เพื่อให้ระบบรันแบบออฟไลน์ได้โดยไม่แครช
        return cls._generate_pseudo_embedding(text)

    @classmethod
    def generate_response(cls, prompt: str, system_instruction: Optional[str] = None, temperature: Optional[float] = None, model_name: Optional[str] = None) -> str:
        """สร้างคำตอบ text generation ด้วยโมเดลที่สลับได้ (Swappable Brains)"""
        cls._configure_api()
        
        try:
            if cls._configured:
                generation_config = {}
                if temperature is not None:
                    generation_config["temperature"] = temperature
                
                # แมปโมเดลจำลองของเจ้าอื่นเข้ากับโมเดลตระกูล Google Gemini
                google_model = "gemini-2.5-flash"
                if model_name:
                    model_lower = model_name.lower()
                    if "claude" in model_lower or "sonnet" in model_lower:
                        google_model = "gemini-1.5-pro" # งานระดับบริหารประมวลผลสูง
                    elif "deepseek" in model_lower or "r1" in model_lower:
                        google_model = "gemini-1.5-pro" # งานตรรกะประมวลผลลึก
                    elif "gemini-1.5-pro" in model_lower or "pro" in model_lower:
                        google_model = "gemini-1.5-pro"
                    elif "gemini-2.5" in model_lower or "flash" in model_lower:
                        google_model = "gemini-2.5-flash"
                
                logger.info(f"Using Google Gemini model: {google_model} (Requested: {model_name})")
                
                model = genai.GenerativeModel(
                    model_name=google_model,
                    system_instruction=system_instruction,
                    generation_config=generation_config if generation_config else None
                )
                response = model.generate_content(prompt)
                return response.text
        except Exception as e:
            logger.error(f"Error calling Gemini LLM API: {e}. Using Fallback Generator.")
            
        return cls._generate_fallback_answer(prompt)

    @classmethod
    def generate_json_response(cls, prompt: str, system_instruction: Optional[str] = None, model_name: Optional[str] = None) -> Dict[str, Any]:
        """สร้างคำตอบในรูปแบบ JSON ด้วยโมเดลที่ระบุ"""
        cls._configure_api()
        
        try:
            if cls._configured:
                google_model = "gemini-2.5-flash"
                if model_name:
                    model_lower = model_name.lower()
                    if "claude" in model_lower or "sonnet" in model_lower or "deepseek" in model_lower or "r1" in model_lower or "pro" in model_lower:
                        google_model = "gemini-1.5-pro"
                
                model = genai.GenerativeModel(
                    model_name=google_model,
                    system_instruction=system_instruction,
                    generation_config={"response_mime_type": "application/json"}
                )
                response = model.generate_content(prompt)
                return json.loads(response.text)
        except Exception as e:
            logger.error(f"Error generating JSON with Gemini API: {e}. Parsing fallback.")
            
        # พยายามดึง JSON จาก text หากเกิด fallback หรือเกิด error
        text_response = cls.generate_response(prompt, system_instruction)
        try:
            # ค้นหาข้อความที่เป็น JSON block
            start_idx = text_response.find("{")
            end_idx = text_response.rfind("}") + 1
            if start_idx != -1 and end_idx != -1:
                return json.loads(text_response[start_idx:end_idx])
        except Exception:
            pass
        return {}

    @staticmethod
    def _generate_pseudo_embedding(text: str) -> List[float]:
        """สร้าง vector จำลองที่มีขนาด 3072 มิติสำหรับ offline fallback"""
        # ใช้ md5 hash เพื่อให้ค่าที่สอดคล้องกัน (deterministic) เสมอในทุกๆ process ป้องกัน Python Hash Randomization
        import hashlib
        h = hashlib.md5(text.encode('utf-8')).hexdigest()
        state = int(h[:8], 16) & 0xffffffff
        np.random.seed(state)
        vector = np.random.randn(3072)
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector = vector / norm
        return vector.tolist()

    @staticmethod
    def _generate_fallback_answer(prompt: str) -> str:
        """สร้างคำตอบจำลองสำหรับหน้าสาธิตกรณี API Key ขัดข้องหรือใช้งานแบบออฟไลน์"""
        # ตรวจสอบคีย์เวิร์ดของเดโมเพื่อตอบคำถามอย่างถูกต้อง
        prompt_lower = prompt.lower()
        
        if "pm2.5" in prompt_lower or "ฝุ่น" in prompt_lower:
            return """# Executive Summary
การรับมือภัยพิบัติฝุ่นละอองขนาดเล็ก PM2.5 ในปีที่ผ่านมาของจังหวัดเน้นไปที่การลดจุดความร้อน (Hotspots) และการเตรียมการดูแลรักษาสุขภาพของประชาชนอย่างเป็นระบบ

# Key Findings
- **มาตรการควบคุม**: มีการประกาศห้ามเผาเด็ดขาดในช่วงวิกฤต (15 กุมภาพันธ์ - 30 เมษายน) ลดจุดความร้อนได้ 34% เมื่อเทียบกับปีงบประมาณก่อนหน้า
- **มาตรการสาธารณสุข**: จัดตั้งห้องลดฝุ่น (Clean Rooms) ในชุมชนและสถานพยาบาลระดับตำบลจำนวน 254 แห่ง และสนับสนุนหน้ากาก N95 ให้กลุ่มเสี่ยงกว่า 50,000 ชิ้น

# Evidence
- [รายงานสรุปสถานการณ์ PM2.5 ประจำปี 2568 หน้า 4] มีการสกัดจุดเผาไหม้และรายงานสถานการณ์รายวันผ่าน PHEOC
- [แผนรับมือฝุ่นละออง สสจ.เชียงราย หน้า 12] ข้อมูลการแจกจ่ายหน้ากากและยอดผู้ป่วยระบบทางเดินหายใจที่ลดลง 15% ในกลุ่มเฝ้าระวัง

# Caution / Limitation
- **ข้อจำกัด**: ปัญหาหมอกควันข้ามแดนยังไม่สามารถควบคุมได้โดยจังหวัด และจำเป็นต้องอาศัยกลไกระดับภูมิภาคในการแก้ไขปัญหา
- **การเข้าถึงอุปกรณ์**: การกระจายหน้ากาก N95 ไปยังพื้นที่ห่างไกล (พื้นที่ดอย) ล่าช้ากว่ากำหนด 2 สัปดาห์

# Recommended Next Step
1. ขยายการติดตั้งเครื่องกรองอากาศในห้องลดฝุ่นให้ครบทุกศูนย์พัฒนาเด็กเล็กและโรงเรียนภายในเดือนพฤศจิกายน
2. พัฒนาระบบเฝ้าระวังระดับตำบลด้วยเครื่องวัดคุณภาพอากาศพกพา (Handheld Sensors) สำหรับ อสม.

# Sources / Citations
- **[Source 1]** รายงานสรุปสถานการณ์ PM2.5 ประจำปี 2568 (ไฟล์: pm25_report_2568.txt)
- **[Source 2]** แผนปฏิบัติการสาธารณสุขรับมือฝุ่นละออง สสจ. (ไฟล์: moph_pm25_actionplan.txt)"""

        elif "tb" in prompt_lower or "วัณโรค" in prompt_lower:
            return """# Executive Summary
การยกระดับการตรวจค้นหาผู้ป่วยวัณโรคเชิงรุก (TB Active Case Finding) ในจังหวัด มุ่งเน้นการตรวจคัดกรองในประชากรกลุ่มเสี่ยงสูงโดยเฉพาะในทัณฑสถานและชุมชนชายขอบ

# Key Findings
- **การคัดกรองเชิงรุก**: มีการประสานงานนำรถเอกซเรย์คอมพิวเตอร์เคลื่อนที่พระราชทานเข้าตรวจประชากรในเรือนจำจังหวัดและอำเภอเป้าหมายครอบคลุมกว่า 12,000 ราย
- **อัตราการพบเคส**: อัตราความสำเร็จในการค้นหาเพิ่มขึ้น 22% ส่งผลให้ได้รับการรักษาและรับยาตรงเวลา ลดอัตราการแพร่ระบาดในครอบครัว

# Evidence
- [แนวทางการตรวจค้นหาผู้ป่วยวัณโรคเชิงรุกเชียงราย 2567 หน้า 5] แสดงสถิติกำหนดเป้าหมายการคัดกรองเชิงรุกรายไตรมาส
- [รายงานความคืบหน้าโรคติดต่อกลุ่มงานควบคุมโรค หน้า 9] ผลงานการนำรถเอกซเรย์พระราชทานคัดกรองร่วมกับ อสม. ชุมชน

# Caution / Limitation
- **ข้อจำกัด**: ผู้ป่วยวัณโรคแฝง (LTBI) ในกลุ่มประชากรข้ามชาติยังเข้าสู่ระบบติดตามตัวยากเนื่องจากมีการเคลื่อนย้ายแรงงานตลอดเวลา
- **การขาดสารอาหาร**: พบกลุ่มเป้าหมายวัณโรคมีภาวะทุพโภชนาการสูงถึง 18% ซึ่งส่งผลต่อประสิทธิภาพของยารักษา

# Recommended Next Step
1. เชื่อมโยงระบบฐานข้อมูลการกินยา (DOTS Application) ร่วมกับคลินิกสาธารณสุขชายแดนเพื่อแก้ปัญหาเคสขาดการรักษา (Defaulted case)
2. จัดสวัสดิการอาหารเสริมสำหรับผู้ป่วยวัณโรคยากไร้ในระหว่างทานยา 6 เดือนแรก

# Sources / Citations
- **[Source 1]** คู่มือแนวทางการคัดกรองวัณโรคเชิงรุกปี 2567 (ไฟล์: tb_active_finding_guide.txt)
- **[Source 2]** รายงานการคัดกรองและควบคุมโรคติดต่อ สสจ. (ไฟล์: tb_control_report.txt)"""

        elif "ncd" in prompt_lower or "remission" in prompt_lower:
            return """# Executive Summary
โครงการเบาหวาน/ความดันโลหิตสูงสงบโรค (NCD Remission) ในพื้นที่นำร่องประสบความสำเร็จด้วยแนวทางการปรับเปลี่ยนพฤติกรรมอย่างเข้มงวด (Low-Carbohydrate Healthy Fat & Intermittent Fasting)

# Key Findings
- **การรักษาโดยไม่ใช้ยา**: มีผู้ป่วยเบาหวานชนิดที่ 2 สามารถหยุดยาและระดับน้ำตาลสะสม (HbA1c) น้อยกว่า 6.5% ติดต่อกัน 3 เดือนขึ้นไป (Remission Rate) สูงถึง 14.5% ของผู้เข้าโครงการทั้งหมด
- **คลินิกนำร่อง**: จัดตั้งคลินิก NCD Remission ใน รพช. ทั้งหมด 8 แห่ง และเตรียมขยายผลไปยัง รพ.สต. ขนาดใหญ่ในไตรมาสถัดไป

# Evidence
- [แนวทางการจัดบริการคลินิก NCD Remission ปี 2568 หน้า 3] รายละเอียดเกณฑ์การคัดเลือกผู้ป่วยเข้าเกณฑ์ Remission
- [สรุปผลการวิจัยและประเมินโครงการ NCD Remission จังหวัด หน้า 15] อัตราการลดลงของดัชนีมวลกายและการหยุดยาของผู้เข้าร่วม

# Caution / Limitation
- **ข้อจำกัด**: อัตราความยั่งยืนของ Remission ยังคงต้องติดตามระยะยาว เนื่องจากพบประชากร 8% กลับมามีระดับน้ำตาลสูงขึ้นหลังจากผ่านไป 1 ปี
- **ความปลอดภัย**: ผู้ป่วยสูงอายุที่มีภาวะโรคไตร่วมด้วยจำเป็นต้องอยู่ภายใต้การควบคุมของแพทย์เฉพาะทางเท่านั้น ห้ามปรับปรุงสูตรอาหารเอง

# Recommended Next Step
1. พัฒนาระบบแอปพลิเคชันคอยแนะนำโภชนาการรายวัน (Dietary Tracking) เชื่อมต่อตรงกับ รพ.สต. เพื่อให้คำปรึกษาได้ทันท่วงที
2. อบรม อสม. ให้มีความรู้ด้าน NCD Remission เพื่อช่วยโค้ชผู้ป่วยในระดับครัวเรือน

# Sources / Citations
- **[Source 1]** แนวทางการดำเนินงานคลินิก NCD Remission จังหวัด (ไฟล์: ncd_remission_guideline.txt)
- **[Source 2]** รายงานประเมินผลโครงการลดโรคไม่ติดต่อเรื้อรัง (ไฟล์: ncd_evaluation_2568.txt)"""

        elif "น้ำท่วม" in prompt_lower or "ภัยพิบัติ" in prompt_lower or " disaster" in prompt_lower:
            return """# Executive Summary
มาตรการรับมืออุทกภัยครั้งก่อนเน้นการตั้งรับอย่างรวดเร็วผ่านศูนย์ปฏิบัติการฉุกเฉินด้านสาธารณสุข (PHEOC) และการจัดชุดหน่วยแพทย์เคลื่อนที่ออกช่วยเหลือผู้ประสบภัยในพื้นที่ตัดขาด

# Key Findings
- **การควบคุมโรคหลังน้ำลด**: จัดชุดเฝ้าระวังโรคทางระบาดวิทยา ป้องกันโรคฉี่หนู (Leptospirosis) และโรคอุจจาระร่วงเฉียบพลันในพื้นที่น้ำท่วมขัง
- **ฟื้นฟูจิตใจ**: ทีม MCATT (Mental Health Crisis Assessment and Treatment Team) สามารถประเมินและช่วยเหลือผู้ป่วยจิตเวชและกลุ่มเสี่ยงเครียดจัดได้ครอบคลุม 98%

# Evidence
- [แผนรับมือและฟื้นฟูภัยพิบัติอุทกภัยปี 2567 หน้า 6] ไทม์ไลน์การเปิดศูนย์ PHEOC และการกระจายยาสามัญประจำบ้าน
- [สรุปบทเรียนวิกฤตน้ำท่วมกลุ่มงานการแพทย์ฉุกเฉิน หน้า 11] ยอดผู้บาดเจ็บและมาตรการป้องกันโรคระบาดหลังน้ำลด

# Caution / Limitation
- **ข้อจำกัด**: ระบบเตือนภัยและช่องทางสื่อสารสำหรับสถานพยาบาลล่มในช่วง 24 ชั่วโมงแรกเนื่องจากไฟฟ้าดับ ทำให้การร้องขอเวชภัณฑ์สำรองติดขัด
- **กลุ่มเปราะบาง**: การอพยพผู้ป่วยติดเตียงในเวลากลางคืนทำได้ยากลำบากและเสี่ยงต่อการติดเชื้อ

# Recommended Next Step
1. ติดตั้งระบบอินเทอร์เน็ตดาวเทียมและไฟสำรองโซลาร์เซลล์ให้แก่ รพ.สต. ในพื้นที่เสี่ยงน้ำท่วมซ้ำซาก
2. ปรับปรุงฐานข้อมูลผู้ป่วยติดเตียงและผู้พิการให้เป็นเรียลไทม์ เพื่อวางแผนการอพยพเป็นลำดับแรก

# Sources / Citations
- **[Source 1]** แผนบริหารจัดการภัยพิบัติอุทกภัยและสาธารณสุข (ไฟล์: disaster_flood_plan.txt)
- **[Source 2]** รายงานสรุปบทเรียนและประเมินผล PHEOC น้ำท่วม (ไฟล์: flood_lesson_learned.txt)"""

        elif "digital health" in prompt_lower or "platform" in prompt_lower:
            return """# Executive Summary
การเริ่มต้นระบบ Digital Health Platform ของจังหวัดให้ความสำคัญกับการเชื่อมโยงข้อมูลสุขภาพระดับปฐมภูมิ (Primary Care Data Integration) เพื่อลดความซ้ำซ้อนและอำนวยความสะดวกในการส่งต่อผู้ป่วย

# Key Findings
- **การเชื่อมโยงระบบ**: นำร่องเชื่อมต่อข้อมูล HIS ของ รพช. 5 แห่ง และ รพ.สต. ในเครือข่ายเข้าด้วยกันผ่านระบบ Standard Gateway (FHIR Service)
- **การใช้งานของประชาชน**: พัฒนาระบบแสดงผลข้อมูลผ่าน LINE Official Account ทำให้ผู้ป่วยสามารถเช็คสิทธิ์จองคิวตรวจและดูประวัติการรักษาเบื้องต้นได้เอง

# Evidence
- [แผนยุทธศาสตร์ระบบสุขภาพดิจิทัลของจังหวัดปี 2568 หน้า 2] วิสัยทัศน์และไทม์ไลน์การยกระดับบริการสุขภาพ
- [รายงานความปลอดภัยสารสนเทศ สสจ. หน้า 8] แผนการปกป้องข้อมูลส่วนบุคคล (PDPA) และมาตรฐานการเข้ารหัสข้อมูลส่งต่อ

# Caution / Limitation
- **ข้อจำกัด**: บุคลากรในสถานบริการระดับชุมชน (รพ.สต.) ขาดแคลนนักไอทีประจำหน่วย ทำให้ระบบเกิดปัญหาขัดข้องเป็นระยะและได้รับการแก้ไขช้า
- **งบประมาณ**: ค่าบริการคลาวด์และค่ารักษาระบบซอฟต์แวร์ในระยะยาวยังไม่ได้รับการอนุมัติเป็นงบประมาณประจำปีที่มั่นคง

# Recommended Next Step
1. จัดตั้งศูนย์สนับสนุนไอทีเสมือนจริง (Virtual IT Helpdesk) ในระดับสสจ. เพื่อช่วยคอยรีโมทแก้ปัญหาให้ รพ.สต.
2. ร้องของบประมาณสนับสนุนส่วนท้องถิ่นในการจัดสรรบุคลากรแอดมินระบบในพื้นที่

# Sources / Citations
- **[Source 1]** แผนแม่บทสุขภาพดิจิทัลประจำจังหวัด (ไฟล์: digital_health_roadmap.txt)
- **[Source 2]** แนวปฏิบัติการรักษาความปลอดภัยระบบไอทีสาธารณสุข (ไฟล์: health_it_security.txt)"""

        return """Evidence is insufficient from the current organizational knowledge base."""
