.PHONY: help install test lint format clean docker-build docker-run setup

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install all dependencies
	pip install -r requirements.txt
	pip install -r requirements-async.txt
	pip install -r requirements-test.txt
	pip install -r requirements-dev.txt

setup: ## Initialize project setup
	python3 setup.py
	pre-commit install

test: ## Run tests with coverage
	pytest --cov=. --cov-report=html --cov-report=term-missing

test-fast: ## Run tests without coverage
	pytest -x -v

lint: ## Run all linting tools
	black --check .
	isort --check-only .
	flake8 .
	mypy . --ignore-missing-imports
	bandit -r . -f json || true

format: ## Format code with black and isort
	black .
	isort .

security: ## Run security checks
	bandit -r .
	safety check

clean: ## Clean up generated files
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf *.db
	rm -rf __pycache__/
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} +

docker-build: ## Build Docker image
	docker build -t tbomb-enhanced .

docker-run: ## Run Docker container
	docker-compose up -d

docker-stop: ## Stop Docker containers
	docker-compose down

docker-logs: ## View Docker logs
	docker-compose logs -f

run-async: ## Run async bomber
	python3 bomber_async.py

run-health: ## Run health monitor
	python3 health_monitor.py

run-original: ## Run original bomber
	python3 bomber.py

benchmark: ## Run performance benchmarks
	python3 -m pytest tests/ -k "benchmark" -v

coverage-html: ## Generate HTML coverage report
	pytest --cov=. --cov-report=html
	@echo "Coverage report generated in htmlcov/index.html"

pre-commit: ## Run pre-commit hooks
	pre-commit run --all-files

check: lint test ## Run all checks (lint + test)

dev-setup: install setup ## Complete development setup
	@echo "Development environment ready!"

ci: ## Run CI pipeline locally
	make lint
	make test
	make security