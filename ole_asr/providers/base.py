"""Base ASR Provider Classes"""

from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable
from ..models import ASRRequest, ASRResponse


@runtime_checkable
class ASRProvider(Protocol):
    """Abstract protocol for ASR providers - defines the standard interface"""

    @abstractmethod
    async def transcribe(self, request: ASRRequest) -> ASRResponse:
        """Process audio and return transcription"""
        ...

    @abstractmethod
    async def health_check(self) -> bool:
        """Check if the ASR provider is healthy and ready"""
        ...
