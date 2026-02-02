FROM pytorch/pytorch:2.3.1-cuda12.1-cudnn8-devel

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY pyproject.toml .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir "modelscope>=1.9.0" && \
    pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121 && \
    pip install --no-cache-dir "transformers>=4.35.0" && \
    pip install --no-cache-dir "numpy>=1.21.0" && \
    pip install --no-cache-dir "pydantic>=2.0.0" && \
    pip install --no-cache-dir "fastapi>=0.104.0" && \
    pip install --no-cache-dir "uvicorn[standard]>=0.24.0" && \
    pip install --no-cache-dir "python-multipart>=0.0.6" && \
    pip install --no-cache-dir "soundfile>=0.12.1" && \
    pip install --no-cache-dir "librosa>=0.10.0"

# Copy source code
COPY . .

# Install the package in development mode
RUN pip install -e .

# Download the model in advance to avoid download during runtime (as root)
RUN mkdir -p /tmp/asr_models && \
    python -c "from modelscope.hub.snapshot_download import snapshot_download; snapshot_download('damo/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch', cache_dir='/tmp/asr_models')"

# Expose port
EXPOSE 8000

# Create non-root user for security
RUN groupadd -r asruser && useradd -r -g asruser asruser && \
    chown -R asruser:asruser /app /tmp/asr_models
USER asruser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["python", "main.py"]