FROM python:3.13-slim

# Set working directory
WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry==1.8.3

RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock* ./

RUN poetry install --no-interaction --no-ansi --no-root

# Disable Python output buffering
ENV PYTHONUNBUFFERED=1

# Copy application code
COPY . .
