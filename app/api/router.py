from fastapi import APIRouter
from app.api.v1.rag_api import router as rag_router
from app.api.v1.vector_api import router as vector_router

api_router = APIRouter(prefix="/v1")
api_router.include_router(rag_router, tags=["rag"], prefix="/rag")
api_router.include_router(vector_router, tags=["vector"], prefix="/vector")