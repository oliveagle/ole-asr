"""Main entry point for the ASR service"""

import uvicorn
import os
from ole_asr.api import app


def main():
    """Start the ASR service"""
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    reload = os.getenv("RELOAD", "false").lower() == "true"

    print(f"Starting ASR service on {host}:{port}")
    print(f"Development mode (reload): {reload}")

    uvicorn.run(
        "ole_asr.api:app", host=host, port=port, reload=reload, log_level="info"
    )


if __name__ == "__main__":
    main()
