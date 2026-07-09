# M0.3 Obsidian Graph Fixture Validation Checklist

Date: 2026-07-10

Linked issue: #156

## Purpose

This checklist is a lightweight repository-local validation artifact for the next TEST stage. It does not claim that Obsidian was executed, that graph rendering was observed, that CI passed, that RAG is active, that sources are approved, or that Organizational Memory was promoted.

## Fixture root

```text
storage/personal_memory/example-person/vault/
```

## Expected fixture notes

```text
meetings/m0-3-demo-meeting.md
decisions/m0-3-demo-decision.md
tasks/m0-3-demo-task.md
sources/m0-3-demo-source-reference.md
lessons/m0-3-demo-lesson.md
```

## Required visible Wikilinks for the next TEST stage

```text
MEETING_NOTE links to [[m0-3-demo-decision]]
DECISION_NOTE links to [[m0-3-demo-meeting]]
DECISION_NOTE links to [[m0-3-demo-task]]
DECISION_NOTE links to [[m0-3-demo-source-reference]]
TASK_NOTE links to [[m0-3-demo-decision]]
TASK_NOTE links to [[m0-3-demo-lesson]]
LESSON_NOTE links to [[m0-3-demo-task]]
LESSON_NOTE links to [[m0-3-demo-decision]]
SOURCE_NOTE links to [[m0-3-demo-decision]]
```

## Required boundary strings for the next TEST stage

```text
GRAPH_LINKS_ARE_NAVIGATION_NOT_PROOF = true
SOURCE_APPROVAL_CLAIMED = false
RAG_ACTIVATION_CLAIMED = false
ORGANIZATIONAL_MEMORY_PROMOTION_CLAIMED = false
REAL_WORLD_EXECUTION_CLAIMED = false
REAL_PERSONAL_CONTENT_USED = false
PATIENT_OR_SENSITIVE_CONTENT_USED = false
```

## Non-claims

```text
OBSIDIAN_RUNTIME_EXECUTED = false
OBSIDIAN_GRAPH_RENDERING_OBSERVED = false
CI_PASS_CLAIMED = false
USER_ACCEPTANCE_CLAIMED = false
REAL_WORLD_EXECUTION_CLAIMED = false
```
