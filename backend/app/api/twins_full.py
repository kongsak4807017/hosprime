from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..db.session import get_db
from ..auth import get_current_user
from ..schemas.twin_schemas import (
    OrganizationCreate,
    OrganizationUpdate,
    OrganizationSchema,
    RoleCreate,
    RoleUpdate,
    RoleSchema,
    PersonCreate,
    PersonUpdate,
    PersonSchema,
    KnowledgeCreate,
    KnowledgeUpdate,
    KnowledgeSchema,
    AgentCreate,
    AgentUpdate,
    AgentSchema,
)
from ..services.twin_service import (
    get_organizations,
    get_organization,
    create_organization,
    update_organization,
    delete_organization,
    get_roles,
    get_role,
    create_role,
    update_role,
    delete_role,
    get_people,
    get_person,
    create_person,
    update_person,
    delete_person,
    get_knowledge_items,
    get_knowledge,
    create_knowledge,
    update_knowledge,
    delete_knowledge,
    get_agents,
    get_agent,
    create_agent,
    update_agent,
    delete_agent,
)

router = APIRouter(prefix="/twins", tags=["twins"])

# ---------- Organization ----------
@router.get("/organizations", response_model=list[OrganizationSchema])
def list_organizations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), user: object = Depends(get_current_user)):
    return get_organizations(db, skip=skip, limit=limit)

@router.get("/organizations/{org_id}", response_model=OrganizationSchema)
def read_organization(org_id: int, db: Session = Depends(get_db), user: object = Depends(get_current_user)):
    org = get_organization(db, org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org

@router.post("/organizations", response_model=OrganizationSchema, status_code=status.HTTP_201_CREATED)
def create_new_organization(org: OrganizationCreate, db: Session = Depends(get_db), user: object = Depends(get_current_user)):
    return create_organization(db, org)

@router.put("/organizations/{org_id}", response_model=OrganizationSchema)
def update_existing_organization(org_id: int, org: OrganizationUpdate, db: Session = Depends(get_db), user: object = Depends(get_current_user)):
    updated = update_organization(db, org_id, org)
    if not updated:
        raise HTTPException(status_code=404, detail="Organization not found")
    return updated

@router.delete("/organizations/{org_id}", response_model=OrganizationSchema)
def delete_existing_organization(org_id: int, db: Session = Depends(get_db), user: object = Depends(get_current_user)):
    deleted = delete_organization(db, org_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Organization not found")
    return deleted

# ---------- Role ----------
@router.get("/roles", response_model=list[RoleSchema])
def list_roles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), user: object = Depends(get_current_user)):
    return get_roles(db, skip=skip, limit=limit)

@router.get("/roles/{role_id}", response_model=RoleSchema)
def read_role(role_id: int, db: Session = Depends(get_db), user: object = Depends(get_current_user)):
    role = get_role(db, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

@router.post("/roles", response_model=RoleSchema, status_code=status.HTTP_201_CREATED)
def create_new_role(role: RoleCreate, db: Session = Depends(get_db), user: object = Depends(get_current_user)):
    return create_role(db, role)

@router.put("/roles/{role_id}", response_model=RoleSchema)
def update_existing_role(role_id: int, role: RoleUpdate, db: Session = Depends(get_db), user: object = Depends(get_current_user)):
    updated = update_role(db, role_id, role)
    if not updated:
        raise HTTPException(status_code=404, detail="Role not found")
    return updated

@router.delete("/roles/{role_id}", response_model=RoleSchema)
def delete_existing_role(role_id: int, db: Session = Depends(get_db), user: object = Depends(get_current_user)):
    deleted = delete_role(db, role_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Role not found")
    return deleted

# ---------- Person ----------
@router.get("/people", response_model=list[PersonSchema])
def list_people(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), user: object = Depends(get_current_user)):
    return get_people(db, skip=skip, limit=limit)

@router.get("/people/{person_id}", response_model=PersonSchema)
def read_person(person_id: int, db: Session = Depends(get_db), user: object = Depends(get_current_user)):
    person = get_person(db, person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    return person

@router.post("/people", response_model=PersonSchema, status_code=status.HTTP_201_CREATED)
def create_new_person(person: PersonCreate, db: Session = Depends(get_db), user: object = Depends(get_current_user)):
    return create_person(db, person)

@router.put("/people/{person_id}", response_model=PersonSchema)
def update_existing_person(person_id: int, person: PersonUpdate, db: Session = Depends(get_db), user: object = Depends(get_current_user)):
    updated = update_person(db, person_id, person)
    if not updated:
        raise HTTPException(status_code=404, detail="Person not found")
    return updated

@router.delete("/people/{person_id}", response_model=PersonSchema)
def delete_existing_person(person_id: int, db: Session = Depends(get_db), user: object = Depends(get_current_user)):
    deleted = delete_person(db, person_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Person not found")
    return deleted

# ---------- Knowledge ----------
@router.get("/knowledge", response_model=list[KnowledgeSchema])
def list_knowledge(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), user: object = Depends(get_current_user)):
    return get_knowledge_items(db, skip=skip, limit=limit)

@router.get("/knowledge/{knowledge_id}", response_model=KnowledgeSchema)
def read_knowledge(knowledge_id: int, db: Session = Depends(get_db), user: object = Depends(get_current_user)):
    knowledge = get_knowledge(db, knowledge_id)
    if not knowledge:
        raise HTTPException(status_code=404, detail="Knowledge not found")
    return knowledge

@router.post("/knowledge", response_model=KnowledgeSchema, status_code=status.HTTP_201_CREATED)
def create_new_knowledge(knowledge: KnowledgeCreate, db: Session = Depends(get_db), user: object = Depends(get_current_user)):
    return create_knowledge(db, knowledge)

@router.put("/knowledge/{knowledge_id}", response_model=KnowledgeSchema)
def update_existing_knowledge(knowledge_id: int, knowledge: KnowledgeUpdate, db: Session = Depends(get_db), user: object = Depends(get_current_user)):
    updated = update_knowledge(db, knowledge_id, knowledge)
    if not updated:
        raise HTTPException(status_code=404, detail="Knowledge not found")
    return updated

@router.delete("/knowledge/{knowledge_id}", response_model=KnowledgeSchema)
def delete_existing_knowledge(knowledge_id: int, db: Session = Depends(get_db), user: object = Depends(get_current_user)):
    deleted = delete_knowledge(db, knowledge_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Knowledge not found")
    return deleted

# ---------- Agent ----------
@router.get("/agents", response_model=list[AgentSchema])
def list_agents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), user: object = Depends(get_current_user)):
    return get_agents(db, skip=skip, limit=limit)

@router.get("/agents/{agent_id}", response_model=AgentSchema)
def read_agent(agent_id: int, db: Session = Depends(get_db), user: object = Depends(get_current_user)):
    agent = get_agent(db, agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent

@router.post("/agents", response_model=AgentSchema, status_code=status.HTTP_201_CREATED)
def create_new_agent(agent: AgentCreate, db: Session = Depends(get_db), user: object = Depends(get_current_user)):
    return create_agent(db, agent)

@router.put("/agents/{agent_id}", response_model=AgentSchema)
def update_existing_agent(agent_id: int, agent: AgentUpdate, db: Session = Depends(get_db), user: object = Depends(get_current_user)):
    updated = update_agent(db, agent_id, agent)
    if not updated:
        raise HTTPException(status_code=404, detail="Agent not found")
    return updated

@router.delete("/agents/{agent_id}", response_model=AgentSchema)
def delete_existing_agent(agent_id: int, db: Session = Depends(get_db), user: object = Depends(get_current_user)):
    deleted = delete_agent(db, agent_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Agent not found")
    return deleted
