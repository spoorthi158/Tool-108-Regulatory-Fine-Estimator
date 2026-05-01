import hashlib
import json
import logging

logger = logging.getLogger(__name__)

def get_cache_key(data: dict) -> str:
    """Generate a SHA256 cache key from input dictionary."""
    serialised = json.dumps(data, sort_keys=True)
    return hashlib.sha256(serialised.encode()).hexdigest()

def get_cached(redis_client, key: str) -> dict | None:
    """Retrieve cached value from Redis. Returns dict or None."""
    try:
        value = redis_client.get(key)
        if value:
            return json.loads(value)
    except Exception as e:
        logger.error(f"Cache get error: {e}")
    return None

def set_cached(redis_client, key: str, data: dict, ttl: int = 900) -> None:
    """Store value in Redis with TTL in seconds (default 15 minutes)."""
    try:
        redis_client.setex(key, ttl, json.dumps(data))
    except Exception as e:
        logger.error(f"Cache set error: {e}")