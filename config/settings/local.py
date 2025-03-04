from dotenv import dotenv_values

from config.settings.base import *

INSTALLED_APPS = BASE_INSTALLED_APPS

ENV = dotenv_values(BASE_DIR / "envs/.env.local")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ENV.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

NCP_STORAGE_ENDPOINT = ENV.get("NCP_STORAGE_ENDPOINT")
NCP_STORAGE_BUCKET_NAME = ENV.get("NCP_STORAGE_BUCKET_NAME")
NCP_ACCESS_KEY_ID = ENV.get("NCP_ACCESS_KEY_ID")
NCP_SECRET_ACCESS_KEY = ENV.get("NCP_SECRET_ACCESS_KEY")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": ENV.get("POSTGRES_HOST"),
        "NAME": ENV.get("POSTGRES_DBNAME"),
        "USER": ENV.get("POSTGRES_USER"),
        "PASSWORD": ENV.get("POSTGRES_PASSWORD"),
        "PORT": ENV.get("POSTGRES_PORT"),
        "OPTIONS": {
            "options": "-c search_path=weshare" # 로컬 테스트 시 public 으로 수정
        },
    }
}

SWAGGER_SETTINGS = {
    "USE_SESSION_AUTH": False,
    "DEFAULT_API_URL": "http://175.45.203.70:8000/",  # HTTPS URL로 명시
    "SECURITY_DEFINITIONS": {
        "Bearer": {  # JWT 인증 방식 정의
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": 'JWT Authorization header using the Bearer scheme. Example: "Authorization: Bearer {token}"',
        },
    },
}

# Static files (CSS, JavaScript, Images)
STATIC_URL = "static/"

NAVER_CLIENT_ID = ENV.get("NAVER_CLIENT_ID")
NAVER_SECRET = ENV.get("NAVER_CLIENT_SECRET")
NAVER_REDIRECT_URI = ENV.get("NAVER_REDIRECT_URI")

KAKAO_CLIENT_ID = ENV.get("KAKAO_CLIENT_ID")
KAKAO_SECRET = ENV.get("KAKAO_CLIENT_SECRET")
KAKAO_REDIRECT_URI = ENV.get("KAKAO_REDIRECT_URI")
