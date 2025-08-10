🏗️ Multi-Platform Docker Build Guide

🚀 Quick Fix - Build for Multiple Platforms

1. Setup Docker Buildx (Multi-platform builder)

```bash
# Create and use a new builder instance
docker buildx create --name multiplatform --use

# Bootstrap the builder (downloads required components)
docker buildx inspect --bootstrap

# Verify buildx is ready
docker buildx ls
```
2. Build for Multiple Platforms

```bash
# Build and push for both AMD64 and ARM64
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t moabukar/devops-interview-prep:latest \
  --push .

# Or build with version tag as well
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t moabukar/devops-interview-prep:latest \
  -t moabukar/devops-interview-prep:v1.0.0 \
  --push .
```

3. Test the Multi-Platform Image

```bash
# Pull and test (should work on both platforms now)
docker pull moabukar/devops-interview-prep:latest
docker run -it --rm moabukar/devops-interview-prep:latest topics
```

🔧 Alternative Solutions
Option 1: Quick Local Test (Specific Platform)

```bash
# Build specifically for AMD64
docker build --platform linux/amd64 -t moabukar/devops-interview-prep:amd64 .


# Test it
docker run -it --rm moabukar/devops-interview-prep:amd64 topics

# Push the AMD64 version
docker push moabukar/devops-interview-prep:amd64
```

Option 2: Force Platform When Running

```bash
# Force AMD64 platform when running
docker run --platform linux/amd64 -it --rm moabukar/devops-interview-prep:latest topics

# Or for ARM64
docker run --platform linux/arm64 -it --rm moabukar/devops-interview-prep:latest topics
```

Option 3: Local Build Without Buildx

```bash
# Remove existing image
docker rmi moabukar/devops-interview-prep:latest

# Build for your specific platform
docker build -t moabukar/devops-interview-prep:latest .

# Test locally
docker run -it --rm moabukar/devops-interview-prep:latest topics

# Push
docker push moabukar/devops-interview-prep:latest
📋 Updated Makefile with Multi-Platform Support
makefile.PHONY: docker-setup docker-build-multi docker-build-local docker-test

# Setup buildx for multi-platform builds
docker-setup:
	docker buildx create --name multiplatform --use || true
	docker buildx inspect --bootstrap

# Build for multiple platforms and push
docker-build-multi: docker-setup
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
🎯 Platform-Specific Commands
For Users on Different Platforms
bash# AMD64 (Intel/AMD processors - most common)
docker run --platform linux/amd64 -it --rm moabukar/devops-interview-prep practice aws

# ARM64 (Apple Silicon, ARM servers)
docker run --platform linux/arm64 -it --rm moabukar/devops-interview-prep practice aws

# Let Docker auto-detect (recommended after multi-platform build)
docker run -it --rm moabukar/devops-interview-prep practice aws
🔍 Debugging Platform Issues
Check Image Platform
bash# Inspect image to see available platforms
docker manifest inspect moabukar/devops-interview-prep:latest

# Check your system platform
docker version --format '{{.Server.Os}}/{{.Server.Arch}}'

# Check what platform an image was built for
docker image inspect moabukar/devops-interview-prep:latest | grep -i arch
Verify Multi-Platform Build
bash# List all platforms available for the image
docker buildx imagetools inspect moabukar/devops-interview-prep:latest
🚀 GitHub Actions for Automated Multi-Platform Builds
Create .github/workflows/docker-multiplatform.yml:
yamlname: Multi-Platform Docker Build

on:
  push:
    branches: [ main ]
    tags: [ 'v*' ]

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout
      uses: actions/checkout@v4
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3
    
    - name: Login to Docker Hub
      uses: docker/login-action@v3
      with:
        username: moabukar
        password: ${{ secrets.DOCKER_PASSWORD }}
    
    - name: Extract metadata
      id: meta
      uses: docker/metadata-action@v5
      with:
        images: moabukar/devops-interview-prep
        tags: |
          type=ref,event=branch
          type=ref,event=pr
          type=semver,pattern={{version}}
          type=raw,value=latest,enable={{is_default_branch}}
    
    - name: Build and push multi-platform
      uses: docker/build-push-action@v5
      with:
        context: .
        platforms: linux/amd64,linux/arm64
        push: true
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}
        cache-from: type=gha
        cache-to: type=gha,mode=max
⚡ Quick Resolution Steps
Right now, to fix your immediate issue:

Setup buildx:
bashdocker buildx create --name multiplatform --use
docker buildx inspect --bootstrap

Build for both platforms:
bashdocker buildx build --platform linux/amd64,linux/arm64 -t moabukar/devops-interview-prep:latest --push .

Test it:
bashdocker run -it --rm moabukar/devops-interview-prep:latest topics


This will ensure your image works on both Intel/AMD processors AND Apple Silicon Macs! 🎯