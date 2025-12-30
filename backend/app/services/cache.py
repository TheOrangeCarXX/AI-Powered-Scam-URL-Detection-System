import time

# Simple in-memory cache with TTL for domain-related data
_CACHE = {}
TTL_SECONDS = 60 * 60 * 12   # 12 hours

# Cache structure: { domain: (value, timestamp) }
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

# Set or update cache entry
def set_cache(domain, value):
    print(f"[CACHE SET] {domain}")
    _CACHE[domain] = (value, time.time())

# Clear the entire cache
def clear_cache():
    _CACHE.clear()
    print("[CACHE CLEARED]")
