"""Redis client for episodic/short-term cache during execution (T008)."""
from config import settings


def get_redis():
    """Return a Redis client (stub until connection pool is configured)."""
    try:
        import redis.asyncio as redis
        return redis.from_url(settings.redis_url)
    except Exception:
        return None
