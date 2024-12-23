import os, sys
from pathlib import Path
from decouple import config

from .auth import *
from .middlewares import *
from .cache import CACHES
from .templates_and_passwords import TEMPLATES, AUTH_PASSWORD_VALIDATORS

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../apps'))

SECRET_KEY = config('SECRET_KEY', cast=str)

INSTALLED_APPS = [
    # Django Apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Core Apps
    'users',
    'videos',
    'channel',
    'LiveStream',
    'authentication',

    # JWT Authentication
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',

    # Third-party Apps
    'corsheaders',
    'django_celery_beat',
    'django_celery_results',
]

ROOT_URLCONF = 'core.urls'

WSGI_APPLICATION = 'core.wsgi.application'

# Language
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static
STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Celery
CELERY_BROKER_URL = config("REDIS_CELERY_URL", cast=str)
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULTS_BACKEND = 'django-db'
CELERY_TIMEZONE = TIME_ZONE

# Celery Beat
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'