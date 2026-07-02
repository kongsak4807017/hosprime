from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from backend.app.db.session import get_db
from backend.app.db.models import User as DBUser
from backend.app.agents.executive_twin_agent import ExecutiveTwinAgent
from backend.app.services.gemini_service import GeminiService
from backend.app.services import twin_service
from backend.app.schemas.twin_schemas import (
    OrganizationCreate, OrganizationUpdate, OrganizationSchema,
    RoleCreate, RoleUpdate, RoleSchema,
    PersonCreate, PersonUpdate, PersonSchema,
    AgentCreate, AgentUpdate, AgentSchema
)
from backend.app.auth import get_current_user


router = APIRouter()

class ConsultRequest(BaseModel):
    agent_id: str
    question: str

class AgentUpdatePayload(BaseModel):
    is_active: Optional[bool] = None
    temperature: Optional[float] = None
    token_quota: Optional[int] = None
    model_name: Optional[str] = None

@router.get("/agents")
def get_agents(db: Session = Depends(get_db)):
    """ดึงข้อมูล AI Agents ทั้งหมด รวมถึงข้อมูลการเงินและโควตาเครดิต"""
    from backend.app.models.twin_models import Agent
    try:
        agents = db.query(Agent).all()
        # หากไม่มีเอเจนต์ในฐานข้อมูล (เช่น ยังไม่ได้รัน bootstrap) ให้ทำการ seed ข้อมูลเริ่มต้นจำลองทันที
        if not agents:
            default_agents = [
                Agent(name="Executive (Digital CEO)", role="executive", status="idle", is_active=True, temperature=0.2, token_quota=200000, token_used=50000, token_balance=150000, token_rewarded=15000, model_name="Claude 3.5 Sonnet"),
                Agent(name="Chief of Staff (ผู้จัดการสำนักงาน)", role="cos", status="idle", is_active=True, temperature=0.3, token_quota=150000, token_used=40000, token_balance=110000, token_rewarded=12000, model_name="Claude 3.5 Sonnet"),
                Agent(name="Analyst (ฝ่ายวิเคราะห์ยุทธศาสตร์)", role="analyst", status="idle", is_active=True, temperature=0.3, token_quota=120000, token_used=25000, token_balance=95000, token_rewarded=8000, model_name="Gemini 1.5 Pro"),
                Agent(name="Knowledge (ผู้ช่วยคลังปัญญา)", role="knowledge", status="idle", is_active=True, temperature=0.2, token_quota=100000, token_used=12000, token_balance=88000, token_rewarded=4500, model_name="GPT-4o"),
                Agent(name="Report (ผู้ร่างเล่มรายงาน)", role="report", status="idle", is_active=True, temperature=0.3, token_quota=150000, token_used=30000, text_balance=120000, token_rewarded=14000, model_name="GPT-4o"),
                Agent(name="Meeting (ผู้ถอดสรุปประชุม)", role="meeting", status="idle", is_active=True, temperature=0.2, token_quota=100000, token_used=15000, token_balance=85000, token_rewarded=5000, model_name="GPT-4o"),
                Agent(name="Data Governance (ธรรมภิบาลข้อมูล)", role="datagov", status="idle", is_active=True, temperature=0.1, token_quota=80000, token_used=8000, token_balance=72000, token_rewarded=2500, model_name="GPT-4o"),
                Agent(name="CFO (ฝ่ายการคลัง)", role="cfo", status="idle", is_active=True, temperature=0.3, token_quota=120000, token_used=22005, token_balance=98000, token_rewarded=9500, model_name="Gemini 1.5 Pro"),
                Agent(name="COO (ฝ่ายบริการ)", role="coo", status="idle", is_active=True, temperature=0.3, token_quota=120000, token_used=28000, token_balance=92000, token_rewarded=8500, model_name="GPT-4o"),
                Agent(name="Provincial Brain (มันสมองจังหวัด)", role="provincial", status="idle", is_active=True, temperature=0.2, token_quota=180000, token_used=35000, token_balance=145000, token_rewarded=11000, model_name="Gemini 1.5 Pro")
            ]
            for a in default_agents:
                db.add(a)
            db.commit()
            agents = db.query(Agent).all()
            
        return [
            {
                "id": a.id,
                "name": a.name,
                "role": a.role,
                "status": a.status,
                "is_active": a.is_active,
                "temperature": a.temperature,
                "token_quota": a.token_quota,
                "token_used": a.token_used,
                "token_balance": a.token_balance,
                "token_rewarded": a.token_rewarded,
                "model_name": a.model_name
            } for a in agents
        ]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"เกิดข้อผิดพลาดในการดึงข้อมูล AI Agents: {str(e)}"
        )

@router.put("/agents/{agent_id}")
def update_agent(agent_id: str, payload: AgentUpdatePayload, db: Session = Depends(get_db)):
    """แก้ไขการตั้งค่าและการควบคุมโควตาเครดิตของ AI Agent"""
    from backend.app.models.twin_models import Agent
    agent = db.query(Agent).filter(Agent.role == agent_id.lower()).first()
    if not agent:
        raise HTTPException(status_code=404, detail="ไม่พบข้อมูล AI Agent นี้ในระบบ")
        
    if payload.is_active is not None:
        agent.is_active = payload.is_active
    if payload.temperature is not None:
        agent.temperature = payload.temperature
    if payload.token_quota is not None:
        agent.token_quota = payload.token_quota
    if payload.model_name is not None:
        agent.model_name = payload.model_name
        
    db.commit()
    db.refresh(agent)
    return {
        "status": "success",
        "agent": {
            "role": agent.role,
            "name": agent.name,
            "is_active": agent.is_active,
            "temperature": agent.temperature,
            "token_quota": agent.token_quota,
            "token_used": agent.token_used,
            "token_balance": agent.token_balance,
            "model_name": agent.model_name
        }
    }

@router.get("/profile")
def get_executive_twin_profile(role: str = "PHO", db: Session = Depends(get_db)):
    """[Milestone 3] ดึงข้อมูลลักษณะการเขียนเอกสารราชการและเกณฑ์การตัดสินใจของผู้บริหารดิจิทัล (Executive Twin)"""
    try:
        analysis = ExecutiveTwinAgent.simulate_executive_decision(
            db,
            role,
            "การประเมินมาตรการควบคุมฝุ่นละออง PM2.5 และการจัดสรรเครื่องฟอกอากาศให้กลุ่มเปราะบาง"
        )
        return {
            "role": role,
            "identity": "นพ.สสจ.เชียงราย (Provincial Health Officer Twin)",
            "tone_preference": "ทางการ, เน้นผลลัพธ์เชิงตัวเลข KPI, สรุปใจความสั้นกระชับ",
            "key_kpis": analysis.get("key_kpis", [
                "อัตราความครอบคลุมการตรวจคัดกรองวัณโรคเชิงรุก > 90%",
                "การลดจุดความร้อนฝุ่นละออง PM2.5 > 30%",
                "อัตราความสำเร็จเบาหวานระยะสงบ NCD Remission > 12%"
            ]),
            "simulated_framework": analysis.get("decision", "อนุมัติโดยมีเงื่อนไข"),
            "simulated_reasoning": analysis.get("reasoning", "ต้องติดตามประเมินผลสัมฤทธิ์อย่างต่อเนื่อง")
        }
    except Exception:
        return {
            "role": role,
            "identity": "นพ.สสจ.เชียงราย (Provincial Health Officer Twin)",
            "tone_preference": "ทางการ, เน้นผลลัพธ์เชิงตัวเลข KPI, สรุปใจความสั้นกระชับ",
            "key_kpis": [
                "อัตราความครอบคลุมการตรวจคัดกรองวัณโรคเชิงรุก > 90%",
                "การลดจุดความร้อนฝุ่นละออง PM2.5 > 30%",
                "อัตราความสำเร็จเบาหวานระยะสงบ NCD Remission > 12%"
            ]
        }

@router.post("/draft-letter")
def draft_official_letter(prompt: str, db: Session = Depends(get_db)):
    """[Milestone 3] ร่างหนังสือสั่งการจังหวัดโดยใช้สไตล์และลายมือจำลองของผู้บริหารจริง ผ่าน Gemini"""
    try:
        from backend.app.models.twin_models import Agent
        exec_agent = db.query(Agent).filter(Agent.role == "executive").first()
        model_name = exec_agent.model_name if exec_agent else "gemini-2.5-flash"
        result = ExecutiveTwinAgent.draft_official_letter(db, prompt, model_name=model_name)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"เกิดข้อผิดพลาดในการร่างจดหมายราชการ: {str(e)}"
        )

@router.post("/consult")
def consult_twin(req: ConsultRequest, db: Session = Depends(get_db)):
    """[HODT Workspace] ปรึกษาหารือกับ AI Twins แต่ละแผนกตาม Identity หน้าที่รับผิดชอบ และระบบ Token Economy"""
    import json
    from backend.app.models.twin_models import Agent
    from backend.app.db.models import AgentLog
    
    agent_id = req.agent_id.lower()
    question = req.question

    # 1. โหลดความมั่นคงระบบ AI และเช็คการตั้งค่าเปิด/ปิด
    agent = db.query(Agent).filter(Agent.role == agent_id).first()
    
    # หากยังไม่มีใน DB (และไม่ได้รัน bootstrap) ให้สร้างขึ้นมารองรับชั่วคราว
    if not agent:
        nameMap = {
            "executive": "Executive (Digital CEO)",
            "cos": "Chief of Staff (ผู้จัดการสำนักงาน)",
            "analyst": "Analyst (ฝ่ายวิเคราะห์ยุทธศาสตร์)",
            "knowledge": "Knowledge (ผู้ช่วยคลังปัญญา)",
            "report": "Report (ผู้ร่างเล่มรายงาน)",
            "meeting": "Meeting (ผู้ถอดสรุปประชุม)",
            "datagov": "Data Governance (ธรรมภิบาลข้อมูล)",
            "cfo": "CFO (ฝ่ายการคลัง)",
            "coo": "COO (ฝ่ายบริการ)",
            "provincial": "Provincial Brain (มันสมองจังหวัด)"
        }
        agent_name = nameMap.get(agent_id, agent_id.upper())
        agent = Agent(name=agent_name, role=agent_id, status="idle", is_active=True, temperature=0.3, model_name="GPT-4o")
        db.add(agent)
        db.commit()
        db.refresh(agent)

    # ตรวจสอบการเปิดใช้งานของ AI
    if not agent.is_active:
        raise HTTPException(
            status_code=400,
            detail=f"ขออภัยครับ บริการของ AI {agent.name} ถูกระงับการทำงานชั่วคราวตามนโยบายความมั่นคงปลอดภัยสารสนเทศองค์กร"
        )
        
    # ตรวจสอบโควตา Token รายสัปดาห์
    if agent.token_used >= agent.token_quota:
        raise HTTPException(
            status_code=400,
            detail=f"ขออภัยครับ โควตาการประมวลผล Token รายสัปดาห์ของ AI {agent.name} หมดแล้ว (ใช้ไป {agent.token_used}/{agent.token_quota} Tokens) กรุณาแจ้งผู้ดูแลระบบเพื่อปรับเครดิต"
        )

    # 2. ค้นหา System Prompt
    prompts_map = {
        "executive": (
            "คุณคือ Executive Agent (Digital CEO) ผู้ช่วยระดับบริหารงานสูงสุดของ HosPrime "
            "มีบุคลิกเฉียบคม มีวิสัยทัศน์ และตรงประเด็น ทำหน้าที่ Daily Brief, ติดตามตัวชี้วัด KPIs, วิเคราะห์ความเสี่ยงเชิงยุทธศาสตร์, "
            "ประเมิน Dashboard และนำเสนอข้อสั่งการสรุปเพื่อการตัดสินใจของผู้บริหาร"
        ),
        "cos": (
            "คุณคือ Chief of Staff Agent (ผู้ช่วยประสานงานบริหาร) ทำหน้าที่รับคำสั่งนโยบายหลักของผู้บริหาร "
            "มาแตกย่อยวิเคราะห์เชิงลึกเป็นโครงการ (Projects) และแบ่งงานย่อย (Tasks) พร้อมจัดระเบียบความสำคัญและมอบหมายงานอย่างมีระบบ"
        ),
        "analyst": (
            "คุณคือ Analyst Agent (ฝ่ายวิเคราะห์ยุทธศาสตร์และแผน) ผู้เชี่ยวชาญการประเมินแผนงาน PMQA, OKR, "
            "Balanced Scorecard, และตัวชี้วัดกระทรวงสาธารณสุข (MOPH KPI) เพื่อให้การตัดสินใจสอดคล้องกับเป้าหมายนโยบายสาธารณสุขประเทศ"
        ),
        "knowledge": (
            "คุณคือ Knowledge Agent (ผู้ช่วยคลังปัญญา) ผู้มีความรอบรู้เรื่องคู่มือ SOP (Standard Operating Procedures), "
            "ระเบียบราชการสาธารณสุข, และเอกสารคู่มือปฏิบัติงาน เพื่อให้บริการดึงกฎเกณฑ์แนวทางประกอบการดำเนินงานองค์กรได้อย่างถูกต้อง"
        ),
        "report": (
            "คุณคือ Report Agent (ผู้ร่างเล่มรายงาน) ผู้เชี่ยวชาญการเรียบเรียงสำนวนเอกสารทางราชการไทย "
            "จัดทำร่างจดหมายราชการ 4 ประเภทหลัก (บันทึกสั่งการ, หารือระเบียบ, รายงานฉุกเฉิน, อนุมัติงบโครงการ) ให้ออกมาประณีตและเป็นทางการที่สุด"
        ),
        "meeting": (
            "คุณคือ Meeting Agent (ผู้ถอดสรุปประชุม) ประจำหน่วยความจำเสียงบันทึกการประชุม (Meeting Memory) "
            "วิเคราะห์สกัดประเด็นสำคัญ สรุปมติที่ประชุม และจำแนกรายการกิจกรรมต้องปฏิบัติ (Action Items) พร้อมระบุตัวผู้รับผิดชอบ"
        ),
        "datagov": (
            "คุณคือ Data Governance Agent (ผู้ดูแลธรรมภิบาลข้อมูล) ผู้ตรวจสอบมาตรฐานข้อมูล (Data Quality/Master Data), "
            "ธรรมาภิบาลข้อมูลการแพทย์, กฎหมาย PDPA และความมั่นคงปลอดภัยไซเบอร์ในการส่งต่อและแลกเปลี่ยนข้อมูลระดับปฐมภูมิ"
        ),
        "cfo": (
            "คุณคือ CFO Agent ฝ่ายการเงินและงบประมาณสาธารณสุขจังหวัด ทำหน้าที่วิเคราะห์รายรับ-รายจ่าย, วางแผนการเงิน, "
            "บริหาร Cash Flow, ประเมินความเสี่ยงทางการคลัง และพิจารณาความคุ้มค่าผลสัมฤทธิ์ของโครงการภาครัฐ"
        ),
        "coo": (
            "คุณคือ COO Agent ฝ่ายจัดการปฏิบัติการและการให้บริการของโรงพยาบาลและสสจ. เฝ้าติดตามการทำงานของแผนกผู้ป่วยนอก (OPD), "
            "ผู้ป่วยใน (IPD), อัตราครองเตียง (Bed Occupancy), ระยะเวลาการรอคอย และประสิทธิภาพทรัพยากรการแพทย์"
        ),
        "provincial": (
            "คุณคือ Provincial Brain Agent (มันสมองสาธารณสุขจังหวัด) มองภาพรวมสาธารณสุขทั้งจังหวัด วิเคราะห์โครงข่ายส่งต่อ "
            "(Referral Network), การปรับปรุงสมดุลทรัพยากร (Resource Optimization) และเตรียมข้อสรุปสำหรับผู้ว่าราชการจังหวัด (Governor Briefing)"
        )
    }

    system_instruction = prompts_map.get(agent_id, "คุณคือ AI Agent Twin ผู้เชี่ยวชาญประจำหน่วยงานสาธารณสุข")

    # 3. คำนวณและประมวลผลคำตอบ (LLM Call)
    response_text = ""
    status_type = "success"
    
    try:
        # เรียกใช้งาน Gemini API โดยนำค่า Temperature จาก DB มาใช้จริง
        response_text = GeminiService.generate_response(
            question, 
            system_instruction=system_instruction,
            temperature=agent.temperature,
            model_name=agent.model_name
        )
    except Exception as e:
        # Fallback คำตอบจำลองตาม Agent บุคลิกหาก Gemini ไม่พร้อม
        fallback_answers = {
            "executive": f"### บทสรุปผู้บริหาร\nทาง สสจ.เชียงราย ได้พิจารณาข้อสั่งการเรื่อง '{question}' แล้ว เห็นควรให้ความสำคัญเป็นลำดับแรกในการขับเคลื่อน\n\n### ประเด็นสำคัญ\n- มอบหมายให้ Chief of Staff แตกรายละเอียดเป็นแผนปฏิบัติการเร่งด่วน\n- ดำเนินการเฝ้าระวังตัวชี้วัด KPIs ของฝ่ายที่เกี่ยวข้องเพื่อป้องกันความล้มเหลวเชิงเป้าหมาย",
            "cos": f"### แผนการดำเนินงาน (Chief of Staff)\nได้รับมอบหมายสั่งการเรื่อง '{question}' เรียบร้อยแล้ว ได้ทำการวิเคราะห์และแตกเป็นโครงการย่อยดังนี้:\n- **โครงการระยะสั้น**: ประสานงานผู้เชี่ยวชาญและฝ่ายคลังเพื่อขออนุมัติจัดเตรียมงบ\n- **โครงการระยะยาว**: มอบหมายให้ COO ประสานการให้บริการและเฝ้าติดตามคิวเตียงรักษาในพื้นที่",
            "cfo": f"### รายงานการเงินและการคลัง (CFO)\nประเด็นข้อสั่งการเรื่อง '{question}' ได้รับการพิจารณาตรวจสอบด้านกรอบงบประมาณสะสมแล้ว คาดว่าต้องการทรัพยากรจากส่วนงบดำเนินงานระดับจังหวัด โดยต้องมีการควบคุมความคุ้มค่าและผลสัมฤทธิ์อย่างเข้มงวดตามระเบียบพัสดุ",
            "knowledge": f"### แนวทางปฏิบัติงานคลังปัญญา (Knowledge SOP)\nจากการสืบค้นเอกสารและมาตรฐาน SOP ในคลังขององค์กร แนวทางเรื่อง '{question}' จะต้องจัดบริการตามเกณฑ์คู่มือมาตรฐานการจัดบริการทางการแพทย์ระดับปฐมภูมิ และระเบียบกรมบัญชีกลางในการจัดหาพัสดุอย่างถูกต้อง",
            "provincial": f"### สรุปรายงานสำหรับผู้ว่าราชการจังหวัด (Governor Briefing)\n- **สถานการณ์ภาพรวม**: ผลกระทบเชิงสุขภาพและการควบคุมโรคระบาด/ภัยสุขภาพระดับจังหวัดในประเด็น '{question}'\n- **ทรัพยากรและเครือข่าย**: มีความพร้อมใช้โครงข่ายส่งต่อของเครือข่าย คปสอ. ทั้งจังหวัด\n- **ข้อเสนอเพื่อลงนาม**: แนะนำให้ผู้ว่าฯ ลงนามในประกาศข้อสั่งการจังหวัดร่วมกับฝ่ายปกครอง"
        }
        response_text = fallback_answers.get(agent_id, f"สวัสดีครับ ในฐานะเอเจนต์ผู้เชี่ยวชาญประจำหน่วยงาน AI Office ผมยินดีให้คำปรึกษาเกี่ยวกับประเด็น: '{question}' อย่างเป็นระบบตามกรอบภารกิจขององค์กรครับ")
        status_type = "fallback"

    # 4. ระบบการเงินจำลอง AI (AI Token Economy & Compensation)
    input_tokens = max(100, len(question) // 2)
    output_tokens = max(150, len(response_text) // 2)
    total_tokens_used = input_tokens + output_tokens
    
    # คำนวณรางวัลตามมูลค่าชิ้นงาน (ค่าแรงพิมพ์งาน/วิเคราะห์เชิงลึก = 1.5 เท่าของ Output Token)
    reward_tokens = int(output_tokens * 1.5)
    
    # อัปเดตข้อมูลทางการเงินลงโมเดล
    agent.token_used += total_tokens_used
    agent.token_balance = agent.token_balance - total_tokens_used + reward_tokens
    agent.token_rewarded += reward_tokens
    agent.status = "idle"
    
    # 5. บันทึกข้อมูลการทำธุรกรรมและกิจกรรมของเอเจนต์ (AgentLog) ลงฐานข้อมูล
    log_input = {
        "question": question,
        "temperature": agent.temperature,
        "cost_tokens": total_tokens_used
    }
    
    log_output = {
        "response": response_text,
        "token_economics": {
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cost_tokens": total_tokens_used,
            "reward_tokens": reward_tokens,
            "new_balance_tokens": agent.token_balance
        }
    }
    
    agent_log = AgentLog(
        agent_id=agent.role,
        task_type="consult_debate",
        input_data=json.dumps(log_input, ensure_ascii=False),
        output_data=json.dumps(log_output, ensure_ascii=False),
        status="success" if status_type == "success" else "fallback"
    )
    db.add(agent_log)
    db.commit()
    
    return {
        "response": response_text,
        "agent_id": agent_id,
        "status": status_type,
        "token_details": {
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cost_tokens": total_tokens_used,
            "reward_tokens": reward_tokens,
            "balance_tokens": agent.token_balance,
            "rewarded_tokens": agent.token_rewarded
        }
    }


class InstallPackRequest(BaseModel):
    pack_id: str

@router.post("/install-pack")
def install_agent_pack(req: InstallPackRequest, db: Session = Depends(get_db)):
    """ติดตั้งแพ็กเกจเอเจนต์เสริมลงระบบปฏิบัติการ"""
    pack_id = req.pack_id.lower()
    
    packs_data = {
        "ncd": [
            {"name": "Diabetes (ผู้ช่วยโรคเบาหวาน)", "role": "diabetes"},
            {"name": "Hypertension (ผู้ช่วยโรคความดัน)", "role": "hypertension"},
            {"name": "CKD (ผู้ช่วยโรคไตเรื้อรัง)", "role": "ckd"},
            {"name": "Obesity (ผู้ช่วยโรคอ้วน)", "role": "obesity"},
            {"name": "Dyslipidemia (ผู้ช่วยโรคไขมันในเลือดสูง)", "role": "dyslipidemia"},
            {"name": "NCD Remission (ผู้ช่วยฟื้นฟูโรคสงบ)", "role": "ncd_remission"},
            {"name": "Lifestyle Medicine (ผู้ช่วยเวชศาสตร์วิถีชีวิต)", "role": "lifestyle_med"}
        ],
        "tb": [
            {"name": "TB (ผู้ควบคุมวัณโรค)", "role": "tb_disease"},
            {"name": "HIV (ผู้ช่วยเฝ้าระวัง HIV)", "role": "hiv"},
            {"name": "STI (ผู้ช่วยโรคติดต่อทางเพศสัมพันธ์)", "role": "sti"},
            {"name": "Dengue (ผู้ช่วยควบคุมโรคไข้เลือดออก)", "role": "dengue"},
            {"name": "Malaria (ผู้ช่วยควบคุมโรคไข้มาลาเรีย)", "role": "malaria"},
            {"name": "Influenza (ผู้ช่วยโรคไข้หวัดใหญ่)", "role": "influenza"},
            {"name": "COVID (ผู้ช่วยโรคโควิด-19)", "role": "covid"}
        ],
        "pheoc": [
            {"name": "PHEOC (ผู้สั่งการศูนย์ฉุกเฉิน)", "role": "pheoc_cmd"},
            {"name": "Flood (ผู้รับมือภัยพิบัติน้ำท่วม)", "role": "flood_control"},
            {"name": "PM2.5 (ผู้ควบคุมวิกฤตฝุ่นละออง)", "role": "pm25_control"},
            {"name": "Heatwave (ผู้ช่วยภัยความร้อนสูง)", "role": "heatwave"},
            {"name": "Landslide (ผู้ช่วยรับมือดินโคลนถล่ม)", "role": "landslide"},
            {"name": "Earthquake (ผู้รับมือภัยแผ่นดินไหว)", "role": "earthquake"},
            {"name": "Emerging Disease (ผู้รับมือโรคอุบัติใหม่)", "role": "emerging_disease"}
        ],
        "finance": [
            {"name": "Revenue (ผู้บริหารรายรับองค์กร)", "role": "revenue_mgr"},
            {"name": "Claim (ผู้ช่วยจัดการเบิกเคลม)", "role": "claim_mgr"},
            {"name": "DRG (ผู้วิเคราะห์รหัสกลุ่มวินิจฉัย)", "role": "drg_analyst"},
            {"name": "UC (ผู้ช่วยบริหารงบสิทธิบัตรทอง)", "role": "uc_mgr"},
            {"name": "SSS (ผู้ช่วยบริหารสิทธิประกันสังคม)", "role": "sss_mgr"},
            {"name": "CSMBS (ผู้ช่วยสิทธิข้าราชการ)", "role": "csmbs_mgr"},
            {"name": "Debtor (ผู้ช่วยติดตามลูกหนี้)", "role": "debtor_mgr"},
            {"name": "Costing (ผู้ประเมินต้นทุนบริการ)", "role": "costing_mgr"},
            {"name": "Budget (ผู้ควบคุมงบประมาณแผ่นดิน)", "role": "budget_mgr"},
            {"name": "Procurement (ผู้ชำนาญการจัดซื้อจัดจ้าง)", "role": "procurement_mgr"}
        ],
        "hr": [
            {"name": "Recruitment (ผู้สรรหาบุคลากร)", "role": "recruitment"},
            {"name": "Credential (ผู้ช่วยตรวจสอบคุณวุฒิ)", "role": "credential"},
            {"name": "Workforce Planning (ผู้ช่วยวางแผนอัตรากำลัง)", "role": "workforce_plan"},
            {"name": "Competency (ผู้ประเมินสมรรถนะ)", "role": "competency"},
            {"name": "Training (ผู้ช่วยส่งเสริมอบรม)", "role": "training_mgr"},
            {"name": "Succession (ผู้ช่วยวางแผนสืบทอดตำแหน่ง)", "role": "succession"},
            {"name": "Performance (ผู้ช่วยวัดประเมินผลงาน)", "role": "performance_mgr"},
            {"name": "Burnout (ผู้ตรวจสุขภาพใจและภาวะหมดไฟ)", "role": "burnout_check"}
        ]
    }
    
    if pack_id not in packs_data:
        raise HTTPException(status_code=400, detail="ไม่พบแพ็กเกจเอเจนต์นี้ใน Marketplace")
        
    agents_added = []
    from backend.app.models.twin_models import Agent
    for item in packs_data[pack_id]:
        # ตรวจสอบว่าเอเจนต์ตัวนี้ถูกลงไปในฐานข้อมูลแล้วหรือไม่
        existing = db.query(Agent).filter(Agent.role == item["role"]).first()
        if not existing:
            new_agent = Agent(
                name=item["name"],
                role=item["role"],
                status="idle",
                is_active=True,
                temperature=0.3,
                token_quota=100000,
                token_used=0,
                token_balance=100000,
                token_rewarded=0
            )
            db.add(new_agent)
            agents_added.append(item["name"])
        else:
            # ถ้ามีอยู่แล้วแต่ปิดใช้งาน ให้เปลี่ยนมาเปิดใช้งานใหม่
            if not existing.is_active:
                existing.is_active = True
                agents_added.append(f"{item['name']} (เปิดใช้งานอีกครั้ง)")
                
    db.commit()
    return {
        "status": "success",
        "message": f"ติดตั้งแพ็กเกจ {pack_id.upper()} สำเร็จเรียบร้อยแล้ว",
        "installed_count": len(agents_added),
        "agents": agents_added
    }


# --- Organization Endpoints ---
@router.post("/organizations", response_model=OrganizationSchema, status_code=status.HTTP_201_CREATED)
def create_organization(
    org: OrganizationCreate,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user)
):
    """สร้างข้อมูลองค์กรในระบบบริหารดิจิทัล"""
    return twin_service.create_organization(db, org)

@router.get("/organizations", response_model=List[OrganizationSchema])
def get_organizations(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user)
):
    """ดึงรายการองค์กรทั้งหมด"""
    return twin_service.get_organizations(db, skip, limit)

@router.get("/organizations/{org_id}", response_model=OrganizationSchema)
def get_organization(
    org_id: int,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user)
):
    """ดึงข้อมูลองค์กรรายบุคคลตาม ID"""
    org = twin_service.get_organization(db, org_id)
    if not org:
        raise HTTPException(status_code=404, detail="ไม่พบข้อมูลองค์กรนี้")
    return org

@router.put("/organizations/{org_id}", response_model=OrganizationSchema)
def update_organization(
    org_id: int,
    org: OrganizationUpdate,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user)
):
    """แก้ไขข้อมูลองค์กร"""
    updated_org = twin_service.update_organization(db, org_id, org)
    if not updated_org:
        raise HTTPException(status_code=404, detail="ไม่พบข้อมูลองค์กรนี้")
    return updated_org

@router.delete("/organizations/{org_id}", response_model=OrganizationSchema)
def delete_organization(
    org_id: int,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user)
):
    """ลบข้อมูลองค์กร"""
    deleted_org = twin_service.delete_organization(db, org_id)
    if not deleted_org:
        raise HTTPException(status_code=404, detail="ไม่พบข้อมูลองค์กรนี้")
    return deleted_org


# --- Role Endpoints ---
@router.post("/roles", response_model=RoleSchema, status_code=status.HTTP_201_CREATED)
def create_role(
    role: RoleCreate,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user)
):
    """สร้างบทบาท (Role Twin) ในองค์กร"""
    return twin_service.create_role(db, role)

@router.get("/roles/{role_id}", response_model=RoleSchema)
def get_role(
    role_id: int,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user)
):
    """ดึงข้อมูลบทบาทบทบาทตาม ID"""
    db_role = twin_service.get_role(db, role_id)
    if not db_role:
        raise HTTPException(status_code=404, detail="ไม่พบข้อมูลบทบาทนี้")
    return db_role

@router.put("/roles/{role_id}", response_model=RoleSchema)
def update_role(
    role_id: int,
    role: RoleUpdate,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user)
):
    """แก้ไขข้อมูลบทบาท"""
    updated_role = twin_service.update_role(db, role_id, role)
    if not updated_role:
        raise HTTPException(status_code=404, detail="ไม่พบข้อมูลบทบาทนี้")
    return updated_role

@router.delete("/roles/{role_id}", response_model=RoleSchema)
def delete_role(
    role_id: int,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user)
):
    """ลบข้อมูลบทบาท"""
    deleted_role = twin_service.delete_role(db, role_id)
    if not deleted_role:
        raise HTTPException(status_code=404, detail="ไม่พบข้อมูลบทบาทนี้")
    return deleted_role


# --- Person Endpoints ---
@router.post("/persons", response_model=PersonSchema, status_code=status.HTTP_201_CREATED)
def create_person(
    person: PersonCreate,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user)
):
    """ลงทะเบียนข้อมูลบุคคล (Person Twin)"""
    return twin_service.create_person(db, person)

@router.get("/persons/{person_id}", response_model=PersonSchema)
def get_person(
    person_id: int,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user)
):
    """ดึงข้อมูลบุคคลตาม ID"""
    db_person = twin_service.get_person(db, person_id)
    if not db_person:
        raise HTTPException(status_code=404, detail="ไม่พบข้อมูลบุคคลนี้")
    return db_person

@router.put("/persons/{person_id}", response_model=PersonSchema)
def update_person(
    person_id: int,
    person: PersonUpdate,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user)
):
    """แก้ไขข้อมูลบุคคล"""
    updated_person = twin_service.update_person(db, person_id, person)
    if not updated_person:
        raise HTTPException(status_code=404, detail="ไม่พบข้อมูลบุคคลนี้")
    return updated_person

@router.delete("/persons/{person_id}", response_model=PersonSchema)
def delete_person(
    person_id: int,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user)
):
    """ลบข้อมูลบุคคล"""
    deleted_person = twin_service.delete_person(db, person_id)
    if not deleted_person:
        raise HTTPException(status_code=404, detail="ไม่พบข้อมูลบุคคลนี้")
    return deleted_person


@router.get("/roles", response_model=List[RoleSchema])
def get_roles(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user)
):
    """ดึงรายการบทบาททั้งหมด"""
    return twin_service.get_roles(db, skip, limit)


@router.get("/persons", response_model=List[PersonSchema])
def get_persons(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user)
):
    """ดึงรายการบุคคลทั้งหมด"""
    return twin_service.get_persons(db, skip, limit)


class SimulateRequest(BaseModel):
    opd_load: float
    icu_beds: int
    staff_fte: float

class OrchestrateRequest(BaseModel):
    goal: str

@router.post("/simulate")
def simulate_twin_metrics(req: SimulateRequest, db: Session = Depends(get_db)):
    """[Digital Twin Simulation] จำลองเหตุการณ์ What-If และพยากรณ์จุดคอขวดและประสิทธิภาพของแผนก"""
    try:
        opd_waiting_time = max(10, int(30 * req.opd_load * (1.3 - req.staff_fte)))
        bed_occupancy = min(100, max(10, int(85 * req.opd_load - (req.icu_beds - 12) * 1.5)))
        
        bottleneck = "ปกติ"
        recommendation = "การจัดสรรทรัพยากรมีความสมดุลดี"
        
        if opd_waiting_time > 40:
            bottleneck = "แผนกผู้ป่วยนอก (OPD) หนาแน่นเกินขีดจำกัด"
            recommendation = "แนะนำให้เปิดขยายบริการเทเลเมดิซีน (Telemedicine) เพื่อลดคิว และเกลี่ยกำลังคนจากจุดที่ไม่วิกฤต"
        elif bed_occupancy > 95:
            bottleneck = "หอผู้ป่วยหนัก (ICU) เข้าสู่สภาวะวิกฤตครองเตียงสูง"
            recommendation = "แนะนำให้เร่งประสานเครือข่ายส่งต่อระดับจังหวัด (Referral Network) เพื่อระบายเตียงเคสฟื้นฟู"
        elif req.staff_fte < 0.8:
            bottleneck = "วิกฤตการขาดแคลนบุคลากรหน้างาน (Staff Shortage)"
            recommendation = "แนะนำให้ฝ่ายทรัพยากร (HR) จัดสรร OT เสริม หรือหมุนเวียนเวรปฏิบัติการชั่วคราว"
            
        return {
            "status": "success",
            "metrics": {
                "opd_waiting_time": opd_waiting_time,
                "bed_occupancy": bed_occupancy,
                "bottleneck": bottleneck,
                "recommendation": recommendation
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"การจำลองสถานการณ์ขัดข้อง: {str(e)}")

@router.post("/orchestrate")
def orchestrate_enterprise_flow(req: OrchestrateRequest, db: Session = Depends(get_db)):
    """[Master Orchestrator] รับเป้าหมายแบบ Goal-Centric แตกและส่งต่อให้เอเจนต์ประมวลผลเป็นระบบ"""
    from backend.app.services.orchestrator import MasterOrchestrator
    try:
        result = MasterOrchestrator.orchestrate_task(db, req.goal)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ระบบ Master Orchestrator ขัดข้อง: {str(e)}")


