import uuid

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.container.containers import Container
from app.model.schema.vector_schema import Gen
from app.service.gen_service import GenService

router = APIRouter()

@router.post(
    path="/response"
)
@inject
async def gen_response(
        data: Gen,
        gen_service: GenService = Depends(Provide[Container.gen_service])
):
    try:
        return gen_service.gen_response(data.workspace_id, data.input)
    except Exception as e:
        return e