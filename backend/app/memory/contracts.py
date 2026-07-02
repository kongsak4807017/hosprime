from __future__ import annotations

import re
from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator


_SAFE_ID = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9._-]{0,127}$")


class MemoryScope(str, Enum):
    PERSONAL = "personal"
    ROLE = "role"
    ORGANIZATIONAL = "organizational"
    RESEARCH = "research"


class ReviewState(str, Enum):
    CAPTURED = "captured"
    DRAFT = "draft"
    REVIEWED = "reviewed"
    PROMOTION_PENDING = "promotion_pending"
    PROMOTED = "promoted"
    EXPIRED = "expired"
    RETRACTED = "retracted"


class Sensitivity(str, Enum):
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"


class MemoryNote(BaseModel):
    note_id: str
    person_id: str
    title: str = Field(min_length=1, max_length=255)
    note_type: str = Field(min_length=1, max_length=64)
    content: str = Field(default="", max_length=100_000)
    links: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    source_refs: list[str] = Field(default_factory=list)
    memory_scope: MemoryScope = MemoryScope.PERSONAL
    review_state: ReviewState = ReviewState.CAPTURED
    sensitivity: Sensitivity = Sensitivity.INTERNAL
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    retention_until: Optional[datetime] = None
    version: int = Field(default=1, ge=1)

    @field_validator("note_id", "person_id")
    @classmethod
    def validate_identifier(cls, value: str) -> str:
        if not _SAFE_ID.fullmatch(value):
            raise ValueError(
                "identifier must contain only letters, numbers, dot, underscore or dash"
            )
        return value

    @field_validator("links", "source_refs")
    @classmethod
    def validate_reference_ids(cls, values: list[str]) -> list[str]:
        cleaned: list[str] = []
        for value in values:
            if not _SAFE_ID.fullmatch(value):
                raise ValueError(f"unsafe reference identifier: {value}")
            if value not in cleaned:
                cleaned.append(value)
        return cleaned

    @field_validator("tags")
    @classmethod
    def clean_tags(cls, values: list[str]) -> list[str]:
        cleaned: list[str] = []
        for value in values:
            tag = value.strip().replace(" ", "-")[:64]
            if tag and tag not in cleaned:
                cleaned.append(tag)
        return cleaned


class PromotionRequest(BaseModel):
    request_id: str
    person_id: str
    source_note_id: str
    target_scope: MemoryScope
    reason: str = Field(min_length=3, max_length=5000)
    requested_by: str = Field(min_length=1, max_length=255)
    evidence_refs: list[str] = Field(default_factory=list)
    private_fields_removed: bool = False
    status: str = "pending_review"
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    @field_validator("request_id", "person_id", "source_note_id")
    @classmethod
    def validate_identifier(cls, value: str) -> str:
        if not _SAFE_ID.fullmatch(value):
            raise ValueError(f"unsafe identifier: {value}")
        return value

    @field_validator("target_scope")
    @classmethod
    def prevent_personal_target(cls, value: MemoryScope) -> MemoryScope:
        if value == MemoryScope.PERSONAL:
            raise ValueError("promotion target must be role, organizational or research")
        return value


class GraphNode(BaseModel):
    id: str
    title: str
    note_type: str
    path: str
    exists: bool = True


class GraphEdge(BaseModel):
    source: str
    target: str
    relation: str = "links_to"


class GraphSnapshot(BaseModel):
    person_id: str
    generated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    nodes: list[GraphNode]
    edges: list[GraphEdge]
