# HOSPRIME ARCHITECTURE BLUEPRINT

## High-Level Architecture

User Login / ThaiD / Provider ID / SSO
  ↓
Identity & Role Resolution Layer
  ↓
Personal Workspace
  ↓
Human Digital Twin
  ↓
Role Twin
  ↓
Organization Twin
  ↓
Agent Council
  ↓
Knowledge Graph Oracle
  ↓
Semantic Data Mart
  ↓
Forecast & Scenario Engine
  ↓
Workflow / Tool Execution
  ↓
Organization Memory

## Production Architecture Layers
1. Source Systems Layer
2. Integration Layer
3. Data Platform Layer
4. Semantic Intelligence Layer
5. Knowledge Layer
6. AI Intelligence Layer
7. Agent Orchestration Layer
8. Experience Layer

## Human Platform
The user should not see hundreds of agents. The user should see:
- My Workspace
- My Twin
- My Work
- My Organization
- My AI Council
- Knowledge Oracle
- Forecast Theater

## Backoffice AI Layer
Backoffice AI prepares and governs everything before front-office AI uses it.

Source Systems
  ↓
DataOps Agents
  ↓
Data Quality Agents
  ↓
Data Governance Agents
  ↓
Semantic Data Mart
  ↓
KnowledgeOps Agents
  ↓
Knowledge Graph Oracle
  ↓
TwinOps Agents
  ↓
Person / Role / Organization Twin
  ↓
ForecastOps Agents
  ↓
Scenario & Forecast Engine
  ↓
AgentOps / AIOC
  ↓
Front Office AI Agents
  ↓
Human Users

## Recommended Tech Stack
Frontend:
- React
- TypeScript
- TailwindCSS
- shadcn/ui

Backend:
- FastAPI
- Python
- Microservices later

Data:
- PostgreSQL
- ClickHouse later
- Redis
- MinIO later

Knowledge:
- Neo4j later
- Qdrant or pgvector
- OpenSearch later

AI Runtime:
- OpenAI-compatible API for MVP
- Ollama / vLLM later

Workflow:
- Temporal later

Auth:
- Keycloak later
- Basic login acceptable for local MVP
