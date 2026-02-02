"""ASR Service API Layer"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Optional
import logging
from .models import ASRRequest, ASRResponse
from .services import ASRService


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Ole ASR Service",
    description="Universal ASR Service supporting multiple ASR models",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, configure specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global ASR service instance
asr_service: ASRService = ASRService()


@app.on_event("startup")
async def startup_event():
    """Initialize the ASR service on startup"""
    logger.info("Initializing ASR service...")

    # Dynamically load and initialize Qwen3 ASR provider to handle import issues
    try:
        from .providers.qwen3_asr import Qwen3ASRProvider

        qwen3_provider = Qwen3ASRProvider()
        await qwen3_provider.initialize()
        asr_service.register_provider("qwen3-asr", qwen3_provider)
        logger.info(f"Registered ASR providers: {asr_service.list_providers()}")
    except ImportError as e:
        logger.warning(
            f"Could not load Qwen3 ASR provider: {e}. This may be due to missing dependencies."
        )
    except Exception as e:
        logger.error(f"Failed to initialize Qwen3 ASR provider: {e}")


@app.post("/transcribe", response_model=ASRResponse, status_code=status.HTTP_200_OK)
async def transcribe_audio(request: ASRRequest, provider: Optional[str] = None):
    """
    Transcribe audio to text using specified or default ASR provider

    Args:
        request: ASR request containing audio data
        provider: Optional provider name (uses default if not specified)

    Returns:
        ASRResponse with transcription results
    """
    try:
        logger.info(
            f"Received transcription request for provider: {provider or 'default'}"
        )
        result = await asr_service.transcribe(request, provider)
        logger.info(
            f"Successfully processed transcription, result length: {len(result.text)}"
        )
        return result
    except ValueError as e:
        logger.error(f"Value error in transcription: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in transcription: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.post("/health", response_model=Dict[str, bool])
async def health_check():
    """
    Health check endpoint to verify all providers are working

    Returns:
        Dictionary with provider health status
    """
    try:
        health_status = await asr_service.health_check()
        logger.info(f"Health check completed: {health_status}")
        return health_status
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")


@app.get("/providers", response_model=Dict[str, list])
async def list_providers():
    """
    List all available ASR providers

    Returns:
        Dictionary with available providers
    """
    try:
        providers = asr_service.list_providers()
        logger.info(f"Listing available providers: {providers}")
        return {"providers": providers}
    except Exception as e:
        logger.error(f"Error listing providers: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error listing providers: {str(e)}"
        )


@app.get("/")
async def root():
    """Root endpoint for basic service information"""
    return {
        "message": "Ole ASR Service",
        "version": "0.1.0",
        "providers": asr_service.list_providers(),
        "status": "running",
    }


@app.get("/info")
async def get_service_info():
    """Get detailed service information"""
    return {
        "service": "Ole ASR",
        "version": "0.1.0",
        "providers_count": len(asr_service.list_providers()),
        "providers": asr_service.list_providers(),
        "supported_formats": ["wav", "mp3", "flac", "m4a", "aac", "ogg"],
        "default_sample_rate": 16000,
    }
