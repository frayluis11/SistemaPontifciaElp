.PHONY: help build up down restart logs clean init test

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

build: ## Build all Docker containers
	docker-compose build

up: ## Start all services
	docker-compose up -d
	@echo "✅ Services started!"
	@echo "Frontend: http://localhost:3000"
	@echo "Backend: http://localhost:8000"
	@echo "API Docs: http://localhost:8000/docs"

down: ## Stop all services
	docker-compose down

restart: ## Restart all services
	docker-compose restart

logs: ## Show logs from all services
	docker-compose logs -f

logs-backend: ## Show backend logs
	docker-compose logs -f backend

logs-frontend: ## Show frontend logs
	docker-compose logs -f frontend

logs-db: ## Show database logs
	docker-compose logs -f db

clean: ## Stop services and remove volumes
	docker-compose down -v
	@echo "⚠️  All data has been removed!"

init: ## Initialize database with sample data
	@chmod +x init.sh
	@./init.sh

shell-backend: ## Open shell in backend container
	docker-compose exec backend /bin/bash

shell-frontend: ## Open shell in frontend container
	docker-compose exec frontend /bin/sh

shell-db: ## Open PostgreSQL shell
	docker-compose exec db psql -U postgres -d pontificia_db

backup-db: ## Backup database
	@mkdir -p backups
	docker-compose exec db pg_dump -U postgres pontificia_db > backups/backup_$$(date +%Y%m%d_%H%M%S).sql
	@echo "✅ Database backed up to backups/"

restore-db: ## Restore database from latest backup (make restore-db FILE=backups/backup.sql)
	@if [ -z "$(FILE)" ]; then \
		echo "❌ Please specify a backup file: make restore-db FILE=backups/backup.sql"; \
		exit 1; \
	fi
	docker-compose exec -T db psql -U postgres -d pontificia_db < $(FILE)
	@echo "✅ Database restored from $(FILE)"

test-backend: ## Run backend tests
	docker-compose exec backend pytest

test-frontend: ## Run frontend tests
	docker-compose exec frontend npm test

dev: ## Start in development mode with logs
	docker-compose up

status: ## Show status of all services
	docker-compose ps

install: ## Initial setup (build, start, init database)
	@echo "🚀 Starting initial setup..."
	@make build
	@make up
	@sleep 10
	@make init
	@echo "✅ Setup complete!"
	@echo ""
	@echo "Access the application at http://localhost:3000"

update: ## Update and rebuild services
	git pull
	docker-compose down
	docker-compose build
	docker-compose up -d
	@echo "✅ Services updated and restarted!"
