.PHONY: up down build logs migrate migration test clean help

# Default target: Show help
help:
	@echo "🚀 OpsConnect Makefile"
	@echo "Usage:"
	@echo "  make up         Start the full stack (detached)"
	@echo "  make down       Stop the stack"
	@echo "  make build      Force rebuild and start (use after code changes)"
	@echo "  make logs       Follow API logs in real-time"
	@echo "  make migrate    Run pending database migrations"
	@echo "  make migration  Generate a new migration file (usage: make migration msg='desc')"
	@echo "  make test       Run the test suite inside the container"
	@echo "  make clean      Stop containers and remove volumes (RESET EVERYTHING)"

up:
	docker-compose up -d

down:
	docker-compose down

build:
	docker-compose up --build -d

logs:
	docker-compose logs -f api

migrate:
	docker-compose exec api alembic upgrade head

# Usage: make migration msg="add_user_table"
migration:
	@if [ -z "$(msg)" ]; then echo "Error: msg is undefined. Usage: make migration msg='description'"; exit 1; fi
	docker-compose exec api alembic revision --autogenerate -m "$(msg)"

test:
	docker-compose exec api pytest

clean:
	docker-compose down -v
	find . -type d -name "__pycache__" -exec rm -r {} +