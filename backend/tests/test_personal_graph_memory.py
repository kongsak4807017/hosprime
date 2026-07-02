from backend.app.memory.contracts import MemoryNote, MemoryScope
from backend.app.memory.personal_graph_store import PersonalGraphStore


def test_writes_obsidian_notes_and_builds_real_graph(tmp_path):
    store = PersonalGraphStore(tmp_path)
    project = MemoryNote(
        note_id="project-tb",
        person_id="staff-001",
        title="TB Active Case Finding",
        note_type="project",
        content="Pilot project context.",
        links=["role-disease-control"],
    )
    role = MemoryNote(
        note_id="role-disease-control",
        person_id="staff-001",
        title="Disease Control Role",
        note_type="role",
        memory_scope=MemoryScope.ROLE,
        content="Reviewed role responsibility.",
    )

    project_path = store.write_note(project)
    store.write_note(role)
    graph = store.build_graph("staff-001")

    assert project_path.exists()
    assert "[[role-disease-control]]" in project_path.read_text(encoding="utf-8")
    assert {node.id for node in graph.nodes} == {
        "project-tb",
        "role-disease-control",
    }
    assert [(edge.source, edge.target) for edge in graph.edges] == [
        ("project-tb", "role-disease-control")
    ]


def test_unresolved_links_remain_visible(tmp_path):
    store = PersonalGraphStore(tmp_path)
    store.write_note(
        MemoryNote(
            note_id="daily-001",
            person_id="staff-001",
            title="Daily note",
            note_type="daily",
            links=["future-project"],
        )
    )

    graph = store.build_graph("staff-001")
    unresolved = next(node for node in graph.nodes if node.id == "future-project")

    assert unresolved.exists is False


def test_rejects_cross_scope_and_unsafe_identifier(tmp_path):
    store = PersonalGraphStore(tmp_path)

    try:
        store.write_note(
            MemoryNote(
                note_id="org-note",
                person_id="staff-001",
                title="Organization note",
                note_type="policy",
                memory_scope=MemoryScope.ORGANIZATIONAL,
            )
        )
    except ValueError as exc:
        assert "personal or role" in str(exc)
    else:
        raise AssertionError("organizational note was accepted into personal vault")

    try:
        store.vault_dir("../other-user")
    except ValueError as exc:
        assert "unsafe identifier" in str(exc)
    else:
        raise AssertionError("unsafe identifier was accepted")
