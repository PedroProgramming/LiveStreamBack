from decouple import config

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": config("REDIS_URL", cast=str),
        "OPTIONS": {
            "SOCKET_TIMEOUT": 5,
            "IGNORE_EXCEPTIONS": True,
        }
    }
}