# FIRST VIBE CODING PROMPT FOR HOSPRIME

You are an elite AI product engineering team composed of:
- Enterprise Architect
- Senior Full-stack Engineer
- AI Agent Architect
- Data Platform Architect
- Knowledge Graph Architect
- UX Designer
- DevSecOps Engineer
- Public Health Digital Transformation Consultant

Your mission is to build the first working product of **HosPrime: Health Organization Operating System**, starting with **Milestone 1: Knowledge Oracle MVP**.

## 1. Product Vision
HosPrime is not a normal HIS, dashboard, BI system, RAG chatbot, or document search tool. HosPrime is a **Health Organization Operating System** that preserves and amplifies the intelligence of public health organizations.

Ultimate goal:
- Knowledge Oracle
- Meeting Memory
- Executive Twin
- AI Backoffice Workforce
- Provincial Health Brain

The first product must prove this core value:

> Organizational knowledge that used to be scattered, forgotten, and hard to retrieve can now be asked, cited, governed, and reused immediately.

## 2. Build Milestone 1 Only
Do not build the full platform yet. Build the first usable MVP:

# Knowledge Oracle MVP

The system must allow users to:
1. Upload organizational documents.
2. Extract text from PDF/DOCX/TXT/MD initially.
3. Add or infer metadata.
4. Chunk documents.
5. Create embeddings.
6. Search documents semantically in Thai and English.
7. Ask questions.
8. Generate answers only from retrieved evidence.
9. Show citations and source document references.
10. Maintain query logs and basic admin review.

## 3. Key Demo Experience
The executive demo must support questions such as:

- “PM2.5 ปีที่แล้วจังหวัดทำอะไรบ้าง”
- “TB active case finding มีแนวทางอะไร”
- “NCD remission มีเอกสารหรือโครงการอะไรแล้ว”
- “น้ำท่วมครั้งก่อนเรามีมาตรการอะไร”
- “Digital Health platform ควรเริ่มจากอะไร”

The answer must include:
- Executive summary
- Key findings
- Evidence
- Caution / limitation
- Recommended next step
- Sources / citations

## 4. Mandatory AI Behavior Rule
No evidence → no answer.

The AI must never fabricate information. If retrieved evidence is weak, answer:

> Evidence is insufficient from the current organizational knowledge base.

Every answer must include citations from the indexed document chunks.

## 5. Required MVP Modules

### 5.1 Knowledge Upload
- File upload
- Metadata entry
- Processing status
- Document confidentiality level

### 5.2 Knowledge Catalog
- Document list
- Search / filter
- Status: processed / pending review / failed

### 5.3 Ask Oracle
- Question box
- Suggested questions
- Answer panel
- Evidence panel
- Source document list
- Confidence indicator

### 5.4 Admin Review
- Pending documents
- Low-confidence classification
- Edit metadata
- Approve / reject document

### 5.5 Query Log
- User question
- Generated answer
- Retrieved sources
- Confidence
- Feedback

## 6. Recommended Tech Stack
Use a practical local-first stack:

Frontend:
- React
- TypeScript
- TailwindCSS
- shadcn/ui or clean custom components

Backend:
- FastAPI
- Python
- SQLAlchemy
- Pydantic

Database:
- PostgreSQL if available
- SQLite acceptable for first local MVP

Vector Search:
- pgvector if PostgreSQL is used
- FAISS or Chroma acceptable for local MVP

File storage:
- local storage for MVP
- design so it can migrate to MinIO later

AI/LLM:
- Create provider abstraction
- Support OpenAI-compatible API
- Support local/Ollama-compatible mode later

Document parsing:
- PDF, DOCX, TXT, MD

## 7. Suggested Repository Structure

hosprime-knowledge-oracle/
  backend/
    app/
      main.py
      api/
      agents/
      services/
      db/
      schemas/
      core/
  frontend/
    src/
      pages/
      components/
      lib/
  storage/
    documents/
    indexes/
  docs/
  docker-compose.yml
  README.md

## 8. Core Data Models

### Document
- id
- title
- document_type
- department
- program
- year
- owner
- confidentiality_level
- file_path
- status
- created_at
- updated_at

### DocumentChunk
- id
- document_id
- chunk_text
- page_number
- section_title
- embedding_id
- token_count

### QueryLog
- id
- user_id
- question
- answer
- sources
- confidence
- feedback
- created_at

### AgentLog
- id
- agent_id
- task_type
- input
- output
- status
- created_at

## 9. Required Agents for MVP
Implement these as service classes first, not autonomous agents yet:

1. KnowledgeIngestionAgent
2. DocumentClassificationAgent
3. MetadataAgent
4. ChunkingAgent
5. EmbeddingAgent
6. RetrievalAgent
7. RerankingAgent
8. AnswerGenerationAgent
9. CitationAgent
10. FeedbackLearningAgent

## 10. UI Design Principle
The UI must feel executive-grade, clean, calm, and trustworthy.

Avoid clutter. Avoid looking like a developer tool.

Suggested navigation:
- Home
- Ask Oracle
- Upload Knowledge
- Knowledge Catalog
- Admin Review
- Query Logs

## 11. MVP Acceptance Criteria
The first working version is accepted when:
1. User can upload documents.
2. System extracts text.
3. System chunks and indexes content.
4. User can ask Thai questions.
5. System answers from retrieved evidence only.
6. System displays citations.
7. User can open source document reference.
8. Admin can review metadata.
9. Query logs are stored.
10. Demo works with at least 20 prepared questions.

## 12. Development Instruction
Build incrementally. First create a working skeleton, then add features.

Recommended implementation order:
1. Backend skeleton
2. Database models
3. File upload
4. Text extraction
5. Chunking
6. Embedding and search
7. RAG answer generation
8. Citation panel
9. Frontend pages
10. Admin review
11. Demo dataset and demo script

## 13. Non-Negotiable Rules
- No hallucinated answers.
- Citation required.
- Keep all AI access through services, not scattered across frontend.
- Separate document metadata from chunks.
- Separate raw file storage from vector index.
- Keep logs for all AI operations.
- Build local-first, but design for production migration.
- Do not connect to patient-level data in Milestone 1.
- Do not implement clinical decision support in Milestone 1.
- Do not build full Executive Twin yet.

## 14. Final Output Expected From Coding Agent
Produce:
1. Working codebase.
2. README with setup instructions.
3. Demo data folder.
4. Demo question list.
5. Architecture diagram in markdown.
6. API documentation.
7. Known limitations.
8. Next milestone notes.

Start now by creating the repository structure and implementing the first vertical slice:

Upload document → extract text → chunk → search → answer with citation.
