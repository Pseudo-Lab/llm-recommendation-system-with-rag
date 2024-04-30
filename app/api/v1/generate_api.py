import uuid

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from starlette.responses import StreamingResponse

from app.container.containers import Container
from app.model.schema.vector_schema import Gen
from app.service.gen_service import GenService
from fastapi import HTTPException
router = APIRouter()

@router.post(
    path="/response"
)
@inject
async def gen_response(
        request: Gen,
        gen_service: GenService = Depends(Provide[Container.gen_service])
):
    try:
        return await gen_service.gen_response(request.workspace_id, request.input)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post(
    path="/response/stream"
)
@inject
async def gen_response_stream(
        request: Gen,
        gen_service: GenService = Depends(Provide[Container.gen_service])
):
    # return StreamingResponse(content=GenService.gen_response_stream(input=request.input), media_type="text/event-stream")
    return StreamingResponse(content=gen_service.gen_response_stream(input=request.input, workspace_id=request.workspace_id),
                             media_type="text/event-stream")