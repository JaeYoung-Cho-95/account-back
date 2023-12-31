from pathlib import Path
from .secret import SECRET_KEY, DATABASES
from .settings_detail import set_logging, set_restframework, set_simplejwt, set_aws_s3

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = SECRET_KEY
DATABASES = DATABASES
AUTH_USER_MODEL = "accounts.User"

# FIXME : 배포시에는 False, 개발시에는 True
DEBUG = True

if DEBUG:
    ALLOWED_HOSTS = ["backend-django", "0.0.0.0", "localhost"]
else:
    ALLOWED_HOSTS = [
        "account-book.store",
        "www.account-book.store",
        "0.0.0.0",
        "localhost",
    ]

# Application definition

INSTALLED_APPS = [
    # loacl apps
    "accounts",
    "budget",
    "chart",
    "crawling",
    
    # django third party apps
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "corsheaders",
    "storages",
    "background_task",
    
    # django main apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]


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

# CORS 관련 설정

# FIXME : 실 운영서비스 사용시에는 CSRF None 말고 도메인 정확하게 지정하기
# CSRF_COOKIE_DOMAIN = '.account-book.store'
CORS_ALLOW_ALL_ORIGINS = True
CSRF_COOKIE_DOMAIN = None
CORS_ALLOW_CREDENTIALS = True

SIMPLE_JWT = set_simplejwt.SIMPLE_JWT
REST_FRAMEWORK = set_restframework.REST_FRAMEWORK
LOGGING = set_logging.LOGGING


# S3 Storages
AWS_ACCESS_KEY_ID = set_aws_s3.AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = set_aws_s3.AWS_SECRET_ACCESS_KEY
AWS_REGION = set_aws_s3.AWS_REGION

AWS_STORAGE_BUCKET_NAME = set_aws_s3.AWS_STORAGE_BUCKET_NAME
AWS_S3_CUSTOM_DOMAIN = '%s.s3.%s.amazonaws.com' % (AWS_STORAGE_BUCKET_NAME, AWS_REGION)
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'