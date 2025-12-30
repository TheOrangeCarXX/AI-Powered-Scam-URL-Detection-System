import time

_CACHE = {}
TTL_SECONDS = 60 * 30  # 30 minutes


def get_cached(domain):
    entry = _CACHE.get(domain)
    if not entry:
        return None

    value, ts = entry
    if time.time() - ts > TTL_SECONDS:
        _CACHE.pop(domain, None)
        return None

    print(f"[CACHE HIT] {domain}")
    return value


def set_cache(domain, value):
    print(f"[CACHE SET] {domain}")
    _CACHE[domain] = (value, time.time())


def clear_cache():
    _CACHE.clear()
    print("[CACHE CLEARED]")
