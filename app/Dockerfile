FROM python:3.10

WORKDIR /code

COPY ./app /code/app
COPY ./requirements.txt /code/

RUN pip install --no-cache-dir --upgrade pip \
 && pip install -r requirements.txt
