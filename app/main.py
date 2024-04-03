from fastapi import FastAPI
from .api.v1.api import router as api_router
# from . import endpoints
# from .containers import Container


def create_app():
    # container = Container()
    # container.config.from_yaml("config.yml")
    # container.wire(modules=[endpoints])

    app = FastAPI()
    # fastapi_app.container = container
    app.include_router(api_router, prefix="/api")

    return app


app = create_app()