from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from backend.app.core.config import settings
from backend.app.memory.contracts import (
    GraphEdge,
    GraphNode,
    GraphSnapshot,
    MemoryNote,
    MemoryScope,
)


_WIKI_LINK = re.compile(r"\[\[([^\]|#]+)(?:[|#][^\]]*)?\]\]")
_SAFE_FOLDER = re.compile(r"[^a-zA-Z0-9._-]+")


class PersonalGraphStore:
    """Obsidian-compatible Markdown graph scoped to one staff member."""

    def __init__(self, root: str | Path | None = None) -> None:
        base = Path(root) if root is not None else Path(settings.STORAGE_DIR)
        self.root = base / "personal_memory"

    def vault_dir(self, person_id: str) -> Path:
        self._safe_id(person_id)
        return self.root / person_id / "vault"

    def write_note(self, note: MemoryNote) -> Path:
        if note.memory_scope not in {MemoryScope.PERSONAL, MemoryScope.ROLE}:
            raise ValueError("personal graph accepts only personal or role notes")

        folder = self.vault_dir(note.person_id) / self._folder(note.note_type)
        folder.mkdir(parents=True, exist_ok=True)
        path = folder / f"{note.note_id}.md"

        stored_version = self._stored_version(path)
        if stored_version is not None and note.version < stored_version:
            raise ValueError("cannot overwrite a newer memory note version")

        props = note.model_dump(mode="json")
        props["links"] = [f"[[{value}]]" for value in note.links]
        props["source_refs"] = [f"[[{value}]]" for value in note.source_refs]
        markdown = self._render(props, note)

        temporary = path.with_suffix(".md.tmp")
        temporary.write_text(markdown, encoding="utf-8")
        temporary.replace(path)
        return path

    def find_note(self, person_id: str, note_id: str) -> Path | None:
        self._safe_id(note_id)
        matches = list(self.vault_dir(person_id).glob(f"*/{note_id}.md"))
        if len(matches) > 1:
            raise RuntimeError(f"duplicate note id: {note_id}")
        return matches[0] if matches else None

    def read_raw(self, person_id: str, note_id: str) -> str:
        path = self.find_note(person_id, note_id)
        if path is None:
            raise FileNotFoundError(note_id)
        return path.read_text(encoding="utf-8")

    def build_graph(self, person_id: str) -> GraphSnapshot:
        vault = self.vault_dir(person_id)
        nodes: dict[str, GraphNode] = {}
        records: list[tuple[Path, dict[str, Any], str]] = []

        for path in sorted(vault.glob("*/*.md")) if vault.exists() else []:
            props, body = self._parse(path.read_text(encoding="utf-8"))
            note_id = str(props.get("note_id") or path.stem)
            nodes[note_id] = GraphNode(
                id=note_id,
                title=str(props.get("title") or note_id),
                note_type=str(props.get("note_type") or path.parent.name),
                path=str(path.relative_to(vault)),
                exists=True,
            )
            records.append((path, props, body))

        edges: list[GraphEdge] = []
        seen: set[tuple[str, str]] = set()
        for path, props, body in records:
            source = str(props.get("note_id") or path.stem)
            for target in self._links(props, body):
                key = (source, target)
                if source == target or key in seen:
                    continue
                seen.add(key)
                edges.append(GraphEdge(source=source, target=target))
                nodes.setdefault(
                    target,
                    GraphNode(
                        id=target,
                        title=target,
                        note_type="unresolved",
                        path="",
                        exists=False,
                    ),
                )

        return GraphSnapshot(
            person_id=person_id,
            nodes=sorted(nodes.values(), key=lambda item: item.id),
            edges=sorted(edges, key=lambda item: (item.source, item.target)),
        )

    @staticmethod
    def _render(props: dict[str, Any], note: MemoryNote) -> str:
        lines = [
            "---",
            json.dumps(props, ensure_ascii=False, indent=2),
            "---",
            f"# {note.title}",
            "",
            note.content.strip(),
        ]
        if note.links:
            lines += ["", "## Links", ""] + [f"- [[{x}]]" for x in note.links]
        if note.source_refs:
            lines += ["", "## Sources", ""] + [
                f"- [[{x}]]" for x in note.source_refs
            ]
        return "\n".join(lines).rstrip() + "\n"

    @staticmethod
    def _parse(raw: str) -> tuple[dict[str, Any], str]:
        if not raw.startswith("---\n"):
            return {}, raw
        end = raw.find("\n---\n", 4)
        if end < 0:
            return {}, raw
        try:
            props = json.loads(raw[4:end])
            return props if isinstance(props, dict) else {}, raw[end + 5 :]
        except json.JSONDecodeError:
            return {}, raw[end + 5 :]

    @staticmethod
    def _links(props: dict[str, Any], body: str) -> list[str]:
        values = list(props.get("links") or []) + list(props.get("source_refs") or [])
        values.append(body)
        return list(dict.fromkeys(
            match.strip()
            for value in values
            for match in _WIKI_LINK.findall(str(value))
            if match.strip()
        ))

    @staticmethod
    def _folder(value: str) -> str:
        return _SAFE_FOLDER.sub("-", value.lower()).strip("-._") or "notes"

    @staticmethod
    def _safe_id(value: str) -> None:
        if not value or value in {".", ".."} or "/" in value or "\\" in value:
            raise ValueError(f"unsafe identifier: {value}")

    @classmethod
    def _stored_version(cls, path: Path) -> int | None:
        if not path.exists():
            return None
        props, _ = cls._parse(path.read_text(encoding="utf-8"))
        version = props.get("version")
        return version if isinstance(version, int) else None
