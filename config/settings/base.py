import os
from datetime import timedelta
from pathlib import Path
from typing import Any, Dict, List

import environ

env = environ.Env(DEBUG=(bool, False))


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# environ.Env.read_env()
env_path = os.path.join(BASE_DIR, "envs/.env.local")
if os.path.exists(env_path):
    environ.Env.read_env(env_path)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")
ALLOWED_HOSTS: list[str] = ["*"]

# Application definition
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "apps.shared",
]

THIRD_PARTY = [
    "rest_framework",
    "drf_spectacular",
    "rest_framework_simplejwt",
]

OWN_APPS = [
    "apps.users",
]

BASE_INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY + OWN_APPS


SPECTACULAR_SETTINGS = {
    "TITLE": "WeShare API",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"


# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:3000",
#     "https://weshare.com",
# ]
#
# CORS_ALLOW_CREDENTIALS = True

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "config.wsgi.application"


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_TZ = True

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK: Dict[str, Any] = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
        "rest_framework.permissions.AllowAny",
    ],
    # "DEFAULT_AUTHENTICATION_CLASSES": [
    #     "rest_framework.authentication.BasicAuthentication",
    #     "rest_framework.authentication.SessionAuthentication",
    # ],
}

# NCP_STORAGE = {
#     "ACCESS_KEY": env("NCP_ACCESS_KEY"),
#     "SECRET_KEY": env("NCP_SECRET_KEY"),
#     "BUCKET_NAME": "sharing_photos",
#     "ENDPOINT_URL": "https://kr.object.ncloudstorage.com",
# }
#
# SIMPLE_JWT = {
#     "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
#     "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
#     "ROTATE_REFRESH_TOKENS": False,
#     "BLACKLIST_AFTER_ROTATION": True,
# }
