"""Universal ASR Service Interface"""

from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable, Optional
from .models import ASRRequest, ASRResponse


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


class ASRService:
    """Main ASR Service that manages different ASR providers"""

    def __init__(self):
        self.providers: dict[str, ASRProvider] = {}
        self.default_provider: str = ""

    def register_provider(self, name: str, provider: ASRProvider):
        """Register a new ASR provider"""
        self.providers[name] = provider
        if not self.default_provider:
            self.default_provider = name

    def get_provider(self, name: str) -> ASRProvider:
        """Get a specific ASR provider"""
        if name not in self.providers:
            raise ValueError(
                f"Provider '{name}' not found. Available: {list(self.providers.keys())}"
            )
        return self.providers[name]

    def list_providers(self) -> list[str]:
        """List all registered providers"""
        return list(self.providers.keys())

    async def transcribe(
        self, request: ASRRequest, provider_name: Optional[str] = None
    ) -> ASRResponse:
        """Transcribe audio using the specified provider or default"""
        if provider_name is None:
            provider_name = self.default_provider

        if not provider_name:
            raise ValueError("No ASR provider available")

        provider = self.get_provider(provider_name)
        return await provider.transcribe(request)

    async def health_check(self) -> dict:
        """Health check for all providers"""
        results = {}
        for name, provider in self.providers.items():
            try:
                results[name] = await provider.health_check()
            except Exception as e:
                results[name] = False

        return results
