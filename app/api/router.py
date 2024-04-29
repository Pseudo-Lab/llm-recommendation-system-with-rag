from fastapi import APIRouter
from app.api.v1.rag_api import router as rag_router
from app.api.v1.vector_api import router as vector_router
from app.api.v1.generate_api import router as generate_router
# from app.api.v1.model_api import router as model_router
# from app.api.v1.test_api import router as test_router

api_router = APIRouter(prefix="/v1")
api_router.include_router(rag_router, tags=["rag"], prefix="/rag")
api_router.include_router(vector_router, tags=["vector"], prefix="/vector")
api_router.include_router(generate_router, tags=["generate"], prefix="/generate")
# api_router.include_router(model_router, tags=["model"], prefix="/model")
# api_router.include_router(test_router, tags=["rag_test"], prefix="/rag_test")