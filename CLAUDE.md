# Portfolio Shop

Монорепо: `backend/` (Django + DRF + Celery, uv), `frontend/` (Nuxt 4 + Pinia), `nginx/`, `db/`.
Подробности — в README.md.

## Команды проверки

- Backend: `cd backend && uv run ruff check . && uv run ruff format --check .`
- Backend-тесты (нужен запущенный `make up`): `make test`
- Миграции не забыты: `docker compose exec backend uv run python manage.py makemigrations --check --dry-run`
- Frontend: `cd frontend && npm run lint:check && npm run tsc:check && npm run build`

## Соглашения

- Новые API — ViewSet + регистрация в `backend/config/routers.py`.
- Авторизация сессионная; анонимные POST, меняющие состояние, проверяют CSRF явно
  (DRF делает это только для вошедших пользователей — см. `users/viewsets.py`).
- Frontend ходит в API только через модули `app/repository/modules/*`, подключённые в
  `app/plugins/01.fetchData.ts` (`useNuxtApp().$fetchData`).
- Импорты в `app/` — через `~/`, без `../`.
- Публичный репозиторий: никаких секретов, внутренних ссылок и кода работодателя.
