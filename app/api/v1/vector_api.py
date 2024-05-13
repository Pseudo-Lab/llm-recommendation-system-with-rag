import uuid
from fastapi import HTTPException
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from container.containers import Container
from model.schema.vector_schema import Vector
from vector.vector_store import VectorStoreInterface

router = APIRouter()

@router.post("/{text}")
@inject
async def create_vector(
        # vector: Vector,
        text: str,
        vector_service: VectorStoreInterface = Depends(Provide[Container.vector_store])
):
    return vector_service.create_vector(text)

@router.get(
    path="/cnt/{workspace_id}",
    description="벡터 디비에 저장된 개수 확인"
)
@inject
async def vector_cnt(
        workspace_id: uuid.UUID,
        vector_service: VectorStoreInterface = Depends(Provide[Container.vector_store])
):
    try:
        return vector_service.vector_cnt(workspace_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/")
@inject
async def transform_to_vectors(
        vector_service: VectorStoreInterface = Depends(Provide[Container.vector_store])
):
    try:
        return await vector_service.transform_to_vectors()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/{vector_id}", response_model=Vector)
async def update_vector(vector_id: int, vector: Vector):
    pass
    # for v in db:
    #     if v.id == vector_id:
    #         v.values = vector.values
    #         return v
    # raise HTTPException(status_code=404, detail="Vector not found")

# Delete - 특정 ID의 벡터 삭제
@router.delete("/{vector_id}", response_model=Vector)
async def delete_vector(vector_id: int):
    pass
    # for i, vector in enumerate(db):
    #     if vector.id == vector_id:
    #         deleted_vector = db.pop(i)
    #         return deleted_vector
    # raise HTTPException(status_code=404, detail="Vector not found")