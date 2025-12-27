from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import get_repository, require_api_key
from app.models.schemas import WaterCreate, WaterRead
from app.services.repository import Repository

router = APIRouter(prefix="/waters", tags=["eaux"], dependencies=[Depends(require_api_key)])


@router.get("", response_model=list[WaterRead], summary="Lister les eaux disponibles")
def list_waters(repository: Repository = Depends(get_repository)) -> list[WaterRead]:
    return [WaterRead.model_validate(water) for water in repository.list_waters()]


@router.get("/{water_id}", response_model=WaterRead, summary="Récupérer une eau")
def get_water(water_id: UUID, repository: Repository = Depends(get_repository)) -> WaterRead:
    water = repository.get_water(water_id)
    if not water:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Eau introuvable")
    return WaterRead.model_validate(water)


@router.post(
    "",
    response_model=WaterRead,
    status_code=status.HTTP_201_CREATED,
    summary="Déclarer une eau",
)
def create_water(
    payload: WaterCreate, repository: Repository = Depends(get_repository)
) -> WaterRead:
    created = repository.upsert_water(payload)
    return WaterRead.model_validate(created)


@router.put(
    "/{water_id}",
    response_model=WaterRead,
    summary="Mettre à jour une eau",
)
def update_water(
    water_id: UUID, payload: WaterCreate, repository: Repository = Depends(get_repository)
) -> WaterRead:
    if not repository.get_water(water_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Eau introuvable")
    updated = repository.upsert_water(payload, water_id=water_id)
    return WaterRead.model_validate(updated)


@router.delete(
    "/{water_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Supprimer une eau",
)
def delete_water(water_id: UUID, repository: Repository = Depends(get_repository)) -> None:
    if not repository.get_water(water_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Eau introuvable")
    repository.delete_water(water_id)
