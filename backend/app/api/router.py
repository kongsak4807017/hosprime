from fastapi import APIRouter
from backend.app.api.endpoints import auth, documents, oracle, admin, meetings, twins, graph, workflows, hitl

api_router = APIRouter()

# Authentication & User Management
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])


# Milestone 1: Knowledge Oracle
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
api_router.include_router(oracle.router, prefix="/oracle", tags=["oracle"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])

# Milestone 2: Meeting Memory
api_router.include_router(meetings.router, prefix="/meetings", tags=["meetings"])

# Milestone 3: Executive Twin
api_router.include_router(twins.router, prefix="/twins", tags=["twins"])

# Milestone 4: Provincial Health Brain (Graph)
api_router.include_router(graph.router, prefix="/graph", tags=["graph"])

# Milestone 5: Backoffice AI Workforce (Workflow)
api_router.include_router(workflows.router, prefix="/workflows", tags=["workflows"])

# Enterprise HITL Gateway
api_router.include_router(hitl.router, prefix="/v2/hitl", tags=["hitl"])
api_router.include_router(hitl.router, prefix="/hitl", tags=["hitl"])
