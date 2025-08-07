# Prospect Research Platform - Development Commands

.PHONY: help install test lint format type-check clean dev dev-backend dev-frontend docker-up docker-down

help:
	@echo "Available commands:"
	@echo "  install     - Install all dependencies (Python + Node.js)"
	@echo "  test        - Run all tests with coverage"
	@echo "  lint        - Run linting (ruff)"
	@echo "  format      - Format code (black + prettier)"
	@echo "  type-check  - Run type checking (mypy + tsc)"
	@echo "  clean       - Clean build artifacts and cache"
	@echo "  dev         - Start both backend and frontend in development mode"
	@echo "  dev-backend - Start only the backend API server"
	@echo "  dev-frontend- Start only the frontend development server"
	@echo "  docker-up   - Start services with Docker Compose"
	@echo "  docker-down - Stop Docker services"

install:
	@echo "Installing Python dependencies..."
	pip install -r requirements.txt
	pip install -e ".[dev]"
	@echo "Installing Node.js dependencies..."
	cd frontend && npm install

test:
	@echo "Running backend tests with coverage..."
	coverage run -m pytest -v
	coverage report
	coverage html
	@echo "Running frontend tests..."
	cd frontend && npm test

lint:
	@echo "Linting Python code..."
	ruff check .
	@echo "Linting frontend code..."
	cd frontend && npm run lint

format:
	@echo "Formatting Python code..."
	black .
	ruff check --fix .
	@echo "Formatting frontend code..."
	cd frontend && npm run format

type-check:
	@echo "Type checking Python code..."
	mypy .
	@echo "Type checking frontend code..."
	cd frontend && npm run type-check

clean:
	@echo "Cleaning Python cache..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .coverage htmlcov/ .pytest_cache/ .mypy_cache/
	@echo "Cleaning Node.js cache..."
	cd frontend && rm -rf .next/ node_modules/.cache/

dev:
	@echo "Starting development servers..."
	@echo "Backend: http://localhost:8000"
	@echo "Frontend: http://localhost:3000"
	@echo "Press Ctrl+C to stop both servers"
	# Run both servers concurrently
	(trap 'kill 0' SIGINT; python api/main.py & cd frontend && npm run dev & wait)

dev-backend:
	@echo "Starting backend API server..."
	@echo "API: http://localhost:8000"
	@echo "Docs: http://localhost:8000/docs"
	python api/main.py

dev-frontend:
	@echo "Starting frontend development server..."
	@echo "Frontend: http://localhost:3000"
	cd frontend && npm run dev

docker-up:
	@echo "Starting services with Docker Compose..."
	docker-compose up -d
	@echo "Backend: http://localhost:8000"
	@echo "Frontend: http://localhost:3000"

docker-down:
	@echo "Stopping Docker services..."
	docker-compose down

# Quality assurance - run before committing
qa: format lint type-check test
	@echo "✅ Quality assurance checks passed!"

# Production deployment preparation
build:
	@echo "Building for production..."
	cd frontend && npm run build
	@echo "✅ Production build complete!"

# Database operations
db-reset:
	@echo "Resetting database schema..."
	@echo "Run database/schema.sql in Supabase SQL editor"

# AI development helpers
claude-test:
	@echo "Testing Claude Code integration..."
	python -c "from config.settings import settings; print('✅ Settings loaded')"
	python -c "from utils.database import db; print('✅ Database connected')"
	python -c "import asyncio; from agents.research.research_agent import ResearchAgent; print('✅ Agents loadable')"

# Environment setup
setup-env:
	@echo "Setting up environment..."
	cp .env.example .env
	@echo "✅ Environment template created - edit .env with your keys"