# MILESTONE 1 IMPLEMENTATION PLAN

# Knowledge Oracle MVP

## Goal
Build the first product that lets users ask organizational knowledge questions and receive grounded answers with citations.

## In Scope
- Upload PDF/DOCX/TXT/MD
- Extract text
- Add metadata
- Chunk document
- Create embeddings
- Semantic search
- RAG response
- Citation display
- Admin review
- Query log

## Out of Scope
- Patient-level data
- Full Knowledge Graph
- Executive Twin
- Forecast Engine
- Workflow automation

## Modules
1. Knowledge Upload
2. Knowledge Catalog
3. Ask Oracle
4. Citation Viewer
5. Admin Review
6. Query Log

## Agents
1. Knowledge Ingestion Agent
2. Document Classification Agent
3. Metadata Agent
4. Chunking Agent
5. Embedding Agent
6. Retrieval Agent
7. Reranking Agent
8. Answer Generation Agent
9. Citation Agent
10. Feedback Learning Agent

## Development Plan
Week 1: Foundation
- Repository setup
- FastAPI backend
- React frontend
- Database schema
- File upload

Week 2: Document Processing
- Parse PDF/DOCX/TXT/MD
- Extract text
- Store raw text
- Chunk text

Week 3: Vector Search
- Embedding generation
- Vector store
- Search API
- Search UI

Week 4: RAG Answer
- Retrieval pipeline
- Answer generation
- Citation output
- Source viewer

Week 5: Admin + Logs
- Classification
- Metadata editing
- Admin review
- Query log
- Feedback

Week 6: Demo Readiness
- Upload 100 demo documents
- Prepare 20 demo questions
- Tune prompts
- Record demo

## Demo Dataset
Start with 5 domains:
1. PM2.5
2. TB
3. NCD
4. Disaster/Flood
5. Digital Health

Minimum: 20 files per domain.

## Prompt Template
System behavior:
- Answer only from provided context.
- If evidence is insufficient, say so.
- Always cite sources.
- Distinguish fact from interpretation.
- Use concise executive language.

Answer format:
- Summary
- Key findings
- Evidence
- Caution
- Recommended next step
- Sources

## Success Criteria
1. Upload documents works.
2. Text extraction works.
3. Search works.
4. Thai question answering works.
5. Citation works.
6. Admin review works.
7. Query log works.
8. Demo works with 20 questions.
