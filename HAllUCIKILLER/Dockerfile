# ==============================================================================
# HALLUCIKILLER // PRODUCTION CONTAINER DOCKERFILE
# Multi-stage lightweight Python 3.12 container
# ==============================================================================

FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Environment variables
ENV PYTHONUNBUFFERED=1 \
    HALLUCIKILLER_API_HOST=0.0.0.0 \
    HALLUCIKILLER_API_PORT=8000

# Expose HTTP port
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Launch FastAPI server with Uvicorn
CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"]
