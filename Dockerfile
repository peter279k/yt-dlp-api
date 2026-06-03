FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Set PYTHONPATH so Python can find the 'app' module
ENV PYTHONPATH=/app

# Install runtime dependencies + testing/lint tools
COPY requirements.txt .
COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    apt update && \
    apt install -y ffmpeg curl


# Copy FastAPI app
COPY ./routers ./app/
COPY ./main.py ./app/

# Create downloads directory
RUN mkdir -p /app/downloads

RUN groupadd -g 10000 appgroup && \
    useradd -u 1000- -g appgroup -m -s /bin/bash appuser && \
    chown -R appuser:appgroup /app/

USER appuser

RUN curl -fsSL https://deno.land/install.sh | sh
