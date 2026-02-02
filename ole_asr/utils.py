"""Utility functions for ASR service"""

import base64
import io
import numpy as np
import soundfile as sf
import librosa
from typing import Tuple
import torch


def decode_audio(audio_base64: str) -> Tuple[np.ndarray, int]:
    """
    Decode base64 encoded audio to numpy array

    Args:
        audio_base64: Base64 encoded audio data

    Returns:
        Tuple of (audio_array, sample_rate)
    """
    # Decode base64 string
    audio_bytes = base64.b64decode(audio_base64)

    # Load audio using soundfile
    audio_buffer = io.BytesIO(audio_bytes)

    # Try to load with soundfile first
    try:
        audio_data, sample_rate = sf.read(audio_buffer)
    except:
        # If soundfile fails, try librosa (for mp3 and other formats)
        audio_buffer.seek(0)
        audio_data, sample_rate = librosa.load(audio_buffer, sr=None)

    # Ensure audio is mono
    if len(audio_data.shape) > 1:
        audio_data = audio_data.mean(axis=1)

    # Ensure sample_rate is int
    sample_rate_int = (
        int(sample_rate) if isinstance(sample_rate, float) else sample_rate
    )

    return audio_data.astype(np.float32), sample_rate_int


def resample_audio(
    audio_data: np.ndarray, original_sr: int, target_sr: int = 16000
) -> np.ndarray:
    """
    Resample audio to target sample rate

    Args:
        audio_data: Audio data as numpy array
        original_sr: Original sample rate
        target_sr: Target sample rate (default: 16000)

    Returns:
        Resampled audio data
    """
    if original_sr == target_sr:
        return audio_data

    # Use librosa for resampling
    resampled = librosa.resample(audio_data, orig_sr=original_sr, target_sr=target_sr)
    return resampled


def audio_to_tensor(audio_data: np.ndarray) -> torch.Tensor:
    """
    Convert audio numpy array to PyTorch tensor

    Args:
        audio_data: Audio data as numpy array

    Returns:
        Audio data as PyTorch tensor
    """
    return torch.from_numpy(audio_data)


def get_audio_duration(audio_data: np.ndarray, sample_rate: int) -> float:
    """
    Calculate audio duration in seconds

    Args:
        audio_data: Audio data as numpy array
        sample_rate: Sample rate in Hz

    Returns:
        Duration in seconds
    """
    return len(audio_data) / sample_rate
