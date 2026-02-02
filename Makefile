.PHONY: help install dev run test docker-build docker-run docker-push clean

# Project name
PROJECT_NAME = ole-asr

help:
	@echo "Commands for $(PROJECT_NAME):"
	@echo "  install     - Install project dependencies"
	@echo "  dev         - Run the service in development mode with auto-reload"
	@echo "  run         - Run the service in production mode"
	@echo "  test        - Run tests"
	@echo "  docker-build - Build Docker image"
	@echo "  docker-run  - Run Docker container"
	@echo "  docker-push - Push Docker image to registry"
	@echo "  clean       - Clean temporary files"

install:
	pip install -e .

dev:
	python run_server.py --reload --host 0.0.0.0 --port 8000

run:
	python run_server.py --host 0.0.0.0 --port 8000

test:
	python test_asr_service.py

docker-build:
	docker build -t $(PROJECT_NAME) .

docker-run:
	docker run -p 8000:8000 $(PROJECT_NAME)

docker-push:
	docker tag $(PROJECT_NAME) ghcr.io/$(USER)/$(PROJECT_NAME):latest
	docker push ghcr.io/$(USER)/$(PROJECT_NAME):latest

clean:
	rm -rf .pytest_cache __pycache__ */__pycache__ */*/__pycache__
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.pyc" -delete