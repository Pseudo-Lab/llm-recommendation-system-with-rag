FROM python:3.10

WORKDIR /code

COPY . /code/

RUN pip install --no-cache-dir --upgrade pip \
 && pip install -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
