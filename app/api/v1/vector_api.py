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


@router.post("/similarity_search/{text}")
@inject
async def similarity_search(
        request: SimilaritySearch,
        vector_service: VectorService = Depends(Provide[Container.vector_service])
):
    try:
        return vector_service.similarity_search(request.workspace_id, request.input)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


# Read - 모든 벡터 조회
@router.get("/")
@inject
async def transform_to_vectors(
        vector_service: VectorService = Depends(Provide[Container.vector_service])
):
    try:
        return vector_service.transform_to_vectors()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))




# Read - 특정 ID의 벡터 조회
# @router.get("/vector/{vector_id}", response_model=Vector)
# @inject
# async def read_vector(
#         vector_id: uuid.uuid4(),
#         vector_service: VectorService = Depends(Provide[Container.vector_service])
# ):
#     vector_service.get_vector(vector_id)

    # raise HTTPException(status_code=404, detail="Vector not found")

# Update - 특정 ID의 벡터 업데이트
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