# Apex AM Docker Makefile
# Make development and deployment easier with simple commands

.PHONY: help dev prod build clean logs test db-init

# Default target
help:
	@echo "Apex AM Docker Commands"
	@echo "======================="
	@echo ""
	@echo "Development:"
	@echo "  make dev          - Start development environment"
	@echo "  make dev-build    - Build and start development environment"
	@echo "  make dev-logs     - View development logs"
	@echo "  make dev-down     - Stop development environment"
	@echo ""
	@echo "General:"
	@echo "  make build        - Build all Docker images"
	@echo "  make clean        - Stop and remove all containers"
	@echo "  make logs         - View all service logs"
	@echo "  make test         - Run tests in development container"
	@echo "  make shell        - Open shell in backend container"
	@echo ""

# Development environment
dev:
	docker compose up

dev-build:
	docker compose up --build

dev-logs:
	docker compose logs -f
dev-down:
	docker compose down

# Build all images
build:
	docker compose build

# Clean up
clean:
	docker compose down -v --remove-orphans
	docker system prune -f

# View logs
logs:
	docker compose logs -f

# Run tests
test:
	docker compose exec backend pytest

test-coverage:
	docker compose exec backend pytest --cov=app

# Open shell in backend container
shell:
	docker compose exec backend bash

# View service status
status:
	docker compose ps

# Restart services
restart:
	docker compose restart

# Pull latest images
pull:
	docker compose pull

# View resource usage
stats:
	docker stats

# Clean up unused images and volumes
prune:
	docker system prune -a -f
	docker volume prune -f
	docker network prune -f
