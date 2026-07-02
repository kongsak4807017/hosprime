from pathlib import Path
from typing import List, Optional
from uuid import uuid4

from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile, status
from sqlalchemy.orm import Session

from backend.app.agents.agents import KnowledgeIngestionAgent
from backend.app.core.config import settings
from backend.app.db.models import Document, EntityRelation
from backend.app.db.session import get_db
from backend.app.schemas.schemas import DocumentResponse, EntityRelationResponse

router = APIRouter()

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt", ".md"}
ALLOWED_CONFIDENTIALITY = {"Public", "Internal", "Confidential", "Restricted"}


def _clean_title(value: str) -> str:
    cleaned = " ".join(value.replace("\x00", "").split()).strip()
    return cleaned[:255] or "Untitled document"


async def _save_upload_with_limit(file: UploadFile, destination: Path) -> int:
    total = 0
    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        with destination.open("wb") as buffer:
            while chunk := await file.read(1024 * 1024):
                total += len(chunk)
                if total > settings.MAX_UPLOAD_BYTES:
                    raise HTTPException(
                        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                        detail=(
                            "File exceeds the configured upload limit of "
                            f"{settings.MAX_UPLOAD_BYTES} bytes."
                        ),
                    )
                buffer.write(chunk)
        return total
    except Exception:
        destination.unlink(missing_ok=True)
        raise
    finally:
        await file.close()


@router.post(
    "/upload",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_document(
    file: UploadFile = File(...),
    title: Optional[str] = Form(None),
    confidentiality_level: Optional[str] = Form("Internal"),
    db: Session = Depends(get_db),
):
    original_name = Path(file.filename or "document").name
    extension = Path(original_name).suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file format. Use PDF, DOCX, TXT, or MD.",
        )

    confidentiality = confidentiality_level or "Internal"
    if confidentiality not in ALLOWED_CONFIDENTIALITY:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid confidentiality level.",
        )

    document_title = _clean_title(title or Path(original_name).stem)
    destination = Path(settings.DOCUMENT_DIR) / f"{uuid4().hex}{extension}"
    await _save_upload_with_limit(file, destination)

    try:
        return KnowledgeIngestionAgent.ingest(
            db=db,
            file_path=str(destination),
            title=document_title,
            confidentiality_level=confidentiality,
        )
    except Exception as exc:
        destination.unlink(missing_ok=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Document ingestion failed. Review server logs for the request ID.",
        ) from exc


@router.get("/catalog", response_model=List[DocumentResponse])
def get_catalog(
    document_type: Optional[str] = None,
    department: Optional[str] = None,
    program: Optional[str] = None,
    status_value: Optional[str] = Query(default=None, alias="status"),
    db: Session = Depends(get_db),
):
    query = db.query(Document)
    if document_type:
        query = query.filter(Document.document_type == document_type)
    if department:
        query = query.filter(Document.department == department)
    if program:
        query = query.filter(Document.program == program)
    if status_value:
        query = query.filter(Document.status == status_value)
    return query.order_by(Document.created_at.desc()).all()


@router.get("/{doc_id}/relations", response_model=List[EntityRelationResponse])
def get_document_relations(doc_id: int, db: Session = Depends(get_db)):
    return (
        db.query(EntityRelation)
        .filter(EntityRelation.document_id == doc_id)
        .all()
    )


@router.delete("/{doc_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(doc_id: int, db: Session = Depends(get_db)):
    document = db.query(Document).filter(Document.id == doc_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    Path(document.file_path).unlink(missing_ok=True)
    db.delete(document)
    db.commit()
    return None
