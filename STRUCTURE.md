# ole-asr Project Structure

## Overview
ole-asr is a universal Automatic Speech Recognition (ASR) service that supports multiple ASR models with a standardized interface, designed with extensibility in mind.

## Architecture

```
ole-asr/
├── ole_asr/                 # Main package
│   ├── __init__.py         # Package init
│   ├── api.py              # FastAPI application and endpoints
│   ├── models.py           # Pydantic models for request/response
│   ├── services.py         # Core ASR service and provider interface
│   ├── utils.py            # Utility functions for audio processing
│   └── providers/          # ASR model provider implementations
│       ├── __init__.py
│       ├── base.py         # Abstract base classes
│       └── qwen3_asr.py    # Qwen3 ASR implementation
├── config.py               # Configuration management
├── main.py                 # Entry point
├── run_server.py           # Server runner script
├── test_asr_service.py     # Test scripts
├── pyproject.toml          # Project metadata and dependencies
├── requirements.txt        # Dependencies
├── Dockerfile              # Docker build instructions
├── Makefile                # Convenience commands
├── .github/workflows/      # GitHub Actions workflows
│   └── docker-build.yml
├── agents.md               # Development standards
├── STRUCTURE.md            # This file
└── README.md               # Project overview
```

## Components

### Core Services
- **ASRService**: Main service class that manages providers
- **ASRProvider Protocol**: Interface defining required methods for ASR providers

### Data Models
- **ASRRequest**: Input model for transcription requests
- **ASRResponse**: Output model for transcription results
- **ASRSegment**: Individual speech segment with timing and confidence

### Audio Processing
- **utils.py**: Audio decoding, resampling, and preprocessing utilities
- **decode_audio()**: Converts base64 audio to numpy arrays
- **resample_audio()**: Handles sample rate conversion
- **get_audio_duration()**: Calculates audio length

### Providers
- **Qwen3ASRProvider**: Implementation for Qwen3-ASR model
- **Future providers**: Drop-in compatibility for additional ASR models

### API Endpoints
- **POST /transcribe**: Main transcription endpoint
- **POST /health**: Health check for all providers
- **GET /providers**: List available providers
- **GET /info**: Service information
- **GET /**: Root status endpoint

## Key Features

### Extensibility
- Plugin architecture allows easy addition of new ASR models
- Standardized interface for consistent behavior across models
- Runtime provider registration

### Robustness
- Proper error handling throughout the service
- Type safety with Pydantic models
- Async/await support for efficient I/O operations

### Production Ready
- Docker containerization with CUDA support
- GitHub Actions for CI/CD
- Health checks and monitoring endpoints
- Configuration via environment variables

### Performance
- Thread pool execution for CPU-intensive operations
- Asynchronous design for scalability
- Memory-efficient audio processing

## Configuration
Environment variables:
- `HOST`: Host address (default: 0.0.0.0)
- `PORT`: Port number (default: 8000)
- `RELOAD`: Auto-reload in development (default: false)
- `DEBUG`: Enable debug logging (default: false)
- `DEFAULT_MODEL_PATH`: Path to ASR model (default: Qwen3-ASR)
- `DEFAULT_SAMPLE_RATE`: Audio sample rate (default: 16000)

## Deployment
The service can be deployed:
1. Direct Python execution: `python run_server.py`
2. Docker container: `docker run -p 8000:8000 ole-asr`
3. Kubernetes with the provided Docker image

## Supported Audio Formats
- WAV, MP3, FLAC, M4A, AAC, OGG
- Automatic format detection and processing
- Sample rate conversion to target rate

## Future Plans
- Additional ASR model support
- Batch processing capabilities
- WebSocket support for streaming
- Advanced segmentation
- Custom vocabulary support