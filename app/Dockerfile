FROM python:3.10

WORKDIR /app

COPY ./app /app
COPY ./requirements.txt /app/

RUN pip install --no-cache-dir --upgrade pip \
 && pip install -r requirements.txt
