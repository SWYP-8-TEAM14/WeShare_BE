from dotenv import dotenv_values

from config.settings.base import *

INSTALLED_APPS = BASE_INSTALLED_APPS

ENV = dotenv_values(BASE_DIR / "envs/.env.local")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ENV.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": ENV.get("POSTGRES_HOST", "localhost"),
        "NAME": ENV.get("POSTGRES_DBNAME", "weshare"),
        "USER": ENV.get("POSTGRES_USER", "hwangjiwon"),
        "PASSWORD": ENV.get("POSTGRES_PASSWORD", "900326"),
        "PORT": ENV.get("POSTGRES_PORT", 5432),
    }
}

# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"

NAVER_CLIENT_ID = ENV.get("NAVER_CLIENT_ID")
NAVER_SECRET = ENV.get("NAVER_CLIENT_SECRET")
NAVER_REDIRECT_URI = ENV.get("NAVER_REDIRECT_URI")
