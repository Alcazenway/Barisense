from fastapi import APIRouter

from app.core.config import get_settings

router = APIRouter(tags=["health"])


@router.get("/health", summary="Vérification de disponibilité")
def healthcheck() -> dict[str, str]:
    """Return app metadata to quickly validate deployment."""
    settings = get_settings()
    return {"status": "ok", "app": settings.app_name, "version": settings.version}
