# ole-asr - Universal ASR Service

A universal Automatic Speech Recognition service supporting multiple ASR models with a standardized interface.

## Features

- Standard ASR interface supporting multiple models
- Qwen3-ASR model support (first implementation)
- Extensible architecture for adding new ASR models
- GPU acceleration support (NVIDIA V100 ready)

## Architecture

The service follows a plugin architecture:

```
ASRService (interface)
├── Qwen3ASRProvider (implementation)
├── FutureASRProvider (placeholder)
└── ...
```

## Supported Models

- Qwen3-ASR (ModelScope: Qwen/Qwen3-ASR-1.7B)

## API Contract

The service implements standard ASR API contract:

```json
{
  "audio": "base64_encoded_audio",
  "sample_rate": 16000,
  "language": "auto",
  "format": "wav"
}
```

Response:

```json
{
  "text": "recognized speech",
  "segments": [...],
  "duration": 1234,
  "model": "qwen3-asr"
}
```