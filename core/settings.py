from decouple import config

ENVIRONMENT = config('DJANGO_CONFIG_MODULE', default='config.development')

if ENVIRONMENT == 'config.development':
    from config.development import *
elif ENVIRONMENT == 'config.production':
    from config.production import *
else:
    raise ValueError(
        f'Ambiente inválido para DJANGO_CONFIG_MODULE: {ENVIRONMENT}'
    )
