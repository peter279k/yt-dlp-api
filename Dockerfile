FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install runtime dependencies + testing/lint tools
COPY requirements.txt .
COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    mkdir /app/app && \
    apt update && \
    apt install -y ffmpeg curl unzip


# Copy FastAPI app
COPY . /app/app/

# Create downloads directory
RUN mkdir -p /app/downloads

RUN groupadd -g 1000 appgroup && \
    useradd -u 1000 -g appgroup -m -s /bin/bash appuser && \
    chown -R appuser:appgroup /app/

USER appuser

RUN curl -fsSL https://deno.land/install.sh | sh
