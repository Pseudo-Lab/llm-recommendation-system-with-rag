# https://www.youtube.com/watch?v=8c5cOWhpKc8
# import random
# import docker
# from fastapi import APIRouter
#
# router = APIRouter()
# docker_client = docker.from_env()
# models_endpoints=[]
# @router.get("/reload")
# def reload_model(model: str):
#     port = random.randint(8000, 8500)
#     # container = docker_client.containers.run(
#     #     # "serve:latest",
#     #     image="python:3.11-slim-buster",
#     #     ports={'8000/tcp':port},
#     #     environment={
#     #         'model':model,
#     #         'tracking_uri': "http://mlflow-tracking:5001",
#     #     },
#     #     # command=[f'pip install mlflow', f'mlflow models serve --model-uri models:/{model}/1 --port {port}'],
#     #     detach=True
#     # )
#     docker_client.images.pull('ubuntu')
#
#     # 컨테이너 생성
#     container = docker_client.containers.create('ubuntu', command='/bin/bash', detach=True)
#
#     # 컨테이너 시작
#     container.start()
#
#     endpoint = f'http://localhost:{port}'
#     models_endpoints.append((container.id, endpoint))
#     return {"model": endpoint}