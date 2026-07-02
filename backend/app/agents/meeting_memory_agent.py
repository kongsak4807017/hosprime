import json
import logging
from datetime import date
from typing import Any

from sqlalchemy.orm import Session

from backend.app.agents.agents import log_agent_activity
from backend.app.db.models import ActionItem, Meeting
from backend.app.services.ai_gateway import AIGateway
from backend.app.services.speech_to_text import SpeechToTextService

logger = logging.getLogger(__name__)


class MeetingMemoryAgent:
    @staticmethod
    def _validate_extraction(data: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(data, dict):
            raise ValueError("Meeting extraction must be a JSON object.")

        summary = str(data.get("summary", "")).strip()
        decisions = data.get("decisions", [])
        action_items = data.get("action_items", [])

        if not summary:
            raise ValueError("Meeting extraction has no summary.")
        if not isinstance(decisions, list) or not isinstance(action_items, list):
            raise ValueError("Decisions and action_items must be lists.")

        clean_actions = []
        for item in action_items[:100]:
            if not isinstance(item, dict):
                continue
            task = str(item.get("task", "")).strip()
            assignee = str(item.get("assignee", "")).strip()
            due_date = str(item.get("due_date", "")).strip()
            if not task:
                continue
            clean_actions.append(
                {
                    "task": task[:1000],
                    "assignee": assignee[:255] or "Unassigned",
                    "due_date": due_date[:32] or None,
                }
            )

        clean_decisions = [
            str(item).strip()[:2000]
            for item in decisions[:100]
            if str(item).strip()
        ]
        return {
            "summary": summary[:10000],
            "decisions": clean_decisions,
            "action_items": clean_actions,
        }

    @staticmethod
    def process_meeting_recording(
        db: Session,
        title: str,
        audio_path: str,
        meeting_date: str | None = None,
    ) -> dict:
        """Transcribe and extract draft memory; never invent a meeting record."""
        transcript = SpeechToTextService.transcribe(audio_path)

        system_instruction = (
            "You are the HosPrime Meeting Memory extraction agent. "
            "Extract only information explicitly present in the transcript. "
            "Return JSON with keys summary, decisions and action_items. "
            "Each action item contains task, assignee and due_date. "
            "Use null or an empty string when a value is absent. "
            "Do not infer a decision, owner, date, quantity or deadline."
        )
        prompt = (
            f"Meeting title: {title}\n\n"
            f"Transcript:\n{transcript}\n\n"
            "Extract reviewable organizational memory."
        )

        extracted = AIGateway.generate_json_response(
            db=db,
            prompt=prompt,
            system_instruction=system_instruction,
            model_name="gemini-2.5-flash",
            agent_id="MeetingMemoryAgent",
        )
        validated = MeetingMemoryAgent._validate_extraction(extracted)

        meeting = Meeting(
            title=title.strip()[:255],
            date=meeting_date or date.today().isoformat(),
            audio_path=audio_path,
            transcript=transcript,
            summary=validated["summary"],
        )
        db.add(meeting)
        db.flush()

        action_items_response = []
        for item in validated["action_items"]:
            action_item = ActionItem(
                meeting_id=meeting.id,
                task=item["task"],
                assignee=item["assignee"],
                due_date=item["due_date"],
                status="pending_review",
            )
            db.add(action_item)
            action_items_response.append(item | {"status": "pending_review"})

        db.commit()
        db.refresh(meeting)

        result = {
            "meeting_id": meeting.id,
            "title": meeting.title,
            "date": meeting.date,
            "summary": meeting.summary,
            "decisions": validated["decisions"],
            "action_items": action_items_response,
            "memory_status": "draft_pending_human_review",
        }
        log_agent_activity(
            db,
            "MeetingMemoryAgent",
            "extract_draft_meeting_memory",
            {"audio_path": audio_path},
            result,
        )
        return result
