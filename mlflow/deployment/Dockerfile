FROM python:3.11-slim-buster

RUN pip install mlflow[genai]

WORKDIR /mlflow_deployment

COPY /mlflow/deployment/config.yaml /mlflow_deployment/config.yaml