import os
from pathlib import Path
from decouple import Config, RepositoryEnv, config

BASE_DIR = Path(__file__).resolve().parent.parent.parent
BACKEND_DIR = Path(__file__).resolve().parent.parent

config = Config(RepositoryEnv(os.path.join(BASE_DIR, ".env")))

IS_PRODUCTION = config('IS_PRODUCTION', default=False, cast=bool)
DEBUG = config('DEBUG', default=True, cast=bool)

# Determine whether we're in production, as this will affect many settings.
if IS_PRODUCTION:
    # Production settings
    prod = True
else:
    # Development settings
    prod = False

if not prod:
    AZURE_STORAGE_ACCOUNT_NAME = config('AZURE_STORAGE_ACCOUNT_NAME', default="")
    AZURE_STORAGE_CONNECTION_STRING = config('AZURE_STORAGE_CONNECTION_STRING', default='')
    AZURE_CONTAINER_NAME = config('AZURE_CONTAINER_NAME', default='default-container')
    AZURE_STORAGE_ACCOUNT_KEY = config("AZURE_STORAGE_ACCOUNT_KEY", default="")
    STORAGE_BACKEND = config('STORAGE_BACKEND', default='azure')
    DEBUG = True
    DEFAULT_SECRET = config("DEFAULT_SECRET", default="default-secret")
    CSRF_TRUSTED_ORIGINS = [
        config("WEBSITE_HOSTNAME"),
    ]
    if config("CODESPACE_NAME"):
        CSRF_TRUSTED_ORIGINS.append(
            f"https://{config('CODESPACE_NAME')}-8000.{config('GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN')}"
        )
else:
    AZURE_STORAGE_ACCOUNT_NAME = config('AZURE_STORAGE_ACCOUNT_NAME', default="")
    AZURE_STORAGE_CONNECTION_STRING = config('AZURE_STORAGE_CONNECTION_STRING', default='')
    AZURE_CONTAINER_NAME = config('AZURE_CONTAINER_NAME', default='default-container')
    AZURE_STORAGE_ACCOUNT_KEY = config("AZURE_STORAGE_ACCOUNT_KEY", default="")
    STORAGE_BACKEND = config('STORAGE_BACKEND', default='azure')
    DEBUG = False
    DEFAULT_SECRET = None
    CSRF_TRUSTED_ORIGINS = [
        config("WEBSITE_HOSTNAME"),
    ]

ALLOWED_HOSTS = [
        config("WEBSITE_HOSTNAME"),
        "127.0.0.1"
    ]

CORS_ALLOWED_ORIGINS = [
        config("WEBSITE_HOSTNAME"),
    ]

SECRET_KEY = config("SECRET_KEY", default=DEFAULT_SECRET)

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "relecloud.apps.RelecloudConfig",
    "corsheaders",
    "rest_framework"
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'project.middleware.FrontendAuthMiddleware', 
]

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "project.wsgi.application"

# Database configuration based on environment
if prod:
    # Production database (PostgreSQL)
    db_options = {}
    if ssl_mode := config("POSTGRES_SSL"):
        db_options = {"sslmode": ssl_mode}

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": config("POSTGRES_DATABASE"),
            "USER": config("POSTGRES_USERNAME"),
            "PASSWORD": config("POSTGRES_PASSWORD"),
            "HOST": config("POSTGRES_HOST"),
            "PORT": config("POSTGRES_PORT", default=5432),
            "OPTIONS": db_options,
        }
    }
else:
    # Development database (SQLite)
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATICFILES_DIRS = [BACKEND_DIR / "static"]
STATIC_ROOT = BACKEND_DIR / "staticfiles"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG",
    },
}

DJANGO_LOG_LEVEL = DEBUG
DEBUG_PROPAGATE_EXCEPTIONS = DEBUG  # Enables VS Code debugger to break on raised exceptions
