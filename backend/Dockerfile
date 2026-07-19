FROM python:3.10-slim

ARG HOSPRIME_GIT_SHA
LABEL org.opencontainers.image.revision=$HOSPRIME_GIT_SHA

WORKDIR /app

# Install system dependencies required by psycopg2 and native extensions.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies before copying application code for better layer reuse.
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Preserve the repository package namespace expected by imports such as
# `backend.app.*` in both bootstrap and application modules.
COPY . /app/backend
ENV PYTHONPATH=/app

EXPOSE 8000

# Create missing schema and the configured bootstrap administrator without
# deleting existing data, then start the FastAPI application.
CMD ["/bin/sh", "-c", "python -m backend.app.db.safe_bootstrap && uvicorn backend.app.main:app --host 0.0.0.0 --port 8000"]