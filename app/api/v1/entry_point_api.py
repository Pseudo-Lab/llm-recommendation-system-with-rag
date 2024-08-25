from fastapi import APIRouter
from fastapi.responses import JSONResponse, Response, StreamingResponse
router = APIRouter()

@router.get("/health")
async def health() -> Response:
    return Response(status_code=200)

@router.post("/completions")
async def create_completion(request: CompletionRequest):

    # return StreamingResponse(content=generator, media_type="text/event-stream")

@router.post("/chat/completions")
async def create_completion():
    return "test"