from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import coffees, health, shots, tastings, waters
from app.core.config import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name, version=settings.version)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Public healthcheck
    app.include_router(health.router)

    # Versioned API
    api_router = APIRouter(prefix=settings.api_v1_prefix)
    api_router.include_router(coffees.router)
    api_router.include_router(waters.router)
    api_router.include_router(shots.router)
    api_router.include_router(tastings.router)
    app.include_router(api_router)

    return app


app = create_app()
