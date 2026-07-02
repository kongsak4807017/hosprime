from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum

from pydantic import BaseModel, Field


class LoopStage(str, Enum):
    CAPTURED = "captured"
    BASELINED = "baselined"
    RESEARCHING = "researching"
    HYPOTHESIS_READY = "hypothesis_ready"
    PLANNED = "planned"
    BUILDING = "building"
    TESTING = "testing"
    EVALUATING = "evaluating"
    REVIEWING = "reviewing"
    DECIDED = "decided"
    RELEASED = "released"
    OBSERVING = "observing"
    LEARNED = "learned"
    CLOSED = "closed"
    REJECTED_HYPOTHESIS = "rejected_hypothesis"
    STOPPED_RISK = "stopped_risk"
    DEFERRED_DEPENDENCY = "deferred_dependency"
    NO_CHANGE_REQUIRED = "no_change_required"


class LoopRunManifest(BaseModel):
    run_id: str
    task: str = Field(min_length=1, max_length=2000)
    objective: str = Field(min_length=1, max_length=5000)
    owner: str = Field(min_length=1, max_length=255)
    stage: LoopStage = LoopStage.CAPTURED
    target_metrics: list[str] = Field(default_factory=list)
    linked_issues: list[str] = Field(default_factory=list)
    linked_requirements: list[str] = Field(default_factory=list)
    affected_components: list[str] = Field(default_factory=list)
    source_refs: list[str] = Field(default_factory=list)
    commits: list[str] = Field(default_factory=list)
    pull_requests: list[str] = Field(default_factory=list)
    test_artifacts: list[str] = Field(default_factory=list)
    memory_objects: list[str] = Field(default_factory=list)
    decision: str | None = None
    approved_by: str | None = None
    started_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    closed_at: datetime | None = None
