FROM python:3.8-slim-buster

# work directory
WORKDIR /app

# env vars
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

# build deps
COPY Pipfile Pipfile.lock /app/
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y netcat-openbsd gcc libpq-dev && \
    apt-get clean
RUN pip install --upgrade pip pipenv=="2018.11.26" && \
    pipenv install --system --deploy

COPY . /app/

EXPOSE 8000:8000
