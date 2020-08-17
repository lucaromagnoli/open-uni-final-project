FROM python:3.7-slim-buster

ARG APP_USER=appuser
RUN groupadd -r ${APP_USER} && useradd --no-log-init -r -g ${APP_USER} ${APP_USER}
WORKDIR /app

# env vars
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

ARG BUILD_DEPS="build-essential libpq-dev"
ARG DEPS="gdal-bin gettext postgresql-client"

COPY requirements.txt /app

RUN apt-get update && \
    apt-get install -y $BUILD_DEPS $DEPS --no-install-recommends
RUN pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y --auto-remove $BUILD_DEPS \
    && rm -rf /var/lib/apt/lists/*

COPY . /app
