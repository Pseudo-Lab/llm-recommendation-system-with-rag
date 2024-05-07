from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, HTTPException, Depends

from container.containers import Container
from model.schema.vector_schema import Search
from service.retrieval_service import RetrievalService

router = APIRouter()


@router.post(
    path="/similarity_search/",
    description="유사도 기반 검색"
)
@inject
async def similarity_search(
        request: Search,
        retrieval_service: RetrievalService = Depends(Provide[Container.retrieval_service])
):
    try:
        return retrieval_service.similarity_search(request.workspace_id, request.input, request.top_k)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post(
    path="/similarity_search/self_query",
    description="셀프 쿼리 기반 검색"

)
@inject
async def similarity_search_with_self_query(
        request: Search,
        retrieval_service: RetrievalService = Depends(Provide[Container.retrieval_service])
):
    try:
        return await retrieval_service.similarity_search_with_self_query(request.workspace_id, request.input)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))