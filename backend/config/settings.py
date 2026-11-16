"""Настройки Django."""

from os import environ, getenv
from pathlib import Path
from sys import argv

from django.core.exceptions import ImproperlyConfigured
from django.http import HttpRequest
from django.urls import reverse_lazy

BASE_DIR = Path(__file__).resolve().parent.parent

TESTING = "test" in argv or any("pytest" in arg for arg in argv)
DEBUG = getenv("DEBUG", "False") == "True" and not TESTING
API_DOCS_ENABLE = getenv("API_DOCS_ENABLE", "False") == "True"

SECRET_KEY = getenv("SECRET_KEY") or ("insecure-test-key" if TESTING else "")
if not SECRET_KEY:
    msg = "Переменная окружения SECRET_KEY не задана"
    raise ImproperlyConfigured(msg)

SITE_HOST = getenv("SITE_HOST", "localhost")
# backend — имя сервиса в docker: по нему ходят SSR-запросы Nuxt
ALLOWED_HOSTS = [
    host.strip()
    # `or`: пустая переменная из .env тоже означает «по умолчанию»
    for host in (getenv("ALLOWED_HOSTS") or f"{SITE_HOST},localhost,127.0.0.1,backend").split(",")
    if host.strip()
]
CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in getenv("CSRF_TRUSTED_ORIGINS", f"https://{SITE_HOST}").split(",")
    if origin.strip()
]
# За nginx схема приходит в заголовке
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

INSTALLED_APPS = [
    # Тема админки должна идти до django.contrib.admin, чтобы переопределить её шаблоны
    "unfold",
    "unfold.contrib.filters",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    # Third party
    "rest_framework",
    "django_filters",
    "drf_spectacular",
    "solo",
    # Apps
    "common.apps.CommonConfig",
    "users.apps.UsersConfig",
    "catalog.apps.CatalogConfig",
    "content.apps.ContentConfig",
    "newsletter.apps.NewsletterConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if DEBUG:
    INSTALLED_APPS.append("debug_toolbar")
    MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")

    def show_toolbar_callback(request: HttpRequest) -> bool:
        """Debug toolbar в DEBUG без привязки к INTERNAL_IPS (docker); в админке не мешает."""
        return DEBUG and not request.path.startswith("/admin/")

    DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": "config.settings.show_toolbar_callback"}

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": getenv("POSTGRES_NAME", "postgres"),
        "USER": getenv("POSTGRES_USER", "postgres"),
        "PASSWORD": getenv("POSTGRES_PASSWORD"),
        "HOST": getenv("POSTGRES_HOST", "db"),
        "PORT": getenv("POSTGRES_PORT", "5432"),
        "CONN_MAX_AGE": 600,
    },
}

AUTH_USER_MODEL = "users.User"
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "ru"
TIME_ZONE = "Europe/Moscow"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/s/"
STATIC_ROOT = BASE_DIR / "static"
MEDIA_URL = "/m/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Django REST framework
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
    # Сессия Django + обязательный CSRF для небезопасных методов
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "auth": "10/min",
        "newsletter": "5/min",
    },
    # IP клиента для throttling берётся из X-Forwarded-For, который дописывает nginx
    "NUM_PROXIES": int(getenv("NUM_PROXIES", "1")),
}
if not (DEBUG or API_DOCS_ENABLE):
    REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = ["rest_framework.renderers.JSONRenderer"]

SPECTACULAR_SETTINGS = {
    "TITLE": "Portfolio Shop API",
    "VERSION": "0.1.0",
    "SERVE_INCLUDE_SCHEMA": False,
}

# Redis / Celery
REDIS_URL = f"redis://{getenv('REDIS_HOST', 'redis')}:{getenv('REDIS_PORT', '6379')}"
CELERY_BROKER_URL = f"{REDIS_URL}/0"
CELERY_RESULT_BACKEND = f"{REDIS_URL}/0"
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_ALWAYS_EAGER = TESTING

# Cache и сессии
if TESTING:
    CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}
else:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": f"{REDIS_URL}/1",
        },
    }
SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
SESSION_COOKIE_AGE = 60 * 60 * 24 * 30
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
# Secure-cookie только при HTTPS; без TLS (локальный prod-стек на :80) задайте COOKIE_SECURE=False
SESSION_COOKIE_SECURE = getenv("COOKIE_SECURE", "True") == "True" and not DEBUG and not TESTING
CSRF_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SECURE = SESSION_COOKIE_SECURE

# Email
EMAIL_BACKEND = (
    "django.core.mail.backends.console.EmailBackend"
    if DEBUG
    else "django.core.mail.backends.smtp.EmailBackend"
)
EMAIL_HOST = getenv("EMAIL_HOST", "")
EMAIL_PORT = int(getenv("EMAIL_PORT", "587"))
EMAIL_HOST_USER = getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = getenv("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = getenv("EMAIL_USE_TLS", "True") == "True"
SERVER_EMAIL = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER or f"noreply@{SITE_HOST}"

# Sentry
if environ.get("SENTRY_DSN"):
    import sentry_sdk
    from sentry_sdk.integrations.celery import CeleryIntegration
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=environ["SENTRY_DSN"],
        environment=environ.get("SENTRY_ENVIRONMENT"),
        traces_sample_rate=0.1,
        integrations=[DjangoIntegration(), CeleryIntegration()],
    )

# Админка (django-unfold): боковое меню по разделам
UNFOLD = {
    "SITE_TITLE": "Clicon — админка",
    "SITE_HEADER": "Clicon",
    "SITE_SUBHEADER": "Управление магазином",
    "SITE_URL": "/",
    "SITE_SYMBOL": "storefront",
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": [
            {
                "title": "Главная страница",
                "items": [
                    {
                        "title": "Блоки главной",
                        "icon": "view_agenda",
                        "link": reverse_lazy("admin:content_homeblock_changelist"),
                    },
                    {
                        "title": "Настройки сайта",
                        "icon": "tune",
                        "link": reverse_lazy("admin:content_sitesettings_change"),
                    },
                    {
                        "title": "Меню",
                        "icon": "menu",
                        "link": reverse_lazy("admin:content_menu_changelist"),
                    },
                ],
            },
            {
                "title": "Каталог",
                "items": [
                    {
                        "title": "Товары",
                        "icon": "inventory_2",
                        "link": reverse_lazy("admin:catalog_product_changelist"),
                    },
                    {
                        "title": "Категории",
                        "icon": "category",
                        "link": reverse_lazy("admin:catalog_category_changelist"),
                    },
                    {
                        "title": "Бренды",
                        "icon": "sell",
                        "link": reverse_lazy("admin:catalog_brand_changelist"),
                    },
                ],
            },
            {
                "title": "Пользователи и рассылка",
                "items": [
                    {
                        "title": "Пользователи",
                        "icon": "person",
                        "link": reverse_lazy("admin:users_user_changelist"),
                    },
                    {
                        "title": "Группы",
                        "icon": "group",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                    },
                    {
                        "title": "Подписчики",
                        "icon": "mail",
                        "link": reverse_lazy("admin:newsletter_subscriber_changelist"),
                    },
                ],
            },
        ],
    },
}
