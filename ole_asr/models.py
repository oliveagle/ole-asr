"""ASR Data Models"""

from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from enum import Enum


class AudioFormat(str, Enum):
    """Supported audio formats"""

    WAV = "wav"
    MP3 = "mp3"
    FLAC = "flac"
    M4A = "m4a"
    AAC = "aac"
    OGG = "ogg"


class ASRRequest(BaseModel):
    """ASR Request Model"""

    audio: str  # Base64 encoded audio data
    sample_rate: int = 16000  # Audio sample rate in Hz
    language: str = "auto"  # Language code (e.g., 'en', 'zh', 'auto')
    format: AudioFormat = AudioFormat.WAV  # Audio format
    model_params: Optional[Dict[str, Any]] = None  # Model-specific parameters


class ASRSegment(BaseModel):
    """ASR Segment Model - represents a portion of recognized speech"""

    start_time: float  # Start time in seconds
    end_time: float  # End time in seconds
    text: str  # Transcribed text
    confidence: Optional[float] = None  # Confidence score


class ASRResponse(BaseModel):
    """ASR Response Model"""

    text: str  # Full transcribed text
    segments: List[ASRSegment]  # Segmented transcriptions
    duration: float  # Audio duration in seconds
    model: str  # Model identifier
    language: Optional[str] = None  # Detected/used language
    sample_rate: Optional[int] = None  # Sample rate used for processing
