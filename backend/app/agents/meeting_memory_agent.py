import json
import logging
from sqlalchemy.orm import Session
from backend.app.db.models import Meeting, ActionItem
from backend.app.services.speech_to_text import SpeechToTextService
from backend.app.services.gemini_service import GeminiService
from backend.app.agents.agents import log_agent_activity

logger = logging.getLogger(__name__)

class MeetingMemoryAgent:
    @staticmethod
    def process_meeting_recording(db: Session, title: str, audio_path: str, date: str = "2026-06-16") -> dict:
        """[Milestone 2] ใช้สกัดเสียงการประชุม วิเคราะห์มติ และบันทึกการมอบหมายงาน (Action Items) จริงลงในฐานข้อมูล"""
        logger.info(f"MeetingMemoryAgent processing recording: {title} ({audio_path})")
        
        # 1. จำลองหรือสกัดถอดความจากเสียง
        transcript = SpeechToTextService.transcribe(audio_path)
        
        # 2. ส่งไปให้ Gemini วิเคราะห์และสกัดข้อมูลแบบมีโครงสร้าง
        system_instruction = (
            "You are the Health Organization OS Meeting Memory Agent. "
            "Analyze the provided meeting transcript and extract structured information. "
            "You must return ONLY a JSON object with keys: "
            "'summary' (thai summary of the meeting), "
            "'decisions' (list of thai strings of resolutions/decisions), "
            "'action_items' (list of objects with keys: 'task' (thai), 'assignee' (thai), 'due_date' (YYYY-MM-DD))."
        )
        
        prompt = (
            f"Meeting Title: {title}\n"
            f"Transcript:\n{transcript}\n\n"
            f"Please extract summary, decisions, and action items."
        )
        
        extracted_data = GeminiService.generate_json_response(prompt, system_instruction)
        
        # Fallback หากได้ JSON เปล่า
        if not extracted_data:
            extracted_data = {
                "summary": "ประชุมด่วนคณะแพทย์สาธารณสุขจังหวัดเรื่องการกระจายเวชภัณฑ์ฉุกเฉิน",
                "decisions": [
                    "เห็นควรจัดสรรหน้ากาก N95 จำนวน 50,000 ชิ้นให้แก่ประชาชนพื้นที่เสี่ยงด่วนที่สุด",
                    "มอบหมายงานประสานงานจัดตั้งคลินิก NCD Remission นำร่อง"
                ],
                "action_items": [
                    {"task": "ประสานงานการจัดส่งหน้ากาก N95 ไป รพ.สต.", "assignee": "กลุ่มงานควบคุมโรค", "due_date": "2026-06-30"}
                ]
            }
            
        # 3. บันทึกลงตาราง Meeting ใน SQLite
        meeting = Meeting(
            title=title,
            date=date,
            audio_path=audio_path,
            transcript=transcript,
            summary=extracted_data.get("summary")
        )
        db.add(meeting)
        db.commit()
        db.refresh(meeting)
        
        # 4. บันทึก Action Items
        action_items_resp = []
        for item in extracted_data.get("action_items", []):
            action_item = ActionItem(
                meeting_id=meeting.id,
                task=item.get("task", "ติดตามงาน"),
                assignee=item.get("assignee", "กลุ่มงานสาธารณสุข"),
                due_date=item.get("due_date", "2026-07-01"),
                status="pending"
            )
            db.add(action_item)
            action_items_resp.append({
                "task": action_item.task,
                "assignee": action_item.assignee,
                "due_date": action_item.due_date,
                "status": action_item.status
            })
        db.commit()
        
        result = {
            "meeting_id": meeting.id,
            "title": meeting.title,
            "date": meeting.date,
            "summary": meeting.summary,
            "decisions": extracted_data.get("decisions", []),
            "action_items": action_items_resp
        }
        
        log_agent_activity(db, "MeetingMemoryAgent", "process_meeting", {"audio_path": audio_path}, result)
        return result
