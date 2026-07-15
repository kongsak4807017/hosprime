import os
import sys
import glob
import logging

# เพิ่มระดับ Root ของโครงการเข้าไปใน sys.path เพื่อป้องกัน ModuleNotFoundError
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from sqlalchemy import text
from sqlalchemy.orm import Session
from backend.app.db.session import engine, SessionLocal
from backend.app.db.models import Base, Document, User as DBUser, EntityRelation
from backend.app.agents.agents import KnowledgeIngestionAgent
from backend.app.auth import get_password_hash


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def ensure_database_extensions() -> None:
    """Create database extensions required by SQLAlchemy column types.

    The pgvector image ships the extension binaries but PostgreSQL still
    requires CREATE EXTENSION for each database before tables using VECTOR
    columns can be created. SQLite-based tests do not require this step.
    """
    if engine.dialect.name != "postgresql":
        return

    logger.info("Ensuring required PostgreSQL extensions are enabled...")
    with engine.begin() as connection:
        connection.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
    logger.info("PostgreSQL extension 'vector' is ready.")


def bootstrap_data():
    logger.info("Initializing database schema...")
    ensure_database_extensions()
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    logger.info("Database schema initialized successfully.")

    db: Session = SessionLocal()
    try:
        # สร้างผู้ใช้เริ่มต้น (Default Users)
        logger.info("Creating default users...")
        admin_user = DBUser(
            username="admin",
            hashed_password=get_password_hash("admin1234"),
            role="admin",
            department="IT",
            confidentiality_level="Confidential"
        )
        general_user = DBUser(
            username="user",
            hashed_password=get_password_hash("user1234"),
            role="user",
            department="PHEOC",
            confidentiality_level="Internal"
        )
        db.add(admin_user)
        db.add(general_user)
        db.commit()
        logger.info("Default users (admin/user) created successfully.")

        # สร้าง AI Agents เริ่มต้นสำหรับบอร์ดกำกับดูแลและการเงินจำลอง
        logger.info("Creating default AI Agent Twins for Governance Board...")
        from backend.app.models.twin_models import Agent
        
        default_agents = [
            Agent(name="Executive (Digital CEO)", role="executive", status="idle", is_active=True, temperature=0.2, token_quota=200000, token_used=50000, token_balance=150000, token_rewarded=15000),
            Agent(name="Chief of Staff (ผู้จัดการสำนักงาน)", role="cos", status="idle", is_active=True, temperature=0.3, token_quota=150000, token_used=40000, token_balance=110000, token_rewarded=12000),
            Agent(name="Analyst (ฝ่ายวิเคราะห์ยุทธศาสตร์)", role="analyst", status="idle", is_active=True, temperature=0.3, token_quota=120000, token_used=25000, token_balance=95000, token_rewarded=8000),
            Agent(name="Knowledge (ผู้ช่วยคลังปัญญา)", role="knowledge", status="idle", is_active=True, temperature=0.2, token_quota=100000, token_used=12000, token_balance=88000, token_rewarded=4500),
            Agent(name="Report (ผู้ร่างเล่มรายงาน)", role="report", status="idle", is_active=True, temperature=0.3, token_quota=150000, token_used=30000, token_balance=120000, token_rewarded=14000),
            Agent(name="Meeting (ผู้ถอดสรุปประชุม)", role="meeting", status="idle", is_active=True, temperature=0.2, token_quota=100000, token_used=15000, token_balance=85000, token_rewarded=5000),
            Agent(name="Data Governance (ธรรมภิบาลข้อมูล)", role="datagov", status="idle", is_active=True, temperature=0.1, token_quota=80000, token_used=8000, token_balance=72000, token_rewarded=2500),
            Agent(name="CFO (ฝ่ายการคลัง)", role="cfo", status="idle", is_active=True, temperature=0.3, token_quota=120000, token_used=22005, token_balance=98000, token_rewarded=9500),
            Agent(name="COO (ฝ่ายบริการ)", role="coo", status="idle", is_active=True, temperature=0.3, token_quota=120000, token_used=28000, token_balance=92000, token_rewarded=8500),
            Agent(name="Provincial Brain (มันสมองจังหวัด)", role="provincial", status="idle", is_active=True, temperature=0.2, token_quota=180000, token_used=35000, token_balance=145000, token_rewarded=11000)
        ]
        
        for agent in default_agents:
            existing = db.query(Agent).filter(Agent.role == agent.role).first()
            if not existing:
                db.add(agent)
        db.commit()
        logger.info("Default AI Agent Twins created successfully.")

        # ค้นหาไฟล์เดโมทั้งหมดใน demo_data (ถอยขึ้นไป 4 ชั้นไปยัง Root ของโปรเจกต์)
        root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        demo_files_path = os.path.join(root_dir, "demo_data", "*.md")
        demo_files = glob.glob(demo_files_path)
        
        if not demo_files:
            logger.warning("No demo files found in demo_data folder.")
            return

        logger.info(f"Found {len(demo_files)} demo files to ingest.")
        
        for file_path in demo_files:
            filename = os.path.basename(file_path)
            # ตั้งชื่อเรื่องจากชื่อไฟล์แบบง่ายๆ
            title = filename.replace(".md", "").replace("_", " ").title()
            
            logger.info(f"Ingesting: {filename}...")
            try:
                # ทำการ Ingest ผ่าน Agent
                doc = KnowledgeIngestionAgent.ingest(
                    db=db,
                    file_path=file_path,
                    title=title,
                    confidentiality_level="Internal"
                )
                # อนุมัติโดยอัตโนมัติเพื่อให้ค้นหาได้ทันทีในเดโม
                doc.status = "processed"
                db.commit()
                logger.info(f"Successfully ingested and approved: {doc.title} (ID: {doc.id})")
            except Exception as e:
                logger.error(f"Failed to ingest file {filename}: {e}")
                
        # สร้างความสัมพันธ์ข้อมูลระดับจังหวัดจำลอง (Entity Relations) เพื่อให้แสดงผลโครงข่ายเชื่อมโยงได้จริงๆ
        logger.info("Generating entity relations for demo documents...")
        
        pm25_doc = db.query(Document).filter(Document.title.like("%Pm25%")).first()
        tb_doc = db.query(Document).filter(Document.title.like("%Tb%")).first()
        ncd_doc = db.query(Document).filter(Document.title.like("%Ncd%")).first()
        flood_doc = db.query(Document).filter(Document.title.like("%Flood%")).first()
        digital_doc = db.query(Document).filter(Document.title.like("%Digital%")).first()

        relations_to_create = []

        if pm25_doc:
            relations_to_create.extend([
                EntityRelation(document_id=pm25_doc.id, source_node="สสจ.เชียงราย", relation_type="owns", target_node="แผนควบคุมฝุ่น PM2.5", source_type="Organization", target_type="Project", confidence=1.0),
                EntityRelation(document_id=pm25_doc.id, source_node="กลุ่มงานควบคุมโรค", relation_type="implements", target_node="มาตรการห้ามเผาเด็ดขาด", source_type="Department", target_type="KPI", confidence=1.0),
                EntityRelation(document_id=pm25_doc.id, source_node="นพ.สสจ.", relation_type="approves", target_node="การจัดสรรเครื่องฟอกอากาศ", source_type="Role", target_type="Project", confidence=1.0),
                EntityRelation(document_id=pm25_doc.id, source_node="กลุ่มเปราะบาง", relation_type="receives", target_node="หน้ากาก N95", source_type="Person", target_type="Project", confidence=1.0)
            ])

        if tb_doc:
            relations_to_create.extend([
                EntityRelation(document_id=tb_doc.id, source_node="สสจ.เชียงราย", relation_type="owns", target_node="แผนงาน Active Case Finding", source_type="Organization", target_type="Project", confidence=1.0),
                EntityRelation(document_id=tb_doc.id, source_node="กลุ่มงานควบคุมโรค", relation_type="supports", target_node="วัณโรค (TB)", source_type="Department", target_type="Program", confidence=1.0),
                EntityRelation(document_id=tb_doc.id, source_node="โรงพยาบาลเป้าหมาย", relation_type="utilizes", target_node="ระบบตรวจยีน GeneXpert", source_type="Department", target_type="Project", confidence=1.0),
                EntityRelation(document_id=tb_doc.id, source_node="เรือนจำเชียงราย", relation_type="undergoes", target_node="การตรวจคัดกรองเชิงรุก", source_type="Department", target_type="KPI", confidence=1.0)
            ])

        if ncd_doc:
            relations_to_create.extend([
                EntityRelation(document_id=ncd_doc.id, source_node="สสจ.เชียงราย", relation_type="owns", target_node="เบาหวานระยะสงบ (NCD Remission)", source_type="Organization", target_type="Program", confidence=1.0),
                EntityRelation(document_id=ncd_doc.id, source_node="กลุ่มงานควบคุมโรค", relation_type="implements", target_node="คลินิก NCD Remission", source_type="Department", target_type="Project", confidence=1.0),
                EntityRelation(document_id=ncd_doc.id, source_node="รพ.สต.เครือข่าย", relation_type="monitors", target_node="ผู้ป่วยโรคเบาหวาน", source_type="Department", target_type="Person", confidence=1.0)
            ])

        if flood_doc:
            relations_to_create.extend([
                EntityRelation(document_id=flood_doc.id, source_node="สสจ.เชียงราย", relation_type="coordinates", target_node="ทีมปฏิบัติการ PHEOC", source_type="Organization", target_type="Department", confidence=1.0),
                EntityRelation(document_id=flood_doc.id, source_node="นพ.สสจ.", relation_type="leads", target_node="ศูนย์ PHEOC จังหวัด", source_type="Role", target_type="Department", confidence=1.0),
                EntityRelation(document_id=flood_doc.id, source_node="ทีม MCATT", relation_type="assists", target_node="กลุ่มเปราะบาง/ผู้ป่วยติดเตียง", source_type="Department", target_type="Person", confidence=1.0)
            ])

        if digital_doc:
            relations_to_create.extend([
                EntityRelation(document_id=digital_doc.id, source_node="สสจ.เชียงราย", relation_type="owns", target_node="แผนสุขภาพดิจิทัล", source_type="Organization", target_type="Project", confidence=1.0),
                EntityRelation(document_id=digital_doc.id, source_node="กลุ่มงานยุทธศาสตร์", relation_type="manages", target_node="FHIR Gateway", source_type="Department", target_type="Project", confidence=1.0),
                EntityRelation(document_id=digital_doc.id, source_node="บุคลากรไอที", relation_type="maintains", target_node="ระบบความปลอดภัยไซเบอร์", source_type="Role", target_type="KPI", confidence=1.0)
            ])

        if relations_to_create:
            db.bulk_save_objects(relations_to_create)
            db.commit()
            logger.info(f"Successfully generated {len(relations_to_create)} entity relations in Database.")

        logger.info("Database bootstrapping completed successfully.")
    finally:
        db.close()

if __name__ == "__main__":
    bootstrap_data()
