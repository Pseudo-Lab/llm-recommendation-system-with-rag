import argparse
import os
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware

from fastapi.templating import Jinja2Templates


def create_app() -> FastAPI:
    # 환경 변수 설정 후 아래의 모듈이 import되도록 위치 전환
    from api.router import api_router
    from container.containers import Container

    app = FastAPI()
    container = Container()
    container.config.db_url.from_env("MYSQL_DB_URL")
    # templates = Jinja2Templates(directory="app/templates")
    db = container.db()
    db.create_database()
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
    app.container = container
    app.include_router(api_router, prefix="/api")
    return app

    # @app.get("/")
    # async def read_index(request: Request):
    #     return templates.TemplateResponse("index.html", {"request":request})
    # return app

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script description')
    parser.add_argument('--host', default='127.0.0.1', help='Host address')
    parser.add_argument('--port', type=int, default=8989, help='Port number')
    parser.add_argument('--workers', type=int, help='Number of workers')
    parser.add_argument('--log-level', default='debug', choices=['debug', 'info', 'warning', 'error', 'critical'],
                        help='Log level')
    parser.add_argument('--env', default='local', choices=['local', 'dev'], help='environment')
    parser.add_argument('--reload', action='store_true', help='Enable auto-reload')
    args = parser.parse_args()

    if args.env == "local":
        os.environ['ENV'] = "local"
    elif args.env == "dev":
        os.environ['ENV'] = "dev"
    env = os.getenv('ENV', 'dev')
    load_dotenv(f'../.env.{env}')

    db_url = os.getenv("MYSQL_DB_URL")
    vector_db_url = os.getenv("ES_URL")
    print(f'db connected : {db_url}')
    print(f'vector db connected : {vector_db_url}')

    uvicorn.run(
        "main:create_app",
        host=args.host,
        port=args.port,
        workers=args.workers,
        log_level=args.log_level,
        reload=args.reload,
    )



