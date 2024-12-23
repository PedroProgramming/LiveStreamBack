from decouple import config
from datetime import timedelta

# Auth
AUTH_USER_MODEL = 'users.User'

AUTHENTICATION_BACKENDS = ('users.backends.CustomBackend',)

SIGNING_KEY = config('SIGNING_KEY', cast=str)
ALGORITHM = config('ALGORITHM', cast=str)

SIMPLE_JWT = {
    'ALGORITHM': ALGORITHM,
    'SIGNING_KEY': SIGNING_KEY,
    'ACCESS_TOKEN_LIFETIME': timedelta(days=7),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=10),
    'BLACKLIST_AFTER_ROTATION': True,
    'ROTATE_REFRESH_TOKENS': True,
}
