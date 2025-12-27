from functools import lru_cache

from fastapi import Depends, Header, HTTPException, Request, status

from app.core.config import get_settings
from app.services.repository import Repository


@lru_cache
def get_repository() -> Repository:
    """Provide a shared in-memory repository."""
    return Repository()


def require_api_key(request: Request, x_api_key: str | None = Header(default=None)) -> None:
    """Basic API-key style authentication when BARISENSE_API_KEY is set."""
    settings = get_settings()
    if settings.api_key is None:
        return
    provided = request.headers.get(settings.api_key_header) or x_api_key
    if provided != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Clé API manquante ou invalide",
        )
