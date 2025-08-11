# DevOps Interview Prep - Development Makefile
.DEFAULT_GOAL := help

# Configuration
PYTHON := python3
PIP := pip
PACKAGE_NAME := devops_ip
VERSION := $(shell git describe --tags --always --dirty 2>/dev/null || echo "dev")
IMAGE_NAME := moabukar/devops-interview-prep

# Colors for output
BLUE := \033[36m
GREEN := \033[32m
YELLOW := \033[33m
RED := \033[31m
RESET := \033[0m

.PHONY: help setup install install-dev clean test test-cov lint format type-check
.PHONY: docker-build docker-test docker-push docker-clean
.PHONY: validate-questions add-question release

help: ## Show this help message
	@echo "$(BLUE)DevOps Interview Prep - Development Commands$(RESET)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-20s$(RESET) %s\n", $$1, $$2}'

## Development Setup
setup: clean install-dev install-pre-commit ## Complete development setup
	@echo "$(GREEN)✓ Development environment ready!$(RESET)"
	@echo "Try: $(BLUE)make test$(RESET) or $(BLUE)devops-ip practice aws$(RESET)"

install: ## Install package in production mode
	$(PIP) install .

install-dev: ## Install package in development mode with dev dependencies
	$(PIP) install -e ".[dev]"

install-pre-commit: ## Install pre-commit hooks
	pre-commit install

## Code Quality
lint: ## Run all linters
	@echo "$(BLUE)Running flake8...$(RESET)"
	flake8 $(PACKAGE_NAME) tests
	@echo "$(BLUE)Running mypy...$(RESET)"
	mypy $(PACKAGE_NAME)

format: ## Format code with black and isort
	@echo "$(BLUE)Formatting with black...$(RESET)"
	black $(PACKAGE_NAME) tests
	@echo "$(BLUE)Sorting imports with isort...$(RESET)"
	isort $(PACKAGE_NAME) tests

type-check: ## Run type checking with mypy
	mypy $(PACKAGE_NAME)

check: lint test ## Run all checks (lint + test)

## Testing
test: ## Run tests
	pytest tests/ -v

test-cov: ## Run tests with coverage report
	pytest tests/ -v --cov=$(PACKAGE_NAME) --cov-report=html --cov-report=term-missing

test-fast: ## Run tests without slow tests
	pytest tests/ -v -m "not slow"

## Question Management
validate-questions: ## Validate question JSON format and content
	$(PYTHON) scripts/validate_questions.py

add-question: ## Interactive script to add a new question
	$(PYTHON) scripts/add_question.py

question-stats: ## Show question bank statistics
	$(PYTHON) scripts/question_stats.py

## Docker Operations
docker-build: ## Build Docker image
	@echo "$(BLUE)Building Docker image $(IMAGE_NAME):$(VERSION)...$(RESET)"
	docker build -t $(IMAGE_NAME):$(VERSION) -t $(IMAGE_NAME):latest .

docker-test: ## Test Docker image
	@echo "$(BLUE)Testing Docker image...$(RESET)"
	docker run --rm $(IMAGE_NAME):latest --help
	docker run --rm $(IMAGE_NAME):latest topics
	docker run --rm $(IMAGE_NAME):latest stats

docker-push: docker-build ## Build and push Docker image to registry
	@echo "$(BLUE)Pushing Docker image...$(RESET)"
	docker push $(IMAGE_NAME):latest
	docker push $(IMAGE_NAME):$(VERSION)

docker-clean: ## Clean Docker images and containers
	@echo "$(BLUE)Cleaning Docker images...$(RESET)"
	docker system prune -f
	docker rmi $(IMAGE_NAME):latest $(IMAGE_NAME):$(VERSION) 2>/dev/null || true

## Utility
clean: ## Clean build artifacts and cache files
	@echo "$(BLUE)Cleaning build artifacts...$(RESET)"
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .mypy_cache/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

version: ## Show current version
	@echo "Version: $(VERSION)"

install-tools: ## Install development tools globally
	$(PIP) install black isort flake8 mypy pytest pre-commit

## Release Management
changelog: ## Generate changelog (requires git-cliff)
	@if command -v git-cliff >/dev/null 2>&1; then \
		git-cliff -o CHANGELOG.md; \
		echo "$(GREEN)✓ Changelog updated$(RESET)"; \
	else \
		echo "$(YELLOW)⚠ git-cliff not installed. Install with: cargo install git-cliff$(RESET)"; \
	fi

release: check validate-questions ## Prepare release (run checks, validate questions)
	@echo "$(GREEN)✓ All checks passed. Ready for release!$(RESET)"
	@echo "Next steps:"
	@echo "  1. Update version in pyproject.toml"
	@echo "  2. git tag v<version>"
	@echo "  3. git push origin v<version>"

## Demo and Examples
demo: ## Run a quick demo
	@echo "$(BLUE)Running DevOps Interview Prep demo...$(RESET)"
	@echo "2" | devops-ip practice aws --count 1 || echo "$(YELLOW)Install with 'make install-dev' first$(RESET)"

example-docker: ## Show Docker usage examples
	@echo "$(BLUE)Docker Usage Examples:$(RESET)"
	@echo "  docker run -it --rm $(IMAGE_NAME) practice aws"
	@echo "  docker run -it --rm $(IMAGE_NAME) interview --count 10"
	@echo "  docker run --rm $(IMAGE_NAME) topics"

## Development Workflow
dev: install-dev ## Quick development setup
	@echo "$(GREEN)✓ Development mode installed$(RESET)"

ci: lint test validate-questions ## Run CI pipeline locally
	@echo "$(GREEN)✓ All CI checks passed$(RESET)"

## Debugging
debug-env: ## Show development environment info
	@echo "$(BLUE)Development Environment$(RESET)"
	@echo "Python: $(shell $(PYTHON) --version)"
	@echo "Pip: $(shell $(PIP) --version)"
	@echo "Git: $(shell git --version)"
	@echo "Working directory: $(shell pwd)"
	@echo "Git branch: $(shell git branch --show-current 2>/dev/null || echo 'Not a git repo')"
	@echo "Git status:"
	@git status --porcelain 2>/dev/null || echo "Not a git repository"

# Safety checks
guard-%:
	@if [ "${${*}}" = "" ]; then \
		echo "$(RED)Error: Variable $* is not set$(RESET)"; \
		exit 1; \
	fi