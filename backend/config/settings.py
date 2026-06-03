import os 
from pathlib import Path 
from dotenv import load_dotenv
from datetime import timedelta 
load_dotenv() 
BASE_DIR = Path(__file__).resolve().parent.parent 
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "fallback-dev-key") 
DEBUG = os.getenv("DJANGO_DEBUG", "True") == "True" 
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",") 
INSTALLED_APPS = [ 
"django.contrib.admin", 
"django.contrib.auth", 
"django.contrib.contenttypes", 
"django.contrib.sessions", 
"django.contrib.messages", 
"django.contrib.staticfiles", 
"rest_framework", 
"corsheaders", 
"api", 
] 

MIDDLEWARE = [ 
    "corsheaders.middleware.CorsMiddleware", 
    "django.middleware.security.SecurityMiddleware", 
    "whitenoise.middleware.WhiteNoiseMiddleware", 
    "django.contrib.sessions.middleware.SessionMiddleware", 
    "django.middleware.common.CommonMiddleware", 
    "django.middleware.csrf.CsrfViewMiddleware", 
    "django.contrib.auth.middleware.AuthenticationMiddleware", 
    "django.contrib.messages.middleware.MessageMiddleware", 
    "django.middleware.clickjacking.XFrameOptionsMiddleware", 
] 
 
ROOT_URLCONF = "config.urls" 
 
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
 
DATABASES = { 
    "default": { 
        "ENGINE": "django.db.backends.postgresql", 
        "NAME": os.getenv("DB_NAME"), 
        "USER": os.getenv("DB_USER"), 
        "PASSWORD": os.getenv("DB_PASSWORD"), 
        "HOST": os.getenv("DB_HOST", "localhost"), 
        "PORT": os.getenv("DB_PORT", "5432"), 
    } 
} 
 
AUTH_PASSWORD_VALIDATORS = [ 
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"}, 
] 
 
REST_FRAMEWORK = { 
    "DEFAULT_AUTHENTICATION_CLASSES": ( 
        "rest_framework_simplejwt.authentication.JWTAuthentication", 
), 
"DEFAULT_PERMISSION_CLASSES": ( 
"rest_framework.permissions.IsAuthenticated", 
), 
} 
SIMPLE_JWT = { 
"ACCESS_TOKEN_LIFETIME": timedelta(minutes=60), 
"REFRESH_TOKEN_LIFETIME": timedelta(days=7), 
"AUTH_HEADER_TYPES": ("Bearer",), 
} 
CORS_ALLOWED_ORIGINS = os.getenv( 
"CORS_ALLOWED_ORIGINS", "http://localhost:5173" 
).split(",") 
STATIC_URL = "/static/" 
STATIC_ROOT = BASE_DIR / "staticfiles" 
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage" 
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField" 
LANGUAGE_CODE = "en-us" 
TIME_ZONE = "Asia/Amman" 
USE_I18N = True 
USE_TZ = True 