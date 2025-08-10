.PHONY: help install dev test clean docker-build docker-run docker-push

help:
	@echo "DevOps Interview Prep CLI - Available commands:"
	@echo ""
	@echo "Development:"
	@echo "  install     Install the package"
	@echo "  dev         Install in development mode"
	@echo "  test        Run tests"
	@echo "  clean       Clean build artifacts"
	@echo ""
	@echo "Docker:"
	@echo "  docker-build    Build Docker image"
	@echo "  docker-run      Run Docker container"
	@echo "  docker-push     Push to Docker Hub"
	@echo ""
	@echo "Usage examples:"
	@echo "  make dev && devops-ip practice aws"
	@echo "  make docker-build && make docker-run"
	@echo "  devops-ip interview --count 10"

install:
	pip install -r requirements.txt
	pip install .

dev:
	pip install -r requirements.txt
	pip install -e .

test:
	python -m pytest tests/ -v

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

docker-setup:
	docker buildx create --name multiplatform --use || true
	docker buildx inspect --bootstrap

# Build for multiple platforms and push
docker-build-multi:
	docker buildx build \
		--platform linux/amd64,linux/arm64 \
		-t moabukar/devops-interview-prep:latest \
		-t moabukar/devops-interview-prep:v1.0.0 \
		--push .

# Build for local platform only
docker-build-local:
	docker build -t moabukar/devops-interview-prep:latest .

# Test the image
docker-test:
	docker run --rm moabukar/devops-interview-prep:latest --help
	docker run --rm moabukar/devops-interview-prep:latest topics
	docker run --rm moabukar/devops-interview-prep:latest stats

# Build and test locally
docker-dev: docker-build-local docker-test

# Full production build (multi-platform)
docker-prod: docker-build-multi
	@echo "✅ Multi-platform image built and pushed!"
	@echo "🚀 Users can now run: docker run -it --rm moabukar/devops-interview-prep practice aws"

# Quick development setup
setup: dev
	@echo "✅ Setup complete! Try: devops-ip practice aws"

# Run a sample interview
demo:
	devops-ip practice aws --count 3 --interview-mode

# Show available topics
topics:
	devops-ip topics

# Full interview simulation
interview:
	devops-ip interview --count 10