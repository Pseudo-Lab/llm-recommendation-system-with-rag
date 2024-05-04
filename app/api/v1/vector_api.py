import uuid
from fastapi import HTTPException
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from container.containers import Container
from model.schema.vector_schema import Vector, SimilaritySearch
from service.vector_service import VectorService

router = APIRouter()

@router.post("/{text}")
@inject
async def create_vector(
        # vector: Vector,
        text: str,
        vector_service: VectorService = Depends(Provide[Container.vector_service])
):
    return vector_service.create_vector(text)

@router.get(
    path="/vector_cnt/{workspace_id}",
    description="벡터 디비에 저장된 개수 확인"
)
@inject
async def vector_cnt(
        workspace_id: uuid.UUID,
        vector_service: VectorService = Depends(Provide[Container.vector_service])
):
    try:
        return vector_service.vector_cnt(workspace_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post(
    path="/similarity_search/",
    description="유사도 기반 검색"
)
@inject
async def similarity_search(
        request: SimilaritySearch,
        vector_service: VectorService = Depends(Provide[Container.vector_service])
):
    try:
        return vector_service.similarity_search(request.workspace_id, request.input, request.top_k)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post(
    path="/similarity_search/self_query"
)
@inject
async def gen_response_with_self_query(
        request: SimilaritySearch,
        vector_service: VectorService = Depends(Provide[Container.vector_service])
):
    try:
        return await vector_service.similarity_search_with_self_query(request.workspace_id, request.input)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


# @router.get("/")
# @inject
# async def transform_to_vectors(
#         vector_service: VectorService = Depends(Provide[Container.vector_service])
# ):
#     try:
#         return vector_service.transform_to_vectors()
#     except Exception as e:
#         raise HTTPException(status_code=404, detail=str(e))

@router.put("/vector/{vector_id}", response_model=Vector)
async def update_vector(vector_id: int, vector: Vector):
    pass
    # for v in db:
    #     if v.id == vector_id:
    #         v.values = vector.values
    #         return v
    # raise HTTPException(status_code=404, detail="Vector not found")

# Delete - 특정 ID의 벡터 삭제
@router.delete("/vector/{vector_id}", response_model=Vector)
async def delete_vector(vector_id: int):
    pass
    # for i, vector in enumerate(db):
    #     if vector.id == vector_id:
    #         deleted_vector = db.pop(i)
    #         return deleted_vector
    # raise HTTPException(status_code=404, detail="Vector not found")