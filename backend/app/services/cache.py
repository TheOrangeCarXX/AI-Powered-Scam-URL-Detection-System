import time

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

    print(f"[CACHE HIT] {domain}")
    return value


def set_cache(domain: str, value: dict):
    print(f"[CACHE SET] {domain}")
    _CACHE[domain] = (value, time.time())


def clear_cache():
    _CACHE.clear()
