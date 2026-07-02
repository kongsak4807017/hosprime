from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.types import TypeDecorator
from backend.app.db.session import Base

# Import twin models to ensure they are registered with the main Base
from backend.app.models.twin_models import (
    Organization, Role, Person, Knowledge, Agent,
    LegalTwin, FinanceTwin, HRTwin, TBTwin, NCDTwin,
    KnowledgeNode, KnowledgeRelationship
)

# Custom SQLAlchemy type to handle Vector on PostgreSQL and fallback to Text on SQLite
class SafeVector(TypeDecorator):
    impl = Text
    cache_ok = True
    
    def __init__(self, dim=3072, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dim = dim

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            try:
                from pgvector.sqlalchemy import Vector
                return dialect.type_descriptor(Vector(self.dim))
            except ImportError:
                pass
        return dialect.type_descriptor(Text)

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        if dialect.name == "postgresql":
            return value
        import json
        if isinstance(value, list):
            return json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        if dialect.name == "postgresql":
            return value
        import json
        try:
            if isinstance(value, str):
                return json.loads(value)
        except Exception:
            pass
        return value

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    document_type = Column(String(100), nullable=True)  # Policy, SOP, Meeting Notes, Report
    department = Column(String(100), nullable=True)     # แผนกที่เกี่ยวข้อง
    program = Column(String(100), nullable=True)        # แฟ้มงาน/โปรแกรม เช่น PM2.5, TB, NCD
    year = Column(String(10), nullable=True)            # ปีงบประมาณ / ปีเอกสาร
    owner = Column(String(100), nullable=True)          # ผู้จัดทำ/เจ้าของ
    confidentiality_level = Column(String(50), default="Internal") # Public, Internal, Confidential
    file_path = Column(String(500), nullable=False)
    status = Column(String(50), default="pending review") # pending review, processed, failed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    # Enterprise Metadata & PDPA Fields
    data_classification = Column(String(50), default="Internal") # Public, Internal, Confidential, Restricted
    retention_years = Column(Integer, default=7)
    pdpa_consent = Column(Boolean, default=False)
    encryption_at_rest = Column(Boolean, default=False)

    chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")
    entities = relationship("EntityRelation", back_populates="document", cascade="all, delete-orphan")

class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"), nullable=False)
    chunk_text = Column(Text, nullable=False)
    page_number = Column(Integer, nullable=True)
    section_title = Column(String(255), nullable=True)
    embedding_id = Column(String(100), nullable=True)  # ID อ้างอิง Vector Cache
    token_count = Column(Integer, default=0)
    embedding_data = Column(Text, nullable=True)       # เก็บ Vector Embedding เป็น JSON string (สำหรับ SQLite)
    embedding = Column(SafeVector(3072), nullable=True) # คอลัมน์เวกเตอร์สำหรับ pgvector (PostgreSQL)

    document = relationship("Document", back_populates="chunks")

class EntityRelation(Base):
    __tablename__ = "entity_relations"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"), nullable=False)
    source_node = Column(String(255), nullable=False)       # Entity ต้นทาง เช่น "นพ.สสจ."
    relation_type = Column(String(100), nullable=False)     # ประเภทความสัมพันธ์ เช่น "reports_to", "owns"
    target_node = Column(String(255), nullable=False)       # Entity ปลายทาง เช่น "สสจ.เชียงราย"
    source_type = Column(String(100), nullable=True)       # เช่น Person, Role, Department
    target_type = Column(String(100), nullable=True)
    confidence = Column(Float, default=1.0)
    extracted_at = Column(DateTime(timezone=True), server_default=func.now())

    document = relationship("Document", back_populates="entities")

class QueryLog(Base):
    __tablename__ = "query_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), default="guest")
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    sources = Column(Text, nullable=True)                  # ข้อมูล Chunks ที่ใช้อ้างอิงแบบ JSON string
    confidence = Column(Float, default=0.0)                # ค่าความมั่นใจในการตอบคำถาม
    feedback = Column(String(50), nullable=True)            # positive (thumbs up), negative (thumbs down)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class AgentLog(Base):
    __tablename__ = "agent_logs"

    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(String(100), nullable=False)          # ชื่อ Agent
    task_type = Column(String(100), nullable=False)         # ประเภทงาน เช่น "classification", "metadata_extraction"
    input_data = Column(Text, nullable=True)                # input ที่ส่งให้ agent (JSON string)
    output_data = Column(Text, nullable=True)               # output ที่ตอบกลับ (JSON string)
    status = Column(String(50), default="success")          # success, failed
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Meeting(Base):
    __tablename__ = "meetings"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    date = Column(String(50), nullable=True)
    audio_path = Column(String(500), nullable=True)
    transcript = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    action_items = relationship("ActionItem", back_populates="meeting", cascade="all, delete-orphan")

class ActionItem(Base):
    __tablename__ = "action_items"

    id = Column(Integer, primary_key=True, index=True)
    meeting_id = Column(Integer, ForeignKey("meetings.id", ondelete="CASCADE"), nullable=False)
    task = Column(Text, nullable=False)
    assignee = Column(String(100), nullable=False)
    due_date = Column(String(50), nullable=True)
    status = Column(String(50), default="pending")  # pending, in_progress, completed
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    meeting = relationship("Meeting", back_populates="action_items")

class WorkflowRun(Base):
    __tablename__ = "workflow_runs"

    id = Column(Integer, primary_key=True, index=True)
    workflow_name = Column(String(255), nullable=False)
    status = Column(String(100), default="RUNNING")  # RUNNING, COMPLETED, PENDING_APPROVAL, FAILED, SUSPENDED
    current_step = Column(String(255), nullable=True)
    payload_data = Column(Text, nullable=True)       # บันทึกข้อมูล Payload (JSON string)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), default="user")  # admin, knowledge_admin, twin_admin, user, guest
    department = Column(String(100), nullable=True)  # แผนก เช่น PHEOC, IT, TB
    confidentiality_level = Column(String(50), default="Internal")  # Public, Internal, Confidential
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Enterprise SSO & Security
    sso_provider = Column(String(50), nullable=True) # thaid, ldap, keycloak
    sso_subject = Column(String(255), nullable=True)
    mfa_enabled = Column(Boolean, default=False)
    last_login = Column(DateTime(timezone=True), nullable=True)

# --- Enterprise AI Governance & Audit Tables ---

class AgentRegistry(Base):
    __tablename__ = "agent_registry"

    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(String(100), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    version = Column(String(50), default="1.0.0")
    owner = Column(String(100), default="IT")
    risk_tier = Column(String(50), default="Low") # Low, Medium, High, Critical
    allowed_tools = Column(Text, default="[]")    # JSON Array ของเครื่องมือที่อนุญาต
    forbidden_actions = Column(Text, default="[]") # JSON Array ของการกระทำที่ห้าม
    model_provider = Column(String(50), default="gemini")
    model_name = Column(String(100), default="gemini-1.5-flash")
    approval_level = Column(String(50), default="None") # None, Manager, Executive
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

class AgentPermission(Base):
    __tablename__ = "agent_permissions"

    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(String(100), ForeignKey("agent_registry.agent_id", ondelete="CASCADE"), nullable=False)
    tool_name = Column(String(100), nullable=False)
    action = Column(String(50), nullable=False) # read, write, execute
    allowed = Column(Boolean, default=False)
    conditions = Column(Text, nullable=True) # JSON object ของเงื่อนไขเพิ่มเติม

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    agent_id = Column(String(100), nullable=True)
    workflow_id = Column(String(100), nullable=True)
    user_id = Column(String(100), nullable=True)
    action_type = Column(String(100), nullable=False)
    input_data = Column(Text, nullable=True) # JSON string
    output_data = Column(Text, nullable=True) # JSON string
    tools_used = Column(Text, nullable=True) # JSON string
    decisions = Column(Text, nullable=True) # JSON string
    approval_token = Column(String(100), nullable=True)
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(Text, nullable=True)

class CostLog(Base):
    __tablename__ = "cost_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    agent_id = Column(String(100), nullable=True)
    provider = Column(String(50), nullable=True)
    model = Column(String(100), nullable=True)
    input_tokens = Column(Integer, default=0)
    output_tokens = Column(Integer, default=0)
    cost_usd = Column(Float, default=0.0)
    request_id = Column(String(100), nullable=True)

class HITLQueue(Base):
    __tablename__ = "hitl_queue"

    id = Column(Integer, primary_key=True, index=True)
    workflow_id = Column(String(100), nullable=False, index=True)
    task_id = Column(String(100), nullable=False)
    agent_id = Column(String(100), nullable=True)
    status = Column(String(50), default="pending") # pending, approved, rejected, expired
    requested_at = Column(DateTime(timezone=True), server_default=func.now())
    approved_at = Column(DateTime(timezone=True), nullable=True)
    approved_by = Column(String(100), nullable=True)
    approval_token = Column(String(100), nullable=True)
    payload = Column(Text, nullable=True) # JSON string
    context = Column(Text, nullable=True) # JSON string



