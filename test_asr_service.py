#!/usr/bin/env python3
"""Basic test script to validate ASR service setup"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from ole_asr.services import ASRService
from ole_asr.models import ASRRequest, AudioFormat


def test_service_initialization():
    """Test that the ASR service initializes correctly"""
    print("Testing ASR service initialization...")

    try:
        service = ASRService()
        print(f"✓ ASR Service initialized successfully")
        print(f"  - Available providers: {service.list_providers()}")
        return True
    except Exception as e:
        print(f"✗ Failed to initialize ASR service: {e}")
        return False


def test_models():
    """Test that ASR data models work correctly"""
    print("\nTesting ASR data models...")

    try:
        # Test ASRRequest creation
        request = ASRRequest(
            audio="dGVzdCBhdWRpbw==",  # base64 encoded "test audio"
            sample_rate=16000,
            language="en",
            format=AudioFormat.WAV,
        )
        print(f"✓ ASRRequest created successfully: {request.format}")

        # Test that properties work
        print(f"  - Audio: {len(request.audio)} chars")
        print(f"  - Sample rate: {request.sample_rate}")
        print(f"  - Language: {request.language}")
        return True
    except Exception as e:
        print(f"✗ Failed to create ASR models: {e}")
        return False


async def test_service_async():
    """Test async functionality of the service"""
    print("\nTesting ASR service async functionality...")

    try:
        service = ASRService()

        # Try to perform a health check (should handle uninitialized providers gracefully)
        health_status = await service.health_check()
        print(f"✓ Health check completed: {health_status}")

        # Try to list providers again
        providers = service.list_providers()
        print(f"  - Registered providers: {providers}")
        return True
    except Exception as e:
        print(f"✗ Async service test failed: {e}")
        return False


async def main():
    """Run all tests"""
    print("Running ASR Service Validation Tests...\n")

    results = []

    # Run tests
    results.append(test_service_initialization())
    results.append(test_models())
    results.append(await test_service_async())

    # Summary
    passed = sum(results)
    total = len(results)

    print(f"\n{'=' * 50}")
    print(f"Test Results: {passed}/{total} passed")

    if passed == total:
        print("✓ All tests passed! ASR service structure is valid.")
        print("\nTo run the ASR service:")
        print("  python run_server.py")
        print("\nTo build and run with Docker:")
        print("  docker build -t ole-asr .")
        print("  docker run -p 8000:8000 ole-asr")
        return True
    else:
        print("✗ Some tests failed.")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
