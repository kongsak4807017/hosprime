from pathlib import Path
from typing import List
from uuid import uuid4

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from backend.app.agents.meeting_memory_agent import MeetingMemoryAgent
from backend.app.auth import get_current_user
from backend.app.core.config import settings
from backend.app.db.models import ActionItem, Meeting, User as DBUser
from backend.app.db.session import get_db
from backend.app.services.ai_gateway import AIGateway
from backend.app.services.document_parser import DocumentParser
from backend.app.services.gemini_service import AIProviderUnavailable
from backend.app.services.speech_to_text import SpeechToTextUnavailable

router = APIRouter()

AUDIO_EXTENSIONS = {".wav", ".mp3", ".m4a", ".mp4", ".webm"}
DOCUMENT_EXTENSIONS = {".pdf", ".docx", ".txt", ".md"}


class MeetingAskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=12000)


async def _save_with_limit(file: UploadFile, directory: Path, allowed: set[str]) -> Path:
    original_name = Path(file.filename or "upload").name
    extension = Path(original_name).suffix.lower()
    if extension not in allowed:
        raise HTTPException(status_code=400, detail="Unsupported meeting file format.")

    destination = directory / f"{uuid4().hex}{extension}"
    directory.mkdir(parents=True, exist_ok=True)
    total = 0
    try:
        with destination.open("wb") as output:
            while chunk := await file.read(1024 * 1024):
                total += len(chunk)
                if total > settings.MAX_UPLOAD_BYTES:
                    raise HTTPException(
                        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                        detail="Meeting file exceeds the configured upload limit.",
                    )
                output.write(chunk)
        return destination
    except Exception:
        destination.unlink(missing_ok=True)
        raise
    finally:
        await file.close()


@router.post("/upload-audio")
async def upload_meeting_audio(
    file: UploadFile = File(...),
    title: str = Form(..., min_length=1, max_length=255),
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user),
):
    destination = await _save_with_limit(
        file,
        Path(settings.STORAGE_DIR) / "meetings",
        AUDIO_EXTENSIONS,
    )
    try:
        result = MeetingMemoryAgent.process_meeting_recording(
            db,
            title,
            str(destination),
        )
        return {
            "status": "draft_pending_human_review",
            "message": "Meeting memory was extracted as a draft for human review.",
            "data": result,
        }
    except (SpeechToTextUnavailable, AIProviderUnavailable) as exc:
        destination.unlink(missing_ok=True)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        destination.unlink(missing_ok=True)
        raise HTTPException(
            status_code=500,
            detail="Meeting processing failed. No meeting memory was created.",
        ) from exc


@router.get("/list")
def list_meetings(
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user),
):
    meetings = db.query(Meeting).order_by(Meeting.id.desc()).all()
    result = []
    for meeting in meetings:
        action_items = (
            db.query(ActionItem)
            .filter(ActionItem.meeting_id == meeting.id)
            .all()
        )
        result.append(
            {
                "id": meeting.id,
                "title": meeting.title,
                "date": meeting.date,
                "summary": meeting.summary,
                "action_items": [
                    {
                        "task": item.task,
                        "assignee": item.assignee,
                        "due_date": item.due_date,
                        "status": item.status,
                    }
                    for item in action_items
                ],
            }
        )
    return result


@router.post("/{meeting_id}/upload-document")
async def upload_meeting_document(
    meeting_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user),
):
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")

    original_name = Path(file.filename or "document").name[:255]
    destination = await _save_with_limit(
        file,
        Path(settings.STORAGE_DIR) / "meetings",
        DOCUMENT_EXTENSIONS,
    )
    try:
        pages = DocumentParser.parse_document(str(destination))
        parsed_text = "\n".join(
            str(page.get("text", "")) for page in pages if page.get("text")
        ).strip()
        if not parsed_text:
            raise ValueError("No usable text was extracted from the document.")

        meeting.transcript = (
            (meeting.transcript or "")
            + f"\n\n[Meeting attachment: {original_name}]\n"
            + parsed_text
        )
        db.commit()
        return {
            "status": "success",
            "message": "Meeting attachment text was added.",
            "filename": original_name,
        }
    except Exception as exc:
        db.rollback()
        destination.unlink(missing_ok=True)
        raise HTTPException(
            status_code=500,
            detail="Meeting document extraction failed.",
        ) from exc


@router.post("/{meeting_id}/ask")
def ask_meeting_oracle(
    meeting_id: int,
    request: MeetingAskRequest,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user),
):
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")

    context = (
        f"Meeting title: {meeting.title}\n"
        f"Meeting date: {meeting.date or 'not recorded'}\n\n"
        f"Reviewed summary or draft summary:\n{meeting.summary or 'none'}\n\n"
        f"Transcript and attachments:\n{meeting.transcript or 'none'}"
    )
    system_instruction = (
        "Answer only from the supplied meeting context. "
        "Do not use outside knowledge. Cite the relevant meeting section in plain text. "
        "When the context does not contain the answer, state that the meeting record does not contain it."
    )
    try:
        response = AIGateway.generate_response(
            db=db,
            prompt=f"Context:\n{context}\n\nQuestion: {request.question}",
            system_instruction=system_instruction,
            model_name="gemini-2.5-flash",
            agent_id="MeetingOracleAgent",
        )
        return {"response": response, "status": "success"}
    except AIProviderUnavailable as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc
