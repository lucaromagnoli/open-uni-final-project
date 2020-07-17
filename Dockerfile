FROM python:3.7-alpine

# work directory
WORKDIR /app

# env vars
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

# build deps
COPY Pipfile Pipfile.lock /app/
RUN apk update && \
    apk add --virtual build-deps gcc python3-dev musl-dev libffi-dev && \
    apk add postgresql-dev libxml2-dev libxslt-dev && \
    pip install --upgrade pip pipenv=="2018.11.26" && \
    pipenv install --system --deploy && \
    apk del build-deps

COPY . /app/

EXPOSE 8000:8000
