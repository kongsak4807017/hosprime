from fastapi import APIRouter, Depends

from backend.app.api.endpoints import (
    admin,
    auth,
    documents,
    graph,
    hitl,
    meetings,
    oracle,
    twins,
    workflows,
)
from backend.app.auth import check_role, get_current_user


api_router = APIRouter()

# Public authentication endpoints only.
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

# Milestone 1: Knowledge Oracle — authenticated organizational users.
api_router.include_router(
    documents.router,
    prefix="/documents",
    tags=["documents"],
    dependencies=[Depends(get_current_user)],
)
api_router.include_router(
    oracle.router,
    prefix="/oracle",
    tags=["oracle"],
    dependencies=[Depends(get_current_user)],
)

# Knowledge administration — restricted to governed reviewers.
api_router.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(check_role(["admin", "knowledge_admin"]))],
)

# Milestone 2: Organization Memory.
api_router.include_router(
    meetings.router,
    prefix="/meetings",
    tags=["meetings"],
    dependencies=[Depends(get_current_user)],
)

# Milestone 3: Twin Runtime.
api_router.include_router(
    twins.router,
    prefix="/twins",
    tags=["twins"],
    dependencies=[Depends(get_current_user)],
)

# Graph intelligence is readable only by authenticated users.
api_router.include_router(
    graph.router,
    prefix="/graph",
    tags=["graph"],
    dependencies=[Depends(get_current_user)],
)

# Backoffice execution and HITL approval are privileged operations.
api_router.include_router(
    workflows.router,
    prefix="/workflows",
    tags=["workflows"],
    dependencies=[Depends(check_role(["admin", "twin_admin"]))],
)
api_router.include_router(
    hitl.router,
    prefix="/v2/hitl",
    tags=["hitl"],
    dependencies=[Depends(check_role(["admin", "twin_admin"]))],
)
