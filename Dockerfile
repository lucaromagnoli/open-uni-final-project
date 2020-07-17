FROM python:3.7-alpine

# work directory
WORKDIR /app

# env vars
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

# install psycopg2 deps
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql-dev

# install env deps
RUN pip install pipenv
COPY Pipfile Pipfile.lock /app/
RUN pipenv install --system

# del psycopg deps
RUN apk del build-deps

COPY . /app/

EXPOSE 8000:8000
