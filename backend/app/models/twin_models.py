from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table, Boolean, Float
from sqlalchemy.orm import relationship
from backend.app.db.session import Base

person_role = Table(
    "person_role",
    Base.metadata,
    Column("person_id", Integer, ForeignKey("person_twin.id"), primary_key=True),
    Column("role_id", Integer, ForeignKey("role_twin.id"), primary_key=True),
)

class Organization(Base):
    __tablename__ = "organization_twin"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    roles = relationship("Role", back_populates="organization")

class Role(Base):
    __tablename__ = "role_twin"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    organization_id = Column(Integer, ForeignKey("organization_twin.id"))
    organization = relationship("Organization", back_populates="roles")
    persons = relationship("Person", secondary=person_role, back_populates="roles")

class Person(Base):
    __tablename__ = "person_twin"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String)
    roles = relationship("Role", secondary=person_role, back_populates="persons")
    knowledge_id = Column(Integer, ForeignKey("knowledge_twin.id"))
    knowledge = relationship("Knowledge", back_populates="person", uselist=False)

class Knowledge(Base):
    __tablename__ = "knowledge_twin"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    person = relationship("Person", back_populates="knowledge")
    nodes = relationship("KnowledgeNode", back_populates="knowledge")

class Agent(Base):
    __tablename__ = "agent_twin"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    role = Column(String)
    status = Column(String, default="idle")
    person_id = Column(Integer, ForeignKey("person_twin.id"), nullable=True)
    person = relationship("Person")
    model_name = Column(String, default='gemini-2.5-flash')
    
    # AI Governance & Token Economy
    is_active = Column(Boolean, default=True)
    temperature = Column(Float, default=0.3)
    token_quota = Column(Integer, default=100000)
    token_used = Column(Integer, default=0)
    token_balance = Column(Integer, default=50000)
    token_rewarded = Column(Integer, default=0)

class LegalTwin(Agent):
    __tablename__ = "legal_twin"
    id = Column(Integer, ForeignKey("agent_twin.id"), primary_key=True)

class FinanceTwin(Agent):
    __tablename__ = "finance_twin"
    id = Column(Integer, ForeignKey("agent_twin.id"), primary_key=True)

class HRTwin(Agent):
    __tablename__ = "hr_twin"
    id = Column(Integer, ForeignKey("agent_twin.id"), primary_key=True)

class TBTwin(Agent):
    __tablename__ = "tb_twin"
    id = Column(Integer, ForeignKey("agent_twin.id"), primary_key=True)

class NCDTwin(Agent):
    __tablename__ = "ncd_twin"
    id = Column(Integer, ForeignKey("agent_twin.id"), primary_key=True)

class KnowledgeNode(Base):
    __tablename__ = "knowledge_node"
    id = Column(Integer, primary_key=True, index=True)
    label = Column(String, nullable=False)
    type = Column(String)
    knowledge_id = Column(Integer, ForeignKey("knowledge_twin.id"))
    knowledge = relationship("Knowledge", back_populates="nodes")
    relationships = relationship(
        "KnowledgeRelationship",
        back_populates="source_node",
        foreign_keys="KnowledgeRelationship.source_id",
    )

class KnowledgeRelationship(Base):
    __tablename__ = "knowledge_relationship"
    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer, ForeignKey("knowledge_node.id"))
    target_id = Column(Integer, ForeignKey("knowledge_node.id"))
    relation_type = Column(String)
    source_node = relationship(
        "KnowledgeNode",
        foreign_keys=[source_id],
        back_populates="relationships",
    )
    target_node = relationship("KnowledgeNode", foreign_keys=[target_id])
