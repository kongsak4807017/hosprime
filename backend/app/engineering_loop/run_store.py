from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from backend.app.core.config import settings
from backend.app.engineering_loop.contracts import LoopRunManifest, LoopStage


_STAGE_FILES = {
    LoopStage.CAPTURED: "00-task.md",
    LoopStage.BASELINED: "01-baseline.md",
    LoopStage.RESEARCHING: "02-research.md",
    LoopStage.HYPOTHESIS_READY: "03-hypothesis.md",
    LoopStage.PLANNED: "04-plan.md",
    LoopStage.BUILDING: "05-implementation.md",
    LoopStage.TESTING: "06-tests.md",
    LoopStage.EVALUATING: "07-evaluation.md",
    LoopStage.REVIEWING: "08-review.md",
    LoopStage.DECIDED: "09-decision.md",
    LoopStage.RELEASED: "10-observation.md",
    LoopStage.OBSERVING: "10-observation.md",
    LoopStage.LEARNED: "11-learning.md",
}

_SEQUENCE = [
    LoopStage.CAPTURED,
    LoopStage.BASELINED,
    LoopStage.RESEARCHING,
    LoopStage.HYPOTHESIS_READY,
    LoopStage.PLANNED,
    LoopStage.BUILDING,
    LoopStage.TESTING,
    LoopStage.EVALUATING,
    LoopStage.REVIEWING,
    LoopStage.DECIDED,
    LoopStage.RELEASED,
    LoopStage.OBSERVING,
    LoopStage.LEARNED,
    LoopStage.CLOSED,
]

_TERMINAL = {
    LoopStage.CLOSED,
    LoopStage.REJECTED_HYPOTHESIS,
    LoopStage.STOPPED_RISK,
    LoopStage.DEFERRED_DEPENDENCY,
    LoopStage.NO_CHANGE_REQUIRED,
}


class LoopRunStore:
    def __init__(self, root: str | Path | None = None) -> None:
        base = Path(root) if root is not None else Path(settings.STORAGE_DIR)
        self.root = base / "engineering_runs"

    def create_run(
        self,
        *,
        task: str,
        objective: str,
        owner: str,
        target_metrics: list[str] | None = None,
        linked_issues: list[str] | None = None,
    ) -> Path:
        now = datetime.now(timezone.utc)
        run_id = f"{now:%Y%m%d}-{self._slug(task)[:40]}-{uuid4().hex[:8]}"
        run_dir = self.root / now.strftime("%Y-%m-%d") / run_id
        run_dir.mkdir(parents=True, exist_ok=False)

        manifest = LoopRunManifest(
            run_id=run_id,
            task=task,
            objective=objective,
            owner=owner,
            target_metrics=target_metrics or [],
            linked_issues=linked_issues or [],
        )
        self._write_manifest(run_dir, manifest)
        for stage, filename in _STAGE_FILES.items():
            path = run_dir / filename
            if not path.exists():
                path.write_text(self._template(stage, manifest), encoding="utf-8")
        return run_dir

    def load(self, run_dir: str | Path) -> LoopRunManifest:
        path = Path(run_dir) / "manifest.json"
        return LoopRunManifest.model_validate_json(path.read_text(encoding="utf-8"))

    def advance(
        self,
        run_dir: str | Path,
        target_stage: LoopStage,
        *,
        evidence_file: str | None = None,
        decision: str | None = None,
        approved_by: str | None = None,
    ) -> LoopRunManifest:
        directory = Path(run_dir)
        manifest = self.load(directory)
        self._validate_transition(manifest.stage, target_stage)

        required = evidence_file or _STAGE_FILES.get(target_stage)
        if required:
            path = directory / required
            if not path.exists() or not path.read_text(encoding="utf-8").strip():
                raise ValueError(f"missing evidence for stage {target_stage}: {required}")

        manifest.stage = target_stage
        manifest.updated_at = datetime.now(timezone.utc)
        if decision is not None:
            manifest.decision = decision
        if approved_by is not None:
            manifest.approved_by = approved_by
        if target_stage in _TERMINAL:
            manifest.closed_at = manifest.updated_at
        self._write_manifest(directory, manifest)
        return manifest

    def add_reference(
        self,
        run_dir: str | Path,
        field_name: str,
        value: str,
    ) -> LoopRunManifest:
        allowed = {
            "source_refs",
            "commits",
            "pull_requests",
            "test_artifacts",
            "memory_objects",
            "linked_requirements",
            "affected_components",
        }
        if field_name not in allowed:
            raise ValueError(f"unsupported manifest field: {field_name}")
        manifest = self.load(run_dir)
        values = getattr(manifest, field_name)
        if value not in values:
            values.append(value)
        manifest.updated_at = datetime.now(timezone.utc)
        self._write_manifest(Path(run_dir), manifest)
        return manifest

    @staticmethod
    def _validate_transition(current: LoopStage, target: LoopStage) -> None:
        if current in _TERMINAL:
            raise ValueError(f"run is terminal: {current}")
        if target in _TERMINAL:
            return
        current_index = _SEQUENCE.index(current)
        target_index = _SEQUENCE.index(target)
        if target_index != current_index + 1:
            raise ValueError(f"invalid loop transition: {current} -> {target}")

    @staticmethod
    def _write_manifest(directory: Path, manifest: LoopRunManifest) -> None:
        path = directory / "manifest.json"
        temporary = path.with_suffix(".json.tmp")
        temporary.write_text(
            json.dumps(manifest.model_dump(mode="json"), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        temporary.replace(path)

    @staticmethod
    def _slug(value: str) -> str:
        slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
        return slug or "task"

    @staticmethod
    def _template(stage: LoopStage, manifest: LoopRunManifest) -> str:
        title = stage.value.replace("_", " ").title()
        return (
            f"# {title}\n\n"
            f"- Run ID: `{manifest.run_id}`\n"
            f"- Task: {manifest.task}\n"
            f"- Objective: {manifest.objective}\n\n"
            "## Evidence\n\n"
            "Record facts, source references, results, limitations and decisions.\n"
        )
