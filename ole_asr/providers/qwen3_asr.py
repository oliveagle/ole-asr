"""Qwen3 ASR Provider Implementation"""

import asyncio
import torch
import numpy as np
from typing import Optional, Any, TYPE_CHECKING
from ..models import ASRRequest, ASRResponse, ASRSegment
from .base import ASRProvider
from ..utils import decode_audio, resample_audio, get_audio_duration

# Only import for type checking to avoid runtime import issues
if TYPE_CHECKING:
    pass  # We won't import modelscope here to avoid static analysis issues


class Qwen3ASRProvider:
    """Qwen3 ASR Provider implementing the ASRProvider protocol"""

    def __init__(
        self,
        model_path: str = "damo/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch",
    ):
        """
        Initialize the Qwen3 ASR Provider

        Args:
            model_path: Path to the Qwen3 ASR model on ModelScope
        """
        self.model_path = model_path
        self.pipeline = None
        self.is_initialized = False

    def _get_pipeline_class(self):
        """Lazy load the pipeline class to avoid import issues during static analysis"""
        # Dynamically import only when called
        import importlib

        pipelines_module = importlib.import_module(
            "modelscope.pipelines.automatic_speech_recognition"
        )
        constants_module = importlib.import_module("modelscope.utils.constant")
        return getattr(pipelines_module, "AutomaticSpeechRecognitionPipeline"), getattr(
            constants_module, "Tasks"
        )

    async def initialize(self):
        """Initialize the ASR pipeline asynchronously"""
        if not self.is_initialized:
            # Run model loading in a thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, self._load_model)
            self.is_initialized = True

    def _load_model(self):
        """Load the ASR model (runs in thread pool)"""
        pipeline_cls, tasks_cls = self._get_pipeline_class()

        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.pipeline = pipeline_cls(
            task=tasks_cls.auto_speech_recognition,
            model=self.model_path,
            model_revision="v1.0.4",
            device=device,
        )

    async def transcribe(self, request: ASRRequest) -> ASRResponse:
        """
        Transcribe audio using Qwen3 ASR model

        Args:
            request: ASR request containing audio data

        Returns:
            ASR response with transcription
        """
        if not self.is_initialized:
            await self.initialize()

        if self.pipeline is None:
            raise RuntimeError("ASR pipeline not initialized properly")

        # Decode the base64 audio
        audio_data, original_sample_rate = decode_audio(request.audio)

        # Resample audio if needed
        if original_sample_rate != request.sample_rate:
            audio_data = resample_audio(
                audio_data, original_sample_rate, request.sample_rate
            )

        # Calculate audio duration
        duration = get_audio_duration(audio_data, request.sample_rate)

        # Perform transcription (run in thread pool to avoid blocking)
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None, self._perform_transcription, audio_data
        )

        # Extract text from result
        if isinstance(result, dict) and "text" in result:
            text = result["text"]
        elif isinstance(result, str):
            text = result
        else:
            text = str(result) if result is not None else ""

        # Create a single segment for the full audio
        segments = [
            ASRSegment(
                start_time=0.0,
                end_time=duration,
                text=text,
                confidence=0.9,  # Placeholder confidence value
            )
        ]

        return ASRResponse(
            text=text,
            segments=segments,
            duration=duration,
            model="qwen3-asr",
            language=request.language,
            sample_rate=request.sample_rate,
        )

    def _perform_transcription(self, audio_data: np.ndarray):
        """Perform transcription with the loaded model (runs in thread pool)"""
        if self.pipeline is None:
            raise RuntimeError("ASR pipeline not initialized")

        # The pipeline expects audio in the correct format
        result = self.pipeline(audio_data)
        return result

    async def health_check(self) -> bool:
        """
        Check if the ASR provider is healthy and ready

        Returns:
            True if the provider is ready, False otherwise
        """
        try:
            if not self.is_initialized:
                await self.initialize()
            return self.pipeline is not None
        except Exception as e:
            print(f"Health check failed: {e}")
            return False
