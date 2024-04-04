from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from .api.router import api_router
# from . import endpoints
# from .containers import Container


def create_app():
    # container = Container()
    # container.config.from_yaml("config.yml")
    # container.wire(modules=[endpoints])
    # fastapi_app.container = container
    app = FastAPI()
    origins = [
        "*"
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(api_router, prefix="/api")
    return app


app = create_app()