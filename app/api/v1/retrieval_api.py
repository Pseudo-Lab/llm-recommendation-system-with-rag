import os
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, HTTPException, Depends
from container.containers import Container
from model.schema.vector_schema import Search
from service.retrieval_service import RetrievalService

router = APIRouter()

@router.post(
    path="/dense_search/",
    description="유사도 기반 검색"
)
@inject
async def dense_search(
        request: Search,
        retrieval_service: RetrievalService = Depends(Provide[Container.retrieval_service])
):
    try:
        if request.openai_key:
            os.environ["OPENAI_API_KEY"] = request.openai_key
        return await retrieval_service.dense_search(request.workspace_id, request.input, request.top_k, request.score_threshold)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post(
    path="/sparse_search/",
    description="키워드 기반 검색"
)
@inject
async def sparse_search(
        request: Search,
        retrieval_service: RetrievalService = Depends(Provide[Container.retrieval_service])
):
    try:
        if request.openai_key:
            os.environ["OPENAI_API_KEY"] = request.openai_key
        return await retrieval_service.sparse_search(request.workspace_id, request.input, request.top_k, request.score_threshold)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post(
    path="/ensemble_search/",
    description="유사도 기반 + key word 검색"
)
@inject
async def ensemble_search(
        request: Search,
        retrieval_service: RetrievalService = Depends(Provide[Container.retrieval_service])
):
    try:
        if request.openai_key:
            os.environ["OPENAI_API_KEY"] = request.openai_key
        return await retrieval_service.ensemble_search(request.workspace_id, request.input, request.top_k, request.score_threshold)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post(
    path="/self_query/",
    description="셀프 쿼리 기반 검색"

)
@inject
async def similarity_search_with_self_query(
        request: Search,
        retrieval_service: RetrievalService = Depends(Provide[Container.retrieval_service])
):
    try:
        if request.openai_key:
            os.environ["OPENAI_API_KEY"] = request.openai_key

        return await retrieval_service.similarity_search_with_self_query(
            request.workspace_id,
            request.input,
            request.top_k,
            request.score_threshold
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))