FROM python:3.9-slim
LABEL maintainer="Ikarus"

ENV PYTHONUNBUFFERED=1
ENV PATH="/py/bin:$PATH"
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
ARG DEV=true

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ "$DEV" = "true" ]; then /py/bin/pip install -r /tmp/requirements.dev.txt ; fi

COPY ./Backend /app

RUN useradd -m ikarus-user && \
    mkdir -p /vol/web/static /vol/web/media && \
    chown -R ikarus-user:ikarus-user /vol /app

USER ikarus-user
EXPOSE 8000
