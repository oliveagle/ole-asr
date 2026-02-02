"""Configuration for the ASR service"""

import os
from typing import Optional


class ASRConfig:
    """Configuration class for ASR service"""

    # Service configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    RELOAD: bool = os.getenv("RELOAD", "false").lower() == "true"

    # Model configuration
    DEFAULT_MODEL_PATH: str = os.getenv(
        "DEFAULT_MODEL_PATH",
        "damo/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch",
    )

    # Audio processing configuration
    DEFAULT_SAMPLE_RATE: int = int(os.getenv("DEFAULT_SAMPLE_RATE", "16000"))
    SUPPORTED_FORMATS: list = ["wav", "mp3", "flac", "m4a", "aac", "ogg"]

    # GPU/CUDA configuration
    CUDA_DEVICE: str = os.getenv(
        "CUDA_DEVICE", "cuda:0" if os.path.exists("/usr/local/cuda") else "cpu"
    )

    # Model caching configuration
    MODEL_CACHE_DIR: str = os.getenv("MODEL_CACHE_DIR", "/tmp/asr_models")

    # Performance configuration
    MAX_AUDIO_DURATION: float = float(
        os.getenv("MAX_AUDIO_DURATION", "300")
    )  # 5 minutes max
    THREAD_POOL_SIZE: int = int(os.getenv("THREAD_POOL_SIZE", "4"))


# Global config instance
config = ASRConfig()
