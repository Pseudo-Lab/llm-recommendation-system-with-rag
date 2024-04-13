from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from .api.router import api_router
from app.container.containers import Container

def create_app():
    app = FastAPI()
    container = Container()
    db = container.db()
    db.create_database()

    app.container = container

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