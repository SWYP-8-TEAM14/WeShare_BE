import os
from datetime import timedelta
from pathlib import Path
from typing import Any, Dict, List

import environ
from django.conf.global_settings import AUTH_USER_MODEL

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
    "corsheaders",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "apps.shared",
    "sslserver",
]

THIRD_PARTY = [
    "rest_framework",
    "rest_framework_simplejwt",
    "drf_spectacular",
]

OWN_APPS = [
    "apps.users",
    "apps.groups",
]

BASE_INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY + OWN_APPS

AUTH_USER_MODEL = "auth.User"


SPECTACULAR_SETTINGS = {
    "TITLE": "WeShare API",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

SECURE_CROSS_ORIGIN_OPENER_POLICY = None
# CORS_ALLOW_ALL_ORIGINS = True
CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOWED_ORIGINS = [
    "https://kauth.kakao.com",
    "http://127.0.0.1:8000",
    "http://localhost:8000",
    # "http://localhost:3000",
    # "https://weshare.com",
    "http://175.45.203.70:8000",
    "http://54.180.87.253",
    "http://54.180.87.253:80"
]

CORS_ALLOW_CREDENTIALS = True

# CSRF_TRUSTED_ORIGINS = ["https://kauth.kakao.com", "http://127.0.0.1:8000", "http://localhost:8000", "http://175.45.203.70:8000", "http://54.180.87.253:80"]

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
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
        "rest_framework.permissions.AllowAny",
    ],
}

AUTHENTICATION_BACKENDS = [
    "apps.users.auth_backends.EmailBackend",
    "django.contrib.auth.backends.ModelBackend",  # 기본 인증 방식
]


# NCP_STORAGE = {
#     "ACCESS_KEY": env("NCP_ACCESS_KEY"),
#     "SECRET_KEY": env("NCP_SECRET_KEY"),
#     "BUCKET_NAME": "sharing_photos",
#     "ENDPOINT_URL": "https://kr.object.ncloudstorage.com",
# }
#
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": env("SECRET_KEY"),
}
