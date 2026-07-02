import logging
from typing import List, Optional

from sqlalchemy.orm import Session

from .. import models
from ..schemas.twin_schemas import (
    OrganizationCreate,
    OrganizationUpdate,
    RoleCreate,
    RoleUpdate,
    PersonCreate,
    PersonUpdate,
    KnowledgeCreate,
    KnowledgeUpdate,
    AgentCreate,
    AgentUpdate,
)

logger = logging.getLogger(__name__)

# Organization CRUD

def get_organization(db: Session, org_id: int) -> Optional[models.Organization]:
    return db.query(models.Organization).filter(models.Organization.id == org_id).first()

def get_organizations(db: Session, skip: int = 0, limit: int = 100) -> List[models.Organization]:
    return db.query(models.Organization).offset(skip).limit(limit).all()

def create_organization(db: Session, org: OrganizationCreate) -> models.Organization:
    db_org = models.Organization(**org.dict())
    db.add(db_org)
    db.commit()
    db.refresh(db_org)
    return db_org

def update_organization(db: Session, org_id: int, org: OrganizationUpdate) -> Optional[models.Organization]:
    db_org = get_organization(db, org_id)
    if not db_org:
        return None
    for field, value in org.dict(exclude_unset=True).items():
        setattr(db_org, field, value)
    db.commit()
    db.refresh(db_org)
    return db_org

def delete_organization(db: Session, org_id: int) -> Optional[models.Organization]:
    db_org = get_organization(db, org_id)
    if not db_org:
        return None
    db.delete(db_org)
    db.commit()
    return db_org

# Role CRUD

def get_role(db: Session, role_id: int) -> Optional[models.Role]:
    return db.query(models.Role).filter(models.Role.id == role_id).first()

def get_roles(db: Session, skip: int = 0, limit: int = 100) -> List[models.Role]:
    return db.query(models.Role).offset(skip).limit(limit).all()

def create_role(db: Session, role: RoleCreate) -> models.Role:
    db_role = models.Role(**role.dict())
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

def update_role(db: Session, role_id: int, role: RoleUpdate) -> Optional[models.Role]:
    db_role = get_role(db, role_id)
    if not db_role:
        return None
    for field, value in role.dict(exclude_unset=True).items():
        setattr(db_role, field, value)
    db.commit()
    db.refresh(db_role)
    return db_role

def delete_role(db: Session, role_id: int) -> Optional[models.Role]:
    db_role = get_role(db, role_id)
    if not db_role:
        return None
    db.delete(db_role)
    db.commit()
    return db_role

# Person CRUD

def get_person(db: Session, person_id: int) -> Optional[models.Person]:
    return db.query(models.Person).filter(models.Person.id == person_id).first()

def get_persons(db: Session, skip: int = 0, limit: int = 100) -> List[models.Person]:
    return db.query(models.Person).offset(skip).limit(limit).all()

def create_person(db: Session, person: PersonCreate) -> models.Person:
    person_data = person.dict(exclude={"role_ids"})
    db_person = models.Person(**person_data)
    if person.role_ids:
        roles = db.query(models.Role).filter(models.Role.id.in_(person.role_ids)).all()
        db_person.roles = roles
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person

def update_person(db: Session, person_id: int, person: PersonUpdate) -> Optional[models.Person]:
    db_person = get_person(db, person_id)
    if not db_person:
        return None
    person_data = person.dict(exclude_unset=True, exclude={"role_ids"})
    for field, value in person_data.items():
        setattr(db_person, field, value)
    if person.role_ids is not None:
        roles = db.query(models.Role).filter(models.Role.id.in_(person.role_ids)).all()
        db_person.roles = roles
    db.commit()
    db.refresh(db_person)
    return db_person


def delete_person(db: Session, person_id: int) -> Optional[models.Person]:
    db_person = get_person(db, person_id)
    if not db_person:
        return None
    db.delete(db_person)
    db.commit()
    return db_person

# Knowledge CRUD

def get_knowledge(db: Session, knowledge_id: int) -> Optional[models.Knowledge]:
    return db.query(models.Knowledge).filter(models.Knowledge.id == knowledge_id).first()

def create_knowledge(db: Session, knowledge: KnowledgeCreate) -> models.Knowledge:
    db_knowledge = models.Knowledge(**knowledge.dict())
    db.add(db_knowledge)
    db.commit()
    db.refresh(db_knowledge)
    return db_knowledge

def update_knowledge(db: Session, knowledge_id: int, knowledge: KnowledgeUpdate) -> Optional[models.Knowledge]:
    db_knowledge = get_knowledge(db, knowledge_id)
    if not db_knowledge:
        return None
    for field, value in knowledge.dict(exclude_unset=True).items():
        setattr(db_knowledge, field, value)
    db.commit()
    db.refresh(db_knowledge)
    return db_knowledge

def delete_knowledge(db: Session, knowledge_id: int) -> Optional[models.Knowledge]:
    db_knowledge = get_knowledge(db, knowledge_id)
    if not db_knowledge:
        return None
    db.delete(db_knowledge)
    db.commit()
    return db_knowledge

# Agent CRUD

def get_agent(db: Session, agent_id: int) -> Optional[models.Agent]:
    return db.query(models.Agent).filter(models.Agent.id == agent_id).first()

def create_agent(db: Session, agent: AgentCreate) -> models.Agent:
    db_agent = models.Agent(**agent.dict())
    db.add(db_agent)
    db.commit()
    db.refresh(db_agent)
    return db_agent

def update_agent(db: Session, agent_id: int, agent: AgentUpdate) -> Optional[models.Agent]:
    db_agent = get_agent(db, agent_id)
    if not db_agent:
        return None
    for field, value in agent.dict(exclude_unset=True).items():
        setattr(db_agent, field, value)
    db.commit()
    db.refresh(db_agent)
    return db_agent

def delete_agent(db: Session, agent_id: int) -> Optional[models.Agent]:
    db_agent = get_agent(db, agent_id)
    if not db_agent:
        return None
    db.delete(db_agent)
    db.commit()
    return db_agent
