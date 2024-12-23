from .base import *

DEBUG = True
ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS', cast=lambda v: [item.strip() for item in v.split(',')]
)
CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS',
    cast=lambda v: [item.strip() for item in v.split(',')],
)


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
