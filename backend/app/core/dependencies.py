from functools import lru_cache

from app.services.repository import InMemoryRepository


@lru_cache
def get_repository() -> InMemoryRepository:
    """Provide a singleton in-memory repository."""
    return InMemoryRepository()
