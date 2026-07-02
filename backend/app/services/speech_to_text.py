import logging
import os
from typing import Any, Optional

logger = logging.getLogger(__name__)


class SpeechToTextUnavailable(RuntimeError):
    """Raised when an approved speech-to-text engine is unavailable."""


class SpeechToTextService:
    _model: Optional[Any] = None

    @classmethod
    def _get_model(cls):
        """Lazy-load Whisper so unrelated API modules can start without it."""
        if cls._model is not None:
            return cls._model

        try:
            import whisper
        except ImportError as exc:
            raise SpeechToTextUnavailable(
                "Whisper is not installed. Configure an approved transcription provider."
            ) from exc

        logger.info("Loading Whisper 'tiny' model for controlled transcription.")
        try:
            cls._model = whisper.load_model("tiny")
            return cls._model
        except Exception as exc:
            raise SpeechToTextUnavailable(
                "Whisper model could not be loaded."
            ) from exc

    @classmethod
    def transcribe(cls, audio_file_path: str) -> str:
        """Transcribe an existing audio file or fail without inventing content."""
        if not audio_file_path or not os.path.isfile(audio_file_path):
            raise FileNotFoundError("Meeting audio file was not found.")

        try:
            model = cls._get_model()
            result = model.transcribe(audio_file_path, language="th")
            text = str(result.get("text", "")).strip()
            if not text:
                raise SpeechToTextUnavailable(
                    "The transcription provider returned no usable text."
                )
            return text
        except (FileNotFoundError, SpeechToTextUnavailable):
            raise
        except Exception as exc:
            logger.error("Speech-to-text processing failed: %s", exc)
            raise SpeechToTextUnavailable(
                "Speech-to-text processing failed. No transcript was generated."
            ) from exc
