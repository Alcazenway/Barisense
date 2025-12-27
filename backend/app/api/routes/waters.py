from fastapi import APIRouter, Depends, status

from app.core.dependencies import get_repository
from app.models.schemas import Water, WaterCreate
from app.services.repository import InMemoryRepository

router = APIRouter(prefix="/waters", tags=["eaux"])


@router.get("", response_model=list[Water], summary="Lister les eaux disponibles")
def list_waters(repository: InMemoryRepository = Depends(get_repository)) -> list[Water]:
    return list(repository.list_waters())


@router.post(
    "",
    response_model=Water,
    status_code=status.HTTP_201_CREATED,
    summary="Déclarer une eau",
)
def create_water(
    payload: WaterCreate, repository: InMemoryRepository = Depends(get_repository)
) -> Water:
    return repository.add_water(payload)
