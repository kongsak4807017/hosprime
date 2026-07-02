from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

# --- Document Schemas ---
class DocumentBase(BaseModel):
    title: str
    document_type: Optional[str] = None
    department: Optional[str] = None
    program: Optional[str] = None
    year: Optional[str] = None
    owner: Optional[str] = None
    confidentiality_level: Optional[str] = "Internal"

class DocumentCreate(DocumentBase):
    file_path: str
    status: Optional[str] = "pending review"

class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    document_type: Optional[str] = None
    department: Optional[str] = None
    program: Optional[str] = None
    year: Optional[str] = None
    owner: Optional[str] = None
    confidentiality_level: Optional[str] = None
    status: Optional[str] = None

class DocumentResponse(DocumentBase):
    id: int
    file_path: str
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# --- Entity Relation Schemas ---
class EntityRelationResponse(BaseModel):
    id: int
    document_id: int
    source_node: str
    relation_type: str
    target_node: str
    source_type: Optional[str] = None
    target_type: Optional[str] = None
    confidence: float
    extracted_at: datetime

    class Config:
        from_attributes = True

# --- Oracle Query Schemas ---
class QueryRequest(BaseModel):
    question: str
    user_id: Optional[str] = "guest"

class SourceChunkInfo(BaseModel):
    document_id: int
    document_title: str
    chunk_id: int
    chunk_text: str
    page_number: Optional[int] = None
    section_title: Optional[str] = None
    score: float

class QueryResponse(BaseModel):
    answer: str  # คำตอบที่มีโครงสร้าง (Executive Summary, Key findings, Evidence, Caution, Recommended next step, Sources)
    sources: List[SourceChunkInfo]
    confidence: float
    query_log_id: int

class FeedbackRequest(BaseModel):
    feedback: str  # "positive" (like) หรือ "negative" (dislike)

# --- Admin Review Schemas ---
class DocumentReviewAction(BaseModel):
    action: str  # "approve", "reject"
    metadata: Optional[DocumentUpdate] = None

# --- Query Log Schemas ---
class QueryLogResponse(BaseModel):
    id: int
    user_id: str
    question: str
    answer: str
    sources: Optional[List[Dict[str, Any]]] = None
    confidence: float
    feedback: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
