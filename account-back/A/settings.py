from pathlib import Path
from .secret import SECRET_KEY, DATABASES
from .settings_detail import set_logging, set_restframework, set_simplejwt

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = SECRET_KEY
DATABASES = DATABASES
AUTH_USER_MODEL = "accounts.User"

# FIXME : 배포시에는 False, 개발시에는 True
DEBUG = False

if DEBUG:
    ALLOWED_HOSTS = ["backend-django", "0.0.0.0", "localhost"]
else:
    ALLOWED_HOSTS = ["account-book.store", "www.account-book.store", "0.0.0.0", "localhost"]

# Application definition

INSTALLED_APPS = [
    # loacl apps
    "accounts",
    # django third party apps
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "corsheaders",
    # django main apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]


# CORS 관련 설정
# CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True


MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "A.urls"

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

WSGI_APPLICATION = "A.wsgi.application"

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

from datetime import timedelta
from A.secret import SECRET_KEY

SESSION_COOKIE_DOMAIN = '.account-book.store'

SIMPLE_JWT = set_simplejwt.SIMPLE_JWT
REST_FRAMEWORK = set_restframework.REST_FRAMEWORK
LOGGING = set_logging.LOGGING
