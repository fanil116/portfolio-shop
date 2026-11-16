# Portfolio Shop

Портфолио AI-проектов: витрина кейсов, заявки, магазин, личный кабинет и админка.

## Стек

- **Backend**: Python 3.13, Django 5.2, Django REST framework, drf-spectacular, Celery, Redis, PostgreSQL 17, uv
- **Frontend**: Nuxt 4, Vue 3 (Composition API), TypeScript, Pinia, SCSS
- **Инфраструктура**: Docker Compose, nginx
- **CI**: GitHub Actions (ruff, pytest, eslint, stylelint, prettier, vue-tsc, сборка)

## Структура

| Папка       | Что внутри                                                         |
| ----------- | ------------------------------------------------------------------ |
| `backend/`  | Django: API (`/api/`), админка (`/admin/`), Celery                 |
| `frontend/` | Nuxt-приложение: страницы, store, репозиторий API                  |
| `nginx/`    | Прокси для production: `/api`, `/admin`, статика → backend, остальное → Nuxt |
| `db/`       | Образ PostgreSQL 17 с `pg_trgm`                                    |

## Авторизация

Сессии Django в httpOnly-cookie + CSRF. Браузер и API живут на одном origin:
в разработке `/api` и `/admin` проксирует Nuxt dev-сервер, в production — nginx.

- `GET /api/auth/csrf/` — выставляет cookie `csrftoken`
- `POST /api/auth/register/`, `POST /api/auth/login/`, `POST /api/auth/logout/`
- `GET|PATCH /api/auth/me/` — текущий пользователь

Небезопасные запросы передают токен в заголовке `X-CSRFToken`. Вход и регистрация
ограничены 10 запросами в минуту с одного IP.

## Админка и главная страница

Админка — Django admin в теме [Unfold](https://unfoldadmin.com/), разделы в боковом меню:

- **Блоки главной** — секции главной страницы. Порядок перетаскиванием, каждую можно скрыть.
  Тип блока задаёт содержимое: слайдер с баннерами, преимущества, лучшие предложения с таймером,
  категории, товары с табами, баннеры (1 — широкий, 2+ — рядом), колонки товаров, подписка с брендами.
  Товары, категории и баннеры блока редактируются после первого сохранения.
- **Настройки сайта** — промо-полоса, контакты, соцсети, футер; **Меню** — ссылки шапки и футера.
- **Каталог** — товары, категории (дерево), бренды.

Пустые блоки (например, без активных товаров) API не отдаёт, на сайте они не появляются.

- `GET /api/home/` — блоки главной; `GET /api/site/` — настройки и меню;
  `GET /api/catalog/categories/` — дерево категорий; `POST /api/newsletter/subscribe/` — подписка (CSRF, 5/мин).
- `make seed` заполняет каталог и главную демо-данными по структуре макета (картинки — сгенерированные плейсхолдеры).
  Картинки хранятся в `MEDIA_ROOT` (`/m/`), в production их раздаёт nginx.

## Локальная разработка

Нужны Docker, Node.js 22.12+ (рекомендуется версия из `frontend/.nvmrc`) и uv.

```shell
make env            # .env из .env.template
make build
make up             # backend :8000, db :15432, redis, celery
make createsuperuser
make front_install
make front_dev      # http://localhost:3000
```

- Сайт: http://localhost:3000
- Админка: http://localhost:3000/admin/ (или напрямую http://localhost:8000/admin/)
- API-документация: http://localhost:8000/api/docs/ (при `API_DOCS_ENABLE=True`)

## Проверки

```shell
make test           # pytest в контейнере backend
make lint           # ruff
make front_lint     # eslint + stylelint + prettier + vue-tsc
```

Git-хуки ставятся при `npm install` во `frontend/`: pre-commit (lint-staged + ruff),
commit-msg (commitlint, [Conventional Commits](https://www.conventionalcommits.org/)).

## Production-стек локально

```shell
make prod_up        # nginx на http://localhost
make prod_down
```

Без HTTPS в `.env` должно быть `COOKIE_SECURE=False`, иначе браузер не сохранит cookie сессии.
TLS и деплой пока не настроены.

## Атрибуция

- Дизайн: [Clicon — eCommerce Marketplace Website Figma Template](https://www.figma.com/community/file/1271751279140741643/clicon-ecommerce-marketplace-website-figma-template-community)
  by Templatecookie, [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
- [django-solo](https://github.com/lazybird/django-solo) — CC BY 3.0.
