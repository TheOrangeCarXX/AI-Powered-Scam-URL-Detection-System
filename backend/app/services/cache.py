import time

# Simple in-memory cache
_CACHE = {}
TTL_SECONDS = 60 * 30  # 30 minutes


def get_cached(domain: str):
    entry = _CACHE.get(domain)
    if not entry:
        return None

    value, timestamp = entry
    if time.time() - timestamp > TTL_SECONDS:
        _CACHE.pop(domain, None)
        return None

    return value


def set_cache(domain: str, value):
    _CACHE[domain] = (value, time.time())


def clear_cache():
    _CACHE.clear()
