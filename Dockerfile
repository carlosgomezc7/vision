# ==============================================================================
# Dockerfile — VISION MCP Server#
# Carlos Gómez#

# ── Stage 1: Builder ─────────────────────────────────────────────────────────
FROM python:3.12-slim AS builder

WORKDIR /build

# System deps required for building native extensions (chromadb, numpy, etc.)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Install Python packages into a virtual-env so we can copy it cleanly
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


# ── Stage 2: Runtime ─────────────────────────────────────────────────────────
FROM python:3.12-slim AS runtime

LABEL maintainer="Carlos Gómez <carlos@ctisoluciones.com>"
LABEL description="VISION MCP Server — CTI Soluciones"

WORKDIR /app

# Copy the pre-built virtual-env from the builder stage
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Runtime system deps (git is needed by auto_commit.py; SQLite comes with Python)
RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    rm -rf /var/lib/apt/lists/*

# Copy application source
COPY src/              ./src/
COPY templates/        ./templates/
COPY requirements.txt  .

# Copy seed data used by the memory seeder
COPY src/seed_data/    ./src/seed_data/

# Persistent volumes for databases (SQLite + ChromaDB vector store)
VOLUME ["/app/data"]

# Environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Expose default MCP SSE transport port (if using HTTP transport)
EXPOSE 8000

# Health-check: verify Python and fastmcp are importable
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD python -c "import fastmcp; print('ok')" || exit 1

# Default entrypoint: start the VISION MCP server
ENTRYPOINT ["python", "-m", "src.main"]
