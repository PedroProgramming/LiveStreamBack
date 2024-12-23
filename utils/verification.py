from typing import Tuple
from datetime import timedelta
from django.http import HttpRequest
from django.core.cache import cache

def check_rate_limit_status(request: HttpRequest, limit: int = 10) -> Tuple[int, dict]:
    ip_key = f"rl:ip:{request.META["REMOTE_ADDR"]}:{limit}/h"
    count = cache.get(ip_key)

    if count is None:
        cache.set(ip_key, 1, timeout=timedelta(hours=1).total_seconds())
        count = 1
    else:
        cache.incr(ip_key, 1)

    remaining = limit - int(count)
    
    if remaining <= 0:
        return 429, {"error": "Rate limit exceeded. Try again later"}
    return 200, {'message': 'Request successful.'}