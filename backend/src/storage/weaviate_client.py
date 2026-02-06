"""Weaviate client for semantic memory and RAG (T007).

Configure with WEAVIATE_URL and WEAVIATE_API_KEY.
Schema and collections to be added when Planner/Judge use semantic context.
"""
from config import settings


def get_client():
    """Return a Weaviate client instance; None if not configured or unavailable."""
    _ = settings.weaviate_url
    try:
        import weaviate
        return weaviate.Client(url=settings.weaviate_url) if settings.weaviate_url else None
    except Exception:
        return None
