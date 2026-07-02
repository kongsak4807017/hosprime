from pydantic import BaseModel, Field
from typing import List, Optional

class OrganizationBase(BaseModel):
    name: str = Field(..., title="Organization Name")
    description: Optional[str] = Field(None, title="Description")

class OrganizationCreate(OrganizationBase):
    pass

class OrganizationUpdate(OrganizationBase):
    pass

class OrganizationSchema(OrganizationBase):
    id: int
    class Config:
        orm_mode = True

class RoleBase(BaseModel):
    title: str = Field(..., title="Role Title")
    organization_id: int = Field(..., title="Organization ID")

class RoleCreate(RoleBase):
    pass

class RoleUpdate(RoleBase):
    pass

class RoleSchema(RoleBase):
    id: int
    class Config:
        orm_mode = True

class PersonBase(BaseModel):
    full_name: str = Field(..., title="Full Name")
    email: Optional[str] = Field(None, title="Email")

class PersonCreate(PersonBase):
    knowledge_id: Optional[int] = None
    role_ids: Optional[List[int]] = None

class PersonUpdate(PersonBase):
    knowledge_id: Optional[int] = None
    role_ids: Optional[List[int]] = None

class PersonSchema(PersonBase):
    id: int
    knowledge_id: Optional[int]
    roles: Optional[List[RoleSchema]] = None
    class Config:
        orm_mode = True

class KnowledgeBase(BaseModel):
    content: Optional[str] = Field(None, title="Extracted Knowledge JSON")

class KnowledgeCreate(KnowledgeBase):
    pass

class KnowledgeUpdate(KnowledgeBase):
    pass

class KnowledgeSchema(KnowledgeBase):
    id: int
    class Config:
        orm_mode = True

class AgentBase(BaseModel):
    name: str = Field(..., title="Agent Name")
    role: Optional[str] = Field(None, title="Agent Role")
    status: Optional[str] = Field('idle', title="Current Status")

class AgentCreate(AgentBase):
    person_id: Optional[int] = None

class AgentUpdate(AgentBase):
    person_id: Optional[int] = None

class AgentSchema(AgentBase):
    id: int
    class Config:
        orm_mode = True
