#!/usr/bin/env python3
"""Script to run the ASR service"""

import argparse
import os
import uvicorn


def main():
    """Run the ASR service"""
    # Use environment variables or defaults
    default_host = os.getenv("HOST", "0.0.0.0")
    default_port = int(os.getenv("PORT", "8000"))
    default_reload = os.getenv("RELOAD", "false").lower() == "true"

    parser = argparse.ArgumentParser(description="Ole ASR Service")
    parser.add_argument("--host", default=default_host, help="Host to bind to")
    parser.add_argument(
        "--port", type=int, default=default_port, help="Port to bind to"
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        default=default_reload,
        help="Enable auto-reload for development",
    )
    parser.add_argument(
        "--workers", type=int, default=1, help="Number of worker processes"
    )

    args = parser.parse_args()

    print(f"Starting Ole ASR Service on {args.host}:{args.port}")
    print(f"Development mode (reload): {args.reload}")
    print(f"Workers: {args.workers}")
    print("Access the service at:")
    print(f"  http://{args.host}:{args.port}")
    print(f"  http://{args.host}:{args.port}/docs (Swagger UI)")

    uvicorn.run(
        "ole_asr.api:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        workers=args.workers,
        log_level="info",
    )


if __name__ == "__main__":
    main()
