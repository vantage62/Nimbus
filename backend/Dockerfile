# Base Image
FROM python:3.14-slim AS builder

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | env UV_UNMANAGED_INSTALL="/usr/local/bin" sh

# Install dependencies using uv
COPY pyproject.toml .
RUN uv pip compile pyproject.toml -o requirements.txt
RUN uv pip install --system --no-cache -r requirements.txt

# Production Image
FROM python:3.14-slim AS runner

WORKDIR /app/backend
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN addgroup --system nimbus && adduser --system --group nimbus
USER nimbus

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.14/site-packages /usr/local/lib/python3.14/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application source
COPY --chown=nimbus:nimbus backend /app/backend
# Copy pyproject.toml for completeness
COPY --chown=nimbus:nimbus pyproject.toml /app/pyproject.toml

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
