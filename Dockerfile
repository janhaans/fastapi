FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

RUN pip install --no-cache-dir sqlalchemy

COPY ./app /app

WORKDIR /app

RUN mkdir data