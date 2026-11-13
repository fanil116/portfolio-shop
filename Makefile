# =============================================================================
# Makefile для управления проектом
# =============================================================================

COMPOSE = docker compose
COMPOSE_PROD = docker compose -f docker-compose.yml -f docker-compose.frontend.yml -f docker-compose.production.yml

.PHONY: help env build up down logs exec_backend shell migrate makemigrations \
	createsuperuser test lint lint_fix front_install front_dev front_lint prod_up prod_down

.DEFAULT_GOAL := help

help:
	@echo "Docker (локальная разработка):"
	@echo "  make env              - Создать .env из .env.template"
	@echo "  make build            - Собрать образы"
	@echo "  make up               - Запустить backend, db, redis, celery"
	@echo "  make down             - Остановить контейнеры"
	@echo "  make logs             - Логи backend"
	@echo ""
	@echo "Backend:"
	@echo "  make exec_backend     - Shell в контейнере backend"
	@echo "  make shell            - Django shell"
	@echo "  make migrate          - Применить миграции"
	@echo "  make makemigrations   - Создать миграции"
	@echo "  make createsuperuser  - Создать администратора"
	@echo "  make test             - pytest в контейнере backend"
	@echo "  make lint             - ruff check + ruff format --check"
	@echo "  make lint_fix         - ruff check --fix + ruff format"
	@echo ""
	@echo "Frontend:"
	@echo "  make front_install    - npm ci"
	@echo "  make front_dev        - Nuxt dev-сервер на http://localhost:3000"
	@echo "  make front_lint       - eslint + stylelint + vue-tsc"
	@echo ""
	@echo "Production:"
	@echo "  make prod_up          - Собрать и запустить всё за nginx на :80"
	@echo "  make prod_down        - Остановить production-стек"

env:
	@test -f .env && echo ".env уже существует" || cp .env.template .env

build:
	$(COMPOSE) build

up:
	$(COMPOSE) up -d --remove-orphans

down:
	$(COMPOSE) down

logs:
	$(COMPOSE) logs -f backend

exec_backend:
	$(COMPOSE) exec backend sh

shell:
	$(COMPOSE) exec backend uv run python manage.py shell

migrate:
	$(COMPOSE) exec backend uv run python manage.py migrate

makemigrations:
	$(COMPOSE) exec backend uv run python manage.py makemigrations

createsuperuser:
	$(COMPOSE) exec backend uv run python manage.py createsuperuser

test:
	$(COMPOSE) exec backend uv run pytest

lint:
	$(COMPOSE) exec backend uv run ruff check .
	$(COMPOSE) exec backend uv run ruff format --check .

lint_fix:
	$(COMPOSE) exec backend uv run ruff check --fix .
	$(COMPOSE) exec backend uv run ruff format .

front_install:
	cd frontend && npm ci

front_dev:
	cd frontend && npm run dev

front_lint:
	cd frontend && npm run lint:check && npm run tsc:check

prod_up:
	$(COMPOSE_PROD) up -d --build --remove-orphans

prod_down:
	$(COMPOSE_PROD) down
