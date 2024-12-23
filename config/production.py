from .base import *


# TODO Trocar informações para produção

DEBUG = False
ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS', cast=lambda v: [item.strip() for item in v.split(',')]
)
CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS',
    cast=lambda v: [item.strip() for item in v.split(',')],
)

DATABASES = {
    'default': {
        'ENGINE': config('ENGINE', cast=str),
        'NAME': config('DB_NAME', cast=str),
        'USER': config('DB_USER', cast=str),
        'PASSWORD': config('DB_PASSWORD', cast=str),
        'HOST': config('DB_HOST', cast=str),
        'PORT': config('DB_PORT', cast=int),
    }
}

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'