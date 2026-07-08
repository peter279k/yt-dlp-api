FROM docker.io/library/python:3.12-slim

# Set working directory
WORKDIR /app

# Install runtime dependencies + testing/lint tools
COPY requirements.txt .
COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    mkdir /app/app && \
    apt update && \
    apt install -y curl unzip


# Copy FastAPI app
COPY . /app/app/

RUN groupadd -g 1000 appgroup && \
    useradd -u 1000 -g appgroup -m -s /bin/bash appuser && \
    chown -R appuser:appgroup /app/

USER appuser

RUN curl -fsSL https://deno.land/install.sh | sh
